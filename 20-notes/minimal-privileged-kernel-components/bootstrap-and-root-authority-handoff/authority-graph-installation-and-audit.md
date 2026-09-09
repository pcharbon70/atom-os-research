---
title: "Authority-graph installation and audit"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Authority-graph installation and audit

How can the initialized authority graph be checked without inventing a universal administrative capability?

## Research basis and status

capDL and its initialization literature distinguish the described graph from the process used to instantiate it. [1](../../../30-sources/kuz-et-al-2010-capdl.md), [2](../../../30-sources/boyton-et-al-2013-verified-system-initialisation.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bootstrap-and-root-authority-handoff.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The installer owns a bounded sequence of slot installations into precreated capability spaces. Ordinary service access, lifecycle control, diagnostics, recovery and shared-reset control are separate facets. The audit view describes effective rights and dependencies; it is not another route to invoke them.

### Admission, transitions and completion

Install attenuated capabilities using the precomputed slots and stable lineage records. Resolve every recovery and reset escrow from independently held authority, not from the future child or replaceable supervisor. Once the graph is installed, enumerate its normalized object identities, slot generations, rights, anchors and resource assignments into a bounded audit stream. Compare the resulting digest and critical graph predicates with the authorized construction description.

### Failure and adversarial behavior

An extra cap hidden in a loader table matters if any live context can exercise it. Conversely, inert residue is a different assurance question from executable ambient authority. Audit truncation must be explicit and cannot be accepted as full graph conformance. Hash equality does not prove that the intended graph itself is safe.

### Alternatives and unresolved tradeoffs

Deleting all loader metadata immediately minimizes residue but may destroy the only audit explanation. Retaining a read-only description is useful if it cannot carry authority or keep objects live indefinitely. Inspection capacity and its eventual release need their own payer.

## Verification obligations

Insert one extra lifecycle or reset facet; attenuate one required recovery right too far; make an audit cursor truncate before the offending slot. Require mismatch detection in all cases. Verify that audit consumers cannot convert reported identities into selectors in another capability space.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Construction must preserve effect-bearing authority.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Bootstrap must provision an independently usable recovery path.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [capDL: A language for describing capability-based systems](../../../30-sources/kuz-et-al-2010-capdl.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Formally verified system initialisation](../../../30-sources/boyton-et-al-2013-verified-system-initialisation.md) — comparative evidence; its methods and limits are recorded in the source note.
