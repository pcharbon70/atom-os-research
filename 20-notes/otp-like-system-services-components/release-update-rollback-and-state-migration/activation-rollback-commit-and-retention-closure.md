---
title: "Activation, rollback commit, and retention closure"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Activation, rollback commit, and retention closure

This study decomposes [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration.md).

Research question: When may the old generation and its evidence actually be destroyed?

## Research basis and status

Retained immutable generations enable selection rollback only while required
artifacts and compatible state remain available. [1](../../../30-sources/dolstra-et-al-2008-nixos.md) [2](../../../30-sources/chen-et-al-2015-fscq.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The release controller owns the active root, previous compatible root, rollout
outcome, point-of-no-return decision and retention claims. These claims include
sessions, callbacks, snapshots, retry outcomes, audit and roll-forward repair
assets.

### Admission, transitions and completion

Force the new root before publishing its selector through a crash-safe protocol.
Reobserve uncertain activation results. After observation, choose compatible
rollback, authorized roll-forward or quarantine. Commit ends only the declared
automatic rollback promise; reclamation still waits for every independent retention
obligation.

### Failure and adversarial behavior

Code rollback after irreversible schema or physical effects may be unsafe. A failed
restore must not overwrite evidence of the failed release. Garbage collection based
solely on 'not current' can remove the only means of resolving late retries or
recovering a mixed-version peer.

### Alternatives and unresolved tradeoffs

Long retention improves repair options at finite storage cost. Early commit reduces
footprint while narrowing recovery. Treat retention expiry as an explicit
authorization and admission constraint, not an incidental cache policy or an
implementation of retroactive cancellation.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash during selector publication and require recovery to select a fully durable root.
- Keep an old session and retry-result obligation after rollout commit; reclamation must preserve their required artifacts or perform an acknowledged handoff.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
