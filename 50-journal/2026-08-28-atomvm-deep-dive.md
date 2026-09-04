---
title: "2026-08-28 AtomVM deep dive"
kind: journal
created: "2026-08-28"
tags:
  - atom-vm
  - literature-search
  - repository-audit
  - research-session
aliases:
  - "AtomVM source and literature audit"
---

# 2026-08-28 AtomVM deep dive

## Observations

- AtomVM is already structured as a portable managed runtime with a narrow
  platform event/scheduling seam, and its STM32 and RP2 entry points do not
  require a conventional host OS.
- "No host OS" does not mean "no substrate": current MCU builds still use
  vendor boot paths, SDK/HAL code, C-library behavior, an allocator, linker
  layout, interrupts, and native drivers.
- The main architectural risk is the difference between Erlang-process
  isolation and native protection. All processes and native extensions occupy
  one VM/native address space at the inspected revision.
- Published measurements support microcontroller-scale concurrency but expose
  mailbox, allocator, driver, and watchdog failure surfaces.
- Source evolution is fast enough that literature must be interpreted by
  revision. Several 2024–2025 missing features are present in the 2026
  development tree.

## Environment

- Host: Linux Mint `22.1 (Xia)` on the Ubuntu `noble` base, Linux
  `6.8.0-51-generic`, x86-64.
- C compiler: GCC `13.3.0`.
- CMake: `3.28.3`.
- Git: `2.49.0`.
- Python: `3.12.12`.
- `jq` was available.
- Erlang, `erlc`, and `rebar3` resolved to ASDF shims, but no project/global
  versions were selected for the clone.
- `gperf` was absent. Mbed TLS, Gleam, Sphinx, and Graphviz were also not found
  by CMake; Mbed TLS and the documentation tools were optional for the attempted
  target.
- No MCU, radio, power meter, or simulator was used.

## Evidence

### Official source acquisition

The official repository was cloned shallowly and pinned:

```bash
git clone --depth=1 https://github.com/atomvm/AtomVM.git
git -C AtomVM rev-parse HEAD
git -C AtomVM log -1 --format='%H%n%aI%n%an%n%s'
```

Result:

```text
0220c78ee9e7cf6c763a278b44d81ce309fcf1ab
2026-07-13T19:53:07+02:00
Davide Bettio
Merge pull request #2356 from petermm/fix-globalcontext-leaks
```

`git ls-remote` returned the same `main` revision on 2026-08-28.
`version.cmake` reported `0.8.0-dev`; the top changelog section was
`0.7.0-beta.0 - Unreleased`.

Orientation counts:

```bash
git ls-files 'src/libAtomVM/*.c' 'src/libAtomVM/*.h' | xargs wc -l
git ls-files 'src/platforms/generic_unix/**' 'src/platforms/esp32/**' \
  'src/platforms/stm32/**' 'src/platforms/rp2/**' \
  'src/platforms/emscripten/**' | rg '\.(c|h|cpp|S|s)$' | xargs wc -l
git ls-files 'libs/**/*.erl' 'libs/**/*.ex' | xargs wc -l
```

Totals were about 63,731 core C/header lines, 36,192 selected platform-native
lines, and 85,195 library Erlang/Elixir lines. The tracked extension counts
included 806 `.erl`, 132 `.c`, 97 `.h`, and 82 `.ex` files. These counts include
large generated-style interpreter code and optional features; they are not a
trusted-computing-base measurement.

### Static architecture audit

Files inspected directly included:

```text
src/libAtomVM/globalcontext.h
src/libAtomVM/scheduler.c
src/libAtomVM/scheduler.h
src/libAtomVM/sys.h
src/libAtomVM/smp.h
src/libAtomVM/CMakeLists.txt
src/platforms/esp32/main/main.c
src/platforms/stm32/src/main.c
src/platforms/rp2/src/main.c
doc/src/atomvm-internals.md
doc/src/memory-management.md
doc/src/differences-with-beam.md
doc/src/distributed-erlang.md
doc/src/build-instructions.md
doc/src/programmers-guide.md
doc/src/stubbed-functions.md
CHANGELOG.md
version.cmake
```

Targeted searches looked for bootloader ownership, OTA/update and persistence,
MPU/PMP or privilege terms, capabilities/sandboxing, allocator and memory
layout, scheduling reductions, driver/event integration, distribution
security, and platform startup. No documented core/MCU protection layer was
found. This negative search is scoped to the pinned tree and is not proof about
all downstream vendor configurations.

### Generic-Unix build attempt

```bash
cmake -S AtomVM -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel 4
```

CMake configured successfully and detected the host's POSIX facilities,
threads, atomics, and zlib. Compilation then stopped before producing AtomVM:

```text
/bin/sh: 1: gperf: not found
No version is set for command erlc
No version is set for command rebar3
```

This is a host-prerequisite failure. It says nothing about the correctness or
buildability of AtomVM in its documented environment. No packages or tool
versions were installed during this pass.

### Release-state check

The official GitHub releases API showed:

```text
v0.7.0-alpha.1  prerelease  2026-04-06
v0.7.0-alpha.0  prerelease  2026-03-20
v0.6.6          stable      2025-06-23
```

The stable, prerelease, and development baselines were kept separate in the
synthesis.

### Literature and web search

