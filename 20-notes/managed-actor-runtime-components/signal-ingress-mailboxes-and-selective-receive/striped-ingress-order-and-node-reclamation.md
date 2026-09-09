---
title: "Striped ingress order and node reclamation"
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

# Striped ingress order and node reclamation

This study decomposes [Signal ingress, mailboxes and selective receive](../signal-ingress-mailboxes-and-selective-receive.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Sender-striped ingress is an ERTS contention optimization; safe reclamation remains a separate obligation from queue linearization. [1](../../../30-sources/winblad-2021-parallel-signal-sending.md), [2](../../../30-sources/michael-2004-hazard-pointers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Physical enqueue order, ordered signal delivery and selective mailbox placement are three separate contracts.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own stripe generations, sender-to-stripe assignment, drain cursors and producer pins. A queue backend must state its memory-ordering and reclamation assumptions. The actor-facing contract preserves each sender's signal order to a destination, not a global total order among senders.

### Admission, transitions and completion

Keep a sender on an order-preserving route within a stripe generation. When resizing or disabling stripes, drain the old route or establish a cutover barrier before its successor becomes eligible. The receiver drains bounded batches and retires detached nodes only after producers/readers can no longer access them.

### Failure and adversarial behavior

A queue implementation can be linearizable yet violate actor ordering if one sender migrates paths between signals. A stale producer can corrupt a recycled dummy node. Coalesced wakeups require a check-before-sleep protocol so a nonempty ingress cannot remain asleep indefinitely.

### Alternatives and unresolved tradeoffs

One locked ingress is a useful correctness and low-contention baseline. Adaptive striping spends metadata and scan work to relieve measured enqueue contention. Queue length alone is not evidence of contention; unmatched receive backlog may be the real bottleneck.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Send ordered pairs across every stripe cutover and reject inversions.
- Suspend a producer holding a node reference while draining and recycling nodes.
- Race last-drain, receiver sleep and new publication to test lost wakeups.

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

1. [Parallel signal sending](../../../30-sources/winblad-2021-parallel-signal-sending.md).
2. [Hazard pointers](../../../30-sources/michael-2004-hazard-pointers.md).
