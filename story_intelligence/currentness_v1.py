"""Pure SI domain dependency freshness under R1/R1a and approved G01/G02.

Observations are caller-supplied, not trusted authority. CURRENT certifies neither
execution, facts, eligibility, identity, rights nor production readiness. No I/O.
"""
from .codec_v1 import canonical_si_json
from .model_v1 import SIValidationError, validate_si_ref
from .provenance_v1 import verify_si_provenance
from .records_v1 import _SCHEMAS

__all__ = ['check_si_currentness']

_NON_DOMAIN = frozenset(('RunRecord', 'Selection', 'ReviewPacket'))


def _key(ref):
    return (ref['type'], ref['id'], ref['revision'], ref['sha256'])


def _identity(ref):
    return (ref['type'], ref['id'])


def _fail(code, path, message):
    raise SIValidationError(code, path, message)


def _ref(value, path):
    try:
        return validate_si_ref(value)
    except SIValidationError as error:
        raise SIValidationError(error.code, path + error.path[1:], str(error)) from error


def _observed(values, path, heads=False):
    if type(values) is not list:
        _fail('TYPE', path, 'Expected finite plain list of exact SIRefs')
    checked, seen = [], set()
    for i, value in enumerate(values):
        current = f'{path}[{i}]'
        ref = _ref(value, current)
        if (heads and ref['type'] != 'Selection') or (not heads and ref['type'] in _NON_DOMAIN):
            _fail('REF_TYPE_MISMATCH', current + '.type', 'Wrong observed reference role')
        identity = _identity(ref)
        if identity in seen:
            _fail('SELECTION_CONFLICT' if heads else 'TYPE', current,
                  'Duplicate or conflicting observed identity; no version selection')
        seen.add(identity)
        checked.append(ref)
    return checked


def _payload_refs(record):
    """Yield typed SI/E refs and schema paths, including Known/list nesting.

    Read-only dependency on the accepted schema vocabulary, as in the resolver.
    No ref-like dictionary detection or text parsing; future tags fail closed.
    """
    stack = [(record['payload'], _SCHEMAS[record['H']['type']], '$.payload')]
    while stack:
        value, schema, path = stack.pop()
        tag = schema[0]
        if tag in ('ref', 'eref'):
            yield tag, value, path
        elif tag == 'object':
            for field, child in reversed(tuple(schema[1].items())):
                stack.append((value[field], child, path + '.' + field))
        elif tag == 'list':
            for i in range(len(value) - 1, -1, -1):
                stack.append((value[i], schema[1], f'{path}[{i}]'))
        elif tag == 'nullable':
            if value is not None:
                stack.append((value, schema[1], path))
        elif tag == 'known':
            if value['state'] == 'KNOWN':
                stack.append((value['value'], schema[1], path + '.value'))
        elif tag not in ('text', 'hash', 'utc', 'bool', 'true', 'enum', 'int'):
            _fail('VERSION_UNSUPPORTED', path, 'Unsupported accepted schema tag')


def _result(state, codes=()):
    return {'currentness':state, 'reason_codes':sorted(set(codes))}


