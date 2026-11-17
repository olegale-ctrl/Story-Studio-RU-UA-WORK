"""Tk interface for editing and producing one local project at a time."""
import os
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import uuid

from experimental_mvp.pipeline import (DEMOS, ROOT, audio_status, brief, build, executable,
                                       identify, load, save, scene_audio)


def launch():
    root = tk.Tk()
    root.title("Story Studio · Экспериментальный MVP")
    root.geometry("1050x790")
    root.minsize(760, 650)
    shell = ttk.Frame(root, padding=16)
    shell.pack(fill="both", expand=True)
    state = {"path": None, "video": None, "busy": False, "project": {}}
    updates = queue.Queue()
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

    def button(parent, label, action):
        widget = ttk.Button(parent, text=label, command=action)
        widget.pack(side="left", padx=(0, 5))
        buttons.append(widget)
        return widget

    def text_tab(book, name):
        page = ttk.Frame(book, padding=8)
        book.add(page, text=name)
        text = tk.Text(page, wrap="word", font=("Segoe UI", 11), undo=True)
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

    def fill(value, path=None):
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
        state.update(path=path, video=None, project=value)
        show_scene(None)
        refresh(scenes[0]["id"] if scenes else None)
        notebook.select(scenes_tab)
        status.set(str(path) if path else "Новый проект")

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
        status.set(f"Сохранено: {path}")
        return path, value

    def editorial():
        write("brief", brief(topic.get(), locale.get()))
        if baseline.get():
            # The established preview uses its own existing, explicit input schema.
            from scripts.editor_preview import preview
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

    def perform(work, done):
        state["busy"] = True
        for widget in buttons:
            widget.state(["disabled"])
        progress.start(15)

        def worker():
            try:
                updates.put((done, work()))
            except Exception as exc:
                updates.put(("error", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def run():
        if not approved.get():
            messagebox.showinfo("Редакционное решение", "Подтвердите переход к производству.")
            return
        try:
            path, project = save_project()
        except OSError as exc:
            messagebox.showerror("Сохранение проекта", str(exc))
            return
        state["video"] = None
        perform(lambda: build(project, path.parent / "runs",
                              lambda s: updates.put(("progress", s))), "done")

    def poll():
        while not updates.empty():
            kind, value = updates.get()
            if kind == "progress":
                status.set(value)
                continue
            state["busy"] = False
            progress.stop()
            for widget in buttons:
                widget.state(["!disabled"])
            commit_scene()
            refresh(selected)
            if kind == "audio":
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
        root.after(100, poll)

    def play():
        video = state["video"]
        if not video and state["path"]:
            runs = list((state["path"].parent / "runs").glob("run-*/final.mp4"))
            if runs:
                video = max(runs, key=lambda p: p.stat().st_mtime)
        if video:
            os.startfile(video)
        else:
            messagebox.showinfo("Видео", "Сначала соберите проект.")

    def close():
        if state["busy"]:
            messagebox.showinfo("Сборка", "Дождитесь завершения сборки.")
        else:
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
        ("Демо RU", lambda: fill(load(DEMOS / "ru.json"))),
        ("Демо UA", lambda: fill(load(DEMOS / "uk.json"))),
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
        widget = tk.Text(row, height=height, wrap="word", font=("Segoe UI", 10), undo=True)
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
    ttk.Combobox(row, textvariable=scene_voice, values=voice_options, state="readonly",
                 width=20).pack(side="left")
    ttk.Label(shell, text="Общая дорожка имеет приоритет. Без неё используется файл сцены или Edge TTS. "
                          "Таймкоды реплик оценочные.", wraplength=920).pack(anchor="w", pady=6)
    controls = ttk.Frame(shell)
    controls.pack(fill="x")
    ttk.Checkbutton(controls, text="Подтверждаю производство этой версии",
                    variable=approved).pack(side="left", padx=6)
    button(controls, "Собрать MP4", run)
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
    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, poll)
    root.mainloop()
