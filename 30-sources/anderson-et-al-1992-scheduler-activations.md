---
title: "Scheduler activations: Effective kernel support for the user-level management of parallelism"
kind: source
created: "2026-08-31"
authors:
  - "Thomas E. Anderson"
  - "Brian N. Bershad"
  - "Edward D. Lazowska"
  - "Henry M. Levy"
published: 1992
citation_key: "anderson-et-al-1992-scheduler-activations"
container: "ACM Transactions on Computer Systems 10(1), 53–79"
edition: null
isbn: null
doi: "10.1145/146941.146944"
url: "https://homes.cs.washington.edu/~tom/pubs/sched_act.html"
accessed: "2026-08-31"
tags:
  - multicore
  - operating-systems
  - scheduling
  - threads
  - user-level-scheduling
aliases:
  - "Scheduler activations"
---

# Scheduler activations: Effective kernel support for the user-level management of parallelism

## Reference

Thomas E. Anderson, Brian N. Bershad, Edward D. Lazowska, and Henry M. Levy.
“Scheduler Activations: Effective Kernel Support for the User-Level Management
of Parallelism.” *ACM Transactions on Computer Systems* 10(1), pages 53–79,
February 1992. DOI
[10.1145/146941.146944](https://doi.org/10.1145/146941.146944).
[Author-hosted record and paper](https://homes.cs.washington.edu/~tom/pubs/sched_act.html).

## Research question or contribution

Can a kernel expose processor allocation and blocking events to a user-level
runtime without moving that runtime's fine-grained thread scheduling policy and
operations into the kernel?

## Method

The authors add scheduler activations to the Topaz operating system and adapt
the FastThreads user-level thread package on a DEC SRC Firefly. Microbenchmarks
compare user-level operations, Topaz kernel threads, and Ultrix processes. An
N-body application on a six-processor CVAX Firefly evaluates compute-bound,
simulated blocking-I/O, and two-application multiprogramming cases.

## Findings

- The design separates processor allocation, which remains a kernel decision,
  from assignment of an address space's user threads to those processors,
  which remains a runtime decision.
- A scheduler activation is an execution context used for an upcall when a
  processor is allocated, a running user thread blocks or is preempted, or an
  earlier block completes. The kernel exposes saved state; the user scheduler
  updates its own queues and selects the next runnable thread.
- The interface preserves the invariant that an address space knows how many
  processors it owns and which user threads occupy them. The runtime reports
  only changes that can affect processor allocation rather than every cheap
  thread operation.
- On the evaluated CVAX system, modified FastThreads took 37 microseconds for a
  null fork and 42 microseconds for signal-wait, versus 34 and 37 for original
  FastThreads and 948 and 441 for Topaz kernel threads. These are historical
  operation costs, not portable ratios.
- The prototype's forced kernel signal-wait/upcall path took 2.4 milliseconds,
  about five times the Topaz-thread cost. The authors attributed this negative
  result to an untuned modification and its Modula-2+ implementation.
- With two N-body instances sharing six processors, modified FastThreads
  achieved a reported speedup of 2.45, compared with 1.29 for Topaz threads and
  1.26 for original FastThreads, where three was the maximum possible speedup.
  Handling preemption inside user-scheduler critical sections nevertheless
  required explicit recovery machinery.

## Relevance

BEAM actors should remain runtime objects rather than privileged kernel
threads. An activation-like contract could let the runtime schedule actors and
apply reductions while the kernel grants execution contexts and reports
blocking, preemption, and processor-allocation changes. Unlike the historical
interface, scheduling-context capabilities must still enforce the runtime's CPU
budget independently; an event notification is not authority to consume
unbounded time. The design is evidence for a clean kernel/runtime division, not
a decision to reproduce the Scheduler Activations API.

## Limits

The implementation and measurements use Topaz, FastThreads, CVAX processors,
and one six-processor Firefly. Upcalls were expensive, and correct recovery from
preemption inside runtime critical sections made the user scheduler reentrant
and more complex. The paper does not evaluate capabilities, temporal budgets,
modern many-core or NUMA hardware, BEAM scheduling, malicious runtimes, or
supervisor failure boundaries. Later threading systems made different
engineering choices, so the result identifies an interface problem and one
historical solution rather than a mandatory modern mechanism.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
