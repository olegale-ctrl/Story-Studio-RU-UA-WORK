"""Developer-only synthetic Dispatcher demonstration using the existing test lab.

Run from a checkout with its test dependencies installed. Each case uses one
in-memory job. Printed records are diagnostics, without a persistent wire format.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))
# The existing fake store lives in the test harness and depends on pytest.
sys.path.insert(0, str(ROOT / "tests"))

from core.topic_to_film_v1_1 import prepare_intent
from experimental_mvp.offline_execution.observer import observe
from test_offline_generation_job_controller import Lab


def snapshot(lab, job_id):
    return observe(lab.namespace, lab.store, lab.authority, job_id,
                   lab.clock, lab.token["clock_epoch_id"])


def cancellation_case():
    lab = Lab()
    admitted = lab.admit()
    initial = snapshot(lab, lab.job_id)
    replay = lab.c.admit(lab.command, lab.mid())
    cancelled = lab.c.cancel(lab.job_id, lab.job().value["revision"], lab.mid())
    terminal = snapshot(lab, lab.job_id)
    terminal_replay = lab.c.admit(lab.command, lab.mid())
    return lab, [
        ("admitted", admitted), ("initial_snapshot", initial),
        ("identical_replay", replay), ("cancelled", cancelled),
        ("terminal_snapshot", terminal), ("cancelled_job", lab.job().value),
        ("terminal_replay", terminal_replay),
    ]


def lost_ack_case():
    lab = Lab()
    mutation_id = lab.mid()
    lab.store.fault = "after"  # Existing model commits then loses its ACK.
    uncertain = lab.c.admit(lab.command, mutation_id)
    job_id = next(iter(lab.store.state["jobs"]))
    barrier = snapshot(lab, job_id)
    blocked_replay = lab.c.admit(lab.command, lab.mid())
    lab.restart()  # A new controller object over the same in-memory fake store.
    resolved = lab.c.resolve_commit(mutation_id)
    current = snapshot(lab, job_id)
    replay = lab.c.admit(lab.command, lab.mid())
    job = lab.store.state["objects"][current["job_ref"]["digest"]].value
    return lab, [
        ("lost_ack", uncertain), ("barrier_snapshot", barrier),
        ("replay_while_uncertain", blocked_replay), ("resolved", resolved),
        ("resolved_snapshot", current), ("resolved_job", job),
        ("resolved_replay", replay),
    ]


def run_demo():
    diagnostic = prepare_intent(topic="Synthetic Dispatcher memory scenario")
    cancel_lab, cancel_events = cancellation_case()
    uncertain_lab, uncertain_events = lost_ack_case()
    for lab in (cancel_lab, uncertain_lab):
        if len(lab.store.state["jobs"]) != 1 or lab.ledger.calls != 0:
            raise RuntimeError("Synthetic case exceeded its one-job/no-dispatch boundary")
    return [("sp_diagnostic", diagnostic), *cancel_events, *uncertain_events]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    print("PURE_FAKE_ONLY - synthetic in-memory records")
    for label, value in run_demo():
        print(label)
        print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
