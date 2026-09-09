---
title: "Polling and interrupt handoff"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - interrupt-event-fabric
aliases: []
---

# Polling and interrupt handoff

Polling should be an explicit bounded ownership mode with a loss-aware transition back to interrupts. It is a scheduling and workload tradeoff, not an unconditional optimization.

## Scope and research question

How can a service switch between polling and interrupt-driven work without a lost wakeup or unbounded privileged loop?

This report refines [component 5: Interrupt event fabric](../interrupt-event-fabric.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A polling lease identifies source/binding generation, admitted poller, budget, completion conditions and event state retained during handoff. Device servicing belongs to the driver domain or an explicitly bounded mediator, not generic hard entry. The interrupt fabric controls masking and rearm; scheduling policy chooses whether polling deserves CPU time.

### Protocol and publication points

InterruptDriven → mask/stabilize under selected flow → PollLeaseActive → bounded polling → recheck pending/device state → release polling ownership → rearm only after the shared handoff predicate. Work arriving at either boundary must remain visible through device state or retained event evidence. Budget exhaustion keeps a named continuation owner rather than spinning indefinitely.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Finishing exactly at a processing budget can be ambiguous; state must distinguish exhausted from known drained. Releasing a lease is not proof that the poller's code stopped using its resources. Fast-device experiments do not justify busy waiting on a stalled or malicious device, nor a fixed performance crossover for all workloads.

### Alternatives and tradeoffs

Pure interrupts reduce idle CPU use but can cost more under dense events. Pure polling reduces notification overhead but consumes budget under idle/stalled conditions. Hybrid control needs measured workload and latency objectives, with correctness independent of the chosen threshold.

### Cross-architecture realization

The handoff invariant is portable; pending-bit, edge-latching and device-poll semantics are not. Backends must reject a polling mode when they cannot preserve the declared event semantics.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Inject work between mask and poll scheduling, and between final empty observation and rearm.
- Finish at exactly the budget, at zero budget and with an indefinitely stalled device.
- Disable/rebind while a poller retains references; prevent storage reuse until its actual access is drained.

Performance crossover, fairness and the exact handoff algorithm require separate measurement and model validation.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Controller and source normalization](controller-and-source-normalization.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [When poll is better than interrupt](../../../30-sources/yang-et-al-2012-when-poll-is-better-than-interrupt.md) — Workload-dependent evidence, not a universal polling advantage.
- [Linux NAPI](../../../30-sources/linux-kernel-community-2026-napi-contracts.md) — Budgeted processing and explicit masking/ownership handoff.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
