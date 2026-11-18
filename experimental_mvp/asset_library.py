"""Local experimental library. No network, production authority, or secure-store claim.

SQLite serializes writers, including imports/recovery. Binaries are never deleted or
replaced; incomplete publications are retained for verified reuse on a later import.
"""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import stat
import subprocess
import tempfile
import uuid

IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
VIDEO_EXT = {'.mp4', '.mov', '.mkv', '.webm'}
RIGHTS = {'UNKNOWN', 'PENDING_REVIEW', 'CLEARED_FOR_EXPERIMENT', 'RESTRICTED', 'REJECTED'}
SOURCES = {'MANUAL', 'AI_GENERATED', 'DERIVED', 'EXTERNAL_LICENSED', 'UNKNOWN'}
UNKNOWN = 'UNKNOWN'


class LibraryError(ValueError):
    def __init__(self, code, message=''):
        self.code = code
        super().__init__(code + (': ' + message if message else ''))


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def now():
    return datetime.now(timezone.utc).isoformat()


def safe_path(path, *, directory=False):
    raw = os.fspath(path)
    p = Path(raw).expanduser()
    if not p.is_absolute() or '..' in p.parts or raw.startswith(('\\\\', '//')) or '\x00' in raw:
        raise LibraryError('UNSAFE_PATH')
    if os.name == 'nt' and (':' in str(p)[2:] or str(p).startswith('\\\\')):
        raise LibraryError('UNSAFE_PATH')
    for part in [*reversed(p.parents), p]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise LibraryError('UNSAFE_PATH', 'symlink/reparse point')
    if p.exists() and directory and not p.is_dir():
        raise LibraryError('UNSAFE_PATH', 'not directory')
    return p


