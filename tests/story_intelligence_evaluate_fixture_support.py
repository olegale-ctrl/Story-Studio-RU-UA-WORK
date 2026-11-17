"""Authored content-addressed fixture graphs; no evaluator import or test cases.

Reference bytes use independent stdlib JSON/SHA256 from the existing test Graph.
Expected edges, active selections, source roles and literal T25 data are authored
here, never obtained from production semantic projection/scoring functions.
"""
from copy import deepcopy as cp
import hashlib

from tests.test_story_intelligence_records_v1 import fixtures, known, unknown, eref
from tests.test_story_intelligence_resolver_v1 import Graph, key, digest
from tests.test_story_intelligence_provenance_v1 import data_refs

AT = '2026-11-12T00:00:00Z'
KEYS = ('audience_interest', 'channel_fit', 'angle_novelty', 'evidence_quality',
        'narrative_potential', 'visual_feasibility', 'resource_fit',
        'risk_manageability', 'portfolio_distinctness')
WEIGHTS = (15, 10, 10, 20, 15, 10, 10, 5, 5)
RANGE = {'from_utc': '2026-11-01T00:00:00Z', 'to_utc': '2026-11-04T00:00:00Z'}
WIDE = {'from_utc': '2026-10-31T00:00:00Z', 'to_utc': '2026-11-05T00:00:00Z'}


def un(reason='Review pending'): return {'state': 'UNKNOWN', 'reason': reason}


