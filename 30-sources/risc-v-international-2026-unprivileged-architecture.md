---
title: "The RISC-V instruction set manual, unprivileged architecture"
kind: source
created: "2026-09-02"
authors:
  - "RISC-V International"
published: 2026
citation_key: "risc-v-international-2026-unprivileged-architecture"
container: "RISC-V Ratified Specifications Library"
edition: "Release 20260120"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/isa/v20260120/unpriv/unpriv-index.html"
accessed: "2026-09-02"
tags:
  - concurrency
  - instruction-fetch
  - memory-models
  - risc-v
aliases:
  - "RISC-V unprivileged ISA 20260120"
---

# The RISC-V instruction set manual, unprivileged architecture

## Reference

RISC-V International. *The RISC-V Instruction Set Manual, Volume I:
Unprivileged Architecture*, release 20260120.
[Official ratified specification](https://docs.riscv.org/reference/isa/v20260120/unpriv/unpriv-index.html).

## Research question or contribution

Which ordinary-memory, device-ordering, atomic, and instruction-fetch
guarantees can portable RISC-V systems software rely on?

## Method

The ratified specification is treated as the normative source. The analysis
uses RVWMO, `FENCE`, atomic ordering, and the Zifencei chapter rather than
inferring behavior from a particular processor.

## Findings

- RVWMO is the weakest standard RISC-V memory model for portable software;
  implementations may be stronger, but software cannot assume that.
- `FENCE` names predecessor and successor classes for memory reads, writes,
  device input, and device output. It does not order external signaling paths
  that fall outside those observations.
- `FENCE.I` orders prior visible stores against later instruction fetches on
  the executing hart only. Publishing to other harts also requires a data
  fence and a remote instruction-fence protocol.
- The specification discusses JIT batching as a legitimate way to amortize
  potentially expensive instruction synchronization and notes why user-level
  `FENCE.I` is insufficient when a task may migrate.

## Relevance

RISC-V forces the architecture facade to distinguish ordinary CPU ordering,
I/O ordering, and local versus remote code-fetch completion. The managed
runtime should batch immutable code objects and request kernel-mediated
publication rather than execute `FENCE.I` itself.

## Limits

The unprivileged ISA does not supply interrupt routing, remote-hart execution,
page-table authority, cache-block maintenance on every platform, or device DMA
ownership. Those require the privileged ISA, SBI or another execution
environment, and platform-specific profiles.

## Derived work

- [Ordering, coherence, and code publication](../20-notes/ordering-coherence-and-code-publication.md)
