---
title: "Scheduling multithreaded computations by work stealing"
kind: source
created: "2026-09-03"
authors:
  - "Robert D. Blumofe"
  - "Charles E. Leiserson"
published: 1999
citation_key: "blumofe-leiserson-1999-work-stealing"
container: "Journal of the ACM"
edition: "46(5), 720-748"
isbn: null
doi: "10.1145/324133.324234"
url: "https://doi.org/10.1145/324133.324234"
accessed: "2026-09-03"
tags:
  - multicore
  - scheduling
  - work-stealing
aliases:
  - "Blumofe-Leiserson work stealing"
---

# Scheduling multithreaded computations by work stealing

## Reference

Robert D. Blumofe and Charles E. Leiserson. “[Scheduling Multithreaded
Computations by Work Stealing](https://doi.org/10.1145/324133.324234).”
*Journal of the ACM* 46(5), pages 720–748, 1999.

## Research question or contribution

The paper gives a randomized work-stealing scheduler with analytical bounds
for fully strict multithreaded computations, explaining why idle processors
pulling work can combine good expected completion time with bounded space and
communication.

## Method

The authors model a computation by its serial work, critical-path length,
serial space, and activation size. They prove expected execution,
communication, and space bounds for the randomized scheduler rather than only
reporting benchmark throughput.

## Findings

- For the modeled fully strict computations, expected running time on `P`
  processors is `T1/P + O(T∞)`.
- The execution uses at most `S1 P` space and the expected communication bound
  depends on `P`, critical-path length, synchronization depth, and maximum
  activation size.
- Local push/pop on a worker's own deque keeps the common path local; stealing
  is paid primarily by idle workers.
- The proof relies on structured dependencies and its cost model. Arbitrary
  actor mailboxes, priorities, blocking native work, garbage collection,
  kernel budget revocation, and NUMA topology are outside that result.

## Relevance

The paper justifies scheduler-local queues with steal-on-idle as a strong
starting mechanism, while also supplying the reason not to overstate the
guarantee. BEAM actors are not fully strict fork/join tasks. Atom OS therefore
uses work stealing as an adaptive implementation policy beneath actor fairness
and kernel CPU budgets, and measures steal frequency, migrated bytes,
safe-point latency, priorities, and locality rather than claiming the JACM
bounds for arbitrary actor programs.

## Limits

The result is a theoretical model for a particular computation class, not a
BEAM scheduler evaluation. It does not solve overload, cross-domain priority
inversion, scheduler-thread pre-emption, or the attribution of garbage
collection and signal work. Locality-aware actor studies are needed alongside
this foundational result.

## Derived work

- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
