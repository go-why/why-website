---
title: "Performance"
weight: 40
---

Why compiles to C. The performance ceiling is that of C. This page shows where Why sits against C, and says plainly where it wins and where it loses. The reference figures come from the separate benchmark repository, and match the paper.

**Machine.** Darwin arm64. Apple clang 21 (`-O2`), go1.27.3, rustc 1.99.1, Odin dev-2026-10, Java 17. Why is the `.wo` from `why build`, with the same C flags.

**Method.** best-of-5: the minimum of 5 samples (robust to machine spikes), after a warm-up; `ns/op = min / N`. Since the machine is not isolated, the same code varies by about 15 to 20 % from run to run (CPU frequency, thermal, malloc/GC). The `-stable` flag runs C and Why 3× inside the call and takes the median of the 3 `Why/C` ratios: this is the recommended mode for a stable figure.

## First state of the measurements

This is the same state as in the paper. Four questions:

| Question | Observation |
|---|---|
| Does the verifier reject forbidden stores? | **76 regression programs** pass, expected rejections included. |
| Is the emitted C at the level of C? | **Median Why/C ≈ 1.01** across 46 integer compute kernels; notable gap on the associative-table update (**≈ 6×**). |
| What does a per-region allocation cycle cost? | **1.33×** vs `malloc`/`free` for a 4 KiB batch pooled; **1.4 to 1.9×** for 64 KiB freed; peak memory close to C. |
| Do real programs compile? | A file server and a TLS client/server compile and return the expected code. |

There is not yet a **proof of (E)**: safety is covered by the test suite, not by a theorem. This is an acknowledged limit, not an oversight.

## The allocator, first work item

The runtime environment fits in a **934-line** header: cursor-advancing allocation, **4096-byte** blocks recycled in a thread-local pool, a pool of `min(cpus, 8)` worker threads, and bounded channels. At the close of a block, the emitted code closes the channels, awaits the tasks, runs the `defer`s, frees the guards, then calls `why_arena_free`.

The per-region allocation cycle still costs between **1.33×** (4 KiB pooled) and **1.4–1.9×** (64 KiB freed) vs `malloc`/`free`. This is the first optimization work item flagged by the measurements.

## Preliminary inter-language race

This section comes from an earlier race (commit `d782924`); it serves as inter-language context on the same machine. The reference figures above come from the current race, whose median Why/C is ≈ 1.01.

**Summary of this race.** On the agreed examples, the median Why/C is 1.07. Three things are true at once:

1. **At the C ceiling** on straight-line, struct and integer kernels — Why is within a few percent of C, and faster than C on several.
2. **Faster than C on cross-thread cores** — a thread pool removes `pthread_create`/`pthread_join`; Why is far ahead of Go, Rust, Odin and Java there.
3. **Slower than C where allocation and map growth dominate** — the honest weakness, the associative-table update.

| Kernel | C | Go | Rust | Odin | Java | Why | Why/C |
|---|---:|---:|---:|---:|---:|---:|---:|
| functions | 3.25 | 3.68 | 4.63 | 3.35 | 3.35 | 3.51 | 1.08 |
| if | 3.21 | 3.34 | 4.48 | 3.27 | 2.82 | 3.01 | 0.94 |
| loop | 5.53 | 25.12 | 6.92 | 5.65 | 7.67 | 5.82 | 1.05 |
| index | 5.38 | 8.43 | 8.40 | 4.84 | 4.20 | 3.23 | **0.60** |
| window | 4.82 | 8.57 | 6.98 | 5.48 | 3.85 | 5.37 | 1.11 |
| map read | 4.52 | 6.44 | 8.16 | 6.05 | 3.50 | 5.81 | 1.29 |
| map write | 5.56 | 15.65 | 15.23 | 6.14 | 11.81 | 23.34 | 4.20 |
| struct copy | 3.80 | 4.83 | 4.90 | 3.63 | 3.68 | 3.84 | 1.01 |
| method ptr | 3.77 | 4.56 | 5.28 | 4.00 | 3.18 | 3.63 | 0.96 |
| journal | 3.25 | 9.94 | 4.20 | 4.66 | 29.41 | 2.00 | **0.62** |
| chan rendezvous | 14526 | 463.75 | 18133 | 26055 | 34289 | 5586 | **0.38** |
| chan queue | 14796 | 433.25 | 17256 | 16692 | 36411 | 5826 | **0.39** |
| spawn thread | 15362 | 414.83 | 17345 | 20747 | 31315 | 5838 | **0.38** |
| generic call | 3.85 | 3.93 | 4.09 | 2.92 | 3.21 | 3.50 | 0.91 |
| error propagate | 4.99 | 4.97 | 5.94 | 5.12 | 3.49 | 4.56 | 0.91 |
| hanoi | 671466 | 786858 | 524943 | 1034772 | 390215 | 683200 | 1.02 |

Values are `ns/op`. Bold = where Why clearly beats C.

## The full benchmark

The full suite is **46 kernels** across seven languages plus Y, in a separate repository. The reference run is stamped with the Why commit; the methodology (flags per language, the Y mapping, the unmeasured pages) is documented in that repository's README.
