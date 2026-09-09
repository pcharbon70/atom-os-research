---
title: "Bounded cross-CPU request fabric"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - logical-cpu-coordination-and-lifecycle
aliases: []
---

# Bounded cross-CPU request fabric

Remote work should use closed request kinds, bounded storage and incarnation-bound completion records. A notification says work may be available; it does not itself prove that the requested effect happened.

## Scope and research question

How can translation, code-publication and lifecycle clients request remote effects without ambiguous completion or unbounded privileged work?

This report refines [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Request records contain operation ID, request kind, immutable target-incarnation set, payload custody and required completion predicate. Track admitted, executed and acknowledged target sets separately. Per-CPU mailboxes have fixed capacity and an explicit admission policy. Dispatch invokes only registered bounded handlers; arbitrary callbacks would destroy the context and resource contract.

### Protocol and publication points

Validate context and targets → reserve all required request storage or reject → publish immutable work → notify → execute on each admitted target → publish scoped acknowledgements → join exact required sets → terminalize. Duplicate notifications are harmless; duplicate execution is permitted only for explicitly idempotent operations. Cancellation requests closure but cannot invent acknowledgements.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A sender waiting while holding a lock needed by a remote handler deadlocks the system. Saturation must reject before acceptance or retain an independently owned pending operation, never drop accepted work. A target disappearing from a newer online set does not discharge its old obligation. Timeouts report uncertainty, not remote completion.

### Alternatives and tradeoffs

Shared bitmaps are compact for idempotent work but can merge distinct generations incorrectly. Per-request messages preserve identity at higher storage cost. A hybrid needs a proof that coalescing retains every required completion predicate.

### Cross-architecture realization

An IPI, SGI or firmware remote-operation call has its own delivery and completion contract. In particular, successful notification submission is not automatically the same as instruction synchronization or translation quiescence. The adapter must expose the exact stronger semantics it can establish.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Fill every mailbox and inject duplicates and reordered notifications; accepted operation ownership must remain conserved.
- Stop and restart a target between publication and acknowledgement; its stale response must not satisfy a new incarnation.
- Exercise cycles of remote requests with lock-order instrumentation; no handler may depend on a waiting sender's lock.

Bounded progress requires assumptions about target responsiveness, interrupt admissibility and recovery capacity; none has been demonstrated for the proposed fabric.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [CPU drain, stop and reclamation](drain-stop-and-reclamation.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [RISC-V SBI](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