class Fixture:
    def __init__(self, *, t25=False, locale='ru', portfolio='empty', risk=None,
                 visual=None, claim_states=None, claim_kind='factual', materiality='CENTRAL',
                 relation='supports', source_updates=None, audience_updates=None,
                 channel_updates=None, rubric_updates=None, idea_updates=None,
                 confidence='HIGH', discovery_eref=False, bad_discovery_stage=False):
        self.g, self.n, self.active = Graph(), {}, {}
        self.extra_roots, self.main_sources = [], {}
        self._tag = 0
        self.discovery_eref = discovery_eref
        self.bad_discovery_stage = bad_discovery_stage
        self.heads = []
        self.put('T', 'Intake', input_kind='TOPIC', raw_input='Synthetic science topic', locale=locale,
                 supplied_source_refs=[], user_goal=known('Synthetic editorial exercise'))
        source = self.source_payload(); source.update(source_updates or {})
        self.put('S', 'SourceItem', **source)
        self.main_sources[key(self.n['S'])] = self.n['S']
        rd = self.run('DISCOVERY', [self.n['T'], self.n['S']]); self.n['RD'] = rd
        idea = dict(intake_ref=self.n['T'], title='Synthetic science topic', summary='Synthetic editorial premise',
                    viewer_question='What remains uncertain?', source_refs=known([self.n['S']]), candidate_binding=None)
        idea.update(idea_updates or {})
        self.put('I', 'StoryIdea', _run=rd, _inputs=[self.n['T'], self.n['S']], **idea)
        rp = self.run('DISCOVERY', [self.n['T'], self.n['S']]); self.n['RP'] = rp
        self.put('P', 'StoryIdea', _run=rp, _inputs=[self.n['T'], self.n['S']],
                 intake_ref=self.n['T'], title='Synthetic portfolio topic', summary='Prior synthetic premise',
                 viewer_question='What was previously considered?', source_refs=known([self.n['S']]), candidate_binding=None)
        au = dict(locale=locale, region=known('Fixture region'), knowledge_level=known('General'),
                  motivation=known('Learning'), interests=known(['Science history']), age_range=known('Adults'),
                  basis_refs=[self.n['T']], assumptions=['Synthetic editorial hypothesis, not audience statistics'])
        au.update(audience_updates or {}); self.put('AU', 'AudienceHypothesis', **au)
        entry = dict(story_ref=self.n['P'], published_title='Synthetic portfolio topic',
                     published_locator=known('synthetic:portfolio'), published_at=known('2026-11-01T00:00:00Z'),
                     angle_notes='Comparison pending', basis_ref=self.n['T'])
        pf = known([entry]) if portfolio == 'one' or t25 else (un() if portfolio == 'unknown' else known([]))
        channel = dict(channel_alias='Fixture channel', purpose='Science history', audience_ref=self.n['AU'],
                       constraints=[], portfolio=pf, analytics=known('Synthetic hypothesis, not measured statistics'),
                       capability_notes=known('CPU-only editorial planning; not measured execution'))
        channel.update(channel_updates or {}); self.put('H', 'ChannelContext', **channel)
        self.check_names = []
        if visual is not None:
            vp = cp(fixtures()['VisualRequirement']['payload'])
            vp.update(role='REQUIRED', source_refs=[self.n['S']], asset_ref=None,
                      rights_state='UNKNOWN', fallback=un(), licence_basis=un(), material_sha256=un())
            vp.update(visual); self.put('V', 'VisualRequirement', **vp)
            rr = self.risk_payload(); rr.update(category='LEGAL', blocking=True, basis_refs=[self.n['V']])
            rr.update(risk or {})
            if rr['resolution'] == 'MITIGATED' and not rr['resolution_basis_refs']: rr['resolution_basis_refs']=[self.n['T']]
            self.put('R', 'Risk', **rr)
        if claim_states is not None:
            self.put('Q', 'ClaimItem', statement='Synthetic declared claim', claim_kind=claim_kind,
                     materiality=materiality, evidence_expectation='Recorded evidence required', editorial_ref=None)
            self.put('E', 'EvidenceItem', claim_ref=self.n['Q'], source_ref=self.n['S'], relation=relation,
                     locator=known('Section 1'), explanation='Synthetic evidence')
            for i, state in enumerate(claim_states):
                name = 'Check' + str(i); self.check_names.append(name)
                self.put(name, 'ClaimCheck', **self.check_payload(self.n['Q'], self.n['E'], state))
        self.put('A', 'Angle', idea_ref=self.n['I'], audience_ref=self.n['AU'], question='What remains uncertain?',
                 thesis='Synthetic editorial premise', claim_refs=[self.n['Q']] if 'Q' in self.n else [],
                 distinction='Human comparison pending', limitations=[])
        rubric = dict(method_id='si-rubric', method_version='1', blocker_policy_version='1', missing_policy='ALL_REQUIRED',
                      criteria=[dict(key=k, description='Synthetic criterion', weight_percent=w,
                                     min=0, max=5, direction='HIGH_IS_BETTER') for k, w in zip(KEYS, WEIGHTS)])
        rubric.update(rubric_updates or {}); self.put('G', 'Rubric', **rubric)
        if 'R' not in self.n:
            rr = self.risk_payload(); rr.update(basis_refs=[self.n['A']], blocking=t25)
            rr.update(risk or {})
            if rr['resolution'] == 'MITIGATED' and not rr['resolution_basis_refs']: rr['resolution_basis_refs']=[self.n['T']]
            self.put('R', 'Risk', **rr)
        self.include_risk = bool(t25 or risk or visual is not None)
        self.ratings = [dict(criterion_key=k, value=un('Rating not supplied') if t25 and i == 0 else known(5),
                             basis_refs=[self.n['AU'], self.n['A']], explanation='Synthetic supplied rating',
                             confidence=dict(level=confidence, basis='Synthetic judgement, not a probability'))
                        for i, k in enumerate(KEYS)]
        self.confidence_outcomes = {}
        self.duplicate_outcomes = {0: 'UNRESOLVED' if t25 else 'DISTINCT'}
        self.determination = 'UNDETERMINED' if t25 else 'NOT_REQUIRED'
        self.requirements = None
        self.assessments = {}
        self.omit_premise = False
        self.refresh_ratings_bindings()

    @staticmethod
    def source_payload():
        return dict(source_kind='LOCAL', original_locator='synthetic:material', title=known('Synthetic material'),
                    author=known('Fixture'), publisher=known('Fixture'), published_at=known('2026-11-01T00:00:00Z'),
                    captured_at=known('2026-11-01T00:00:00Z'),
                    material_sha256=known(hashlib.sha256(b'synthetic fixture material').hexdigest()),
                    editorial_ref=None, rights_note=known('Synthetic fixture; not a licence'), freshness_requirement=un())

    @staticmethod
    def risk_payload():
        return dict(category='SCIENTIFIC', severity='HIGH', blocking=False, basis_refs=[],
                    description='Synthetic explicit scientific risk', mitigation='Review remains pending',
                    resolution='OPEN', resolution_basis_refs=[], owner_role='Fixture editor')

    @staticmethod
    def check_payload(claim, evidence, state='supported'):
        return dict(claim_ref=claim, evidence_refs=known([evidence]), state=state,
                    qualification='Within the reviewed scope' if state == 'qualified' else None,
                    reviewer_label=None if state == 'unreviewed' else 'Fixture reviewer',
                    reviewed_at=None if state == 'unreviewed' else AT,
                    reason=None if state == 'unreviewed' else 'Synthetic recorded review')

    def record(self, ref): return self.g.refs[key(ref)]
    def payload(self, name): return self.record(self.n[name])['payload']

    def put(self, name, kind, _run=None, _inputs=None, **payload):
        value = cp(fixtures()[kind]); value['payload'] = cp(payload)
        h = value['H']; h.update(created_at=AT, creator_label='Fixture author', input_refs=data_refs(payload), editorial_refs=[])
        if _run is not None:
            h.update(creator_label='SI_ENGINE', origin=dict(mode='TEMPLATE_DERIVED' if kind == 'CreativeAlternative' else 'RULE_DERIVED', run_ref=_run, imported_from=None), input_refs=cp(_inputs))
        ref = self.g.add(value, data_refs(value)); self.n[name] = ref
        if kind != 'RunRecord': self.active[(ref['type'], ref['id'])] = ref
        return ref

    def run(self, stage, roots, context=None):
        value = cp(fixtures()['RunRecord']); h, p = value['H'], value['payload']
        ctx = cp(context) if context is not None else dict(context_version=1, active_input_refs=[],
                    selection_head_refs=[], editorial_snapshot_sha256=un('No editorial snapshot'))
        snapshot = self.g.closure(roots + ctx['active_input_refs'] + ctx['selection_head_refs'])
        method = {'DISCOVERY': 'si.discover-local', 'REVISION': 'si.human-revision'}[stage]
        if stage == 'DISCOVERY' and self.bad_discovery_stage:
            stage, method = 'CREATIVE', 'si.creative-templates'
        p.update(stage=stage, method_id=method, method_version='1-r1', semantic_input_refs=cp(roots),
                 input_snapshot=snapshot, context_snapshot=ctx, editorial_snapshot_sha256=cp(ctx['editorial_snapshot_sha256']),
                 request_payload_sha256=digest({'portfolio_ref': None}), rubric_ref=None, provider=None,
                 started_at=AT, finished_at=AT, confidence=dict(level='HIGH', basis='Synthetic fixture'),
                 fresh_trends=un('No live trends'), caveats=['Synthetic fixture, not executed discovery'])
        h.update(created_at=AT, input_refs=cp(snapshot),
                 editorial_refs=[eref('source')] if stage == 'DISCOVERY' and self.discovery_eref else [])
        return self.g.add(value, data_refs(value))

    def revise(self, name, **updates):
        prior = self.n[name]; value = cp(self.record(prior)); value['payload'].update(cp(updates))
        roots = [prior] + data_refs(value['payload']); run = self.run('REVISION', roots)
        value['H'].update(revision=prior['revision'] + 1, previous=prior, input_refs=roots,
                          origin=dict(mode='HUMAN_EDIT', run_ref=run, imported_from=None))
        ref = self.g.add(value, data_refs(value), keep_identity=True); self.n[name] = ref
        self.active[(ref['type'], ref['id'])] = ref
        if name in ('S', 'S2'):
            self.main_sources.pop(key(prior), None); self.main_sources[key(ref)] = ref
        return ref

    def roots(self):
        return [self.n[n] for n in ('I', 'A', 'AU', 'H', 'G')] + ([self.n['R']] if self.include_risk else []) + cp(self.extra_roots)

    def context(self):
        return dict(context_version=1, active_input_refs=sorted(self.active.values(), key=key),
                    selection_head_refs=cp(self.heads), editorial_snapshot_sha256=un('No editorial snapshot'))

    def refresh_ratings_bindings(self):
        for rating in self.ratings:
            rating['basis_refs'] = [self.n['AU'], self.n['A']]

    def add_source(self, name='S2', **updates):
        p = self.source_payload(); p.update(updates)
        ref = self.put(name, 'SourceItem', **p); self.extra_roots.append(ref); self.main_sources[key(ref)] = ref
        return ref

    def proof(self, *, state='supported', relation='supports', locator=None, material_known=True,
              material_external=False, coverage=None):
        self._tag += 1; tag = str(self._tag)
        mp = self.source_payload()
        if not material_known: mp['material_sha256'] = un()
        if material_external: mp['editorial_ref'] = eref('source')
        material = self.put('Material' + tag, 'SourceItem', **mp)
        claim = self.put('ProofClaim' + tag, 'ClaimItem', statement='Synthetic temporal review claim',
                         claim_kind='factual', materiality='CONTEXT', evidence_expectation='Recorded support', editorial_ref=None)
        evidence = self.put('ProofEvidence' + tag, 'EvidenceItem', claim_ref=claim, source_ref=material,
                            relation=relation, locator=known('Section 1') if locator is None else locator,
                            explanation='Synthetic recorded support')
        check = self.put('ProofCheck' + tag, 'ClaimCheck', **self.check_payload(claim, evidence, state))
        return dict(evidence_ref=evidence, check_ref=check, material_ref=material,
                    material_sha256=hashlib.sha256(b'synthetic fixture material').hexdigest(),
                    coverage=cp(coverage or RANGE))

    def require(self, source=None, specification=None, period=None):
        self.determination = 'REQUIRED'
        self.requirements = known([dict(source_ref=source or self.n['S'],
            specification=known('Synthetic data scope') if specification is None else specification,
            period=known(cp(RANGE)) if period is None else period)])

    def establish(self, source=None, review=None, evidence=None):
        source = source or self.n['S']
        if evidence is None: evidence = [self.proof()]
        self.assessments[key(source)] = dict(source_ref=source, applicability='APPLICABLE',
            review_period=known(cp(review or RANGE)), outcome='ESTABLISHED', evidence=cp(evidence), reason='Scope considered')

    def uncertain(self, source=None, review=None):
        source = source or self.n['S']
        self.assessments[key(source)] = dict(source_ref=source, applicability='APPLICABLE',
            review_period=known(cp(review or RANGE)), outcome='UNKNOWN', evidence=[], reason='Review pending')

    def mitigate(self, visual=False):
        proof = self.proof()
        self.main_sources[key(proof['material_ref'])] = proof['material_ref']
        basis = [self.n['V']] if visual else [self.n['A']]
        self.revise('R', blocking=True, resolution='MITIGATED', basis_refs=basis,
                    resolution_basis_refs=[proof['check_ref']])
        self.include_risk = True
        return proof

    def arguments(self):
        self.refresh_ratings_bindings()
        ctx = self.context(); roots = self.roots()
        binding = dict(idea_ref=self.n['I'], angle_ref=self.n['A'], audience_ref=self.n['AU'],
            channel_ref=self.n['H'], rubric_ref=self.n['G'], semantic_input_refs=roots,
            context_snapshot=ctx, ratings_sha256=digest(self.ratings))
        findings = dict(contract_tag='si-evaluate-findings/proposal-1', binding=cp(binding),
                        confidence_findings=[], duplicate_findings=[])
        for rating in self.ratings:
            keyname = rating['criterion_key']
            if keyname in self.confidence_outcomes:
                findings['confidence_findings'].append(dict(binding_sha256=digest(binding), criterion_key=keyname,
                    rating_sha256=digest(rating), outcome=self.confidence_outcomes[keyname], reason='Scope considered'))
        pf = self.payload('H')['portfolio']
        if pf['state'] == 'KNOWN':
            for index, entry in enumerate(pf['value']):
                if index in self.duplicate_outcomes:
                    findings['duplicate_findings'].append(dict(binding_sha256=digest(binding), portfolio_entry_index=index,
                        portfolio_entry_sha256=digest(entry), candidate_ref=cp(entry['story_ref']),
                        outcome=self.duplicate_outcomes[index], reason='Comparison pending'))
        required = cp(self.requirements) if self.requirements is not None else (
            un('Scope not specified') if self.determination != 'NOT_REQUIRED' else known([]))
        rh = digest(dict(determination=self.determination, required_data=required))
        items = []
        for source in sorted(self.main_sources.values(), key=key):
            value = cp(self.assessments.get(key(source), dict(source_ref=source, applicability='NOT_APPLICABLE',
                review_period=un('Not applicable'), outcome='UNKNOWN', evidence=[], reason='Scope considered')))
            value.update(binding_sha256=digest(binding), requirements_sha256=rh)
            items.append(value)
        premise = dict(contract_tag='si-required-current/proposal-1', binding=cp(binding),
                       determination=self.determination, required_data=required, source_freshness=items)
        return cp(dict(records=self.g.records, semantic_input_refs=roots, observed_context=ctx,
            ratings=self.ratings, expected_context=ctx, human_findings=findings,
            required_current_premise=None if self.omit_premise else premise))


