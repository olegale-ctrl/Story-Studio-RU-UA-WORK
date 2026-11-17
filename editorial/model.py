"""E01.1 value types only: no codec, hashing, graph, persistence or gates.

Hashes are supplied values whose shape is checked, never computed or verified.
References may be unresolved in this layer. Constructors do not approve facts.
"""
from dataclasses import dataclass
from enum import Enum
import re
from uuid import UUID


class ContentMode(str, Enum):
    FACTUAL = 'factual'
    FICTIONAL = 'fictional'
    HYBRID = 'hybrid'


class Locale(str, Enum):
    RU = 'ru'
    UK = 'uk'


class ObjectKind(str, Enum):
    PRODUCTION = 'production'
    GENRE_PROFILE = 'genre_profile'
    CANDIDATE = 'candidate'
    SOURCE = 'source'
    CLAIM = 'claim'
    SCRIPT = 'script'
    SCENE_PLAN = 'scene_plan'
    ASSET = 'asset'
    RIGHTS_REVIEW = 'rights_review'


class ApprovalDecision(str, Enum):
    APPROVE = 'approve'
    REJECT = 'reject'
    REVISE = 'revise'
    REVOKE = 'revoke'


class RightsStatus(str, Enum):
    APPROVED = 'approved'
    RESTRICTED = 'restricted'
    UNKNOWN = 'unknown'
    BLOCKED = 'blocked'


class ClaimType(str, Enum):
    FACTUAL = 'factual'
    INTERPRETATION = 'interpretation'
    FICTIONAL = 'fictional'


class EvidenceRelation(str, Enum):
    SUPPORTS = 'supports'
    CONTRADICTS = 'contradicts'
    CONTEXT = 'context'
    INSUFFICIENT = 'insufficient'


@dataclass(frozen=True)
class Violation:
    code: str
    field_path: str
    message: str
    object_ref: 'RevisionRef | None' = None

    def __post_init__(self):
        for name in ('code', 'field_path', 'message'):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise ValueError(f'{name} must be a nonempty string')
        if self.object_ref is not None:
            if not isinstance(self.object_ref, RevisionRef):
                raise TypeError('object_ref must be RevisionRef or None')


class ModelError(ValueError):
    """Invalid constructor input, with a structured immutable violation."""

    def __init__(self, violation: Violation):
        if type(violation) is not Violation:
            raise TypeError('violation must be a Violation')
        self.violation = violation
        super().__init__(f'{violation.field_path}: {violation.message}')


def _fail(field, message):
    raise ModelError(Violation('INVALID_VALUE', field, message))


def _text(value, field):
    if type(value) is not str or not value.strip():
        _fail(field, 'must be a nonempty string')


def _instance(value, cls, field):
    if not isinstance(value, cls):
        _fail(field, f'must be {cls.__name__}; implicit coercion is not supported')


def _positive(value, field):
    if type(value) is not int or value < 1:
        _fail(field, 'must be a positive integer, not bool')


def _id(value, field):
    _text(value, field)
    try:
        parsed = UUID(value)
    except ValueError:
        _fail(field, 'must be a canonical UUID string')
    if str(parsed) != value:
        _fail(field, 'must be a canonical lowercase hyphenated UUID string')


def _hash(value, field):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        _fail(field, 'must be 64 lowercase hexadecimal characters')


def _tuple(value, cls, field):
    if type(value) is not tuple:
        _fail(field, 'must be an immutable tuple')
    for item in value:
        _instance(item, cls, field)


@dataclass(frozen=True)
class RevisionRef:
    kind: ObjectKind
    id: str
    revision: int
    content_hash: str

    def __post_init__(self):
        _instance(self.kind, ObjectKind, 'kind')
        _id(self.id, 'id')
        _positive(self.revision, 'revision')
        _hash(self.content_hash, 'content_hash')


@dataclass(frozen=True)
class EditorialRevision:
    """Common immutable header; not a complete arbitrary domain payload."""

    ref: RevisionRef

    def __post_init__(self):
        _instance(self.ref, RevisionRef, 'ref')


