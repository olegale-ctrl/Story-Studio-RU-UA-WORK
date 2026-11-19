# Discovery inventory

**2026-11-19 · READ_ONLY_AUDIT / DOCS_ONLY · no implementation or production authorization.**

Audit branch `audit/mvp-08b-2-implementation-recovery` begins at fetched current remote main `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`. Existing local main was not reset. Other branches inspected by Git objects or isolated detached worktree; no code merged or transferred into audit branch.

## Verified scope

- GitHub snapshot:174advertised remote heads,0tags; fetched all heads,13pull/head refs and6currently advertised PR merge refs.219local refs scanned;320commit objects including reflog and2unreachable commits;1104unique tree-referenced blobs,1009text blobs and279code blobs within configured text bounds. Functional search found257matching blobs,41code blobs across22code paths. Search included all branches/history,not just names. All refs/commit trees and hits saved externally.
- Thirteen accessible PRs independently listed via connector search and paginated REST;all13metadata/file inventories retrieved (PR4 transient tool error succeeded on retry). Seven closed+merged;6open (5draft,1non-draft). No MVP08B.2 PR located. PR11 head6cfa7b4b535b0171ae2871b7e68e545b48ba332a carries the unrelated LAB code;it is open draft,not an MVP08B implementation acceptance.
-29worktrees at discovery snapshot,all clean;one additional detached lab worktree created later solely for pure tests. Local roots /workspace/work,/workspace/artifacts,/workspace/attachments:23862files inventoried,14792small UTF8/text candidates scanned,1501matching files/358code-file matches.105unique matching code artifacts not in matching Git blobs were AST-reviewed:tooling/stdlib and evidence/document builders,not a recovered app JobStore. Tooling/cache/Git/audit-output/symlink directories excluded explicitly (146directory exclusions recorded).
- Seven local archives:all inspected without extraction/execution. Initial32MB bound excluded one36.9MB MVP07.1 packet;it was subsequently revisited with bounded streaming headers (65members,135354282declared uncompressed bytes),no requested execution-entity hits. Other packet code mostly duplicates pinned source or report builders. Archive hashes and both initial/final coverage records retained.
-24unreachable UTF8 blobs reviewed separately;four job-control keyword hits are uncommitted earlier Markdown drafts of08B.1 proposals,not Python implementation. Two unreachable commits are G2/G3.1 CI merge objects,with known trees504881f/920713b;no new job layer.
-37historical Actions runs retrieved with complete pagination:35success,2failure (old Sprint25.1 revisions). No run associated with MVP08B/SP branch names or pinned08B.1/SP01b head. Current main run44048660501 and PR11 head run43935807382 each have successful Ubuntu Python3.10/3.13jobs. No Windows qualification inferred.

Functional terms included Dispatcher,JobStore,GenerationJob,idempotency,lease,fencing,CAS,outbox,reconciliation,result ingestion,observer,recovery,publication receipt,sqlite3,CREATE TABLE,thread pools and queue primitives. All tree text/code scans used size/UTF8 bounds (Git≤4MB,local text≤2MB,archive text≤1MB);binary/tooling/remote-unadvertised data and inaccessible machines are outside semantic verification. This is not proof of absence across every possible copy of the project.

## Candidates and related false positives

All repositories below are `olegale-ctrl/Story-Studio-RU-UA-WORK`. Full ref→commit→tree map and exact tip-commit changed-file lists are in candidates.json;GitHub PR file lists separate. “Tip changes” means first-parent→listed tip,not a fabricated full implementation allowlist.

|ID/ref|Commit|Tree|PR head / tip changes|Completeness / tests|
|---|---|---|---|---|
|C01 `docs/story-studio-experimental-mvp-08b-1-dispatcher-contract`|`f0bce140451bf00a86f3939330e77ed63b2c98be`|`0b5238611cc84ef0a665f75b552757666935516e`|No PR head matched;15 tip files|Docs only;78proposed oracles NOT_RUN|
|C02 `fix/editorial-e01-3-9-4-s3-2a-cold-admission-guard`|`13ed35db93e05641631ad3fa4a0d2ea3475c6719`|`6271df48ce5240574a4e41e880660c19d50b92db`|No PR head matched;4 tip files|RAM fixture dispatcher;bounded pure tests this audit|
|C02-OLD `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core-resume`|`b27a084c99510406c407d5785328a31eb5f1df94`|`42c79c68f6d379caa0a74ba0b58c7ba60b39ed2e`|No PR head matched;7 tip files|Earlier RAM blob;cold guard corrected later;not rerun|
|C03 `fix/editorial-e01-3-9-3-s2-4-parent-epoch-binding`|`21b1f06c1560ff65e6dc9c47ac9a972e5a3f2879`|`3d1a180ef18d25244a92f9f5729ed3d1e1168591`|No PR head matched;3 tip files|Virtual transaction/recovery;selected model tests only|
|C04 `feat/story-studio-experimental-mvp-08a-asset-library`|`1ff403e47d35adb34139278de1d056fbbc563e6d`|`2fecb71e711861431a775f4aa3764d771f35ecb5`|No PR head matched;16 tip files|Persistent assets;no job queue;media tests not run|
|C05 `fix/sp-integration-01b-diagnostic-reconciliation`|`16d28ec0376c8c28f879c8aacb18d5378fea83a3`|`b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`|No PR head matched;18 tip files|Diagnostic only;no submit;source inspected|
|C06 `import/upstream-technology-review`|`b3f3c0513aff09df2a97fdbe1f36f93b732c3f92`|`fceec7d668b22ccdf120d85fab11f9e602c2f988`|#1 closed merged;1 tip files|Upstream reference executor;no render test|
|C07 `feature/sprint27-cpu-lipsync`|`18ab59fba6f10996791457dcb0f97beddfdfc6fc`|`3cef10f1048e0852f9de5ff71307c486604b4f3c`|#5 open;1 tip files|Lip-sync adapter;no render/model test|


C01 is contract-only. C02/C02-OLD are real executable portable **RAM LAB/1 storage dispatchers**,not persistent GenerationJob controllers. C03 is pure S1/S2 transactional/recovery modeling. C04 is a persistent Asset Library plus transient GUI communication queues,not a job ledger. C05 is explicitly blocked diagnostic preparation. C06 is upstream reference rendering with a ThreadPoolExecutor,not qualified/durable job orchestration. C07 is an unrelated CPU lip-sync adapter;no render/model test was run. Exact per-candidate test availability/completeness is in implementation audit.

C02 source has65remote-ref carriers;the fact it appears under many later SI branches does not turn it into08B.2. Source blob identity maps this shared lineage;older b27a dispatcher blobfc1779... is superseded by corrected940614... at13ed and PR11. No API with an actual JobStore/GenerationJob runtime definition was found in verified application code. A match in CPython asyncore/XMLRPC dispatcher classes or Markdown strings is not a project implementation.

No exact historical docs/tasks/MVP_08B* implementation source was found;B.1 authority sources are in experimental_mvp/reports at pinnedf0bce,not current main. New audit documents are not inserted into that normative source. No assumption that a prior authorized task was actually executed.
