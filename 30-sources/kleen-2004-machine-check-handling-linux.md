---
title: "Machine check handling on Linux"
kind: source
created: "2026-09-05"
authors:
  - "Andi Kleen"
published: 2004
citation_key: "kleen-2004-machine-check-handling-linux"
container: "Linux Kongress 2004"
edition: null
isbn: null
doi: null
url: "https://www.halobates.de/mce.pdf"
accessed: "2026-09-05"
tags:
  - diagnostics
  - hardware-errors
  - linux
  - ras
  - x86-64
aliases:
  - "Linux machine-check handling"
---

# Machine check handling on Linux

## Reference

Andi Kleen. “Machine Check Handling on Linux.” *Linux Kongress 2004*, 2004.
[Author-hosted paper](https://www.halobates.de/mce.pdf) and [author publication
index](https://www.halobates.de/).

## Research question or contribution

How can an x86-64 kernel capture and report machine-check banks when the event
can arrive in almost any execution context and the handler's own dependencies
may be unsafe?

## Method

The paper's machine-check record, NMI-like handler constraints, bank handling,
configuration, userspace decoding, and future recovery discussion were read as
a historical first-party implementation account. Current Intel manuals remain
the normative source for today's architecture semantics.

## Findings

- Machine-check exceptions can interrupt critical sections and disabled-
  interrupt regions. Even functions normally described as interrupt-safe can
  deadlock when the fault interrupted code while it held a required lock.
- The handler records a fixed tuple of global status, bank status, address,
  miscellaneous data, instruction pointer, timestamp, bank, and CPU, then
  defers richer decoding to userspace.
- Hardware banks can be overwritten by later errors, so capture must happen
  promptly and preserve validity and overflow fields before explicit clearing.
- The paper separates the very restricted exception handler from periodic
  collection of silent/corrected records and from user-space presentation.
- Memory-controller reporting can be asynchronous and imprecise. Attributing
  an error to the process interrupted at exception time can be wrong near a
  syscall or context switch.
- A configurable willingness to keep running is a policy/risk choice, not a
  property proved by returning from the handler.

## Relevance

Atom's x86 capture program should be fixed, nonallocating, lock-independent,
and limited to raw bank collection, acknowledgement, sealing, and a typed
disposition. Decoder and classifier code should execute later against a pinned
CPU/profile table. Interrupted thread identity must be recorded separately
from detector, consumer, and causal attribution.

## Limits

The paper describes an early Linux x86-64 handler and predates current machine-
check extensions, memory-failure recovery, virtualization, and many vendor
errata. It is neither a formal proof nor evidence that continuation is safe
after arbitrary corruption. Its data structure and policy are precedents, not
an Atom ABI.

## Derived work

- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
