---
title: "Topology and feature eligibility"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - logical-cpu-coordination-and-lifecycle
aliases: []
---

# Topology and feature eligibility

Topology describes relationships; eligibility grants permission to execute a class of work. Keeping these separate avoids turning a discovery hint into scheduling or security authority.

## Scope and research question

How can heterogeneous feature sets and changing CPU membership be exposed without requiring all processors to be identical?

This report refines [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

TopologySnapshot records packages, cores, threads, proximity and provenance. FeatureClass records the required instruction/state profile and an incarnation-bound eligible set. The scheduler owns placement policy; the architecture layer validates mechanism requirements. A context's required feature profile travels with it, independently from its preferred locality.

### Protocol and publication points

Validate discovery relations → publish descriptive topology → validate local feature witnesses → construct execution classes → admit eligible members → recheck class membership when dispatching or migrating → withdraw eligibility before drain or profile change. Existing contexts that depend on a removed facility need explicit migration, transformation or rejection policy.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An affinity hint does not prove shared-cache isolation, equal counter behavior or a security domain. Firmware and virtualized topology may be incomplete. Changing the system-wide feature intersection cannot silently shrink the state format of a saved context. A compatible CPU class also does not establish temporal noninterference.

### Alternatives and tradeoffs

One conservative profile simplifies migration and verification. Multiple classes support specialized processors but create availability and policy dependencies. Embedding topology and policy in every low-level primitive duplicates authority and makes changes harder to reason about.

### Cross-architecture realization

The abstraction supports differing x86 feature masks, Arm extension combinations and RISC-V extension profiles without claiming identical discovery mechanisms. Core/thread/package terminology itself can be incomplete; retain raw relations alongside normalized descriptors.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Supply contradictory topology and preserve uncertainty without manufacturing a placement authority.
- Withdraw the last eligible CPU while a feature-dependent context is blocked; require an explicit outcome rather than incompatible dispatch.
- Race class publication with migration and CPU restart; dispatch must validate the current incarnation and context requirements.

Feature-class availability under failures and the representation of evolving execution environments need a separately specified policy, not an assumed architecture-layer answer.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [CPU quarantine and recovery ledger](quarantine-and-recovery-ledger.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [Arm A-profile architecture](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Architecture-specific exception, ordering and state contracts.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.
- [Time protection](../../../30-sources/ge-et-al-2019-time-protection.md) — Temporal isolation exceeds timer precision.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
