"""Bounded, no-request SI evaluation over explicit untrusted local values.

Checks recorded consistency, never actual execution, identity, truth, rights or
production permission. No clock, randomness, I/O, cache, writer or provider.
Accepted SI modules are reused read-only, including their closed schema grammar.
"""
from copy import deepcopy

from .codec_v1 import canonical_si_json, canonical_si_sha256
from .model_v1 import SIValidationError
from .records_v1 import (validate_si_record, _check, _context, _RATING, _CONTEXT)
from .provenance_v1 import verify_si_provenance
from .currentness_v1 import check_si_currentness, _payload_refs, _observed

__all__ = ['evaluate_si']

_CRITERIA = (('audience_interest', 15), ('channel_fit', 10), ('angle_novelty', 10),
             ('evidence_quality', 20), ('narrative_potential', 15),
             ('visual_feasibility', 10), ('resource_fit', 10),
             ('risk_manageability', 5), ('portfolio_distinctness', 5))
_NON_DOMAIN = frozenset(('RunRecord', 'Selection', 'ReviewPacket'))
_ORDER = {'BLOCKED': 0, 'NEEDS_INPUT': 1, 'NEEDS_RESEARCH': 2, 'REVIEW_DUPLICATE': 3}
_P = '$.required_current_premise'
_H = '$.human_findings'
_TEXT, _HASH, _UTC = ('text',), ('hash',), ('utc',)


def _obj(**fields): return ('object', fields)
def _list(child): return ('list', child)
def _known(child): return ('known', child)
def _ref(*types): return ('ref', types)
def _enum(*values): return ('enum', values)


_BINDING = _obj(idea_ref=_ref('StoryIdea'), angle_ref=_ref('Angle'),
    audience_ref=_ref('AudienceHypothesis'), channel_ref=_ref('ChannelContext'),
    rubric_ref=_ref('Rubric'), semantic_input_refs=_list(_ref()),
    context_snapshot=_CONTEXT, ratings_sha256=_HASH)
_CONFIDENCE = _obj(binding_sha256=_HASH, criterion_key=_TEXT, rating_sha256=_HASH,
    outcome=_enum('SUFFICIENT', 'INSUFFICIENT'), reason=_TEXT)
_DUPLICATE = _obj(binding_sha256=_HASH, portfolio_entry_index=('int', 0, None),
    portfolio_entry_sha256=_HASH, candidate_ref=_ref('StoryIdea', 'ProductionBrief'),
    outcome=_enum('DISTINCT', 'DUPLICATE', 'UNRESOLVED'), reason=_TEXT)
_FINDINGS = _obj(contract_tag=_TEXT, binding=_BINDING,
    confidence_findings=_list(_CONFIDENCE), duplicate_findings=_list(_DUPLICATE))
_PERIOD = _obj(from_utc=_UTC, to_utc=_UTC)
_REQUIREMENT = _obj(source_ref=_ref('SourceItem'), specification=_known(_TEXT),
    period=_known(_PERIOD))
_PROOF = _obj(evidence_ref=_ref('EvidenceItem'), check_ref=_ref('ClaimCheck'),
    material_ref=_ref('SourceItem'), material_sha256=_HASH, coverage=_PERIOD)
_FRESHNESS = _obj(binding_sha256=_HASH, requirements_sha256=_HASH,
    source_ref=_ref('SourceItem'),
    applicability=_enum('APPLICABLE', 'NOT_APPLICABLE', 'UNDETERMINED'),
    review_period=_known(_PERIOD), outcome=_enum('ESTABLISHED', 'INSUFFICIENT', 'UNKNOWN'),
    evidence=_list(_PROOF), reason=_TEXT)
_PREMISE = _obj(contract_tag=_TEXT, binding=_BINDING,
    determination=_enum('REQUIRED', 'NOT_REQUIRED', 'UNDETERMINED'),
    required_data=_known(_list(_REQUIREMENT)), source_freshness=_list(_FRESHNESS))


class _Failure(SIValidationError):
    def __init__(self, code, path, message, ref=None):
        self.ref = ref
        super().__init__(code, path, message)
        self.safe_message = message


def _fail(code, path, message='Required-current premise is malformed.', ref=None):
    raise _Failure(code, path, message, ref)


def _key(ref): return (ref['type'], ref['id'], ref['revision'], ref['sha256'])
def _id(ref): return (ref['type'], ref['id'], ref['revision'])
def _digest(value): return canonical_si_sha256(value)
def _is_known(value): return value['state'] == 'KNOWN'
def _unknown(reason): return {'state': 'UNKNOWN', 'reason': reason}


