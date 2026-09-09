---
title: "CPU identity, incarnation and membership"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - logical-cpu-coordination-and-lifecycle
aliases: []
---

# CPU identity, incarnation and membership

A logical CPU is a durable identity whose execution incarnations have separate authority. Membership is a coherent publication, not a collection of independently updated flags.

## Scope and research question

How can remote protocols distinguish a currently participating CPU from a restarted execution agent with the same hardware identifier?

This report refines [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

The lifecycle owner maintains CpuId, hardware identity, Incarnation and an immutable MembershipSnapshot. Publish present, online, requestable, scheduling-eligible and interrupt-target sets together with one generation. Requestable is a subset of online, which is a subset of present; other eligibility sets also require online membership. Consumers hold a lifetime-protected snapshot view, not a bare pointer whose generation might later be checked.

### Protocol and publication points

Discover identity → register PresentOffline → allocate a fresh incarnation before preparation → publish successive admitted membership views → remove eligibility during drain → retire old views after readers leave. Every request and acknowledgement binds the incarnation observed at admission. An old acknowledgement never discharges work sent to a replacement incarnation.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An atomic generation does not make several mutable bitsets a coherent snapshot. Snapshot consistency does not keep its storage alive. Identifier wrap and reused mailbox storage can create an ABA error unless reuse is delayed or exhaustion fails closed. Hardware IDs remain routing facts, not security capabilities.

### Alternatives and tradeoffs

One global lock simplifies membership proofs but can obstruct hard-path readers. Immutable snapshots with explicit read-side lifetime protection reduce reader contention at a measurable memory and reclamation cost. Independent atomic flags are insufficient for clients requiring a set-wide invariant.

### Cross-architecture realization

APIC identifiers, Arm affinity values and RISC-V hart IDs have different widths and routing meanings. None supplies the kernel's incarnation or membership generation. Firmware present-state evidence must not be normalized into online execution.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Race membership reads with admission and drain; every returned set must satisfy the subset invariants.
- Replay an old acknowledgement after a CPU restarts at the same hardware ID; no current request may complete.
- Hold a reader across repeated snapshot replacement; reclamation must retain its storage.

Generation exhaustion, reader stalls and the formal linearization point of a multi-set membership change need explicit proofs.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Secondary preparation and admission](secondary-preparation-and-admission.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [Sequence counters and sequential locks](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — Reader consistency does not establish pointer lifetime or bounded progress.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
