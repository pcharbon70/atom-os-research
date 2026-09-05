---
title: "Secure memory management on modern hardware"
kind: source
created: "2026-09-04"
authors:
  - "Reto Achermann"
  - "Nora Hossle"
  - "Lukas Humbel"
  - "Daniel Schwyn"
  - "David Cock"
  - "Timothy Roscoe"
published: 2020
citation_key: "achermann-et-al-2020-secure-memory-management"
container: "arXiv preprint 2009.02737"
edition: null
isbn: null
doi: "10.48550/arXiv.2009.02737"
url: "https://arxiv.org/abs/2009.02737"
accessed: "2026-09-04"
tags:
  - capabilities
  - hardware-heterogeneity
  - memory-protection
  - operating-systems
  - virtual-memory
aliases:
  - "Secure memory management reference monitor"
---

# Secure memory management on modern hardware

## Reference

Reto Achermann, Nora Hossle, Lukas Humbel, Daniel Schwyn, David Cock, and
Timothy Roscoe. “Secure Memory Management on Modern Hardware.” arXiv
2009.02737, 2020. DOI
[10.48550/arXiv.2009.02737](https://doi.org/10.48550/arXiv.2009.02737).
[Author-hosted paper](https://retoachermann.ch/static/papers/achermann-2020-smm.pdf).

## Research question or contribution

How can a reference monitor mediate memory authority when heterogeneous modern
systems contain several translation and protection engines with distinct
names, configuration paths, and reachability?

## Method

The authors classify memory-management vulnerabilities as policy-enforcement,
reference-monitor partitioning, and name-resolution failures. They derive an
OS-independent reference-monitor model from a decoding-net representation,
provide an executable Haskell specification, discuss capability and UNIX-style
integration, and evaluate selected prototype operations.

## Findings

- A CPU-MMU-only reference monitor is incomplete when IOMMUs, accelerators,
  firewalls, and other translation nodes can independently reach memory.
- All configuration paths into those nodes require complete mediation, and the
  reference monitor's state must itself be protected.
- Address names need an explicit resolution model; assuming one universal
  physical address space creates alias and authority mistakes.
- The evaluation reports less than 5% overhead for the selected explicit-
  address-space VM operations and 5.7% for a model query followed by
  translation reconfiguration. The authors argue that the model adds no
  *inherent* overhead, but that design claim does not mean zero measured cost.

## Relevance

The encoder and mapping ledger should be the only CPU-translation mutation
path and must compose with, not stand in for, the DMA translation monitor. Raw
addresses are resolved to typed objects and authority before encoding, while
boot, recovery, and diagnostic paths must be enumerated rather than bypass the
same mediation.

## Limits

This is a preprint, abstract model, and prototype evaluation rather than a
production-kernel proof. Correspondence between the abstract model and the
executable Haskell specification was assessed by inspection, not a mechanized
end-to-end verification. It does not prescribe Atom's transaction, shootdown,
or recovery API, and no measured result transfers to the target hardware.

## Derived work

- [Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md)
- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
- [Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
