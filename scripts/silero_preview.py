
"""Optional local Silero TTS preview for Story Studio RU/UA."""

import argparse
import array
import hashlib
import sys
import wave
from pathlib import Path


# Voice names confirmed by the local v5_cis_base_nostress model.
CIS_VOICES = [
    "bak_aigul",
    "ru_aigul",
    "tat_albina",
    "ru_albina",
    "erz_alexandr",
    "ru_alexandr",
    "bak_alfia",
    "ru_alfia",
    "bak_alfia2",
    "ru_alfia2",
    "bel_anatoliy",
    "udm_bogdan",
    "ru_bogdan",
    "bel_dmitriy",
    "ru_dmitriy",
    "chv_ekaterina",
    "ru_ekaterina",
    "kat_vika",
    "ru_vika",
    "aze_gamat",
    "ru_gamat",
    "ukr_igor",
    "ru_igor",
    "kjh_karina",
    "ru_karina",
    "xal_kejilgan",
    "ru_kejilgan",
    "xal_kermen",
    "ru_kermen",
    "bel_larisa",
    "tat_marat",
    "ru_marat",
    "bak_miyau",
    "ru_miyau",
    "kir_nurgul",
    "ru_nurgul",
    "mdf_oksana",
    "ru_oksana",
    "tgk_onaoy",
    "ru_onaoy",
    "bak_ramilia",
    "ru_ramilia",
    "tat_albina",
    "ru_albina",
    "ukr_roman",
    "ru_roman",
    "tgk_safarhuja",
    "ru_safarhuja",
    "uzb_saida",
    "ru_saida",
    "kjh_sibday",
    "ru_sibday",
    "hye_zara",
    "ru_zara",
    "kaz_zhadyra",
    "ru_zhadyra",
    "kaz_zhazira",
    "ru_zhazira",
    "sah_zinaida",
    "ru_zinaida",
    "ru_eduard",
    "kbd_eduard",
]

MODELS = {
    "v5_cis_base_nostress": {
        "ru": list(dict.fromkeys(CIS_VOICES)),
        "uk": ["ukr_igor", "ukr_roman"],
    },
    "v5_6_ru": {
        "ru": [
            "aidar",
            "baya",
            "kseniya",
            "xenia",
            "eugene",
        ],
    },
    "v4_ua": {
        "uk": [
            "mykyta",
            "random",
        ],
    },
}

LICENSE = {
    "v5_cis_base_nostress": "MIT",
    "v5_6_ru": "CC BY-NC 4.0",
    "v4_ua": "CC BY-NC 4.0",
}

# Hash of the previously inspected third-party model copy.
# Matching this hash does not establish official provenance.
EXPECTED_SHA256 = {
    "v5_cis_base_nostress": (
        "0405777e332906f0644e08a680f7cfdc2137ea864090079c1fdd30a43c1b8761"
    ),
}


def calculate_sha256(path):
    """Calculate SHA256 using Python 3.10-compatible APIs."""
    hasher = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            hasher.update(chunk)

    return hasher.hexdigest()


def save_wav(audio, output_path, sample_rate=24000):
    """Save mono audio as 16-bit PCM WAV."""

    if hasattr(audio, "detach"):
        values = audio.detach().cpu().flatten().tolist()
    else:
        values = list(audio)

    if not values:
        raise RuntimeError("Silero returned empty audio")

    pcm = array.array(
        "h",
        (
            max(
                -32768,
                min(32767, int(float(value) * 32767)),
            )
            for value in values
        ),
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_path = output_path.with_suffix(".tmp.wav")

    with wave.open(str(temp_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())

    temp_path.replace(output_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--list-voices",
        action="store_true",
    )

    parser.add_argument(
        "--model",
        choices=MODELS,
        default="v5_cis_base_nostress",
    )

    parser.add_argument(
        "--locale",
        choices=["ru", "uk"],
        default="ru",
    )

    parser.add_argument("--voice")

    parser.add_argument(
        "--text",
        default="Это тест локального голоса.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("silero-preview.wav"),
    )

    parser.add_argument(
        "--allow-noncommercial",
        action="store_true",
    )

    parser.add_argument(
        "--local-model",
        type=Path,
        help="Path to a local Silero .pt package",
    )

    parser.add_argument(
        "--trust-local-model",
        action="store_true",
        help="Explicitly permit loading a trusted local package",
    )

    args = parser.parse_args()

    if args.list_voices:
        for model_name, locales in MODELS.items():
            for locale, voices in locales.items():
                for voice in voices:
                    print(
                        f"{model_name}\t{locale}\t"
                        f"{voice}\t{LICENSE[model_name]}"
                    )
        return

    allowed_voices = MODELS[args.model].get(
        args.locale,
        [],
    )

    if args.voice not in allowed_voices:
        parser.error(
            "Voice is not in the selected model and language. "
            "Run --list-voices."
        )

    if LICENSE[args.model] != "MIT":
        if not args.allow_noncommercial:
            parser.error(
                "Noncommercial model: use "
                "--allow-noncommercial for testing only."
            )

    if not args.text.strip():
        parser.error("Text must not be empty.")

    if args.trust_local_model and not args.local_model:
        parser.error(
            "--trust-local-model requires --local-model"
        )

    if args.local_model:
        if not args.trust_local_model:
            parser.error(
                "Local packages may execute Python code. "
                "Use --trust-local-model only after "
                "verifying provenance."
            )

        if not args.local_model.is_file():
            parser.error(
                f"Local model not found: {args.local_model}"
            )

        if args.local_model.name != args.model + ".pt":
            parser.error(
                "Local model filename must match --model."
            )

    try:
        import torch
    except ImportError:
        parser.error(
            "PyTorch is not installed in this environment."
        )

    try:
        if args.local_model:
            print(
                f"Loading local Silero package: "
                f"{args.local_model}",
                flush=True,
            )

            digest = calculate_sha256(
                args.local_model
            )

            print(
                "Local model SHA256: " + digest,
                flush=True,
            )

            expected = EXPECTED_SHA256.get(
                args.model
            )

            if expected and digest.lower() != expected.lower():
                raise RuntimeError(
                    "Local model SHA256 differs from "
                    "the previously inspected copy. "
                    "Refusing to load."
                )

            print(
                "Importing PyTorch package...",
                flush=True,
            )

            # WARNING:
            # PackageImporter.load_pickle may execute code.
            # Load only packages from trusted sources.
            importer = torch.package.PackageImporter(
                str(args.local_model)
            )

            model = importer.load_pickle(
                "tts_models",
                "model",
                map_location="cpu",
            )

            print(
                "PyTorch package loaded.",
                flush=True,
            )

        else:
            print(
                "Loading Silero model "
                "(may download files)...",
                flush=True,
            )

            language = (
                "ru" if args.locale == "ru" else "ua"
            )

            model, _ = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_tts",
                language=language,
                speaker=args.model,
                trust_repo=True,
            )

        if isinstance(model, (tuple, list)):
            model = model[0]

        # Silero wrappers may not expose to() or eval().
        if hasattr(model, "to"):
            model.to("cpu")

        if hasattr(model, "eval"):
            model.eval()

        print(
            "Synthesizing audio...",
            flush=True,
        )

        audio = model.apply_tts(
            text=args.text,
            speaker=args.voice,
            sample_rate=24000,
        )

        save_wav(
            audio,
            args.output,
            sample_rate=24000,
        )

        print(
            "PREVIEW: " + str(args.output.resolve()),
            flush=True,
        )

    except Exception as exc:
        print(
            "ERROR: Silero synthesis failed: "
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
