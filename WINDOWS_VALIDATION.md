# Windows Validation Plan for Sprint 26 first_video.py

## Prerequisites for Windows Validation

### 1. Environment Setup
- Windows 10/11 (primary target)
- Python 3.13 installed
- Virtual environment `.venv` activated
- FFmpeg binary available (user-managed, not redistributed)
- Silero model at `C:\StoryStudioModels\v5_cis_base_nostress.pt`

### 2. Required Files
- `scripts/first_video.py` - main pipeline script
- `examples/first_video_plan_uk.json` - Ukrainian scene plan
- `examples/first_video_plan_ru.json` - Russian scene plan
- `core/project_schema.py` - project validation
- `core/mp4_render.py` - FFmpeg rendering
- `integrations/silero_local.py` - Silero TTS adapter
- `core/media_paths.py` - media path validation
- `core/subtitles.py` - SRT export

### 3. Directory Structure
```
Story-Studio-RU-UA/
├── .venv/                    # Virtual environment
├── scripts/
│   └── first_video.py
├── examples/
│   ├── first_video_plan_uk.json
│   └── first_video_plan_ru.json
├── core/
├── integrations/
├── tools/
│   └── ffmpeg/               # User-place FFmpeg binary
│       └── bin/ffmpeg.exe
├── output/                   # Will be created by validation
└── models/                   # Model weights (user-provided)
    └── v5_cis_base_nostress.pt
```

## Validation Steps

### Step 1: Verify Python Environment
```powershell
# Check Python version
python --version
# Expected: Python 3.13.x

# Verify venv is active
.\.venv\Scripts\python.exe --version

# Check sys.path includes project root
.\.venv\Scripts\python.exe -c "import sys; print([p for p in sys.path if 'Story-Studio' in p])"
```

### Step 2: Verify FFmpeg Availability
```powershell
# Check local FFmpeg (preferred)
.\.venv\Scripts\python.exe -c "from core.mp4_render import find_ffmpeg; print('FFmpeg:', find_ffmpeg())"

# Or check manually
Get-ChildItem -Path .\tools\ffmpeg\bin\ffmpeg.exe -ErrorAction SilentlyContinue
# Or add to PATH and check
ffmpeg -version
```

### Step 3: Verify Silero Model
```powershell
# Check model exists and is accessible
Test-Path -Path "C:\StoryStudioModels\v5_cis_base_nostress.pt"
# Expected: True

# Check model filename matches expected
(Get-Item -Path "C:\StoryStudioModels\v5_cis_base_nostress.pt").Name
# Expected: v5_cis_base_nostress.pt
```

### Step 4: Verify Voice Availability
For Ukrainian:
```powershell
# List available Ukrainian voices from Silero
.\.venv\Scripts\python.exe -c "
from integrations.silero_local import SileroLocalProvider
provider = SileroLocalProvider(r'C:\StoryStudioModels\v5_cis_base_nostress.pt', trusted=True)
voices = provider.voices('uk')
print('Ukrainian voices:', voices)
"
# Expected: ('ukr_igor', 'ukr_roman')
```

For Russian:
```powershell
.\.venv\Scripts\python.exe -c "
from integrations.silero_local import SileroLocalProvider
provider = SileroLocalProvider(r'C:\StoryStudioModels\v5_cis_base_nostress.pt', trusted=True)
voices = provider.voices('ru')
print('Russian voices:', voices)
"
# Expected: ('ru_dmitriy', 'ru_igor', 'ru_roman')
```

### Step 5: Run the Full Pipeline

#### Ukrainian Version:
```powershell
.\.venv\Scripts\python.exe .\scripts\first_video.py `
  --plan .\examples\first_video_plan_uk.json `
  --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt `
  --voice ukr_igor `
  --output-dir .\output\first-video-uk
```

#### Russian Version:
```powershell
.\.venv\Scripts\python.exe .\scripts\first_video.py `
  --plan .\examples\first_video_plan_ru.json `
  --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt `
  --voice ru_igor `
  --output-dir .\output\first-video-ru
```

## Expected Output

### Console Output
```
RENDER: {'video': 'output/first-video-uk/first-video.mp4', 'subtitles': [], 'duration_ms': 11250, 'clips': 3, 'burned_subtitles': True, 'crf': 22, 'width': 1280, 'height': 720}
PROJECT: output/first-video-uk/project.json
VIDEO: output/first-video-uk/first-video.mp4
```

