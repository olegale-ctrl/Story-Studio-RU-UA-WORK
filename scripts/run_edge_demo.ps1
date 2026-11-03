param(
    [ValidateSet('uk','ru')][string]$Locale='uk',
    [ValidateSet('female','male')][string]$Gender='female',
    [string]$Voice='',
    [switch]$ListVoices,
    [switch]$NoRender,
    [switch]$ExportSrt,
    [string]$Rate='+0%',
    [string]$Pitch='+0Hz',
    [switch]$Preview,
    [switch]$StrictVoiceSettings,
    [string]$PreviewText=''
)
$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$LocalPython=Join-Path $Root '.venv/Scripts/python.exe'
if (-not (Test-Path $LocalPython)) { throw 'Project Python .venv not found. Create it with: py -3.10 -m venv .venv' }
$ArgsList=@('scripts/edge_voice_demo.py','--locale',$Locale,'--gender',$Gender,'--rate',$Rate,'--pitch',$Pitch)
if ($Voice) { $ArgsList+=@('--voice',$Voice) }
if ($ListVoices) { $ArgsList+='--list-voices' }
if ($NoRender) { $ArgsList+='--no-render' }
if ($ExportSrt) { $ArgsList+='--export-srt' }
if ($Preview) { $ArgsList+='--preview' }
if ($StrictVoiceSettings) { $ArgsList+='--strict-voice-settings' }
if ($PreviewText) { $ArgsList+=@('--preview-text',$PreviewText) }
& $LocalPython @ArgsList
if ($LASTEXITCODE -ne 0) { throw 'Edge voice demo failed. See Python error above.' }
