---
title: "AtomVM source tree at 0220c78e"
kind: source
created: "2026-08-28"
authors:
  - "AtomVM contributors"
published: "2026-07-13"
citation_key: "atomvm-source-0220c78e"
container: "GitHub"
edition: "Git revision 0220c78ee9e7cf6c763a278b44d81ce309fcf1ab"
isbn: null
doi: null
url: "https://github.com/atomvm/AtomVM/tree/0220c78ee9e7cf6c763a278b44d81ce309fcf1ab"
accessed: "2026-08-28"
tags:
  - atom-vm
  - beam
  - embedded-systems
  - repository-audit
  - systems-architecture
  - virtual-machines
aliases:
  - "AtomVM repository audit"
---

# AtomVM source tree at 0220c78e

## Reference

AtomVM contributors. *AtomVM* source tree, revision
[`0220c78ee9e7cf6c763a278b44d81ce309fcf1ab`](https://github.com/atomvm/AtomVM/commit/0220c78ee9e7cf6c763a278b44d81ce309fcf1ab),
authored 2026-07-13. Accessed 2026-08-28.

The root repository is Apache-2.0, while the inspected core source headers
generally declare `Apache-2.0 OR LGPL-2.1-or-later`; `unicode.c` also includes
MIT terms. A derivative must preserve the applicable file-level SPDX terms
rather than relying only on GitHub's repository-level license label.

## Research question or contribution

The audit asks what AtomVM actually owns at runtime, what a platform must
provide, and whether any current MCU port already runs without a conventional
host OS.

## Method

A shallow clone of the official `main` branch was pinned to the full revision.
The review covered:

- `src/libAtomVM/globalcontext.h`, `scheduler.c`, `scheduler.h`, `sys.h`,
  `smp.h`, `memory.*`, `mailbox.*`, and `CMakeLists.txt`;
- platform entry points and system implementations for `generic_unix`, ESP32,
  STM32, RP2, and Emscripten;
- core and platform library layout, source file counts, version metadata, and
  the current changelog; and
- a release-mode generic-Unix CMake configuration and build attempt.

The commands and environment are recorded in the [journal
entry](../50-journal/2026-08-28-atomvm-deep-dive.md).

## Findings

- `GlobalContext` roots ready/running/waiting process lists, the process and
  registered-name tables, atoms, modules, reference-counted binaries,
  listeners, select events, timers, ETS, distribution connections, scheduler
  state, and opaque platform data.
- `scheduler.c` selects a ready `Context`, integrates timer expiry and
  `sys_poll_events`, and coordinates scheduler threads. The inspected default
  reduction quantum is 1,024.
- `sys.h` defines the most visible platform seam: event poll/signal and select
  registration, time, module/AVM loading, port creation, platform init/free,
  system information, and JIT/native-code mapping and caching.
- `smp.h` requires mutexes, condition variables, read/write locks, atomics or
  platform substitutes, processor discovery, scheduler start/join, and
  main-thread identification.
- ESP32 enters through `app_main` as an ESP-IDF/FreeRTOS application. STM32
  calls `HAL_Init`, maps the application from flash, constructs a
  `GlobalContext`, and calls `globalcontext_run` directly. RP2 similarly enters
  from a Pico SDK `main`, maps library/application AVM regions from flash, and
  runs the VM. Removing a conventional OS is therefore not the same task as
  removing all vendor runtime, HAL, libc, allocator, startup, and boot
  dependencies.
- Ordinary BEAM processes share one native address space and one
  `GlobalContext`. Their heaps are independently collected but are native
  allocations, not protected address spaces. The search found no documented
  MPU/PMP, privilege, capability, or sandbox layer in the inspected core and
  MCU ports.
- Native ports and NIFs are part of the same executable and scheduling
  environment. A native memory fault or blocking call is outside ordinary
  Erlang-process fault isolation.
- The tracked tree contains substantial implementation and test material: 132
  C files, 97 headers, 806 Erlang files, and 82 Elixir files. The direct
  `src/libAtomVM` C/header set is about 63,731 lines, current platform-native
  source about 36,192 lines, and `libs` Erlang/Elixir about 85,195 lines. These
  are orientation counts, not maintainability or trusted-computing-base
  metrics; generated/large interpreter code and optional features affect them.
- `version.cmake` identifies the revision as `0.8.0-dev`; the changelog's top
  section is an unreleased v0.7.0-beta.0. Upstream's README still recommends
  stable v0.6.x for stability-sensitive use.

## Relevance

The source supports the execution-nucleus hypothesis and narrows the first
design task. AtomVM already runs directly over vendor MCU support on STM32 and
RP2. A new OS does not need to invent the actor runtime, scheduler, or managed
heap, but it must make the entire substrate and native trust boundary explicit.

## Limits

This was a static audit without target hardware. CMake configuration succeeded,
but compilation stopped because the host lacked `gperf` and its ASDF shims had
no selected Erlang/rebar versions. No executable, benchmark, simulator result,
binary-size result, interrupt trace, or fault injection was produced. Absence
of protection-related terms in a targeted search is not a formal proof that no
optional vendor mechanism can be configured downstream.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [Kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
- [2026-08-28 source audit](../50-journal/2026-08-28-atomvm-deep-dive.md)
