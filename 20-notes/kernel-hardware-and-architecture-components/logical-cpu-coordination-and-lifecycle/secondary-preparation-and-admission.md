---
title: "Secondary preparation and admission"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - logical-cpu-coordination-and-lifecycle
aliases: []
---

# Secondary preparation and admission

Starting execution and admitting a CPU are different operations. A secondary must demonstrate that its local execution substrate is ready before any subsystem may target it as online.

## Scope and research question

Which dependencies must be installed and validated between a firmware start request and publication of usable membership?

This report refines [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A StartTransaction owns a unique start cookie, incarnation, entry storage and dependency ledger. Preparation includes stack and exceptional-stack bounds, translation roots, context layouts, required feature evidence, interrupt reception, timer state, executable-generation catch-up and diagnostic buffers. The entering CPU claims exactly its cookie; only the lifecycle owner publishes Online.

### Protocol and publication points

PresentOffline → Preparing(txn) → Prepared(incarnation) → StartRequested(txn) → Joining(txn) → JoinReady(txn) → Online. JoinReady attests the dependency ledger, not merely arrival at an entry address. Duplicate entry or stale-cookie entry goes to a bounded rejection path. Failure before exposure may unwind proven-local resources; uncertain remote execution transfers them to quarantine.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Firmware acceptance can precede execution by an unbounded interval. Reusing a startup stack after a timeout lets a late CPU execute on somebody else's storage. Catch-up of instruction publication and translations must close against concurrent changes before online publication; a checklist inspected earlier is not an admission barrier.

### Alternatives and tradeoffs

Serial CPU admission reduces coordination complexity but sacrifices parallel startup. Parallel admission needs per-transaction custody and a coordinated membership cut. Automatically treating firmware success as online is not a weaker performance option; it violates the contract.

### Cross-architecture realization

PSCI CPU_ON and SBI hart-start involve higher-privilege software; x86 startup has a different instruction and rendezvous mechanism. All require separate kernel readiness evidence. Architecture-specific entry alignment, privilege, addressability and cache requirements stay in the backend profile.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Delay a start until after timeout and begin a second request; the first cookie must not claim the second stack or incarnation.
- Change executable publication while a secondary is joining; it must join with the required generation or remain ineligible.
- Fail each local dependency before JoinReady; no scheduling or interrupt routing may target that CPU.

Concurrent publication/admission closure and recovery when a secondary fails between JoinReady and Online remain unverified.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Bounded cross-CPU request fabric](cross-cpu-request-fabric.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Arm PSCI 1.3](../../../30-sources/arm-2024-power-state-coordination-interface.md) — Firmware CPU requests and OS admission have different states.
- [RISC-V SBI](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
