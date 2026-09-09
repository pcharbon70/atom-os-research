---
title: "Product authority and durable detachment"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Product authority and durable detachment

Which input authorities must continue to constrain a newly created object after its constructor returns?

## Research basis and status

Capability derivation supplies the comparison, but Atom's multi-input product algebra is not a theorem supplied by that literature. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md), [2](../../../30-sources/kuz-et-al-2010-capdl.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../capability-spaces-and-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each operation schema classifies inputs as future-effect authority, consumed or admission-only guards, or resource/placement consent. A product retains the deduplicated union of effect-bearing lifetime anchors. Backing ownership and quota acceptance are recorded separately; neither silently grants permission to detach another principal's revocation dependency.

### Admission, transitions and completion

Compute the proposed anchor set before reserving publication. Validate every input under one admission transaction and reject a union exceeding the configured depth/capacity bound. An ephemeral fault resolver may authorize one repair without becoming the lifetime owner of an independently authorized mapping. A durable product may omit an effect-bearing anchor only with explicit CreateDurable consent from each affected lifetime authority and an accepted new group and payer.

### Failure and adversarial behavior

Keeping only the constructor's strongest input lets a weaker, revocable grant manufacture irrevocable access. Conversely, inheriting every transient guard can destroy a legitimately durable product when a one-shot token is consumed. The schema must justify each exclusion; this is not a heuristic based on object type names.

### Alternatives and unresolved tradeoffs

Conservative union is easier to audit but can over-couple unrelated lifetimes. Explicit detachment is more expressive but enlarges the authority algebra and policy-review burden. The baseline should reject ambiguous compositions rather than infer an owner's intention.

## Verification obligations

Model two independently revocable inputs, close each before and after publication, and verify the expected product admission result. Test duplicate anchors, depth overflow and missing detachment consent. Prove that resource-account transfer alone cannot alter effect authority.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Lookup admission must acquire a safe object lifetime.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Current authority and original operation identity remain distinct.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [capDL: A language for describing capability-based systems](../../../30-sources/kuz-et-al-2010-capdl.md) — comparative evidence; its methods and limits are recorded in the source note.
