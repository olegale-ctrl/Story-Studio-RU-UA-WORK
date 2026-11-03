"""Minimal desktop voice preview UI for Story Studio RU/UA (stdlib Tkinter).

Runs Edge TTS or an explicitly trusted local Silero model in a child process.
"""
from __future__ import annotations
import hashlib
import os
import queue
import re
import subprocess
import sys
import threading
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.hardware_profile import probe, recommend

VOICE_CATALOG = {
    'ru': {'female': 'ru-RU-SvetlanaNeural', 'male': 'ru-RU-DmitryNeural'},
    'uk': {'female': 'uk-UA-PolinaNeural', 'male': 'uk-UA-OstapNeural'},
}
SILERO_VOICES = {'ru': ('ru_dmitriy', 'ru_igor', 'ru_roman'), 'uk': ('ukr_igor', 'ukr_roman')}
RATE_PATTERN = re.compile(r'^[+-]\d{1,3}%$')
PITCH_PATTERN = re.compile(r'^[+-]\d{1,3}Hz$')


def validate_settings(locale: str, gender: str, rate: str, pitch: str, text: str) -> None:
    if locale not in VOICE_CATALOG or gender not in VOICE_CATALOG[locale]:
        raise ValueError('Choose a supported language and voice.')
    if not RATE_PATTERN.fullmatch(rate) or not -100 <= int(rate[:-1]) <= 100:
        raise ValueError('Speed must be from -100% to +100%, e.g. +10%.')
    if not PITCH_PATTERN.fullmatch(pitch) or not -100 <= int(pitch[:-2]) <= 100:
        raise ValueError('Pitch must be from -100Hz to +100Hz, e.g. +0Hz.')
    if not text.strip():
        raise ValueError('Enter a preview phrase.')


def preview_command(python: Path, locale: str, gender: str, rate: str,
                    pitch: str, text: str, strict: bool = False) -> list[str]:
    validate_settings(locale, gender, rate, pitch, text)
    cmd = [str(python), str(ROOT / 'scripts' / 'edge_voice_demo.py'),
           '--locale', locale, '--gender', gender,
           '--voice', VOICE_CATALOG[locale][gender], '--rate', rate,
           '--pitch', pitch, '--preview', '--preview-text', text]
    if strict:
        cmd.append('--strict-voice-settings')
    return cmd



def silero_preview_command(python: Path, locale: str, voice: str, text: str,
                           *, trusted: bool = False) -> list[str]:
    if locale not in SILERO_VOICES or voice not in SILERO_VOICES[locale]:
        raise ValueError('Unsupported Silero voice for the selected language.')
    if not text.strip():
        raise ValueError('Enter a preview phrase.')
    if not trusted:
        raise ValueError('Confirm that you trust the local PyTorch model before loading it.')
    return [str(python), str(ROOT / 'scripts' / 'silero_studio_preview.py'),
            '--locale', locale, '--voice', voice, '--text', text,
            '--model-path', str(Path(os.environ.get('STORY_SILERO_MODEL',
                r'C:\StoryStudioModels\v5_cis_base_nostress.pt' if sys.platform == 'win32'
                else str(ROOT / 'models' / 'silero' / 'v5_cis_base_nostress.pt')))),
            '--trust-local-model']

def preview_output_path(provider: str, locale: str, voice: str,
                        rate: str = '+0%', pitch: str = '+0Hz', text: str = '',
                        *, root: Path = ROOT) -> Path:
    """Determine the expected output without trusting subprocess console encoding.

    The path calculation must stay in sync with the CLI preview scripts.
    """
    if provider == 'silero_local':
        if voice not in SILERO_VOICES.get(locale, ()):
            raise ValueError('Unsupported Silero voice for the selected language.')
        return root / 'examples' / 'voice_previews' / f'silero-{locale}-{voice}.wav'
    if provider == 'edge':
        if voice not in VOICE_CATALOG.get(locale, {}):
            raise ValueError('Unsupported Edge voice for the selected language.')
        selected = VOICE_CATALOG[locale][voice]
        voice_folder = re.sub(r'[^a-zA-Z0-9_-]', '_', selected).lower()
        folder = root / 'examples' / f'narrated_{locale}' / voice_folder
        if rate != '+0%' or pitch != '+0Hz':
            settings_hash = hashlib.sha256(f'{rate}|{pitch}'.encode()).hexdigest()[:12]
            folder = folder / f'settings-{settings_hash}'
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]
        return folder / 'media' / f'preview-{text_hash}.mp3'
    raise ValueError(f'Unknown provider: {provider}')


