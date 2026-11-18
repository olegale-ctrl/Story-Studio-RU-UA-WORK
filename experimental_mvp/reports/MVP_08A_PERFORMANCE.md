# MVP-08A — Local performance measurements

**Status: EXPERIMENTAL — independent review required.** Date2026-11-18. Linux only; WINDOWS_NOT_RUN.

Final implementation measured after the full suite completed, on synthetic FFmpeg patterns. Single-run exploratory timings, not percentiles/SLA. Warm local filesystem;30catalog records at search/recovery. Python tracemalloc peaks exclude native FFmpeg/SQLite allocations. Process lifetime maxRSS isn't per-operation native memory.

Environment: Linux-6.18.57-x86_64-with-glibc2.41; Python 3.12.14, SQLite 3.53.1; ffmpeg version 7.1.5-0+deb13u1 Copyright (c) 2000-2026 the FFmpeg developers.3logical CPUs; Tk9.0.4 when GUI used.

|Operation|Input bytes|Catalog records before|Seconds|Peak Python allocation bytes|
|---|---:|---:|---:|---:|
|image import|30324|0|0.140144|1202967|
|MP4 import full decode|177682|1|0.188910|1241276|
|duplicate content independent record|177682|2|0.239412|1241164|
|catalog exact tag search 30 records|0|30|0.003352|165302|
|SHA verify MP4|177682|30|0.001640|1239609|
|image thumbnail|30324|30|0.265742|1094284|
|video poster thumbnail|177682|30|0.316038|1241559|
|restart recovery after exit73|0|30|0.020328|1247011|
|repeated recovery|0|30|0.014366|1244666|

Process lifetime maxRSS 22908KiB. All9measured operations exit0. Crash setup deliberately exits73 after publication; recovery aborts one pending intent, repeat aborts none. Final source hashes match code-under-test snapshot. External performance.json/log and synthetic PNG30324bytes/MP4177682bytes retained outside Git. No large-catalog, hostile-writer, power-loss, Windows or provider-latency benchmark claimed.
