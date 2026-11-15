"""Run the single registered D1 synthetic RU/UK test scenario."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import wave

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import first_video
from story_intelligence.codec_v1 import canonical_si_json
from story_intelligence.decision_projection_v1 import project_evaluation
from story_intelligence.evaluate_v1 import evaluate_si


LOCALES = ("ru", "uk")
SCENARIO = "si-product-02.2.1-d1"
PURPOSE = "SYNTHETIC_TEST_ONLY"
VERSION = "SyntheticRenderPermitV1"
REGISTERED_DIGEST = '469e3db84ee2d97ed76460a684d2cb4b5977e2b493084a0d4bfc0bdb373a71a8'
FIELDS = {"scenario", "purpose", "evaluation_inputs", "plans", "permit"}
WIDTH, HEIGHT = 640, 360


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256(canonical_si_json(value)).hexdigest()


def synthetic_wav():
    buffer = BytesIO()
    with wave.open(buffer, "wb") as stream:
        stream.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
        stream.writeframes(bytes(48000))
    return buffer.getvalue()


def write_wav(path):
    path.write_bytes(synthetic_wav())


def binding(topic, evaluation, cards, audio):
    return digest({
        "version": VERSION,
        "scenario": topic["scenario"],
        "purpose": topic["purpose"],
        "inputs": topic["evaluation_inputs"],
        "evaluation": evaluation,
        "cards": cards,
        "plans": topic["plans"],
        "wav_sha256": audio,
    })


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inspect_video(path):
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name:format=duration", "-of", "json", str(path)],
        capture_output=True, check=True, timeout=30,
    )
    info = json.loads(probe.stdout)
    streams = {value["codec_type"]: value["codec_name"] for value in info["streams"]}
    require(len(info["streams"]) == 2 and streams == {"video": "h264", "audio": "aac"},
            "Expected H.264 and AAC")
    require(abs(float(info["format"]["duration"]) - 1.4) <= 0.08,
            "Unexpected video duration")
    # The synthetic gradient has no near-white pixels. During the first
    # subtitle interval the rendered white subtitle is the only bright region.
    frame = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", "0.4", "-i", str(path), "-frames:v", "1",
         "-vf", "format=gray", "-f", "rawvideo", "-"],
        capture_output=True, check=True, timeout=30,
    ).stdout
    require(len(frame) == WIDTH * HEIGHT and
            sum(pixel >= 200 for pixel in frame[HEIGHT // 2 * WIDTH:]) >= 20,
            "Expected visible burned subtitle")
    return info


def run(topic_path, output):
    require(not output.exists(), "Output directory already exists")
    with topic_path.open("rb") as source:
        raw = source.read(1_000_001)
    require(len(raw) <= 1_000_000, "Topic exceeds size limit")
    topic = json.loads(raw, object_pairs_hook=pairs)
    canonical_si_json(topic)
    require(type(topic) is dict and set(topic) == FIELDS, "Unexpected topic fields")
    require(topic["scenario"] == SCENARIO and topic["purpose"] == PURPOSE,
            "This scenario is restricted to synthetic testing")
    permit = topic["permit"]
    require(permit == {"version": VERSION, "purpose": PURPOSE, "digest": REGISTERED_DIGEST},
            "Missing or unregistered synthetic render permit")
    plans = topic["plans"]
    require(type(plans) is dict and set(plans) == set(LOCALES), "Expected RU and UK plans")
    for locale, plan in plans.items():
        require(type(plan) is dict and set(plan) == {"locale", "title", "scenes"}
                and plan["locale"] == locale and type(plan["title"]) is str
                and type(plan["scenes"]) is list and len(plan["scenes"]) == 1
                and type(plan["scenes"][0]) is dict and set(plan["scenes"][0]) == {"text"},
                "Unexpected scene plan or external material")
        content = plan["scenes"][0]["text"]
        require(type(content) is str and 0 < len(content.strip()) and len(content) <= 2000,
                "Invalid scene text")
    inputs = topic["evaluation_inputs"]
    require(type(inputs) is dict, "Expected evaluator arguments")
    evaluation = evaluate_si(**inputs)
    require(evaluation["status"] == "OK" and
            evaluation["eligibility"]["state"] == "ELIGIBLE_FOR_CREATIVE",
            "Evaluation is not eligible for this synthetic scenario")
    cards = {locale: project_evaluation(inputs, evaluation, locale) for locale in LOCALES}
    require(all(card["availability"] == "DISPLAYABLE" for card in cards.values()),
            "Projection unavailable")

    output = output.absolute()
    require(output.parent.is_dir(), "Output parent directory must exist")
    with TemporaryDirectory(prefix=".d1-", dir=output.parent) as temporary:
        staging = Path(temporary)
        publish = staging / "result"
        publish.mkdir()
        audio = {}
        for locale in LOCALES:
            directory = staging / f"wav-{locale}"
            directory.mkdir()
            path = directory / "voice1.wav"
            write_wav(path)
            actual = path.read_bytes()
            require(actual == synthetic_wav(), "Unexpected synthetic WAV bytes")
            audio[locale] = {"voice1.wav": sha256(actual).hexdigest()}

        require(binding(topic, evaluation, cards, audio) == REGISTERED_DIGEST,
                "Synthetic permit binding mismatch")
        for locale in LOCALES:
            path = publish / f"plan-{locale}.json"
            write_json(path, plans[locale])
            first_video.read_plan(path)

        media = {}
        for locale in LOCALES:
            _, video = first_video.build(
                publish / f"plan-{locale}.json", publish / locale,
                audio_dir=staging / f"wav-{locale}", width=WIDTH, height=HEIGHT,
            )
            media[locale] = inspect_video(video)
        write_json(publish / "evaluation.json", evaluation)
        write_json(publish / "private-cards.json", cards)
        write_json(publish / "manifest.json", {
            "purpose": PURPOSE, "scenario": SCENARIO, "permit": permit,
            "wav_sha256": audio, "ffprobe": media,
            "videos": {locale: f"{locale}/first-video.mp4" for locale in LOCALES},
            "subtitles": "burned; verified by frame brightness on synthetic gradient",
        })
        require(not output.exists(), "Output directory already exists")
        publish.rename(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.topic, args.output_dir)
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as error:
        print(f"Synthetic render rejected: {type(error).__name__}", file=sys.stderr)
        return 2
    print("Synthetic render complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
