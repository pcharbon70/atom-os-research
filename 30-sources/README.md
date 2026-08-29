---
title: "Sources"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Sources index"
---

# Sources (`30-sources`)

## Purpose

Source notes preserve bibliographic provenance and evidence-focused reading
notes separately from the archive's synthesis.

## What belongs here

Create one note for each substantively used paper, book, specification,
official documentation set, codebase revision, talk, dataset, or other primary
work. Incidental mentions can remain citations in the document using them.

## Index

### Subdirectories

- None yet.

### Documents

- [Making reliable distributed systems in the presence of software errors](armstrong-2003-making-reliable-distributed-systems.md) —
  develops the original isolation, failure-detection, supervision, upgrade,
  and stable-storage argument.
- [A History of Erlang](armstrong-2007-history-of-erlang.md) — records the
  concurrency model's origin and candid lessons about isolation, foreign code,
  atoms, protocols, and distributed security.
- [AtomVM source tree at `0220c78e`](atomvm-project-2026-source-tree.md) — pins and audits the current
  runtime, platform seam, MCU entry points, native trust boundary, and build
  attempt.
- [AtomVM main documentation](atomvm-project-2026-main-documentation.md) —
  records the development documentation's process, memory, scheduling,
  execution, distribution, platform, and compatibility model.
- [Announcing AtomVM v0.7.0-alpha.0](atomvm-project-2026-v0-7-alpha0.md) — captures the official
  prerelease feature and stability boundary after the v0.6 line.
- [What's on your mind for AtomVM v0.7?](atomvm-community-2025-v0-7-priorities.md) — preserves a dated
  community view of performance, tooling, network, peripheral, power, and
  flash-layout priorities.
- [Functional Programming for the Internet of Things](branch-weinstock-2024-functional-programming-iot.md) — summarizes a
  2024 AtomVM/Elixir versus C++ LoRa–MQTT gateway comparison and its
  reproducibility limits.
- [Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems](ferenczi-ruda-toth-2025-evaluating-atomvm.md) — records
  abstract-level evidence about redundant hardware and remote-node monitoring.
- [Measuring Erlang-Based Scalability and Fault Tolerance on the Edge](ferenczi-ruda-toth-2025-measuring-erlang-scalability.md) — records
  open-access process, supervision, mailbox, LoRa, memory, and power
  measurements on ESP32-S3.
- [Erlang/OTP 29.0.5 system documentation](erlang-otp-team-2026-otp-29-documentation.md) —
  records current process, signal, scheduler, memory, code-loading,
  supervision, release, distribution, and security contracts.
- [Erlang/OTP source tree at 5cf5f9725452](erlang-otp-team-2026-otp-29-source-tree.md) —
  pins and audits current ERTS internals, constants, code publication, native
  boundaries, and host-OS dependencies.
- [The Road to the JIT](gustavsson-2020-road-to-the-jit.md) — traces Erlang
  execution engines and the whole-system trade-offs behind BeamAsm.
- [A brief introduction to BEAM](hogberg-2020-brief-introduction-to-beam.md) —
  establishes the official distinction between BEAM instructions and ERTS
  runtime facilities.
- [Efficient memory management for concurrent programs that use message passing](sagonas-wilhelmsson-2006-efficient-memory-management.md) —
  compares local, communal, and hybrid heaps and evaluates incremental
  collection trade-offs.
- [The BEAM Book](stenman-2025-beam-book.md) — provides a detailed secondary
  guide to compiler and ERTS internals, used with current primary checks.
- [Scaling Reliably](trinder-et-al-2017-scaling-reliably.md) — evaluates VM and
  distributed-actor scaling and shows the costs of global topology,
  namespaces, and recovery data.
- [Characterizing the scalability of Erlang VM on many-core processors](zhang-2011-erlang-vm-many-core-scalability.md) —
  provides historical evidence about hidden runtime synchronization beneath a
  share-nothing programming model.

## Maintaining this index

Index every direct source note with a concise description. Preserve exact
metadata where available, never invent unknown fields, and link derived work.