def _walk(value, schema, path):
    """Typed local traversal; text never acquires a semantic ref role."""
    yield value, schema, path
    tag = schema[0]
    if tag == 'object' and type(value) is dict:
        for field, child in schema[1].items():
            if field in value:
                yield from _walk(value[field], child, path + '.' + field)
    elif tag == 'list' and type(value) is list:
        for i, child in enumerate(value):
            yield from _walk(child, schema[1], f'{path}[{i}]')
    elif tag == 'known' and type(value) is dict and value.get('state') == 'KNOWN' and 'value' in value:
        yield from _walk(value['value'], schema[1], path + '.value')


def _local(value, schema, path):
    try:
        _check(value, schema, path, {})
    except SIValidationError as error:
        # Preserve schema traversal order while hiding arbitrary unknown key names,
        # including names containing dots and keys inside Known/ref values.
        if error.code == 'UNKNOWN_FIELD':
            for child, kind, at in _walk(value, schema, path):
                if type(child) is not dict:
                    continue
                if kind[0] == 'object':
                    fields = set(kind[1])
                elif kind[0] == 'known':
                    fields = {'state', 'value' if child.get('state') == 'KNOWN' else 'reason'}
                elif kind[0] == 'ref':
                    fields = {'type', 'id', 'revision', 'sha256'}
                else:
                    continue
                if any(error.path == at + '.' + field for field in child if field not in fields):
                    _fail('UNKNOWN_FIELD', at)
        raise
    try:
        canonical_si_json(value)
    except SIValidationError as error:
        raise _Failure(error.code, path + error.path[1:],
                       'Required-current premise is malformed.' if path.startswith(_P)
                       else 'Supplied references cannot be validated.') from error
    for child, kind, at in _walk(value, schema, path):
        if kind == _PERIOD and child['from_utc'] > child['to_utc']:
            _fail('TYPE', at + '.to_utc')
    return value


def _local_refs(value, schema, path):
    return [(child, at) for child, kind, at in _walk(value, schema, path)
            if kind[0] == 'ref']


def _shape_records(records):
    if type(records) is not list:
        _fail('TYPE', '$.records', 'Supplied references cannot be validated.')
    checked = []
    for i, record in enumerate(records):
        try:
            checked.append(validate_si_record(record))
        except SIValidationError as error:
            raise _Failure(error.code, f'$.records[{i}]' + error.path[1:],
                           'Supplied references cannot be validated.') from error
    return checked


def _projection(index, roots):
    """Accepted currentness semantic roles, not audit Closure or latest lookup.

    Currentness itself remains the accepted API's responsibility; this projection
    supplies the source/claim/risk inventory for the newly approved evaluator.
    """
    found, pending = {}, list(roots)
    while pending:
        ref = pending.pop()
        if _key(ref) in found:
            continue
        found[_key(ref)] = ref
        record = index[_id(ref)][0]
        h, p = record['H'], record['payload']
        kind = h['type']
        if kind == 'RunRecord':
            values = p['semantic_input_refs']
            pending.extend(values[1:] if p['stage'] == 'REVISION' else values)
            continue
        for tag, child, path in _payload_refs(record):
            if tag != 'ref':
                continue  # Accepted currentness independently enforces ERefs.
            if kind in ('CreativeAlternative', 'EvaluationReport') and path == '$.payload.run_ref':
                continue
            pending.append(child)
        producer = h['origin']['run_ref']
        if kind == 'CreativeAlternative':
            producer = p['run_ref']
        if producer is None or (h['origin']['mode'] == 'HUMAN_EDIT' and kind != 'CreativeAlternative'):
            continue
        original_angle = None
        if kind == 'CreativeAlternative':
            genesis = record
            while genesis['H']['previous'] is not None:
                genesis = index[_id(genesis['H']['previous'])][0]
            original_angle = genesis['payload']['angle_ref']
        for child in index[_id(producer)][0]['payload']['semantic_input_refs']:
            if child == h['previous'] or (kind == 'CreativeAlternative' and child == original_angle):
                continue
            pending.append(child)
    return found


def _unique_order(items, key, path, source=False):
    seen, keys = set(), []
    for i, item in enumerate(items):
        value = key(item)
        if value in seen:
            _fail('TYPE', f'{path}[{i}]' + ('.source_ref' if source else ''),
                  'A source entry is repeated.' if source else 'A finding entry is repeated.',
                  item['source_ref'] if source else None)
        seen.add(value)
        keys.append(value)
    if keys != sorted(keys):
        _fail('TYPE', path)


def _covers(outer, inner):
    return outer['from_utc'] <= inner['from_utc'] and outer['to_utc'] >= inner['to_utc']


