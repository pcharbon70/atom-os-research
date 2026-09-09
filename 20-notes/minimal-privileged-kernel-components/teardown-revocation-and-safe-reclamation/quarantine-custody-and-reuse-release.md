---
title: "Quarantine custody and reuse release"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Quarantine custody and reuse release

When is quarantine a safe terminal disposition rather than a name for unknown damage?

## Research basis and status

DMA security evidence requires exact reachable memory and lifetime control; isolation labels alone are insufficient. [1](../../../30-sources/markettos-et-al-2019-thunderclap.md), [2](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../teardown-revocation-and-safe-reclamation.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A quarantine record names the exact non-reusable resource set, proven confinement conditions, independent custodian, payer and unresolved completion obligations. REAPED_WITH_QUARANTINE means custody was transferred for that set; it does not mean the device stopped or all backing became free.

### Admission, transitions and completion

Deny new frame mutations, close every submission/configuration alias and establish that remaining effects cannot escape the declared set. Transfer custody and retained charges atomically to a capable independent owner. If later matching completion permits release, join all remaining effects and pass an exact-generation eligibility receipt to the allocator for sanitization and fresh publication. New use requires a new identity generation.

### Failure and adversarial behavior

An uncertain DMA reachability set cannot be safely called quarantined. If confinement is not proven, use Escalated or node-level failure and do not claim successful reaping. Releasing a charge account before custody transfer creates invisible retained debt; reopening old mutating frame facets resurrects stale authority.

### Alternatives and unresolved tradeoffs

Permanent confined quarantine can preserve unrelated service at a storage and device-capacity cost. Aggressive reclamation improves availability only when completion evidence is real. Deployment admission should bound the retained set and decide what happens when quarantine capacity is exhausted.

## Verification obligations

Leave one direct alias live, expand a device's reachable set and remove the custodian reserve. Require quarantine rejection or escalation. Then supply valid delayed completion and verify sanitization, exact charge transfer and permanent staleness of old capabilities.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sanitization and generation-safe reuse](../typed-object-storage-and-explicit-memory/sanitization-and-generation-safe-reuse.md) — Only the allocator completes sanitization and fresh publication.
- [Device completion and reset composition](../memory-mappings-and-architecture-resource-bindings/device-completion-and-reset-composition.md) — Device-specific graphs supply physical completion evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [VFIO - Virtual Function I/O](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — comparative evidence; its methods and limits are recorded in the source note.
