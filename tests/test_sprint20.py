import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from voice_studio import VOICE_CATALOG, preview_command, validate_settings


def test_catalog():
    assert VOICE_CATALOG['ru']['male'] == 'ru-RU-DmitryNeural'
    assert VOICE_CATALOG['uk']['female'] == 'uk-UA-PolinaNeural'


def test_command_has_preview_and_voice():
    cmd = preview_command(Path('python.exe'), 'ru', 'male', '+10%', '+5Hz', 'Тест', True)
    assert '--preview' in cmd
    assert '--strict-voice-settings' in cmd
    assert cmd[cmd.index('--voice') + 1] == 'ru-RU-DmitryNeural'
    assert cmd[cmd.index('--preview-text') + 1] == 'Тест'


@pytest.mark.parametrize('rate,pitch', [('+101%', '+0Hz'), ('0%', '+0Hz'), ('+0%', '5Hz'), ('+0%', '+101Hz')])
def test_invalid_settings(rate, pitch):
    with pytest.raises(ValueError):
        validate_settings('ru', 'male', rate, pitch, 'Тест')


def test_empty_text():
    with pytest.raises(ValueError):
        validate_settings('uk', 'female', '+0%', '+0Hz', '  ')
