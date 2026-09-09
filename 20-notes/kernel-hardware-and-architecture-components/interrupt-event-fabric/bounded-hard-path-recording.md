---
title: "Bounded hard-path recording"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - interrupt-event-fabric
aliases: []
---

# Bounded hard-path recording

The hard path should record bounded, generation-tagged evidence that work is pending. It should not promise one message for every physical event or invoke the ordinary driver inline.

## Scope and research question

How does the system preserve useful event state when receivers are slow, failed or out of capacity?

This report refines [component 5: Interrupt event fabric](../interrupt-event-fabric.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Preallocate per-binding records, saturating counters or sticky flags, destination references and a bounded debit plan. Delivery semantics are declared as coalescing, counted-with-saturation or another explicitly supported profile. EventSink notification is a hint to inspect retained state. Hard-path storage and deferred borrows remain pinned to the IRQBinding lifetime.

### Protocol and publication points

Capture current binding → perform allowed flow stabilization → update retained event state → attempt bounded notification → return. Receiver consumption uses an atomic handoff that preserves an event racing the clear. Overflow updates a bounded loss/storm record and independent management path; it does not allocate more storage or spin until a queue accepts work.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A sink enqueue failure can strand work unless pending state survives. A Boolean clear can erase a concurrent arrival. Saturated counts cannot be interpreted as exact occurrence totals. Diagnostic formatting and runtime callbacks can destroy the hard path's stack/time bounds. NMI-like events require a stricter path than ordinary maskable IRQs.

### Alternatives and tradeoffs

One queued record per occurrence is simple until overload. Coalescing bounds memory but makes device inspection essential. A counting profile preserves more information only when hardware and overflow semantics justify its meaning.

### Cross-architecture realization

Controller event aggregation may happen before software observes an interrupt. Normalization cannot recover events the hardware did not distinguish. Kernel IPIs carry subsystem request identity through component 7; this recorder does not make transport arrival into semantic completion.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Fill the sink, kill the receiver and saturate counters while preserving pollable pending evidence.
- Inject an event during every consume/clear cut and verify no silent loss beyond the declared profile.
- Measure static call/stack bounds separately from hardware response latency; reject hidden allocation and waits.

The exact receiver handoff algorithm and worst-case hard-path budgets remain to be verified.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Binding, routing and teardown](binding-routing-and-teardown.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [Linux NAPI](../../../30-sources/linux-kernel-community-2026-napi-contracts.md) — Budgeted processing and explicit masking/ownership handoff.
- [Tock HIL design](../../../30-sources/tock-project-2026-hil-design.md) — Submission, returned ownership and asynchronous completion contracts.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
