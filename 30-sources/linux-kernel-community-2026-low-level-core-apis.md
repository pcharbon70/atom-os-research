---
title: "Linux kernel low-level core API documentation"
kind: source
created: "2026-08-30"
authors:
  - "The Linux kernel development community"
published: 2026
citation_key: "linux-kernel-community-2026-low-level-core-apis"
container: "The Linux Kernel documentation"
edition: "Latest documentation accessed 2026-08-30"
isbn: null
doi: null
url: "https://www.kernel.org/doc/html/latest/core-api/index.html"
accessed: "2026-08-30"
tags:
  - cpu-lifecycle
  - dma
  - interrupts
  - kernel-interfaces
  - memory-ordering
  - timekeeping
  - virtual-memory
aliases:
  - "Linux low-level kernel contracts"
---

# Linux kernel low-level core API documentation

## Reference

The Linux kernel development community. *The Linux Kernel documentation*,
latest documentation accessed 2026-08-30:

- [Entry/exit handling for exceptions, interrupts, syscalls and KVM](https://www.kernel.org/doc/html/latest/core-api/entry.html)
- [Generic interrupt handling](https://www.kernel.org/doc/html/latest/core-api/genericirq.html)
- [Clock sources, clock events, `sched_clock()` and delay timers](https://www.kernel.org/doc/html/latest/timers/timekeeping.html)
- [Linux kernel memory barriers](https://www.kernel.org/doc/html/latest/core-api/wrappers/memory-barriers.html)
- [Cache and TLB flushing under Linux](https://www.kernel.org/doc/html/latest/core-api/cachetlb.html)
- [CPU hotplug in the kernel](https://www.kernel.org/doc/html/latest/core-api/cpu_hotplug.html)
- [Dynamic DMA mapping](https://www.kernel.org/doc/html/latest/core-api/dma-api.html)

## Research question or contribution

How does a mature portable kernel divide low-level architecture mechanisms
into contracts whose callers can rely on semantic effects without knowing each
architecture's instruction sequences?

## Method

This note compares seven current normative or maintainer-facing documentation
sets. It extracts interface boundaries and ordering obligations, not Linux's
policy choices or an endorsement of its implementation structure.

## Findings

- Entry code is a protocol rather than a jump into a handler. Low-level
  architecture code first establishes a defined state; common code then
  transitions lock tracking, RCU/context tracking, tracing, time accounting,
  and preemption in constrained order. Some transition windows must remain
  non-instrumentable. NMI-like entry requires nesting-aware state.
- The generic interrupt subsystem separates an interrupt descriptor and driver
  API, flow handlers for edge, level, fast-EOI, simple, and per-CPU semantics,
  and controller-specific chip operations. A single generic acknowledge path
  cannot erase electrical/controller flow differences safely.
- Timekeeping separates a free-running clock source, programmable clock-event
  devices, a cheap scheduler clock, and delay timers. Their resolution,
  stability, per-CPU scope, and suspend behavior are different contracts.
- The barrier documentation specifies a portable minimum ordering contract and
  distinguishes compiler, CPU-memory, device-I/O, and DMA ordering. A stronger
  implementation on one ISA does not justify weakening the source-level
  contract.
- Cache/TLB operations are documented by the state change callers may assume,
  while architecture implementations choose the required invalidation,
  broadcast, and barrier sequence.
- CPU hotplug is an ordered lifecycle with startup and teardown states,
  callbacks, error returns, and rollback. Removing a CPU entails migration or
  shutdown of interrupts, timers, and work; it is not a Boolean flag.
- The DMA API distinguishes CPU virtual, CPU physical, and device-visible DMA
  addresses, and makes mapping lifetime and synchronization explicit.

## Relevance

These documents offer a useful decomposition vocabulary for a new kernel:
entry transitions, interrupt flow, time primitives, ordering, translation
maintenance, logical-CPU lifecycle, and DMA should be separate semantic
components. They also expose cross-component transitions that need explicit
state machines rather than undocumented call ordering.

## Limits

Linux supports a much broader compatibility surface than this project needs,
and the documentation sometimes records evolved implementation constraints
rather than minimal mechanisms. It does not establish that Linux APIs, data
structures, or policy should be copied. Versioned online documentation may
change after the access date.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
