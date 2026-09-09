---
title: "Effect ledger and dependency graph"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Effect ledger and dependency graph

How can teardown know every effect that must finish without discovering dependencies after resources are already failing?

## Research basis and status

Software-reference and DMA research cover different effect classes; neither alone supplies complete reclamation evidence. [1](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md), [2](../../../30-sources/haecki-et-al-2019-cleanq.md), [3](../../../30-sources/markettos-et-al-2019-thunderclap.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../teardown-revocation-and-safe-reclamation.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each admitted TeardownProduct records type, stable generation, backing, payer, lifetime anchors, immutable operation identity, participant dependencies and expected completion classes. The domain's lifecycle remains authoritative; product state is a local projection, not a second domain-stop protocol.

### Admission, transitions and completion

Create and charge the ledger entry when admitting the effect. On closure, freeze new product admission and form the dependency graph from those existing records. Software calls, donated contexts, mappings, IRQs, timers and device operations can progress independently where their dependencies permit. A device profile determines whether physical mapping withdrawal precedes or follows drain/reset.

### Failure and adversarial behavior

Building the ledger only after a crash can omit an in-flight effect or require unavailable allocation. A universal teardown list may remove DMA translation needed by a recovery sequence. Missing IRQ or timer nodes can permit late callbacks after apparently complete memory reclamation.

### Alternatives and unresolved tradeoffs

One conservative total order is easier to describe but unnecessarily serializes independent work and can conflict with device requirements. A typed acyclic dependency graph is more expressive; every edge and absent effect class must be justified by the operation schema.

## Verification obligations

Remove each effect class from a constructed ledger and check that the consistency audit detects the omission. Delay independent branches, introduce a profile cycle and replay a duplicate product. Require no reusable result before every applicable dependency is completed or explicitly transferred to confined custody.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sanitization and generation-safe reuse](../typed-object-storage-and-explicit-memory/sanitization-and-generation-safe-reuse.md) — Only the allocator completes sanitization and fresh publication.
- [Device completion and reset composition](../memory-mappings-and-architecture-resource-bindings/device-completion-and-reset-composition.md) — Device-specific graphs supply physical completion evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer](../../../30-sources/haecki-et-al-2019-cleanq.md) — comparative evidence; its methods and limits are recorded in the source note.
3. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
