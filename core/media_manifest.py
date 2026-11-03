"""Editor-neutral media inventory for v2 projects. No files are read or copied.

References are relative to the project media root. This deliberately rejects
absolute paths and traversal, including Windows paths when run on Linux.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from core.media_paths import validate_media_path
from core.project_schema import Project

_KINDS = {'image', 'audio'}

@dataclass(frozen=True)
class MediaReference:
    id: str
    scene_id: str
    kind: str
    path: str

    def validate(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError('invalid media id')
        if not isinstance(self.scene_id, str) or not self.scene_id.strip():
            raise ValueError('invalid scene id')
        if self.kind not in _KINDS:
            raise ValueError('unsupported media kind')
        validate_media_path(self.path)


def manifest_for_project(project: Project) -> dict:
    project.validate()
    refs = []
    for scene in project.scenes:
        for kind, field in (('image', 'image_path'), ('audio', 'audio_path')):
            path = getattr(scene, field)
            if path is not None:
                ref = MediaReference(f'{scene.id}:{kind}', scene.id, kind, validate_media_path(path))
                ref.validate()
                refs.append(asdict(ref))
    return {'manifest_version': 1, 'project_schema_version': project.schema_version,
            'content_locale': project.content_locale, 'media': refs}


def manifest_json(project: Project) -> str:
    return json.dumps(manifest_for_project(project), ensure_ascii=False, indent=2) + '\n'
