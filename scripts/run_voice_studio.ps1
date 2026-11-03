$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Python=Join-Path $Root '.venv/Scripts/python.exe'
if (-not (Test-Path $Python)) { throw 'Project .venv Python not found. Run: py -3.10 -m venv .venv' }
& $Python (Join-Path $Root 'scripts/voice_studio.py')
if ($LASTEXITCODE -ne 0) { throw 'Voice Studio failed. See Python output above.' }
