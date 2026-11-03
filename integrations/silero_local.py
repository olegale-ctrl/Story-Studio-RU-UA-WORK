"""Optional local Silero adapter. Does not download or bundle model weights."""
from __future__ import annotations

import array
import hashlib
import wave
from pathlib import Path

MODEL_NAME = 'v5_cis_base_nostress'
KNOWN_SHA256 = '0405777e332906f0644e08a680f7cfdc2137ea864090079c1fdd30a43c1b8761'
VOICES = {'ru': ('ru_dmitriy', 'ru_igor', 'ru_roman'), 'uk': ('ukr_igor', 'ukr_roman')}


class SileroLocalProvider:
    """Small adapter for a locally installed Silero PyTorch package."""

    provider_id = 'silero_local'

    def __init__(self, model_path: str | Path, *, trusted: bool = False):
        self.model_path = Path(model_path)
        self.trusted = trusted
        self._model = None
        if not self.trusted:
            raise ValueError('Loading a PyTorch package requires explicit trusted=True')
        if not self.model_path.is_file():
            raise FileNotFoundError(self.model_path)
        if self.model_path.name != MODEL_NAME + '.pt':
            raise ValueError('Unexpected model filename')
        if not str(self.model_path.resolve()).isascii() and __import__('os').name == 'nt':
            raise ValueError('Silero model path must be ASCII-only on this Windows/PyTorch setup. Use C:\\StoryStudioModels\\v5_cis_base_nostress.pt')
        digest = hashlib.sha256(self.model_path.read_bytes()).hexdigest()
        if digest != KNOWN_SHA256:
            raise ValueError('Model SHA256 does not match the previously tested copy')

    @staticmethod
    def voices(locale: str) -> tuple[str, ...]:
        return VOICES.get(locale, ())

    def _load(self):
        if self._model is None:
            import torch
            importer = torch.package.PackageImporter(str(self.model_path))
            self._model = importer.load_pickle('tts_models', 'model', map_location='cpu')
            if hasattr(self._model, 'eval'):
                self._model.eval()
        return self._model

    def synthesize(self, *, text: str, locale: str, voice: str, output: str | Path) -> Path:
        if not text.strip():
            raise ValueError('Text cannot be empty')
        if voice not in self.voices(locale):
            raise ValueError(f'Unsupported voice {voice!r} for locale {locale!r}')
        result = self._load().apply_tts(text=text, speaker=voice, sample_rate=24000)
        if hasattr(result, 'detach'):
            samples = result.detach().cpu().flatten().tolist()
        else:
            samples = list(result)
        if not samples:
            raise RuntimeError('Silero returned empty audio')
        pcm = array.array('h', (max(-32768, min(32767, int(float(x) * 32767))) for x in samples))
        target = Path(output)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.tmp.wav')
        try:
            with wave.open(str(temporary), 'wb') as stream:
                stream.setnchannels(1)
                stream.setsampwidth(2)
                stream.setframerate(24000)
                stream.writeframes(pcm.tobytes())
            temporary.replace(target)
        finally:
            if temporary.exists():
                temporary.unlink()
        return target
