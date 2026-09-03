---
title: "Lockless ring buffer design"
kind: source
created: "2026-09-03"
authors:
  - "Steven Rostedt"
published: 2009
citation_key: "rostedt-2009-lockless-ring-buffer-design"
container: "Linux kernel documentation"
edition: null
isbn: null
doi: null
url: "https://docs.kernel.org/trace/ring-buffer-design.html"
accessed: "2026-09-03"
tags:
  - concurrency
  - kernels
  - observability
  - ring-buffers
  - tracing
aliases:
  - "Linux tracing ring-buffer design"
---

# Lockless ring buffer design

## Reference

Steven Rostedt. “Lockless Ring Buffer Design.” Linux kernel documentation,
written for Linux 2.6.31, 2009. [Current official
documentation](https://docs.kernel.org/trace/ring-buffer-design.html).

## Research question or contribution

How can the Linux tracing subsystem allow low-overhead per-CPU event production,
including writers nested by interrupt entry, while a reader consumes records
without a conventional writer lock? The document specifies the tracing ring's
page roles, pointer states, commit discipline, overwrite and producer/consumer
modes, and writer/reader concurrency assumptions.

## Method

This is an implementation design document maintained with the Linux kernel. It
defines terminology and invariants, illustrates the page-list transitions, and
walks through writer nesting, reader-page exchange, full-buffer behavior, and
the compare-and-exchange protocol. It is neither a peer-reviewed performance
study nor a formal memory-model or worst-case execution-time proof.

## Findings

- The ring is per CPU, reducing cross-CPU producer contention and cache-line
  exchange on the common write path.
- Same-CPU writers may nest through interrupt-like entry, but completion is
  stack ordered: the inner writer finishes before the interrupted writer can
  publish its final commit.
- A separate commit position distinguishes space being written from the last
  completely committed record that a reader may consume.
- The buffer exposes two materially different saturation contracts: overwrite
  mode discards older records, while producer/consumer mode refuses newer
  records when no space remains.
- Reader-page exchange and tagged page-pointer transitions avoid a conventional
  writer lock under the document's stated single-reader and nesting rules.

## Relevance

The minimal privileged kernel can borrow the explicit producer roles, nested-
writer ordering, commit boundary, and separately named full-buffer modes for
fixed per-CPU diagnostic rings. These mechanisms support a design in which a
reader never treats an in-progress record as committed and loss policy is part
of the buffer type rather than an undocumented accident.

Atom OS should not copy the data structure without checking its own memory
model, interrupt/NMI nesting, CPU-lifecycle, snapshot, and teardown rules. The
kernel proposal also needs explicit sequence, loss, schema, authority, and
redaction metadata that are outside this document's core algorithm.

## Limits

The design is tied to Linux's stated writer-stack and reader assumptions and to
an implementation whose details have continued to evolve. “Lockless” does not
mean bounded in hard real time, wait-free for every participant, secure across
domains, persistent across reset, or safe in an arbitrary fatal context. The
document supplies no target-specific latency bound, confidentiality proof, or
guarantee that records survive corrupted memory, hostile DMA, firmware, or a
failed CPU. Those properties require separate measurement and lower-layer
completion evidence.

## Derived work

- [Observability and crash evidence](../20-notes/minimal-privileged-kernel-components/observability-and-crash-evidence.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
