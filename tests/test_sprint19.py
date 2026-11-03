import json
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import edge_voice_demo as demo


def test_fallback_and_cache(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(demo.time, 'sleep', lambda _: None)
    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        pitch = cmd[cmd.index('--pitch') + 1]
        if pitch == '+0Hz':
            Path(cmd[cmd.index('--write-media') + 1]).write_bytes(b'a' * 2000)
            return SimpleNamespace(returncode=0)
        return SimpleNamespace(returncode=1)
    monkeypatch.setattr(demo.subprocess, 'run', fake_run)
    monkeypatch.setattr(demo, 'valid_audio', lambda p, _: p.exists() and p.stat().st_size > 1024)
    target = tmp_path / 'voice.mp3'
    demo.synthesize('ru-RU-DmitryNeural', 'hello', target, attempts=2, rate='+10%', pitch='+5Hz')
    assert len(calls) == 3
    data = json.loads(target.with_suffix('.cache.json').read_text())
    assert data['fallback'] is True
    assert data['actual_rate'] == '+10%' and data['actual_pitch'] == '+0Hz'
    demo.synthesize('ru-RU-DmitryNeural', 'hello', target, attempts=2, rate='+10%', pitch='+5Hz')
    assert len(calls) == 3


def test_strict_mode_does_not_fallback(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(demo.time, 'sleep', lambda _: None)
    def fail(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=1)
    monkeypatch.setattr(demo.subprocess, 'run', fail)
    try:
        demo.synthesize('ru-RU-DmitryNeural', 'hello', tmp_path/'v.mp3',
                        attempts=2, pitch='+5Hz', allow_fallback=False)
        assert False, 'should fail'
    except RuntimeError:
        pass
    assert len(calls) == 2
    assert not (tmp_path/'v.cache.json').exists()


def test_invalid_audio_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(demo.subprocess, 'run', lambda *a, **kw: SimpleNamespace(returncode=0, stdout=''))
    p = tmp_path/'bad.mp3'
    p.write_bytes(b'')
    assert not demo.valid_audio(p)
