---
title: "Operation-result ledger, retry rendezvous, and expiry"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Operation-result ledger, retry rendezvous, and expiry

This study decomposes [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery.md).

Research question: How can duplicate suppression remain bounded without executing an old operation again?

## Research basis and status

RIFL couples mutations with durable results and rejects stale leased clients after
safe result reclamation. [1](../../../30-sources/lee-et-al-2015-rifl.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The result service owns logical operation identity, authenticated principal binding,
request digest, in-progress state, terminal result and retention validity. Delivery
references and service incarnations may change without creating a new logical
operation.

### Admission, transitions and completion

Atomically admit the operation and its retention reservation. Commit mutation and
result together where the store owns both. Concurrent duplicates attach to the same
pending record; status can progress from Accepted to Committed without reexecution.
Migration transfers result ownership with the state or installs a durable
rendezvous.

### Failure and adversarial behavior

After result collection, the original operation must be rejected as stale or
resolved through retained evidence, never treated as unseen new work. A new
transport session or a fenced writer does not prove the prior attempt absent.
External sinks require their own deduplication/status contract.

### Alternatives and unresolved tradeoffs

Keeping every result forever simplifies retries but is unbounded.
Lease/acknowledgement collection requires trustworthy expiry or durable sequence
frontiers. Client-state loss remains indeterminate. Define future retention promises
at admission, not opportunistically under space pressure.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Retry after result collection and prove the stale identity cannot cause a second mutation.
- Move an object with an in-progress request, lose the forwarding reply, and verify one outcome owner remains discoverable.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Device-service policy and management](../device-service-policy-and-management/README.md) — settles hardware outcomes and buffer custody.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
