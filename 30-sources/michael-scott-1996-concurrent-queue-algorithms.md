---
title: "Simple, fast, and practical non-blocking and blocking concurrent queue algorithms"
kind: source
created: "2026-09-03"
authors:
  - "Maged M. Michael"
  - "Michael L. Scott"
published: 1996
citation_key: "michael-scott-1996-concurrent-queues"
container: "15th ACM Symposium on Principles of Distributed Computing"
edition: "PODC '96, 267-275"
isbn: null
doi: "10.1145/248052.248106"
url: "https://www.cs.rochester.edu/~scott/papers/1996_PODC_queues.pdf"
accessed: "2026-09-03"
tags:
  - concurrent-data-structures
  - mailboxes
  - message-passing
  - synchronization
aliases:
  - "Michael-Scott queues"
---

# Simple, fast, and practical non-blocking and blocking concurrent queue algorithms

## Reference

Maged M. Michael and Michael L. Scott. “[Simple, Fast, and Practical
Non-Blocking and Blocking Concurrent Queue
Algorithms](https://doi.org/10.1145/248052.248106).” *15th ACM Symposium on
Principles of Distributed Computing*, pages 267–275, 1996. [Author-hosted
paper](https://www.cs.rochester.edu/~scott/papers/1996_PODC_queues.pdf).

## Research question or contribution

The paper presents one non-blocking FIFO queue and one two-lock FIFO queue,
seeking simple algorithms that allow useful concurrency without the single-lock
bottleneck of conventional queues.

## Method

The algorithms are specified with their atomic steps and evaluated against
contemporary alternatives on a 12-processor SGI Challenge. Tests include both
dedicated processors and multiprogrammed execution so that scheduler delay of
a queue participant is visible.

## Findings

- The non-blocking queue uses a linked list with an always-present dummy node
  and compare-and-swap operations on head, tail, and link fields. Competing
  threads help advance a lagging tail.
- The two-lock design permits one enqueue and one dequeue to proceed
  concurrently and is useful where only weaker atomic primitives exist.
- On the evaluated hardware the non-blocking variant consistently outperformed
  compared alternatives when universal atomic primitives were available; the
  two-lock queue improved over a single lock under contention.
- Safe node reclamation is a separate obligation. The paper's counted-pointer
  treatment assumes atomic capabilities that many modern targets do not
  provide directly; hazard pointers, epochs, ownership, or another proven
  scheme is still required.

## Relevance

The work supplies a baseline for reasoning about multi-producer actor signal
ingress, especially linearization, publication of a complete node, delayed
producers, and memory reclamation. It does not imply that one global
Michael–Scott queue is the best mailbox: ERTS evidence favors sender-striped
ingress under extreme fan-in, while the actor owner alone should drain and
materialize its receivable queue. Atom OS should compare a simple MPSC queue,
striped FIFOs, and a two-lock fallback under its actual memory model.

## Limits

The 1996 machine and workload do not predict cache-coherence, NUMA, or tail
behavior on current processors. The algorithm guarantees queue progress, not
fairness, bounded enqueue latency, bounded memory, actor signal ordering, or
correct interaction with receiver exit. Those properties need a higher-level
mailbox protocol and target-specific tests.

## Derived work

- [Signal ingress, mailboxes, and selective receive](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
