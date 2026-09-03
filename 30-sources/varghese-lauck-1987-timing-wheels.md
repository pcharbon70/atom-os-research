---
title: "Hashed and hierarchical timing wheels: Data structures for the efficient implementation of a timer facility"
kind: source
created: "2026-09-03"
authors:
  - "George Varghese"
  - "Tony Lauck"
published: 1987
citation_key: "varghese-lauck-1987-timing-wheels"
container: "11th ACM Symposium on Operating Systems Principles"
edition: "SOSP '87, 25-38"
isbn: "0-89791-242-X"
doi: "10.1145/41457.37504"
url: "https://www.cs.columbia.edu/~nahum/w6998/papers/sosp87-timing-wheels.pdf"
accessed: "2026-09-03"
tags:
  - data-structures
  - operating-systems
  - timekeeping
  - timers
aliases:
  - "Hierarchical timing wheels"
---

# Hashed and hierarchical timing wheels: Data structures for the efficient implementation of a timer facility

## Reference

George Varghese and Tony Lauck. “[Hashed and Hierarchical Timing Wheels: Data
Structures for the Efficient Implementation of a Timer
Facility](https://doi.org/10.1145/41457.37504).” *11th ACM Symposium on
Operating Systems Principles*, pages 25–38, 1987. [Paper
copy](https://www.cs.columbia.edu/~nahum/w6998/papers/sosp87-timing-wheels.pdf).

## Research question or contribution

The paper classifies timer data structures by the costs of starting, stopping,
and maintaining many outstanding timers. It introduces hashed and hierarchical
timing-wheel variants to avoid linear scans and priority-queue costs where
bounded clock granularity is acceptable.

## Method

The authors compare seven schemes analytically, relate timer maintenance to
sorting and discrete-event simulation, and work through cost and storage
trade-offs for different interval distributions and tick mechanisms.

## Findings

- A circular wheel can make start, stop, and per-tick operations constant time
  for deadlines within its range.
- Hashing extends the range but trades insertion ordering against work when a
  slot expires.
- A hierarchy of wheels gives large range through coarse placement at distant
  horizons and refinement as time advances. Cascading a populated slot can
  migrate many timers, so migration cost is workload- and distribution-
  dependent rather than a per-level worst-case bound.
- Complexity claims depend on wheel geometry, timer distribution, expiry
  bursts, cancellation representation, and a tick or equivalent advancement
  mechanism. Many timers in one slot can still create a large expiry batch.

## Relevance

The work supports per-scheduler hierarchical wheels for ordinary actor timers,
with a small exact near-deadline structure and one or a few kernel deadline
channels. Atom OS adds requirements absent from the original data structure:
generation-stamped references, cancellation/fire linearization, monotonic-era
handling, bounded expiry batches, actor/resource charging, and sticky overflow
telemetry.

## Limits

The paper predates multicore runtimes and does not specify BEAM timer
semantics, late-delivery behavior, cancellation races with mailbox publication,
tickless hardware, clock discontinuity, or adversarial timer bursts. Its
algorithmic result chooses a candidate structure; measurements must select
wheel levels, granularity, shard count, and heap crossover for Atom OS.

## Derived work

- [Timers, events, and asynchronous I/O integration](../20-notes/managed-actor-runtime-components/timers-events-and-asynchronous-io-integration.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
