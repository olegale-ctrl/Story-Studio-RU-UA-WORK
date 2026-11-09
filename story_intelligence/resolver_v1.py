"""Read-only closed-bundle SI/1 resolution, audit DAG and exact Run snapshots.

APIs accept exact plain lists, with no new bundle count/byte cap. Every supplied
record is locally validated; only root-reachable records are graph-certified.
Both public APIs verify the complete reachable audit graph. No ERef resolution,
semantic currentness, stage/output certification, authority, I/O or mutable cache.
"""
from copy import deepcopy

from .codec_v1 import canonical_si_json
from .model_v1 import SIValidationError, validate_si_ref
from .records_v1 import validate_si_record, si_record_ref, _SCHEMAS

__all__ = ['resolve_si_closure', 'resolve_si_record']


def _fail(code, path, message):
    raise SIValidationError(code, path, message)


def _at(check, value, path):
    try:
        return check(value)
    except SIValidationError as error:
        raise SIValidationError(error.code, path + error.path[1:], str(error)) from error


def _identity(ref):
    return (ref['type'], ref['id'], ref['revision'])


def _sort_key(ref):
    return (*_identity(ref), ref['sha256'])


def _direct_refs(record, path):
    """Typed paths only; accepted schema tags, never dictionary-shape heuristics.

    _SCHEMAS is a read-only dependency on the accepted schema vocabulary. No edits
    or mutations to that module. Origin/H SIRefs are enumerated explicitly.
    """
    h = record['H']
    if h['previous'] is not None:
        yield h['previous'], path + '.H.previous'
    if h['origin']['run_ref'] is not None:
        yield h['origin']['run_ref'], path + '.H.origin.run_ref'
    for i, ref in enumerate(h['input_refs']):
        yield ref, f'{path}.H.input_refs[{i}]'
    stack = [(record['payload'], _SCHEMAS[h['type']], path + '.payload')]
    while stack:
        value, schema, current = stack.pop()
        tag = schema[0]
        if tag == 'ref':
            yield value, current
        elif tag == 'object':
            for key, child in reversed(tuple(schema[1].items())):
                stack.append((value[key], child, current + '.' + key))
        elif tag == 'list':
            for i in range(len(value) - 1, -1, -1):
                stack.append((value[i], schema[1], f'{current}[{i}]'))
        elif tag == 'nullable':
            if value is not None:
                stack.append((value, schema[1], current))
        elif tag == 'known':
            if value['state'] == 'KNOWN':
                stack.append((value['value'], schema[1], current + '.value'))
        elif tag not in ('eref', 'text', 'hash', 'utc', 'bool', 'true', 'enum', 'int'):
            # A future schema extension must not silently omit graph edges.
            _fail('VERSION_UNSUPPORTED', current, 'Unsupported accepted schema tag')


def _index(records):
    if type(records) is not list:
        _fail('TYPE', '$.records', 'Expected finite plain list of complete SI records')
    index, id_types = {}, {}
    for i, value in enumerate(records):
        path = f'$.records[{i}]'
        record = _at(validate_si_record, value, path)
        ref = _at(si_record_ref, record, path)
        key = _identity(ref)
        if key in index:
            if (index[key]['ref']['sha256'] != ref['sha256'] or
                    canonical_si_json(index[key]['record']) != canonical_si_json(record)):
                _fail('REF_HASH_MISMATCH', path, 'Conflicting bytes for one record identity')
            _fail('TYPE', path, 'Duplicate identical canonical record in bundle')
        index[key] = {'record':record, 'ref':ref, 'path':path,
                      'edges':tuple(_direct_refs(record, path))}
        id_types.setdefault((ref['id'], ref['revision']), set()).add(ref['type'])
    return index, id_types


def _lookup(index, id_types, ref, path):
    key = _identity(ref)
    if key not in index:
        if (ref['id'], ref['revision']) in id_types:
            _fail('REF_TYPE_MISMATCH', path + '.type', 'Only other record types supplied for this id/revision')
        _fail('REF_MISSING', path, 'Exact record identity missing (no latest fallback)')
    return key


