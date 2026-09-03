---
title: "When poll is better than interrupt"
kind: source
created: "2026-09-02"
authors:
  - "Jisoo Yang"
  - "Dave B. Minturn"
  - "Frank Hady"
published: 2012
citation_key: "yang-et-al-2012-when-poll-is-better-than-interrupt"
container: "10th USENIX Conference on File and Storage Technologies"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/fast12/when-poll-better-interrupt"
accessed: "2026-09-02"
tags:
  - interrupts
  - io
  - operating-systems
  - performance
  - polling
aliases:
  - "Polling versus interrupts for low-latency storage"
---

# When poll is better than interrupt

## Reference

Jisoo Yang, Dave B. Minturn, and Frank Hady. “When Poll Is Better than
Interrupt.” *10th USENIX Conference on File and Storage Technologies*, 2012.
[USENIX paper and metadata](https://www.usenix.org/conference/fast12/when-poll-better-interrupt).

## Research question or contribution

Can synchronous polling outperform interrupt-driven completion for a class of
very low-latency storage operations, despite spending CPU time while waiting?

## Method

The paper analyzes an interrupt-driven storage path, implements synchronous
polling for selected low-latency devices and workloads, compares latency and
CPU tradeoffs, and argues the safety of its completion model.

## Findings

- For the evaluated very low-latency storage configuration, interrupt entry,
  scheduling, and deferred completion overhead could exceed useful device
  wait time, making polling faster.
- Polling consumes processor capacity and its advantage depends on device
  latency, queue occupancy, workload, and whether the CPU has other useful
  work.
- “Polling or interrupt” is a service-policy decision; it does not remove the
  need to configure, mask, account for, and recover the interrupt source.

## Relevance

The event fabric should provide a capability-controlled transition to a
masked polling lease for suitable queues, while charging the polling thread's
scheduling budget. Polling is not the baseline for all devices and must not be
used to bypass source generations, reset ownership, or storm evidence.

## Limits

The study targets storage technology and systems from 2012. Absolute latency
and crossover points are obsolete for current machines. It is evidence that
polling can be useful, not that it is universally superior or that the kernel
should execute driver polling loops in privileged context.

## Derived work

- [Interrupt event fabric](../20-notes/kernel-hardware-and-architecture-components/interrupt-event-fabric.md)
