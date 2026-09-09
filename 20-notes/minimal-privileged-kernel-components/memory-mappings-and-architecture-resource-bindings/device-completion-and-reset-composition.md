---
title: "Device completion and reset composition"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Device completion and reset composition

Which evidence can release a device effect, especially when recovery authority changes mid-operation?

## Research basis and status

The formal-proof assumptions and device-interface research constrain any claim that logical revocation proves physical completion. [1](../../../30-sources/sel4-foundation-2026-proof-assumptions.md), [2](../../../30-sources/markettos-et-al-2019-thunderclap.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../memory-mappings-and-architecture-resource-bindings.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A DeviceCompletionToken names the immutable profile, device/resource generations, operation epoch and exact completed postcondition. ResetControl and ResetLease govern a reset scope that may include several functions. Domain recovery authority does not automatically grant permission for that collateral effect.

### Admission, transitions and completion

Admit reset or drain using both the current required lease and independently held target authority. Execute the profile's dependency graph, which may retain DMA translations through a device-specific drain/reset stage. Match each lower-layer completion to its original operation identity. A successor manager may adopt a valid late completion from the old operation while its own authority epoch governs subsequent mutations.

### Failure and adversarial behavior

Relabeling an old completion with the new manager epoch hides whether it matches the original device action. A driver-written done flag or elapsed timeout is not proof of quiescence. Repeating a non-idempotent reset stage after uncertain progress can introduce a second collateral failure.

### Alternatives and unresolved tradeoffs

A universal unmap-then-reset sequence is attractive but unsound across device classes. Typed profile-specific graphs are more explicit and auditable, although they enlarge qualification work. When the profile cannot prove completion, retain exact confined resources or escalate.

## Verification obligations

Take over management between every profile stage; deliver duplicate, stale and correctly delayed tokens; fail a shared reset. Require exact operation attribution, no unauthorized collateral reset and no frame or IOVA reuse until the applicable completion conditions hold.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [What the Proofs Assume](../../../30-sources/sel4-foundation-2026-proof-assumptions.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
