---
title: "Private object construction transaction"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Private object construction transaction

Where is the boundary between initialization that can roll back and authority that has escaped?

## Research basis and status

Verified initialization research supplies a useful model-to-configuration precedent, with explicitly limited implementation assurance. [1](../../../30-sources/boyton-et-al-2013-verified-system-initialisation.md), [2](../../../30-sources/sel4-foundation-2026-capdl-loader-contract.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bootstrap-and-root-authority-handoff.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A private construction transaction owns unpublished objects and reservation receipts. It does not expose selectors to running domains or allow hardware submission. Private object state can be destroyed through type-specific bounded cleanup because no external actor has yet acquired an activation, mapping or queue effect.

### Admission, transitions and completion

Construct typed objects in dependency order, initialize their generation and payer records, and attach required lifetime dependencies before any capability becomes visible. Keep construction receipts separate from the future public object graph. A failure walks only initialized receipts, restoring reservations exactly once. At the publication boundary, transfer responsibility to the normal lifetime and teardown protocols rather than retaining a second bootstrap destructor.

### Failure and adversarial behavior

A constructor that starts a timer, publishes a page table to a running CPU, or exposes a capability has crossed the private boundary even if a global boot flag still says initializing. Such effects require an explicitly modeled publication stage; ordinary rollback cannot erase their history. Retrying after uncertain publication must not duplicate roots.

### Alternatives and unresolved tradeoffs

A single giant transaction makes atomicity simple on paper but creates long non-preemptible work. Private staged construction with fixed-size operations is preferable, provided its final publication and failure semantics are explicit. The transaction model still needs refinement to actual Zig control flow and memory operations.

## Verification obligations

Inject failure after each object initialization and receipt update. Check exact quota restoration, no double destruction and no reachable half-initialized header. Force a simulated publication race and require the post-publication terminal path instead of private rollback.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Construction must preserve effect-bearing authority.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Bootstrap must provision an independently usable recovery path.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Formally verified system initialisation](../../../30-sources/boyton-et-al-2013-verified-system-initialisation.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [capDL Loader](../../../30-sources/sel4-foundation-2026-capdl-loader-contract.md) — comparative evidence; its methods and limits are recorded in the source note.
