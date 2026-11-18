"""Run from repo root with DISPLAY; exercises actual main Tk widgets, not OS playback."""
from pathlib import Path
import json
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk
from experimental_mvp.ui import launch
from experimental_mvp.timeline_ui import TimelinePanel

root=tk.Tk();errors=[];result={}
def descendants(w):
    out=[]
    for c in w.winfo_children():out.append(c);out+=descendants(c)
    return out

def exercise():
    try:
        widgets=descendants(root);book=next(w for w in widgets if isinstance(w,ttk.Notebook))
        result['tabs']=[book.tab(t,'text') for t in book.tabs()]
        next(w for w in widgets if isinstance(w,ttk.Button) and w.cget('text')=='Демо RU').invoke();root.update()
        panel=next(w for w in widgets if isinstance(w,TimelinePanel));panel.refresh();root.update()
        result['ru_scenes']=len(panel.editor.project['scenes']);result['ru_anchors']=sum(len(s['anchors']) for s in panel.editor.project['scenes'])
        result['ru_topic']=panel.editor.project['topic'];result['measured_audio']=panel.editor.timing['measured']
        a=panel.editor.project['scenes'][0]['anchors'][0];panel.sid=a['scene_id'];panel.aid=a['anchor_id']
        panel.edit('set',start_ms=100);assert not panel.editor.project['approved'];panel.undo()
        book.select(panel);panel.position=2500;panel.draw();root.update()
        result['canvas_items']=len(panel.canvas.find_all());result['windows']='WINDOWS_NOT_RUN'
        print(json.dumps(result,ensure_ascii=False),flush=True)
        root.after(6000,root.destroy)
    except Exception as exc:errors.append(repr(exc));root.destroy()
root.report_callback_exception=lambda *args:errors.append(str(args))
root.after(300,exercise)
with patch('experimental_mvp.ui.tk.Tk',return_value=root),patch('tkinter.messagebox.showerror',side_effect=lambda *a,**k:errors.append(str(a))):launch()
print('GUI_ERRORS',errors)
if errors:raise SystemExit(1)