class _Evaluation:
    def __init__(self, records, roots, observed, ratings, expected, findings, premise, locale):
        self.records = _shape_records(records)
        self.roots = deepcopy(_local(roots, _list(_ref()), '$.semantic_input_refs'))
        for i, ref in enumerate(self.roots):
            if ref['type'] in _NON_DOMAIN:
                _fail('REF_TYPE_MISMATCH', f'$.semantic_input_refs[{i}].type',
                      'Supplied references cannot be validated.')
        self.observed = deepcopy(_local(observed, _CONTEXT, '$.observed_context'))
        self.expected = deepcopy(_local(expected, _CONTEXT, '$.expected_context'))
        for value, path in ((self.observed, '$.observed_context'), (self.expected, '$.expected_context')):
            _context(value, path)
            _observed(value['active_input_refs'], path + '.active_input_refs')
            _observed(value['selection_head_refs'], path + '.selection_head_refs', True)
        self.ratings = deepcopy(_local(ratings, _list(_RATING), '$.ratings'))
        self.findings = deepcopy(_local(findings, _FINDINGS, _H))
        self.premise = None if premise is None else deepcopy(_local(premise, _PREMISE, _P))
        if self.findings['contract_tag'] != 'si-evaluate-findings/proposal-1':
            _fail('VERSION_UNSUPPORTED', _H + '.contract_tag')
        if self.premise is not None and self.premise['contract_tag'] != 'si-required-current/proposal-1':
            _fail('VERSION_UNSUPPORTED', _P + '.contract_tag')
        self.local_ref_paths = _local_refs(self.findings, _FINDINGS, _H)
        if self.premise is not None:
            self.local_ref_paths += _local_refs(self.premise, _PREMISE, _P)
        all_roots = (self.roots + self.observed['active_input_refs'] +
                     self.observed['selection_head_refs'] + self.expected['active_input_refs'] +
                     self.expected['selection_head_refs'] +
                     [ref for ref, _ in self.local_ref_paths] +
                     [ref for ref, _ in _local_refs(self.ratings, _list(_RATING), '$.ratings')])
        # Reuse exact graph/provenance preflight, including all supplied record shapes.
        try:
            verify_si_provenance(self.records, all_roots)
        except SIValidationError as error:
            # D15: normalize a uniquely identified declared local failure. Binding
            # and context repetitions do not hide the source/proof field. Never
            # guess a nested path from a code-only accepted API result.
            if error.code in ('REF_MISSING', 'REF_HASH_MISMATCH'):
                record_index = {(r['H']['type'], r['H']['id'], r['H']['revision']): r
                                for r in self.records}
                failed = {}
                for ref in all_roots:
                    record = record_index.get(_id(ref))
                    if ((error.code == 'REF_MISSING' and record is None) or
                        (error.code == 'REF_HASH_MISMATCH' and record is not None and
                         _digest(record) != ref['sha256'])):
                        failed[_key(ref)] = ref
                if len(failed) == 1:
                    ref = next(iter(failed.values()))
                    for declared, path in self.local_ref_paths:
                        if path.startswith(_P + '.') and '.binding.' not in path and declared == ref:
                            _fail(error.code, path, 'Supplied references cannot be validated.', ref)
            raise
        self.index = {(v['H']['type'], v['H']['id'], v['H']['revision']): (v, i)
                      for i, v in enumerate(self.records)}
        self.active = {_key(ref) for ref in self.observed['active_input_refs']}
        self.conditions, self.stales = [], []
        self.core = {}
        for kind, name in (('StoryIdea', 'idea_ref'), ('Angle', 'angle_ref'),
                           ('AudienceHypothesis', 'audience_ref'), ('ChannelContext', 'channel_ref'),
                           ('Rubric', 'rubric_ref')):
            candidates = {_key(r): r for r in self.roots if r['type'] == kind}
            if len(candidates) != 1:
                _fail('REF_MISSING' if not candidates else 'TYPE', '$.semantic_input_refs',
                      'Evaluation roles are incomplete or ambiguous.')
            self.core[name] = next(iter(candidates.values()))
        self.idea = self.core['idea_ref']
        self.channel = self.payload(self.core['channel_ref'])
        self.locale = self.payload(self.core['audience_ref'])['locale']
        if locale is not None:
            if locale not in ('ru', 'uk') or type(locale) is not str:
                _fail('LOCALE_MISMATCH', '$.ui_locale', 'Evaluation locale does not match.')
            if locale != self.locale:
                _fail('LOCALE_MISMATCH', self.path(self.core['audience_ref'], 'locale'),
                      'Evaluation locale does not match.')
        intake = self.payload(self.payload(self.idea)['intake_ref'])
        if intake['locale'] != self.locale:
            _fail('LOCALE_MISMATCH', self.path(self.payload(self.idea)['intake_ref'], 'locale'),
                  'Evaluation locale does not match.')
        angle = self.payload(self.core['angle_ref'])
        if (angle['idea_ref'] != self.idea or angle['audience_ref'] != self.core['audience_ref'] or
                self.channel['audience_ref'] != self.core['audience_ref']):
            _fail('PROVENANCE_MISMATCH', '$.semantic_input_refs',
                  'Evaluation roles do not match.')
        self.binding = {**self.core, 'semantic_input_refs': self.roots,
                        'context_snapshot': self.expected, 'ratings_sha256': _digest(self.ratings)}
        self._rubric()
        self.main_roots = list(self.roots)
        # Q1/Q2 typed applicability extensions from the explicit active view.
        while True:
            self.main = _projection(self.index, self.main_roots)
            claims = {k for k, r in self.main.items() if r['type'] == 'ClaimItem'}
            extra = []
            for ref in self.observed['active_input_refs']:
                p = self.payload(ref)
                if ref['type'] in ('ClaimCheck', 'EvidenceItem') and _key(p['claim_ref']) in claims:
                    extra.append(ref)
                if ref['type'] == 'Risk' and any(_key(r) in self.main for r in p['basis_refs']):
                    extra.append(ref)
            known = {_key(r) for r in self.main_roots}
            extra = [r for r in extra if _key(r) not in known]
            if not extra:
                break
            self.main_roots.extend(extra)
        self.sources = sorted((r for r in self.main.values() if r['type'] == 'SourceItem'), key=_key)
        self.claims = sorted((r for r in self.main.values() if r['type'] == 'ClaimItem'), key=_key)
        self.checks = sorted((r for r in self.main.values() if r['type'] == 'ClaimCheck'), key=_key)
        self.risks = sorted((r for r in self.main.values() if r['type'] == 'Risk'), key=_key)
        self.proof_roots = []
        self._bindings()
        self._findings()
        self._required_validation()
        for check in self.checks:
            self._check_claim_roles(check)

    def payload(self, ref): return self.index[_id(ref)][0]['payload']
    def record(self, ref): return self.index[_id(ref)][0]
    def path(self, ref, field): return f'$.records[{self.index[_id(ref)][1]}].payload.{field}'

    def add(self, state, code, path, ref, message):
        self.conditions.append((state, {'code': code, 'field_path': path,
                                        'input_ref': ref, 'message': message}))

    def stale(self, path, ref, message='Evaluation context has changed.'):
        self.stales.append({'code': 'INPUT_STALE', 'field_path': path,
                            'input_ref': ref, 'message': message})

    def _rubric(self):
        ref = self.core['rubric_ref']
        p = self.payload(ref)
        for field, expected in (('method_id', 'si-rubric'), ('method_version', '1'),
                                ('blocker_policy_version', '1')):
            if p[field] != expected:
                _fail('VERSION_UNSUPPORTED', self.path(ref, field), 'Evaluation profile is unsupported.')
        if len(p['criteria']) != 9 or len(self.ratings) != 9:
            _fail('TYPE', '$.ratings', 'Exactly nine approved criteria are required.')
        seen = set()
        for i, ((key, weight), criterion, rating) in enumerate(zip(_CRITERIA, p['criteria'], self.ratings)):
            if criterion['key'] != key or criterion['weight_percent'] != weight:
                _fail('TYPE', self.path(ref, f'criteria[{i}]'), 'Approved criterion identity or weight differs.')
            if rating['criterion_key'] != key or rating['criterion_key'] in seen:
                _fail('TYPE', f'$.ratings[{i}].criterion_key', 'Approved rating order or identity differs.')
            seen.add(rating['criterion_key'])

    def _bindings(self):
        for binding, prefix in [(self.findings['binding'], _H + '.binding')] + (
                [] if self.premise is None else [(self.premise['binding'], _P + '.binding')]):
            _context(binding['context_snapshot'], prefix + '.context_snapshot')
            old_angle = self.payload(binding['angle_ref'])
            old_channel = self.payload(binding['channel_ref'])
            if (old_angle['idea_ref'] != binding['idea_ref'] or
                old_angle['audience_ref'] != binding['audience_ref'] or
                old_channel['audience_ref'] != binding['audience_ref']):
                _fail('PROVENANCE_MISMATCH', prefix,
                      'Exact source or review binding is inconsistent.', binding['idea_ref'])
            if binding['ratings_sha256'] != _digest(self.ratings):
                _fail('REF_HASH_MISMATCH', prefix + '.ratings_sha256',
                      'Exact content binding does not match.', self.idea)
            for field in self.binding:
                if field == 'ratings_sha256':
                    continue
                if canonical_si_json(binding[field]) != canonical_si_json(self.binding[field]):
                    self.stale(prefix + '.' + field, self.idea)
        if canonical_si_json(self.expected) != canonical_si_json(self.observed):
            self.stale(_P + '.binding.context_snapshot' if self.premise is not None else '$.expected_context', self.idea)

    def _findings(self):
        f = self.findings
        bh = _digest(f['binding'])
        confidence = f['confidence_findings']
        ranks = {k: i for i, (k, _) in enumerate(_CRITERIA)}
        seen, previous = set(), -1
        for i, value in enumerate(confidence):
            at = f'{_H}.confidence_findings[{i}]'
            key = value['criterion_key']
            if key in seen:
                _fail('TYPE', at, 'A finding entry is repeated.')
            seen.add(key)
            if key not in ranks or ranks[key] <= previous:
                _fail('TYPE', at + '.criterion_key')
            previous = ranks[key]
            rating = self.ratings[ranks[key]]
            if rating['confidence']['level'] != 'UNKNOWN':
                _fail('TYPE', at, 'Known confidence cannot be replaced by a finding.')
            for field, expected in (('binding_sha256', bh), ('rating_sha256', _digest(rating))):
                if value[field] != expected:
                    _fail('REF_HASH_MISMATCH', at + '.' + field, 'Exact content binding does not match.', self.core['rubric_ref'])
        duplicates = f['duplicate_findings']
        portfolio = self.payload(f['binding']['channel_ref'])['portfolio']
        _unique_order(duplicates, lambda v: v['portfolio_entry_index'], _H + '.duplicate_findings')
        for i, value in enumerate(duplicates):
            at = f'{_H}.duplicate_findings[{i}]'
            n = value['portfolio_entry_index']
            if not _is_known(portfolio) or n >= len(portfolio['value']):
                _fail('TYPE', at + '.portfolio_entry_index')
            entry = portfolio['value'][n]
            for field, expected in (('binding_sha256', bh), ('portfolio_entry_sha256', _digest(entry))):
                if value[field] != expected:
                    _fail('REF_HASH_MISMATCH', at + '.' + field, 'Exact content binding does not match.', self.core['channel_ref'])
            if value['candidate_ref'] != entry['story_ref']:
                _fail('PROVENANCE_MISMATCH', at + '.candidate_ref', 'Exact source or review binding is inconsistent.', self.core['channel_ref'])

    def _required_validation(self):
        p = self.premise
        if p is None:
            return
        req = p['required_data']
        determination = p['determination']
        if ((determination == 'UNDETERMINED' and _is_known(req)) or
                (determination == 'NOT_REQUIRED' and (not _is_known(req) or req['value']))):
            _fail('TYPE', _P + '.required_data')
        values = req['value'] if _is_known(req) else []
        _unique_order(values, lambda v: _key(v['source_ref']), _P + '.required_data.value', True)
        assessments = p['source_freshness']
        _unique_order(assessments, lambda v: _key(v['source_ref']), _P + '.source_freshness', True)
        # Internally intact old scope is STALE, not an invented wrong-subject error.
        premise_sources = _projection(self.index, p['binding']['semantic_input_refs'])
        allowed = {k for k, r in premise_sources.items() if r['type'] == 'SourceItem'}
        if canonical_si_json(p['binding']) == canonical_si_json(self.binding):
            allowed = {_key(s) for s in self.sources}
        required = {_key(v['source_ref']) for v in values}
        for i, value in enumerate(values):
            if _key(value['source_ref']) not in allowed:
                _fail('PROVENANCE_MISMATCH', f'{_P}.required_data.value[{i}].source_ref',
                      'Exact source or review binding is inconsistent.', value['source_ref'])
        bh, rh = _digest(p['binding']), _digest({k: p[k] for k in ('determination', 'required_data')})
        for i, value in enumerate(assessments):
            at = f'{_P}.source_freshness[{i}]'
            source = value['source_ref']
            if _key(source) not in allowed:
                _fail('PROVENANCE_MISMATCH', at + '.source_ref', 'Exact source or review binding is inconsistent.', source)
            for field, expected in (('binding_sha256', bh), ('requirements_sha256', rh)):
                if value[field] != expected:
                    _fail('REF_HASH_MISMATCH', at + '.' + field, 'Exact content binding does not match.', source)
            if value['applicability'] == 'NOT_APPLICABLE':
                if _key(source) in required:
                    _fail('TYPE', at + '.applicability')
                if value['outcome'] != 'UNKNOWN':
                    _fail('TYPE', at + '.outcome')
                if _is_known(value['review_period']) or value['evidence']:
                    _fail('TYPE', at)
            for j, proof in enumerate(value['evidence']):
                pp = at + f'.evidence[{j}]'
                e, c, m = (self.payload(proof[k]) for k in ('evidence_ref', 'check_ref', 'material_ref'))
                if e['source_ref'] != proof['material_ref']:
                    _fail('PROVENANCE_MISMATCH', pp + '.material_ref', 'Exact source or review binding is inconsistent.', source)
                if c['claim_ref'] != e['claim_ref'] or (_is_known(c['evidence_refs']) and proof['evidence_ref'] not in c['evidence_refs']['value']):
                    _fail('PROVENANCE_MISMATCH', pp + '.check_ref', 'Exact source or review binding is inconsistent.', source)
                if _is_known(m['material_sha256']) and m['material_sha256']['value'] != proof['material_sha256']:
                    _fail('REF_HASH_MISMATCH', pp + '.material_sha256', 'Exact content binding does not match.', source)
                for field in ('evidence_ref', 'check_ref', 'material_ref'):
                    self.proof_roots.append((proof[field], pp + '.' + field))

    def _check_claim_roles(self, check):
        p = self.payload(check)
        if _is_known(p['evidence_refs']):
            for j, ref in enumerate(p['evidence_refs']['value']):
                if self.payload(ref)['claim_ref'] != p['claim_ref']:
                    _fail('PROVENANCE_MISMATCH', self.path(check, f'evidence_refs.value[{j}]'),
                          'Exact claim and review binding is inconsistent.', check)

    def currentness(self):
        invalid = []
        queries = [(r, f'$.semantic_input_refs[{i}]') for i, r in enumerate(self.roots)]
        queries += [(r, '$.observed_context.active_input_refs') for r in self.main_roots
                    if _key(r) not in {_key(q) for q in self.roots}]
        queries += self.proof_roots
        for ref, path in queries:
            result = check_si_currentness(self.records, ref,
                self.observed['active_input_refs'], self.observed['selection_head_refs'])
            if result['currentness'] == 'INVALID':
                for code in result['reason_codes']:
                    invalid.append({'code': code, 'field_path': path, 'input_ref': ref,
                                    'message': 'Supplied references cannot be validated.'})
            elif result['currentness'] == 'STALE':
                self.stale(path, ref, 'Evaluation dependencies have changed.')
        for ref in self.checks:
            if _key(ref) not in self.active:
                self.stale(self.path(ref, 'claim_ref'), ref, 'Evaluation dependencies have changed.')
        if invalid:
            # D15 proof-boundary normalization: retain the independently failing
            # declared support leaf, rather than repeat its failure for every
            # enclosing evidence/check query. Main-root paths stay untouched.
            # This uses only explicit query results and exact semantic edges;
            # it never invents an underlying ERef path from a code-only result.
            proof_paths = {path for _, path in self.proof_roots}
            direct = [d for d in invalid if d['field_path'] in proof_paths]
            minimal = []
            for diagnostic in invalid:
                if diagnostic in direct and diagnostic['code'] == 'REF_MISSING':
                    ref = diagnostic['input_ref']
                    dependencies = _projection(self.index, [ref])
                    if any(other['code'] == diagnostic['code'] and
                           other['input_ref'] != ref and _key(other['input_ref']) in dependencies
                           for other in direct):
                        continue
                minimal.append(diagnostic)
            return 'INVALID', minimal
        if self.stales:
            return 'STALE', self.stales
        return 'CURRENT', []

    def _positive(self, check):
        p = self.payload(check)
        if p['state'] not in ('supported', 'qualified') or not _is_known(p['evidence_refs']):
            return False
        return any(self.payload(e)['relation'] == 'supports' and _is_known(self.payload(e)['locator']) and
                   _is_known(self.payload(self.payload(e)['source_ref'])['material_sha256'])
                   for e in p['evidence_refs']['value'])

    def _mitigated(self, risk):
        rec, p = self.record(risk), self.payload(risk)
        if p['resolution'] != 'MITIGATED' or rec['H']['origin']['mode'] != 'HUMAN_EDIT':
            return False
        for ref in p['resolution_basis_refs']:
            if ref['type'] != 'ClaimCheck' or not self._positive(ref):
                continue
            claim = self.payload(ref)['claim_ref']
            if not any(self.payload(c)['claim_ref'] == claim and not self._positive(c) for c in self.checks):
                return True
        return False

    def classify(self):
        self._scoring_findings()
        self._freshness_conditions()
        self._claim_conditions()
        self._risk_conditions()
        self._editorial_conditions()
        unknown = any(not _is_known(r['value']) for r in self.ratings)
        aggregate = (_unknown('At least one required rating is unknown.') if unknown else
                     {'state': 'KNOWN', 'value': 2 * sum(w * r['value']['value']
                      for (_, w), r in zip(_CRITERIA, self.ratings))})
        primary = min((s for s, _ in self.conditions), key=_ORDER.get, default='ELIGIBLE_FOR_CREATIVE')
        diagnostics = _diagnostics(self.conditions)
        codes = sorted({d['code'] for d in diagnostics})
        return {'status': 'OK', 'currentness': 'CURRENT', 'locale': self.locale,
                'eligibility': {'state': primary, 'reason_codes': codes},
                'aggregate_tenths': aggregate, 'ratings': self.ratings, 'diagnostics': diagnostics}

    def _scoring_findings(self):
        confidence = {v['criterion_key']: v for v in self.findings['confidence_findings']}
        for i, rating in enumerate(self.ratings):
            if not _is_known(rating['value']):
                self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', f'$.ratings[{i}].value',
                         self.core['rubric_ref'], 'A required rating is unknown.')
            if rating['confidence']['level'] == 'UNKNOWN':
                finding = confidence.get(rating['criterion_key'])
                if finding is None or finding['outcome'] == 'INSUFFICIENT':
                    self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', _H + '.confidence_findings',
                             self.core['rubric_ref'], 'Confidence consideration is missing or insufficient for ' + rating['criterion_key'] + '.')
        portfolio = self.channel['portfolio']
        if not _is_known(portfolio):
            self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', self.path(self.core['channel_ref'], 'portfolio'),
                     self.core['channel_ref'], 'Portfolio research is incomplete.')
            return
        findings = {v['portfolio_entry_index']: (i, v) for i, v in enumerate(self.findings['duplicate_findings'])}
        for n in range(len(portfolio['value'])):
            if n not in findings:
                self.add('REVIEW_DUPLICATE', 'DUPLICATE_REVIEW_NEEDED', _H + '.duplicate_findings',
                         self.core['channel_ref'], f'Portfolio comparison is missing for index {n}.')
            else:
                i, value = findings[n]
                if value['outcome'] != 'DISTINCT':
                    self.add('REVIEW_DUPLICATE', 'DUPLICATE_REVIEW_NEEDED', f'{_H}.duplicate_findings[{i}].outcome',
                             self.core['channel_ref'], 'A portfolio comparison is unresolved.')

    def _freshness_conditions(self):
        p = self.premise
        if p is None:
            self.add('NEEDS_INPUT', 'EVIDENCE_NEEDED', _P, None, 'Required-current determination is missing.')
            return
        req = p['required_data']
        values = req['value'] if _is_known(req) else []
        required = {_key(v['source_ref']): v for v in values}
        if p['determination'] == 'UNDETERMINED':
            self.add('NEEDS_INPUT', 'EVIDENCE_NEEDED', _P + '.determination', self.idea,
                     'Required-current determination is unresolved.')
        elif p['determination'] == 'REQUIRED':
            if not values:
                self.add('NEEDS_INPUT', 'EVIDENCE_NEEDED', _P + '.required_data', self.idea,
                         'Required data specification is missing.')
            for k, value in enumerate(values):
                for field, message in (('specification', 'Required source data are unspecified.'),
                                       ('period', 'Required period is unspecified.')):
                    if not _is_known(value[field]):
                        self.add('NEEDS_INPUT', 'EVIDENCE_NEEDED', f'{_P}.required_data.value[{k}].{field}',
                                 value['source_ref'], message)
        supplied = {_key(v['source_ref']): (i, v) for i, v in enumerate(p['source_freshness'])}
        for source in self.sources:
            if _key(source) not in supplied:
                self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', _P + '.source_freshness', source,
                         'Source freshness review is missing.')
                continue
            i, value = supplied[_key(source)]
            at = f'{_P}.source_freshness[{i}]'
            if value['applicability'] == 'NOT_APPLICABLE':
                continue
            if value['applicability'] == 'UNDETERMINED':
                self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', at + '.applicability', source,
                         'Source freshness applicability is unresolved.')
                continue
            adequate = value['outcome'] == 'ESTABLISHED' and _is_known(value['review_period'])
            if not _is_known(value['review_period']):
                self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', at + '.review_period', source,
                         'Source review period is unspecified.')
            if adequate:
                q = value['review_period']['value']
                r = required.get(_key(source))
                if r is not None and _is_known(r['period']) and not _covers(q, r['period']['value']):
                    adequate = False
                adequate = adequate and any(self._proof_adequate(proof, q) for proof in value['evidence'])
            if not adequate:
                self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', at + '.outcome', source,
                         'Source freshness evidence is insufficient.')

    def _proof_adequate(self, proof, period):
        e, c, m = (self.payload(proof[k]) for k in ('evidence_ref', 'check_ref', 'material_ref'))
        return (e['relation'] == 'supports' and _is_known(e['locator']) and
                c['state'] in ('supported', 'qualified') and _is_known(c['evidence_refs']) and
                proof['evidence_ref'] in c['evidence_refs']['value'] and
                _is_known(m['material_sha256']) and _covers(proof['coverage'], period))

    def _claim_conditions(self):
        for claim in self.claims:
            p = self.payload(claim)
            if p['claim_kind'] == 'fictional':
                continue
            central = p['claim_kind'] == 'factual' and p['materiality'] == 'CENTRAL'
            state, code = ('BLOCKED', 'CENTRAL_CLAIM_UNSUPPORTED') if central else ('NEEDS_RESEARCH', 'EVIDENCE_NEEDED')
            checks = [c for c in self.checks if self.payload(c)['claim_ref'] == claim]
            if not checks:
                self.add(state, code, self.path(claim, 'materiality' if central else 'evidence_expectation'), claim,
                         'A central factual claim lacks applicable support.' if central else 'Claim support requires research.')
            for check in checks:
                if not self._positive(check):
                    self.add(state, code, self.path(check, 'state'), check,
                             'A central factual claim has unresolved review.' if central else 'Claim review requires further research.')
            for ref in self.main.values():
                if ref['type'] == 'EvidenceItem':
                    e = self.payload(ref)
                    if e['claim_ref'] == claim and e['relation'] == 'contradicts':
                        self.add(state, code, self.path(ref, 'relation'), ref, 'Recorded evidence remains in conflict.')

    def _risk_conditions(self):
        for risk in self.risks:
            p = self.payload(risk)
            if p['blocking'] and not self._mitigated(risk):
                field = 'resolution_basis_refs' if p['resolution'] == 'MITIGATED' else 'blocking'
                self.add('BLOCKED', 'EVIDENCE_NEEDED', self.path(risk, field), risk,
                         'An explicit ' + p['category'].lower() + ' risk remains blocking.')
        for ref in self.main.values():
            if ref['type'] != 'VisualRequirement':
                continue
            p = self.payload(ref)
            if p['role'] != 'REQUIRED':
                continue
            material = (_is_known(p['material_sha256']) and any(
                _is_known(self.payload(s)['material_sha256']) and
                self.payload(s)['material_sha256'] == p['material_sha256'] for s in p['source_refs']))
            review = any(ref in self.payload(r)['basis_refs'] and self._mitigated(r) for r in self.risks)
            if not (p['rights_state'] == 'DOCUMENTED' and _is_known(p['licence_basis']) and material and review):
                self.add('BLOCKED', 'RIGHTS_BLOCKED', self.path(ref, 'rights_state'), ref,
                         'Essential material rights are unresolved.')

    def _editorial_conditions(self):
        audience = self.core['audience_ref']
        for field, message in (('knowledge_level', 'Audience knowledge level is unspecified.'),
                               ('motivation', 'Audience motivation is unspecified.')):
            if not _is_known(self.payload(audience)[field]):
                self.add('NEEDS_INPUT', 'EVIDENCE_NEEDED', self.path(audience, field), audience, message)
        if not _is_known(self.channel['capability_notes']):
            self.add('NEEDS_INPUT', 'EVIDENCE_NEEDED', self.path(self.core['channel_ref'], 'capability_notes'),
                     self.core['channel_ref'], 'Production constraints are unspecified.')
        if (not _is_known(self.payload(self.idea)['source_refs']) and
                any(self.payload(q)['claim_kind'] != 'fictional' for q in self.claims)):
            self.add('NEEDS_RESEARCH', 'EVIDENCE_NEEDED', self.path(self.idea, 'source_refs'), self.idea,
                     'Source research is incomplete.')


