---
title: "Characterizing the Scalability of Erlang VM on Many-core Processors"
kind: source
created: "2026-08-28"
authors:
  - "Jianrong Zhang"
published: "2011-01-20"
citation_key: "zhang-2011-erlang-vm-scalability"
container: "KTH Information and Communication Technology"
edition: "Master of Science thesis; TRITA-ICT-EX-2011:5"
isbn: null
doi: null
url: "https://kth.diva-portal.org/smash/record.jsf?pid=diva2:392243"
accessed: "2026-08-28"
tags:
  - erlang
  - many-core
  - runtime-internals
  - scalability
  - scheduling
aliases:
  - "Zhang Erlang VM scalability thesis"
---

# Characterizing the Scalability of Erlang VM on Many-core Processors

## Reference

Jianrong Zhang. *[Characterizing the Scalability of Erlang VM on Many-core
Processors](https://kth.diva-portal.org/smash/record.jsf?pid=diva2:392243)*.
Master of Science thesis, KTH Information and Communication Technology, 2011.
TRITA-ICT-EX-2011:5.

## Research question or contribution

The thesis studies how the parallel Erlang VM of its period scaled on a
64-core TILEPro64 processor, seeks runtime bottlenecks, and proposes directions
for reducing synchronization overhead.

## Method

Zhang runs several benchmark programs across scheduler counts, profiles and
traces the runtime, compares parallel and sequential VM configurations, and
examines locks, atomics, allocators, process tables, queues, garbage-collection
statistics, and other shared implementation structures. The platform and VM
revision are specific to the 2010–2011 investigation.

## Findings

- Most selected benchmarks achieved reported maximum speedups of roughly 40–50
  on 60 cores when given suitable workloads. Scaling differed substantially by
  workload.
- Contended synchronization was a major bottleneck in several tests. Even an
  uncontended lock or atomic operation could impose enough latency to make the
  parallel VM with one scheduler slower than the sequential VM for a
  message-heavy benchmark.
- Allocators, process and runtime tables, queues, statistics, message handling,
  and memory management introduced shared implementation work underneath
  Erlang's no-shared-state programming abstraction.
- The thesis recommends reducing contention and using lower-overhead locks,
  lock-free structures, or algorithms where appropriate rather than assuming
  language-level message passing removes runtime synchronization.

## Relevance

This is direct historical evidence for an important kernel-design warning:
user-visible actors can share no mutable application state while their runtime
still bottlenecks on global metadata and memory infrastructure. The project
must inventory both semantic sharing and hidden implementation sharing.

The benchmark methodology also suggests comparing one-scheduler overhead,
strong scaling, workload size, message intensity, memory intensity, and
contention separately. A many-core result without those controls can hide the
cost of the parallel runtime itself.

## Limits

The thesis is not evidence about current OTP 29 performance. It studies an old
VM, old compiler, unusual TILEPro64 architecture, Linux host, and selected
benchmarks. Many cited locks and runtime structures have since changed or been
removed. Maximum speedup is not efficiency, tail latency, energy, or a hard
scalability limit. The author also worked with guidance and benchmark material
from the Erlang/OTP team, which is useful context but not an independent
replication.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
