---
title: "CPU drain, stop and reclamation"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - logical-cpu-coordination-and-lifecycle
aliases: []
---

# CPU drain, stop and reclamation

CPU removal is a multi-owner drain followed by an irreversible stop commitment. Software ineligibility, no further kernel execution and physical power-off are distinct facts.

## Scope and research question

When may CPU-local memory and shared participation records be reclaimed after removal?

This report refines [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A StopTransaction owns the incarnation and gathers scheduler, interrupt, timer, translation, executable-publication, extended-state and diagnostic custody dependencies. The lifecycle owner removes new-work eligibility and prevents fresh participants. Component owners certify only their respective drain predicates. Resources retain their original owners until the joined release predicate passes.

### Protocol and publication points

Online → Draining → StopCommitted → FirmwareStopping → PresentOffline(next incarnation). Before StopCommitted, rollback requires restoring a coherent whole-system membership state. After commitment, no rollback may reintroduce the old incarnation. If stopping or acknowledgement is uncertain, enter Quarantined with the unresolved ledger rather than PresentOffline.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An empty task queue does not establish absence of interrupt handlers, delayed memory accesses or retained context state. A successful stop indication may have a narrower meaning than physical power removal. Releasing startup or terminal stacks before the final execution boundary creates use-after-free. A late timer interrupt must not revive an old lifecycle.

### Alternatives and tradeoffs

Permanent parking avoids some power-control complexity but still needs proof that the parked CPU cannot use reclaimed objects. Full firmware power-off reduces residual activity only under the applicable firmware contract. Neither eliminates software lifetime bookkeeping.

### Cross-architecture realization

PSCI CPU_OFF is a local non-returning successful transition with prerequisites; SBI hart-stop has its own state contract; x86 software parking and platform power control are not equivalent. Backend evidence must name whether it establishes execution cessation, restartability or power state.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Inject removal at each subsystem's drain boundary while work arrives; new admissions must close and existing owners remain accountable.
- Fail after StopCommitted and attempt rollback; the old incarnation must remain ineligible.
- Retain a diagnostic or translation participant past stop and verify its storage is not reclaimed early.

A complete proof composing all drain owners and stop failure modes is missing; a timeout-based reclaim policy is specifically rejected.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Topology and feature eligibility](topology-and-feature-eligibility.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Arm PSCI 1.3](../../../30-sources/arm-2024-power-state-coordination-interface.md) — Firmware CPU requests and OS admission have different states.
- [RISC-V SBI](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
