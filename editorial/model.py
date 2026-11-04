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