### Generated Files (in output\first-video-uk\)
```
project.json          # Validated v3 project schema
first-video.mp4       # Final MP4 with burned subtitles
media/
│   ├── voice1.wav    # Synthesized audio
│   ├── voice2.wav
│   ├── voice3.wav
│   ├── frame1.ppm    # Generated gradient frame
│   ├── frame2.ppm
│   └── frame3.ppm
```

### Verification Checklist

#### MP4 Verification (in VLC or similar):
- [ ] Audible Ukrainian/Russian speech (correct language)
- [ ] Correct clip order and timing (scenes appear in order)
- [ ] Subtitle text matches scene text
- [ ] Subtitle timing is correct (appears/disappears at correct moments)
- [ ] No subtitle shadows/filename overlays (clean appearance)
- [ ] Correct image aspect ratio (1280x720 or specified dimensions)
- [ ] Video plays through without errors

#### Project JSON Verification:
```powershell
.\.venv\Scripts\python.exe -m core.cli check .\output\first-video-uk\project.json
# Expected: OK: schema v3, locale=uk, clips=3
# Or for Russian: locale=ru
```

#### Test Suite:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
# Expected: 106 tests passed (Linux) or relevant tests pass (Windows)
```

## Troubleshooting Common Issues

### Issue 1: FFmpeg not found
**Symptom**: `ValueError: FFmpeg not found: place it at tools/ffmpeg/bin/ffmpeg.exe or add to PATH`
**Solution**: 
- Place `ffmpeg.exe` at `tools/ffmpeg/bin/ffmpeg.exe`
- Or add FFmpeg to system PATH
- Or specify explicit path: `--ffmpeg C:\path\to\ffmpeg.exe`

### Issue 2: Silero model not found or wrong SHA256
**Symptom**: `FileNotFoundError` or `ValueError: Model SHA256 does not match`
**Solution**:
- Ensure model exists at `C:\StoryStudioModels\v5_cis_base_nostress.pt`
- Verify the file is not corrupted
- Use the exact model name: `v5_cis_base_nostress.pt`

### Issue 3: Unicode console path issues
**Symptom**: `ValueError: Silero model path must be ASCII-only on this Windows/PyTorch setup`
**Solution**:
- Use ASCII-only path: `C:\StoryStudioModels\v5_cis_base_nostress.pt`
- Avoid non-ASCII characters in paths
- Use raw strings in PowerShell: `r'C:\StoryStudioModels\...'`

### Issue 4: Output directory already exists
**Symptom**: `FileExistsError: Output directory already exists`
**Solution**:
- Use a different output directory name
- Remove existing output directory: `Remove-Item -Recurse -Force .\output\first-video-uk`
- Or use `--no-render` flag to skip video rendering

### Issue 5: Voice not supported for locale
**Symptom**: `ValueError: Unsupported voice ukr_igor for locale uk` (or similar)
**Solution**:
- Verify voice is in the supported list for the locale
- Ukrainian: `ukr_igor`, `ukr_roman`
- Russian: `ru_dmitriy`, `ru_igor`, `ru_roman`
- Check Silero version compatibility

### Issue 6: Audio duration issues
**Symptom**: Subtitle timing incorrect, video too short/long
**Solution**:
- Ensure WAV files have correct sample rate (24000 Hz)
- Check scene text length is reasonable (< 2000 chars)
- Verify frame duration calculation: `scene_ms = ((audio_ms + 400 + FRAME_MS - 1) // FRAME_MS) * FRAME_MS`

## Success Criteria for Windows Validation

**Pass conditions (all must be met):**
1. `first_video.py` runs without errors on both UK and RU plans
2. Output MP4 plays with audible speech in correct language
3. Subtitles are burned into video with correct text and timing
4. Images/frames are displayed correctly with proper aspect ratio
5. `python -m unittest discover -s tests -v` passes relevant tests
6. `python -m core.cli check` validates generated project.json
7. No crashes related to Unicode paths, FFmpeg, or Silero model loading

**Fail conditions (any one stops validation):**
1. Script crashes before generating output
2. FFmpeg fails during MP4 rendering
3. Silero model loading fails
4. Output MP4 has no audio or corrupted audio
5. Subtitles are missing, wrong text, or wrong timing
6. Output directory not created or permissions error

## Next Steps After Successful Validation

1. Document the successful Windows workflow in `CLI_WINDOWS.md`
2. Add Windows-specific integration tests to `tests/`
3. Update `ROADMAP_STATUS.md` with validation results
4. Consider adding the validation as part of CI pipeline
5. Prepare user guide for Windows users