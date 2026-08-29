---
title: "Efficient memory management for concurrent programs that use message passing"
kind: source
created: "2026-08-28"
authors:
  - "Konstantinos Sagonas"
  - "Jesper Wilhelmsson"
published: 2006
citation_key: "sagonas-wilhelmsson-2006-memory"
container: "Science of Computer Programming 62(2), 98-121"
edition: null
isbn: null
doi: "10.1016/j.scico.2006.02.006"
url: "https://doi.org/10.1016/j.scico.2006.02.006"
accessed: "2026-08-28"
tags:
  - erlang
  - garbage-collection
  - memory-management
  - message-passing
aliases:
  - "Sagonas and Wilhelmsson memory management"
---

# Efficient memory management for concurrent programs that use message passing

## Reference

Konstantinos Sagonas and Jesper Wilhelmsson. “[Efficient memory management for
concurrent programs that use message
passing](https://doi.org/10.1016/j.scico.2006.02.006).” *Science of Computer
Programming* 62, no. 2 (2006): 98–121. DOI 10.1016/j.scico.2006.02.006.

## Research question or contribution

The paper asks how a concurrent functional runtime with message-passing
semantics can retain process-local allocation advantages while reducing
message-copying cost and meeting soft real-time pause goals. It develops a
hybrid heap architecture and incremental collector.

## Method

The authors compare three architectures conceptually:

- process-local heaps with copying between processes;
- a communal heap that permits shared message objects; and
- a hybrid with private process heaps plus a shared message area.

Static analysis speculatively directs likely message data to the shared area.
The implemented hybrid is evaluated with work-based and time-based incremental
collection on synthetic programs and AdHoc, YAWS, and Mnesia workloads. The
reported machine is a dual-Xeon Linux 2.6.10 system with 1 GB of memory.

## Findings

- Process-local heaps allow allocation and collection without global
  synchronization, reclaim all private memory cheaply on process exit, and keep
  pauses local. Their principal messaging cost is copying terms proportional
  to message size, with possible fragmentation across many small heaps.
- A communal heap can make message sharing constant-time but expands the root
  set and introduces global synchronization and collection concerns.
- The hybrid architecture tries to retain independent local heaps while placing
  likely message objects in a shared area. It depends on analysis quality and a
  more complex collector.
- The incremental collector avoids a conventional write barrier and can be
  scheduled by work or time quanta. The work-based version guarantees eventual
  collection progress but does not give a hard time bound for every pause; the
  time-based version can target short quanta but has different progress risks.
- Reported garbage-collection overhead ranged from a few percent to roughly
  2.5–3 times for most programs in the collector-focused measurements. The
  adversarial worker benchmark reached 5.6 times GC overhead, while its complete
  execution time was about 1.7 times the non-incremental case.
- A one-millisecond time quantum produced short pauses in the tested setting,
  but the paper does not establish a platform-independent hard real-time bound.

## Relevance

The paper shows that actor/message semantics leave important implementation
choices open. “Processes do not share state” does not uniquely determine where
message objects live or how they are collected. A kernel and managed runtime
can choose copying, lending, immutable sharing, regions, or a hybrid as long as
ownership, isolation, and observable message semantics remain clear.

It also supports aligning collection and reclamation with failure domains while
measuring copying cost, shared-object lifetime, synchronization, pause
distribution, and total throughput separately.

## Limits

The evaluated implementation and hardware are about two decades old. The
hybrid collector described here is not evidence that current OTP 29 uses that
architecture. Workloads, memory size, CPU topology, compiler, and allocator all
limit transferability. Mean or percentile pause measurements under selected
benchmarks do not prove hard real-time behavior under arbitrary roots, heaps,
native code, or memory pressure.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
