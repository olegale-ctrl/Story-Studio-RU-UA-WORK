# Future minimal implementation task proposal

**MVP-08B.2a · 2026-11-19 · DOCS_ONLY · PROPOSAL — NOT APPROVED FOR IMPLEMENTATION.**

## NOT AUTHORIZED — entry conditions first

This is a proposed technical task, not an instruction to execute now. The owner must review these six documents, resolve applicable EC choices, accept the exact scope and separately authorize implementation. D01–D08 and MVP-08A limitations remain unchanged; publication approves no new runtime rule.

Recommended future implementation base: `16d28ec0376c8c28f879c8aacb18d5378fea83a3`, tree `b509c60f396c0f47ce99a9d73de9d9afdb9fa53d`, which contains the existing Asset Library and SP/1.1 code. **The owner must confirm that exact future base.** The current audit/docs branch lacks that experimental implementation, so it must not be silently substituted. Read B.1 at `f0bce140451bf00a86f3939330e77ed63b2c98be`, B.2 at `04ea194e4d57c8a0550d7412281da58d4ba252c5`, and this proposal by immutable commit; do not merge their code automatically.

Pin this proposal's final commit/tree from the external handoff before coding. Proposed future branch `feat/offline-generationjob-core` is not created here. A mismatch in source, tree, allowlist, agreed profile, or missing positive fixture is a STOP. No model/render/download operation is implied to manufacture missing F01 bytes or licence evidence. A pure-only scope cannot be reported as durable execution acceptance.

## Exact prospective file allowlist

All rows are PROPOSED_NOT_CREATED. The initial implementation changes no existing file. If a public Library/SP/G3 change is needed, STOP and report the specific contract gap. No CI workflow, main or production configuration change.

|Path|Purpose/interfaces|Constraints/oracles|
|---|---|---|
|`experimental_mvp/offline_execution/__init__.py`|Public fixedprofile exports only|No import-time DB/thread/provider effects|
|`experimental_mvp/offline_execution/contracts.py`|ClosedRequestIntent/Job/Receipt/Error/Cursorvalidators;canonical bytes/hash using existingencoded|Request/batch/auth projections,strict types,versioned namespaces;P001–P005/P020|
|`experimental_mvp/offline_execution/job_store.py`|ManagedSQLiteJobStore,accept/lookup/snapshot/fencedCAS,event/outbox/receipttransactions|W atomicity,unique keys,versions,storeidentity;D001–D018|
|`experimental_mvp/offline_execution/controller.py`|Single lifecycle/effectgateway/claim/reconcile/cancel/run_oneowner|No extraqueue/scheduler;originalguardedsubset,lease/currentness|
|`experimental_mvp/offline_execution/simulator.py`|Fixedproviderfacade,separate durableacceptanceledger,FixtureRegistry,persistedscriptcursor|Onlysyntheticidentities;lookupbyeffecttoken,zerospend;no models/render/network|
|`experimental_mvp/offline_execution/policy.py`|SyntheticFixtureContext/BatchPermit validation andLeaseClockinterfaces|Notrealattestation/issuer;no newcryptoscheme;EC-04/07|
|`experimental_mvp/offline_execution/observer.py`|Consistentreadonlysnapshot/cursor/boundedwait|Timeoutnodata/statechanges;nolocalmirrorauthority|
|`scripts/offline_generation_job.py`|Thinaccept/observe/wait/run-one/reconcile/cancelcommands|CallsonecontrollerAPI;no privatequeue/retry/recovery/renderer|
|`tests/test_offline_generation_job_contracts.py`|Purevalue/hash/key/version/authoritytests|P001–P007/P011/P020/P022–P024|
|`tests/test_offline_generation_job_store.py`|FakeStoretests andseparatelymarkedlocalSQLitequalification|No claimedpowerloss/native qualification|
|`tests/test_offline_generation_job_controller.py`|Guardedstates/revision/fencing/canceltests|P008–P010/P014/P017/P018|
|`tests/test_offline_generation_job_simulator.py`|Deterministicscript/acceptance/lostACK/identitytests|P013/P015/P016;applicableSIMprefixesonly|
|`tests/test_offline_generation_job_observer.py`|Snapshot/cursor/deadline/unavailablestoretests|P019/P021,D014|
|`tests/test_offline_generation_job_faults.py`|Finitebefore/aftercommit/effect/replyfaultmatrix|Pureanddurablemarkersseparate;boundeddeadline|
|`tests/test_offline_generation_job_no_effects.py`|Network/subprocess/model/render/Library/saveprohibitionguards|Allforbiddencalls0;no fabricatedproductiongrant|
|`tests/fixtures/offline_generation_job/manifest.json`|Owner-reviewedfixtureprofile/bytes/rights/limits/tracebindings|Noplaceholderhashpositive;EC-07required|
|`tests/fixtures/offline_generation_job/F01.mp4`|Exactprequalifiedself-authoredfixturecopyonly|Notgenerated/downloadedbythisproposal;≤8MiBproposed|
|`tests/fixtures/offline_generation_job/project.json`|Exactnon-userprojectfixturewithdeclaredstableIDs|Noimplicitmigrationofactualprojects|
|`tests/fixtures/offline_generation_job/prompt.txt`|Exactself-authorednonsensitivepromptfixture|Rawbyteshash,notnewlivemodelinput|
|`tests/fixtures/offline_generation_job/requests.json`|Closedscopedinputfixtures,positive/negativeproposals|Noauthenticattestations/secrets|
|`tests/fixtures/offline_generation_job/expected_trace.json`|Versionedexactevent/callcount/ledger/phaseexpectations|COMPLETEDnotpositivecoreexit|
|`docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md`|Futureactualversions/commands/counts/skips/exitcodes/faultlimits/hashhandoff|Stopforindependentreview;noautomaticnextstage|

