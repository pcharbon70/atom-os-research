---
title: "A NUMA-aware runtime environment for the actor model"
kind: source
created: "2026-09-03"
authors:
  - "Emilio Francesquini"
  - "Alfredo Goldman"
  - "Jean-François Méhaut"
published: 2013
citation_key: "francesquini-et-al-2013-numa-actors"
container: "42nd International Conference on Parallel Processing"
edition: "ICPP 2013, 250-259"
isbn: null
doi: "10.1109/ICPP.2013.34"
url: "https://doi.org/10.1109/ICPP.2013.34"
accessed: "2026-09-03"
tags:
  - actor-model
  - erlang
  - numa
  - scheduling
aliases:
  - "NUMA-aware Erlang runtime"
---

# A NUMA-aware runtime environment for the actor model

## Reference

Emilio Francesquini, Alfredo Goldman, and Jean-François Méhaut. “[A NUMA-Aware
Runtime Environment for the Actor
Model](https://doi.org/10.1109/ICPP.2013.34).” *42nd International Conference
on Parallel Processing*, pages 250–259, 2013.

## Research question or contribution

The paper asks how an Erlang runtime can use hierarchical memory topology when
placing actors and stealing work instead of treating all cores and memory as
uniform.

## Method

The authors modify an Erlang VM with topology discovery, actor placement, and
hierarchical work-stealing policies, then compare configurations on actor
benchmarks across NUMA hardware.

## Findings

- Actor “share nothing” semantics do not remove runtime locality: copied
  messages, heaps, queues, code, and scheduler data still move through a cache
  and NUMA hierarchy.
- Topology-aware placement and hierarchical stealing produced gains up to
  2.50× in selected experiments, while the worst reported regression was about
  1.09×.
- Benefits varied with communication shape and allocation; locality policy is
  not semantically universal.

## Relevance

The study supports topology hints and local-first stealing after Atom OS has a
correct scheduler, while its regressions argue for an adaptive switch and an
unbiased fallback. Actor migration must move scheduling ownership, not mutate
PID or mailbox semantics, and kernel-admitted scheduling contexts rather than
discovered CPU count determine concurrency.

## Limits

The evaluated VM and hardware are historical. The experiments do not include
current ERTS signal queues, modern GC/JIT behavior, runtime-domain CPU budgets,
hostile load, or high-percentile latency. The speedups are evidence for an
experiment, not a target promise.

## Derived work

- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
