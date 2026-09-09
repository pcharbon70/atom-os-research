---
title: "Nested-event and terminal handoff"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - privileged-entry-exit-and-execution-context
aliases: []
---

# Nested-event and terminal handoff

Nesting control should distinguish ordinary reentry from a state in which only minimal terminal capture is safe. It must preserve component 9's evidence and disposition protocol rather than create a competing fault handler.

## Scope and research question

How can another exception be handled when the interrupted entry path has not yet made its own state coherent?

This report refines [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Maintain separate ordinary and NMI-like depth/state evidence with bounded storage and exact CPU incarnation. The early path classifies which capture context can be minted; FatalCaptureContext is not CrashContext. The latter becomes available only after component 9 seals terminal evidence. Entry snapshots that diagnostics borrow retain their generation until every accepted copy or continuation hold is rehomed or drained.

### Protocol and publication points

NestedEntry → classify interrupted phase → use admissible independent storage → bounded capture handoff. If normal invariants cannot be recovered, use the preclassified recursive terminal route. Do not resume because a sink accepted bytes. On a valid continuation, component 9's exact return/park proof and component 2's final return machinery must agree before releasing entry custody.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Incrementing a depth counter is not enough if it can itself fault or be observed half-updated. Ordinary IRQ masks do not exclude all NMI-like classes. Overwriting the first event with a second destroys provenance. A terminal path that waits on an interrupted lock can deadlock despite containing no dynamic allocation.

### Alternatives and tradeoffs

Disabling more events reduces some interleavings but cannot promise immunity from every fault. Arbitrary recursive recovery is flexible but undermines bounded evidence. A small explicit nesting policy trades recoverability for a reviewable terminal path.

### Cross-architecture realization

Arm FEAT_NMI masking, x86 exceptional entry and optional RISC-V double-trap/RNMI facilities differ. Their availability belongs in the entry profile; no generic label supplies a portable safe stack or guaranteed reset.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Interrupt each entry-state publication and each capture handoff; check exact old/new snapshot identities.
- Exhaust the allowed nesting reserve and require finite terminal behavior rather than recursive logging.
- Attempt to widen NmiContext or pre-seal FatalCaptureContext into ordinary or post-seal crash authority.

The complete cross-component custody/continuation model must be checked alongside the existing component 9 reports.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Transition-security profile](transition-security-profile.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux entry/exit handling](../../../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — Ordering and instrumentation restrictions in partial entry states.
- [A-profile non-maskable interrupts](../../../30-sources/dall-2022-a-profile-non-maskable-interrupts.md) — NMI masking and stack-state behavior are feature-specific.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