def _diagnostics(conditions):
    found = {}
    for state, diagnostic in conditions:
        identity = (diagnostic['code'], diagnostic['field_path'],
                    canonical_si_json(diagnostic['input_ref']), diagnostic['message'])
        rank = _ORDER.get(state, -1)
        if identity not in found or rank < found[identity][0]:
            found[identity] = (rank, diagnostic)
    return [v[1] for _, v in sorted(found.items(), key=lambda item: (item[1][0], *item[0]))]


def _rejected(status, diagnostics):
    return {'status': status, 'currentness': status, 'locale': None,
            'eligibility': None, 'aggregate_tenths': None, 'ratings': [],
            'reason_codes': sorted({d['code'] for d in diagnostics}),
            'diagnostics': _diagnostics([(status, d) for d in diagnostics])}


def evaluate_si(records, semantic_input_refs, observed_context, ratings,
                expected_context, human_findings, required_current_premise=None, *, ui_locale=None):
    """Return detached non-authoritative plain values; never create SI records.

    Context arguments are complete existing ContextSnapshot values. This keeps
    active refs, selection heads AND snapshot marker explicit. Optional ui_locale
    must match the exact Audience/Idea Intake locale; otherwise that supplied
    Audience determines the result locale (no translation or demographic inference).

    OK: currentness=CURRENT, eligibility={state,reason_codes}, aggregate_tenths,
    preserved ratings and ordered Diagnostic values. INVALID/STALE: no accepted
    eligibility or aggregate, diagnostics and reason_codes only. Supplied objects
    must stay stable during the call; no shared mutable state or retained inputs.
    """
    try:
        evaluation = _Evaluation(records, semantic_input_refs, observed_context, ratings,
                                 expected_context, human_findings, required_current_premise, ui_locale)
        state, diagnostics = evaluation.currentness()
        result = evaluation.classify() if state == 'CURRENT' else _rejected(state, diagnostics)
        return deepcopy(result)
    except SIValidationError as error:
        ref = getattr(error, 'ref', None)
        message = getattr(error, 'safe_message',
                          'Required-current premise is malformed.' if error.path.startswith(_P)
                          else 'Supplied references cannot be validated.')
        return _rejected('INVALID', [{'code': error.code, 'field_path': error.path,
                                     'input_ref': deepcopy(ref), 'message': message}])