@dataclass(frozen=True)
class ProductionRevision(EditorialRevision):
    title: str
    profile_ref: RevisionRef
    content_mode: ContentMode
    script_locale: Locale
    narration_locale: Locale
    subtitle_locale: Locale
    ui_locale: Locale
    intended_use: str
    output_preset: str
    created_at: str

    def __post_init__(self):
        super().__post_init__()
        if self.ref.kind is not ObjectKind.PRODUCTION:
            _fail('ref.kind', 'must be production')
        _text(self.title, 'title')
        _instance(self.profile_ref, RevisionRef, 'profile_ref')
        _instance(self.content_mode, ContentMode, 'content_mode')
        for name in ('script_locale', 'narration_locale', 'subtitle_locale', 'ui_locale'):
            _instance(getattr(self, name), Locale, name)
        for name in ('intended_use', 'output_preset', 'created_at'):
            _text(getattr(self, name), name)


@dataclass(frozen=True)
class SourceRevision(EditorialRevision):
    title: str
    locator: str
    rights_ref: RevisionRef

    def __post_init__(self):
        super().__post_init__()
        if self.ref.kind is not ObjectKind.SOURCE:
            _fail('ref.kind', 'must be source')
        _text(self.title, 'title')
        _text(self.locator, 'locator')
        _instance(self.rights_ref, RevisionRef, 'rights_ref')


@dataclass(frozen=True)
class EvidenceLink:
    source_ref: RevisionRef
    relation: EvidenceRelation
    locator: str
    explanation: str
    reviewer: str
    reviewed_at: str

    def __post_init__(self):
        _instance(self.source_ref, RevisionRef, 'source_ref')
        _instance(self.relation, EvidenceRelation, 'relation')
        for name in ('locator', 'explanation', 'reviewer', 'reviewed_at'):
            _text(getattr(self, name), name)


@dataclass(frozen=True)
class ClaimRevision(EditorialRevision):
    statement: str
    claim_type: ClaimType
    materiality: str
    evidence_links: tuple[EvidenceLink, ...] = ()

    def __post_init__(self):
        super().__post_init__()
        if self.ref.kind is not ObjectKind.CLAIM:
            _fail('ref.kind', 'must be claim')
        _text(self.statement, 'statement')
        _instance(self.claim_type, ClaimType, 'claim_type')
        _text(self.materiality, 'materiality')
        _tuple(self.evidence_links, EvidenceLink, 'evidence_links')


@dataclass(frozen=True)
class RightsReview(EditorialRevision):
    subject_id: str
    subject_revision: int
    material_digest: str
    intended_use: str
    allowed_actions: tuple[str, ...]
    status: RightsStatus
    reviewer: str
    reviewed_at: str
    basis: str

    def __post_init__(self):
        super().__post_init__()
        if self.ref.kind is not ObjectKind.RIGHTS_REVIEW:
            _fail('ref.kind', 'must be rights_review')
        _id(self.subject_id, 'subject_id')
        _positive(self.subject_revision, 'subject_revision')
        _hash(self.material_digest, 'material_digest')
        _tuple(self.allowed_actions, str, 'allowed_actions')
        for action in self.allowed_actions:
            _text(action, 'allowed_actions')
        _instance(self.status, RightsStatus, 'status')
        for name in ('intended_use', 'reviewer', 'reviewed_at', 'basis'):
            _text(getattr(self, name), name)


@dataclass(frozen=True)
class ApprovalRecord:
    id: str
    gate: str
    object_ref: RevisionRef
    dependency_digest: str
    policy_version: str
    actor: str
    timestamp: str
    decision: ApprovalDecision
    reason: str
    review_declarations: tuple[str, ...] = ()

    def __post_init__(self):
        _id(self.id, 'id')
        _instance(self.object_ref, RevisionRef, 'object_ref')
        _hash(self.dependency_digest, 'dependency_digest')
        _instance(self.decision, ApprovalDecision, 'decision')
        for name in ('gate', 'policy_version', 'actor', 'timestamp', 'reason'):
            _text(getattr(self, name), name)
        _tuple(self.review_declarations, str, 'review_declarations')
        for item in self.review_declarations:
            _text(item, 'review_declarations')


