"""Exact RC02 Tk widget-driven Linux exercise. File-dialog selection automated, not Windows/manual acceptance."""
import json,sys,os
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk,messagebox
BASE=Path('/workspace/work/rc02-independent');OUT=Path('/workspace/work/rc02-addendum-evidence')
os.environ['STORY_MVP_HOME']=str(OUT/'isolated-profile')
sys.path.insert(0,str(BASE))
from experimental_mvp.ui import launch
errors=[];root=tk.Tk();phase=sys.argv[1]
def children(widget):
 result=[]
 for c in widget.winfo_children():result.append(c);result.extend(children(c))
 return result
def button(parent,label):return next(w for w in children(parent) if isinstance(w,ttk.Button) and w.cget('text')==label)
def replace(widget,text):widget.delete('1.0','end');widget.insert('1.0',text)
def saved():return next((OUT/'isolated-profile/projects').glob('*/project.json'))
def fail(*args,**kwargs):errors.append(str(args));root.after(10,root.destroy)
def captions(manual=True):
 button(root,'Субтитры сцены').invoke();root.update()
 dialog=next(w for w in children(root) if isinstance(w,tk.Toplevel))
 entries=[w for w in children(dialog) if isinstance(w,ttk.Entry)]
 if not manual:
  button(dialog,'Рассчитать заново').invoke();button(dialog,'Сохранить субтитры').invoke();root.update();return
 for w,value in zip(entries,['100','999999','Ручные титры — Київ']):root.setvar(w.cget('textvariable'),value)
 button(dialog,'Применить к реплике').invoke();root.update()
 tree=next(w for w in children(dialog) if isinstance(w,ttk.Treeview))
 assert any('invalid' in tree.item(i,'tags') for i in tree.get_children())
 button(dialog,'Сохранить субтитры').invoke();root.update();assert dialog.winfo_exists()
 root.setvar(entries[1].cget('textvariable'),'1000')
 button(dialog,'Сохранить субтитры').invoke();root.update()
def exercise():
 try:
  book=next(w for w in children(root) if isinstance(w,ttk.Notebook))
  tree=next(w for w in children(root) if isinstance(w,ttk.Treeview))
  if phase=='create':
   button(root,'Демо RU').invoke();root.update();assert len(tree.get_children())==2
   button(root,'Новый').invoke();root.update();assert not tree.get_children()
   for _ in range(2):button(root,'Добавить сцену').invoke();root.update()
   scene_page=root.nametowidget(next(t for t in book.tabs() if book.tab(t,'text')=='Сцены'))
   fields=[w for w in children(scene_page) if isinstance(w,tk.Text)]
   ids=list(tree.get_children());tree.selection_set(ids[0]);root.update()
   replace(fields[0],'Красивое видео ещё не объяснение.');replace(fields[3],str(OUT/'Кириллица и пробелы/Моя схема.png'))
   tree.selection_set(ids[1]);root.update();replace(fields[0],'Начните с вопроса зрителя.')
   button(root,'Выше').invoke();root.update();assert tree.get_children()[0]==ids[1]
   button(root,'Добавить сцену').invoke();root.update();button(root,'Удалить').invoke();root.update();assert len(tree.get_children())==2
   for label in children(root):
    if isinstance(label,ttk.Label) and label.cget('text')=='Озвучка MP3/WAV':
     entry=next(w for w in label.master.winfo_children() if isinstance(w,ttk.Entry));root.setvar(entry.cget('textvariable'),str(OUT/'Кириллица и пробелы/Озвучка сцены.wav'));break
   button(root,'Сохранить').invoke();root.update()
   captions();captions(False);captions()
   button(root,'Сохранить').invoke();root.update()
   value=json.loads(saved().read_text());assert value['captions_by_scene'];assert set(s['id'] for s in value['scenes'])==set(ids)
   (OUT/'gui-expected.json').write_text(json.dumps(value,ensure_ascii=False,indent=2))
   print('PASS: GUI RU open/new/add/delete/text/image/reorder/manual captions/recalculate/overrun/save')
  else:
   with patch('experimental_mvp.ui.filedialog.askopenfilename',return_value=str(saved())):button(root,'Открыть').invoke()
   root.update();button(root,'Сохранить').invoke();root.update()
   before=json.loads((OUT/'gui-expected.json').read_text());after=json.loads(saved().read_text())
   assert after['scenes']==before['scenes'];assert after['captions_by_scene']==before['captions_by_scene']
   print('PASS: GUI fresh process reopen preserves scene IDs/text/image/captions UTF-8')
  root.after(10,root.destroy)
 except Exception as exc:errors.append(repr(exc));root.after(10,root.destroy)
root.report_callback_exception=lambda *args:fail(*args)
root.after(300,exercise)
with patch('experimental_mvp.ui.tk.Tk',return_value=root),patch.object(messagebox,'showerror',side_effect=fail),patch.object(messagebox,'askyesno',return_value=True):launch()
print('ERRORS',errors)
if errors:raise SystemExit(1)
