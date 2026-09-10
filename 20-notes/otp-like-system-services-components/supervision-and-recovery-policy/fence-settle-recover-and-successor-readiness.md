---
title: "Fence, settle, recover, and successor readiness"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Fence, settle, recover, and successor readiness

This study decomposes [Supervision and recovery policy](../supervision-and-recovery-policy.md).

Research question: What distinguishes a restarted process from a recovered service?

## Research basis and status

Fine-grained restart requires state separation; retained outcome records support
retry without duplicating completed mutations. [1](../../../30-sources/candea-et-al-2004-microreboot.md) [2](../../../30-sources/lee-et-al-2015-rifl.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The recovery executor owns a child attempt, sink-fence receipts, teardown
obligations, durable recovery frontier and readiness evidence. It consumes kernel
and device settlement proofs rather than manufacturing them from actor monitor
messages.

### Admission, transitions and completion

Close admission, fence the old writer at relevant sinks, settle or quarantine
retained resources, recover authoritative state and reconcile unresolved operations.
Construct the successor privately with fresh handles. Publication requires its exact
state frontier, dependency revisions and permissions, not merely a successful start
callback.

### Failure and adversarial behavior

A reply lost during fencing or publication remains unknown until reobserved.
Resource quarantine can block a successor even after the old actor dies. Duplicate
operations must rendezvous with retained outcomes across the new placement;
generation change alone cannot erase them.

### Alternatives and unresolved tradeoffs

Recover-before-start minimizes application-visible uncertainty but increases outage
time. Restricted read-only recovery mode may restore partial availability if
explicitly typed. Never offer full Ready while write ownership or required outcomes
remain unresolved.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash between fence, state replay and publication; verify no two current writers and no lost retry record.
- Let the new process run while storage recovery is incomplete; its public write endpoint must remain unavailable.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance/README.md) — budgets retained work, retries and recovery.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
