import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from edge_voice_demo import cache_key, resolve_voice, safe_voice_name

def test_cache_parameters_isolated():
    a=cache_key('ru-RU-DmitryNeural','hello')
    assert a != cache_key('ru-RU-DmitryNeural','hello','+10%')
    assert a != cache_key('ru-RU-DmitryNeural','hello','+0%','+5Hz')
    assert a != cache_key('ru-RU-SvetlanaNeural','hello')

def test_catalog_ru_ua():
    assert resolve_voice('ru',None,'male') == 'ru-RU-DmitryNeural'
    assert resolve_voice('uk',None,'female') == 'uk-UA-PolinaNeural'
    assert safe_voice_name('ru-RU-DmitryNeural') == 'ru-ru-dmitryneural'

def test_powershell_uses_project_python():
    source=(Path(__file__).resolve().parents[1]/'scripts/run_edge_demo.ps1').read_text()
    assert '.venv/Scripts/python.exe' in source
    assert '& $LocalPython @ArgsList' in source
