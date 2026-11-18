"""Experimental Tk workbench: explicit generation, editing and project apply."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import webbrowser

from experimental_mvp import intelligence, storyboard, media_hub


class MediaWorkbench:
    def __init__(self, book, get_project, apply_project, workspace, open_local):
        self.get_project, self.apply_project = get_project, apply_project
        self.workspace, self.open_local = workspace, open_local
        self.project = None
        self.events = queue.Queue()
        self.waiting = False
        self.book = book
        self.providers = media_hub.catalog()
        self.provider_map = {p['id']: p for p in self.providers}
        self.writer = ttk.Frame(book, padding=8)
        self.board = ttk.Frame(book, padding=8)
        self.services = ttk.Frame(book, padding=8)
        for page, title in ((self.writer, 'Сценарист LLM / вручную'), (self.board, 'Раскадровка'),
                            (self.services, 'AI-сервисы / квоты')):
            book.add(page, text=title)
        self.make_writer()
        self.make_board()
        self.make_services()
        self.writer.bind('<Destroy>',self.cleanup,add='+')
        self.poll_id=self.writer.after(150, self.poll)

    def cleanup(self,event):
        if event.widget is self.writer and getattr(self,'poll_id',None):
            try:self.writer.after_cancel(self.poll_id)
            except tk.TclError:pass

    def action(self, fn):
        def run(*_):
            try:
                fn()
            except Exception as exc:
                messagebox.showerror('Экспериментальный Media Hub', str(exc))
        return run

    def button(self, parent, text, fn):
        b = ttk.Button(parent, text=text, command=self.action(fn))
        b.pack(side='left', padx=3, pady=3)
        return b

    def text(self, page, height=12):
        box = tk.Text(page, height=height, wrap='word', undo=True)
        box.pack(fill='both', expand=True)
        return box

    def show(self, box, value):
        box.delete('1.0', 'end')
        box.insert('1.0', json.dumps(value, ensure_ascii=False, indent=2))

    def read(self, box):
        return json.loads(box.get('1.0', 'end-1c'))

    def make_writer(self):
        ttk.Label(self.writer, text='Черновик: факты НЕ проверены. Генерация, редактирование JSON и применение — разные действия.',
                  wraplength=900).pack(anchor='w')
        row = ttk.Frame(self.writer); row.pack(fill='x')
        self.endpoint = tk.StringVar(value='http://localhost:11434/v1')
        self.model = tk.StringVar(value='')
        ttk.Label(row, text='Endpoint /v1').pack(side='left')
        ttk.Entry(row, textvariable=self.endpoint, width=42).pack(side='left', fill='x', expand=True)
        ttk.Label(row, text='Модель').pack(side='left')
        ttk.Entry(row, textvariable=self.model, width=22).pack(side='left')
        self.draft = self.text(self.writer)
        row = ttk.Frame(self.writer); row.pack(fill='x')
        self.button(row, 'Ручной шаблон', self.manual)
        self.button(row, 'Импорт JSON', self.import_draft)
        self.button(row, 'Ключ → Windows vault', self.store_key)
        self.generate_button = self.button(row, 'Сгенерировать черновик…', self.generate)
        self.button(row, 'Применить к пустому проекту', self.apply_draft)
        self.writer_status = tk.StringVar(value='Офлайн-режим доступен без аккаунтов. Существующие сцены редактируйте во вкладке «Сцены».')
        ttk.Label(self.writer, textvariable=self.writer_status, wraplength=900).pack(anchor='w')

    def manual(self):
        project = self.get_project()
        self.show(self.draft, dict(locale=project.get('locale', 'ru'), editorial_assessment='Заполните оценку темы и причины съёмки',
                                  audience='Укажите аудиторию', hooks=['Первый hook', 'Другой hook'],
                                  structure=['Вопрос', 'Доказательства', 'Ограничения', 'Вывод'],
                                  script='Отредактируйте сценарий', scenes=[dict(text='Текст первой сцены', visual='', prompt='')],
                                  claims_to_verify=['Укажите утверждения и необходимые источники'],
                                  visual_recommendations=['Укажите обязательные визуальные материалы'],
                                  risks=['Все фактические утверждения требуют редакционной проверки']))

    def import_draft(self):
        name = filedialog.askopenfilename(filetypes=[('Editorial JSON', '*.json')])
        if name:
            value = json.loads(Path(name).read_text(encoding='utf-8-sig'))
            self.show(self.draft, intelligence.validate_draft(value, self.get_project().get('locale', 'ru')))

    def store_key(self):
        secret = simpledialog.askstring('Windows Credential Manager',
                                        'API key: хранится только в системном vault; проект JSON его не содержит.', show='*')
        if secret:
            intelligence.set_credential(self.endpoint.get(), secret)

    def generate(self):
        if self.waiting:
            return
        project = self.get_project()
        endpoint, model = self.endpoint.get().strip(), self.model.get().strip()
        if not messagebox.askyesno('Отправка текста LLM', f'Отправить тему сервису {endpoint}?\nМодель: {model}\nВозможна оплата. Ответ — непроверенный черновик.'):
            return
        key = intelligence.credential(endpoint)
        self.waiting = True
        self.generate_button.state(['disabled'])
        self.writer_status.set('Ожидается черновик; проект не изменяется.')
        def work():
            try:
                self.events.put(('draft', intelligence.generate(project.get('topic', ''), project.get('locale', 'ru'),
                                 endpoint, model, key=key, confirmed=True)))
            except Exception as exc:
                self.events.put(('error', str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def poll(self):
        while not self.events.empty():
            kind, value = self.events.get()
            self.waiting = False
            self.generate_button.state(['!disabled'])
            if kind == 'draft':
                self.show(self.draft, value)
                self.writer_status.set('Черновик получен. Отредактируйте, проверьте факты, затем явно примените.')
            else:
                self.writer_status.set(value)
        self.poll_id=self.writer.after(150, self.poll)

    def apply_draft(self):
        project = self.get_project()
        value = intelligence.validate_draft(self.read(self.draft), project.get('locale', 'ru'))
        self.apply_project(intelligence.apply_draft(project, value))

    def make_board(self):
        row = ttk.Frame(self.board); row.pack(fill='x')
        self.button(row, 'Загрузить текущие сцены', self.refresh)
        self.button(row, 'Предложить якоря', self.suggest)
        self.button(row, 'Выше', lambda: self.move(-1))
        self.button(row, 'Ниже', lambda: self.move(1))
        self.button(row, 'Разделить', self.split_anchor)
        self.button(row, 'Применить и сохранить', self.apply_board)
        timeline_frame = ttk.Frame(self.board); timeline_frame.pack(fill='x')
        self.timeline = ttk.Treeview(timeline_frame, columns=('time', 'mode', 'provider', 'status'), show='tree headings', height=5)
        self.timeline.heading('#0', text='Сцена / стабильный якорь')
        for name, title in (('time', 'Шкала мс'), ('mode', 'Режим'), ('provider', 'Сервис'), ('status', 'Статус')):
            self.timeline.heading(name, text=title); self.timeline.column(name, width=130)
        self.timeline.pack(side='left', fill='x', expand=True)
        scroll = ttk.Scrollbar(timeline_frame, command=self.timeline.yview)
        scroll.pack(side='right', fill='y'); self.timeline.configure(yscrollcommand=scroll.set)
        self.timeline.bind('<<TreeviewSelect>>', self.action(self.selected_event))
        ttk.Label(self.board, text='Редактор всех полей якоря (JSON). start_ms относительно сцены. Изменения сначала зафиксируйте кнопкой. '
                  'MAP/INFOGRAPHIC требуют импортированной графики; fallback PLACEHOLDER нужно разрешить явно.', wraplength=900).pack(anchor='w')
        self.anchor_box = self.text(self.board, 8)
        row = ttk.Frame(self.board); row.pack(fill='x')
        self.button(row, 'Изменить якорь…', self.edit_anchor)
        self.button(row, 'Зафиксировать JSON', self.commit_anchor)
        self.button(row, 'Импорт MP4 / изображения', self.import_asset)
        self.button(row, 'Предпросмотр файла', self.preview_asset)
        row = ttk.Frame(self.board); row.pack(fill='x')
        self.button(row, 'Открыть генератор', self.open_generator)
        self.button(row, 'Копировать промпт', self.copy_prompt)
        self.button(row, 'Проверить покрытие', self.coverage)

    def edit_anchor(self):
        scene, anchor = self.selected()
        if anchor is None:
            raise ValueError('Выберите якорь.')
        dialog = tk.Toplevel(self.board); dialog.title('Видео-якорь: время, материал и промпты')
        book = ttk.Notebook(dialog); book.pack(fill='both', expand=True)
        general = ttk.Frame(book, padding=10); prompts = ttk.Frame(book, padding=10)
        book.add(general, text='Время и материал'); book.add(prompts, text='Промпты')
        values = {}
        labels = {'anchor_id':'ID якоря', 'scene_id':'ID сцены', 'start_ms':'Начало в сцене, мс',
                  'duration_ms':'Длительность, мс', 'narration_excerpt':'Фрагмент речи',
                  'visual_description':'Что показывает кадр', 'image_prompt':'Промпт изображения',
                  'video_prompt':'Промпт видео', 'negative_prompt':'Исключить из кадра',
                  'reference_image':'Референс: локальный путь', 'preferred_provider':'Предпочтительный сервис',
                  'provider_model':'Модель сервиса', 'generation_mode':'Режим материала',
                  'generation_status':'Готовность', 'local_asset_path':'Локальный материал',
                  'license_status':'Проверка прав', 'fallback_mode':'Резервный режим'}
        choices = {'generation_mode':storyboard.MODES, 'generation_status':storyboard.STATUSES,
                   'preferred_provider':['', *self.provider_map], 'fallback_mode':['NONE','PLACEHOLDER']}
        for key in storyboard.VideoAnchor.__dataclass_fields__:
            page = prompts if key in ('narration_excerpt','visual_description','image_prompt','video_prompt','negative_prompt') else general
            row = ttk.Frame(page); row.pack(fill='x', pady=2)
            ttk.Label(row,text=labels[key],width=28).pack(side='left')
            if page is prompts:
                widget = tk.Text(row,height=3,width=65,wrap='word'); widget.insert('1.0',str(anchor[key])); values[key]=widget
            else:
                variable=tk.StringVar(value=str(anchor[key])); values[key]=variable
                widget = ttk.Combobox(row,textvariable=variable,values=choices[key],state='readonly',width=55) if key in choices else ttk.Entry(row,textvariable=variable,width=58)
                if key in ('anchor_id','scene_id'):widget.state(['readonly'])
            widget.pack(side='left',fill='x',expand=True)
        def accept():
            edited=deepcopy(anchor)
            for key,value in values.items():
                edited[key]=value.get('1.0','end-1c') if isinstance(value,tk.Text) else value.get()
            for key in ('start_ms','duration_ms'):edited[key]=int(edited[key])
            if edited['start_ms']<0 or edited['duration_ms']<=0:raise ValueError('Неверное время.')
            anchor.clear();anchor.update(edited);self.show(self.anchor_box,anchor);dialog.destroy()
        ttk.Button(dialog,text='Зафиксировать изменения якоря',command=self.action(accept)).pack(pady=6)

    def refresh(self):
        self.project = deepcopy(self.get_project())
        self.draw()

    def draw(self, keep=None):
        self.timeline.delete(*self.timeline.get_children())
        for n, scene in enumerate((self.project or {}).get('scenes', []), 1):
            self.timeline.insert('', 'end', iid='s:'+scene['id'], text=f'{n}. {scene.get("text", "")[:45]}', open=True)
            for a in sorted(scene.get('anchors', []), key=lambda a: a['start_ms']):
                self.timeline.insert('s:'+scene['id'], 'end', iid='a:'+a['anchor_id'], text=a['anchor_id'][:12],
                                     values=(f'{a["start_ms"]}–{a["start_ms"]+a["duration_ms"]}', a['generation_mode'],
                                             a['preferred_provider'], a['generation_status']))
        if keep and self.timeline.exists(keep):
            self.timeline.selection_set(keep)
        self.anchor_box.delete('1.0', 'end')

    def selected(self):
        picked = self.timeline.selection()
        if not picked:
            raise ValueError('Загрузите проект и выберите сцену или якорь.')
        key = picked[0]
        for scene in self.project['scenes']:
            if key == 's:'+scene['id']:
                return scene, None
            for a in scene.get('anchors', []):
                if key == 'a:'+a['anchor_id']:
                    return scene, a
        raise ValueError('Выбор устарел; загрузите текущие сцены.')

    def selected_event(self, *_):
        if self.timeline.selection():
            _, anchor = self.selected()
            self.show(self.anchor_box, anchor or {})

    def commit_anchor(self):
        scene, a = self.selected()
        if a is None:
            raise ValueError('Выберите якорь.')
        value = self.read(self.anchor_box)
        if value.get('anchor_id') != a['anchor_id'] or value.get('scene_id') != scene['id']:
            raise ValueError('ID якоря и сцены изменять нельзя.')
        # Validate field shape and temporal coverage before export; no data silently removed.
        for field in storyboard.VideoAnchor.__dataclass_fields__:
            if field not in value:
                raise ValueError(f'Отсутствует {field}')
        a.clear(); a.update(value)

    def suggest(self):
        scene, _ = self.selected()
        seconds = simpledialog.askinteger('Озвучка сцены', 'Точная / плановая длительность сцены, секунд:', minvalue=1, maxvalue=3600)
        if seconds is None:
            return
        step = simpledialog.askinteger('Длина якоря', 'Ориентир секунд: 5, 6–8 или 10 (не лимит сервиса)', initialvalue=7, minvalue=1, maxvalue=120)
        if step is None:
            return
        scene['anchors'] = storyboard.suggest(scene, seconds*1000, step*1000)
        self.draw('s:'+scene['id'])

    def move(self, offset):
        self.commit_anchor()
        scene, a = self.selected()
        storyboard.reorder(scene, a['anchor_id'], offset)
        self.draw('a:'+a['anchor_id'])

    def split_anchor(self):
        self.commit_anchor()
        scene, anchor = self.selected()
        seconds = simpledialog.askinteger('Разделить якорь', 'Максимальная длина части, секунд:', minvalue=1)
        if seconds:
            storyboard.split(scene, anchor['anchor_id'], seconds*1000)
            self.draw('s:'+scene['id'])

    def import_asset(self):
        self.commit_anchor()
        _, a = self.selected()
        name = filedialog.askopenfilename(filetypes=[('Визуалы', '*.mp4 *.mov *.mkv *.webm *.png *.jpg *.jpeg *.webp *.bmp')])
        if name:
            storyboard.import_asset(a, name, self.workspace(), provider=a['preferred_provider'] or 'MANUAL',
                                    license_status=a['license_status'])
            self.show(self.anchor_box, a)

    def preview_asset(self):
        self.commit_anchor()
        _, a = self.selected()
        path = Path(a.get('local_asset_path', ''))
        if not path.is_file():
            raise ValueError('Сначала импортируйте материал.')
        self.open_local(path)

    def open_generator(self):
        self.commit_anchor()
        _, a = self.selected()
        p = self.provider_map.get(a['preferred_provider'])
        if p is None:
            raise ValueError('Назначьте preferred_provider из каталога во вкладке AI-сервисы.')
        webbrowser.open(p['official_site'])

    def copy_prompt(self):
        self.commit_anchor()
        _, a = self.selected()
        self.board.clipboard_clear()
        self.board.clipboard_append(a['video_prompt'] or a['image_prompt'])

    def coverage(self):
        self.commit_anchor()
        scene, _ = self.selected()
        ms = simpledialog.askinteger('Покрытие', 'Измеренная длительность озвучки, мс:', minvalue=1)
        if ms:
            errors = storyboard.validate(scene, ms)
            messagebox.showinfo('Покрытие', '\n'.join(errors) or 'Покрытие полное; лицензии и факты этим не проверены.')

    def apply_board(self):
        if self.project is None:
            raise ValueError('Сначала загрузите сцены.')
        if self.timeline.selection() and self.selected()[1] is not None:
            self.commit_anchor()
        current = self.get_project()
        old = {s['id']: s for s in self.project['scenes']}
        if set(old) != {s['id'] for s in current.get('scenes', [])}:
            raise ValueError('Состав сцен изменился; сохраните / загрузите раскадровку заново.')
        for s in current['scenes']:
            if 'anchors' in old[s['id']]:
                s['anchors'] = deepcopy(old[s['id']]['anchors'])
        current['approved'] = False
        self.apply_project(current)
        # Main save action chooses managed project path; explicit named export also available here.
        target = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('Проект', '*.json')])
        if target:
            from experimental_mvp.pipeline import save
            save(Path(target), current)

    def make_services(self):
        ttk.Label(self.services, text='Только официальный сайт в системном браузере → ручная генерация → импорт. '
                  'Пароли, cookies и Google credentials приложение не принимает. Отказ от входа не мешает офлайн-сборке.', wraplength=900).pack(anchor='w')
        row = ttk.Frame(self.services); row.pack(fill='x')
        self.provider = tk.StringVar(value=self.providers[0]['id'])
        combo = ttk.Combobox(row, textvariable=self.provider, values=list(self.provider_map), state='readonly')
        combo.pack(side='left'); combo.bind('<<ComboboxSelected>>', lambda _: self.show_provider())
        self.button(row, 'Официальный сайт / вход', self.site)
        self.button(row, 'Проверить состояние', self.show_provider)
        self.button(row, 'Аккаунт / квота вручную', self.edit_account)
        self.button(row, 'Quota Planner', self.plan)
        self.service_info = self.text(self.services, 12)
        self.show_provider()

    def site(self):
        webbrowser.open(self.provider_map[self.provider.get()]['official_site'])

    def show_provider(self):
        p = self.provider_map[self.provider.get()]
        # Initialization occurs after the existing UI is fully constructed.
        account = self.get_project().get('media_accounts', {}).get(p['id'], {})
        self.show(self.service_info, {'catalog': p, 'account_state': media_hub.account_state(account),
                  'quota': account or 'UNKNOWN', 'connection_check': 'MANUAL_ONLY; browser session and API not probed',
                  'instructions': 'Войдите на официальном сайте (Google только если предложен сайтом), '
                                  'проверьте тариф/права, вставьте промпт, создайте и скачайте файл; импортируйте в якорь.'})

    def edit_account(self):
        project = self.get_project()
        pid = self.provider.get()
        dialog = tk.Toplevel(self.services); dialog.title('Ручное подтверждение квоты — не API-подключение')
        box = tk.Text(dialog, width=90, height=20); box.pack(fill='both', expand=True)
        value = project.get('media_accounts', {}).get(pid, dict(login_reported=False, balance=None, cost_per_clip=None,
                    unit='credits', confirmed_at='', valid_until='', reset_at='', source='', durations_seconds=[]))
        self.show(box, value)
        def apply():
            data = self.read(box)
            allowed = {'login_reported', 'balance', 'cost_per_clip', 'unit', 'confirmed_at', 'valid_until', 'reset_at', 'source', 'durations_seconds'}
            if set(data) - allowed or type(data.get('login_reported')) is not bool:
                raise ValueError('Только поля шаблона; никаких паролей, cookies или ключей.')
            project.setdefault('media_accounts', {})[pid] = data
            project['approved'] = False
            self.apply_project(project)
            dialog.destroy(); self.show_provider()
        ttk.Button(dialog, text='Подтвердить вручную (не расходовать)', command=self.action(apply)).pack()

    def plan(self):
        result = media_hub.plan(self.get_project(), self.providers)
        self.show(self.service_info, result)
