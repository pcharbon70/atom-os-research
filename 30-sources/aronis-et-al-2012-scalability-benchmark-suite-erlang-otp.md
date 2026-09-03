---
title: "A scalability benchmark suite for Erlang/OTP"
kind: source
created: "2026-09-02"
authors:
  - "Stavros Aronis"
  - "Nikolaos Papaspyrou"
  - "Katerina Roukounaki"
  - "Konstantinos Sagonas"
  - "Yiannis Tsiouris"
  - "Ioannis E. Venetis"
published: 2012
citation_key: "aronis-et-al-2012-bencherl"
container: "Proceedings of the 11th ACM SIGPLAN Workshop on Erlang"
edition: "Erlang '12, 33-42"
isbn: "978-1-4503-1575-3"
doi: "10.1145/2364489.2364495"
url: "https://uu.diva-portal.org/smash/record.jsf?pid=diva2%3A574861"
accessed: "2026-09-02"
tags:
  - benchmarking
  - erlang
  - erts
  - multicore
  - scalability
aliases:
  - "Bencherl paper"
---

# A scalability benchmark suite for Erlang/OTP

## Reference

Stavros Aronis, Nikolaos Papaspyrou, Katerina Roukounaki, Konstantinos
Sagonas, Yiannis Tsiouris, and Ioannis E. Venetis. “[A scalability benchmark
suite for Erlang/OTP](https://doi.org/10.1145/2364489.2364495).” *Proceedings
of the 11th ACM SIGPLAN Workshop on Erlang*, pages 33–42, 2012. DOI
10.1145/2364489.2364495. The [Uppsala University
record](https://uu.diva-portal.org/smash/record.jsf?pid=diva2%3A574861) and
paper were consulted.

## Research question or contribution

The paper introduces Bencherl, a suite intended to measure how Erlang/OTP
applications change as CPUs, scheduler threads, machines, input size, and
other resources are varied. Its important methodological claim is that one
peak throughput number does not characterize runtime scalability.

## Method

The authors define several scalability dimensions and package parallel and
distributed Erlang workloads with an execution and results infrastructure.
They use a limited set of measurements to demonstrate the suite rather than to
declare one VM configuration universally best.

## Findings

- Scalability is a curve across resource and workload sizes, not a single
  speedup number. A runtime can improve at one point while becoming less
  efficient or less stable elsewhere.
- One-scheduler measurements are needed to expose the overhead introduced by
  the parallel runtime itself before interpreting strong-scaling results.
- The suite separates shared-memory and distributed workloads and varies
  message, compute, and coordination structure. Those dimensions exercise
  different runtime bottlenecks.
- Reproducible execution and retained result series are part of the benchmark
  design; a chart without the workload and configuration matrix is weak
  evidence.

## Relevance

The managed actor runtime needs a compatibility suite and a scalability suite.
Bencherl supplies a useful shape for the latter: sweep scheduler counts,
topology, actor counts, message sizes, mailbox pressure, allocation intensity,
and node counts while preserving single-scheduler baselines and tail-latency
results. This guards against optimizing an impressive isolated throughput point
while degrading responsiveness or resource efficiency.

## Limits

The suite and illustrative results reflect 2012-era Erlang/OTP, hardware, and
distributed infrastructure. It does not supply hard real-time, security,
energy, garbage-collection-pause, or hostile-overload guarantees. Its workload
set is a starting point for an Atom OS evaluation matrix, not proof that a new
runtime is compatible or scalable.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Observability, deterministic testing, and crash evidence](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
