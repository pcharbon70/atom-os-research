---
title: "Shared-ring ownership and incarnation"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Shared-ring ownership and incarnation

What contract surrounds a shared queue when either endpoint may fail or supply hostile descriptors?

## Research basis and status

CleanQ formalizes data-transfer ownership while leaving surrounding control responsibilities to other mechanisms. [1](../../../30-sources/haecki-et-al-2019-cleanq.md), [2](../../../30-sources/markettos-et-al-2019-thunderclap.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bounded-invocation-and-transport.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The shared transport names finite ring and buffer regions, endpoint generations, a transport epoch, ownership states and mapping rights. The kernel authorizes setup, notification and teardown; user-space protocols validate descriptors and handle payloads. Sharing bytes does not make another domain's indices trustworthy.

### Admission, transitions and completion

Publish descriptor contents before transferring ownership under the backend's memory-ordering contract. Validate region bounds, lengths, buffer generation and allowed state transitions before using a peer's descriptor. Bind restart to a new transport epoch and reconcile old offered or in-flight buffers before admitting them to the replacement. Teardown closes new submission but preserves old-effect tracking.

### Failure and adversarial behavior

A peer can modify intentionally shared metadata without violating page permissions. Reading a descriptor twice can therefore observe inconsistent values; validation needs a stable local copy or an explicitly safe concurrent protocol. Revoking a queue handle alone does not remove writable mappings or stop device DMA.

### Alternatives and unresolved tradeoffs

Shared rings reduce privileged data movement but place more protocol responsibility in service code. Small protected calls are simpler for control operations; they are not a reason to copy arbitrarily large data through the kernel. Copying can improve isolation when zero-copy trust and lifetime costs dominate.

## Verification obligations

Inject duplicate buffers, forged offsets, wraparound, late epoch traffic and modification during validation. Crash either endpoint at every ownership transition. Require no simultaneous exclusive ownership, no stale buffer reuse and explicit quarantine or reconciliation for unresolved transfers.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Exclusive binding, donation and migration](../scheduling-contexts-and-temporal-authority/exclusive-binding-donation-and-migration.md) — Call acceptance and donation share a commit boundary.
- [Recipient fences and service publication](../failure-boundaries-and-recovery-topology/recipient-fences-and-service-publication.md) — Replacement must preserve old call outcomes.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer](../../../30-sources/haecki-et-al-2019-cleanq.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