def _walk(index, id_types, roots):
    """Iterative identity-DAG preflight followed by exact edge-hash checks.

    A cycle cannot in general have self-consistent content-addressed SHA refs.
    Detect explicit identity cycles before edge-hash mismatches: negative cycle
    fixtures need not pretend to solve SHA fixed points. Root hashes are verified
    first. No result is returned unless every reachable edge hash also matches.
    """
    root_keys = []
    for ref, path in roots:
        key = _lookup(index, id_types, ref, path)
        if index[key]['ref']['sha256'] != ref['sha256']:
            _fail('REF_HASH_MISMATCH', path + '.sha256', 'Root bytes differ from exact SIRef')
        root_keys.append(key)
    colors, edges_to_verify = {}, []
    for root in root_keys:
        if colors.get(root) == 2:
            continue
        colors[root] = 1
        stack = [(root, iter(index[root]['edges']))]
        while stack:
            key, children = stack[-1]
            try:
                ref, path = next(children)
            except StopIteration:
                colors[key] = 2
                stack.pop()
                continue
            child = _lookup(index, id_types, ref, path)
            edges_to_verify.append((child, ref, path))
            if colors.get(child) == 1:
                _fail('DEPENDENCY_CYCLE', path, 'Typed SIRef edge closes an identity cycle')
            if colors.get(child) != 2:
                colors[child] = 1
                stack.append((child, iter(index[child]['edges'])))
    for key, expected, path in edges_to_verify:
        if index[key]['ref']['sha256'] != expected['sha256']:
            _fail('REF_HASH_MISMATCH', path + '.sha256', 'Referenced bytes differ from exact SIRef')
    return set(colors), root_keys


def _reachable(index, root_keys):
    """Closure within an already verified DAG; no Python graph recursion."""
    found, stack = set(), list(root_keys)
    while stack:
        key = stack.pop()
        if key in found:
            continue
        found.add(key)
        stack.extend(_identity(ref) for ref, _ in index[key]['edges'])
    return found


def _manifest(index, keys):
    return [deepcopy(ref) for ref in sorted((index[k]['ref'] for k in keys), key=_sort_key)]


def _verify_snapshots(index, reachable):
    for key in sorted(reachable):
        entry = index[key]
        if entry['record']['H']['type'] != 'RunRecord':
            continue
        p = entry['record']['payload']
        context = p['context_snapshot']
        roots = p['semantic_input_refs'] + context['active_input_refs'] + context['selection_head_refs']
        expected = _manifest(index, _reachable(index, [_identity(r) for r in roots]))
        if p['input_snapshot'] != expected:
            _fail('PROVENANCE_MISMATCH', entry['path'] + '.payload.input_snapshot',
                  'Run snapshot is not exact canonical transitive Closure of declared roots')


def _resolve(records, roots):
    index, id_types = _index(records)
    reachable, root_keys = _walk(index, id_types, roots)
    _verify_snapshots(index, reachable)
    return index, reachable, root_keys


def resolve_si_closure(records, roots):
    """Detached canonical audit Closure; ERefs are shape-checked, not resolved.

    Duplicate exact roots are permitted (set-valued Closure). Identical duplicate
    bundle records are rejected TYPE; conflicting identities REF_HASH_MISMATCH.
    Structurally invalid unrelated records also fail bundle validation; unrelated
    valid records are not included or transitively certified. No bundle-size cap.
    """
    if type(roots) is not list:
        _fail('TYPE', '$.roots', 'Expected finite plain list of exact SIRefs')
    checked = [(_at(validate_si_ref, ref, f'$.roots[{i}]'), f'$.roots[{i}]')
               for i, ref in enumerate(roots)]
    index, reachable, _ = _resolve(records, checked)
    return _manifest(index, reachable)


def resolve_si_record(records, expected_ref):
    """Return detached exact record after verifying its full reachable audit DAG.

    The supplied bundle is the only source. No implicit latest, ERef adapter,
    external material, editorial authority or semantic currentness is inferred.
    """
    ref = _at(validate_si_ref, expected_ref, '$.expected_ref')
    index, _, roots = _resolve(records, [(ref, '$.expected_ref')])
    return deepcopy(index[roots[0]]['record'])
