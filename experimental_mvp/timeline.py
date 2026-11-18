"""Pure, transactional experimental editing and explicit audio-timing provenance.

No production contracts or storage are implemented here. Operations receive measured
milliseconds; probing and Tk are adapters, not prerequisites for the editing model.
"""
from copy import deepcopy
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from pathlib import Path
import uuid

MEASURED_AUDIO_DURATION = 'MEASURED_AUDIO_DURATION'
ESTIMATED_SCENE_BOUNDARY = 'ESTIMATED_SCENE_BOUNDARY'
MANUAL_SCENE_BOUNDARY = 'MANUAL_SCENE_BOUNDARY'
ESTIMATED_CAPTION_TIMING = 'ESTIMATED_CAPTION_TIMING'
MANUAL_CAPTION_TIMING = 'MANUAL_CAPTION_TIMING'


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'Ожидается целое число >= {minimum}.')
    return value


def validate_project(project):
    """Draft shape validation: gaps/conflicts remain editable, never silently repaired."""
    if not isinstance(project, dict) or not isinstance(project.get('scenes'), list):
        raise ValueError('Проект требует scenes.')
    ids, anchors = set(), set()
    for scene in project['scenes']:
        sid = scene.get('id')
        if not isinstance(sid, str) or not sid or sid in ids:
            raise ValueError('Отсутствующий/повторный ID сцены.')
        ids.add(sid)
        for a in scene.get('anchors', []):
            aid = a.get('anchor_id')
            if not isinstance(aid, str) or not aid or aid in anchors or a.get('scene_id') != sid:
                raise ValueError('Неверный или повторный ID якоря/сцены.')
            anchors.add(aid)
            integer(a['start_ms']); integer(a['duration_ms'], 1)
            integer(a.get('source_start_ms', 0))
            if 'source_end_ms' in a:
                if integer(a['source_end_ms'], 1) <= a.get('source_start_ms', 0):
                    raise ValueError('Пустой исходный интервал.')
            if a.get('short_clip_policy', 'ERROR') not in ('ERROR', 'HOLD_LAST_FRAME', 'LOOP'):
                raise ValueError('Неизвестное решение для короткого клипа.')
            if a.get('fit_mode', 'FIT') not in ('FIT', 'CROP'):
                raise ValueError('Неизвестный режим кадрирования.')
    for sid, cues in project.get('captions_by_scene', {}).items():
        if sid not in ids or not isinstance(cues, list):
            raise ValueError('Субтитры ссылаются на отсутствующую сцену.')
        for cue in cues:
            if integer(cue['end_ms'], 1) <= integer(cue['start_ms']) or not isinstance(cue['text'], str):
                raise ValueError('Неверный интервал/текст субтитра.')
    for sid, length in project.get('timeline', {}).get('scene_durations_ms', {}).items():
        if sid not in ids:
            raise ValueError('Ручная длительность ссылается на отсутствующую сцену.')
        integer(length, 1)
    return True


