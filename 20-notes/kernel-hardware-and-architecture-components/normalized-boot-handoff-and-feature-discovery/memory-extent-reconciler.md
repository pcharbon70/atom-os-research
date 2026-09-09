---
title: "Memory extent reconciler"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - normalized-boot-handoff-and-feature-discovery
aliases: []
---

# Memory extent reconciler

The reconciler should produce a conservative, disjoint physical-memory ledger while preserving the provenance and release conditions of every restriction. Unknown space must never become RAM merely because no reservation describes it.

## Scope and research question

How can overlapping discovery claims become allocator inputs without releasing bytes still owned by firmware, boot modules or kernel state?

This report refines [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Each input extent records byte interval, source, memory class, attributes and retention condition. CanonicalExtent retains original byte coverage alongside allocator-granule coverage. One provider profile authorizes positive RAM discovery; other inputs can restrict that set but cannot enlarge it. ReclaimableAfter is a typed completion dependency, not a duration. The allocator receives an ownership transfer only after snapshot seal and all applicable retention predicates.

### Protocol and publication points

Collect authoritative candidate RAM → overlay reservations → split at checked endpoints → reconcile restrictive classes → round usable ranges inward and protected ranges outward → publish canonical extents. Contradictions become ReservedConflict with both source identities. Preserve separate memory-type conflicts rather than inventing a universal ordering for incomparable attributes. Release a retained range through an explicit later transaction that revalidates its exact extent and dependency generation.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Overflow in end-address arithmetic or outward rounding can expose reserved bytes. A module may share a page with data whose lifetime is longer; byte-level release must not free that page early. Page-table roots, adapter scratch and the snapshot itself must be included in the reservation ledger. Firmware runtime memory does not become ordinary RAM simply because boot services ended.

### Alternatives and tradeoffs

Rejecting every conflict is simple but can make imperfect firmware unusable. Conservative reservation preserves safety at the cost of capacity. Keeping the provider map verbatim is cheap but makes every allocator client repeat lifetime and conflict reasoning.

### Cross-architecture realization

The invariant is independent of page-table format. UEFI memory types, ACPI reservations and device-tree reserved regions are normalized without asserting identical semantics. Physical address width and allocator granule are explicit backend inputs; larger-page optimization cannot override byte reservations.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Permute identical input sets and demand the same canonical output and conflict provenance.
- Inject partially overlapping usable, device, bad and retained ranges; no output usable byte may violate any applicable restriction.
- Complete retention tokens out of order and with stale generations; only the exact currently eligible physical range can transfer.

The overlap lattice, attribute incompatibilities and retention-to-frame handoff need a machine-checked model.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [CPU feature admission](cpu-feature-admission.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [UEFI specification](../../../30-sources/uefi-forum-2024-uefi-2-11.md) — Provider memory-map and service-lifetime contracts.
- [ACPI 6.6](../../../30-sources/uefi-forum-2025-acpi-6-6.md) — Structured discovery with explicit table validation.
- [Devicetree 0.4](../../../30-sources/devicetree-org-2023-devicetree-specification-0-4.md) — Bounded blob structure and reserved-memory descriptions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
