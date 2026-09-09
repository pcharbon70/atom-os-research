---
title: "Interrupt flow-state machines"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - interrupt-event-fabric
aliases: []
---

# Interrupt flow-state machines

Controller completion, device-cause clearing and rearming are different transitions. The fabric should choose a closed flow plan rather than let an arbitrary driver callback define privileged acknowledgement order.

## Scope and research question

Which state transitions preserve events while preventing rearm before a source is safe?

This report refines [component 5: Interrupt event fabric](../interrupt-event-fabric.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A FlowPlan names the controller chain, trigger semantics, mask/ack/EOI/deactivate sequence, pending representation and permitted completion conditions. It is chosen from validated data. The device service clears device-specific cause under its own authority; the interrupt fabric owns controller state. Binding completion carries the current source, route, binding and delivery generations.

### Protocol and publication points

Armed → Captured → FlowStabilized → NoticeAvailable → ServiceCompletionValidated → RearmPermitted. The exact transitions vary by flow; do not force edge and level sources through an identical acknowledgement sequence. A still-asserted level may require continued masking. Events while masked must be represented by supported pending/retrigger semantics or explicit loss, not invented occurrence counts.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Completing a controller does not prove the device queue was drained. Edge loss and repeated level delivery are different hazards. A stale completion must not rearm a replacement binding. Spurious interrupts need a source-specific treatment that does not consume another source's completion authority.

### Alternatives and tradeoffs

One generic acknowledge routine reduces code size but hides essential behavior. Per-device privileged callbacks are flexible but enlarge the trusted hard path. Closed generated plans preserve variation while keeping effects reviewable.

### Cross-architecture realization

APIC/vector handling, GIC priority/deactivation and PLIC/IMSIC completion differ. A source profile must preserve these distinctions even when the user-visible event notice is common.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Hold a level asserted through service completion and check safe rearm policy.
- Deliver edges during masking and verify the declared pending/loss semantics.
- Exercise pending-and-active states, spurious identities and duplicated completion in every flow family.

Flow-specific state-machine refinement and device/controller integration tests are not yet executed.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Bounded hard-path recording](bounded-hard-path-recording.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [Relaxed exception semantics for Arm-A](../../../30-sources/simner-et-al-2024-relaxed-exception-semantics.md) — Precise exception transitions are not general memory barriers.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
