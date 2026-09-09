---
title: "Frame normalization and bounded dispatch"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - privileged-entry-exit-and-execution-context
aliases: []
---

# Frame normalization and bounded dispatch

The normalized entry frame should preserve origin and validity without making captured bytes into return authority. Dispatch begins only after entry state is coherent and stays separate from scheduling and device policy.

## Scope and research question

How can common handlers consume architecture-neutral evidence without losing raw information or trusting user-controlled return fields?

This report refines [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

EntryFrame is a tagged sum of UserCall, UserFault, ExternalInterrupt, KernelFault, NmiLike, MachineFault and RecursiveFatal views. Common fields include CPU/context incarnations, entry class, valid register subsets and a raw-record reference with bounded lifetime. Architecture-specific syndrome values retain namespace and validity. A UserReturnEnvelope is a separate validated product, not a cast of EntryFrame.

### Protocol and publication points

RawCaptured → OriginEstablished → ShapeValidated → Normalized → BoundedDispatch or DeferredOwnershipTransfer. A synchronous call can pass copied arguments to the capability boundary; an interrupt records a bounded event and delegates controller flow to component 5. A kernel fault enters only an explicitly declared recovery region or component 9. Deferred users must own copied evidence or an accounted borrow before entry storage can recycle.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Uniform zero-filled fields can conflate unavailable syndrome data with an observed zero. A debug exception's safe handling can depend on its origin, not just its vector. Dispatching a driver or runtime callback on the raw stack imports uncontrolled blocking, allocation and reentry. Raw user pointers are not validated control snapshots.

### Alternatives and tradeoffs

One universal flat frame simplifies handler signatures but encourages interpreting nonexistent fields. Separate architecture structs preserve detail but leak backend dependencies. A common tagged header plus bounded raw extension provides a reviewable middle ground.

### Cross-architecture realization

Frame normalization must distinguish hardware-saved and software-saved state and preserve ISA-specific syndrome semantics. It need not make all event classes available on every backend. Unsupported classes are explicit profile exclusions rather than empty handlers.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Feed every raw-frame variant and verify lossless origin/validity tagging.
- Attempt to manufacture a return envelope from a raw capture; require independent checks.
- Exhaust deferred-event capacity and verify bounded evidence/loss behavior without dropping stack ownership.

Normalized schema versioning and complete raw-to-semantic refinement require executable tests.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Validated less-privileged return](validated-user-return.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux entry/exit handling](../../../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — Ordering and instrumentation restrictions in partial entry states.
- [AArch64 Exception Model](../../../30-sources/arm-2025-aarch64-exception-model.md) — Hardware exception capture is only part of software context preservation.
- [Flux OSKit](../../../30-sources/ford-et-al-1997-flux-oskit.md) — Component dependencies include their execution environment.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