@dataclass(frozen=True)
class EditorialSnapshot:
    """Minimal envelope; collection existence/graph/gates are checked later."""

    production_id: str
    generation: int
    revisions: tuple[EditorialRevision, ...] = ()
    approvals: tuple[ApprovalRecord, ...] = ()
    active_refs: tuple[RevisionRef, ...] = ()
    editorial_schema_version: int = 1

    def __post_init__(self):
        _id(self.production_id, 'production_id')
        _positive(self.generation, 'generation')
        if type(self.editorial_schema_version) is not int or self.editorial_schema_version != 1:
            _fail('editorial_schema_version', 'must be integer 1')
        _tuple(self.revisions, EditorialRevision, 'revisions')
        _tuple(self.approvals, ApprovalRecord, 'approvals')
        _tuple(self.active_refs, RevisionRef, 'active_refs')


# E01.1b-1 additions. Existing E01.1 constructors deliberately stay unchanged.
def _contract_text(value, field):
    _text(value, field)
    if len(value) > 100_000 or any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        _fail(field, 'must contain valid Unicode, at most 100000 code points')


def _optional_text(value, field):
    if value is not None:
        _contract_text(value, field)


def _choice(value, choices, field):
    if type(value) is not str or value not in choices:
        _fail(field, 'must be one of: ' + ', '.join(choices))


def _owner(value, kind, field='owner_ref'):
    _instance(value, RevisionRef, field)
    if value.kind is not kind:
        _fail(field, f'must reference {kind.value}')


def _key(value, field):
    if type(value) is not str or re.fullmatch('[a-z][a-z0-9_]{0,63}', value) is None:
        _fail(field, 'must be a lowercase ASCII snake_case key of length 1..64')


def _range_int(value, low, high, field):
    if type(value) is not int or not low <= value <= high:
        _fail(field, f'must be integer {low}..{high}, not bool')


def _utc(value, field):
    if type(value) is not str or re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', value) is None:
        _fail(field, 'must be a UTC timestamp YYYY-MM-DDTHH:MM:SSZ')
    from datetime import datetime
    try:
        datetime.fromisoformat(value[:-1] + '+00:00')
    except ValueError:
        _fail(field, 'must be an existing calendar date and time')


def _optional_utc(value, field):
    if value is not None:
        _utc(value, field)


def _unique(values, field):
    if len(set(values)) != len(values):
        _fail(field, 'must not contain duplicates')


@dataclass(frozen=True)
class RubricCriterion:
    key: str
    description: str
    rating_min: int
    rating_max: int
    weight_percent: int

    def __post_init__(self):
        _key(self.key, 'key')
        _contract_text(self.description, 'description')
        _range_int(self.rating_min, 0, 0, 'rating_min')
        _range_int(self.rating_max, 5, 5, 'rating_max')
        _range_int(self.weight_percent, 0, 100, 'weight_percent')


@dataclass(frozen=True)
class GenreProfile(EditorialRevision):
    profile_key: str
    version: str
    display_name_ru: str
    display_name_uk: str
    allowed_modes: tuple[ContentMode, ...]
    narrative_structure: tuple[str, ...]
    review_policy_version: str
    rubric: tuple[RubricCriterion, ...] | None

    def __post_init__(self):
        super().__post_init__()
        _owner(self.ref, ObjectKind.GENRE_PROFILE, 'ref')
        _key(self.profile_key, 'profile_key')
        for name in ('version', 'display_name_ru', 'display_name_uk', 'review_policy_version'):
            _contract_text(getattr(self, name), name)
        _tuple(self.allowed_modes, ContentMode, 'allowed_modes')
        _tuple(self.narrative_structure, str, 'narrative_structure')
        if not self.allowed_modes or not self.narrative_structure:
            _fail('allowed_modes/narrative_structure', 'both must be nonempty')
        _unique(self.allowed_modes, 'allowed_modes')
        for text in self.narrative_structure:
            _contract_text(text, 'narrative_structure')
        if self.rubric is not None:
            _tuple(self.rubric, RubricCriterion, 'rubric')
            if not self.rubric or sum(c.weight_percent for c in self.rubric) != 100:
                _fail('rubric', 'non-null rubric must be nonempty with weights summing to 100')
            _unique(tuple(c.key for c in self.rubric), 'rubric.keys')