Exactly22 paths above: seven package files, one thin CLI, seven test modules, six frozen fixture files and one result document. No secondJobStore/controller,no genericDAG,nomodel/provider/downloader/GUI/nativebroker implementation. RuntimeDBs/journals/lock/logs innewmanagedtestroot,outsideGit;fixtureMP4onlyifexplicitlyregisteredandqualified,nobigmodels/userimages.

## Proposed interface contract

|Owner|Interface|Semantics|
|---|---|---|
|contracts|validate_request /request_bytes /request_sha256 /validate_binding|Closedexplicitversions;core→manifest→grantgraph;noSP/PGhashalias|
|JobStore|create_store(root,new_store_id,profile);open_store(root,expected_store_id,profile)|Explicitcreatevsopen;refuseunknownexisting/corrupt/missingidentity;no repair/migration|
|Controllerfacade|accept_request(intent,key,batch_permit,fixture_context)|ACCEPTED/REUSED/CONFLICT+immutablecommitreceipt;noexecutionpermissionfromdisposition|
|JobStore|lookup_acceptance(key,expected_request_hash);snapshot(job_id,cursor)|Authoritativeconsistentread;unavailable≠noacceptance|
|JobStore|cas_mutate(job_id,expected_revision,controller_fence,worker_fence,edge,evidence,outbox_delta)|OneSQLtransactionjob/event/outbox/receipt;onlyoriginalenabledguardededges|
|Controller|claim/renew_lease(job_id,expected_revision);run_one(job_id);reconcile(job_id);cancel(job_id,scope)|Singleowner;fence/clock/authorityonallrelevantboundaries;nonewsubmitonunknown|
|SimulatorStore|accept(effect_token,payload_hash,fixture_context);lookup(effect_token);poll(provider_id,cursor);cancel_same_intent|Durableproviderledgeronly,nolifecyclequeue;fixedscript/zerocharge|
|Observer|observe(job_id,cursor);wait(job_id,predicate,deadline,cursor)|Readonlyboundedobservation;no state mutation/retry/cancel ontimeout|
|policy|validate_fixture_scope;LeaseClock.observe|Synthetictrustedharnessonly,notrealidentity/rights/productionissuer|

Admission/preflight transactions use the exclusive **controller** fence plus expected revision; worker-phase changes also require the current job lease. First lease claim allocates an epoch atomically under the controller fence, without requiring a prior worker lease. Internal DDL/index SQL is an implementation detail within the closed contract; public schema or guarantee changes require review and STOP.

