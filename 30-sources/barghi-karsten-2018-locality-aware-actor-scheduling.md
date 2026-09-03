---
title: "Work-Stealing, Locality-Aware Actor Scheduling"
kind: source
created: "2026-09-02"
authors:
  - "Saman Barghi"
  - "Martin Karsten"
published: 2018
citation_key: "barghi-karsten-2018-locality-aware-actors"
container: "2018 IEEE International Parallel and Distributed Processing Symposium"
edition: "IPDPS 2018, 484-494"
isbn: "978-1-5386-4368-6"
doi: "10.1109/IPDPS.2018.00058"
url: "https://cs.uwaterloo.ca/~mkarsten/papers/ipdps2018-preprint.pdf"
accessed: "2026-09-02"
tags:
  - actor-model
  - multicore
  - numa
  - scheduling
  - work-stealing
aliases:
  - "Locality-aware actor scheduling"
---

# Work-Stealing, Locality-Aware Actor Scheduling

## Reference

Saman Barghi and Martin Karsten. “[Work-Stealing, Locality-Aware Actor
Scheduling](https://doi.org/10.1109/IPDPS.2018.00058).” *2018 IEEE
International Parallel and Distributed Processing Symposium*, pages 484–494,
2018. DOI 10.1109/IPDPS.2018.00058. [Author-hosted
preprint](https://cs.uwaterloo.ca/~mkarsten/papers/ipdps2018-preprint.pdf).

## Research question or contribution

The paper asks how actor-runtime work stealing should account for cache and
NUMA topology. It characterizes communication and actor behavior, then compares
randomized and hierarchical locality-aware policies in the C++ Actor Framework.

## Method

The authors implement scheduler variants in CAF and evaluate actor workloads on
AMD and Intel multi-socket machines. The experiments vary communication
patterns and actor behavior to distinguish locality benefits from queueing and
stealing overhead.

## Findings

- Random victim selection can create remote cache and NUMA traffic even when
  the actor abstraction itself shares little mutable application state.
- The locality-aware search checks topology-local nonempty deques first and
  ascends by NUMA distance. Polling counts and backoff limit steal contention;
  the evaluated variants were competitive with or faster than the baseline on
  most tested workloads.
- Locality policy is workload-dependent. Communication shape, actor lifetime,
  and the amount of work performed per activation change which placement is
  useful.
- An affinity-oriented unblocking design created lock contention and severe
  tail behavior in some cases. Preserving locality can therefore cost more
  than it saves when the mechanism centralizes wakeups or queue ownership.

## Relevance

The result supports scheduler-local run queues and topology hints in a managed
actor runtime, but not a mandatory actor-to-core affinity rule. Atom OS should
make placement an adaptive, observable policy above kernel scheduling-context
budgets, then test it against message locality, memory locality, migration,
fairness, and latency together.

## Limits

This is a CAF study, not an ERTS implementation or a BEAM semantic result. The
machines, scheduler variants, and applications constrain the comparison. It
does not measure garbage collection, selective receive, dirty native work,
kernel budget enforcement, or adversarial tenants. NUMA-aware scheduling must
therefore remain an optional measured policy rather than part of the public
actor contract.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
