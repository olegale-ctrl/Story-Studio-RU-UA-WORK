"""Small local library UI. Workers never call Tk; GUI applies results with CAS."""
from copy import deepcopy
import json
import gc
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

from experimental_mvp.asset_library import AssetLibrary, anchor_token, encoded, find_anchor, LibraryError


class AssetLibraryPanel(ttk.Frame):
    def __init__(self, parent, get_project, apply_project, library_root, timeline_panel=None):
        super().__init__(parent, padding=8)
        self.get_project, self.apply_project = get_project, apply_project
        self.library_root, self.timeline_panel = library_root, timeline_panel
        self.events = queue.Queue(); self.busy = False; self.closed = False
        self.records = {}; self.image = None
        controls = ttk.Frame(self); controls.pack(fill='x')
        self.query = tk.StringVar(); self.filter_by = tk.StringVar(value='asset_id')
        ttk.Combobox(controls, textvariable=self.filter_by, width=18, state='readonly', values=(
            'asset_id','media_type','provider','model','rights_status','technical_status','sha256',
            'project_id','anchor_id','tag','date_from','date_to')).pack(side='left')
        ttk.Entry(controls,textvariable=self.query,width=32).pack(side='left')
        self.controls = []
        for text, fn in [('Открыть / найти',self.refresh),('Импорт…',self.import_file),('Проверить / recovery',self.recover)]:
            self.button(controls,text,fn)
        self.offset = 0
        self.button(controls,'←',lambda:self.page(-50)); self.button(controls,'→',lambda:self.page(50))
        self.list = ttk.Treeview(self, columns=('type','rights','revision'), show='tree headings',height=7)
        self.list.heading('#0',text='Asset ID / original filename')
        for name in ('type','rights','revision'): self.list.heading(name,text=name)
        self.list.pack(fill='both',expand=True); self.list.bind('<<TreeviewSelect>>',lambda _:self.details())
        row = ttk.Frame(self); row.pack(fill='x')
        self.anchor_id = tk.StringVar()
        self.anchors = ttk.Combobox(row,textvariable=self.anchor_id,width=35,state='readonly');self.anchors.pack(side='left')
        for text,fn in [('Якоря проекта',self.load_anchors),('Привязать',self.attach),('Удалить связь',self.detach),
                        ('Метаданные / права…',self.metadata),('Retire',self.retire)]: self.button(row,text,fn)
        self.detail = tk.Text(self,height=10,wrap='word'); self.detail.pack(fill='both',expand=True)
        self.poster = ttk.Label(self);self.poster.pack()
        self.note = tk.StringVar(value='Локальная экспериментальная библиотека. Права UNKNOWN не разрешают привязку. API отсутствуют.')
        ttk.Label(self,textvariable=self.note,wraplength=950).pack(fill='x')
        self.bind('<Destroy>',self.cleanup,add='+');self.poll_id=self.after(80,self.poll)

    def button(self,parent,text,fn):
        def safe():
            try: fn()
            except Exception as exc: messagebox.showerror('Asset Library',str(exc),parent=self)
        b=ttk.Button(parent,text=text,command=safe);b.pack(side='left',padx=2);self.controls.append(b)

    def snapshot(self):
        if self.timeline_panel and self.timeline_panel.editor:
            return deepcopy(self.timeline_panel.editor.project)
        return deepcopy(self.get_project())

    def load_anchors(self):
        ids=[a['anchor_id'] for s in self.snapshot().get('scenes',[]) for a in s.get('anchors',[])]
        self.anchors.configure(values=ids)
        if ids and self.anchor_id.get() not in ids:self.anchor_id.set(ids[0])

    def work(self, fn):
        if self.busy: raise ValueError('Дождитесь текущей операции.')
        # Tcl resources from previously closed panels must be finalized on the GUI thread.
        gc.collect()
        self.busy=True;self.note.set('Локальная операция…')
        for b in self.controls:b.configure(state='disabled')
        events=self.events
        def run():
            try:events.put(('ok',fn()))
            except Exception as exc:events.put(('error',str(exc)))
        threading.Thread(target=run,daemon=True).start()

    def library(self):return AssetLibrary(self.library_root)

    def page(self,delta):
        self.offset=max(0,self.offset+delta);self.refresh()

    def refresh(self):
        filters={self.filter_by.get():self.query.get()} if self.query.get() else {}
        offset=self.offset; library_root=self.library_root
        self.work(lambda:('list',AssetLibrary(library_root).search(offset=offset,**filters)))

    def recover(self):
        library_root=self.library_root
        self.work(lambda:('message',AssetLibrary(library_root).recover_incomplete_imports()))

    def import_file(self):
        path=filedialog.askopenfilename(parent=self,filetypes=[('Media','*.png *.jpg *.jpeg *.bmp *.webp *.mp4 *.mov *.mkv *.webm')])
        library_root=self.library_root
        if path:self.work(lambda:('import',AssetLibrary(library_root).import_file(path,provenance={'source_type':'MANUAL'})))

    def selected(self):
        ids=self.list.selection()
        if not ids:raise ValueError('Выберите AssetRecord.')
        return self.records[ids[0]]

    def details(self):
        if self.busy or not self.list.selection():return
        record=self.selected();self.detail.delete('1.0','end');self.detail.insert('1.0',json.dumps(record,ensure_ascii=False,indent=2))
        aid,rev=record['asset_id'],record['revision']
        library_root=self.library_root
        def make():
            lib=AssetLibrary(library_root);result=lib.thumbnail(aid,rev)
            result['preview_path']=str(lib.managed(result['storage_reference']))
            return ('thumbnail',result)
        self.work(make)

    def metadata(self):
        r=self.selected()
        value=simpledialog.askstring('Экспериментальные метаданные','JSON provenance / rights / tags. Это запись review, не production permission.',
            initialvalue=json.dumps({k:r[k] for k in ('provenance','rights','tags')},ensure_ascii=False),parent=self)
        if value is None:return
        data=json.loads(value);data.get('provenance',{}).pop('import_timestamp',None)
        library_root=self.library_root
        self.work(lambda:('import',AssetLibrary(library_root).update_metadata(r['asset_id'],expected_revision=r['revision'],**data)))

    def retire(self):
        r=self.selected();library_root=self.library_root
        if messagebox.askyesno('Retire','Оригинал сохранится. Новое использование будет заблокировано.',parent=self):
            self.work(lambda:('import',AssetLibrary(library_root).retire(r['asset_id'])))

    def change(self, detach=False):
        project=self.snapshot();before=encoded(project);aid=self.anchor_id.get();anchor=find_anchor(project,aid)
        record=None if detach else self.selected()
        if not detach and anchor.get('local_asset_path') and not messagebox.askyesno('Замена ссылки','Явно заменить прежнюю ссылку? Оригинальные байты сохраняются.',parent=self):return
        library_root=self.library_root
        def job():
            lib=AssetLibrary(library_root)
            if detach:lib.detach(project,aid,expected_anchor=anchor_token(anchor))
            else:lib.attach(project,'experimental:'+project.get('topic','untitled'),aid,record['asset_id'],record['revision'],expected_anchor=anchor_token(anchor),replace=True)
            return ('project',(project,before))
        self.work(job)

    def attach(self):self.change()
    def detach(self):self.change(True)

    def poll(self):
        if self.closed:return
        try:
            kind,value=self.events.get_nowait();self.busy=False
            for b in self.controls:b.configure(state='normal')
            if kind=='error':self.note.set(value)
            else:
                action,data=value
                if action=='list':
                    self.list.delete(*self.list.get_children());self.records={r['asset_id']:r for r in data}
                    for r in data:self.list.insert('','end',iid=r['asset_id'],text=r['asset_id']+' / '+r['original_filename'],values=(r['media_type'],r['rights']['rights_status'],r['revision']))
                    self.note.set(f'{len(data)} записей; offset {self.offset}')
                elif action=='thumbnail':
                    self.image=tk.PhotoImage(file=data['preview_path'])
                    self.poster.configure(image=self.image);self.note.set('Poster: производный preview, не оценка качества.')
                elif action=='project':
                    candidate,before=data
                    if encoded(self.snapshot()) != before:raise LibraryError('STALE_TARGET')
                    if self.timeline_panel and self.timeline_panel.editor:
                        self.timeline_panel.editor.asset_change(candidate,expected_project=before);self.timeline_panel.draw()
                    else:candidate['approved']=False;self.apply_project(candidate)
                    self.note.set('Связь изменена. В Timeline доступны Undo/Redo; примените и сохраните проект явно.')
                else:
                    self.detail.delete('1.0','end');self.detail.insert('1.0',json.dumps(data,ensure_ascii=False,indent=2));self.note.set('Готово. Обновите каталог.')
        except queue.Empty:pass
        except Exception as exc:self.note.set(str(exc))
        self.poll_id=self.after(80,self.poll)

    def cleanup(self,event):
        if event.widget is self:
            self.closed=True
            if self.poll_id:self.after_cancel(self.poll_id)
            # Release Tcl finalizers in their creating thread, even if a local worker finishes later.
            self.poster.configure(image='') if self.poster.winfo_exists() else None
            self.image=None
            self.query=self.filter_by=self.anchor_id=self.note=None