Searches covered the official site, documentation, repository, release notes,
Crossref, scholarly indexes, research-paper text, articles, blogs, GitHub
issues/discussions, Erlang Forums, and Reddit. Search concepts combined
`AtomVM` with architecture, BEAM, ESP32, STM32, RP2/Pico, performance,
scalability, memory, fault tolerance, LoRa, bare metal, operating system,
isolation, drivers, and community experience.

Sources promoted because they materially affected the synthesis:

- [AtomVM main documentation](../30-sources/atomvm-project-2026-main-documentation.md)
- [AtomVM source tree](../30-sources/atomvm-project-2026-source-tree.md)
- [Official v0.7 alpha blog post](../30-sources/atomvm-project-2026-v0-7-alpha0.md)
- [Ferenczi, Ruda, and Tóth's open-access 2025 Sensors paper](../30-sources/ferenczi-ruda-toth-2025-measuring-erlang-scalability.md)
- [Branch and Weinstock's 2024 Electronics paper](../30-sources/branch-weinstock-2024-functional-programming-iot.md)
- [Ferenczi, Ruda, and Tóth's Erlang '25 paper](../30-sources/ferenczi-ruda-toth-2025-evaluating-atomvm.md),
  limited here to abstract-level claims
- [The v0.7 GitHub planning discussion](../30-sources/atomvm-community-2025-v0-7-priorities.md)

Contextual sources screened but not used as independent proof included:

- the Elixir project's 2025 [interoperability and portability
  article](https://elixir-lang.org/blog/2025/08/18/interop-and-portability/),
  which recognizes AtomVM as a constrained-runtime portability target;
- a 2025 Alembic Labs [practitioner
  post](https://alembiclabs.fr/en/blog/iot-monitoring-elixir-atomvm-esp32),
  whose production-readiness and development-time claims lack a pinned public
  artifact or measurement method;
- [Erlang Forums](https://erlangforums.com/tag/atomvm) setup and hardware
  threads, useful for onboarding friction but not architecture evidence;
- the Reddit [ElixirConf EU AtomVM
  thread](https://www.reddit.com/r/elixir/comments/1jo2xnn/atomvm_new_horizons_for_elixir_elixirconf_eu/),
  containing anecdotal maintainer/user comments about missing pieces; and
- the open draft [Zephyr port](https://github.com/atomvm/AtomVM/pull/958),
  which demonstrates interest in another RTOS substrate but is not merged
  platform support.

The full open-access Sensors paper was read through its NCBI/PMC text and its
data link, not through search snippets. The Branch/Weinstock PDF was downloaded
from MDPI and converted locally to text for review. Crossref supplied DOI,
author, venue, and publication metadata. The ACM paper note is deliberately
limited because only authoritative metadata and the abstract were reviewed.

## Source manifest

This is the authoritative session-level provenance list. “Newly introduced”
means that the source note first entered the archive during this deep dive;
“reused” means that an existing source note substantively informed the work.

### Newly introduced sources

- [AtomVM main documentation](../30-sources/atomvm-project-2026-main-documentation.md) — established the documented runtime, platform, execution, distribution, and compatibility surface.
- [AtomVM source tree at `0220c78e`](../30-sources/atomvm-project-2026-source-tree.md) — supplied the pinned implementation and platform-boundary audit.
- [AtomVM v0.7.0-alpha.0 announcement](../30-sources/atomvm-project-2026-v0-7-alpha0.md) — bounded prerelease maturity and post-v0.6 feature evolution.
- [Ferenczi, Ruda, and Tóth, Measuring Erlang-Based Scalability and Fault Tolerance on the Edge](../30-sources/ferenczi-ruda-toth-2025-measuring-erlang-scalability.md) — supplied ESP32-S3 process, supervision, mailbox, memory, LoRa, and power measurements.
- [Branch and Weinstock, Functional Programming for the Internet of Things](../30-sources/branch-weinstock-2024-functional-programming-iot.md) — supplied a workload-specific AtomVM/Elixir and C++ LoRa–MQTT comparison.
- [Ferenczi, Ruda, and Tóth, Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems](../30-sources/ferenczi-ruda-toth-2025-evaluating-atomvm.md) — supplied abstract-level evidence about remote monitoring and redundant-node recovery directions.
- [AtomVM community, What's on your mind for AtomVM v0.7?](../30-sources/atomvm-community-2025-v0-7-priorities.md) — supplied a dated community agenda for performance, tooling, networking, power, and storage work.

### Reused sources

- None.

## Threads

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
  is the durable synthesis from this session.
- [The operational inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
  needs a successful pinned build and MCU/simulator trace next.
- [The AtomVM foundation map](../10-maps/atomvm-foundation.md) organizes the
  evidence by architecture, measurement, and project evolution.

## Follow-ups

- Select explicit ASDF Erlang/rebar versions, install `gperf`, and reproduce the
  generic-Unix build without changing the upstream source.
- Choose an STM32 or RP2 board/simulator and record reset-to-first-BEAM
  dependencies, link map, image size, boot time, and idle memory.
- Read the complete Erlang '25 paper before citing its methods or results.
- Reproduce process, mailbox, and driver-pressure measurements on pinned v0.6,
  v0.7 prerelease, and main baselines.
- Audit allocator/OOM paths and native fault containment before designing the
  service or capability API.
