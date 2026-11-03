param(
    [ValidateSet('ru','uk')][string]$Locale = 'uk',
    [string]$VoiceName = ''
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
try { Add-Type -AssemblyName System.Speech } catch { throw 'System.Speech is unavailable. Run with Windows PowerShell 5.1.' }
$Synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$Voices = @($Synth.GetInstalledVoices() | Where-Object { $_.Enabled })
$Prefix = if ($Locale -eq 'uk') { 'uk' } else { 'ru' }
if ($VoiceName) {
    $Voice = $Voices | Where-Object { $_.VoiceInfo.Name -eq $VoiceName } | Select-Object -First 1
} else {
    $Voice = $Voices | Where-Object { $_.VoiceInfo.Culture.Name -like "$Prefix*" } | Select-Object -First 1
}
if (-not $Voice) {
    Write-Host 'Installed voices:'
    $Voices | ForEach-Object { Write-Host ('  ' + $_.VoiceInfo.Name + ' [' + $_.VoiceInfo.Culture.Name + ']') }
    throw "No suitable $Locale voice. Install a Windows speech voice for this language, or specify -VoiceName. No other-language voice is substituted."
}
$Synth.SelectVoice($Voice.VoiceInfo.Name)
$Texts = if ($Locale -eq 'uk') { @(
    'Вітаємо у Story Studio. Тут починається ваша історія.',
    'Додавайте зображення, озвучення та субтитри.',
    'Створюйте відео українською або російською мовою.'
) } else { @(
    'Добро пожаловать в Story Studio. Здесь начинается ваша история.',
    'Добавляйте изображения, озвучивание и субтитры.',
    'Создавайте видео на русском или украинском языке.'
) }
$Dir = Join-Path $Root "examples\narrated_$Locale\media"
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
try {
    for ($i=0; $i -lt $Texts.Count; $i++) {
        $Path = Join-Path $Dir ('voice' + ($i+1) + '.wav')
        $Synth.SetOutputToWaveFile($Path)
        try { $Synth.Speak($Texts[$i]) } finally { $Synth.SetOutputToNull() }
        Write-Host "Voice created: $Path"
    }
} finally { $Synth.Dispose() }
python scripts/build_narrated_demo.py --locale $Locale --output-dir "examples/narrated_$Locale"
if ($LASTEXITCODE -ne 0) { throw 'Project generation failed' }
Write-Host 'Next: python -m core.cli render-mp4 ... (see docs/SPRINT14_WINDOWS.md)'
