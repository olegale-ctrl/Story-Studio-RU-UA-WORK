"""Tk interface for editing and producing one local project at a time."""
import os
import subprocess
import sys
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import uuid

from experimental_mvp.captions import CueError, calculated, validate

from experimental_mvp.pipeline import (DEMOS, ROOT, BuildStopped, audio_status, brief, build,
                                       check_project, executable, export_history, preview_signature,
                                       identify, load, preview_audio, render_preview, save, scene_audio)


def open_local(path):
    if os.name == "nt":
        os.startfile(path)
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", str(path)])


def launch():
    root = tk.Tk()
    available = {name.lower() for name in font.families(root)}
    ui_family = next((name for name in ("Segoe UI", "DejaVu Sans", "Noto Sans", "Arial")
                      if name.lower() in available), font.nametofont("TkDefaultFont").actual("family"))
    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
        font.nametofont(name).configure(family=ui_family)
    root.title("Story Studio · Экспериментальный MVP")
    root.geometry("1050x790")
    root.minsize(760, 650)
    shell = ttk.Frame(root, padding=16)
    shell.pack(fill="both", expand=True)
    state = {"path": None, "video": None, "busy": False, "project": {}}
    updates = queue.Queue()
    stop_requested = threading.Event()
    preview_label = tk.StringVar(value="Предпросмотр ролика не создан")
    topic = tk.StringVar()
    locale = tk.StringVar(value="ru")
    audio = tk.StringVar()
    baseline = tk.StringVar()
    voice = tk.StringVar()
    voice_options = ("", "ru-RU-SvetlanaNeural", "ru-RU-DmitryNeural", "uk-UA-PolinaNeural")
    approved = tk.BooleanVar()
    status = tk.StringVar(value="Создайте или откройте проект.")
    editor = {}
    scenes = []
    selected = None
    scene_audio_path = tk.StringVar()
    scene_voice = tk.StringVar()
    scene_fields = {}
    buttons = []

    after_ids=set()
    def later(ms,fn):
        def invoke():
            after_ids.discard(token)
            fn()
        token=root.after(ms,invoke);after_ids.add(token)
    def cleanup(event):
        if event.widget is root:
            for token in list(after_ids):
                try:root.after_cancel(token)
                except tk.TclError:pass
            after_ids.clear()
    root.bind('<Destroy>',cleanup,add='+')

    def button(parent, label, action):
        widget = ttk.Button(parent, text=label, command=action)
        widget.pack(side="left", padx=(0, 5))
        buttons.append(widget)
        return widget

    def text_tab(book, name):
        page = ttk.Frame(book, padding=8)
        book.add(page, text=name)
        text = tk.Text(page, wrap="word", font=(ui_family, 11), undo=True)
        text.pack(side="left", expand=True, fill="both")
        scroll = ttk.Scrollbar(page, command=text.yview)
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)
        return text

    def read(key):
        return editor[key].get("1.0", "end-1c")

    def write(key, value):
        editor[key].delete("1.0", "end")
        editor[key].insert("1.0", value)

    def signature():
        from experimental_mvp.timeline_ui import content
        return content(collect())

    def leave_project():
        panel=state.get("timeline_panel")
        try:
            if panel and not panel.confirm_leave():return False
        except Exception as exc:
            messagebox.showerror("Временная шкала",str(exc));return False
        if state.get("saved_content") is not None and signature()!=state["saved_content"]:
            answer=messagebox.askyesnocancel("Несохранённые изменения", "Сохранить текущий проект? «Нет» — отбросить изменения.")
            if answer is None:return False
            if answer:
                try:save_project()
                except Exception as exc:
                    messagebox.showerror("Сохранение проекта",str(exc));return False
        return True

    def apply_edit(value):
        old=state.get("saved_content")
        fill(value,state["path"],force=True)
        state["saved_content"]=old

    def fill(value, path=None, *, force=False):
        if not force and not leave_project():return
        if not force and state.get("timeline_panel"):
            state["timeline_panel"].editor=None
            state["timeline_panel"].base=None
            state["timeline_panel"].draw()

        topic.set(value.get("topic", ""))
        locale.set(value["locale"])
        audio.set(value.get("audio", ""))
        voice.set(value.get("voice", ""))
        write("timing", "")
        baseline.set(value.get("story_input", ""))
        approved.set(False)
        write("brief", value.get("brief", ""))
        scenes[:] = value.get("scenes", [])
        identify({"scenes": scenes})
        state.update(path=path, video=None, project=value, movie=None)
        preview_label.set("Предпросмотр ролика не создан")
        show_scene(None)
        refresh(scenes[0]["id"] if scenes else None)
        notebook.select(scenes_tab)
        history = export_history(path.parent / "runs") if path else []
        if history and history[0][1] != "complete":
            status.set(f"Последний экспорт не завершён: {history[0][0].name}")
        else:
            status.set(str(path) if path else "Новый проект")
        state["saved_content"]=signature()

    def collect():
        commit_scene()
        return {**state["project"], "topic": topic.get().strip(), "locale": locale.get(),
                "audio": audio.get().strip(), "voice": voice.get(), "story_input": baseline.get().strip(),
                "brief": read("brief"), "scenes": [dict(scene) for scene in scenes],
                "approved": approved.get()}

    def cache_path():
        path = state["path"]
        if path and path.resolve().is_relative_to(ROOT / "projects"):
            return path.parent / "runs" / "scene-audio"
        return None

    def current():
        return next((scene for scene in scenes if scene["id"] == selected), None)

    def commit_scene():
        scene = current()
        if scene is not None:
            for key, widget in scene_fields.items():
                scene[key] = widget.get("1.0", "end-1c").strip()
            scene["audio"] = scene_audio_path.get().strip()
            scene["voice"] = scene_voice.get()

    def show_scene(scene):
        nonlocal selected
        selected = scene["id"] if scene else None
        for key, widget in scene_fields.items():
            widget.delete("1.0", "end")
            widget.insert("1.0", scene.get(key, "") if scene else "")
        scene_audio_path.set(scene.get("audio", "") if scene else "")
        scene_voice.set(scene.get("voice", "") if scene else "")

    def refresh(keep=None):
        tree.delete(*tree.get_children())
        project = {"locale": locale.get(), "voice": voice.get(), "audio": audio.get()}
        cache = cache_path()
        for index, scene in enumerate(scenes, 1):
            label = audio_status(project, scene, cache) if cache else (
                "Общая дорожка" if audio.get() else "Ожидает сборки")
            tree.insert("", "end", iid=scene["id"],
                        values=(index, scene.get("text", "")[:65], label))
        if keep and tree.exists(keep):
            tree.selection_set(keep)
            tree.see(keep)
        show_scene(next((scene for scene in scenes if scene["id"] == keep), None))

    def change_selection(_event=None):
        selection = tree.selection()
        key = selection[0] if selection else None
        if key != selected:
            commit_scene()
            show_scene(next((scene for scene in scenes if scene["id"] == key), None))

    def change_order(offset):
        commit_scene()
        scene = current()
        if scene is None:
            return
        index = scenes.index(scene)
        target = index + offset
        if 0 <= target < len(scenes):
            scenes[index], scenes[target] = scenes[target], scenes[index]
            approved.set(False)
            refresh(scene["id"])

    def add_scene():
        commit_scene()
        scene = {"id": uuid.uuid4().hex, "text": ""}
        scenes.append(scene)
        approved.set(False)
        refresh(scene["id"])

    def remove_scene():
        scene = current()
        if scene and messagebox.askyesno("Удалить сцену", "Удалить выбранную сцену?"):
            index = scenes.index(scene)
            scenes.remove(scene)
            state["project"].get("captions_by_scene", {}).pop(scene["id"], None)
            state["project"].get("timeline", {}).get("scene_durations_ms", {}).pop(scene["id"], None)
            approved.set(False)
            refresh(scenes[min(index, len(scenes)-1)]["id"] if scenes else None)

    def new():
        fill({"locale": locale.get()})

    def open_project():
        path = filedialog.askopenfilename(filetypes=[("Story Studio JSON", "*.json")])
        if path:
            try:
                fill(load(Path(path)), Path(path))
            except (OSError, ValueError, TypeError, KeyError) as exc:
                messagebox.showerror("Открытие проекта", str(exc))

    def save_project():
        value = collect()
        path = state["path"]
        if path is None or not path.resolve().is_relative_to(ROOT / "projects"):
            path = ROOT / "projects" / uuid.uuid4().hex[:12] / "project.json"
        save(path, value)
        state["path"] = path
        state["saved_content"]=signature()
        status.set(f"Сохранено: {path}")
        return path, value

    def editorial():
        write("brief", brief(topic.get(), locale.get()))
        if baseline.get():
            # The established preview uses its own existing, explicit input schema.
            try:
                from scripts.editor_preview import preview
            except ModuleNotFoundError as exc:
                if exc.name not in {"scripts", "scripts.editor_preview"}:
                    raise
                notebook.select(0)
                messagebox.showinfo(
                    "Editorial Preview",
                    "Анализ внешнего JSON доступен в полном checkout Story Studio. "
                    "Запустите редактор из его корня и выберите JSON снова. "
                    "Локальный шаблон темы уже показан.",
                )
                return
            snapshot = preview(load(Path(baseline.get())))
            from pprint import pformat
            write("brief", read("brief") + "\n\nStory Intelligence · Existing input\n"
                  + pformat(snapshot, width=100, sort_dicts=False))
        notebook.select(0)

    def choose(variable, types):
        name = filedialog.askopenfilename(filetypes=types)
        if name:
            variable.set(name)

    def image():
        if current() is None:
            return
        name = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if name:
            widget = scene_fields["image"]
            widget.delete("1.0", "end")
            widget.insert("1.0", name)
            approved.set(False)

    def selected_audio():
        if current() is None:
            raise ValueError("Выберите сцену.")
        path, project = save_project()
        index = next(i for i, scene in enumerate(project["scenes"]) if scene["id"] == selected)
        workspace = path.parent / "runs"
        return project, index, workspace, preview_audio(project, index, workspace)

    def edit_captions():
        project, index, _, (_, _, length, approximate) = selected_audio()
        scene = project["scenes"][index]
        key = scene["id"]
        automatic = calculated(scene["text"], length)
        overrides = state["project"].setdefault("captions_by_scene", {})
        dialog = tk.Toplevel(root)
        dialog.title(f"Субтитры сцены {index + 1}")
        dialog.transient(root)
        dialog.grab_set()
        box = ttk.Frame(dialog, padding=12)
        box.pack(fill="both", expand=True)
        wording = "Приблизительный отрезок общей дорожки" if approximate else "Длительность озвучки"
        ttk.Label(box, text=f"{wording}: {length} мс. Начало и конец относительно сцены.").pack(anchor="w")
        caption_tree = ttk.Treeview(box, columns=("start", "end", "text"), show="headings",
                                   height=7, selectmode="browse")
        for name, label, width in (("start", "Начало, мс", 90), ("end", "Конец, мс", 90),
                                   ("text", "Реплика", 540)):
            caption_tree.heading(name, text=label)
            caption_tree.column(name, width=width, stretch=name == "text")
        caption_tree.tag_configure("invalid", background="#ffd8d8", foreground="#761a1a")
        caption_tree.pack(fill="both", expand=True, pady=5)
        start_var, end_var, text_var, error = (tk.StringVar(master=dialog) for _ in range(4))
        entries = ttk.Frame(box)
        entries.pack(fill="x", pady=5)
        for var, width in ((start_var, 9), (end_var, 9), (text_var, 55)):
            ttk.Entry(entries, textvariable=var, width=width).pack(side="left", padx=2)
        ttk.Label(box, textvariable=error, foreground="#9f1b1b").pack(anchor="w")

        def select_row(_event=None):
            picked = caption_tree.selection()
            if picked:
                for var, value in zip((start_var, end_var, text_var),
                                      caption_tree.item(picked[0], "values")):
                    var.set(value)

        def verify_rows():
            for item in caption_tree.get_children():
                caption_tree.item(item, tags=())
            rows = []
            try:
                for i, item in enumerate(caption_tree.get_children()):
                    a, b, text = caption_tree.item(item, "values")
                    try:
                        rows.append({"start_ms": int(a), "end_ms": int(b), "text": text})
                    except ValueError:
                        raise CueError(index + 1, i, "таймкод должен быть целым числом мс.") from None
                validate(rows, length, index + 1)
            except CueError as exc:
                items = caption_tree.get_children()
                if exc.index < len(items):
                    item = items[exc.index]
                    caption_tree.item(item, tags=("invalid",))
                    caption_tree.selection_set(item)
                    caption_tree.see(item)
                    select_row()
                error.set(str(exc))
                return None
            error.set("")
            return rows

        def populate(rows):
            caption_tree.delete(*caption_tree.get_children())
            for row in rows:
                caption_tree.insert("", "end", values=(row["start_ms"], row["end_ms"], row["text"]))
            items = caption_tree.get_children()
            if items:
                caption_tree.selection_set(items[0])
                select_row()

        def apply_row():
            items = caption_tree.selection()
            if items:
                caption_tree.item(items[0], values=(start_var.get(), end_var.get(), text_var.get()))
            return verify_rows()

        def store_captions():
            rows = apply_row()
            if rows is None:
                return
            if rows == automatic:
                overrides.pop(key, None)
            else:
                overrides[key] = rows
            save_project()
            dialog.destroy()

        caption_tree.bind("<<TreeviewSelect>>", select_row)
        populate(overrides.get(key, automatic))
        verify_rows()
        actions = ttk.Frame(box)
        actions.pack(fill="x", pady=5)
        for label, action in (("Применить к реплике", apply_row),
                              ("Рассчитать заново", lambda: (populate(automatic), verify_rows())),
                              ("Сохранить субтитры", reported(store_captions))):
            ttk.Button(actions, text=label, command=action).pack(side="left", padx=3)

    def preview_scene():
        project, index, workspace, audio_data = selected_audio()
        perform(lambda: render_preview(project, index, workspace, audio_data,cancelled=stop_requested.is_set), "preview",stoppable=True)

    def retry():
        if current() is None:
            return
        if audio.get().strip():
            messagebox.showinfo("Озвучка", "Очистите общую дорожку, чтобы использовать озвучку сцен.")
            return
        if not approved.get():
            messagebox.showinfo("Редакционное решение", "Подтвердите производство этой версии.")
            return
        path, project = save_project()
        scene = next(scene for scene in project["scenes"] if scene["id"] == selected)
        cache = path.parent / "runs" / "scene-audio"

        def work():
            scene_audio(project, scene, cache, executable("ffmpeg"), executable("ffprobe"),
                        lambda s: updates.put(("progress", s)))
            return "Озвучка сцены готова"

        perform(work, "audio")

    def check():
        project = collect()
        workspace = cache_path()
        runs = workspace.parent if workspace else ROOT / "runs"
        perform(lambda: check_project(project, runs), "checked")

    def show_issues(issues):
        if not issues:
            messagebox.showinfo("Проверка проекта", "Локальные проверки пройдены.")
            return
        dialog = tk.Toplevel(root)
        dialog.title("Проверка проекта")
        dialog.transient(root)
        box = ttk.Frame(dialog, padding=12)
        box.pack(fill="both", expand=True)
        listing = tk.Listbox(box, width=103, height=min(14, len(issues)), exportselection=False)
        listing.pack(fill="both", expand=True)
        for key, field, message, pending in issues:
            index = next((i for i, scene in enumerate(scenes, 1) if scene["id"] == key), None)
            location = f"Сцена {index} / {field}" if index else field
            listing.insert("end", f"{'Ожидание' if pending else 'Ошибка'} · {location} · {message}")
        listing.selection_set(0)

        def fix():
            picked = listing.curselection()
            if not picked:
                return
            key, field, _, _ = issues[picked[0]]
            dialog.destroy()
            if key and tree.exists(key):
                commit_scene()
                refresh(key)
                notebook.select(scenes_tab)
            if field == "image":
                image()
            elif field == "scene_audio":
                choose(scene_audio_path, [("Аудио", "*.mp3 *.wav")])
            elif field == "audio":
                choose(audio, [("Аудио", "*.mp3 *.wav")])
            elif field == "captions":
                reported(edit_captions)()
            elif field == "scenes":
                add_scene()
                notebook.select(scenes_tab)
            elif field == "voice":
                scene_voice_box.focus_set()
            elif field in scene_fields:
                scene_fields[field].focus_set()

        ttk.Button(box, text="Перейти к исправлению", command=fix).pack(anchor="w", pady=5)
        listing.bind("<Double-Button-1>", lambda _: fix())

    def movie_preview():
        path, project = save_project()
        # Local preview uses the same explicit experimental-render confirmation as export.
        signature = preview_signature(project)
        perform(lambda: (build(project, path.parent / "runs", progress_event,
                               preview=True, cancelled=stop_requested.is_set), signature),
                "movie", stoppable=True)

    def update_preview_status():
        movie = state.get("movie")
        if movie:
            stale = movie[1] != preview_signature(collect())
            preview_label.set("Предпросмотр устарел" if stale else "Предпросмотр актуален")
        later(500, update_preview_status)

    def progress_event(message):
        updates.put(("progress", message))

    def perform(work, done, stoppable=False):
        stop_requested.clear()
        if stoppable:
            stop_button.state(["!disabled"])
        state["busy"] = True
        for widget in buttons:
            widget.state(["disabled"])
        progress.start(15)

        def worker():
            try:
                updates.put((done, work()))
            except BuildStopped as exc:
                updates.put(("stopped", str(exc)))
            except Exception as exc:
                updates.put(("error", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def run():
        if not approved.get():
            messagebox.showinfo("Редакционное решение", "Подтвердите локальную экспериментальную сборку.")
            return
        try:
            path, project = save_project()
        except OSError as exc:
            messagebox.showerror("Сохранение проекта", str(exc))
            return
        state["video"] = None
        perform(lambda: build(project, path.parent / "runs", progress_event,
                              cancelled=stop_requested.is_set), "done", stoppable=True)

    def poll():
        while not updates.empty():
            kind, value = updates.get()
            if kind == "progress":
                status.set(value)
                continue
            state["busy"] = False
            progress.stop()
            stop_button.state(["disabled"])
            for widget in buttons:
                widget.state(["!disabled"])
            if kind in ("preview","movie") and stop_requested.is_set():
                from experimental_mvp.pipeline import discard_preview_result
                try:discard_preview_result(value[0],value[0].parent.parent)
                except (OSError,ValueError) as exc:
                    messagebox.showerror("Очистка preview",str(exc))
                status.set("Предпросмотр отменён; результат не открыт.")
                continue
            commit_scene()
            refresh(selected)
            if kind == "checked":
                status.set("Проверка проекта завершена")
                show_issues(value)
            elif kind == "movie":
                state["movie"] = value
                status.set("Предпросмотр ролика готов. В проигрывателе доступна дорожка субтитров.")
                try:
                    open_local(value[0])
                except OSError as exc:
                    messagebox.showerror("Предпросмотр ролика", str(exc))
            elif kind == "stopped":
                status.set(value + " Экспорт не завершён.")
            elif kind == "preview":
                path, approximate = value
                suffix = " (приблизительные границы общей дорожки)" if approximate else ""
                status.set(f"Предпросмотр сцены{suffix}: {path}")
                try:
                    open_local(path)
                except OSError as exc:
                    messagebox.showerror("Предпросмотр сцены", str(exc))
            elif kind == "audio":
                status.set(value)
            elif kind == "done":
                state["video"] = value
                status.set(f"Готово: {value}")
                timing = load(value.parent / "timing.json")
                write("timing", "\n".join(
                    f"{i}. {(end-start)/1000:.2f} с"
                    for i, (start, end) in enumerate(timing["scenes_ms"], 1))
                    + "\n\nТаймкоды реплик оценочные. " + timing["method"])
            else:
                status.set("Ошибка сборки")
                messagebox.showerror("Ошибка сборки", value)
        later(100, poll)

    def play():
        video = state["video"]
        if not video and state["path"]:
            history = export_history(state["path"].parent / "runs")
            if history and history[0][1] != "complete":
                messagebox.showinfo("Видео", "Последний экспорт не завершён. Запустите сборку снова.")
                return
            if history:
                video = history[0][0] / "final.mp4"
        if video:
            open_local(video)
        else:
            messagebox.showinfo("Видео", "Сначала соберите проект.")

    def close():
        if state["busy"]:
            messagebox.showinfo("Сборка", "Дождитесь завершения сборки.")
        elif leave_project():
            root.destroy()

    def reported(action):
        def invoke():
            try:
                action()
            except Exception as exc:
                messagebox.showerror("Story Studio", str(exc))
        return invoke

    bar = ttk.Frame(shell)
    bar.pack(fill="x", pady=(0, 10))
    for name, action in (
        ("Новый", new), ("Открыть", open_project), ("Сохранить", save_project),
        ("Демо RU", lambda: fill(load(DEMOS / "timeline" / "ru.json"))),
        ("Демо UA", lambda: fill(load(DEMOS / "timeline" / "uk.json"))),
    ):
        button(bar, name, reported(action))
    topics = ttk.Frame(shell)
    topics.pack(fill="x", pady=(0, 7))
    ttk.Label(topics, text="Тема").pack(side="left", padx=(0, 8))
    ttk.Entry(topics, textvariable=topic).pack(side="left", expand=True, fill="x")
    ttk.Combobox(topics, textvariable=locale, values=("ru", "uk"), state="readonly",
                 width=5).pack(side="left", padx=8)
    ttk.Combobox(topics, textvariable=voice, values=voice_options, state="readonly",
                 width=22).pack(side="left", padx=(0, 8))
    button(topics, "Анализ темы", reported(editorial))
    for title, variable, types in (
        ("Озвучка MP3/WAV", audio, [("Аудио", "*.mp3 *.wav")]),
        ("Вход Story Intelligence (необязательно)", baseline, [("JSON", "*.json")]),
    ):
        row = ttk.Frame(shell)
        row.pack(fill="x", pady=(0, 7))
        ttk.Label(row, text=title, width=43).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", expand=True, fill="x")
        button(row, "Выбрать", lambda v=variable, t=types: choose(v, t))
    notebook = ttk.Notebook(shell)
    notebook.pack(fill="both", expand=True)
    for key, label in (("brief", "Редакторский анализ"), ("timing", "Длительности и тайминг")):
        editor[key] = text_tab(notebook, label)
    scenes_tab = ttk.Frame(notebook, padding=8)
    notebook.insert(1, scenes_tab, text="Сцены")
    tree = ttk.Treeview(scenes_tab, columns=("order", "text", "audio"), show="headings",
                        height=5, selectmode="browse")
    for column, heading, width in (("order", "№", 44), ("text", "Сцена", 470),
                                   ("audio", "Озвучка", 160)):
        tree.heading(column, text=heading)
        tree.column(column, width=width, stretch=column == "text")
    tree.pack(fill="x")
    tree.bind("<<TreeviewSelect>>", change_selection)
    actions = ttk.Frame(scenes_tab)
    actions.pack(fill="x", pady=5)
    for label, action in (("Добавить сцену", add_scene), ("Удалить", remove_scene),
                          ("Выше", lambda: change_order(-1)), ("Ниже", lambda: change_order(1))):
        button(actions, label, action)
    for key, label, height in (("text", "Текст диктора", 3), ("visual", "Описание", 1),
                               ("prompt", "Промпт", 1), ("image", "Путь к изображению", 1)):
        row = ttk.Frame(scenes_tab)
        row.pack(fill="x")
        ttk.Label(row, text=label, width=24).pack(side="left")
        widget = tk.Text(row, height=height, wrap="word", font=(ui_family, 10), undo=True)
        widget.pack(side="left", fill="x", expand=True)
        scene_fields[key] = widget
        if key == "image":
            button(row, "Выбрать", image)
    row = ttk.Frame(scenes_tab)
    row.pack(fill="x", pady=4)
    ttk.Label(row, text="Аудиофайл сцены", width=24).pack(side="left")
    ttk.Entry(row, textvariable=scene_audio_path).pack(side="left", fill="x", expand=True)
    button(row, "MP3/WAV", lambda: choose(scene_audio_path, [("Аудио", "*.mp3 *.wav")]))
    button(row, "Подготовить / повторить сцену", reported(retry))
    ttk.Label(row, text="Голос сцены").pack(side="left", padx=(8, 3))
    scene_voice_box = ttk.Combobox(row, textvariable=scene_voice, values=voice_options,
                                   state="readonly", width=20)
    scene_voice_box.pack(side="left")
    ttk.Label(shell, text="Общая дорожка имеет приоритет. Без неё используется файл сцены или Edge TTS. "
                          "Таймкоды реплик оценочные.", wraplength=920).pack(anchor="w", pady=6)
    controls = ttk.Frame(shell)
    controls.pack(fill="x")
    ttk.Checkbutton(controls, text="Подтверждаю локальную сборку (без production permissions)",
                    variable=approved).pack(side="left", padx=6)
    button(controls, "Субтитры сцены", reported(edit_captions))
    button(controls, "Предпросмотр сцены", reported(preview_scene))
    build_controls = ttk.Frame(shell)
    build_controls.pack(fill="x", pady=(4, 0))
    button(build_controls, "Проверить проект", reported(check))
    button(build_controls, "Предпросмотр ролика", reported(movie_preview))
    button(build_controls, "Собрать MP4", run)
    stop_button = ttk.Button(build_controls, text="Остановить сборку", command=stop_requested.set)
    stop_button.state(["disabled"])
    stop_button.pack(side="left", padx=4)
    ttk.Label(build_controls, textvariable=preview_label).pack(side="left", padx=5)
    button(controls, "Просмотр MP4", reported(play))
    progress = ttk.Progressbar(shell, mode="indeterminate")
    progress.pack(fill="x", pady=(12, 3))
    ttk.Label(shell, textvariable=status, wraplength=950).pack(anchor="w")
    for variable in (topic, locale, audio, baseline, voice):
        variable.trace_add("write", lambda *_: approved.set(False))
    for widget in [editor["brief"], *scene_fields.values()]:
        widget.bind("<KeyPress>", lambda _: approved.set(False), add="+")
    scene_audio_path.trace_add("write", lambda *_: approved.set(False) if scene_audio_path.get() !=
                               (current() or {}).get("audio", "") else None)
    scene_voice.trace_add("write", lambda *_: approved.set(False) if scene_voice.get() !=
                          (current() or {}).get("voice", "") else None)
    from experimental_mvp.media_ui import MediaWorkbench
    media_workbench = MediaWorkbench(notebook, collect, apply_edit,
                                    lambda: ROOT / "media-hub", open_local)
    from experimental_mvp.timeline_ui import TimelinePanel
    timeline_panel=TimelinePanel(notebook,collect,apply_edit,
        lambda: state["path"].parent/"runs" if state["path"] else ROOT/"runs",open_local)
    notebook.add(timeline_panel,text="Временная шкала")
    state["timeline_panel"]=timeline_panel
    from experimental_mvp.asset_ui import AssetLibraryPanel
    library_panel = AssetLibraryPanel(notebook, collect, apply_edit, ROOT / "asset-library", timeline_panel)
    notebook.add(library_panel, text="Asset Library")
    state["saved_content"]=signature()
    root.protocol("WM_DELETE_WINDOW", close)
    later(100, poll)
    later(500, update_preview_status)
    root.mainloop()
