"""Consistency of supplied SI provenance; not evidence of actual execution.

No operations, identity/rights/privacy authority, currentness or ERef adapter.
Exact byte/hash/DAG/snapshot verification is delegated to the accepted resolver.
"""
from copy import deepcopy

from .model_v1 import SIValidationError
from .resolver_v1 import resolve_si_closure, _direct_refs

__all__ = ['verify_si_provenance']

_GENERATORS = {
    'StoryIdea': ('DISCOVERY', 'si.discover-local', '1-r1'),
    'CreativeAlternative': ('CREATIVE', 'si.creative-templates', '1-r1'),
    'EvaluationReport': ('EVALUATION', 'si.evaluate', '1-r1'),
    'ReviewPacket': ('PACKET_EXPORT', 'si.review-packet', '1-r1'),
    'ProductionBrief': ('BRIEF_ASSEMBLY', 'si.brief-assembly', '1-r1'),
}
_REVISION = ('REVISION', 'si.human-revision', '1-r1')


def _identity(ref):
    return (ref['type'], ref['id'], ref['revision'])


def _header_identity(h):
    return (h['type'], h['id'], h['revision'])


def _fail(path, message):
    raise SIValidationError('PROVENANCE_MISMATCH', path, message)


def verify_si_provenance(records, roots):
    """Return detached canonical Closure after all reachable provenance checks.

    Same finite plain-list interface/duplicate policy as resolve_si_closure.
    The supplied records must remain stable during a call (no concurrent edits).
    Unrelated records retain the resolver's structural-only validation boundary.
    """
    closure = resolve_si_closure(records, roots)
    # Resolver has validated all inputs and exact reachable refs. Copy locally;
    # no dict supplied by the caller is treated as an authority/index proof.
    index = {_header_identity(v['H']):(deepcopy(v), i) for i, v in enumerate(records)}

    def lookup(ref):
        return index[_identity(ref)][0]

    def generator(ref, expected, path):
        run = lookup(ref)
        actual = tuple(run['payload'][field] for field in ('stage', 'method_id', 'method_version'))
        if run['H']['type'] != 'RunRecord' or actual != expected:
            _fail(path, 'Actual generating Run stage/method/version does not match output mechanism')
        return run

    for ref in closure:
        record, i = index[_identity(ref)]
        h, p = record['H'], record['payload']
        origin = h['origin']
        path = f'$.records[{i}]'
        run = None
        if origin['mode'] == 'HUMAN_EDIT':
            run = generator(origin['run_ref'], _REVISION, path + '.H.origin.run_ref')
        elif origin['mode'] in ('RULE_DERIVED', 'TEMPLATE_DERIVED', 'MODEL_DERIVED'):
            expected = _GENERATORS.get(h['type'])
            if expected is None:
                _fail(path + '.H.origin.run_ref', 'No approved generator for this record mechanism')
            run = generator(origin['run_ref'], expected, path + '.H.origin.run_ref')
        if h['type'] == 'EvaluationReport' and p['rubric_ref'] != run['payload']['rubric_ref']:
            _fail(path + '.payload.rubric_ref', 'EvaluationReport Rubric differs from its actual generating Run')

        # Exact previous hashes and numbering are already verified by the resolver
        # and accepted header validator. Walk their immutable supplied bytes to
        # genesis without re-labelling historical data or synthesizing revisions.
        ancestors = []
        previous = h['previous']
        while previous is not None:
            prior = lookup(previous)
            ph = prior['H']
            if (ph['type'], ph['id']) != (h['type'], h['id']):
                _fail(path + '.H.previous', 'Previous record changes identity')
            ancestors.append(prior)
            previous = ph['previous']
        genesis = ancestors[-1] if ancestors else record

        if origin['mode'] == 'HUMAN_EDIT':
            if not ancestors:
                _fail(path + '.H.previous', 'Human edit has no previous revision')
            for prior in ancestors:
                if origin['run_ref'] == prior['H']['origin']['run_ref']:
                    _fail(path + '.H.origin.run_ref', 'Human revision cannot reuse an ancestral generating Run')
            # R1 §2 / R1a: base first, then direct typed payload SIRefs in schema
            # order, retaining repeated semantic-array entries; never snapshot.
            payload_refs = [value for value, field in _direct_refs(record, '$')
                            if field.startswith('$.payload.')]
            expected_roots = [h['previous']] + payload_refs
            if h['input_refs'] != expected_roots:
                _fail(path + '.H.input_refs', 'Human edit roots must be exact previous then direct payload refs')
            if run['payload']['semantic_input_refs'] != expected_roots:
                run_i = index[_identity(origin['run_ref'])][1]
                _fail(f'$.records[{run_i}].payload.semantic_input_refs',
                      'Revision Run direct semantic roots differ from previous/payload inputs')

        if h['type'] == 'CreativeAlternative':
            original = genesis['H']['origin']['run_ref']
            if genesis['payload']['run_ref'] != original:
                _fail(path + '.payload.run_ref', 'Genesis creative refs disagree')
            generator(original, _GENERATORS['CreativeAlternative'], path + '.payload.run_ref')
            if p['run_ref'] != original:
                _fail(path + '.payload.run_ref', 'Creative revision replaced exact genesis CREATIVE Run')
            if h['revision'] == 1 and origin['run_ref'] != p['run_ref']:
                _fail(path + '.payload.run_ref', 'Initial creative refs disagree')
    return deepcopy(closure)
