"""Tk visual timeline adapter. Playback is explicit temporary prerender + OS player."""
from copy import deepcopy
import json
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

from experimental_mvp import timeline as model
from experimental_mvp.captions import calculated


def content(project):
    value=deepcopy(project);value.pop('approved',None)
    return json.dumps(value,ensure_ascii=False,sort_keys=True)


class TimelinePanel(ttk.Frame):
    def __init__(self, parent, get_project, apply_project, workspace, open_local):
        super().__init__(parent,padding=6)
        self.get_project=get_project;self.apply_project=apply_project;self.workspace=workspace;self.open_local=open_local
        self.editor=None;self.base=None;self.aid=None;self.sid=None;self.cue=None
        self.zoom=40.;self.position=0;self.drag=None;self.regions=[];self.events=queue.Queue()
        self.stop=threading.Event();self.busy=False;self.last_preview=None
        row=ttk.Frame(self);row.pack(fill='x')
        for label,fn in [('Загрузить / Audio Map',self.refresh),('Применить',self.apply),('Сохранить JSON',self.save),
                         ('Undo',self.undo),('Redo',self.redo),('− масштаб',lambda:self.scale(.75)),('+ масштаб',lambda:self.scale(1.33))]:self.button(row,label,fn)
        row=ttk.Frame(self);row.pack(fill='x')
        for label,fn in [('Новый якорь',self.create),('Разделить',self.split),('Объединить →',self.merge),
                         ('Дублировать',self.duplicate),('Удалить',self.delete),('↑ сцена',lambda:self.scene_order(-1)),('↓ сцена',lambda:self.scene_order(1))]:self.button(row,label,fn)
        area=ttk.Frame(self);area.pack(fill='both',expand=True)
        self.canvas=tk.Canvas(area,height=230,background='#142338',takefocus=True,highlightthickness=1)
        self.canvas.pack(side='top',fill='both',expand=True)
        scroll=ttk.Scrollbar(area,orient='horizontal',command=self.canvas.xview);scroll.pack(fill='x')
        self.canvas.configure(xscrollcommand=scroll.set)
        self.canvas.bind('<Configure>',lambda _:self.draw())
        self.canvas.bind('<ButtonPress-1>',self.mouse_down);self.canvas.bind('<B1-Motion>',self.mouse_drag);self.canvas.bind('<ButtonRelease-1>',self.mouse_up)
        self.canvas.bind('<Left>',lambda _:self.nudge(-100));self.canvas.bind('<Right>',lambda _:self.nudge(100))
        self.canvas.bind('<Shift-Left>',lambda _:self.resize(-100));self.canvas.bind('<Shift-Right>',lambda _:self.resize(100))
        self.canvas.bind('<Delete>',lambda _:self.safe(self.delete));self.canvas.bind('<Control-z>',lambda _:self.undo());self.canvas.bind('<Control-y>',lambda _:self.redo())
        self.canvas.bind('<Control-d>',lambda _:self.safe(self.duplicate));self.canvas.bind('<Control-plus>',lambda _:self.scale(1.33));self.canvas.bind('<Control-minus>',lambda _:self.scale(.75))
        row=ttk.Frame(self);row.pack(fill='x')
        self.start=tk.StringVar(value='0');self.length=tk.StringVar(value='1000');self.seek=tk.StringVar(value='0')
        for title,var in [('Начало мс',self.start),('Длина мс',self.length),('Позиция мс',self.seek)]:
            ttk.Label(row,text=title).pack(side='left');ttk.Entry(row,textvariable=var,width=9).pack(side='left')
        self.button(row,'Изменить',self.numbers);self.button(row,'Перейти',self.goto);self.button(row,'Реплика…',self.edit_caption)
        row=ttk.Frame(self);row.pack(fill='x')
        for label,fn in [('Интервал клипа…',self.clip_options),('Ручная сцена…',self.scene_duration),('Распределить якоря',lambda:self.reconcile('redistribute')),
                         ('Fallback в пробелы',lambda:self.reconcile('fallback')),('Обрезать визуалы',lambda:self.reconcile('trim')),('Оценить границы',self.reset_boundaries)]:self.button(row,label,fn)
        row=ttk.Frame(self);row.pack(fill='x')
        for label,scope in [('Preview якоря','anchor'),('Preview сцены','scene'),('Preview проекта','project'),('Preview с позиции','position')]:
            self.button(row,label,lambda scope=scope:self.make_preview(scope))
        self.button(row,'Отменить preview',self.stop.set)
        self.progress=ttk.Progressbar(self,mode='indeterminate');self.progress.pack(fill='x')
        self.info=tk.StringVar(value='Загрузите проект. Это предварительный рендер, не синхронное интерактивное воспроизведение.')
        ttk.Label(self,textvariable=self.info,wraplength=960).pack(anchor='w')
        ttk.Label(self,text='SCENE | AUDIO | ANCHOR | CAPTION · GAP / OVERLAP · ←/→ шаг 100 мс; Shift+←/→ длина; Ctrl+Z/Y; Delete; Ctrl+D',wraplength=960).pack(anchor='w')
        self.poll_id=self.after(100,self.poll)

    def safe(self,fn):
        try:return fn()
        except Exception as exc:messagebox.showerror('Временная шкала',str(exc),parent=self)

    def button(self,parent,label,fn):
        ttk.Button(parent,text=label,command=lambda:self.safe(fn)).pack(side='left',padx=2,pady=2)

    def confirm_leave(self):
        if self.busy:
            messagebox.showinfo('Preview','Отмените preview и дождитесь завершения.',parent=self);return False
        if self.editor and self.editor.dirty:
            answer=messagebox.askyesnocancel('Несохранённая шкала','Применить изменения к текущему проекту? «Нет» — отбросить.',parent=self)
            if answer is None:return False
            if answer:self.apply()
        return True

    def refresh(self):
        if not self.confirm_leave():return
        p=deepcopy(self.get_project())
        from experimental_mvp.pipeline import identify
        identify(p)
        try:
            timing=model.measure_audio(p,self.workspace());note=timing['warning']
        except Exception as exc:
            original_error=exc
            try:
                raw=deepcopy(p);raw.get('timeline',{}).pop('scene_durations_ms',None)
                measured=model.measure_audio(raw,self.workspace())
            except Exception:measured=None
            # Explicit planning estimate, never labelled measured.
            if not p.get('scenes'):raise ValueError('Добавьте сцены.')
            total=sum(max(1000,len(s.get('text','').split())*450) for s in p['scenes'])
            planned=deepcopy(p);planned.pop('timeline',None)
            timing=measured or model.timing_map(planned,whole_ms=total);timing['measured']=bool(measured)
            if not measured:
                for s in timing['scenes']:s['audio_duration_kind']='UNKNOWN_NOT_MEASURED'
            note=('Ошибка ручных границ; показана оценка по измеренному аудио: ' if measured else 'Аудио не измерено; шкала плановая: ')+str(original_error)+'. Данные проекта не исправлены автоматически.'
        self.base=content(p);self.editor=model.Editor(p,timing);self.sid=p['scenes'][0]['id'];self.aid=None;self.cue=None
        self.info.set(f"Всего {timing['total_ms']/1000:.3f} s. "+note);self.draw()

    def entry(self,sid=None):
        if not self.editor:raise ValueError('Сначала загрузите шкалу.')
        return next(s for s in self.editor.timing['scenes'] if s['scene_id']==(sid or self.sid))

    def scene(self):
        return next(s for s in self.editor.project['scenes'] if s['id']==self.sid)

    def anchor(self):
        if not self.aid:raise ValueError('Выберите якорь.')
        return self.editor.locate(self.editor.project,self.aid)[1]

    def edit(self,op,**kwargs):
        self.editor.edit(op,self.aid,**kwargs);self.draw()

    def scale(self,factor):
        self.zoom=max(2,min(400,self.zoom*factor));self.draw()

    def x(self,ms):return 100+ms*self.zoom/1000

    def ms(self,x):return round((x-100)*1000/self.zoom)

    def draw(self):
        c=self.canvas;c.delete('all');self.regions=[]
        if not self.editor:return
        total=self.editor.timing['total_ms'];c.configure(scrollregion=(0,0,self.x(total)+160,240))
        step=max(1,round(100/self.zoom))
        for second in range(0,total//1000+2,step):
            x=self.x(second*1000);c.create_line(x,20,x,225,fill='#35506c');c.create_text(x,10,text=f'{second}s',fill='white',anchor='w')
        for y,label in [(40,'SCENE'),(80,'AUDIO'),(130,'ANCHOR'),(190,'CAPTION')]:c.create_text(4,y,text=label,fill='white',anchor='w')
        for n,entry in enumerate(self.editor.timing['scenes'],1):
            sid=entry['scene_id'];scene=next(s for s in self.editor.project['scenes'] if s['id']==sid)
            x1,x2=self.x(entry['start_ms']),self.x(entry['end_ms'])
            c.create_rectangle(x1,26,x2,58,fill='#244f77',outline='white' if sid==self.sid else '#7394b4')
            c.create_text(x1+3,40,text=f'{n}: {scene.get("text","")[:35]}',fill='white',anchor='w')
            self.regions.append((x1,26,x2,58,'scene',sid,None))
            c.create_rectangle(x1,64,x2,96,fill='#286359');c.create_text(x1+3,80,text=entry['audio_duration_kind']+' / '+entry['boundary_kind'],fill='white',anchor='w')
            conflicts=model.coverage(scene,entry['duration_ms']) if scene.get('anchors') else []
            for span in conflicts:
                a,b=self.x(entry['start_ms']+span['start_ms']),self.x(entry['start_ms']+span['end_ms'])
                c.create_rectangle(a,104,b,158,fill='#7e353e',stipple='gray50');c.create_text(a+2,153,text=span['kind'],anchor='w',fill='white')
            for anchor in scene.get('anchors',[]):
                a,b=self.x(entry['start_ms']+anchor['start_ms']),self.x(entry['start_ms']+anchor['start_ms']+anchor['duration_ms'])
                state=model.status(anchor);bad=any(anchor['start_ms']<s['end_ms'] and anchor['start_ms']+anchor['duration_ms']>s['start_ms'] for s in conflicts)
                if bad:state+=' / КОНФЛИКТ'
                color='#366c50' if state=='ИМПОРТИРОВАН' else '#73572f'
                if 'НЕТ ФАЙЛА' in state or 'ИЗМЕНЁН' in state or bad:color='#8b3641'
                c.create_rectangle(a,106,b,145,fill=color,outline='white' if anchor['anchor_id']==self.aid else '#9aabb9',width=2)
                c.create_text(a+3,116,text=(anchor['anchor_id'][:6]+' '+state)[:max(1,int((b-a-6)/7))],fill='white',anchor='w')
                c.create_text(a+3,133,text=f"{anchor['duration_ms']}ms",fill='white',anchor='w')
                c.create_rectangle(b-5,108,b,143,fill='#d1dce6')
                self.regions.append((a,106,b,145,'anchor',sid,anchor['anchor_id']))
            manual=sid in self.editor.project.get('captions_by_scene',{})
            cues=self.editor.project.get('captions_by_scene',{}).get(sid,calculated(scene.get('text',''),entry['duration_ms']))
            for index,cue in enumerate(cues):
                a,b=self.x(entry['start_ms']+cue['start_ms']),self.x(entry['start_ms']+cue['end_ms'])
                bad=cue['end_ms']>entry['duration_ms'] or cue['start_ms']<0
                c.create_rectangle(a,170,b,209,fill='#8b3641' if bad else '#5a4c86')
                c.create_text(a+2,187,text=(('MANUAL' if cue.get('timing_kind','MANUAL_CAPTION_TIMING' if manual else 'ESTIMATED_CAPTION_TIMING')=='MANUAL_CAPTION_TIMING' else 'ESTIMATED')+' '+cue['text'])[:max(1,int((b-a-4)/7))],fill='white',anchor='w')
                self.regions.append((a,170,b,209,'caption',sid,index))
        c.create_line(self.x(self.position),20,self.x(self.position),220,fill='#ffce65',width=2,tags='position')
        self.y_scale=min(1,max(.4,c.winfo_height()/230))
        c.scale('all',0,0,1,self.y_scale)
        self.seek.set(str(self.position))

    def mouse_down(self,event):
        if not self.editor:return
        self.drag=None
        self.canvas.focus_set();x=self.canvas.canvasx(event.x);y=event.y/getattr(self,'y_scale',1)
        for a,top,b,bottom,kind,sid,key in reversed(self.regions):
            if a<=x<=b and top<=y<=bottom:
                self.sid=sid;self.cue=key if kind=='caption' else None;self.aid=key if kind=='anchor' else None
                if self.aid:
                    anchor=self.anchor();self.start.set(str(anchor['start_ms']));self.length.set(str(anchor['duration_ms']))
                    self.drag=(x,deepcopy(anchor),'resize' if b-x<8 else 'move')
                    self.info.set(model.status(anchor)+'; drag body moves, drag right edge resizes; rights are not certified.')
                if kind=='caption':
                    scene=self.scene();entry=self.entry();cues=self.editor.project.get('captions_by_scene',{}).get(sid,calculated(scene['text'],entry['duration_ms']))
                    self.info.set(str(cues[key])+' / '+entry['caption_kind'])
                self.draw();return
        self.position=max(0,min(self.editor.timing['total_ms'],self.ms(x)));self.draw()

    def mouse_drag(self,event):
        if not self.drag:return
        x=self.canvas.canvasx(event.x)
        self.canvas.delete('ghost');self.canvas.create_line(x,100,x,160,fill='#ffce65',width=3,tags='ghost')

    def mouse_up(self,event):
        if not self.drag:return
        x0,original,op=self.drag;self.drag=None
        delta=round((self.canvas.canvasx(event.x)-x0)*1000/self.zoom)
        self.safe(lambda:self.edit('set',**({'duration_ms':original['duration_ms']+delta} if op=='resize' else {'start_ms':original['start_ms']+delta})))
        self.draw()

    def nudge(self,delta):
        self.safe(lambda:self.edit('set',start_ms=self.anchor()['start_ms']+delta));return 'break'

    def resize(self,delta):
        self.safe(lambda:self.edit('set',duration_ms=self.anchor()['duration_ms']+delta));return 'break'

    def numbers(self):
        try:self.edit('set',start_ms=int(self.start.get()),duration_ms=int(self.length.get()))
        except ValueError:
            if messagebox.askyesno('Границы','Разрешить выход за сцену? Экспорт останется заблокирован до исправления.',parent=self):
                self.edit('set',start_ms=int(self.start.get()),duration_ms=int(self.length.get()),allow_outside_scene=True)
            else:raise

    def goto(self):
        self.position=model.integer(int(self.seek.get()))
        if self.position>self.editor.timing['total_ms']:raise ValueError('Вне проекта.')
        self.canvas.xview_moveto(max(0,(self.x(self.position)-250)/(self.x(self.editor.timing['total_ms'])+160)));self.draw()
        self.info.set(f'Позиция {self.position/1000:.3f}s. Указатель монтажа, не время системного проигрывателя.')

    def create(self):
        self.edit('create',scene_id=self.sid,start_ms=max(0,self.position-self.entry()['start_ms']),duration_ms=1000)

    def split(self):
        value=simpledialog.askinteger('Разделить','Внутренняя позиция от начала якоря, мс:',parent=self,minvalue=1)
        if value is not None:self.edit('split',at_ms=value)

    def merge(self):
        anchors=sorted(self.scene()['anchors'],key=lambda a:a['start_ms']);index=anchors.index(self.anchor())
        if index+1>=len(anchors):raise ValueError('Нет следующего якоря.')
        self.edit('merge',other_id=anchors[index+1]['anchor_id'])

    def duplicate(self):self.edit('duplicate')

    def delete(self):
        if messagebox.askyesno('Удаление','Удалить только ссылку на якорь? Файл остаётся на диске. Undo доступен.',parent=self):
            self.edit('delete',confirmed=True);self.aid=None;self.draw()

    def undo(self):
        if self.editor:self.editor.undo();self.aid=None;self.draw()

    def redo(self):
        if self.editor:self.editor.redo();self.aid=None;self.draw()

    def scene_order(self,offset):
        ids=[s['id'] for s in self.editor.project['scenes']];i=ids.index(self.sid);j=i+offset
        if 0<=j<len(ids):
            if self.editor.timing['whole_audio'] and not messagebox.askyesno('Общая запись','Запись не переставится. Перепроверьте смысл и границы после смены порядка. Продолжить?',parent=self):return
            ids[i],ids[j]=ids[j],ids[i];self.edit('scene_order',ids=ids)

    def scene_duration(self):
        ms=simpledialog.askinteger('Ручная граница','Длительность сцены, мс. Общая дорожка: остаток распределится по другим сценам.',parent=self,minvalue=1)
        if ms is not None:
            self.edit('scene_duration',scene_id=self.sid,duration_ms=ms,keep_intervals=True);self.info.set('Ручная граница задана; проверьте покрытие и титры. Никакие материалы не удалены.')

    def reset_boundaries(self):
        if messagebox.askyesno('Границы сцен','Удалить только ручные границы и явно перейти к оценке по озвучке? Якоря и титры останутся без изменений; проверьте конфликты.',parent=self):
            self.edit('reset_boundaries',keep_intervals=True)

    def reconcile(self,operation):
        if messagebox.askyesno('Изменение покрытия','Применить '+operation+'? Undo сохранит исходные интервалы; материалы и ручные титры не удаляются.',parent=self):
            self.edit(operation,scene_id=self.sid)

    def clip_options(self):
        a=self.anchor();dialog=tk.Toplevel(self);dialog.title('Интервал и обработка материала')
        values={}
        for key,label,default,options in [('source_start_ms','Начало исходника, мс',a.get('source_start_ms',0),None),
              ('source_end_ms','Конец исходника, мс (пусто = весь)',a.get('source_end_ms',''),None),
              ('short_clip_policy','Если клип короче якоря',a.get('short_clip_policy','ERROR'),('ERROR','HOLD_LAST_FRAME','LOOP')),
              ('fit_mode','Вписать / кадрировать',a.get('fit_mode','FIT'),('FIT','CROP'))]:
            row=ttk.Frame(dialog);row.pack(fill='x');ttk.Label(row,text=label,width=38).pack(side='left')
            var=tk.StringVar(value=str(default));values[key]=var
            w=ttk.Combobox(row,textvariable=var,values=options,state='readonly') if options else ttk.Entry(row,textvariable=var)
            w.pack(side='left')
        if a.get('local_asset_path'):
            from experimental_mvp.storyboard import video_spec,VIDEOS
            if Path(a['local_asset_path']).suffix.lower() in VIDEOS:
                try:
                    spec=video_spec({**a,'short_clip_policy':'HOLD_LAST_FRAME'});ttk.Label(dialog,text=f"Измерено {spec['measured_ms']} ms. Скорость не изменяется.").pack()
                except Exception as exc:ttk.Label(dialog,text=str(exc)).pack()
        def accept():
            k={key:var.get() for key,var in values.items() if var.get()!=''}
            for key in ('source_start_ms','source_end_ms'):
                if key in k:k[key]=int(k[key])
            if not values['source_end_ms'].get():k['source_end_ms']=None
            self.edit('set',**k);dialog.destroy()
        ttk.Button(dialog,text='Применить явно',command=lambda:self.safe(accept)).pack()

    def edit_caption(self):
        scene=self.scene();sid=scene['id'];length=self.entry()['duration_ms']
        cues=deepcopy(self.editor.project.get('captions_by_scene',{}).get(sid,calculated(scene['text'],length)))
        if sid not in self.editor.project.get('captions_by_scene',{}):
            for cue in cues:cue['timing_kind']=model.ESTIMATED_CAPTION_TIMING
        index=self.cue if self.cue is not None else 0
        if not cues:raise ValueError('Нет реплик; добавьте текст сцены.')
        dialog=tk.Toplevel(self);dialog.title('Субтитр: ручное редактирование')
        values={}
        for key,label in [('start_ms','Начало мс'),('end_ms','Конец мс'),('text','Текст')]:
            ttk.Label(dialog,text=label).pack(anchor='w');v=tk.StringVar(value=str(cues[index][key]));ttk.Entry(dialog,textvariable=v,width=70).pack(fill='x');values[key]=v
        def accept():
            cues[index]={k:int(v.get()) if k!='text' else v.get() for k,v in values.items()};cues[index]['timing_kind']=model.MANUAL_CAPTION_TIMING
            self.edit('caption',scene_id=sid,cues=cues);dialog.destroy()
        ttk.Button(dialog,text='Сохранить ручную реплику',command=lambda:self.safe(accept)).pack()

    def apply(self):
        if not self.editor:raise ValueError('Нет шкалы.')
        if content(self.get_project())!=self.base:raise ValueError('Основной проект изменился; сохраните/перезагрузите шкалу, чтобы не потерять внешние правки.')
        self.apply_project(deepcopy(self.editor.project));self.base=content(self.get_project());self.editor.saved=deepcopy(self.editor.project)
        self.info.set('Применено к редактору; сохраните основной проект. Подтверждение сборки сброшено.')

    def save(self):
        if not self.editor:raise ValueError('Нет шкалы.')
        path=filedialog.asksaveasfilename(parent=self,defaultextension='.json',filetypes=[('Экспериментальный проект','*.json')])
        if path:
            from experimental_mvp.pipeline import check_project
            issues=check_project(self.editor.project,self.workspace())
            conflicts=bool(self.editor.conflicts()) or any(not row[3] for row in issues)
            if conflicts and not messagebox.askyesno('Черновик','Есть временные конфликты. Сохранить явно как черновик (экспорт потребует исправления)?',parent=self):return
            self.editor.save(path,allow_conflicts=conflicts);self.info.set('Сохранено атомарно: '+path)

    def make_preview(self,scope):
        if self.busy:raise ValueError('Preview уже выполняется.')
        if not self.editor:raise ValueError('Нет шкалы.')
        p=deepcopy(self.editor.project);timing=deepcopy(self.editor.timing)
        kw={}
        if scope=='anchor':kw['anchor_id']=self.anchor()['anchor_id']
        elif scope=='scene':kw['scene_id']=self.sid
        elif scope=='position':kw['seek_ms']=self.position
        self.stop.clear();self.busy=True;self.progress.start(15);self.info.set('Создание временного preview…')
        def work():
            try:self.events.put(('preview',(model.preview(p,timing,self.workspace(),cancelled=self.stop.is_set,**kw),content(p))))
            except Exception as exc:self.events.put(('error',str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def poll(self):
        while not self.events.empty():
            kind,value=self.events.get();self.busy=False;self.progress.stop()
            if kind=='preview':
                path,snapshot=value
                self.last_preview=path
                stale=not self.editor or content(self.editor.project)!=snapshot
                self.info.set(('Preview УСТАРЕЛ: проект изменён. ' if stale else 'Preview создан. ')+'Системный проигрыватель не синхронизирован с указателем шкалы.')
                self.safe(lambda:self.open_local(path))
            else:self.info.set(value)
        self.poll_id=self.after(100,self.poll)

    def destroy(self):
        self.stop.set()
        if getattr(self,'poll_id',None):
            try:self.after_cancel(self.poll_id)
            except tk.TclError:pass
        super().destroy()
