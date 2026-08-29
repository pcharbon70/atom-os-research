---
title: "AtomVM foundation"
kind: map
created: "2026-08-28"
tags:
  - atom-vm
  - beam
  - embedded-systems
  - operating-systems
  - systems-architecture
  - zig
aliases:
  - "AtomVM research map"
---

# AtomVM foundation

## Scope

This map covers AtomVM as the prospective execution nucleus of a new embedded
operating system: what the runtime already owns, what its platform ports and
vendor SDKs currently supply, what empirical work says about its limits, and
which system responsibilities still need design and experimental evidence.

It is a concrete implementation case within the broader [BEAM, ERTS, and OTP
research](beam-erts-and-otp.md), not the repository's prescribed foundation.
Under the project-wide [language
decision](../20-notes/zig-as-the-kernel-implementation-language.md), any new
kernel or substrate built around this case is Zig; AtomVM's existing C core is
an imported runtime boundary.

## Start here

- [BEAM, ERTS, and OTP](beam-erts-and-otp.md) provides the principle-first
  context and alternative implementation strategies against which AtomVM
  should be compared.
- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
  gives the current synthesis and proposed system boundary.
- [Can AtomVM serve as the kernel-facing runtime of a new embedded operating
  system?](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
  turns that assessment into falsifiable criteria and experiments.
- [The 2026-08-28 source audit](../50-journal/2026-08-28-atomvm-deep-dive.md)
  pins the inspected revision, commands, search paths, and failed local build
  attempt.

## Trails

### Runtime and platform boundary

- [AtomVM main documentation](../30-sources/atomvm-project-2026-main-documentation.md)
  describes processes, scheduling, memory, execution modes, distribution, and
  documented compatibility limits.
- [AtomVM source tree at `0220c78e`](../30-sources/atomvm-project-2026-source-tree.md)
  checks those descriptions against `libAtomVM`, `sys.h`, `smp.h`, and the
  ESP32, STM32, and RP2 entry points.
- [AtomVM v0.7.0-alpha.0 announcement](../30-sources/atomvm-project-2026-v0-7-alpha0.md)
  captures the project's prerelease maturity boundary and the major features
  added after v0.6.

### Measured behavior

- [Ferenczi, Ruda, and Tóth (2025)](../30-sources/ferenczi-ruda-toth-2025-measuring-erlang-scalability.md)
  measures process counts, supervision overhead, mailbox overload, LoRa
  behavior, memory, and current draw on an ESP32-S3.
- [Branch and Weinstock (2024)](../30-sources/branch-weinstock-2024-functional-programming-iot.md)
  compares AtomVM/Elixir and C++ LoRa–MQTT gateways and reports a driver- and
  workload-sensitive performance gap.
- [Ferenczi, Ruda, and Tóth's Erlang '25 paper](../30-sources/ferenczi-ruda-toth-2025-evaluating-atomvm.md)
  frames remote-node monitoring and redundant hardware as the next
  fault-tolerance question; only abstract-level findings have been captured.

### Project and community priorities

- [The v0.7 priorities discussion](../30-sources/atomvm-community-2025-v0-7-priorities.md)
  records community concerns about call overhead, tooling, supervisor support,
  networking, GPIO consistency, power management, and flash layout. It is a
  dated agenda, not a current feature checklist.

## Open questions

- What is the smallest explicit Zig substrate beneath `libAtomVM` that can
  replace implicit libc, allocator, boot, interrupt, timer, and vendor-SDK
  services?
- Should the first system promise only single-tenant firmware isolation, or
  must it provide MPU/PMP-backed protection between applications and native
  drivers?
- Can driver faults and mailbox overload be contained without converting a
  managed process failure into a whole-VM reset?
- Which platform is the best reference target for the first experiment:
  STM32, RP2, or a hosted simulator that exposes every dependency?
- What boot, update, rollback, persistence, observability, and recovery
  contracts are required before the result deserves to be called an operating
  system rather than an application runtime?
