---
title: "Containment escalation and terminal handoff"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Containment escalation and terminal handoff

Who may promote a fault into domain termination or a node-fatal decision?

## Research basis and status

Failure detection and proof-scope literature warn against treating a signal as a complete failure model. [1](../../../30-sources/chandra-toueg-1996-failure-detectors.md), [2](../../../30-sources/sel4-foundation-2026-proof-assumptions.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../fault-capture-and-containment.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Containment policy is a trusted, predeclared classification-to-authority mapping. Resolvable thread faults, fatal domain faults and kernel-integrity failures have different owners. The lower architecture layer owns the one terminal fatal protocol and its sealed CrashContext; this layer does not create a competing crash sink.

### Admission, transitions and completion

For a qualified domain-fatal class, invoke the existing close/stop lifecycle with its reserved execution and cleanup resources. For evidence that privileged invariants may be corrupt, hand off through the lower fatal route. Continuously maintained domain metadata may enrich that record only under the sealed context's restrictions. Unprivileged supervision chooses later restart strategy.

### Failure and adversarial behavior

A diagnostic subscriber cannot obtain termination authority by interpreting a severe-looking event. Recursive faults must not allocate, acquire ordinary locks or wait for remote services. If stop cannot establish safe kernel checkpoints, limiting the report to domain failure would falsely claim containment.

### Alternatives and unresolved tradeoffs

Aggressive escalation protects integrity but reduces availability. Narrow containment preserves service only when the trust boundary and fault classification justify it. Make this tradeoff a reviewed profile, not an ad hoc handler decision during a damaged state.

## Verification obligations

Feed the same raw event under profiles with different justified scopes; attempt escalation with observer-only authority; fault during capture and during stop. Verify a single authoritative terminal route and explicit uncertainty when evidence cannot establish domain-local containment.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [SMP stop and completion evidence](../protection-domains-threads-and-address-spaces/smp-stop-and-completion-evidence.md) — Fatal domain handling uses the existing stop protocol.
- [Post-seal crash enrichment](../observability-and-crash-evidence/post-seal-crash-enrichment.md) — Higher-level evidence enriches, but never replaces, lower fatal capture.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Unreliable failure detectors for reliable distributed systems](../../../30-sources/chandra-toueg-1996-failure-detectors.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [What the Proofs Assume](../../../30-sources/sel4-foundation-2026-proof-assumptions.md) — comparative evidence; its methods and limits are recorded in the source note.