## Mandatory invariants

- I01: one controller owns all queue transitions, effects and recovery. CLI and observer own no retry or scheduling loop.
- I02: accepted content, key and initial scope are immutable. Reuse returns the exact receipt; no implicit renewal.
- I03: request hashing is acyclic. Distinct hash domains and exact canonical bytes are checked, not merely labels.
- I04: acceptance ACK follows store commit. Job revision, event and outbox mutation are atomic.
- I05: current controller and applicable job fence are checked before effects/receipts. Stale or expired tokens make no new progress.
- I06: W precedes effects; simulator acceptance commits before its reply. No atomic transaction across the two DBs is assumed.
- I07: unknown outcome means hold and lookup of the original token, never store reset or new generation.
- I08: fixed synthetic profile, budget0, one generation attempt. No live/model/paid fallback.
- I09: observer is authoritative and read-only. Deadline/cursor logic cannot change job truth.
- I10: RESULT_AVAILABLE is not COMPLETED. Deferred SM12–16 and SG05/SG10 qualification cannot be faked.
- I11: Library, user projects, Tk and protected storage remain unchanged; initial core does not import/attach/save.
- I12: synthetic grants/receipts/fixtures are not real identity, rights, render or release authority.
- I13: explicit caps and qualified local root/clock; no unknown user-file overwrite, deletion, repair or migration.
- I14: no actual Route D execution until a separate mapping is approved; no DAG or direct renderer bypass.

## Required execution/report order once separately authorized

1. Reverifyexactbase/tree/source andacceptedECprofile,all22proposedfiles/fixturehashes;createisolatedbranch,freeze runtime/toolingandresource/timecaps.
2. Implementboundedpurelogic andFakeStore/ClocktestsP001–P024;allreportedcurrentcounts/exitcodes. Noexistingruntimecodechangesorrealprovider.
3. Onlyunderapprovedlocalstoragequalification,runD001–D018withnewprivateSQLiteDBs;distinguishprocesscrash/powerloss,unknown/corruptstore,noautomaticrepair. Usefinitefaultpoints,recordfailed/interruptedattempts.
4. Runavailable**safe**regressionsandoldSP37tests/46freeze/new1.1vectorswhereapplicable;nohistoricalcountsreportedfresh. No renderer/modeltestsunderthisprofile. Missingtestdependency/platformreportedNOT_RUN,nosilentPASS.
5. WindowsW001–W008onlywithrealauthorizedenvironmentandseparatescope;otherwiseNOT_RUN. A001–A010andL001–L006remainlaterqualification,notpartinitialsuccess.
6. Exportfull-indexdiff,filemodes/Gitblobs/rawSHA,actualDB/receipt/traceproofunderprivacybounds;reportaccepted/reused/conflict,uncertainty,stale-fence,noeffects,knownlimits. Stopforindependentcoreaudit;noautomaticSPintegration/Library/native/livequalificationorproduction.

## Explicit STOP conditions

STOP_VERSION/BASE:exactsource/schema/profile/baseunexpected,unreviewedmigrationorallowlistedexistingfileeditneeded.
STOP_CONTRACT:unresolvedapplicableEC/OD dependency,ambiguoushashprojection/key/state,requiredclosedinterfacechange.
STOP_FIXTURE:missing/unqualifiedF01/project/prompt/manifest/rights/hash;nonewmodel/download/render.
STOP_INTEGRITY:store/ledger/cursor/receiptcontradiction,wrongidentity,missingexpectedstore;preserveevidence,no reset.
STOP_AUTHORITY:unknown/revoked/expired/wrong-scopegrant,unqualifiedclock/root/platform,budget/providerchange;noeffect.
STOP_SCOPE:actualLibrary/save/renderer/GUI/native/live/paid/productionrequested;notcoveredbythisfuturetask.
STOP_COMPLETION:falseCOMPLETEDorartifact/GUI-linkinsteadSGreceipts;donotweakencontracttogettests green.

No implementation task runs automatically after this document is committed. Owner authorization must name the accepted proposal commit, profile, base, paths and allowed stages. Publishing this proposal authorizes none of those effects.