@dataclass(frozen=True)
class CriterionRating:
    criterion_key: str
    rating: int
    reason: str

    def __post_init__(self):
        _key(self.criterion_key, 'criterion_key')
        _range_int(self.rating, 0, 5, 'rating')
        _contract_text(self.reason, 'reason')


@dataclass(frozen=True)
class CandidateRevision(EditorialRevision):
    title: str
    summary: str
    source_refs: tuple[RevisionRef, ...]
    discovery_method: str
    discovery_input: str
    assessment: tuple[CriterionRating, ...] | None
    rationale: str | None

    def __post_init__(self):
        super().__post_init__()
        _owner(self.ref, ObjectKind.CANDIDATE, 'ref')
        for name in ('title', 'summary', 'discovery_input'):
            _contract_text(getattr(self, name), name)
        _tuple(self.source_refs, RevisionRef, 'source_refs')
        for source in self.source_refs:
            _owner(source, ObjectKind.SOURCE, 'source_refs')
        _choice(self.discovery_method, ('manual_topic', 'manual_url', 'manual_local'), 'discovery_method')
        _optional_text(self.rationale, 'rationale')
        if self.assessment is not None:
            _tuple(self.assessment, CriterionRating, 'assessment')
            _unique(tuple(r.criterion_key for r in self.assessment), 'assessment.keys')


@dataclass(frozen=True)
class SourceDetails:
    owner_ref: RevisionRef
    source_type: str
    author: str | None
    publisher: str | None
    published_at: str | None
    accessed_at: str | None
    access_notes: str | None
    reliability_notes: str | None
    material_digest: str | None

    def __post_init__(self):
        _owner(self.owner_ref, ObjectKind.SOURCE)
        _choice(self.source_type, ('url', 'local'), 'source_type')
        for name in ('author', 'publisher', 'access_notes', 'reliability_notes'):
            _optional_text(getattr(self, name), name)
        for name in ('published_at', 'accessed_at'):
            _optional_utc(getattr(self, name), name)
        if self.material_digest is not None:
            _hash(self.material_digest, 'material_digest')


@dataclass(frozen=True)
class ClaimReview:
    owner_ref: RevisionRef
    review_status: str
    qualification: str | None
    reviewer: str | None
    reviewed_at: str | None
    reason: str | None

    def __post_init__(self):
        _owner(self.owner_ref, ObjectKind.CLAIM)
        _choice(self.review_status, ('unreviewed', 'supported', 'disputed', 'unverified', 'qualified', 'removed'), 'review_status')
        for name in ('qualification', 'reviewer', 'reason'):
            _optional_text(getattr(self, name), name)
        _optional_utc(self.reviewed_at, 'reviewed_at')
        if self.review_status == 'unreviewed':
            if any(v is not None for v in (self.qualification, self.reviewer, self.reviewed_at, self.reason)):
                _fail('review_status', 'unreviewed requires null review metadata')
        else:
            if any(v is None for v in (self.reviewer, self.reviewed_at, self.reason)):
                _fail('review_status', 'reviewed status requires reviewer, reviewed_at and reason')
            if (self.review_status == 'qualified') != (self.qualification is not None):
                _fail('qualification', 'must be present exactly for qualified status')