def preview_file_signature(path: Path) -> tuple[int, int] | None:
    try:
        stat = path.stat()
        return stat.st_size, stat.st_mtime_ns
    except OSError:
        return None


def hardware_summary(profile: dict, advice: dict) -> str:
    cpu = profile.get('cpu_name') or 'Unknown CPU'
    ram = profile.get('ram_gib')
    memory = f'{ram} GiB RAM' if isinstance(ram, (int, float)) else 'RAM unknown'
    gpu = ', '.join(profile.get('gpu_names') or []) or 'GPU unknown'
    warning = ' | LOW RAM' if advice.get('low_memory_warning') else ''
    return f'{cpu} | {memory} | {gpu} | TTS: CPU{warning}'


def audio_duration_seconds(path: Path) -> float | None:
    if path.suffix.lower() != '.wav':
        return None
    try:
        with wave.open(str(path), 'rb') as wav:
            rate = wav.getframerate()
            return wav.getnframes() / rate if rate > 0 else None
    except (OSError, EOFError, wave.Error):
        return None


def synthesis_metrics(path: Path, elapsed_seconds: float) -> str:
    duration = audio_duration_seconds(path)
    if duration is None or duration <= 0:
        return f'Synthesis time: {elapsed_seconds:.1f}s (audio duration unavailable)'
    return (f'Synthesis time: {elapsed_seconds:.1f}s | Audio: {duration:.1f}s | '
            f'Real-time factor: {elapsed_seconds / duration:.2f}x')


