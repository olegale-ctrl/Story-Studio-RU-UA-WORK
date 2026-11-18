# Independent MVP-05/06 acceptance packet

**Target status:** READY_FOR_INDEPENDENT_MVP_05_06_REVIEW. This is a request for independent review and owner decision, not Windows acceptance, a merge request, a release or permission to produce/publish real materials.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `feat/story-studio-experimental-rc-02`.
- Exact base: `1f27a9bb024b4e2ad18121843f14fe57d0522f17`.
- Base tree: `2fd1e0f9f121016827f726606b821b510f6806e3`.
- Base parent: `0dc314311b1f6ae2d0a0ed51aaabe3406badcbec`.
- Publication branch: `feat/story-studio-experimental-mvp-05-06-media-hub`.
- Main observed before work: `a28277b4cb68a3db5da52edc598c37ce66314604`; main must remain unchanged.
- Exact final commit/tree/blob SHA-1 and byte SHA-256 are supplied by the accompanying post-commit `ACCEPTANCE_MANIFEST.json`. A document cannot contain its own final Git blob/commit hash without self-reference; use the manifest and reproducible commands below, not a guessed placeholder.

## Review contents

1. RC02_INDEPENDENT_BASELINE.md — exact baseline, actual Linux checks, Windows NOT_RUN.
2. ../MVP_05_06_WINDOWS.md — installation, complete manual/offline walkthrough, optional LLM and credentials, independent Windows checklist.
3. MVP_05_06_ARCHITECTURE_AND_LIMITATIONS.md — implemented versus unimplemented, known risks and proposed next priorities.
4. AI_PROVIDER_RESEARCH_2026_11.md and ../providers.json — all 13 services, official sources, date and explicit UNKNOWN fields.
5. MVP_05_06_TEST_RESULTS.md and evidence/ — actual test counts, skips, versions, exit codes, widget smoke, probe/decode results.
6. MVP_05_06_LICENSES.md and DEJAVU_NOTICE.txt — source/asset/license review, no bundled external runtimes.
7. ../demos/media_hub/ — portable RU/UK project JSON, manual editorial inputs, original cards and local synthetic narration.
8. ../test_media_hub.py and ../test_media_ui.py — offline oracles and real Tk widget smoke. ../test_pipeline.py retained unchanged.

## Independent review questions

- Confirm all changed paths are under experimental_mvp and the parent is the exact RC-02 base; inspect the full diff, including binaries, without importing deferred PR #11 files.
- Re-run both experimental and core suites, and FFprobe/full-decode both included-demo renders. Verify transcript content and timing by human listening; a full decode is a technical check only.
- Run Windows 10/11 CPU-only acceptance. Test fonts/scaling, Cyrillic file paths, shell player and Windows Credential Manager on the actual target environment.
- Verify the five-stage product flow with a manual project and separately with an owner-chosen compatible LLM. Actual remote/local-model inference, real provider login, quotas and generation have not been tested.
- Confirm self-reported account status is not described as verified connection, READY is not a credit reservation, and UNKNOWN rights/quotas never imply permission. Do not reuse web credits as API credits by assumption.
- Review TOCTOU/reparse, untrusted media, filesystem trust, cancellation granularity, estimated timing, partially written evidence and lack of protected production storage. No production authorization is implemented.

## Reproducible Git verification

Run in a clean checkout of the exact final commit from the manifest:

```bash
git rev-parse HEAD HEAD^{tree} HEAD^
git diff --name-status 1f27a9bb024b4e2ad18121843f14fe57d0522f17 HEAD
git diff --check 1f27a9bb024b4e2ad18121843f14fe57d0522f17 HEAD
git diff --binary 1f27a9bb024b4e2ad18121843f14fe57d0522f17 HEAD > exact-change.patch
git ls-tree -r HEAD -- experimental_mvp
```

The manifest lists every changed path with mode, Git blob SHA and SHA-256 of bytes from `git show HEAD:path`. It is generated after the commit and accompanies the final reply; it is not a self-hashing repository file.

**STOP:** independent ChatGPT audit and owner decision required before any further implementation stage, merge, release or production deployment. No CI workflow was changed or new CI run requested. Publishing this feature branch does not change main.
