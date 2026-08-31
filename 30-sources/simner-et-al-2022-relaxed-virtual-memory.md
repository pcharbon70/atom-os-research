---
title: "Relaxed virtual memory in Armv8-A"
kind: source
created: "2026-08-30"
authors:
  - "Ben Simner"
  - "Alasdair Armstrong"
  - "Jean Pichon-Pharabod"
  - "Christopher Pulte"
  - "Richard Grisenthwaite"
  - "Peter Sewell"
published: 2022
citation_key: "simner-et-al-2022-relaxed-virtual-memory"
container: "31st European Symposium on Programming"
edition: null
isbn: "978-3-030-99336-8"
doi: "10.1007/978-3-030-99336-8_6"
url: "https://www.cl.cam.ac.uk/~pes20/RelaxedVM-Arm/"
accessed: "2026-08-30"
tags:
  - aarch64
  - concurrency
  - formal-methods
  - tlb
  - virtual-memory
aliases:
  - "Relaxed VM in Armv8-A"
---

# Relaxed virtual memory in Armv8-A

## Reference

Ben Simner et al. “Relaxed Virtual Memory in Armv8-A.” *ESOP 2022*, pages
143–173. DOI
[10.1007/978-3-030-99336-8_6](https://doi.org/10.1007/978-3-030-99336-8_6).
[Authors' project page, models, and tests](https://www.cl.cam.ac.uk/~pes20/RelaxedVM-Arm/).

## Research question or contribution

How do weak memory, concurrent page-table walks, TLB maintenance, multiple
translation stages, and page-table mutation interact at the privileged
hardware/software boundary?

## Method

The authors develop axiomatic models and bare-metal litmus tests in discussion
with Arm and pKVM developers, integrate the model with instruction semantics,
and test a defined subset on hardware.

## Findings

- A mapping change is a publication and revocation protocol. Writing a page
  table entry, ordering that write, invalidating cached translations, waiting
  for remote observers, and reusing memory are not one atomic action.
- Informal “the TLB was flushed” assumptions omit concurrent walks, multiple
  cores, translation stages, and relaxed ordering needed for real verification.
- Safe break-before-make and invalidation sequences depend on exact
  architectural preconditions and a stable configuration.
- The paper states open cases and modeling limits, demonstrating that even a
  carefully formalized architecture contract must keep a claim ledger.

## Relevance

All mapping mutations should pass through one transaction engine with
authority checks, page-table ownership or locking, release publication, local
and remote invalidation, acknowledgements, generations, and deferred physical
reuse. A driver or managed runtime must never directly edit live hardware page
tables without an equivalent protected delegation protocol.

## Limits

The model targets Armv8-A and does not claim coverage of every architecture
feature, side channel, dirty/access-bit behavior, instruction-fetch interaction,
or invalidation form. Other ISAs need their own conformance evidence.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
