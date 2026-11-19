# Hardware preflight integration

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

Existing `python scripts/check_hardware.py` calls `core.hardware_profile.probe/recommend`: CPU-first OS/CPU/logical processors, Windows CIM RAM/GPU if available, no benchmarks/network/model installation. Linux RAM may be unknown; presence of a GPU does not establish backend suitability. Existing recommendation enabling Silero/Edge is not execution authorization and cannot override D01-D08 or current network STOP.

New pure `hardware_preflight(profile,available_disk_bytes=...,required_ram_gib=4,required_disk_bytes=1000000000)` consumes existing profile v1. Unknown/insufficient RAM/disk and unavailable CPU block. Thresholds are explicitly diagnostic examples, not an approved model workload budget. Even sufficient numbers always return BLOCKED_WORKLOAD_QUALIFICATION and provider_execution_allowed=false. Optional models/ComfyUI/Wan remain unused; installed is not qualified.

Missing qualification contract must bind workload/model exact version/hash, runtime versions, platform/architecture, RAM/VRAM/peak working set, free disk/staging/cache budgets, allowed providers, bounded resource policy and expiry/currentness. No approved profile exists for proposed SP job types; no new hardware manager, benchmarks, process killing, pagefile changes or model installations introduced. Runtime/tool presence can be passively observed but is not claimed to prove safe generation; CLI does not initiate an automatic hardware probe.

Current environment is Linux Python3.12.14. Windows10/11, Python3.13.17/Tk/native reparse-point behavior are NOT_RUN. Existing limitations remain open. Hardware command output/exit code is preserved externally and reported honestly, including unknown RAM. No heavy generation is used to claim qualification.
