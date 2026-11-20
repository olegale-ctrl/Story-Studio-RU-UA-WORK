# DQ-01 first cloud experiment — prepared run

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
