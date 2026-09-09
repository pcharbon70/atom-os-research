---
title: "CPU quarantine and recovery ledger"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - logical-cpu-coordination-and-lifecycle
aliases: []
---

# CPU quarantine and recovery ledger

Quarantine records what remains unsafe to reuse when CPU progress or stop evidence is missing. It is an owned recovery state, not a synonym for an offline flag.

## Scope and research question

How does the system preserve safety after partial CPU removal without leaking responsibility or falsely declaring resources reusable?

This report refines [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

QuarantineRecord binds an incarnation, unresolved requests, retained memory and context objects, last trusted observation and permitted recovery actions. An independent recovery owner survives the failed transaction's caller. It may request platform reset or additional evidence only within an explicit scope; it cannot forge component completion tokens.

### Protocol and publication points

Detect uncertainty → close new eligibility → atomically transfer custody to recovery → record bounded diagnostics → attempt an authorized recovery path → join newly established completion predicates → retire only resources covered by that evidence. If no supported recovery exists, retain quarantine or enter a declared system-terminal policy.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Continuing after uncertainty can exhaust quarantine storage and threaten availability. Capacity therefore needs admission reserves and escalation policy. A reset observed through an untrusted or narrower control path is not automatically proof that all old execution and DMA stopped. Diagnostic capture may preserve evidence but never substitutes for containment.

### Alternatives and tradeoffs

Immediate whole-system termination simplifies uncertainty containment but forfeits availability. Scoped recovery preserves service only when independent control and complete release evidence exist. Silently abandoning records is neither containment nor recovery.

### Cross-architecture realization

Firmware stop queries, hardware reset domains and watchdog facilities vary and may depend on code above the kernel's privilege level. Each backend must state its trust assumptions and the scope of what its observation proves.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Destroy the initiating caller after timeout; each retained resource must still have exactly one accountable recovery owner.
- Exhaust quarantine capacity before admitting another lifecycle transaction; the system must reject or escalate safely.
- Deliver a late completion after reset and incarnation change; only the original ledger may consume it.

Recovery liveness, bounded retention under repeated faults and trust in platform reset observations remain open architecture questions.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [CPU identity, incarnation and membership](identity-incarnation-and-membership.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [Arm PSCI 1.3](../../../30-sources/arm-2024-power-state-coordination-interface.md) — Firmware CPU requests and OS admission have different states.
- [RISC-V SBI](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
