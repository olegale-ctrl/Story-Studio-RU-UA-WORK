"""Boundary checks for the developer scenario through the existing Controller."""
import builtins
from copy import deepcopy
import io
import json
import os
import socket
import sqlite3
import subprocess
import time

import pytest

from scripts import dispatcher_memory_demo as demo
from experimental_mvp.offline_execution import policy
from experimental_mvp.offline_execution.contracts import seal
from test_offline_generation_job_contracts import record
from test_offline_generation_job_controller import Lab


def test_cancel_replay_and_terminal_snapshot():
    lab, events = demo.cancellation_case()
    result = dict(events)
    assert result["admitted"]["disposition"] == "ACCEPTED"
    assert result["identical_replay"]["disposition"] == "REUSED"
    assert result["cancelled"]["disposition"] == "APPLIED"
    assert lab.job().value["state"] == "CANCELLED"
    assert result["cancelled_job"] == lab.job().value
    assert result["terminal_replay"]["receipt_ref"] == result["admitted"]["receipt_ref"]
    assert result["terminal_replay"]["disposition"] == "REUSED"
    assert result["initial_snapshot"]["job_ref"] != result["terminal_snapshot"]["job_ref"]
    assert result["terminal_snapshot"]["job_ref"] == lab.job().ref
    assert result["terminal_snapshot"]["pipeline_complete"] is False
    assert len(lab.store.state["jobs"]) == 1
    assert not lab.store.state["slots"]
    assert lab.store.commits == 2
    assert lab.ledger.calls == 0


def test_lost_ack_resolves_original_mutation_without_recommit():
    lab, events = demo.lost_ack_case()
    result = dict(events)
    for label in ("lost_ack", "replay_while_uncertain"):
        assert result[label]["disposition"] == "HOLD"
        assert result[label]["error"]["code"] == "UNKNOWN_COMMIT_OUTCOME"
    assert result["barrier_snapshot"]["barriers"] == ["UNKNOWN_COMMIT_OUTCOME"]
    assert result["resolved"]["mutation_outcome"] == "COMMITTED"
    assert result["resolved"]["disposition"] == "ACCEPTED"
    assert result["resolved_replay"]["receipt_ref"] == result["resolved"]["receipt_ref"]
    assert result["resolved_replay"]["disposition"] == "REUSED"
    assert result["resolved_snapshot"]["barriers"] == []
    assert result["resolved_snapshot"]["pipeline_complete"] is False
    assert result["resolved_job"]["state"] == "DRAFT"
    assert len(lab.store.state["jobs"]) == lab.store.commits == 1
    assert not lab.store.state["pending"]
    assert lab.ledger.calls == 0


@pytest.mark.parametrize("case,code", [
    ("changed_key", "IDEMPOTENCY_CONFLICT"),
    ("namespace", "NAMESPACE_MISMATCH"),
    ("revision", "CAS_CONFLICT"),
    ("authority", "AUTHORITY_MISSING"),
    ("terminal", "ILLEGAL_TRANSITION"),
])
def test_rejected_operations_preserve_store(case, code):
    lab = Lab()
    lab.admit()
    if case == "changed_key":
        changed = lab.variant().value
        changed["key_ref"] = lab.command.value["key_ref"]
        command = lab.add(seal("AdmissionCommand", **{
            key: value for key, value in changed.items()
            if key not in ("kind", "version", "scope")
        }))
        operation = lambda: lab.c.admit(command, lab.mid())
    elif case == "namespace":
        changed = lab.command.value
        changed["namespace_ref"] = {**changed["namespace_ref"], "digest": "0" * 64}
        command = seal("AdmissionCommand", **{
            key: value for key, value in changed.items()
            if key not in ("kind", "version", "scope")
        })
        operation = lambda: lab.c.admit(command, lab.mid())
    elif case == "revision":
        operation = lambda: lab.c.cancel(lab.job_id, 0, lab.mid())
    elif case == "authority":
        lab.c.authority = policy.Authority(frozenset())
        operation = lambda: lab.c.advance(
            lab.job_id, lab.job().value["revision"], lab.mid(), "AWAITING_APPROVAL")
    else:
        lab.c.cancel(lab.job_id, lab.job().value["revision"], lab.mid())
        operation = lambda: lab.c.cancel(lab.job_id, lab.job().value["revision"], lab.mid())
    before = lab.store.snapshot()
    commits = lab.store.commits
    outcome = operation()
    assert outcome["disposition"] == "REJECTED"
    assert outcome["error"]["code"] == code
    assert lab.store.snapshot() == before
    assert lab.store.commits == commits
    assert lab.ledger.calls == 0


def test_corrupt_store_holds_without_claiming_resolution():
    lab = Lab()
    mutation_id = lab.mid()
    lab.store.fault = "partial"
    lab.c.admit(lab.command, mutation_id)
    before = lab.store.snapshot()
    result = lab.c.resolve_commit(mutation_id)
    assert result["disposition"] == "HOLD"
    assert result["error"]["code"] == "STORE_CORRUPT"
    assert result["mutation_outcome"] == "UNKNOWN_COMMIT_OUTCOME"
    assert lab.store.snapshot() == before
    assert lab.store.state["pending"] == {mutation_id}


def test_demo_is_deterministic_and_fixtures_remain_unchanged():
    original = deepcopy(record("AdmissionCommand").value)
    first = demo.run_demo()
    assert demo.run_demo() == first
    assert record("AdmissionCommand").value == original
    diagnostic = dict(first)["sp_diagnostic"]
    assert diagnostic["schema_version"] == "SP/1.1-DIAGNOSTIC"
    assert diagnostic["accepted_job_ids"] == []
    assert diagnostic["status"] == "BLOCKED_DISPATCHER_CONTRACT"
    assert diagnostic["intent_sha256"] != dict(first)["admitted"]["job_ref"]["digest"]


def test_no_effects_during_scenario(monkeypatch):
    original_open = builtins.open
    original_io_open = io.open
    hits = []

    def forbidden(*args, **kwargs):
        hits.append("native_effect")
        raise AssertionError("Unexpected native effect")

    def read_only(opener):
        def open_checked(file, mode="r", *args, **kwargs):
            if any(letter in mode for letter in "wax+"):
                return forbidden()
            return opener(file, mode, *args, **kwargs)
        return open_checked

    monkeypatch.setattr(builtins, "open", read_only(original_open))
    monkeypatch.setattr(io, "open", read_only(original_io_open))
    for module, names in (
        (os, ("open", "system", "urandom", "mkdir", "remove", "rename")),
        (socket, ("socket", "create_connection")),
        (sqlite3, ("connect",)),
        (subprocess, ("Popen", "run", "call", "check_output")),
        (time, ("time", "monotonic", "sleep", "perf_counter")),
    ):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    assert demo.run_demo()
    assert hits == []


def test_cli_prints_existing_records(capsys):
    assert demo.main([]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("PURE_FAKE_ONLY")
    records = [json.loads(line) for line in lines[2::2]]
    assert len(records) == len(demo.run_demo())
    assert records[0]["accepted_job_ids"] == []
    assert all(value["scope"] == "PURE_FAKE_ONLY" for value in records[1:])


def test_cli_rejects_execution_options():
    with pytest.raises(SystemExit) as error:
        demo.main(["--production"])
    assert error.value.code == 2
