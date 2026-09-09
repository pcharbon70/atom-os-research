---
title: "Scoped inspection and redacted cursors"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Scoped inspection and redacted cursors

How can an inspector traverse changing kernel state without gaining ambient authority or holding objects forever?

## Research basis and status

Capability mechanisms support scoped access; safe observation additionally requires explicit lifetime and resource bounds. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md), [2](../../../30-sources/michael-2004-hazard-pointers.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../observability-and-crash-evidence.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

An inspection capability constrains target set, fields, depth, rate and lifetime. A cursor identifies a protected snapshot or bounded traversal generation, not a raw kernel pointer. Each page of results has its own authorization and pin lifetime, paid by the observation account.

### Admission, transitions and completion

At each page request, revalidate current inspection rights and cursor generation, acquire bounded pins, copy redacted values into caller-owned output and release pins before returning. If a consistent global view is required, create a separately funded immutable snapshot with explicit scope; ordinary cursor results may instead report intervening changes.

### Failure and adversarial behavior

Checking authority only at cursor creation can leak data after inspection is revoked. Returning addresses can expose layout and invite accidental reuse as capabilities. A malicious reader that never advances must not keep an unbounded object graph live or consume the recovery reserve.

### Alternatives and unresolved tradeoffs

Weakly consistent paginated views are economical and sufficient for many diagnostics but cannot justify a global invariant claim. Strong snapshots are more expensive and need bounded capture semantics. Both must distinguish missing, redacted, changed and lost data.

## Verification obligations

Revoke inspection mid-cursor, close target objects, exhaust output capacity and hold readers indefinitely. Verify bounded retention, per-page checks and explicit consistency limitations. Attempt to invoke a reported identity in another CSpace and require failure.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Containment escalation and terminal handoff](../fault-capture-and-containment/containment-escalation-and-terminal-handoff.md) — One lower terminal protocol owns fatal disposition.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Reading evidence needs a real backing-storage lifetime.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Hazard pointers: Safe memory reclamation for lock-free objects](../../../30-sources/michael-2004-hazard-pointers.md) — comparative evidence; its methods and limits are recorded in the source note.
