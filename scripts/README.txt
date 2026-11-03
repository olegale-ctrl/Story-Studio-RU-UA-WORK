Silero local model patch for Story Studio RU/UA

Replace scripts/silero_preview.py with the provided file. Back up the old one.
The model is NOT included. This patch has only been syntax-checked, not tested with actual model weights.

Run in PowerShell from the project root:
.\.venv\Scripts\python.exe .\scripts\silero_preview.py --model v5_cis_base_nostress --locale ru --voice ru_bel_dmitriy --local-model .\models\silero\v5_cis_base_nostress.pt --trust-local-model --text "Привет! Это проверка локального синтеза речи." --output silero-test.wav

WARNING: --trust-local-model allows deserialization of a .pt file, which can execute code. The downloaded checkpoint's provenance has not been independently authenticated. Run only if you accept this risk. For commercial distribution, independently validate model provenance and license.
