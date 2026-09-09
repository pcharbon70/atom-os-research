---
title: "Fault taxonomy and bounded capture"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Fault taxonomy and bounded capture

How can the kernel record a fault without overstating either its cause or its containment?

## Research basis and status

Failure-detector theory distinguishes suspicion from certainty; local hardware reports also require profile-specific interpretation. [1](../../../30-sources/chandra-toueg-1996-failure-detectors.md), [2](../../../30-sources/sel4-foundation-2026-proof-assumptions.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../fault-capture-and-containment.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A preallocated FaultRecord contains source and normalized code, object and thread generations, CPU identity, clock information, certainty class, containment state, operation identity and loss status. The record distinguishes proven local conditions, reported conditions and liveness suspicion. Observation rights do not grant repair or lifecycle authority.

### Admission, transitions and completion

Copy the lower architecture's bounded captured facts into the authorized fault schema, preserving raw classification where safe. Apply only the trusted normalization profile; do not dereference arbitrary user addresses to improve the diagnosis. Ordinary invalid user arguments may be a syscall result rather than a fatal fault. Publish a committed record or explicit loss marker without allocation.

### Failure and adversarial behavior

A runtime-reported actor crash is not proof of kernel or domain corruption. A missed heartbeat can be caused by starvation, and a device error report may not locate the full damaged region. Recursively faulting during evidence collection must fall back to the lower terminal protocol rather than invoking the same unsafe reader again.

### Alternatives and unresolved tradeoffs

Rich diagnostics help diagnosis but enlarge data exposure and capture cost. Prefer a small authoritative record with optional premaintained enrichment. Interpretive symbolization and large memory inspection belong in an independently authorized service.

## Verification obligations

Inject malformed exception state, user-copy faults, runtime reports and delayed heartbeats. Check correct certainty and scope labels, bounded capture under memory exhaustion and no promotion from observer to repair authority.

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
