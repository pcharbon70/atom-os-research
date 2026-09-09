---
title: "One-way root handoff and abort"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# One-way root handoff and abort

What evidence permits a root service to begin ordinary operation, and what happens if it never accepts?

## Research basis and status

Microkit's initialization caveat shows why service eligibility cannot be inferred from an assumed global initialization barrier. [1](../../../30-sources/sel4-foundation-2026-microkit-system-contracts.md), [2](../../../30-sources/sel4-foundation-2026-capdl-loader-contract.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bootstrap-and-root-authority-handoff.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The handoff gate owns the current boot generation, one-shot HandoffAccept authority, bootstrap sealing state and an independently reserved terminal route. The parent sequence remains FactsSealed → PlanValidated → ObjectsPrivate → GraphInstalled → AwaitingAck → Sealed → NormalOperation. A child's acknowledgement is evidence of its contract, not proof of the loader's internals.

### Admission, transitions and completion

Make only the designated initial domain and funded execution context eligible. Deliver an immutable handoff description and an acceptance facet bound to that boot generation. Acceptance atomically consumes the facet and seals temporary bootstrap power before normal admission opens. A deadline or explicit rejection uses the predeclared failure route. An optional fallback root requires an exclusive, separately reserved profile; it is not chosen by arbitrary recovery code.

### Failure and adversarial behavior

After public authority exists, returning to manifest editing can create two competing roots. A late acknowledgement must not reopen a sealed or aborted generation. Root failure before acceptance cannot rely on the same root to allocate its fault buffer, replenish its timeout handler or grant recovery rights.

### Alternatives and unresolved tradeoffs

Waiting indefinitely preserves a stalled root but sacrifices boot availability. A deadline provides a terminal decision only under a specified time source and reserved execution budget. Neither choice grants permission to retry initialization with already escaped authority.

## Verification obligations

Race accept, deadline and root death; replay an old boot-generation token; interrupt sealing. Check a single outcome, no simultaneous primary/fallback root and no usable bootstrap path in NormalOperation. Explicitly record which failure states require external restart.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Construction must preserve effect-bearing authority.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Bootstrap must provision an independently usable recovery path.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Microkit User Manual (v2.3.0)](../../../30-sources/sel4-foundation-2026-microkit-system-contracts.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [capDL Loader](../../../30-sources/sel4-foundation-2026-capdl-loader-contract.md) — comparative evidence; its methods and limits are recorded in the source note.
