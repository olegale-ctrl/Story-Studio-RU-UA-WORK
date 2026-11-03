param(
    [ValidateSet('ru','uk')][string]$Locale = 'uk',
    [string]$VoiceName = '',
    [switch]$ListVoices,
    [switch]$ExportSrt,
    [ValidateRange(0,51)][int]$Crf = 22
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
try { Add-Type -AssemblyName System.Speech } catch { throw 'System.Speech unavailable. Use Windows PowerShell 5.1.' }
$Synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $Voices = @($Synth.GetInstalledVoices() | Where-Object { $_.Enabled })
    if ($ListVoices) {
        if ($Voices.Count -eq 0) { Write-Host 'No enabled SAPI voices found.' }
        foreach ($V in $Voices) { Write-Host ('{0} [{1}]' -f $V.VoiceInfo.Name,$V.VoiceInfo.Culture.Name) }
        exit 0
    }
    $Prefix = if ($Locale -eq 'uk') { 'uk' } else { 'ru' }
    $Selected = if ($VoiceName) {
        $Voices | Where-Object { $_.VoiceInfo.Name -eq $VoiceName -and $_.VoiceInfo.Culture.Name -like "$Prefix*" } | Select-Object -First 1
    } else {
        $Voices | Where-Object { $_.VoiceInfo.Culture.Name -like "$Prefix*" } | Select-Object -First 1
    }
    if (-not $Selected) {
        Write-Host "No $Locale SAPI voice available. Installed voices:"
        foreach ($V in $Voices) { Write-Host ('  {0} [{1}]' -f $V.VoiceInfo.Name,$V.VoiceInfo.Culture.Name) }
        throw 'Speech generation stopped; no cross-language substitution.'
    }
    Write-Host ('Selected voice: {0} [{1}]' -f $Selected.VoiceInfo.Name,$Selected.VoiceInfo.Culture.Name)
} finally { $Synth.Dispose() }
$ArgsVoice = @('-NoProfile','-ExecutionPolicy','Bypass','-File',(Join-Path $Root 'scripts\make_voice_demo.ps1'),'-Locale',$Locale,'-VoiceName',$Selected.VoiceInfo.Name)
& powershell.exe @ArgsVoice
if ($LASTEXITCODE -ne 0) { throw 'Voice demo generation failed.' }
$Project = ".\examples
arrated_$Locale
arrated_project.json"
$Media = ".\examples
arrated_$Locale\media"
& python .\scripts\inspect_voice_demo.py --locale $Locale
if ($LASTEXITCODE -ne 0) { throw 'Narrated project inspection failed.' }
& python -m core.cli check $Project
if ($LASTEXITCODE -ne 0) { throw 'Project validation failed.' }
$Video = ".
arrated-$Locale-s15.mp4"
if (Test-Path $Video) { throw "Output already exists: $Video. Rename/move the old file first." }
$RenderArgs = @('-m','core.cli','render-mp4',$Project,'--media-root',$Media,'--output',$Video,'--burn-subtitles','--width','1920','--height','1080','--crf',"$Crf")
if ($ExportSrt) { $RenderArgs += '--export-srt' }
& python @RenderArgs
if ($LASTEXITCODE -ne 0) { throw 'Video render failed.' }
Write-Host "SUCCESS: $Video"
Write-Host 'Note: external SRT may be displayed twice by some players when ExportSrt is used.'
