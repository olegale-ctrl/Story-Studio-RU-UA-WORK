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
