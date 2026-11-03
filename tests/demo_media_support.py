"""Generate portable test-only media in a temporary directory (no bundled binaries)."""
from __future__ import annotations
import wave
from pathlib import Path


def create_demo_media(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    width, height = 32, 18
    for name, color in (('scene1.ppm', (220, 40, 40)),
                        ('scene2.ppm', (40, 160, 80)),
                        ('scene3.ppm', (50, 70, 230))):
        with (root / name).open('wb') as file:
            file.write(f'P6\n{width} {height}\n255\n'.encode('ascii'))
            file.write(bytes(color) * width * height)
    with wave.open(str(root / 'music.wav'), 'wb') as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(24000)
        stream.writeframes(b'\x00\x00' * (24000 * 4))
    return root
