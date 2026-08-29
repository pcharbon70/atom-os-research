---
title: "Relaxed virtual memory in Armv8-A"
kind: source
created: "2026-08-29"
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
accessed: "2026-08-29"
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
[Authors' project page, paper, models, and tests](https://www.cl.cam.ac.uk/~pes20/RelaxedVM-Arm/).

## Research question or contribution

How do weak memory, page-table walks, TLB maintenance, multiple translation
stages, and concurrent page-table modification interact at the hardware/
software boundary?

## Method

The work develops models and bare-metal litmus tests in consultation with Arm
and pKVM developers, connects them to full instruction semantics, and tests a
defined subset on hardware.

## Findings

- Virtual-memory updates are concurrent publication protocols. Writing a PTE,
  invalidating cached translations, issuing barriers, and allowing reuse are
  not one atomic operation.
- Previously used informal assumptions were too simple for verification of
  real page-table and hypervisor behavior.
- Safe break-before-make, stage interaction, and TLB invalidation depend on a
  stable configuration and an exact ordered sequence.
- Even this extensive work has explicit non-goals and incomplete cases,
  illustrating why a kernel should centralize rather than duplicate the
  protocol.

## Relevance

All mapping mutations should pass through one transaction engine with page-
table locks or ownership, release publication, local and remote invalidation,
acknowledgement, deferred physical reuse, and traceable generations. An actor
or driver must never edit a hardware page table directly.

## Limits

The model targets Armv8-A and does not claim authoritative coverage of every
feature, side channel, access/dirty-bit behavior, instruction-fetch
interaction, or TLBI form. Other ISAs need their own proofs and tests.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
