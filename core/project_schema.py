"""Editor-neutral Story Studio project contract (v2), standard-library only.

Version 1 payloads are migrated in memory; no source file is rewritten.
All timing values are integer milliseconds, all paths are user-controlled references.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
import math

SUPPORTED_LOCALES = frozenset({'ru', 'uk'})
SCHEMA_VERSION = 3
TRACK_KINDS = frozenset({'video', 'audio', 'subtitle'})


def _text(value: object, field: str, *, required: bool = True) -> None:
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f'{field} must be a string' + (' with content' if required else ''))


def _int(value: object, field: str, *, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f'{field} must be an integer >= {minimum}')


def _exact(obj: object, fields: set[str], name: str) -> None:
    if not isinstance(obj, dict) or set(obj) != fields:
        raise ValueError(f'invalid {name} fields')


@dataclass(frozen=True)
class Scene:
    id: str
    start_ms: int
    duration_ms: int
    text: str = ''
    image_path: str | None = None
    audio_path: str | None = None

    def validate(self) -> None:
        _text(self.id, 'scene.id')
        _int(self.start_ms, 'scene.start_ms')
        _int(self.duration_ms, 'scene.duration_ms', minimum=1)
        _text(self.text, 'scene.text', required=False)
        for name in ('image_path', 'audio_path'):
            value = getattr(self, name)
            if value is not None:
                _text(value, f'scene.{name}')


@dataclass(frozen=True)
class Track:
    id: str
    kind: str
    label: str = ''

    def validate(self) -> None:
        _text(self.id, 'track.id')
        if self.kind not in TRACK_KINDS:
            raise ValueError('unsupported track.kind')
        _text(self.label, 'track.label', required=False)


@dataclass(frozen=True)
class Subtitle:
    id: str
    track_id: str
    start_ms: int
    duration_ms: int
    text: str
    locale: str

    def validate(self) -> None:
        _text(self.id, 'subtitle.id')
        _text(self.track_id, 'subtitle.track_id')
        _int(self.start_ms, 'subtitle.start_ms')
        _int(self.duration_ms, 'subtitle.duration_ms', minimum=1)
        _text(self.text, 'subtitle.text')
        if self.locale not in SUPPORTED_LOCALES:
            raise ValueError('unsupported subtitle.locale')


@dataclass(frozen=True)
class Clip:
    id: str
    track_id: str
    media_id: str
    start_ms: int
    duration_ms: int
    source_in_ms: int = 0

    def validate(self) -> None:
        _text(self.id, 'clip.id')
        _text(self.track_id, 'clip.track_id')
        _text(self.media_id, 'clip.media_id')
        _int(self.start_ms, 'clip.start_ms')
        _int(self.duration_ms, 'clip.duration_ms', minimum=1)
        _int(self.source_in_ms, 'clip.source_in_ms')


@dataclass(frozen=True)
class MediaAsset:
    id: str
    kind: str
    path: str

    def validate(self) -> None:
        from core.media_paths import validate_media_path
        _text(self.id, 'media.id')
        if self.kind not in {'image', 'video', 'audio'}:
            raise ValueError('unsupported media.kind')
        validate_media_path(self.path)


@dataclass(frozen=True)
class Project:
    title: str
    content_locale: str
    scenes: tuple[Scene, ...]
    fps: float = 25.0
    width: int = 1920
    height: int = 1080
    schema_version: int = SCHEMA_VERSION
    tracks: tuple[Track, ...] = ()
    subtitles: tuple[Subtitle, ...] = ()
    media: tuple[MediaAsset, ...] = ()
    clips: tuple[Clip, ...] = ()

    def validate(self) -> None:
        if type(self.schema_version) is not int or self.schema_version != SCHEMA_VERSION:
            raise ValueError('unsupported schema_version')
        _text(self.title, 'title')
        if self.content_locale not in SUPPORTED_LOCALES:
            raise ValueError('content_locale must be ru or uk')
        if isinstance(self.fps, bool) or not isinstance(self.fps, (int, float)) or not math.isfinite(self.fps) or not 1 <= self.fps <= 240:
            raise ValueError('fps out of range')
        _int(self.width, 'width', minimum=1)
        _int(self.height, 'height', minimum=1)
        if self.width > 16384 or self.height > 16384:
            raise ValueError('resolution out of range')
        if not isinstance(self.scenes, tuple) or not isinstance(self.tracks, tuple) or not isinstance(self.subtitles, tuple) or not isinstance(self.media, tuple) or not isinstance(self.clips, tuple):
            raise ValueError('scenes, tracks and subtitles must be tuples')
        scene_ids: set[str] = set()
        for scene in self.scenes:
            if not isinstance(scene, Scene):
                raise ValueError('invalid scene object')
            scene.validate()
            if scene.id in scene_ids:
                raise ValueError('duplicate scene id')
            scene_ids.add(scene.id)
        track_ids: dict[str, str] = {}
        for track in self.tracks:
            if not isinstance(track, Track):
                raise ValueError('invalid track object')
            track.validate()
            if track.id in track_ids:
                raise ValueError('duplicate track id')
            track_ids[track.id] = track.kind
        subtitle_ids: set[str] = set()
        for subtitle in self.subtitles:
            if not isinstance(subtitle, Subtitle):
                raise ValueError('invalid subtitle object')
            subtitle.validate()
            if subtitle.id in subtitle_ids:
                raise ValueError('duplicate subtitle id')
            subtitle_ids.add(subtitle.id)
            if track_ids.get(subtitle.track_id) != 'subtitle':
                raise ValueError('subtitle must reference a subtitle track')

        media_ids: dict[str, str] = {}
        for asset in self.media:
            if not isinstance(asset, MediaAsset):
                raise ValueError('invalid media object')
            asset.validate()
            if asset.id in media_ids:
                raise ValueError('duplicate media id')
            media_ids[asset.id] = asset.kind
        clip_ids: set[str] = set()
        for clip in self.clips:
            if not isinstance(clip, Clip):
                raise ValueError('invalid clip object')
            clip.validate()
            if clip.id in clip_ids:
                raise ValueError('duplicate clip id')
            clip_ids.add(clip.id)
            kind = track_ids.get(clip.track_id)
            media_kind = media_ids.get(clip.media_id)
            if kind not in ('video', 'audio') or media_kind is None:
                raise ValueError('clip must reference valid track and media')
            if kind == 'audio' and media_kind != 'audio':
                raise ValueError('audio track requires audio media')
            if kind == 'video' and media_kind not in ('video', 'image'):
                raise ValueError('video track requires video or image media')

    def to_dict(self) -> dict:
        self.validate()
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, payload: dict) -> 'Project':
        if not isinstance(payload, dict):
            raise ValueError('project must be an object')
        version = payload.get('schema_version')
        if type(version) is not int:
            raise ValueError('schema_version must be an integer')
        if version == 1:
            _exact(payload, {'title', 'content_locale', 'scenes', 'fps', 'width', 'height', 'schema_version'}, 'v1 project')
            payload = {**payload, 'tracks': [], 'subtitles': []}
        elif version not in (2, SCHEMA_VERSION):
            raise ValueError('unsupported schema_version')
        if version in (1, 2):
            if version == 2:
                _exact(payload, {'title', 'content_locale', 'scenes', 'fps', 'width', 'height', 'schema_version', 'tracks', 'subtitles'}, 'v2 project')
            payload = {**payload, 'schema_version': SCHEMA_VERSION, 'media': [], 'clips': []}
        _exact(payload, {'title', 'content_locale', 'scenes', 'fps', 'width', 'height', 'schema_version', 'tracks', 'subtitles', 'media', 'clips'}, 'project')
        specs = (
            ('scenes', Scene, {'id', 'start_ms', 'duration_ms', 'text', 'image_path', 'audio_path'}),
            ('tracks', Track, {'id', 'kind', 'label'}),
            ('subtitles', Subtitle, {'id', 'track_id', 'start_ms', 'duration_ms', 'text', 'locale'}),
            ('media', MediaAsset, {'id', 'kind', 'path'}),
            ('clips', Clip, {'id', 'track_id', 'media_id', 'start_ms', 'duration_ms', 'source_in_ms'}),
        )
        converted = dict(payload)
        for field, cls_type, expected in specs:
            if not isinstance(payload[field], list):
                raise ValueError(f'{field} must be a list')
            values = []
            for item in payload[field]:
                _exact(item, expected, field)
                values.append(cls_type(**item))
            converted[field] = tuple(values)
        project = cls(**converted)
        project.validate()
        return project

    @classmethod
    def from_json(cls, text: str) -> 'Project':
        return cls.from_dict(json.loads(text))
