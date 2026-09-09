---
title: "Selective receive cursors, markers and timeouts"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Selective receive cursors, markers and timeouts

This study decomposes [Signal ingress, mailboxes and selective receive](../signal-ingress-mailboxes-and-selective-receive.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Selective receive examines candidates under language matching rules; systematic testing shows why receive boundaries need explicit scheduling instrumentation. [1](../../../30-sources/hogberg-2021-message-passing.md), [2](../../../30-sources/christakis-et-al-2013-concuerror.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Physical enqueue order, ordered signal delivery and selective mailbox placement are three separate contracts.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the current receive expression, partition-aware scan cursor, saved unmatched position, timeout identity and validated fresh-reference marker. Cursor terms and code continuations are collector roots. The signal service still owns arrival and placement.

### Admission, transitions and completion

Scan messages in the declared mailbox order and clauses in source order, charging candidate and guard work. On budget exhaustion, save a resumable cursor. Recheck priority insertion as required before concluding no match. A compiler-derived marker may skip older messages only when the verifier proves they cannot match the fresh reference.

### Failure and adversarial behavior

An arbitrary pattern index can skip the first matching message or mishandle guard semantics. A stale cursor after GC, alias change or priority insertion can lose messages. Timeout selection must race with eligible message visibility under the exact profile, not an invented wall-clock ordering.

### Alternatives and unresolved tradeoffs

Full scanning is predictable semantically but costly under unmatched backlog. Reference markers are a narrow optimization, not a general mailbox index. Track oldest age and scan work independently from queue count to diagnose overload.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Retain unmatched messages across yields, GC and code change; select the correct first match.
- Insert a priority message during a suspended scan.
- Explore receive-timeout and message-visibility races with replayable schedules.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Relation state ownership](../actor-identity-lifecycle-and-process-state/links-monitors-aliases-and-name-registration.md) — a contract this service must compose with.
- [Payload lifetime and adoption](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [A few notes on message passing](../../../30-sources/hogberg-2021-message-passing.md).
2. [Concuerror](../../../30-sources/christakis-et-al-2013-concuerror.md).
