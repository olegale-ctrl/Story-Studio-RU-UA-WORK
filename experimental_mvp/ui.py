"""Tk interface for editing and producing one local project at a time."""
import os
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import uuid

from experimental_mvp.pipeline import DEMOS, ROOT, brief, build, load, save


def launch():
    root = tk.Tk()
    root.title("Story Studio · Экспериментальный MVP")
    root.geometry("1050x790")
    root.minsize(760, 650)
    shell = ttk.Frame(root, padding=16)
    shell.pack(fill="both", expand=True)
    state = {"path": None, "video": None, "busy": False}
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
        write("script", "\n\n".join(s["text"] for s in value.get("scenes", [])))
        write("scenes", "\n---\n".join(
            "\n".join((s.get("visual", ""), s.get("prompt", ""), s.get("image", "")))
            for s in value.get("scenes", [])))
        state.update(path=path, video=None)
        status.set(str(path) if path else "Новый проект")

    def collect():
        paragraphs = [s.strip() for s in read("script").split("\n\n") if s.strip()]
        visuals = read("scenes").split("\n---\n")
        scenes = []
        for i, text in enumerate(paragraphs):
            fields = (visuals[i].split("\n", 2) if i < len(visuals) else []) + [""] * 3
            scenes.append({"text": text, "visual": fields[0].strip(),
                           "prompt": fields[1].strip(), "image": fields[2].strip()})
        return {"topic": topic.get().strip(), "locale": locale.get(),
                "audio": audio.get().strip(), "voice": voice.get(), "story_input": baseline.get().strip(),
                "brief": read("brief"), "scenes": scenes, "approved": approved.get()}

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
        name = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if name:
            widget = editor["scenes"]
            current = widget.index("insert linestart")
            widget.delete(current, current + " lineend")
            widget.insert(current, name)

    def run():
        if not approved.get():
            messagebox.showinfo("Редакционное решение", "Подтвердите переход к производству.")
            return
        try:
            path, project = save_project()
        except OSError as exc:
            messagebox.showerror("Сохранение проекта", str(exc))
            return
        state["busy"] = True
        state["video"] = None
        for widget in buttons:
            widget.state(["disabled"])
        progress.start(15)

        def work():
            try:
                video = build(project, path.parent / "runs", lambda s: updates.put(("progress", s)))
                updates.put(("done", video))
            except Exception as exc:
                updates.put(("error", str(exc)))

        threading.Thread(target=work, daemon=True).start()

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
            if kind == "done":
                state["video"] = value
                status.set(f"Готово: {value}")
                timing = load(value.parent / "timing.json")
                write("timing", "\n".join(
                    f"{i}. {(end-start)/1000:.2f} с"
                    for i, (start, end) in enumerate(timing["scenes_ms"], 1))
                    + "\n\n" + timing["method"])
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
    for key, label in (("brief", "Редакторский анализ"), ("script", "Сценарий"),
                       ("scenes", "Раскадровка"), ("timing", "Длительности и тайминг")):
        editor[key] = text_tab(notebook, label)
    ttk.Label(shell, text="Сценарий: один абзац на сцену. Раскадровка: описание, промпт, путь к изображению. Между сценами — строка --- .",
              wraplength=900).pack(anchor="w", pady=6)
    controls = ttk.Frame(shell)
    controls.pack(fill="x")
    button(controls, "Изображение в текущую строку", image)
    ttk.Checkbutton(controls, text="Подтверждаю производство этой версии",
                    variable=approved).pack(side="left", padx=6)
    button(controls, "Собрать MP4", run)
    button(controls, "Просмотр MP4", reported(play))
    progress = ttk.Progressbar(shell, mode="indeterminate")
    progress.pack(fill="x", pady=(12, 3))
    ttk.Label(shell, textvariable=status, wraplength=950).pack(anchor="w")
    for variable in (topic, locale, audio, baseline, voice):
        variable.trace_add("write", lambda *_: approved.set(False))
    for key in ("script", "scenes", "brief"):
        editor[key].bind("<KeyPress>", lambda _: approved.set(False), add="+")
    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, poll)
    root.mainloop()