def check_si_currentness(records, root, observed_active_input_refs, observed_selection_head_refs):
    """Return detached {currentness, reason_codes}; never mutate supplied values.

    root: one exact domain SIRef (not RunRecord/Selection/ReviewPacket). Observed
    arguments: finite plain lists, active domain refs and Selection refs. Shape,
    wrong-role and duplicate identity errors raise SIValidationError with exact
    $.root / $.observed_*[i] paths (TYPE, REF_TYPE_MISMATCH, SELECTION_CONFLICT or
    the accepted ref validator's code). A non-list records argument raises TYPE
    at $.records. Inputs must remain stable during the call.

    All records retain accepted local validation, including unrelated records;
    root AND observed refs are audit/provenance verified, with no latest fallback.
    Graph/provenance errors return INVALID with the accepted exception code, not
    STALE. Conflicting resolved selection scopes return INVALID/SELECTION_CONFLICT.
    The minimal result contains codes, not graph-error paths; the accepted exact
    resolver/provenance APIs provide those paths when inspecting invalid bundles.

    Valid missing/replaced active dependencies or incompatible frozen Creative
    evaluation bindings return STALE/INPUT_STALE. Relevant typed ERefs (including
    substantive record/producer H.editorial_refs) return INVALID/REF_MISSING: this
    API has no validated editorial snapshot argument. INVALID precedes STALE.
    Root membership itself is not a prerequisite: freshness compares dependencies,
    not whether this output was selected. Ordering of observed lists is irrelevant.
    """
    if type(records) is not list:
        _fail('TYPE', '$.records', 'Expected finite plain list of complete SI records')
    root = _ref(root, '$.root')
    if root['type'] in _NON_DOMAIN:
        _fail('REF_TYPE_MISMATCH', '$.root.type', 'Expected domain record, not metadata/projection')
    active = _observed(observed_active_input_refs, '$.observed_active_input_refs')
    heads = _observed(observed_selection_head_refs, '$.observed_selection_head_refs', True)
    try:
        verify_si_provenance(records, [root] + active + heads)
        # Only after exact graph verification may the local index be trusted.
        index = {(v['H']['type'], v['H']['id'], v['H']['revision']):v for v in records}

        def lookup(ref):
            return index[(ref['type'], ref['id'], ref['revision'])]

        scopes = set()
        for ref in heads:
            scope = canonical_si_json(lookup(ref)['payload']['scope'])
            if scope in scopes:
                return _result('INVALID', ['SELECTION_CONFLICT'])
            scopes.add(scope)

        required, selected, visited = set(), set(), set()
        pending = [root]
        incompatible = False
        while pending:
            ref = pending.pop()
            exact = _key(ref)
            if exact in visited:
                continue
            visited.add(exact)
            record = lookup(ref)
            h, p = record['H'], record['payload']
            kind = h['type']
            if h['editorial_refs']:
                return _result('INVALID', ['REF_MISSING'])

            def dependency(child):
                if child['type'] == 'Selection':
                    selected.add(_key(child))
                elif child['type'] == 'ReviewPacket':
                    # R1: terminal discussion artifacts cannot become domain inputs.
                    _fail('REF_TYPE_MISMATCH', '$.payload', 'Packet is not a domain input')
                elif child['type'] != 'RunRecord':
                    required.add(_key(child))
                pending.append(child)

            if kind == 'RunRecord':
                # Explicit substantive Run refs are transparent, never active
                # metadata identities. Snapshots/context/previous are not edges.
                roots = p['semantic_input_refs']
                for child in roots[1:] if p['stage'] == 'REVISION' else roots:
                    dependency(child)
                continue

            for tag, child, path in _payload_refs(record):
                if tag == 'eref':
                    return _result('INVALID', ['REF_MISSING'])
                if path == '$.payload.run_ref' and kind in ('CreativeAlternative', 'EvaluationReport'):
                    continue
                dependency(child)

            producer = h['origin']['run_ref']
            if kind == 'CreativeAlternative':
                producer = p['run_ref']  # original C, not actual REVISION metadata
            if producer is None:
                continue
            run = lookup(producer)
            rp = run['payload']
            if h['origin']['mode'] == 'HUMAN_EDIT' and kind != 'CreativeAlternative':
                # Accepted provenance certified base-first + exact current payload.
                # Current payload was visited above; no historical base traversal.
                continue
            if run['H']['editorial_refs']:
                return _result('INVALID', ['REF_MISSING'])
            original_angle = None
            if kind == 'CreativeAlternative':
                genesis = record
                while genesis['H']['previous'] is not None:
                    genesis = lookup(genesis['H']['previous'])
                original_angle = genesis['payload']['angle_ref']
            for child in rp['semantic_input_refs']:
                if child == h['previous']:
                    continue  # causal base of an assembled revision, not content
                if kind == 'CreativeAlternative' and child == original_angle:
                    # G01: the current payload explicitly controls the Angle role.
                    # Frozen E1 still contributes its own exact evaluated Angle.
                    continue
                dependency(child)  # G02: every direct C ClaimItem retained
                if kind == 'CreativeAlternative' and child['type'] == 'EvaluationReport':
                    ep = lookup(child)['payload']
                    ap = lookup(p['angle_ref'])['payload']
                    if (ep['angle_ref'] != p['angle_ref'] or ep['idea_ref'] != ap['idea_ref'] or
                            ep['audience_ref'] != ap['audience_ref']):
                        incompatible = True

        active_keys = {_key(ref) for ref in active}
        head_keys = {_key(ref) for ref in heads}
        if incompatible or not required.issubset(active_keys) or not selected.issubset(head_keys):
            return _result('STALE', ['INPUT_STALE'])
        return _result('CURRENT')
    except SIValidationError as error:
        return _result('INVALID', [error.code])
