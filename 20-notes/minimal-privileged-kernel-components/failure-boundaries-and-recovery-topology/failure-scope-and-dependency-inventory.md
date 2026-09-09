---
title: "Failure scope and dependency inventory"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Failure scope and dependency inventory

Which apparently separate components must actually fail or recover together?

## Research basis and status

CuriOS demonstrates that protection and state organization both affect recovery; address-space separation alone is insufficient. [1](../../../30-sources/david-et-al-2008-curios.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../failure-boundaries-and-recovery-topology.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The deployment inventory distinguishes actor, managed-runtime domain, native service, correlated shared-root group, device-reset group, node and external dependency. It records authority, mutable shared state, ordinary and recovery resource paths, and external effects. This is configuration evidence, not a kernel service-name registry.

### Admission, transitions and completion

Before granting execution eligibility, identify which dependencies survive each declared failure scope. Check that cleanup authority, CPU reserve, slots and fault routes do not derive from the child or replaceable supervisor. Represent conditional failure authority too: passive-call cancellation may terminate an accepting server under its declared policy. Preserve separate kernel object generations and user-space service epochs.

### Failure and adversarial behavior

Two domains can share mutable state or a reset scope that lets one failure damage the other. A supervisor waiting on its child for memory or scheduling capacity is not independent. A timeout may justify a policy takeover, but it does not prove the old manager has stopped or that external state is consistent.

### Alternatives and unresolved tradeoffs

Large recovery groups simplify dependency reasoning but increase disruption. Fine-grained restart requires more explicit state and authority boundaries. The correct group is determined by actual shared effects, not the names assigned to processes.

## Verification obligations

Introduce shared roots, reset collateral, a child-owned fault route and cyclic recovery dependency. Require the inventory to reject the proposed independence or name the correlated group. Test mistaken failure suspicion while the old component remains executable.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sealed use facets and epoch sessions](../capability-spaces-and-authority/sealed-use-facets-and-epoch-sessions.md) — Lease enforcement relies on protected facets and closed sessions.
- [Charged reaper and resumable cursors](../teardown-revocation-and-safe-reclamation/charged-reaper-and-resumable-cursors.md) — A successor must continue the same teardown operation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [CuriOS: Improving reliability through operating system structure](../../../30-sources/david-et-al-2008-curios.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Unreliable failure detectors for reliable distributed systems](../../../30-sources/chandra-toueg-1996-failure-detectors.md) — comparative evidence; its methods and limits are recorded in the source note.
