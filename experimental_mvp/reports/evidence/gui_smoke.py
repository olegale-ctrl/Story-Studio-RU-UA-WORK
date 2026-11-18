"""Run from repository root with a real display; does not test OS player/login/vault."""
from pathlib import Path
import tempfile
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk, messagebox
from experimental_mvp.ui import launch

errors = []
root = tk.Tk()

def descendants(widget):
    result = []
    for child in widget.winfo_children():
        result.append(child)
        result.extend(descendants(child))
    return result

def fail(*args, **kwargs):
    errors.append(str(args))
    root.after(1, root.destroy)

def exercise():
    try:
        widgets = descendants(root)
        book = next(w for w in widgets if isinstance(w, ttk.Notebook))
        buttons = {w.cget('text'): w for w in widgets if isinstance(w, ttk.Button)}
        print('TABS', [book.tab(t, 'text') for t in book.tabs()])
        buttons['Демо RU'].invoke()
        root.update()
        trees = [w for w in widgets if isinstance(w, ttk.Treeview)]
        print('RU_SCENES', len(trees[0].get_children()))
        buttons['Загрузить текущие сцены'].invoke()
        root.update()
        print('BOARD_SCENES', len(trees[1].get_children()), 'ANCHORS',
              sum(len(trees[1].get_children(c)) for c in trees[1].get_children()))
        first = trees[1].get_children(trees[1].get_children()[0])[0]
        trees[1].selection_set(first); root.update()
        buttons['Изменить якорь…'].invoke(); root.update()
        dialog = next(w for w in descendants(root) if isinstance(w, tk.Toplevel))
        accept = next(w for w in descendants(dialog) if isinstance(w, ttk.Button)
                      and w.cget('text') == 'Зафиксировать изменения якоря')
        accept.invoke(); root.update()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'Розкадровка.json'
            with patch('experimental_mvp.media_ui.filedialog.asksaveasfilename', return_value=str(target)):
                buttons['Применить и сохранить'].invoke(); root.update()
            assert target.is_file()
            print('BOARD_SAVE_REOPEN', len(__import__('json').loads(target.read_text())['scenes']))
        buttons['Проверить состояние'].invoke(); buttons['Quota Planner'].invoke()
        buttons['Демо UA'].invoke(); root.update()
        print('UA_SCENES', len(trees[0].get_children()))
        print('GUI_ERRORS', errors)
    except Exception as exc:
        errors.append(repr(exc))
    finally:
        root.after(50, root.destroy)

root.report_callback_exception = lambda *args: fail(*args)
root.after(300, exercise)
with patch('experimental_mvp.ui.tk.Tk', return_value=root), patch.object(messagebox, 'showerror', side_effect=fail):
    launch()
if errors:
    print('GUI_ERRORS', errors)
    raise SystemExit(1)