@dataclass(frozen=True)
class RightsDetails:
    """E00 Q5 addendum: explicit subject kind, no reverse hash graph edge.

    Combined with the unchanged RightsReview by a future aggregate/codec.
    No default/inference for legacy RightsReview subjects is provided.
    """

    owner_ref: RevisionRef
    subject_kind: ObjectKind
    expires_at: str | None

    def __post_init__(self):
        _owner(self.owner_ref, ObjectKind.RIGHTS_REVIEW)
        _instance(self.subject_kind, ObjectKind, 'subject_kind')
        if self.subject_kind not in (ObjectKind.SOURCE, ObjectKind.ASSET):
            _fail('subject_kind', 'must be source or asset')
        _optional_utc(self.expires_at, 'expires_at')


def _refs(values, kind, field):
    _tuple(values, RevisionRef, field)
    for value in values:
        _owner(value, kind, field)


def _bounded_tuple(values, cls, field):
    _tuple(values, cls, field)
    if not 1 <= len(values) <= 1000:
        _fail(field, 'must contain 1..1000 values')


@dataclass(frozen=True)
class BriefValue:
    revision: int
    audience: str
    angle: str
    promise: str
    must_include_claim_refs: tuple[RevisionRef, ...]
    must_avoid: tuple[str, ...]
    profile_ref: RevisionRef

    def __post_init__(self):
        _positive(self.revision, 'revision')
        for name in ('audience', 'angle', 'promise'):
            _contract_text(getattr(self, name), name)
        _refs(self.must_include_claim_refs, ObjectKind.CLAIM, 'must_include_claim_refs')
        _tuple(self.must_avoid, str, 'must_avoid')
        for text in self.must_avoid:
            _contract_text(text, 'must_avoid')
        _owner(self.profile_ref, ObjectKind.GENRE_PROFILE, 'profile_ref')


@dataclass(frozen=True)
class ScriptSegment:
    id: str
    text: str
    role: str
    claim_refs: tuple[RevisionRef, ...]
    visual_notes: str | None
    pronunciation_notes: str | None
    disclosure_marker: str | None

    def __post_init__(self):
        _id(self.id, 'id')
        _contract_text(self.text, 'text')
        _choice(self.role, ('opening', 'body', 'closing', 'other'), 'role')
        _refs(self.claim_refs, ObjectKind.CLAIM, 'claim_refs')
        for name in ('visual_notes', 'pronunciation_notes', 'disclosure_marker'):
            _optional_text(getattr(self, name), name)


@dataclass(frozen=True)
class ScriptRevision(EditorialRevision):
    production_ref: RevisionRef
    candidate_ref: RevisionRef
    brief: BriefValue
    locale: Locale
    segments: tuple[ScriptSegment, ...]
    claim_refs: tuple[RevisionRef, ...]

    def __post_init__(self):
        super().__post_init__()
        _owner(self.ref, ObjectKind.SCRIPT, 'ref')
        _owner(self.production_ref, ObjectKind.PRODUCTION, 'production_ref')
        _owner(self.candidate_ref, ObjectKind.CANDIDATE, 'candidate_ref')
        _instance(self.brief, BriefValue, 'brief')
        _instance(self.locale, Locale, 'locale')
        _bounded_tuple(self.segments, ScriptSegment, 'segments')
        _unique(tuple(s.id for s in self.segments), 'segments.id')
        _refs(self.claim_refs, ObjectKind.CLAIM, 'claim_refs')
        expected = tuple(sorted({r for s in self.segments for r in s.claim_refs},
                                key=lambda r: (r.kind.value, r.id, r.revision, r.content_hash)))
        if self.claim_refs != expected:
            _fail('claim_refs', 'must be the sorted unique union of segment claim refs')


