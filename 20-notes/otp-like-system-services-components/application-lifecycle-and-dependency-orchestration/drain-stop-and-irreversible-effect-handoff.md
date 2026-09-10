---
title: "Drain, stop, and irreversible-effect handoff"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Drain, stop, and irreversible-effect handoff

This study decomposes [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration.md).

Research question: When can a bundle be retired rather than merely stopped?

## Research basis and status

Durable outcome ownership must outlive disposable execution; withdrawing authority
cannot reverse earlier effects. [1](../../../30-sources/lee-et-al-2015-rifl.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The drain coordinator owns the admission-close revision, accepted-operation
frontier, shutdown ordering and custodians for unresolved effects. Actor death,
namespace withdrawal, capability revocation and device quiescence are independently
recorded milestones.

### Admission, transitions and completion

Close admission atomically before enumerating accepted work. Complete,
cancel-before-effect or durably transfer every obligation; transfer is acknowledged
by a successor or custodian before the old owner releases it. Stop in the typed
dependency order and retire only after required settlement proofs.

### Failure and adversarial behavior

A drain timeout permits forceful fencing but not a fabricated cancellation result.
Compensation is new authorized work whose domain meaning comes from Layer 5. A
stopped service with pending remote outcomes remains represented by retained records
and a status route.

### Alternatives and unresolved tradeoffs

Long drains improve outcome certainty but retain old code and resources. Forced
termination shortens execution lifetime while potentially increasing quarantine.
Choose deadlines and transfer support per operation class instead of assuming every
queue can simply be discarded.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Race admission close with a new request; each request must be either rejected or included in the drain frontier.
- Kill the old owner during obligation transfer; exactly one custodian must remain accountable even when execution outcome is unknown.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller/README.md) — reconciles desired service generations within the boot envelope.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
