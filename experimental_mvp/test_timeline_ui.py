"""Real Tk canvas events under a display; never Windows acceptance by inference."""
from copy import deepcopy
import os
from pathlib import Path
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch


@unittest.skipUnless(os.name=='nt' or os.environ.get('DISPLAY'),'Tk display unavailable')
class CanvasTests(unittest.TestCase):
    def test_selection_drag_resize_keyboard_undo_save_and_stale_apply(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        from experimental_mvp.test_timeline import project,audio
        root=tk.Tk();root.geometry('1100x750')
        try:
            with tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);audio(folder/'a.wav');p=project();p['audio']=str(folder/'a.wav')
                state={'p':p};errors=[]
                panel=TimelinePanel(root,lambda:deepcopy(state['p']),lambda value:state.update(p=value),lambda:folder,lambda _:None)
                panel.pack(fill='both',expand=True);root.update();panel.refresh();root.update()
                anchor=panel.editor.project['scenes'][0]['anchors'][0];aid=anchor['anchor_id']
                x=panel.x(200);y=125*panel.y_scale
                panel.canvas.event_generate('<ButtonPress-1>',x=round(x),y=round(y));root.update()
                self.assertEqual(panel.aid,aid)
                panel.canvas.event_generate('<B1-Motion>',x=round(x+4),y=round(y));panel.canvas.event_generate('<ButtonRelease-1>',x=round(x+4),y=round(y));root.update()
                self.assertEqual(panel.anchor()['start_ms'],100)
                panel.edit('set',start_ms=0)
                edge=panel.x(1000)-2
                panel.canvas.event_generate('<ButtonPress-1>',x=round(edge),y=round(y));root.update()
                panel.canvas.event_generate('<ButtonRelease-1>',x=round(edge+4),y=round(y));root.update()
                self.assertEqual(panel.anchor()['duration_ms'],1100)
                panel.canvas.focus_force();root.update();panel.canvas.event_generate('<Right>');panel.canvas.event_generate('<Right>');root.update()
                self.assertEqual(panel.anchor()['start_ms'],200)
                panel.resize(-200);self.assertEqual(panel.anchor()['duration_ms'],900)
                panel.undo();panel.redo();self.assertEqual(panel.editor.locate(panel.editor.project,aid)[1]['duration_ms'],900)
                panel.aid=aid;panel.start.set('0');panel.length.set('1000');panel.numbers()
                panel.scale(1.5);panel.seek.set('1250');panel.goto();self.assertEqual(panel.position,1250)
                self.assertTrue(panel.editor.dirty)
                with patch('tkinter.messagebox.askyesnocancel',return_value=None):self.assertFalse(panel.confirm_leave())
                with patch('tkinter.filedialog.asksaveasfilename',return_value=str(folder/'шкала.json')):panel.save()
                self.assertTrue((folder/'шкала.json').is_file());self.assertFalse(panel.editor.dirty)
                state['p']['topic']='Changed elsewhere'
                with self.assertRaises(ValueError):panel.apply()
                self.assertEqual(state['p']['topic'],'Changed elsewhere')
                panel.destroy()
        finally:root.destroy()

    def test_missing_audio_estimate_never_becomes_measured(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        from experimental_mvp.test_timeline import project
        root=tk.Tk()
        try:
            p=project();panel=TimelinePanel(root,lambda:deepcopy(p),lambda _:None,lambda:Path('/no-audio-cache'),lambda _:None)
            panel.pack();root.update();panel.refresh()
            self.assertFalse(panel.editor.timing['measured'])
            self.assertTrue(all(s['audio_duration_kind']=='UNKNOWN_NOT_MEASURED' for s in panel.editor.timing['scenes']))
            self.assertIn('Аудио не измерено',panel.info.get());panel.destroy()
        finally:root.destroy()

    def test_main_window_protects_fresh_unsaved_edits_and_save_failure(self):
        import tkinter as tk
        from tkinter import ttk
        from experimental_mvp.ui import launch
        r=tk.Tk();failures=[];observed=[]
        def children(w):
            result=[]
            for c in w.winfo_children():result.append(c);result+=children(c)
            return result
        def exercise():
            try:
                entry=next(w for w in children(r) if isinstance(w,ttk.Entry))
                r.setvar(entry.cget('textvariable'),'Unsaved topic')
                close=r.protocol('WM_DELETE_WINDOW')
                with patch('tkinter.messagebox.askyesnocancel',return_value=None):r.tk.call(close)
                self.assertTrue(r.winfo_exists());observed.append('cancel-keeps-window')
                with patch('tkinter.messagebox.askyesnocancel',return_value=True),patch('experimental_mvp.ui.save',side_effect=PermissionError('denied')),patch('tkinter.messagebox.showerror') as error:
                    r.tk.call(close);self.assertTrue(r.winfo_exists());self.assertTrue(error.called);observed.append('save-failure-keeps-window')
                with patch('tkinter.messagebox.askyesnocancel',return_value=False):r.tk.call(close)
            except Exception as exc:failures.append(repr(exc));r.destroy()
        r.after(300,exercise)
        with tempfile.TemporaryDirectory() as tmp,patch('experimental_mvp.ui.tk.Tk',return_value=r),patch('experimental_mvp.ui.ROOT',Path(tmp)):
            launch()
        self.assertFalse(failures,failures);self.assertEqual(len(observed),2)

    def test_preview_worker_cancel_and_no_source_mutation(self):
        import tkinter as tk
        from experimental_mvp.timeline_ui import TimelinePanel
        from experimental_mvp.test_timeline import project,audio
        from experimental_mvp.pipeline import BuildStopped
        root=tk.Tk()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);audio(folder/'a.wav');p=project();p['audio']=str(folder/'a.wav');snapshot=deepcopy(p)
                opened=[];panel=TimelinePanel(root,lambda:deepcopy(p),lambda _:None,lambda:folder,opened.append)
                panel.pack();root.update();panel.refresh();panel.aid=p['scenes'][0]['anchors'][0]['anchor_id']
                def waiting(*args,**kw):
                    end=time.monotonic()+3
                    while not kw['cancelled']() and time.monotonic()<end:time.sleep(.01)
                    raise BuildStopped('Предпросмотр отменён')
                with patch('experimental_mvp.timeline.preview',side_effect=waiting):
                    panel.make_preview('anchor');panel.stop.set();end=time.monotonic()+3
                    while panel.busy and time.monotonic()<end:root.update();time.sleep(.01)
                self.assertFalse(panel.busy);self.assertFalse(opened);self.assertEqual(p,snapshot);panel.destroy()
        finally:root.destroy()


if __name__=='__main__':unittest.main()
