# Semantic validation matrix

**SP-INTEGRATION-01b · 2026-11-19 · LIMITED_DIAGNOSTIC_IMPLEMENTATION_CANDIDATE · no execution/release authority.**

|Input/artifact|Stage1 structural obligations|Stage2 semantic obligations|Never inferred|
|---|---|---|---|
|job intent|Exact1.1/policy;closed required fields;exclusive primary input;mode/fallback enums;strict hash;finite stage enum;blocked status/empty IDs|Input-derived route,exact ordered complete stage list,canonical digest,exact blocker list;plan/path/material profile|Job accepted/executed/idempotent|
|Topic/script|Meaningful string;bounded strict JSON|Existing pure classification;A production policy blocker|Editorial/scientific readiness|
|Scene plan|Closed locale/title/scenes/scene fields;ru/uk,1..20,nonblank text≤2000|Existing legacy.validate_plan + portable/simple image name/format rules|Image exists/is decodable/rights-cleared|
|Materials|Nonempty map;voice/image1..20role pattern;closed binding;strict SHA/length|Existing validate_materials/path validator;exact complete D voices/images matching declared plan|Declared hash equals current bytes,PCM/visual decode or licence proof|
|Readiness|All schema fields;axes unknown/false/true;release false;strict SI/Erefs/bindings|Existing typed-ref validation,nonblank blockers/roles,unique artifact roles,canonical relative paths|Ref resolution/currentness,authenticated review,authority|
|Route|1.1,route/mode/hash,blocked status|No cross-file/aggregate acceptance implied|Route report consistent with an unstated intent|
|Jobs|1.1,fixed no-API marker,empty accepted IDs/observations|No status mirror permitted|Authoritative JobStore state|
|Artifact manifest|1.1,diagnostic purpose,blocked publication,closed observations/refs|Existing ref/path rules,unique/nonblank roles|Protected storage receipt or rights|
|Technical gate report|1.1,known route/phase/status/check shape;technical unknown,release false|Fresh read-only observer uses existing validators;no stored-object relabeling|Qualified asset/MP4/full decode/final result PASS|
|Production readiness report|1.1,necessary boolean,release false,BLOCKED_CONTRACT,blockers|Computed from full validated readiness by assess_release;imported report is only a diagnostic declaration|Trusted verifier outcome or permission|

validate_structure alone is intentionally insufficient. validate_diagnostic is the full admission API for local objects. Structural+semantic validation never queues, publishes,mutates source materials or supplies facts/rights/permissions. Paths have a single reused parser; canonical-equality requirement prevents silent backslash normalization. Actual file resolution uses original observer and is subject to documented TOCTOU/OS limits.

Error model: ValueError family; new DiagnosticValidationError exposes code/path (SCHEMA_KIND,SCHEMA_PROFILE,STRUCTURE,PATH,MATERIALS,ROUTE_STAGES,DIGEST,BLOCKERS,TEXT,BINDINGS,SEMANTIC,MODE,STATE). Existing SI limits/type/ref errors are reused unchanged. Invalid readiness assessment fails closed with INVALID_READINESS rather than setting necessary=true; invalid mode/assertion type raises. CLI maps validation/read errors to INVALID_INPUT/exit2. Missing Dispatcher remains explicit exit3, never simulated success.
