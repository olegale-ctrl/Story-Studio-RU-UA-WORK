"""CLI bridge from Voice Studio to the isolated local Silero provider."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from integrations.silero_local import SileroLocalProvider


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--locale', choices=('ru', 'uk'), required=True)
    parser.add_argument('--voice', required=True)
    parser.add_argument('--text', required=True)
    parser.add_argument('--model-path', type=Path, required=True)
    parser.add_argument('--trust-local-model', action='store_true')
    args = parser.parse_args()
    if not args.trust_local_model:
        parser.error('Explicit --trust-local-model is required for local PyTorch packages')
    provider = SileroLocalProvider(args.model_path, trusted=True)
    output = ROOT / 'examples' / 'voice_previews' / ('silero-' + args.locale + '-' + args.voice + '.wav')
    provider.synthesize(text=args.text, locale=args.locale, voice=args.voice, output=output)
    print('PREVIEW: ' + str(output.resolve()), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