def t25_expected(f):
    """Literal expected tuples authored from final oracle, not evaluator output."""
    return [
        dict(code='EVIDENCE_NEEDED', field_path='$.records[10].payload.blocking', input_ref=cp(f.n['R']),
             message='An explicit scientific risk remains blocking.'),
        dict(code='EVIDENCE_NEEDED', field_path='$.required_current_premise.determination', input_ref=cp(f.n['I']),
             message='Required-current determination is unresolved.'),
        dict(code='EVIDENCE_NEEDED', field_path='$.ratings[0].value', input_ref=cp(f.n['G']),
             message='A required rating is unknown.'),
        dict(code='DUPLICATE_REVIEW_NEEDED', field_path='$.human_findings.duplicate_findings[0].outcome', input_ref=cp(f.n['H']),
             message='A portfolio comparison is unresolved.')]


def original_resume_arguments():
    """Exact original EVAL-RESUME-G01 diagnostic graph and input bytes."""
    from copy import deepcopy
    import hashlib
    from tests.test_story_intelligence_records_v1 import fixtures, known, unknown, AT
    from tests.test_story_intelligence_resolver_v1 import Graph, digest
    from tests.test_story_intelligence_provenance_v1 import data_refs

    T, g = fixtures(), Graph()
    def put(kind, **updates):
        value = deepcopy(T[kind]); value['payload'].update(updates)
        return g.add(value, data_refs(value))

    i = put('Intake', user_goal=known('Учебная история науки'))
    s = put('SourceItem', title=known('Синтетический материал'), author=known('Fixture'),
        publisher=known('Fixture'), published_at=known(AT), captured_at=known(AT),
        material_sha256=known(hashlib.sha256(b'synthetic fixture only').hexdigest()),
        rights_note=known('Искусственные данные; не основание реальных прав'),
        freshness_requirement=unknown())
    d = g.run('DISCOVERY', [i, s]); v = deepcopy(T['StoryIdea'])
    v['H']['origin']['run_ref'] = d; v['H']['input_refs'] = [i, s]
    v['payload'].update(intake_ref=i, source_refs=known([s]))
    idea = g.add(v, data_refs(v))
    a = put('AudienceHypothesis', region=known('Fixture'), knowledge_level=known('Начальный'),
        motivation=known('Изучение'), interests=known(['История']), age_range=known('Взрослые'),
        assumptions=['Явная учебная гипотеза, не статистика'])
    k = put('ChannelContext', audience_ref=a, portfolio=known([]),
        analytics=known('Учебная гипотеза, не статистика'), capability_notes=known('CPU-only'))
    an = put('Angle', idea_ref=idea, audience_ref=a, claim_refs=[])
    r = put('Rubric'); roots = [idea, an, a, k, r, s]
    active = [ref for ref in g.closure(roots) if ref['type'] != 'RunRecord']
    ctx = dict(context_version=1, active_input_refs=active, selection_head_refs=[],
               editorial_snapshot_sha256=unknown())
    ratings = [dict(criterion_key=x['key'], value=known(5), basis_refs=[a, s],
        explanation='Синтетическая эвристика, не подтверждение свежести',
        confidence=dict(level='HIGH', basis='Учебное суждение, не truth certificate'))
        for x in T['Rubric']['payload']['criteria']]
    binding = dict(idea_ref=idea, angle_ref=an, audience_ref=a, channel_ref=k, rubric_ref=r,
        semantic_input_refs=roots, context_snapshot=ctx, ratings_sha256=digest(ratings))
    findings = dict(contract_tag='si-evaluate-findings/proposal-1', binding=binding,
                    confidence_findings=[], duplicate_findings=[])
    premise = dict(contract_tag='si-required-current/proposal-1', binding=deepcopy(binding),
                   determination='UNDETERMINED', required_data=un('Scope not specified'), source_freshness=[])
    return dict(records=g.records, semantic_input_refs=roots, observed_context=deepcopy(ctx),
                expected_context=deepcopy(ctx), ratings=ratings, human_findings=findings,
                required_current_premise=premise)
