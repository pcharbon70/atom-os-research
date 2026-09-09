---
title: "Event schema and static probe control"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Event schema and static probe control

What diagnostic information may privileged code emit, at whose expense and under which authority?

## Research basis and status

DTrace demonstrates the value of correlated instrumentation; its programmable scope is not a requirement for this kernel. [1](../../../30-sources/cantrill-et-al-2004-dtrace.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../observability-and-crash-evidence.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

KernelEvent has a fixed schema version, event kind, object generations, operation identity, clock profile/era, certainty, containment state, loss flags and redaction class. TraceControl limits targets, fields, rate, destination, payer and filter generation. Health observation, debug inspection, lifecycle control and crash export remain distinct capabilities.

### Admission, transitions and completion

Enable only reviewed static probe sites and bounded field selection. Validate the control capability before installing an immutable probe configuration, then charge enabled work to an accepted observation account. Each event references the configuration generation that selected its fields. A disabled probe must have a measured, understood cost rather than an assumed zero-cost claim.

### Failure and adversarial behavior

A field such as a pointer, capability identifier or cross-domain timing sample can leak information despite being labeled diagnostic. Arbitrary kernel bytecode would add validation and execution obligations not present in the baseline. Losing events must be explicit rather than disguised by a monotonic event counter alone.

### Alternatives and unresolved tradeoffs

Fixed event types constrain exploratory debugging but keep the trusted execution path small. Rich aggregation and symbolization can run unprivileged on authorized records. Expanding the probe vocabulary requires an authority, cost and data-exposure review.

## Verification obligations

Attempt unauthorized fields and destinations, saturate the rate budget and change filters during production. Require correct generation tags, bounded work and no diagnostic-to-control escalation. Measure enabled and disabled costs separately under representative event density.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Containment escalation and terminal handoff](../fault-capture-and-containment/containment-escalation-and-terminal-handoff.md) — One lower terminal protocol owns fatal disposition.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Reading evidence needs a real backing-storage lifetime.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Dynamic instrumentation of production systems](../../../30-sources/cantrill-et-al-2004-dtrace.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Resource containers: A new facility for resource management in server systems](../../../30-sources/banga-et-al-1999-resource-containers.md) — comparative evidence; its methods and limits are recorded in the source note.