def file_identity(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def digest(path):
    safe_path(path)
    h = sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def anchor_token(anchor):
    """Compare all editing fields, not just generation prompt fingerprint."""
    return sha256(encoded(anchor).encode()).hexdigest()


def find_anchor(project, anchor_id):
    matches = [a for s in project.get('scenes', []) for a in s.get('anchors', [])
               if a.get('anchor_id') == anchor_id]
    if len(matches) != 1:
        raise LibraryError('STALE_TARGET', 'anchor deleted or ambiguous')
    return matches[0]


def metadata(provenance=None, rights=None, tags=None):
    if any(value is not None and not isinstance(value, dict) for value in (provenance, rights)):
        raise LibraryError('INVALID_METADATA', 'provenance/rights must be objects')
    if tags is not None and not isinstance(tags, list):
        raise LibraryError('INVALID_METADATA', 'tags must be list')
    provenance = deepcopy(provenance or {})
    rights = deepcopy(rights or {})
    defaults = dict(source_type='UNKNOWN', provider=UNKNOWN, model=UNKNOWN,
                    provider_job_id=UNKNOWN, generation_timestamp=UNKNOWN,
                    prompt_reference=UNKNOWN, input_asset_references=[], source_sha256=UNKNOWN)
    rdefaults = dict(rights_status=UNKNOWN, license_reference=UNKNOWN, commercial_use=UNKNOWN,
                     attribution_required=UNKNOWN, territory=UNKNOWN, expiration=UNKNOWN,
                     watermark_status=UNKNOWN, review_reference=UNKNOWN)
    if set(provenance) - set(defaults) or set(rights) - set(rdefaults):
        raise LibraryError('INVALID_METADATA', 'unknown fields')
    defaults.update(provenance); rdefaults.update(rights)
    if not isinstance(defaults['source_type'], str) or not isinstance(rdefaults['rights_status'], str) or defaults['source_type'] not in SOURCES or rdefaults['rights_status'] not in RIGHTS:
        raise LibraryError('INVALID_METADATA', 'enum')
    for obj in (defaults, rdefaults):
        for k, v in obj.items():
            if k == 'input_asset_references':
                if not isinstance(v, list) or len(v) > 100 or any(not isinstance(x, str) or len(x) > 256 for x in v):
                    raise LibraryError('INVALID_METADATA', k)
            elif k in ('commercial_use', 'attribution_required'):
                if type(v) is not bool and v != UNKNOWN:
                    raise LibraryError('INVALID_METADATA', k)
            elif not isinstance(v, str) or not v or len(v) > 4096 or '\x00' in v:
                raise LibraryError('INVALID_METADATA', k)
    expiry = rdefaults['expiration']
    if expiry not in (UNKNOWN, 'NOT_APPLICABLE'):
        try:
            value = datetime.fromisoformat(expiry.replace('Z', '+00:00'))
            if value.tzinfo is None: raise ValueError()
        except (ValueError, TypeError):
            raise LibraryError('INVALID_METADATA', 'expiration must include timezone')
    if defaults['source_sha256'] != UNKNOWN and not re.fullmatch('[0-9a-f]{64}', defaults['source_sha256']):
        raise LibraryError('INVALID_METADATA', 'source_sha256')
    tags = deepcopy(tags or [])
    if not isinstance(tags, list) or len(tags) > 100 or any(not isinstance(t, str) or not t or len(t) > 100 for t in tags):
        raise LibraryError('INVALID_METADATA', 'tags')
    return defaults, rdefaults, sorted(set(tags))


class AssetLibrary:
    def __init__(self, root, *, create=True, max_bytes=128*1024*1024, max_duration=120,
                 max_pixels=32_000_000, timeout=20, fault=None):
        self.root = safe_path(root, directory=True)
        self.max_bytes, self.max_duration, self.max_pixels = max_bytes, max_duration, max_pixels
        self.timeout, self.fault = timeout, fault
        if create:
            self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
            for name in ('objects', 'staging', 'thumbnails'):
                safe_path(self.root / name, directory=True).mkdir(exist_ok=True, mode=0o700)
        self.db = safe_path(self.root / 'catalog.sqlite3')
        if not create and not self.db.is_file():
            raise LibraryError('LIBRARY_MISSING')
        for name in ('objects', 'staging', 'thumbnails'):
            safe_path(self.root / name, directory=True)
        if create:
            with self.connection() as db:
                version = db.execute('PRAGMA user_version').fetchone()[0]
                if version not in (0, 1) or (version == 0 and db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchone()):
                    raise LibraryError('SCHEMA_VERSION', 'no implicit migration')
                try:
                    db.execute("SELECT json_valid('{}')").fetchone()
                except sqlite3.OperationalError as exc:
                    raise LibraryError('SQLITE_JSON1_REQUIRED') from exc
                db.executescript('''
                BEGIN IMMEDIATE;
                CREATE TABLE IF NOT EXISTS assets(id TEXT PRIMARY KEY, revision INTEGER NOT NULL,
                    integrity TEXT NOT NULL, lifecycle TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS revisions(id TEXT, revision INTEGER, data TEXT NOT NULL,
                    PRIMARY KEY(id,revision), FOREIGN KEY(id) REFERENCES assets(id));
                CREATE TABLE IF NOT EXISTS imports(id TEXT PRIMARY KEY, state TEXT NOT NULL,
                    stage TEXT NOT NULL, object_ref TEXT, asset_id TEXT);
                CREATE TABLE IF NOT EXISTS links(id TEXT PRIMARY KEY, project TEXT NOT NULL,
                    anchor TEXT NOT NULL, asset TEXT NOT NULL, revision INTEGER NOT NULL,
                    detached INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS derivatives(key TEXT PRIMARY KEY, data TEXT NOT NULL);
                PRAGMA user_version=1;
                COMMIT;
                ''')
        with self.connection() as db:
            if db.execute('PRAGMA user_version').fetchone()[0] != 1:
                raise LibraryError('SCHEMA_VERSION')

    @contextmanager
    def connection(self, *, write=False):
        safe_path(self.db)
        for suffix in ('-journal', '-wal', '-shm'):
            safe_path(Path(str(self.db) + suffix))
        db = sqlite3.connect(self.db, timeout=90)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('PRAGMA synchronous=FULL')
            if write: db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def hit(self, phase):
        if self.fault: self.fault(phase)

    def managed(self, ref):
        p = Path(ref)
        if p.is_absolute() or '..' in p.parts or len(p.parts) != 2 or p.parts[0] not in ('objects', 'staging', 'thumbnails'):
            raise LibraryError('UNSAFE_STORAGE_REFERENCE')
        return safe_path(self.root / p)

    def _run(self, args):
        # Child output is spooled, not accumulated as unbounded RAM. No shell or network protocols.
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            try:
                result = subprocess.run(args, stdout=out, stderr=err, timeout=self.timeout, check=False,
                                        stdin=subprocess.DEVNULL)
            except subprocess.TimeoutExpired as exc:
                raise LibraryError('PROCESS_TIMEOUT') from exc
            if result.returncode:
                raise LibraryError('MEDIA_VALIDATION_FAILED', 'decoder/probe returned nonzero')
            if out.tell() > 1024*1024 or err.tell() > 1024*1024:
                raise LibraryError('INVALID_TOOL_OUTPUT')
            out.seek(0)
            return out.read()

    def technical(self, path, media_type):
        from experimental_mvp.pipeline import executable
        probe = self._run([executable('ffprobe'), '-v', 'error', '-protocol_whitelist', 'file,pipe',
                           '-show_entries', 'format=format_name,duration:stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames,pix_fmt,channels,sample_rate',
                           '-of', 'json', str(path)])
        try:
            value = json.loads(probe)
            streams = value['streams']; videos = [s for s in streams if s.get('codec_type') == 'video']
            if len(videos) != 1 or len(streams) > 8: raise ValueError()
            v = videos[0]; w, h = v['width'], v['height']
            if type(w) is not int or type(h) is not int or not 0 < w <= 8192 or not 0 < h <= 8192 or w*h > self.max_pixels:
                raise LibraryError('MEDIA_LIMIT')
            fmt = value['format']['format_name']
            expected = {'.png': 'png', '.jpg': 'jpeg', '.jpeg': 'jpeg', '.bmp': 'bmp', '.webp': 'webp'}
            if media_type == 'image' and v['codec_name'] != expected[path.suffix.lower()]: raise ValueError()
            if media_type == 'video' and not any(x in fmt.split(',') for x in ('mov', 'mp4', 'matroska', 'webm')): raise ValueError()
            duration = UNKNOWN
            if media_type == 'video':
                duration = float(value['format']['duration'])
                if not math.isfinite(duration) or not 0 < duration <= self.max_duration: raise LibraryError('MEDIA_LIMIT')
            fps = UNKNOWN
            try:
                rate = Fraction(v.get('avg_frame_rate', '0/0'))
                if rate > 0: fps = str(rate)
            except (ValueError, ZeroDivisionError): pass
            count = v.get('nb_frames', UNKNOWN)
            count = int(count) if isinstance(count, str) and count.isdigit() else UNKNOWN
            result = dict(container=fmt, video_codec=v['codec_name'] if media_type == 'video' else UNKNOWN,
                          image_format=v['codec_name'] if media_type == 'image' else UNKNOWN,
                          width=w, height=h, frame_rate=fps if media_type == 'video' else UNKNOWN,
                          duration=duration, frame_count=count if media_type == 'video' else UNKNOWN,
                          audio_streams=[s for s in streams if s.get('codec_type') == 'audio'],
                          color_mode=v.get('pix_fmt', UNKNOWN), technical_status='VALID')
        except LibraryError: raise
        except (ValueError, KeyError, TypeError) as exc:
            raise LibraryError('INVALID_TOOL_OUTPUT') from exc
        args = [executable('ffmpeg'), '-v', 'error', '-xerror', '-nostdin', '-protocol_whitelist', 'file,pipe',
                '-threads', '1', '-i', str(path), '-map', '0:v:0']
        if media_type == 'image': args += ['-frames:v', '1']
        else: args += ['-map', '0:a?']
        self._run(args + ['-f', 'null', '-'])
        return result

    def import_file(self, source, *, provenance=None, rights=None, tags=None):
        prov, law, tags = metadata(provenance, rights, tags)
        source = safe_path(source)
        suffix = source.suffix.lower()
        if suffix not in IMAGE_EXT | VIDEO_EXT: raise LibraryError('UNSUPPORTED_FORMAT')
        media_type = 'image' if suffix in IMAGE_EXT else 'video'
        if any(ord(c)<32 or c in ':\\' for c in source.name) or source.name.endswith((' ', '.')) or source.stem.upper() in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}:
            raise LibraryError('UNSAFE_FILENAME')
        before = source.stat()
        if not stat.S_ISREG(before.st_mode): raise LibraryError('UNSAFE_SOURCE')
        if not 0 < before.st_size <= self.max_bytes: raise LibraryError('SIZE_LIMIT')
        iid, aid = uuid.uuid4().hex, uuid.uuid4().hex
        stage_ref = 'staging/' + iid + suffix
        stage = self.managed(stage_ref)
        with self.connection(write=True) as db:
            db.execute('INSERT INTO imports VALUES(?,?,?,?,?)', (iid, 'PENDING', stage_ref, None, aid))
        try:
            with self.connection(write=True) as db:
                if db.execute('SELECT state FROM imports WHERE id=?', (iid,)).fetchone()[0] != 'PENDING':
                    raise LibraryError('IMPORT_ABORTED_BY_RECOVERY')
                self.hit('source_checked')
                flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0)
                fd = os.open(source, flags)
                with os.fdopen(fd, 'rb') as src:
                    opened = os.fstat(src.fileno())
                    if file_identity(before) != file_identity(opened) or not stat.S_ISREG(opened.st_mode):
                        raise LibraryError('SOURCE_CHANGED')
                    total, h = 0, sha256()
                    with stage.open('xb') as dst:
                        while True:
                            data = src.read(1024*1024)
                            if not data: break
                            total += len(data)
                            if total > self.max_bytes: raise LibraryError('SIZE_LIMIT')
                            dst.write(data); h.update(data); self.hit('copy_chunk')
                        self.hit('staging_written')
                        dst.flush(); os.fsync(dst.fileno())
                    safe_path(source)
                    if file_identity(opened) != file_identity(os.fstat(src.fileno())) or file_identity(opened) != file_identity(source.stat()):
                        raise LibraryError('SOURCE_CHANGED')
                sh = h.hexdigest()
                if prov['source_sha256'] not in (UNKNOWN, sh): raise LibraryError('SOURCE_HASH_MISMATCH')
                prov['source_sha256'] = sh
                if total != before.st_size or digest(stage) != sh: raise LibraryError('STAGING_CORRUPTED')
                self.hit('before_validation')
                tech = self.technical(stage, media_type)
                if digest(stage) != sh: raise LibraryError('STAGING_CORRUPTED')
                # Same bytes share a single object even when source suffixes differ.
                existing = db.execute("SELECT data FROM revisions WHERE json_extract(data,'$.sha256')=? ORDER BY id,revision LIMIT 1", (sh,)).fetchone()
                ref = json.loads(existing[0])['storage_reference'] if existing else 'objects/' + sh + suffix
                target = self.managed(ref)
                self.hit('before_publication')
                if target.exists():
                    if digest(target) != sh: raise LibraryError('OBJECT_CORRUPTED', 'never overwrite existing object')
                else:
                    # Serialized writer/recovery; same-filesystem rename, never replace another object.
                    stage.rename(target)
                self.hit('after_publication')
                if digest(target) != sh: raise LibraryError('OBJECT_CORRUPTED')
                prov['import_timestamp'] = now()
                record = dict(asset_id=aid, schema_version=1, revision=1, sha256=sh, byte_size=total,
                              media_type=media_type, original_filename=source.name, storage_reference=ref,
                              created_at=now(), updated_at=now(), technical=tech, provenance=prov,
                              rights=law, tags=tags)
                db.execute('INSERT INTO assets VALUES(?,?,?,?)', (aid, 1, 'VALID', 'ACTIVE'))
                db.execute('INSERT INTO revisions VALUES(?,?,?)', (aid, 1, encoded(record)))
                self.hit('before_db_commit')
                db.execute('UPDATE imports SET state=?,object_ref=? WHERE id=?', ('COMMITTED', ref, iid))
            return self.get(aid)
        except Exception:
            with self.connection(write=True) as db:
                db.execute("UPDATE imports SET state='ABORTED' WHERE id=? AND state='PENDING'", (iid,))
            raise
        finally:
            stage.unlink(missing_ok=True)

    def _get(self, db, aid, revision=None):
        status = db.execute('SELECT * FROM assets WHERE id=?', (aid,)).fetchone()
        if status is None: raise LibraryError('ASSET_NOT_FOUND')
        rev = status['revision'] if revision is None else revision
        if type(rev) is not int or rev < 1: raise LibraryError('INVALID_REVISION')
        row = db.execute('SELECT data FROM revisions WHERE id=? AND revision=?', (aid, rev)).fetchone()
        if row is None: raise LibraryError('REVISION_NOT_FOUND')
        result = json.loads(row[0])
        result.update(integrity_status=status['integrity'], lifecycle_status=status['lifecycle'], current_revision=status['revision'])
        return result

    def get(self, aid, revision=None):
        with self.connection() as db: return self._get(db, aid, revision)

    def update_metadata(self, aid, *, expected_revision, provenance=None, rights=None, tags=None):
        with self.connection(write=True) as db:
            record = self._get(db, aid)
            if record['revision'] != expected_revision: raise LibraryError('STALE_REVISION')
            p, r, t = metadata(provenance if provenance is not None else {k:v for k,v in record['provenance'].items() if k != 'import_timestamp'},
                               rights if rights is not None else record['rights'], tags if tags is not None else record['tags'])
            if p['source_sha256'] not in (UNKNOWN, record['sha256']): raise LibraryError('SOURCE_HASH_MISMATCH')
            p['source_sha256'] = record['sha256']
            p['import_timestamp'] = record['provenance']['import_timestamp']
            for k in ('integrity_status', 'lifecycle_status', 'current_revision'): record.pop(k)
            record.update(provenance=p, rights=r, tags=t, revision=expected_revision+1, updated_at=now())
            db.execute('INSERT INTO revisions VALUES(?,?,?)', (aid, record['revision'], encoded(record)))
            db.execute('UPDATE assets SET revision=? WHERE id=?', (record['revision'], aid))
        return self.get(aid)

    def retire(self, aid):
        with self.connection(write=True) as db:
            self._get(db, aid)
            db.execute("UPDATE assets SET lifecycle='RETIRED' WHERE id=?", (aid,))
        return self.get(aid)

    def _verify(self, db, aid):
        record = self._get(db, aid)
        try:
            path = self.managed(record['storage_reference'])
            integrity = 'MISSING' if not path.exists() else 'VALID' if path.stat().st_size == record['byte_size'] and digest(path) == record['sha256'] else 'CORRUPTED'
        except FileNotFoundError:
            integrity = 'MISSING'
        except (OSError, LibraryError):
            integrity = 'CORRUPTED'
        lifecycle = record['lifecycle_status']
        if lifecycle != 'RETIRED':
            lifecycle = 'ACTIVE' if integrity == 'VALID' and record['technical']['technical_status'] == 'VALID' else integrity if integrity != 'VALID' else 'QUARANTINED'
        db.execute('UPDATE assets SET integrity=?,lifecycle=? WHERE id=?', (integrity, lifecycle, aid))
        return dict(asset_id=aid, integrity_status=integrity, lifecycle_status=lifecycle)

    def verify_asset(self, aid):
        with self.connection(write=True) as db: return self._verify(db, aid)

    def verify_library(self):
        with self.connection(write=True) as db:
            return [self._verify(db, row[0]) for row in db.execute('SELECT id FROM assets ORDER BY id').fetchall()]

    def list_missing_assets(self):
        return [r for r in self.verify_library() if r['integrity_status'] == 'MISSING']

    def list_corrupted_assets(self):
        return [r for r in self.verify_library() if r['integrity_status'] == 'CORRUPTED']

    def recover_incomplete_imports(self):
        with self.connection(write=True) as db:
            pending = db.execute("SELECT * FROM imports WHERE state='PENDING' ORDER BY id").fetchall()
            for row in pending:
                self.managed(row['stage']).unlink(missing_ok=True)
                db.execute("UPDATE imports SET state='ABORTED' WHERE id=?", (row['id'],))
            # Only our UUID staging names; never arbitrary user paths or external files.
            cleaned = []
            for path in sorted((self.root / 'staging').iterdir()):
                if re.fullmatch(r'[0-9a-f]{32}\.(png|jpg|jpeg|webp|bmp|mp4|mov|mkv|webm)', path.name):
                    safe_path(path).unlink(); cleaned.append(path.name)
            verified = [self._verify(db, r[0]) for r in db.execute('SELECT id FROM assets ORDER BY id').fetchall()]
            return dict(aborted_imports=[r['id'] for r in pending], cleaned_staging=cleaned, verified=verified)

    def search(self, *, offset=0, limit=50, **filters):
        fields = {'asset_id':'asset_id', 'media_type':'media_type', 'provider':'provenance.provider',
                  'model':'provenance.model', 'rights_status':'rights.rights_status',
                  'technical_status':'technical.technical_status', 'sha256':'sha256'}
        allowed = set(fields) | {'date_from','date_to','project_id','anchor_id','tag'}
        if set(filters)-allowed or type(offset) is not int or type(limit) is not int or offset < 0 or not 1 <= limit <= 200:
            raise LibraryError('INVALID_SEARCH')
        clauses, args = [], []
        for k,v in filters.items():
            if not isinstance(v,str): raise LibraryError('INVALID_SEARCH')
            if k in fields:
                clauses.append('json_extract(r.data,?)=?'); args += ['$.'+fields[k],v]
            elif k in ('date_from','date_to'):
                clauses.append('json_extract(r.data,\'$.created_at\')'+('>=' if k=='date_from' else '<=')+'?'); args.append(v)
            elif k == 'tag':
                clauses.append("EXISTS(SELECT 1 FROM json_each(r.data,'$.tags') WHERE value=?)"); args.append(v)
            else:
                column = 'project' if k=='project_id' else 'anchor'
                clauses.append(f'EXISTS(SELECT 1 FROM links l WHERE l.asset=a.id AND l.{column}=?)'); args.append(v)
        sql = 'SELECT a.id FROM assets a JOIN revisions r ON a.id=r.id AND a.revision=r.revision'
        if clauses: sql += ' WHERE '+' AND '.join(clauses)
        sql += ' ORDER BY a.id LIMIT ? OFFSET ?'; args += [limit,offset]
        with self.connection() as db:
            return [self._get(db,row[0]) for row in db.execute(sql,args).fetchall()]

    def resolve(self, aid, revision, *, action='EXPERIMENTAL_PREVIEW'):
        if action not in ('EXPERIMENTAL_PREVIEW','EXPERIMENTAL_EXPORT'):
            raise LibraryError('PRODUCTION_NOT_AUTHORIZED')
        with self.connection(write=True) as db:
            state = self._verify(db, aid)
            record = self._get(db, aid, revision)
            # Operational verification persists even when subsequent policy checks refuse.
        if state['integrity_status'] != 'VALID' or state['lifecycle_status'] != 'ACTIVE': raise LibraryError('ASSET_UNAVAILABLE')
        if record['technical']['technical_status'] != 'VALID': raise LibraryError('INVALID_TECHNICAL_STATUS')
        if record['current_revision'] != revision: raise LibraryError('ASSET_REVISION_CHANGED')
        law = record['rights']
        if law['rights_status'] != 'CLEARED_FOR_EXPERIMENT' or any(law[k] == UNKNOWN for k in ('license_reference','review_reference','territory','watermark_status')):
            raise LibraryError('RIGHTS_NOT_CLEARED')
        if any(law[k] == UNKNOWN for k in ('commercial_use','attribution_required','expiration')):
            raise LibraryError('RIGHTS_NOT_CLEARED')
        if law['expiration'] not in (UNKNOWN,'NOT_APPLICABLE') and datetime.fromisoformat(law['expiration'].replace('Z','+00:00')) <= datetime.now(timezone.utc):
            raise LibraryError('RIGHTS_EXPIRED')
        return self.managed(record['storage_reference'])

    def attach(self, project, project_id, anchor_id, aid, revision, *, expected_anchor, replace=False):
        anchor = find_anchor(project, anchor_id)
        if anchor_token(anchor) != expected_anchor: raise LibraryError('STALE_TARGET')
        if (anchor.get('asset_library_binding') or anchor.get('local_asset_path')) and not replace:
            raise LibraryError('EXPLICIT_REPLACE_REQUIRED')
        path = self.resolve(aid, revision)
        record = self.get(aid, revision)
        self.hit('before_attach')
        if find_anchor(project,anchor_id) is not anchor or anchor_token(anchor) != expected_anchor:
            raise LibraryError('STALE_TARGET')
        link = uuid.uuid4().hex
        binding = dict(library_root=str(self.root), asset_id=aid, revision=revision,
                       sha256=record['sha256'], link_id=link, project_id=project_id)
        previous = {k:deepcopy(anchor[k]) for k in ('local_asset_path','asset_sha256','license_status','generation_status','provenance','asset_library_binding') if k in anchor}
        binding['previous'] = previous
        with self.connection(write=True) as db:
            self._verify(db, aid)
            current = self._get(db, aid)
            if current['revision'] != revision: raise LibraryError('ASSET_REVISION_CHANGED')
            if current['lifecycle_status'] != 'ACTIVE' or current['integrity_status'] != 'VALID': raise LibraryError('ASSET_UNAVAILABLE')
            db.execute('INSERT INTO links VALUES(?,?,?,?,?,0)', (link,project_id,anchor_id,aid,revision))
        anchor.update(asset_library_binding=binding, local_asset_path=str(path), asset_sha256=record['sha256'],
                      license_status='CLEARED_FOR_EXPERIMENT', generation_status='IMPORTED')
        return binding

    def detach(self, project, anchor_id, *, expected_anchor):
        anchor = find_anchor(project,anchor_id)
        if anchor_token(anchor) != expected_anchor: raise LibraryError('STALE_TARGET')
        binding = anchor.get('asset_library_binding')
        if not binding: raise LibraryError('NOT_ATTACHED')
        if binding['library_root'] != str(self.root): raise LibraryError('WRONG_LIBRARY')
        with self.connection(write=True) as db:
            db.execute('UPDATE links SET detached=1 WHERE id=?', (binding['link_id'],))
        for key in ('local_asset_path','asset_sha256','license_status','generation_status','provenance'):
            anchor.pop(key,None)
        anchor.pop('asset_library_binding')
        anchor.update(deepcopy(binding['previous']))

    def thumbnail(self, aid, revision, *, size=256):
        if type(size) is not int or not 16 <= size <= 512: raise LibraryError('INVALID_THUMBNAIL_SIZE')
        # Catalog previews do not grant rights to attach/export; UNKNOWN rights may be inspected locally.
        self.verify_asset(aid); record = self.get(aid,revision)
        if record['integrity_status'] != 'VALID' or record['technical']['technical_status'] != 'VALID': raise LibraryError('ASSET_UNAVAILABLE')
        from experimental_mvp.pipeline import executable
        tool = self._run([executable('ffmpeg'), '-version']).decode().splitlines()[0]
        key = sha256(encoded([aid,revision,record['sha256'],size,tool,'poster-first-frame-v1']).encode()).hexdigest()
        ref = 'thumbnails/'+key+'.png'; target = self.managed(ref)
        with self.connection(write=True) as db:
            old = db.execute('SELECT data FROM derivatives WHERE key=?',(key,)).fetchone()
            if old and target.exists() and digest(target)==json.loads(old[0])['sha256']: return json.loads(old[0])
            tmp = self.managed('staging/'+uuid.uuid4().hex+'.png')
            try:
                self._run([executable('ffmpeg'),'-v','error','-nostdin','-protocol_whitelist','file,pipe','-threads','1',
                           '-i',str(self.managed(record['storage_reference'])),'-frames:v','1','-vf',
                           f'scale={size}:{size}:force_original_aspect_ratio=decrease','-threads','1','-update','1',str(tmp)])
                if not tmp.is_file() or tmp.stat().st_size > 2*1024*1024: raise LibraryError('INVALID_THUMBNAIL')
                self.technical(tmp,'image')
                if digest(self.managed(record['storage_reference'])) != record['sha256']:
                    raise LibraryError('SOURCE_CHANGED')
                derived = dict(source_type='DERIVED', parent_asset_id=aid, parent_revision=revision,
                               source_sha256=record['sha256'], sha256=digest(tmp), storage_reference=ref,
                               params=dict(size=size,algorithm='poster-first-frame-v1'),tool_version=tool)
                tmp.replace(target)
                db.execute('INSERT OR REPLACE INTO derivatives VALUES(?,?)',(key,encoded(derived)))
                return derived
            finally: tmp.unlink(missing_ok=True)


def resolve_anchor(anchor):
    binding = anchor.get('asset_library_binding')
    if not binding: return Path(anchor['local_asset_path'])
    library = AssetLibrary(binding['library_root'],create=False)
    path = library.resolve(binding['asset_id'],binding['revision'])
    if str(path) != anchor.get('local_asset_path') or binding['sha256'] != anchor.get('asset_sha256') or digest(path) != binding['sha256']:
        raise LibraryError('BINDING_MISMATCH')
    return path
