# SI-E01.2b.3-RESUME-2 — independent read-only review (2026-11-10)

**Reviewed feature:** `feat/story-intelligence-si-e01-2b-3-resume-2-currentness` at exact `c90b94a108ba2ef4b1a4a5ab8226d206b79fbf21`.  
**Reviewed base:** `bd16606b55ecf3ef2e29468a39d40b51e0f4e856`.  
**Status:** **REVIEW_BLOCKED_TARGETED_REPRO** — Git scope verified; source/contract inspection completed; independent acceptance **NOT** issued.

## 1. Independently established facts (GitHub)

- Base...head compare: exactly **one commit**, zero behind, correct exact parent.
- Four **added** files and no changes to pre-existing files: `story_intelligence/currentness_v1.py` (211 lines), `tests/test_story_intelligence_currentness_v1.py` (347), `tests/test_story_intelligence_currentness_vectors_v1.py` (117), and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_RESULT.md` (209); **884 added / 0 deleted**.
- Remote feature branch points to reviewed exact commit.
- The 10 literal vector cases, G02 Qa/Qb/Qc case, original CREATIVE ClaimItem retention, review of audit before freshness, exact selection head comparison, and refusal of implicit latest are present in source/tests.
- Codex reports **31 currentness, 134 SI, 976 full** tests OK (raw and outer exit 0). These are **Codex execution claims**, not independently repeated test runs. GitHub connector supports file inspection; the review environment could not clone GitHub (`Could not resolve host: github.com`). No independent test pass is claimed.

## 2. Targeted review finding — REVISION Run ERef boundary (requires proof)

**Relevant source:** `story_intelligence/currentness_v1.py`, `check_si_currentness`, the branch:

```python
run = lookup(producer)
rp = run['payload']
if h['origin']['mode'] == 'HUMAN_EDIT' and kind != 'CreativeAlternative':
    continue
if run['H']['editorial_refs']:
    return _result('INVALID', ['REF_MISSING'])
```

For any ordinary HUMAN_EDIT revision (e.g., SourceItem S2), execution takes `continue` *before* the `run['H']['editorial_refs']` check. That revision's `H.origin.run_ref` is audit/provenance-verified by `verify_si_provenance`, but the currentness semantic walk never visits the Run itself. The accepted `model_v1.py` header schema permits `H.editorial_refs` on `RunRecord` and `records_v1.py` does not explicitly prohibit them for REVISION.

**Concern:** the current actual REVISION Run may declare a relevant typed ERef with no exact validated editorial snapshot, yet the checker could report CURRENT if the revised record's own ERefs and typed payload dependencies are satisfied. This differs from the original CREATIVE Run, for which `H.editorial_refs` is explicitly checked. The RESUME-2 task says relevant typed ERefs and substantive producer `H.editorial_refs` must fail closed without a validated editorial snapshot. **Do not yet call this a confirmed behavior defect**: whether all REVISION Run header ERefs are solely audit evidence, rather than a substantive current-revision producer constraint, must be established from the original contract and an actual valid canonical graph. G01 D1 excludes historical edit bases and audit snapshots; it does not visibly state that an unresolved ERef on the *current revision's* generating Run can be ignored.

**Missing targeted test:** the 21 new unit methods cover `SourceItem.editorial_ref` and other typed external references but do not cover ERefs on an ordinary current REVISION `RunRecord.H.editorial_refs`.

## 3. Bounded independent reproduction requested before acceptance

1. Construct a genuine canonical valid `SourceItem S1 -> S2` HUMAN_EDIT graph with actual REVISION Run R, no mocks, correct Run snapshots/parent SHA/closed ancestry; verify resolver/provenance succeed.
2. Rebuild the Run and S2 hashes after giving **R.H.editorial_refs** one valid unresolved ERef. Keep `S2.H.editorial_refs=[]`, S2 payload without ERefs, and all current substantive SIRefs observed. Verify resolver/provenance still succeed. Evaluate `check_si_currentness` and publish literal graph/context digests, actual state/codes, exits.
3. Compare to a control with same unresolved ERef on a directly relevant current `S2.H.editorial_refs` and a control with the ERef on original CREATIVE Run C. Document why these differ or should not differ according to accepted original/R1/R1a/G01/G02 contracts.
4. If current code yields CURRENT and the REVISION Run ERef is indeed still substantive, mark **DEFECT / NOT ACCEPTED**, design an explicit minimal correction task, do not change accepted contracts or waive the ERef boundary. If it is demonstrably audit-only, cite the exact approved section and add a negative test clarifying the boundary before acceptance. If contract precedence does not decide the role, mark **BLOCKED_CONTRACT** and request owner decision rather than inventing semantics.
5. Independently execute the targeted/currentness and all SI suites with both child and outer exit codes on a checkout of exact SHA (or provide clear evidence why that is unavailable). Do not claim all 976 were independently rerun unless they actually were.

## 4. Disposition and STOP

- **Git hygiene / allowlist: verified PASS.**
- **Design review against G01/G02: largely consistent, one targeted ERef producer-role question outstanding.**
- **Runtime independently executed: NOT VERIFIED.**
- **Independent acceptance: WITHHELD pending bounded reproduction and contract resolution.**
- **No SI-E02, role-map implementation, ERef adapter, persistence, storage, protected writes, PR/merge/release, or changes to main.** `PUBLISH_REVISION` remains DISABLED, partial COMMIT reconstruction OFF, Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.

This review records a source-based concern and a verification requirement, **not** a change in owner-approved semantic policy.
