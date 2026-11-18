"""Widget-level Linux/Xvfb or Windows smoke; not a substitute for independent desktop acceptance."""
from copy import deepcopy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


@unittest.skipUnless(os.name == 'nt' or os.environ.get('DISPLAY'), 'Tk display unavailable')
class WorkbenchWidgetTests(unittest.TestCase):
    def test_tabs_anchor_edit_reorder_save_and_manual_writer(self):
        import tkinter as tk
        from tkinter import ttk
        from experimental_mvp.media_ui import MediaWorkbench
        from experimental_mvp.pipeline import identify, load
        from experimental_mvp.storyboard import suggest
        root=tk.Tk();root.withdraw()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                state={'value':dict(locale='uk',topic='Ручна історія',scenes=[dict(text='Неперевірений сценарій')])}
                identify(state['value'])
                scene=state['value']['scenes'][0];scene['anchors']=suggest(scene,2000,1000)
                original=[a['anchor_id'] for a in scene['anchors']]
                book=ttk.Notebook(root);book.pack()
                panel=MediaWorkbench(book,lambda:deepcopy(state['value']),lambda p:state.update(value=p),lambda:Path(tmp),lambda _:None)
                self.assertEqual(len(book.tabs()),3)
                panel.refresh();panel.timeline.selection_set('a:'+original[0]);root.update()
                panel.selected_event();panel.move(1);root.update();panel.selected_event()
                self.assertEqual(panel.project['scenes'][0]['anchors'][1]['anchor_id'],original[0])
                with patch('experimental_mvp.media_ui.filedialog.asksaveasfilename',return_value=str(Path(tmp)/'проект.json')):
                    panel.apply_board()
                reopened=load(Path(tmp)/'проект.json')
                self.assertFalse(reopened['approved'])
                self.assertEqual(reopened['scenes'][0]['anchors'][1]['anchor_id'],original[0])
                panel.show_provider();panel.plan()
                state['value']={'locale':'uk','topic':'Новий проєкт','scenes':[]}
                panel.manual();panel.apply_draft()
                self.assertEqual(state['value']['locale'],'uk')
                self.assertEqual(len(state['value']['scenes']),1)
                self.assertFalse(state['value']['approved'])
        finally:root.destroy()


if __name__=='__main__':unittest.main()
