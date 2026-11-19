"""Prepare an offline intent on stdout. Dispatcher submission is not available."""
import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.topic_to_film import initial_readiness, prepare_intent
from core.topic_to_film_gates import read_json, read_local, run_gates


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--topic")
    source.add_argument("--script", type=Path)
    source.add_argument("--plan", type=Path)
    parser.add_argument("--materials", type=Path, help="Proposed declared input map JSON; no execution")
    parser.add_argument("--mode", choices=("draft", "production"), default="draft")
    parser.add_argument("--fallback", choices=("none", "equivalent", "degraded", "placeholder"), default="none")
    parser.add_argument("--authorize-render", action="store_true", help="Intent only; never an authorization")
    parser.add_argument("--declare-facts-reviewed", action="store_true")
    parser.add_argument("--declare-rights-cleared", action="store_true")
    parser.add_argument("--wait", type=int, choices=range(1, 301), metavar="1..300", help="Requires approved observation API; currently blocked")
    args = parser.parse_args(argv)
    try:
        intent = prepare_intent(topic=args.topic,
            script=read_local(args.script, 100_000).decode("utf-8") if args.script else None,
            plan=read_json(args.plan) if args.plan else None,
            materials=read_json(args.materials) if args.materials else None,
            mode=args.mode, fallback=args.fallback, authorize_render=args.authorize_render,
            declare_facts_reviewed=args.declare_facts_reviewed,
            declare_rights_cleared=args.declare_rights_cleared)
        result = {"intent": intent, "readiness": initial_readiness(intent),
                  "gates": run_gates(intent["route"], plan_path=args.plan),
                  "wait_status": "BLOCKED_JOBSTORE_CONTRACT" if args.wait else "NOT_REQUESTED"}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))
        return 3  # explicit blocked, never accepted/completed
    except (ValueError, OSError, TypeError, RecursionError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