def main() -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
    except ImportError as exc:
        raise SystemExit('Tkinter is unavailable in this Python installation.') from exc

    root = tk.Tk()
    root.title('Story Studio RU/UA — Voice Studio (Sprint 25.1)')
    root.geometry('880x730')
    root.minsize(650, 450)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(10, weight=1)
    provider = tk.StringVar(value='edge')
    trust_local = tk.BooleanVar(value=False)
    language = tk.StringVar(value='ru')
    gender = tk.StringVar(value='male')
    rate = tk.StringVar(value='+0%')
    pitch = tk.StringVar(value='+0Hz')
    strict = tk.BooleanVar(value=False)
    voice_label = tk.StringVar()
    voice = tk.StringVar()
    status = tk.StringVar(value='Ready')
    metrics_text = tk.StringVar(value='')
    hardware_text = tk.StringVar(value='Detecting hardware…')
    started_at: float | None = None
    events: queue.Queue[tuple[str, str]] = queue.Queue()
    busy = False
    last_preview: Path | None = None
    expected_preview: Path | None = None
    prior_signature: tuple[int, int] | None = None
    active_provider: str = ''

    def update_voice(*_args):
        if provider.get() == 'edge':
            options = ['male', 'female']
            voice_combo.configure(values=options)
            if voice.get() not in options:
                voice.set('male')
            voice_label.set(VOICE_CATALOG[language.get()][voice.get()])
            rate_entry.configure(state='normal')
            pitch_entry.configure(state='normal')
            strict_check.configure(state='normal')
        else:
            options = SILERO_VOICES[language.get()]
            voice_combo.configure(values=options)
            if voice.get() not in options:
                voice.set(options[0])
            voice_label.set('Offline Silero: ' + voice.get())
            rate_entry.configure(state='disabled')
            pitch_entry.configure(state='disabled')
            strict_check.configure(state='disabled')
        if not phrase.get('1.0', 'end').strip() or phrase.get('1.0', 'end').strip() in (
            'Это пример выбранного голоса.', 'Це приклад вибраного голосу.'):
            phrase.delete('1.0', 'end')
            phrase.insert('1.0', 'Это пример выбранного голоса.' if language.get() == 'ru' else 'Це приклад вибраного голосу.')

    def add_line(text: str):
        log.configure(state='normal')
        log.insert('end', text + '\n')
        log.see('end')
        log.configure(state='disabled')

    def hardware_worker():
        try:
            profile = probe()
            advice = recommend(profile)
            events.put(('hardware', hardware_summary(profile, advice)))
        except Exception as exc:
            events.put(('hardware', 'Hardware detection unavailable: ' + str(exc)))

    def worker(cmd: list[str]):
        try:
            child_env = os.environ.copy()
            child_env['PYTHONIOENCODING'] = 'utf-8'
            child_env['PYTHONUTF8'] = '1'
            proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace',
                                    bufsize=1, env=child_env)
            assert proc.stdout is not None
            for line in proc.stdout:
                events.put(('line', line.rstrip('\r\n')))
            code = proc.wait()
            events.put(('done', str(code)))
        except Exception as exc:
            events.put(('error', str(exc)))

    def start_preview():
        nonlocal busy, last_preview, started_at, expected_preview, prior_signature, active_provider
        if busy:
            return
        python = ROOT / '.venv' / 'Scripts' / 'python.exe' if sys.platform == 'win32' else ROOT / '.venv' / 'bin' / 'python'
        if not python.is_file():
            messagebox.showerror('Python missing', f'Project virtual environment not found:\n{python}')
            return
        try:
            active_provider = provider.get()
            preview_text = phrase.get('1.0', 'end').strip()
            if active_provider == 'edge':
                cmd = preview_command(python, language.get(), voice.get(), rate.get(), pitch.get(),
                                      preview_text, strict.get())
            else:
                cmd = silero_preview_command(python, language.get(), voice.get(),
                                             preview_text, trusted=trust_local.get())
            expected_preview = preview_output_path(active_provider, language.get(), voice.get(),
                                                   rate.get(), pitch.get(), preview_text)
            prior_signature = preview_file_signature(expected_preview)
        except ValueError as exc:
            messagebox.showerror('Invalid settings', str(exc))
            return
        busy = True
        last_preview = None
        metrics_text.set('')
        preview_button.configure(state='disabled')
        open_button.configure(state='disabled')
        status.set('Synthesizing…')
        started_at = time.monotonic()
        add_line('--- New preview ---')
        threading.Thread(target=worker, args=(cmd,), daemon=True).start()

    def open_preview():
        if last_preview is None or not last_preview.is_file():
            messagebox.showwarning('Preview', 'No verified preview path yet.')
            return
        import os
        if sys.platform == 'win32':
            os.startfile(str(last_preview))
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', str(last_preview)])
        else:
            subprocess.Popen(['xdg-open', str(last_preview)])

    def poll():
        nonlocal busy, last_preview, started_at
        try:
            while True:
                kind, value = events.get_nowait()
                if kind == 'hardware':
                    hardware_text.set(value)
                    add_line('Hardware: ' + value)
                elif kind == 'line':
                    # Console paths may contain mojibake on Windows. Log them,
                    # but never rely on the printed path to locate output.
                    add_line(value)
                elif kind in ('done', 'error'):
                    busy = False
                    preview_button.configure(state='normal')
                    signature = preview_file_signature(expected_preview) if expected_preview else None
                    valid_output = signature is not None and signature[0] > 1024
                    # Silero must write a new WAV. Edge may reuse its valid MP3 cache.
                    fresh = (active_provider == 'edge' or signature != prior_signature)
                    good = kind == 'done' and value == '0' and valid_output and fresh
                    if good:
                        last_preview = expected_preview
                        status.set('Preview ready')
                        if started_at is not None:
                            metrics = synthesis_metrics(last_preview, time.monotonic() - started_at)
                            metrics_text.set(metrics)
                            add_line(metrics)
                        open_button.configure(state='normal')
                    else:
                        last_preview = None
                        metrics_text.set('')
                        status.set('Preview failed — see log')
                        if kind == 'error':
                            add_line('ERROR: ' + value)
                        elif value != '0':
                            add_line('ERROR: synthesis exited with code ' + value)
                        else:
                            add_line('ERROR: Preview file missing, too small or unchanged: ' + str(expected_preview))
        except queue.Empty:
            pass
        root.after(150, poll)

    pad = {'padx': 10, 'pady': 6}
    ttk.Label(root, text='Provider').grid(row=0, column=0, sticky='w', **pad)
    ttk.Combobox(root, textvariable=provider, values=['edge', 'silero_local'], state='readonly', width=20).grid(row=0, column=1, sticky='w', **pad)
    ttk.Label(root, text='Language').grid(row=1, column=0, sticky='w', **pad)
    ttk.Combobox(root, textvariable=language, values=['ru', 'uk'], state='readonly', width=20).grid(row=1, column=1, sticky='w', **pad)
    ttk.Label(root, text='Voice').grid(row=2, column=0, sticky='w', **pad)
    voice_combo = ttk.Combobox(root, textvariable=voice, state='readonly', width=20)
    voice_combo.grid(row=2, column=1, sticky='w', **pad)
    ttk.Label(root, textvariable=voice_label).grid(row=3, column=1, sticky='w', **pad)
    ttk.Label(root, text='Speed (Edge only)').grid(row=4, column=0, sticky='w', **pad)
    rate_entry = ttk.Entry(root, textvariable=rate, width=20)
    rate_entry.grid(row=4, column=1, sticky='w', **pad)
    ttk.Label(root, text='Pitch (Edge only)').grid(row=5, column=0, sticky='w', **pad)
    pitch_entry = ttk.Entry(root, textvariable=pitch, width=20)
    pitch_entry.grid(row=5, column=1, sticky='w', **pad)
    ttk.Label(root, text='Preview text').grid(row=6, column=0, sticky='nw', **pad)
    phrase = tk.Text(root, height=3, wrap='word')
    phrase.grid(row=6, column=1, sticky='ew', **pad)
    strict_check = ttk.Checkbutton(root, text='Strict Edge settings', variable=strict)
    strict_check.grid(row=7, column=1, sticky='w', **pad)
    ttk.Checkbutton(root, text='I trust this local PyTorch model (Silero only)', variable=trust_local).grid(row=8, column=1, sticky='w', **pad)
    hardware_frame = ttk.Frame(root)
    hardware_frame.grid(row=9, column=0, columnspan=2, sticky='ew', **pad)
    ttk.Label(hardware_frame, textvariable=hardware_text, wraplength=690).pack(side='left', fill='x', expand=True)
    ttk.Button(hardware_frame, text='Refresh hardware', command=lambda: threading.Thread(target=hardware_worker, daemon=True).start()).pack(side='right', padx=4)
    log = tk.Text(root, height=12, state='disabled', wrap='word')
    log.grid(row=10, column=0, columnspan=2, sticky='nsew', **pad)
    buttons = ttk.Frame(root)
    buttons.grid(row=11, column=0, columnspan=2, sticky='ew', **pad)
    preview_button = ttk.Button(buttons, text='Generate preview', command=start_preview)
    preview_button.pack(side='left', padx=4)
    open_button = ttk.Button(buttons, text='Play audio', command=open_preview, state='disabled')
    open_button.pack(side='left', padx=4)
    ttk.Label(buttons, textvariable=status).pack(side='left', padx=12)
    ttk.Label(root, textvariable=metrics_text).grid(row=12, column=0, columnspan=2,
                                                    sticky='w', padx=14, pady=(0, 6))
    language.trace_add('write', update_voice)
    provider.trace_add('write', update_voice)
    voice.trace_add('write', update_voice)
    update_voice()
    root.after(150, poll)
    threading.Thread(target=hardware_worker, daemon=True).start()
    root.mainloop()


if __name__ == '__main__':
    main()
