---
title: "Controller and source normalization"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - interrupt-event-fabric
aliases: []
---

# Controller and source normalization

Interrupt source identity should be scoped to a discovered controller and source incarnation. A vector number is neither global identity nor authority to bind or complete an interrupt.

## Scope and research question

How are unlike controller namespaces normalized without hiding their completion semantics?

This report refines [component 5: Interrupt event fabric](../interrupt-event-fabric.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Controller profiles describe identifier namespace, trigger/polarity, target model, priority, claim/EOI/deactivation rules and remapping dependencies. Source, route and binding are attenuated views over one accounted IRQBinding aggregate, not independently owned objects. Source classes distinguish devices, timers, IPIs and local errors. A device capability cannot select a kernel-reserved source class.

### Protocol and publication points

Inactive descriptor → validated controller profile → source generation allocated → compatible flow selected → binding prepared. No source is armed until destination storage, route, management path and accounting are ready. Device/MSI sources retain endpoint/remapping dependencies owned by component 8. Discovery alone never enables controller delivery.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Equal integers in APIC, GIC, PLIC or IMSIC namespaces are not interchangeable. Multiple firmware records may describe aliases. Unsupported trigger or routing combinations require rejection. An absent interrupt-remapping facility cannot be hidden by returning a normal-looking source handle.

### Alternatives and tradeoffs

A flat interrupt integer API is convenient but pushes namespace and lifecycle checks into every caller. Typed views add validation while preserving one aggregate owner. Separate allocations for each view would create competing teardown ledgers.

### Cross-architecture realization

Normalize semantic source classes while retaining controller-specific flow. Some controllers have separate priority-drop/deactivation operations; others use different claim/completion schemes. These differences belong in explicit profiles, not simulated synonyms.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Reuse a numeric source across two controllers and verify no cross-completion.
- Attempt device authority on a kernel IPI source and reject it.
- Arm a source with missing sink, account or remapping prerequisites; no device-visible enable may occur.

A complete controller/profile compatibility matrix and alias detection strategy remain open.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Interrupt flow-state machines](interrupt-flow-state-machines.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [seL4 reference manual](../../../30-sources/sel4-foundation-2026-reference-manual.md) — Capability-mediated authority and distinct kernel object kinds.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