def distribute(weights, total):
    integer(total, 1)
    if total < len(weights):
        raise ValueError('Недостаточно миллисекунд для сцен/якорей.')
    if not weights:
        raise ValueError('Нет интервалов.')
    # Integer cumulative allocation, no independent rounding drift.
    weights = [max(1, w) for w in weights]
    ends, cumulative = [0], 0
    remaining = total-len(weights)
    for i, weight in enumerate(weights, 1):
        cumulative += weight
        ends.append(i+remaining*cumulative//sum(weights))
    return [b-a for a,b in zip(ends, ends[1:])]


def timing_map(project, *, whole_ms=None, scene_ms=None):
    """Pure map. A whole recording is never claimed to be speech aligned."""
    scene_ms = scene_ms or {}
    scenes = project.get('scenes', [])
    manual = project.get('timeline', {}).get('scene_durations_ms', {})
    lengths, kinds = {}, {}
    if whole_ms is not None:
        integer(whole_ms, 1)
        unknown = [s for s in scenes if s['id'] not in manual]
        residual = whole_ms-sum(manual.values())
        if not unknown and residual != 0:
            raise ValueError('Ручные границы не покрывают измеренную общую озвучку.')
        if unknown:
            values=distribute([len(s.get('text','').split()) for s in unknown],residual)
            lengths.update(zip((s['id'] for s in unknown), values))
        lengths.update(manual)
        kinds={s['id']:MANUAL_SCENE_BOUNDARY if s['id'] in manual else ESTIMATED_SCENE_BOUNDARY for s in scenes}
    else:
        for s in scenes:
            sid=s['id']
            if sid not in scene_ms:
                raise ValueError('Озвучка сцены не подготовлена: '+sid)
            integer(scene_ms[sid],1)
            if sid in manual and manual[sid] != scene_ms[sid]:
                raise ValueError('Длительность сцены отличается от аудио: обрежьте/дополните аудио явно.')
            lengths[sid]=scene_ms[sid]
            kinds[sid]=MANUAL_SCENE_BOUNDARY if sid in manual else MEASURED_AUDIO_DURATION
    result=[]; start=0
    for s in scenes:
        length=lengths[s['id']]
        result.append(dict(scene_id=s['id'],start_ms=start,end_ms=start+length,duration_ms=length,
                           audio_duration_kind=MEASURED_AUDIO_DURATION,boundary_kind=kinds[s['id']],
                           caption_kind=(MANUAL_CAPTION_TIMING if any(c.get('timing_kind',MANUAL_CAPTION_TIMING)==MANUAL_CAPTION_TIMING for c in project.get('captions_by_scene',{}).get(s['id'],[])) else ESTIMATED_CAPTION_TIMING)))
        start+=length
    return dict(total_ms=start,scenes=result,whole_audio=whole_ms is not None,measured=True,
                warning='Границы оценочные, если не заданы вручную; запись не переставляется вместе со сценами.' if whole_ms else '')


def measure_audio(project, workspace):
    """FFprobe adapter. Reads local audio/cache only; never invokes TTS."""
    from experimental_mvp.pipeline import duration, executable, audio_key
    probe=executable('ffprobe')
    if project.get('audio'):
        value=timing_map(project,whole_ms=duration(Path(project['audio']).expanduser().resolve(strict=True),probe))
    else:
        lengths={}
        for scene in project.get('scenes',[]):
            if scene.get('audio'):
                source=Path(scene['audio']).expanduser().resolve(strict=True)
            else:
                _, entry=audio_key(project,scene,Path(workspace)/'scene-audio')
                source=entry/'audio.wav'
            lengths[scene['id']]=duration(source,probe)
        value=timing_map(project,scene_ms=lengths)
    return value


def coverage(scene, length):
    """Display gaps/overlaps/outside separately, retaining all user anchors."""
    spans=[]; end=0
    for a in sorted(scene.get('anchors',[]),key=lambda a:a['start_ms']):
        start=a['start_ms']; stop=start+a['duration_ms']
        if start>end:spans.append(dict(kind='GAP',start_ms=end,end_ms=start))
        if start<end:spans.append(dict(kind='OVERLAP',start_ms=start,end_ms=min(end,stop)))
        if stop>length:spans.append(dict(kind='OUTSIDE_SCENE',start_ms=max(start,length),end_ms=stop))
        end=max(end,stop)
    if end<length:spans.append(dict(kind='GAP',start_ms=end,end_ms=length))
    return spans


def status(anchor):
    path=anchor.get('local_asset_path')
    if not path:return 'ОЖИДАЕТ / FALLBACK' if anchor.get('fallback_mode')=='PLACEHOLDER' else 'ОЖИДАЕТ МАТЕРИАЛ'
    p=Path(path)
    if not p.is_file():return 'НЕТ ФАЙЛА'
    try:
        if anchor.get('asset_sha256') and sha256(p.read_bytes()).hexdigest()!=anchor['asset_sha256']:return 'МАТЕРИАЛ ИЗМЕНЁН'
    except OSError:return 'ФАЙЛ НЕДОСТУПЕН'
    if anchor.get('license_status','UNKNOWN') in ('UNKNOWN','UNVERIFIED',''):
        return 'ИМПОРТИРОВАН / ПРОВЕРИТЬ ПРАВА'
    return 'ИМПОРТИРОВАН'


class Editor:
    """Copy-on-write transactions with bounded undo/redo and deterministic IDs."""
    def __init__(self, project, timing):
        validate_project(project)
        self.project=deepcopy(project);self.timing=deepcopy(timing)
        self.undo_stack=[];self.redo_stack=[];self.saved=deepcopy(project)

    @property
    def dirty(self):
        a=deepcopy(self.project);b=deepcopy(self.saved);a.pop('approved',None);b.pop('approved',None)
        return a!=b

    def conflicts(self):
        issues=[]
        for scene in self.project['scenes']:
            length=next(s['duration_ms'] for s in self.timing['scenes'] if s['scene_id']==scene['id'])
            if scene.get('anchors'):issues.extend(coverage(scene,length))
            for anchor in scene.get('anchors',[]):
                state=status(anchor)
                if state in ('НЕТ ФАЙЛА','МАТЕРИАЛ ИЗМЕНЁН','ФАЙЛ НЕДОСТУПЕН'):
                    issues.append(dict(kind='ASSET_ERROR',anchor_id=anchor['anchor_id'],message=state))
            for cue in self.project.get('captions_by_scene',{}).get(scene['id'],[]):
                if cue['end_ms']>length:issues.append(dict(kind='CAPTION_OUTSIDE_SCENE',scene_id=scene['id']))
        return issues

    def locate(self, project, aid):
        for scene in project['scenes']:
            for a in scene.get('anchors',[]):
                if a['anchor_id']==aid:return scene,a
        raise ValueError('Якорь не найден.')

    def new_id(self, project):
        t=project.setdefault('timeline',{'version':1});n=t.get('next_id',0)
        existing={a['anchor_id'] for s in project['scenes'] for a in s.get('anchors',[])}
        while True:
            key=uuid.uuid5(uuid.NAMESPACE_URL,'story-timeline:'+json.dumps([sorted(s['id'] for s in project['scenes']),n])).hex
            n+=1
            if key not in existing:break
        t['next_id']=n
        return key

    def edit(self, operation, aid=None, **kwargs):
        candidate=deepcopy(self.project)
        result=self._apply(candidate,operation,aid,kwargs)
        validate_project(candidate)
        new_timing=deepcopy(self.timing)
        if operation in ('scene_duration','reset_boundaries'):
            new_timing=timing_map(candidate,whole_ms=self.timing['total_ms']) if self.timing['whole_audio'] else timing_map(candidate,scene_ms={s['scene_id']:s['duration_ms'] for s in self.timing['scenes']})
        elif operation=='scene_order':
            lookup={s['scene_id']:s for s in new_timing['scenes']};start=0;new_timing['scenes']=[]
            for scene in candidate['scenes']:
                entry=lookup[scene['id']];entry.update(start_ms=start,end_ms=start+entry['duration_ms']);start=entry['end_ms'];new_timing['scenes'].append(entry)
        if self.timing.get('measured') is False:
            new_timing['measured']=False
            for entry in new_timing['scenes']:entry['audio_duration_kind']='UNKNOWN_NOT_MEASURED'
        bounds={s['scene_id']:s['duration_ms'] for s in new_timing['scenes']}
        for s in candidate['scenes']:
            for a in s.get('anchors',[]):
                if operation in ('scene_duration','reset_boundaries') and kwargs.get('keep_intervals') and a['start_ms']+a['duration_ms']>bounds.get(s['id'],0):
                    a['allow_outside_scene']=True
                if a['start_ms']+a['duration_ms']>bounds.get(s['id'],0) and not a.get('allow_outside_scene'):
                    old_scene,old_anchor = self.locate(self.project,a['anchor_id']) if any(a['anchor_id']==x['anchor_id'] for ss in self.project['scenes'] for x in ss.get('anchors',[])) else (None,None)
                    old_bound=next((x['duration_ms'] for x in self.timing['scenes'] if x['scene_id']==s['id']),0)
                    unchanged_existing=(old_anchor is not None and old_anchor['start_ms']==a['start_ms'] and old_anchor['duration_ms']==a['duration_ms'] and old_bound==bounds[s['id']] and old_anchor['start_ms']+old_anchor['duration_ms']>old_bound)
                    if not unchanged_existing:raise ValueError('Якорь вне сцены. Разрешите выход явно или измените интервал.')
        candidate.setdefault('timeline',{})['version']=1
        candidate['approved']=False
        self.undo_stack.append((deepcopy(self.project),deepcopy(self.timing)))
        self.undo_stack=self.undo_stack[-100:];self.redo_stack.clear();self.project=candidate;self.timing=new_timing
        return result

    def _apply(self,p,op,aid,k):
        if op=='scene_order':
            ids=k['ids']
            if len(ids)!=len(set(ids)) or set(ids)!={s['id'] for s in p['scenes']}:raise ValueError('Неверный порядок сцен.')
            by_id={s['id']:s for s in p['scenes']};p['scenes']=[by_id[i] for i in ids];return
        if op=='caption':
            cues=deepcopy(k['cues'])
            from experimental_mvp.captions import validate
            length=next(s['duration_ms'] for s in self.timing['scenes'] if s['scene_id']==k['scene_id'])
            validate(cues,length,1);p.setdefault('captions_by_scene',{})[k['scene_id']]=cues;return
        if op=='reset_boundaries':
            p.setdefault('timeline',{}).pop('scene_durations_ms',None);return
        if op=='scene_duration':
            p.setdefault('timeline',{}).setdefault('scene_durations_ms',{})[k['scene_id']]=integer(k['duration_ms'],1);return
        if op in ('redistribute','fallback','trim'):
            scene=next(s for s in p['scenes'] if s['id']==k['scene_id'])
            length=next(s['duration_ms'] for s in self.timing['scenes'] if s['scene_id']==scene['id'])
            items=sorted(scene.get('anchors',[]),key=lambda a:a['start_ms'])
            if op=='redistribute':
                lengths=distribute([a['duration_ms'] for a in items],length);start=0
                for a,ms in zip(items,lengths):a.update(start_ms=start,duration_ms=ms,allow_outside_scene=False);start+=ms
            elif op=='fallback':
                from experimental_mvp.storyboard import VideoAnchor
                for gap in coverage(scene,length):
                    if gap['kind']=='GAP':
                        scene.setdefault('anchors',[]).append(asdict(VideoAnchor(self.new_id(p),scene['id'],gap['start_ms'],gap['end_ms']-gap['start_ms'],fallback_mode='PLACEHOLDER')))
            else:
                for a in items:
                    if a['start_ms']>=length:raise ValueError('Якорь полностью вне сцены: удалите его явно (с Undo).')
                    a['duration_ms']=min(a['duration_ms'],length-a['start_ms']);a['allow_outside_scene']=False
            return
        if op=='create':
            from experimental_mvp.storyboard import VideoAnchor
            scene=next(s for s in p['scenes'] if s['id']==k['scene_id'])
            a=asdict(VideoAnchor(self.new_id(p),scene['id'],integer(k['start_ms']),integer(k['duration_ms'],1)))
            scene.setdefault('anchors',[]).append(a);return a['anchor_id']
        scene,a=self.locate(p,aid)
        if op=='set':
            allowed={'start_ms','duration_ms','source_start_ms','source_end_ms','short_clip_policy','fit_mode','generation_mode','visual_description','fallback_mode','source_duration_ms'}
            if set(k)-allowed-{'allow_outside_scene'}:raise ValueError('Неизвестное поле якоря.')
            values={key:value for key,value in k.items() if key in allowed}
            if values.get('source_end_ms',0) is None:
                values.pop('source_end_ms');a.pop('source_end_ms',None)
            a.update(values)
            if k.get('allow_outside_scene') is True:a['allow_outside_scene']=True
        elif op=='duplicate':
            b=deepcopy(a);b['anchor_id']=self.new_id(p);b['start_ms']=k.get('start_ms',a['start_ms']);scene['anchors'].append(b);return b['anchor_id']
        elif op=='delete':
            if k.get('confirmed') is not True:raise ValueError('Подтвердите удаление ссылки (файл сохраняется).')
            scene['anchors'].remove(a)
        elif op=='split':
            at=integer(k['at_ms'],1)
            if at>=a['duration_ms']:raise ValueError('Точка разделения вне якоря.')
            b=deepcopy(a);b.update(anchor_id=self.new_id(p),start_ms=a['start_ms']+at,duration_ms=a['duration_ms']-at)
            a['duration_ms']=at
            from experimental_mvp.storyboard import VIDEOS
            if Path(a.get('local_asset_path','')).suffix.lower() in VIDEOS:
                start=a.get('source_start_ms',0);out=a.get('source_end_ms',start+at+b['duration_ms'])
                # Splitting repeated/held clips is ambiguous; require an explicit material decision first.
                if a.get('short_clip_policy','ERROR') in ('LOOP','HOLD_LAST_FRAME'):
                    raise ValueError('Перед разделением held/loop клипа выберите точные исходные интервалы.')
                a['source_end_ms']=start+at;b['source_start_ms']=start+at;b['source_end_ms']=out
            scene['anchors'].append(b);return b['anchor_id']
        elif op=='merge':
            _,b=self.locate(p,k['other_id'])
            if b is a or b['scene_id']!=a['scene_id'] or a['start_ms']+a['duration_ms']!=b['start_ms']:
                raise ValueError('Нужны соседние якоря одной сцены в порядке времени.')
            ignored={'anchor_id','start_ms','duration_ms','source_start_ms','source_end_ms','narration_excerpt'}
            if {k:v for k,v in a.items() if k not in ignored}!={k:v for k,v in b.items() if k not in ignored}:
                raise ValueError('Материалы/происхождение/режимы несовместимы.')
            from experimental_mvp.storyboard import VIDEOS
            if Path(a.get('local_asset_path','')).suffix.lower() in VIDEOS:
                if a.get('source_end_ms',a.get('source_start_ms',0)+a['duration_ms'])!=b.get('source_start_ms',0):
                    raise ValueError('Исходные интервалы клипа не соседние.')
                a['source_end_ms']=b.get('source_end_ms',b.get('source_start_ms',0)+b['duration_ms'])
            a['duration_ms']+=b['duration_ms'];a['narration_excerpt']+=' '+b.get('narration_excerpt','');scene['anchors'].remove(b)
        else:raise ValueError('Неизвестная операция.')

    def undo(self):
        if not self.undo_stack:return
        self.redo_stack.append((deepcopy(self.project),deepcopy(self.timing)))
        self.project,self.timing=self.undo_stack.pop();self.project['approved']=False

    def redo(self):
        if not self.redo_stack:return
        self.undo_stack.append((deepcopy(self.project),deepcopy(self.timing)))
        self.project,self.timing=self.redo_stack.pop();self.project['approved']=False

    def save(self,path,*,allow_conflicts=False):
        validate_project(self.project)
        if not allow_conflicts and self.conflicts():raise ValueError('Есть конфликты покрытия/субтитров; сохраните явно как черновик.')
        from experimental_mvp.pipeline import save
        candidate=deepcopy(self.project)
        if allow_conflicts:candidate['approved']=False
        save(Path(path),candidate)
        self.project=candidate;self.saved=deepcopy(candidate)


def preview(project, timing, workspace, *, scene_id=None, anchor_id=None, seek_ms=0, cancelled=lambda:False):
    from experimental_mvp.pipeline import preview_session
    with preview_session(cancelled):
        return _preview(project,timing,workspace,scene_id=scene_id,anchor_id=anchor_id,seek_ms=seek_ms,cancelled=cancelled)


def _preview(project, timing, workspace, *, scene_id=None, anchor_id=None, seek_ms=0, cancelled=lambda:False):
    """Temporary prerender, not interactive playback. Never edits the source project."""
    from experimental_mvp.pipeline import build, render_scene, preview_audio, command, executable, BuildStopped
    from experimental_mvp.captions import render_srt
    import subprocess
    candidate=deepcopy(project);validate_project(candidate)
    workspace=Path(workspace);workspace.mkdir(parents=True,exist_ok=True)
    if not scene_id and not anchor_id and seek_ms==0:
        candidate['approved']=True
        return build(candidate,workspace,lambda _:None,preview=True,cancelled=cancelled)
    if anchor_id:scene,anchor=Editor(candidate,timing).locate(candidate,anchor_id);scene_id=scene['id']
    else:scene=next(s for s in candidate['scenes'] if s['id']==scene_id) if scene_id else None;anchor=None
    if scene is None:
        entry=next((s for s in timing['scenes'] if s['start_ms']<=seek_ms<s['end_ms']),None)
        if entry is None:raise ValueError('Позиция вне проекта.')
        scene=next(s for s in candidate['scenes'] if s['id']==entry['scene_id'])
        local_seek=seek_ms-entry['start_ms']
    else:local_seek=0
    index=candidate['scenes'].index(scene)
    source,start,length,_=preview_audio(candidate,index,workspace)
    offset=anchor['start_ms'] if anchor else local_seek
    length=anchor['duration_ms'] if anchor else length-local_seek
    rendered=deepcopy(scene)
    if anchor:rendered['anchors']=[{**deepcopy(anchor),'start_ms':0}]
    elif local_seek:
        # Render the scene unchanged, then seek the prerendered result; no destructive clipping of anchors.
        length+=local_seek;offset=0
    folder=workspace/('timeline-preview-'+uuid.uuid4().hex[:12]);folder.mkdir()
    from experimental_mvp.pipeline import register_preview_folder
    register_preview_folder(folder)
    ffmpeg=executable('ffmpeg');log=folder/'preview.log'
    if cancelled():raise BuildStopped('Предпросмотр отменён.')
    from experimental_mvp.storyboard import output_profile
    profile={**candidate.get('output_profile',{}),'timeline_version':1,'scene_start_ms':0,
             'frame_count':round(length*output_profile(candidate.get('output_profile'))[2]/1000)}
    clip=render_scene(rendered,1,length/1000,folder,log,ffmpeg,profile,cancelled)
    if cancelled():raise BuildStopped('Предпросмотр отменён.')
    cues=candidate.get('captions_by_scene',{}).get(scene['id'])
    if anchor and cues is not None:
        cues=[dict(start_ms=max(0,c['start_ms']-offset),end_ms=min(length,c['end_ms']-offset),text=c['text'])
              for c in cues if c['end_ms']>offset and c['start_ms']<offset+length]
    overrides={scene['id']:cues} if cues else {}
    (folder/'captions.srt').write_text(render_srt([rendered],[(0,length)],overrides),encoding='utf-8')
    command([ffmpeg,'-nostdin','-v','error','-i',clip,'-ss',str((start+offset)/1000),'-i',str(source),
             '-i','captions.srt','-map','0:v:0','-map','1:a:0','-map','2:s:0','-t',str(length/1000),
             '-c:v','copy','-c:a','aac','-c:s','mov_text','pending.mp4'],folder,log)
    if cancelled():raise BuildStopped('Предпросмотр отменён.')
    if local_seek:
        command([ffmpeg,'-nostdin','-v','error','-ss',str(local_seek/1000),'-i','pending.mp4',
                 '-map','0','-c:v','libx264','-preset','ultrafast','-threads','4','-c:a','aac','-c:s','mov_text','preview.mp4'],folder,log)
        (folder/'pending.mp4').unlink()
    else:(folder/'pending.mp4').replace(folder/'preview.mp4')
    if cancelled():
        (folder/'preview.mp4').unlink(missing_ok=True);raise BuildStopped('Предпросмотр отменён.')
    return folder/'preview.mp4'
