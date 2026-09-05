---
title: "Don't shoot down TLB shootdowns!"
kind: source
created: "2026-09-04"
authors:
  - "Nadav Amit"
  - "Amy Tai"
  - "Michael Wei"
published: 2020
citation_key: "amit-et-al-2020-dont-shoot-down-tlb-shootdowns"
container: "Proceedings of the Fifteenth European Conference on Computer Systems"
edition: null
isbn: "978-1-4503-6882-7"
doi: "10.1145/3342195.3387518"
url: "https://doi.org/10.1145/3342195.3387518"
accessed: "2026-09-04"
tags:
  - linux
  - multicore
  - operating-systems
  - performance
  - tlb
  - virtual-memory
aliases:
  - "Don't shoot down TLB shootdowns"
---

# Don't shoot down TLB shootdowns!

## Reference

Nadav Amit, Amy Tai, and Michael Wei. “Don't Shoot Down TLB Shootdowns!”
*EuroSys 2020*, article 35, 14 pages. DOI
[10.1145/3342195.3387518](https://doi.org/10.1145/3342195.3387518).
[Author-hosted paper](https://nadav.amit.zone/publications/pdfs/amit2020tlb.pdf).

## Research question or contribution

Which parts of a conventional synchronous TLB shootdown can safely overlap,
acknowledge earlier, defer, or batch so the initiating and responding CPUs do
less serialized work?

## Method

The authors analyze correctness constraints for four optimizations, implement
them in Linux 5.2.8 on x86, and evaluate microbenchmarks and applications on
multisocket systems. The techniques include concurrent initiator/responder
work, early acknowledgement, deferred user-space invalidation, and safer
aggressive batching.

## Findings

- An acknowledgement may be sent after a target has entered the IPI handler
  and can no longer access the affected user mapping, allowing local flush work
  to overlap with the initiator.
- That early acknowledgement is not sufficient when page-table pages will be
  freed, because speculative or in-progress page walks may still reference
  them.
- NMI-like paths and kernel user-access helpers can violate the assumption that
  an IPI handler closes all access, so they require an additional guard.
- Deferring a flush until return to user mode can be safe only when the CPU
  cannot access the mapping in the interim and the implementation supplies the
  required ordering and speculation defenses.
- The reported implementation reduced shootdown latency by about 10–20% for
  the two principal techniques; combinations produced larger initiator and
  responder reductions in the paper's particular cross-socket microbenchmark.

## Relevance

The work forces Atom to name different completion facts. Under the paper's
strict return gates, an early response can at most support Atom's weaker
`CpuUserReturnClosed`; it does not establish `CpuAccessQuiescent` for privileged
helper borrows, `CpuTranslationQuiescent`, table-specific
`HardwareWalkerQuiescent(table)`, or safe reclamation. Every optimization must
preserve the caller's requested proof class instead of returning one
undifferentiated “flush complete” result.

## Limits

The implementation and measurements are Linux/x86-specific and depend on the
kernel's interrupt, NMI, uaccess, scheduler, and page-table conventions. The
performance percentages are not portable. The proposed Atom proof classes and
state machine are cross-source synthesis, not constructs evaluated by the
paper.

## Derived work

- [Invalidation planner](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/invalidation-planner.md)
- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
- [Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
