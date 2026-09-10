---
title: "Operator-action facets, probe bounds, and break-glass"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Operator-action facets, probe bounds, and break-glass

This study decomposes [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control.md).

Research question: How can recovery tooling remain powerful without becoming permanent ambient privilege?

## Research basis and status

Capability attenuation limits delegation; DTrace demonstrates constrained
instrumentation rather than a universal worst-case execution proof. [1](../../../30-sources/miller-et-al-2003-capability-myths.md) [2](../../../30-sources/cantrill-et-al-2004-dtrace.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The gateway owns operation-specific facets, target generations, field visibility,
magnitude limits, expiry and action-result identities. Probe admission owns finite
instruction, memory, event-rate and lifetime budgets. Forced containment belongs to
an external lifecycle holder.

### Admission, transitions and completion

Authenticate the actual holder, validate current revocation state and bind each
action to target and request digest. Atomically record one-shot admission in an
outcome ledger; exact replay returns the same evolving outcome rather than executing
again. Verify probes before attachment and permit only declared observation effects.

### Failure and adversarial behavior

Inspect must not imply arbitrary state mutation, secret reveal or device reset. A
probe that is memory-safe can still overwhelm a hot path; charge execution and
disable on limit. Identity-service loss cannot justify an unauthenticated emergency
console; break-glass authority must be pre-established and audited.

### Alternatives and unresolved tradeoffs

Fine-grained facets require more policy configuration but constrain compromise.
Broad operator roles are simpler yet expand blast radius. Dual approval can reduce
unilateral risk without proving action correctness; choose it for explicit high-risk
operations and preserve an independent evidence path.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Replay a reset or release-activation request after losing its reply; the gateway must query the original outcome rather than repeat the action.
- Attach a high-rate probe and exhaust its budget; ordinary service and recovery progress must remain protected.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets/README.md) — supplies configuration adoption and credential-generation evidence.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [DTrace](../../../30-sources/cantrill-et-al-2004-dtrace.md).
