---
title: "AtomVM main documentation"
kind: source
created: "2026-08-28"
authors:
  - "AtomVM contributors"
published: null
citation_key: "atomvm-docs-main-0220c78e"
container: "AtomVM documentation"
edition: "0.8.0-dev+git.0220c78e"
isbn: null
doi: null
url: "https://doc.atomvm.org/main/index.html"
accessed: "2026-08-28"
tags:
  - atom-vm
  - beam
  - embedded-systems
  - memory-management
  - scheduling
  - virtual-machines
aliases:
  - "AtomVM 0.8 development documentation"
---

# AtomVM main documentation

## Reference

AtomVM contributors. *AtomVM documentation*, development edition
`0.8.0-dev+git.0220c78e`. [Canonical documentation
index](https://doc.atomvm.org/main/index.html). Accessed 2026-08-28.

This reading used the documentation source at the same revision as the local
source-tree audit. The principal pages were [Welcome to
AtomVM](https://doc.atomvm.org/main/welcome-to-atomvm.html), [AtomVM
Internals](https://doc.atomvm.org/main/atomvm-internals.html), [Memory
Management](https://doc.atomvm.org/main/memory-management.html), [Differences
with BEAM](https://doc.atomvm.org/main/differences-with-beam.html), [Distributed
Erlang](https://doc.atomvm.org/main/distributed-erlang.html), [Build
Instructions](https://doc.atomvm.org/main/build-instructions.html), [Programmers
Guide](https://doc.atomvm.org/main/programmers-guide.html), and [Stubbed
Functions](https://doc.atomvm.org/main/stubbed-functions.html).

## Research question or contribution

The corpus explains AtomVM's intended scope, internal process and memory model,
scheduler, JIT/native modes, supported platforms and peripherals, packaging,
distribution, and deliberate differences from BEAM. For this archive, the
central question is which services the VM owns and which still come from a
host, runtime system, vendor SDK, or platform port.

## Method

The relevant pages were read against their Markdown sources in a shallow clone
of the official repository at `0220c78e`. Claims about implementation boundaries
were cross-checked against `GlobalContext`, `sys.h`, `smp.h`, the scheduler, and
platform entry points in the companion [source-tree
note](atomvm-project-2026-source-tree.md).

## Findings

- AtomVM implements 170-plus BEAM instructions, but the official BEAM
  implementation is its behavioral reference because there is no standalone
  formal BEAM instruction specification.
- The VM owns BEAM loading and execution, Erlang-process lifecycle and message
  passing, per-process memory, pre-emptive scheduling, NIFs/ports, and the
  interface to a host OS "or facsimile."
- Each process uses a single allocated heap/stack block that starts at eight
  words. The default bounded-free growth policy keeps 16–32 free terms. Messages
  are copied into mailbox fragments. Binaries at least 64 bytes are normally
  reference-counted off-heap.
- SMP builds run one scheduler per core, started on demand. The scheduler runs
  a ready process until it waits or exhausts reductions, and uses
  `sys_poll_events` to integrate driver events and idle waiting.
- Four execution modes are described: emulated, JIT, native/AOT, and hybrid.
  The JIT compiler is written in Erlang. Current backends cover x86-64,
  AArch64, ARM32, ARMv6-M/Thumb-2, RV32, and RV64; the Pico port can cache
  generated code in flash.
- AtomVM is intentionally not a full OTP environment. It has a limited
  standard library, 256-bit integer ceiling, restricted non-byte-aligned bit
  syntax, no code reloading, incomplete OTP behaviors, no dirty schedulers,
  and compatibility stubs that may return fixed values.
- Distribution supports TCP/IP on networked platforms and serial/USB CDC
  carriers, with message passing, process monitoring, I/O/group-leader
  support, and some RPC interoperability. It is explicitly described as very
  partial; cookie authentication exists, but distribution over TLS does not.
- The ESP32 build uses ESP-IDF/FreeRTOS and an IDF-built bootloader; the
  documentation explicitly says AtomVM does not define its own ESP32
  bootloader. RP2 and STM32 use their vendor SDK/HAL arrangements.
- ESP32 persistence includes NVS, partitions, and mounted FAT storage. NVS is
  documented as plaintext. The programmers guide says AtomVM currently has no
  OTA update support.

## Relevance

The documentation shows that AtomVM already contains a scheduler, managed
process model, event loop, memory manager, module loader, and driver boundary.
It also prevents category errors: these facilities do not by themselves
provide early boot, hardware privilege, protected address spaces, durable
update/recovery, or a portable storage and device-management policy.

## Limits

This is development documentation for an unstable branch, not the stable
v0.6.6 contract. Some pages describe experimental features, and the main
branch can change after the pinned revision. Documentation also cannot prove
latency, memory bounds, fault containment, or hardware behavior. Those require
source inspection and reproducible target experiments.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [Kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
- [2026-08-28 source audit](../50-journal/2026-08-28-atomvm-deep-dive.md)
