---
title: "Hierarchical timer queues and bounded cascade"
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

# Hierarchical timer queues and bounded cascade

This study decomposes [Timers, events and asynchronous I/O integration](../timers-events-and-asynchronous-io-integration.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Timing-wheel analysis exposes range/granularity tradeoffs and burst work; resource attribution applies to timer metadata and delivery work, not only payload bytes. [1](../../../30-sources/varghese-lauck-1987-timing-wheels.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime owns timer and actor semantics; the kernel supplies qualified time and deadline events, not one kernel timer per actor.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own wheel geometry, near-deadline structure, shard generation, occupancy hints and a resumable cascade cursor. Store one charge and one authoritative owner for each timer even while it moves between levels or workers.

### Admission, transitions and completion

Insert distant deadlines into coarse levels and refine them toward expiry; use exact comparisons before publishing a due result. Bound advancement and cascade work per activation. Tickless skipping consults validated occupancy state; a stale hint may cause extra scanning but never skip a real due timer.

### Failure and adversarial behavior

A million deadlines in one slot still require substantial expiry work. Describing insertion as constant-time does not bound a burst or guarantee timely message consumption. Reconfiguration must prevent duplicates and missed timers across old/new queue generations.

### Alternatives and unresolved tradeoffs

A binary heap is a useful simple reference with predictable ordering costs. Wheels reduce routine operations under suitable distributions but add geometry and cascade complexity. Measure cancellation-heavy, synchronized-expiry and long-horizon loads before choosing parameters.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Place all timers in one bucket and verify bounded slices plus eventual delivery under stated budget.
- Advance time across many empty levels without skipping occupied slots.
- Migrate a shard during cancellation and account each timer exactly once.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Timeout consumption and receive races](../signal-ingress-mailboxes-and-selective-receive/selective-receive-cursors-markers-and-timeouts.md) — a contract this service must compose with.
- [External request disposition](../native-work-ports-and-drivers/native-request-outcomes-and-cancellation-drain.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Hashed and hierarchical timing wheels](../../../30-sources/varghese-lauck-1987-timing-wheels.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
