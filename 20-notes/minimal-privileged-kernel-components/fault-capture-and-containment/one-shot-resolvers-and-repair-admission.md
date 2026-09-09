---
title: "One-shot resolvers and repair admission"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# One-shot resolvers and repair admission

What authority lets a fault handler repair one blocked thread without gaining ambient control over its domain?

## Research basis and status

Capability-mediated fault handling suggests narrow repair authority, but the proposed resolver has stricter identity and outcome rules. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../fault-capture-and-containment.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A Resolver names one fault record, thread and address-space generation, allowed repair operations, deadline policy and a single-use outcome state. The handler also needs independently valid frame or other effect-bearing authority for products it creates. A resolver is not a reusable debug or lifecycle capability.

### Admission, transitions and completion

Admit only the allowed repair against the still-current fault and closed/open domain gates. Commit the repair before consuming the successful resume transition; competing expiry, abort and domain close select a single result. A mapping created through FaultMap inherits its actual frame/address-space lifetime dependencies, not automatically the ephemeral resolver that merely authorized this admission.

### Failure and adversarial behavior

Expired repair authority must not resume a replacement thread sharing a numeric identifier. A failed repair or consumed token leaves the thread blocked unless another authorized transition applies. Token expiry does not itself prove corruption or authorize domain death.

### Alternatives and unresolved tradeoffs

Allowing arbitrary register or address-space editing makes a resolver convenient but equivalent to broad debugging power. A typed repair family is narrower and easier to model. More complex recovery can use separately granted debug authority without disguising it as ordinary page-fault resolution.

## Verification obligations

Race repair commit, expiry, duplicate use and domain close; replace the target generation; omit frame authority. Verify one outcome, no stale resume and correct lifetime inheritance for a successful repair product.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [SMP stop and completion evidence](../protection-domains-threads-and-address-spaces/smp-stop-and-completion-evidence.md) — Fatal domain handling uses the existing stop protocol.
- [Post-seal crash enrichment](../observability-and-crash-evidence/post-seal-crash-enrichment.md) — Higher-level evidence enriches, but never replaces, lower fatal capture.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
