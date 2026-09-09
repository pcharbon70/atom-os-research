---
title: "Reset-domain and recovery authority"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# Reset-domain and recovery authority

Reset is a scoped destructive capability, not a general permission held by every device manager. Recovery must remain possible after a manager fails without leaving that manager's stale credentials effective.

## Scope and research question

Who can reset a shared domain, and how is authority transferred safely when its ordinary owner crashes?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

ResetDomain names all affected endpoints and dependencies. A scoped Reset facet plus current ResetLease.Use authorizes an ordinary operation. Independent ResetControl belongs to a recovery authority that can close the old manager's lease and install a successor through escrow. It is not an interchangeable ordinary reset credential. The ledger preserves buffer, queue and interrupt custody throughout.

### Protocol and publication points

Validate scope and lease → close affected new work → coordinate dependent owners → issue the specified reset → observe its documented completion → reinitialize or quarantine → rotate generations and install successor authority. A recovery takeover first invalidates the old lease; it cannot assume that a vanished caller returned resources.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Shared reset may disrupt unrelated principals or erase evidence needed for diagnosis. Reset success does not necessarily prove all external traffic drained or all configuration reverted. Stale manager callbacks must not operate on reinitialized hardware. Automatically handing the failed manager another ordinary credential defeats recovery separation.

### Alternatives and tradeoffs

A central reset broker simplifies scope accounting but is a privileged availability dependency. Delegated scoped leases reduce central traffic while requiring reliable revocation and escrow. Restarting a driver process alone is insufficient when hardware state and outstanding transfers survive.

### Cross-architecture realization

Function, bus, controller and platform reset domains are not universal architectural categories with identical effects. Each control path must document its higher-privilege dependencies, collateral scope and what completion actually establishes.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Crash the manager before and after reset issue; retained resources and reset authority must have a unique surviving owner.
- Attempt reset with a stale lease and with authority covering only part of the affected domain; both must fail.
- Complete reset while DMA drainage remains uncertain; no unrelated release predicate may be inferred.

Independent recovery availability and trustworthy reset observation remain unresolved system-level requirements.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [I/O fault attribution and quarantine](io-fault-attribution-and-quarantine.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [VFIO isolation groups](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — Device functions do not necessarily form independent isolation units.
- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [Tock deployment retrospective](../../../30-sources/schuermann-et-al-2025-tock-decade.md) — Typed interfaces still require sound ABI and runtime validation.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
