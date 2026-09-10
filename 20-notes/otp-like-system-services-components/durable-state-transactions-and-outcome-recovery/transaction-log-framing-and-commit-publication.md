---
title: "Transaction-log framing and commit publication"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Transaction-log framing and commit publication

This study decomposes [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery.md).

Research question: How can recovery distinguish a committed transaction from a plausible but incomplete log tail?

## Research basis and status

Crash-specified logging and atomic mutation/result coupling motivate a precise
commit record rather than a success flag. [1](../../../30-sources/chen-et-al-2015-fscq.md) [2](../../../30-sources/lee-et-al-2015-rifl.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The writer owns bounded transaction buffers, contiguous store LSNs, frame checksums,
transaction digests and the current logical state root. It is the sole writer for
its store generation. Client namespace capabilities constrain which objects a
transaction may affect.

### Admission, transitions and completion

Reserve log and retained-result capacity before acceptance. Append canonical frames
and a commit record covering exact ordered count, range and digest. Force the
profile-required predecessors and commit before acknowledging durability. Publish
in-memory visibility consistently with that durable decision.

### Failure and adversarial behavior

An intact commit frame cannot validate missing earlier mutation frames. Stop at a
broken contiguous prefix instead of searching arbitrary later bytes for another
header. Space exhaustion before commit leaves an uncommitted attempt, while a lost
reply after commit requires outcome lookup.

### Alternatives and unresolved tradeoffs

Single-writer copy-on-write state avoids in-place undo complexity but limits write
concurrency. An ARIES-like concurrent design would require additional page, locking
and recovery contracts; the simple protocol cannot inherit those properties by
analogy.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Remove or duplicate a middle mutation while preserving Commit; recovery must reject the incomplete transaction.
- Crash after durable commit before acknowledgement and retry with the same ID; exactly the retained mutation and result must be visible.

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

1. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
