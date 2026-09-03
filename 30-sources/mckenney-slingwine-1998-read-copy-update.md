---
title: "Read-copy update: Using execution history to solve concurrency problems"
kind: source
created: "2026-09-03"
authors:
  - "Paul E. McKenney"
  - "John D. Slingwine"
published: 1998
citation_key: "mckenney-slingwine-1998-read-copy-update"
container: "International Conference on Parallel and Distributed Computing and Systems"
edition: null
isbn: null
doi: null
url: "https://www.eecg.utoronto.ca/~amza/ece1747h/papers/readings/rcu.pdf"
accessed: "2026-09-03"
tags:
  - concurrency
  - kernels
  - memory-reclamation
  - quiescence
aliases:
  - "Original RCU paper"
---

# Read-copy update: Using execution history to solve concurrency problems

## Reference

Paul E. McKenney and John D. Slingwine. “Read-Copy Update: Using Execution
History to Solve Concurrency Problems.” *International Conference on Parallel
and Distributed Computing and Systems*, Las Vegas, October 1998, pp. 509–518.
[Open paper](https://www.eecg.utoronto.ca/~amza/ece1747h/papers/readings/rcu.pdf).

## Research question or contribution

How can an updater remove and eventually reclaim shared objects without forcing
read-mostly paths to take expensive locks or reference-count operations? The
paper presents read-copy update (RCU), using observed execution history and
quiescent states to determine when pre-existing readers can no longer retain
references to removed data.

## Method

The authors define quiescent states and quiescent periods, apply the method to
several kernel data structures, describe a production implementation, and
report measurements on a 32-processor Pentium Pro NUMA-Q system. The evidence
is historical and tied to the evaluated workloads and machine.

## Findings

- Removal from a lookup structure and physical reclamation are different
  transitions. New readers can be denied immediately while old readers finish.
- Once every relevant execution context has passed a quiescent state after
  removal, an updater may reclaim storage that those pre-existing readers
  could have referenced.
- The approach makes reader paths particularly cheap for read-mostly data and
  can batch reclamation behind a grace period.
- Readers may observe the old or new version during an update, so an RCU use
  requires data and API semantics that tolerate that concurrency.

## Relevance

The split between logical closure and physical reclamation is directly useful
for capability entries, endpoint lookup tables, domain membership snapshots,
and other read-mostly kernel indices. It suggests a low-cost implementation of
lookup pins and deferred freeing once per-CPU kernel activations have crossed
declared checkpoints.

RCU is only one quiescence class in the proposed kernel. TLB invalidation,
interrupt drainage, timer cancellation, DMA completion, and device reset each
need their own architecture- or device-specific evidence before backing memory
can be reused.

## Limits

The original evaluation predates modern weak-memory, preemptible-kernel, and
many-core implementations. RCU does not itself revoke a capability, stop an
uncooperative user thread, flush a translation, cancel an IRQ, or drain a DMA
engine. A stalled reader can delay reclamation, so retained-storage bounds and
backpressure are part of the design. Current implementation guidance should be
cross-checked against the [Linux RCU documentation](https://docs.kernel.org/RCU/whatisRCU.html),
but Atom OS still needs its own memory model and checkpoint proof.

## Derived work

- [Teardown, revocation, and safe reclamation](../20-notes/minimal-privileged-kernel-components/teardown-revocation-and-safe-reclamation.md)
- [Typed object storage and explicit memory](../20-notes/minimal-privileged-kernel-components/typed-object-storage-and-explicit-memory.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
