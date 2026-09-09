---
title: "Sanitization and generation-safe reuse"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Sanitization and generation-safe reuse

When may an old object's bytes and identifier safely become a new object?

## Research basis and status

Software reclamation literature motivates delayed reuse; it does not establish that device writers have stopped. [1](../../../30-sources/michael-2004-hazard-pointers.md), [2](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../typed-object-storage-and-explicit-memory.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The allocator owns the final transition from an authorized reusable extent to fresh typed backing. The reaper supplies effect-completion eligibility; the allocator must not independently infer it from elapsed time. The parent lifecycle remains Private → Live → Closing → Draining → Quiescent → Sanitizing → Reusable → Free, with retained and quarantined alternatives.

### Admission, transitions and completion

Accept an exact-generation release receipt whose ledger covers software activations and every applicable hardware effect class. Sanitize only after all old writers are stopped or otherwise excluded from that reusable extent. Record sanitization completion before incrementing identity generation and publishing the new object. Retain lineage tombstones until references and cursors can no longer resolve them.

### Failure and adversarial behavior

Zeroing while DMA remains possible can be immediately undone. Reusing an identifier before a late completion is rejected may let that completion mutate the replacement. A checksum of zeroed bytes establishes neither absence of future writes nor device confinement. Non-RAM resources need a separate type-specific reuse contract.

### Alternatives and unresolved tradeoffs

Always scrubbing maximizes confidentiality simplicity but may impose large cleanup latency; incremental scrubbing is acceptable only while the extent remains unpublished and charged. Generation widths and wrap retirement are deployment choices requiring quantitative analysis, not arbitrary constants.

## Verification obligations

Delay a writer until after attempted zeroing, replay an old completion after retype, and force generation exhaustion. Require non-reuse or rejection, never reopening an old mutating facet. Measure zeroing work in charged slices and distinguish reusable bytes from quarantined custody.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Quarantine custody and reuse release](../teardown-revocation-and-safe-reclamation/quarantine-custody-and-reuse-release.md) — The reaper proves eligibility; the allocator performs final reuse.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Creation must attach the correct lifetime dependencies.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Hazard pointers: Safe memory reclamation for lock-free objects](../../../30-sources/michael-2004-hazard-pointers.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
