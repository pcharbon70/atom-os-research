---
title: "Reducing liveness to safety in first-order logic"
kind: source
created: "2026-09-04"
authors:
  - "Oded Padon"
  - "Jochen Hoenicke"
  - "Giuliano Losa"
  - "Andreas Podelski"
  - "Mooly Sagiv"
  - "Sharon Shoham"
published: 2018
citation_key: "padon-et-al-2018-reducing-liveness-to-safety"
container: "Proceedings of the ACM on Programming Languages 2 (POPL)"
edition: null
isbn: null
doi: "10.1145/3158114"
url: "https://doi.org/10.1145/3158114"
accessed: "2026-09-04"
tags:
  - formal-methods
  - liveness
  - multicore
  - tlb
  - verification
aliases:
  - "TLB shootdown liveness case study"
---

# Reducing liveness to safety in first-order logic

## Reference

Oded Padon, Jochen Hoenicke, Giuliano Losa, Andreas Podelski, Mooly Sagiv, and
Sharon Shoham. “Reducing Liveness to Safety in First-Order Logic.” *PACMPL* 2,
POPL, article 26, 2018. DOI
[10.1145/3158114](https://doi.org/10.1145/3158114).
[Author-hosted paper](https://www.wisdom.weizmann.ac.il/~padon/reducing-liveness-to-safety-in-first-order-logic/popl18-reducing-liveness-to-safety-in-first-order-logic.pdf).

## Research question or contribution

Can liveness properties of parameterized infinite-state protocols be reduced
to safety properties that automated first-order verification tools can prove?

## Method

The paper presents a verification transformation and applies it to several
protocols. One case study formalizes a Mach-style TLB shootdown in which a
mutator interrupts every processor using a page map and waits until responders
flush or deactivate.

## Findings

- Safety and liveness are distinct obligations: preventing premature mapping
  reuse does not show that a shootdown will eventually finish.
- The case study imports a repaired shootdown algorithm from prior safety work;
  that repair added an atomic critical region absent from the informal
  algorithm, showing how decisive exact atomicity can be.
- Padon et al. provide the first mechanized liveness proof for that repaired
  model, under explicit strong-fairness assumptions for lock acquisition rather
  than deriving progress from the protocol alone.
- First-order parameterized models can expose assumptions about arbitrary CPU
  counts that finite scenario tests may miss.

## Relevance

Atom should model the shootdown and activation product state before optimizing
it, prove safety independently from liveness, and list interrupt-delivery,
scheduler, lock, CPU-lifecycle, and reset fairness assumptions. Timeout and
quarantine behavior must remain valid when liveness assumptions fail.

## Limits

The case study is an abstract Mach protocol, not a model of current ISA page-
table walkers, firmware, DMA, or malfunctioning CPUs. The paper validates a
verification method; it does not prove the proposed Atom algorithm.

## Derived work

- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
- [Mapping transaction](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-transaction.md)
