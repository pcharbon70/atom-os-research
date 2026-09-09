---
title: "Split-phase operation and terminal ownership"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - typed-kernel-facing-architecture-facade
aliases: []
---

# Split-phase operation and terminal ownership

Asynchronous acceptance transfers responsibility, not merely control flow. Every accepted operation needs a durable owner and an at-most-once terminal transition, including cancellation and caller failure.

## Scope and research question

How can a facade distinguish rejection, acceptance, cancellation and completion without losing buffers or manufacturing success?

This report refines [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

OperationRecord stores identity, generation, accepted resource set, independent owner, cancellation state and terminal result. Rejection returns caller-owned resources and accepts no effects for this operation. Acceptance retains resources in the ledger. A result union distinguishes Completed, FailedWithRetainedResources, CancelledAfterDrain and Quarantined; names are proposed, while the parent protocol defines the authoritative semantics.

### Protocol and publication points

Validate and reserve → Rejected or Accepted → Pending → effect-specific progress → terminal claim → resource disposition → terminal observation. Cancellation requests closure; it is not completion. Exactly one contender wins terminal ownership. Eventual terminalization additionally requires explicit progress and recovery assumptions; catastrophic failure can prevent delivery even when duplicate completion is excluded.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A callback reporting BUSY for a new request must not be confused with a callback belonging to an earlier accepted operation. Reentrant synchronous callbacks can observe incompletely transferred custody. Dropping a caller or timing out cannot return hardware-owned storage. An error after partial effects is an accepted failure state, not a clean pre-acceptance rejection.

### Alternatives and tradeoffs

Blocking calls hide the state machine but retain it in stacks and scheduler dependencies. Explicit split-phase records make custody and failure visible at a metadata cost. Fire-and-forget operations are suitable only when a separate owner and loss policy are part of the contract.

### Cross-architecture realization

Hardware interrupts, firmware returns and device completion queues all feed the same operation identity discipline but provide different effect evidence. The facade must not upgrade any of them into a stronger completion guarantee.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Race completion, cancellation and caller destruction; one terminal owner must retain or return every resource.
- Reject a second request while an earlier one remains active; its later callback must still identify only the earlier operation.
- Inject failure after hardware acceptance but before callback publication; the ledger must preserve effect uncertainty and custody.

At-most-once safety is specified; crash recovery and eventual completion remain unproved and may require system-terminal outcomes.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Feature profiles and backend binding](feature-profiles-and-backend-binding.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Tock HIL design](../../../30-sources/tock-project-2026-hil-design.md) — Submission, returned ownership and asynchronous completion contracts.
- [Tock deployment retrospective](../../../30-sources/schuermann-et-al-2025-tock-decade.md) — Typed interfaces still require sound ABI and runtime validation.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
