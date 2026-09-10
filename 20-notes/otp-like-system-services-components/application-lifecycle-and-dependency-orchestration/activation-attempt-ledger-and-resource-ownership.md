---
title: "Activation-attempt ledger and resource ownership"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Activation-attempt ledger and resource ownership

This study decomposes [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration.md).

Research question: How does failed activation clean up only what it created?

## Research basis and status

Version-sensitive reconciliation and attenuated authority motivate explicit
ownership of preparation effects. [1](../../../30-sources/sun-et-al-2024-anvil.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The lifecycle service owns bundle generation, attempt ID, provisional resources and
adapter receipts. Shared dependencies have independent owners and borrowed
references. The attempt ledger distinguishes newly created, borrowed, transferred
and quarantined objects.

### Admission, transitions and completion

Persist one intent per effectful step with expected revisions. After an interrupted
request, reobserve using the original operation ID. Cleanup walks owned objects in a
dependency-safe order, awaiting terminal and reclamation evidence. An existing
application borrowed by this attempt is never included in rollback destruction.

### Failure and adversarial behavior

Lost create replies cannot justify issuing a new identity and leaking the first
object. Lost cleanup replies cannot justify assuming resources are free. A partially
completed external transaction is delegated to its outcome owner rather than deleted
with the local attempt record.

### Alternatives and unresolved tradeoffs

One generic resource list is attractive but hides object-specific settlement
conditions. Typed receipts cost schema work yet permit precise recovery. Decide
retention from unresolved effects and durable retry promises, not from the lifetime
of the orchestration actor.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash after creating an endpoint but before receiving its handle; recovery must discover or quarantine the same object.
- Fail a consumer activation that borrowed a running provider and verify cleanup leaves the provider intact.

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

1. [Anvil](../../../30-sources/sun-et-al-2024-anvil.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
