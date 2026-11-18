"""Real Tk widget/worker checks; dialogs mocked, no native Windows acceptance claim."""
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

@unittest.skipUnless(os.name=='nt' or os.environ.get('DISPLAY'),'Tk display unavailable')
class LibraryWidgetTests(unittest.TestCase):
    def test_import_search_metadata_thumbnail_attach_detach_retire(self):
        import tkinter as tk
        from tkinter import ttk
        from experimental_mvp.asset_ui import AssetLibraryPanel
        from experimental_mvp.asset_library import AssetLibrary
        from experimental_mvp.test_asset_library import LibraryTests,cleared
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);image=folder/'схема.png'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=80x60','-frames:v','1','-threads','1',str(image)],check=True)
            root=tk.Tk();root.geometry('1100x800');errors=[];root.report_callback_exception=lambda *args:errors.append(str(args))
            state={'project':LibraryTests().project()};main=threading.get_ident();workers=[]
            def apply(p):self.assertEqual(threading.get_ident(),main);state['project']=p
            panel=AssetLibraryPanel(root,lambda:deepcopy(state['project']),apply,folder/'lib');panel.pack(fill='both',expand=True)
            def drain():
                end=time.monotonic()+15
                while panel.busy and time.monotonic()<end:root.update();time.sleep(.01)
                root.update();self.assertFalse(panel.busy);self.assertFalse(errors)
            try:
                original=AssetLibrary.import_file
                def observed(lib,*a,**k):workers.append(threading.get_ident());return original(lib,*a,**k)
                with patch('experimental_mvp.asset_ui.filedialog.askopenfilename',return_value=str(image)),patch.object(AssetLibrary,'import_file',observed):panel.import_file();drain()
                self.assertTrue(workers);self.assertNotEqual(workers[0],main)
                panel.refresh();drain();self.assertEqual(len(panel.records),1)
                aid=next(iter(panel.records));panel.list.selection_set(aid);root.update();drain();self.assertIsNotNone(panel.image)
                r=panel.records[aid]
                with patch('experimental_mvp.asset_ui.simpledialog.askstring',return_value=json.dumps({'rights':cleared()})):
                    panel.metadata();drain()
                panel.refresh();drain();panel.list.selection_set(aid);root.update();drain();panel.load_anchors()
                panel.attach();drain();self.assertIn('asset_library_binding',state['project']['scenes'][0]['anchors'][0])
                panel.detach();drain();self.assertNotIn('asset_library_binding',state['project']['scenes'][0]['anchors'][0])
                panel.filter_by.set('rights_status');panel.query.set('CLEARED_FOR_EXPERIMENT');panel.refresh();drain()
                panel.list.selection_set(aid);root.update();drain()
                with patch('experimental_mvp.asset_ui.messagebox.askyesno',return_value=True):panel.retire();drain()
                self.assertEqual(AssetLibrary(folder/'lib').get(aid)['lifecycle_status'],'RETIRED')
                self.assertEqual(panel.records[aid]['original_filename'],image.name)
                panel.recover();drain()
            finally:root.destroy()

    def test_background_edit_stale_result_not_applied_and_close_is_safe(self):
        import tkinter as tk
        from experimental_mvp.asset_ui import AssetLibraryPanel
        from experimental_mvp.asset_library import encoded
        with tempfile.TemporaryDirectory() as tmp:
            root=tk.Tk();state={'p':{'topic':'old','scenes':[]}};applied=[]
            panel=AssetLibraryPanel(root,lambda:deepcopy(state['p']),applied.append,Path(tmp)/'lib');panel.pack()
            old=encoded(state['p']);state['p']['topic']='edited'
            panel.events.put(('ok',('project',({'topic':'result','scenes':[]},old))))
            panel.poll();self.assertEqual(applied,[]);self.assertIn('STALE_TARGET',panel.note.get())
            panel.work(lambda:('message','finished after close'));root.destroy();time.sleep(.05)
