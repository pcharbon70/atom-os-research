---
title: "Executable retirement and quarantine"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Executable retirement and quarantine

Retiring an executable image requires excluding future entry and proving that current execution and retained references no longer depend on it. Waiting a fixed interval or unmapping one address does not establish that result.

## Scope and research question

When can code bytes be reused without invalidating a live instruction, return address or diagnostic reference?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A retirement operation binds the exact image version, executor set, no-new-dispatch gate, mapping references, outstanding publication operations and diagnostic/unwind borrows. The parent ExecutableImage retains its single account and lifetime owner. Runtime cooperation supplies evidence about managed execution only within its declared trusted interface; the kernel does not parse BEAM continuations to guess quiescence.

### Protocol and publication points

RetirementAccepted → commit no-new-dispatch → wait for exact-version execution quiescence while RX remains live → remove RX through restrictive mapping protocol → join translation/fetch, writer, lifecycle and reference predicates → transfer to the reclamation gate. Before the irreversible admission closure, cancellation may restore the documented previous state; afterwards it cannot invent rollback. Missing evidence produces quarantine with retained ownership.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A return address, suspended continuation or stale dispatch table can reenter code after visible call sites were replaced. Relaxed best-effort patching supplies no deadline for old instruction disappearance. Reclamation based only on TLB completion ignores software references and live execution. Quarantine is not automatically recoverable merely because a late acknowledgement arrived.

### Alternatives and tradeoffs

Never reclaiming code avoids reuse races but gives unbounded memory growth. Global execution stopping makes quiescence clearer at a latency cost. Epoch schemes can reduce cost only if every execution and reference source participates in the epoch protocol.

### Cross-architecture realization

Different instruction caches and return mechanisms change the required backend proof, not the obligation to exclude future and current execution. The component 3 reclamation gate remains the final authority for the physical storage it owns.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Hold a suspended execution and diagnostic borrow while retiring its image; reclamation must remain closed.
- Deliver late acknowledgements after cancellation or quarantine and reject cross-generation completion.
- Attempt frame reuse with one unsatisfied execution/reference predicate and require failure.

Complete managed/native continuation coverage and recovery from incomplete retirement remain unproved.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Ordinary-memory synchronization](ordinary-memory-synchronization.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Arm threaded code-publication article](../../../30-sources/bramley-2025-arm-self-modifying-code-threads.md) — Writer-side synchronization does not synchronize every executing core.
- [Concurrency in the Linux kernel](../../../30-sources/alglave-et-al-2018-linux-kernel-concurrency.md) — Executable litmus models and reclamation reasoning.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
