---
title: "Changeset validation, migration, and atomic publication"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - dynamic-software-update
  - live-programming
  - state-migration
aliases: []
---

# Changeset validation, migration, and atomic publication

This study decomposes [Capability-scoped live tools and transactional evolution](../capability-scoped-live-tools-and-transactional-evolution.md).

Research question: What evidence and transition protocol make a live code or
schema change publishable, recoverable, and honest about irreversible effects?

## Research basis and status

Proteus and practical DSU research constrain update points and state
transformation. Fault-tolerant time-traveling state transfer isolates versions
and validates migrations. ARIES and Sagas distinguish durable recovery records
from domain compensation. [1](../../../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md)
[2](../../../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md)
[3](../../../30-sources/giuffrida-et-al-2013-fault-tolerant-live-update.md)
[4](../../../30-sources/mohan-et-al-1992-aries.md)
[5](../../../30-sources/garcia-molina-salem-1987-sagas.md)

No Atom changeset state machine has been implemented.

## Development

### Owned state and trust boundary

The changeset service owns immutable artifacts, author, target scope, base
code/schema/policy generations, requested authority, semantic diff, migration,
tests, resource delta, compatibility, rollback, compensation, and expiry.
Validation workers cannot commit; the smaller coordinator accepts only typed
receipts from approved workers.

### Admission, transitions, and completion

Stage seals artifacts, validate checks provenance, type/interface, authority,
migration, behavior, resources, and applicable canaries. Commit rechecks every
base generation, quiesces only declared targets, persists intent, prepares
candidate state in isolation, and atomically publishes code/state generations.
Unknown outcomes reconcile by change ID.

### Failure and adversarial behavior

Migration crash, stale validation, hidden authority growth, old/new version
message mismatch, irreversible external effects, and false rollback claims are
expected. Old state remains protected until commit proof and retention closure.
Code rollback, data restoration, compensation, and forward repair are distinct.

### Alternatives and unresolved tradeoffs

Arbitrary immediate mutation maximizes liveness but makes safety unknowable.
Restart-only deployment simplifies state but loses continuity. Transactional
scope-specific change is preferred; supported update granularity and safe-point
availability remain empirical.

## Verification obligations

- Kill editor, validator, coordinator, target, and store before/after every
  lifecycle record; each change ID reaches one honest outcome.
- Change code, schema, policy, and authority after preview; stale evidence must
  fail or be explicitly rebased and rerun.
- Attempt code rollback after forward-only migration and observed external
  effect; the system must refuse false reversal and present valid repair paths.

## Connections

- [Internal-service index](README.md) — transactional live tools.
- [Tool publication](tool-packaging-provenance-rollout-and-recovery.md) — reusable release stage.
- [Release system services](../../otp-like-system-services-components/release-update-rollback-and-state-migration/README.md) — deployment coordination.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — source manifest.

## Sources

1. [Mutatis Mutandis](../../../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md).
2. [Practical dynamic software updating](../../../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md).
3. [Fault-tolerant live update](../../../30-sources/giuffrida-et-al-2013-fault-tolerant-live-update.md).
4. [ARIES](../../../30-sources/mohan-et-al-1992-aries.md).
5. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
