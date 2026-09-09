---
title: "Typed MMIO ordering and completion"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Typed MMIO ordering and completion

An MMIO write can be ordered with other accesses without having reached its device. The service should expose those effects separately and require a device-safe completion recipe.

## Scope and research question

How does a caller distinguish access issue, ordering, receipt and semantic device completion?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

An authorized MMIO view binds endpoint incarnation, range, width, endianness, memory type and register side effects. Operations declare ordered or relaxed relationships and the relevant device/interconnect scope. A completion recipe identifies a safe readback/status mechanism and its validity during reset/removal. Component 8 owns device authority and lifetime; this service supplies ordering semantics.

### Protocol and publication points

Prepare validated access → issue with selected compiler/CPU/device ordering → optionally establish posted-write receipt → await separately defined device operation completion. Receipt cannot become proof that a queue drained or DMA ceased. An asynchronous recipe must retain its endpoint generation and resource borrow until its terminal observation or explicit quarantine.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Reading an arbitrary register to flush writes can acknowledge or destroy an event. Completion across two devices is not implied by ordering within one device. A spinlock release may not drain posted writes. Register access can stall on failed hardware, so a fixed sequence length is not a hardware response-time guarantee.

### Alternatives and tradeoffs

Fully ordered accessors are a conservative default but cannot hide bus completion semantics. Relaxed accessors can lower cost only where a named protocol supplies the missing ordering. Generic memory-copy routines are not substitutes for side-effect-aware device access.

### Cross-architecture realization

Mapping attributes, I/O instructions and ordering domains vary across backends. Port space and MMIO may require different mechanisms. The common interface names the required effect and endpoint scope rather than exposing one universal fence.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Model delayed posted writes and verify that receipt and operation completion remain false after mere issue.
- Use clear-on-read and reset-inaccessible registers to reject unsafe completion recipes.
- Change endpoint generation while a completion observation is pending; prevent it from completing the replacement operation.

Device-specific safe completion registers and interconnect failure behavior require profile-level evidence.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Cache-maintenance planner](cache-maintenance-planner.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux device-I/O contracts](../../../30-sources/linux-kernel-community-2026-device-io-contracts.md) — Posted-write receipt differs from CPU-side ordering.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
