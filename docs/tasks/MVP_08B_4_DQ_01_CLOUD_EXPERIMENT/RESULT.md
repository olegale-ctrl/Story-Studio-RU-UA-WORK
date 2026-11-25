# DQ-01 first cloud experiment — observed result

## Follow-up verification on 2026-11-25

GitHub Actions [run 44784929633](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/actions/runs/44784929633), head `a410a7c29a5ab31c46ad97f1fa79c56ed12866bc`, completed **success** after creation on 2026-11-20 at 17:36:37 UTC. The `preflight` job and its environment-observation, evidence-preservation and gate-reporting steps all report success in the GitHub API.

The pinned workflow deliberately reports **BLOCKED_PRE_WRITE_GATE / SQLITE_SMOKE=NOT_RUN**. It does not authorize a SQLite connection or choose a qualified native lab root. The observation confirms completion of the bounded workflow; native qualification and Stage B remain pending their separate conditions.

The artifacts endpoint returned an empty list on 2026-11-25. The original metadata evidence bytes, their SHA256SUMS and artifact digest were unavailable for re-download through that endpoint. This follow-up does not reconstruct their hashes or assert measured filesystem/runtime facts from the job's success alone. Preserve any previously downloaded evidence separately if it exists. Actual runner measurements and an exact owner-confirmed root/profile must be reviewed before any native experiment.

This follow-up changes only this report on a separate documentation branch. The original experimental branch and workflow stay at their recorded revision. No workflow rerun was requested. The preparation record below is retained as historical context and its future-tense result instructions are superseded by this observation.

## Historical preparation record

Experimental branch: `experiment/dq01-cloud-lab-01`.
Exact base: `32bc369ef66e45f1bc72d7afbef6a41688036774`, tree
`2c1bcbfd130911c1a5619f2a784daf94c8de61e6`.
Contract: `4a6780bf519e03ddafa5ae9d7ed0f4309bff7c89`, tree
`e327219b1ba07de5479d167d3280ff29024f90a8`.

Owner task authorizes one GitHub Actions cloud experiment. No main change,
merge, FI, native process kill, production access or production permission.
The accepted Stage A and contract files are unchanged.

The first run is deliberately preflight-only: no exact cloud root grant or
measured runtime profile has been confirmed. No SQLite connect, database,
lab root or journal is created; no smoke implementation can bypass the gate.
GitHub-managed CI evidence artifacts are separate from any native lab root.
They contain selected runner/runtime/mount metadata only, not secrets or data.

Trigger: push on this exact experimental branch, only when this new workflow
path changes. No workflow_dispatch/default-branch dependency, PR, schedule,
automatic repeat or default-branch workflow update. run_attempt must be 1.
No checkout, Python installation, dependencies, repository secrets or named
GitHub environment. Permissions: contents read, all other explicit scopes
absent. Hosted runner label ubuntu-24.04; job 5 minutes, preflight command
60 seconds, artifact step 2 minutes. No native children. Evidence JSON <=64
KiB, exactly three own metadata files, retention 3 days.

GitHub API observations before launch: repository public, active, default
branch main. Actions permissions and default-workflow-permissions endpoints
both returned HTTP 403 Resource not accessible by integration. No settings
were changed and settings availability is not claimed. Existing workflow runs
are readable. Actual runner availability and effective token permissions will
be reported from this one run. ubuntu-latest historical jobs do not prove
ubuntu-24.04 availability. upload-artifact v4.6.2 Git tag was checked and
matches pinned commit ea165f8d65b6e75b540449e92b4886f43607fa02.

Execution results/run URL/artifact hashes will replace this prepared record
following the single run. Updating this report alone cannot trigger it again.
A successful Actions job is not a passed native gate or smoke test.
