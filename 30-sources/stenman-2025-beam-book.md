---
title: "The BEAM Book: Understanding the Erlang Runtime System"
kind: source
created: "2026-08-28"
authors:
  - "Erik Stenman"
published: 2025
citation_key: "stenman-2025-beam-book"
container: "The BEAM Book"
edition: "First edition; web version updated 2026-04-26"
isbn: "978-91-531-4253-9"
doi: null
url: "https://blog.stenmans.org/theBeamBook/"
accessed: "2026-08-28"
tags:
  - beam
  - erts
  - memory-management
  - runtime-internals
  - scheduling
aliases:
  - "The BEAM Book"
---

# The BEAM Book: Understanding the Erlang Runtime System

## Reference

Erik Stenman and contributors. *[The BEAM Book: Understanding the Erlang
Runtime System](https://blog.stenmans.org/theBeamBook/)*. First edition, 2025.
ISBN 978-91-531-4253-9. The online edition reported a last update of
2026-04-26. Accessed 2026-08-28.

## Contribution

The book is a long-form guide to the Erlang compiler, BEAM code, ERTS process
representation, scheduling, memory, message passing, code loading, ports,
drivers, NIFs, tracing, distribution, and source-tree organization. It bridges
the high-level manual and direct C/Erlang source reading.

## Method

The author develops conceptual models, diagrams, examples, and source-guided
walkthroughs. For this archive, chapters on processes, garbage collection,
mailboxes, scheduler queues and balancing, code loading, memory allocators,
ports, and NIFs were used as navigation. Claims that materially affect the
synthesis were checked against OTP 29.0.5 official documentation or the pinned
source tree.

## Findings

- An ERTS process is represented by much more than an instruction pointer: its
  process control block ties together scheduling state, registers, heap/stack,
  signal queues, links, monitors, and runtime metadata.
- SMP ERTS uses scheduler-local queues, priority-aware selection, stealing and
  migration rather than a single global queue. Host CPU placement and memory
  locality influence the result.
- Process-local heaps simplify independent garbage collection, while message
  queues and shared binaries require careful ownership and signal handling.
- Local and fully qualified calls have different code-version semantics. This
  distinction is the language-level hook that allows a long-running process to
  enter newly loaded module code deliberately.
- Ports, linked-in drivers, and NIFs are different native integration paths
  with different scheduling and failure consequences.

## Relevance

The book makes the implementation cost behind Erlang's simple process model
legible and identifies source paths for deeper audit. It is especially useful
for avoiding an unrealistically small model of an ERTS scheduler or mailbox.
For this project it functions as an informed secondary map, while the matching
official manual and source revision remain authoritative.

## Limits

This is a living secondary work spanning many OTP generations. Some diagrams
and explanations intentionally simplify the current implementation, and the
title uses “BEAM” in the broader community sense even when discussing ERTS.
The web edition can change after the access date. It is not a normative
specification, controlled benchmark, or security evaluation.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [2026-08-28 research journal](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md)
