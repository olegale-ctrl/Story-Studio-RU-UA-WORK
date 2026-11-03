"""CPU-first, privacy-preserving hardware capability probe for Story Studio.

No external packages, network calls, or hardware benchmarks required.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def _run(command: list[str], timeout: int = 6) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=timeout,
                                check=False)
        return result.stdout.strip() if result.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired):
        return ''


def _windows_info() -> dict:
    if sys.platform != 'win32':
        return {}
    ps = shutil.which('powershell.exe') or shutil.which('powershell')
    if not ps:
        return {}
    script = (
        "$ErrorActionPreference='Stop';"
        "$c=Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfLogicalProcessors;"
        "$m=Get-CimInstance Win32_ComputerSystem;"
        "$g=@(Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name);"
        "@{cpu=$c.Name;logical_processors=$c.NumberOfLogicalProcessors;"
        "ram_bytes=$m.TotalPhysicalMemory;gpu_names=$g} | ConvertTo-Json -Compress"
    )
    raw = _run([ps, '-NoProfile', '-NonInteractive', '-Command', script])
    try:
        return json.loads(raw) if raw else {}
    except (ValueError, TypeError):
        return {}


def probe() -> dict:
    win = _windows_info()
    cpu = str(win.get('cpu') or platform.processor() or platform.machine() or 'unknown')
    logical = win.get('logical_processors') or os.cpu_count()
    ram_bytes = win.get('ram_bytes')
    try:
        ram_gib = round(int(ram_bytes) / 1024**3, 1) if ram_bytes else None
    except (TypeError, ValueError):
        ram_gib = None
    gpu = win.get('gpu_names') or []
    if isinstance(gpu, str):
        gpu = [gpu]
    gpu = [str(x) for x in gpu if x]
    return {
        'schema_version': 1,
        'os': platform.system(),
        'architecture': platform.machine(),
        'cpu_name': cpu,
        'logical_processors': logical,
        'ram_gib': ram_gib,
        'gpu_names': gpu,
        'cpu_available': True,
        # Presence of a graphics adapter does not prove TTS backend support.
        'gpu_tts_acceleration_verified': False,
        'diagnostics_complete': bool(cpu != 'unknown' and ram_gib is not None),
    }


def recommend(profile: dict) -> dict:
    ram = profile.get('ram_gib')
    return {
        'default_device': 'cpu',
        'edge_tts': {'enabled': True, 'requires_internet': True},
        'silero_local': {'enabled': True, 'device': 'cpu', 'requires_internet': False},
        'experimental_large_models': {
            'auto_enable': False,
            'reason': 'Requires explicit compatibility and performance test',
        },
        'low_memory_warning': bool(ram is not None and ram < 4),
        'gpu_acceleration': 'disabled_until_backend_verified',
    }


def main() -> None:
    profile = probe()
    print(json.dumps({'hardware': profile, 'recommendations': recommend(profile)},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
