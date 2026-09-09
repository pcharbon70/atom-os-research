---
title: "Mapping authority and rights ceilings"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Mapping authority and rights ceilings

Which authorities bound a mapping throughout its lifetime, including later protection changes?

## Research basis and status

The seL4 mapping API intersects requested access with frame rights; Atom adds an explicit persistent binding ceiling. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../memory-mappings-and-architecture-resource-bindings.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A Mapping records address-space generation, range, frame offset and authority epoch, effective rights, immutable rights ceiling, architecture profile and completion state. The lower architecture layer owns page-table encoding and invalidation machinery; this service owns authorization and the lifetime of that binding.

### Admission, transitions and completion

Validate address-space placement authority, frame use rights, alignment, range arithmetic, memory type and inherited anchors before publishing a mapping. Effective permissions are the intersection of every applicable authority and backend restriction. Protect may never exceed the original ceiling or currently presented authority. Executable publication additionally requires the lower architecture's instruction-visibility contract; it is not just setting an execute bit.

### Failure and adversarial behavior

A later broader frame capability must not silently upgrade a mapping whose original creator received narrower authority. Conflicting cacheability aliases can invalidate the memory model even with apparently correct access bits. Unmap completion requires the named participant set and translation evidence before backing reuse.

### Alternatives and unresolved tradeoffs

Replacing a binding for every permission change simplifies immutable-state reasoning but adds object and invalidation cost. In-place attenuation can be cheaper if generation and completion semantics remain precise. W+X is excluded in the baseline; any alternative profile needs an explicit authority and publication argument.

## Verification obligations

Attempt rights amplification through Protect, mixed-type aliases, range overflow and stale address-space generations. Delay remote invalidation and require retained backing. Verify that effective rights, not merely requested masks, appear in the returned binding description.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
