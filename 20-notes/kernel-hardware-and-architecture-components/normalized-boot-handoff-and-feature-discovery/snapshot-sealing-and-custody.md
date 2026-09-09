---
title: "Snapshot sealing and custody"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - normalized-boot-handoff-and-feature-discovery
aliases: []
---

# Snapshot sealing and custody

BootSnapshot should be the immutable publication boundary for validated boot facts. Sealing must close mutable input dependencies and retain the evidence needed to explain each fact, without presenting a digest as authentication.

## Scope and research question

When may downstream components rely on boot facts and release the storage from which those facts originated?

This report refines [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

The snapshot owns canonical extents, admitted boot-CPU facts, CPU candidates, inactive mechanism descriptors, modules, retained ranges, conflicts and provenance. A seal record binds format version, adapter identity, accepted input digests and validation profile. Consumer views contain values and bounded references to snapshot-owned storage. Diagnostics export identifiers and confidence, not provider callbacks or capability-bearing handles.

### Protocol and publication points

StructurallyParsed → SemanticallyReconciled → DependenciesOwned → Sealed → Published. The publish point makes one complete object visible; it never exposes partially filled arrays. Original buffers become releasable only when every dependent value was copied or has an explicit retained owner. Later discovery creates separate versioned objects, not silent mutation of the initial snapshot. Whole-snapshot retirement needs drainage of all consumer views.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A digest proves neither origin nor semantic truth. Separate observed facts, authenticated claims, unresolved conflicts and assumptions. An authenticated loader may still misreport hardware. Snapshot memory itself cannot appear as allocator-usable. Keeping raw bytes for diagnostics requires capacity limits and sanitization of secrets; deleting raw bytes requires enough retained interpretation provenance for audit.

### Alternatives and tradeoffs

Permanent raw retention aids forensic analysis but increases memory and disclosure cost. Minimal normalized values are easier to consume but can lose important ambiguity. Retain bounded raw digests and selected records with explicit limits, while keeping uncertainty in typed facts.

### Cross-architecture realization

The seal contract should be identical across provider and ISA backends; the content records which facilities remain externally supplied. Neither a second architecture nor a new firmware revision may silently reinterpret an existing snapshot format.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Interrupt construction at each publication cut and verify consumers see either no snapshot or a complete sealed one.
- Poison released adapter storage and traverse every published reference.
- Vary provenance authentication independently from structural validity; consumers must not upgrade confidence from checksum success.

Snapshot confidentiality, long-term diagnostic custody and a formal consumer-lifetime proof are unresolved.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Provider handoff adapter](provider-handoff-adapter.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [BootStomp](../../../30-sources/redini-et-al-2017-bootstomp.md) — Empirical motivation for adversarial early-input analysis.
- [Flux OSKit](../../../30-sources/ford-et-al-1997-flux-oskit.md) — Component dependencies include their execution environment.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