@dataclass(frozen=True)
class Scene:
    id: str
    start: int
    end: int
    narration_text: str
    visual_kind: str
    visual_brief: str
    asset_ref: RevisionRef | None
    estimate_ms: int | None

    def __post_init__(self):
        _id(self.id, 'id')
        if type(self.start) is not int or self.start < 0:
            _fail('start', 'must be a nonnegative integer, not bool')
        if type(self.end) is not int or self.end <= self.start:
            _fail('end', 'must be an integer greater than start, not bool')
        _contract_text(self.narration_text, 'narration_text')
        _choice(self.visual_kind, ('still',), 'visual_kind')
        _contract_text(self.visual_brief, 'visual_brief')
        if self.asset_ref is not None:
            _owner(self.asset_ref, ObjectKind.ASSET, 'asset_ref')
        if self.estimate_ms is not None:
            _positive(self.estimate_ms, 'estimate_ms')


@dataclass(frozen=True)
class ScenePlanRevision(EditorialRevision):
    script_ref: RevisionRef
    scenes: tuple[Scene, ...]

    def __post_init__(self):
        super().__post_init__()
        _owner(self.ref, ObjectKind.SCENE_PLAN, 'ref')
        _owner(self.script_ref, ObjectKind.SCRIPT, 'script_ref')
        _bounded_tuple(self.scenes, Scene, 'scenes')
        _unique(tuple(s.id for s in self.scenes), 'scenes.id')
        cursor = 0
        for scene in self.scenes:
            if scene.start != cursor:
                _fail('scenes', 'ranges must start at zero and be continuous in given order')
            cursor = scene.end


def _relative_path(value):
    _contract_text(value, 'file_ref')
    if len(value) > 240 or any(ord(c) < 32 or c in '<>:"|?*\\' for c in value):
        _fail('file_ref', 'must be a safe relative POSIX path, at most 240 characters')
    for part in value.split('/'):
        stem = part.split('.')[0].upper()
        reserved = stem in ('CON', 'PRN', 'AUX', 'NUL', 'CLOCK$') or re.fullmatch(r'(COM|LPT)[1-9¹²³]', stem)
        if part in ('', '.', '..') or len(part) > 100 or part.endswith(('.', ' ')) or reserved:
            _fail('file_ref', 'unsafe or reserved path component')


@dataclass(frozen=True)
class AssetRevision(EditorialRevision):
    file_ref: str
    sha256: str
    kind: str
    rights_ref: RevisionRef
    scene_id: str | None
    script_ref: RevisionRef | None
    text_digest: str | None

    def __post_init__(self):
        super().__post_init__()
        _owner(self.ref, ObjectKind.ASSET, 'ref')
        _relative_path(self.file_ref)
        _hash(self.sha256, 'sha256')
        _choice(self.kind, ('image', 'audio', 'video'), 'kind')
        _owner(self.rights_ref, ObjectKind.RIGHTS_REVIEW, 'rights_ref')
        if self.scene_id is not None:
            _id(self.scene_id, 'scene_id')
        if (self.script_ref is None) != (self.text_digest is None):
            _fail('script_ref/text_digest', 'both must be null or both present')
        if self.script_ref is not None:
            _owner(self.script_ref, ObjectKind.SCRIPT, 'script_ref')
            _hash(self.text_digest, 'text_digest')


@dataclass(frozen=True)
class Event:
    id: str
    actor: str
    at: str
    action: str
    refs: tuple[RevisionRef, ...]
    reason: str
    error_code: str | None

    def __post_init__(self):
        _id(self.id, 'id')
        _contract_text(self.actor, 'actor')
        _utc(self.at, 'at')
        _choice(self.action, ('production_created', 'revision_added', 'active_selection_changed',
                             'review_recorded', 'approval_recorded', 'recovery_recorded',
                             'operation_failed'), 'action')
        _tuple(self.refs, RevisionRef, 'refs')
        _contract_text(self.reason, 'reason')
        _optional_text(self.error_code, 'error_code')


@dataclass(frozen=True)
class ActiveSelections:
    production: RevisionRef | None
    candidate: RevisionRef | None
    script: RevisionRef | None
    scene_plan: RevisionRef | None

    def __post_init__(self):
        for name, kind in (('production', ObjectKind.PRODUCTION),
                           ('candidate', ObjectKind.CANDIDATE),
                           ('script', ObjectKind.SCRIPT),
                           ('scene_plan', ObjectKind.SCENE_PLAN)):
            value = getattr(self, name)
            if value is not None:
                _owner(value, kind, name)


_REVISION_TYPES = (
    (ObjectKind.PRODUCTION, ProductionRevision), (ObjectKind.GENRE_PROFILE, GenreProfile),
    (ObjectKind.CANDIDATE, CandidateRevision), (ObjectKind.SOURCE, SourceRevision),
    (ObjectKind.CLAIM, ClaimRevision), (ObjectKind.SCRIPT, ScriptRevision),
    (ObjectKind.SCENE_PLAN, ScenePlanRevision), (ObjectKind.ASSET, AssetRevision),
    (ObjectKind.RIGHTS_REVIEW, RightsReview),
)


@dataclass(frozen=True)
class ContractSnapshot:
    """Full in-memory aggregate; not a JSON schema or graph integrity proof.

    Missing companions/targets and hash correctness belong to later integrity
    validation. All supplied values are retained without sorting or inference.
    """

    base: EditorialSnapshot
    source_details: tuple[SourceDetails, ...]
    claim_reviews: tuple[ClaimReview, ...]
    rights_details: tuple[RightsDetails, ...]
    events: tuple[Event, ...]
    snapshot_checksum: str

    def __post_init__(self):
        _instance(self.base, EditorialSnapshot, 'base')
        _hash(self.snapshot_checksum, 'snapshot_checksum')
        for name, cls in (('source_details', SourceDetails), ('claim_reviews', ClaimReview),
                          ('rights_details', RightsDetails), ('events', Event)):
            values = getattr(self, name)
            _tuple(values, cls, name)
            if len(values) > 10_000:
                _fail(name, 'at most 10000 values')
            keys = tuple(v.id if name == 'events' else
                         (v.owner_ref.kind, v.owner_ref.id, v.owner_ref.revision)
                         for v in values)
            _unique(keys, name)
        _unique(tuple(a.id for a in self.base.approvals), 'base.approvals.id')
        if len(self.base.revisions) > 10_000:
            _fail('base.revisions', 'at most 10000 revisions')
        _unique(tuple((v.ref.kind, v.ref.id, v.ref.revision) for v in self.base.revisions), 'base.revisions')
        for value in self.base.revisions:
            if not any(value.ref.kind is kind and type(value) is cls for kind, cls in _REVISION_TYPES):
                _fail('base.revisions', 'must contain concrete payload types, not ref-only headers')
        ranks = {kind: i for i, (kind, _) in enumerate(_REVISION_TYPES)}
        order = tuple((ranks[v.ref.kind], v.ref.id, v.ref.revision) for v in self.base.revisions)
        if order != tuple(sorted(order)):
            _fail('base.revisions', 'must use contract collection/id/revision order')
        active_kinds = (ObjectKind.PRODUCTION, ObjectKind.CANDIDATE, ObjectKind.SCRIPT, ObjectKind.SCENE_PLAN)
        indices = []
        for value in self.base.active_refs:
            if value.kind not in active_kinds:
                _fail('base.active_refs', 'unsupported selection kind')
            indices.append(active_kinds.index(value.kind))
        if indices != sorted(set(indices)):
            _fail('base.active_refs', 'must be unique and in slot order')

    @property
    def active_selections(self) -> ActiveSelections:
        selected = {r.kind: r for r in self.base.active_refs}
        return ActiveSelections(*(selected.get(k) for k in (
            ObjectKind.PRODUCTION, ObjectKind.CANDIDATE, ObjectKind.SCRIPT, ObjectKind.SCENE_PLAN)))

    @property
    def rights_reviews(self) -> tuple[RightsReview, ...]:
        """Distinct typed collection for the future wire mapping, no serialization."""
        return tuple(r for r in self.base.revisions if r.ref.kind is ObjectKind.RIGHTS_REVIEW)
