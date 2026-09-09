---
title: "Relaxed exception semantics for Arm-A (extended version)"
kind: source
created: "2026-09-08"
authors:
  - "Ben Simner"
  - "Alasdair Armstrong"
  - "Thomas Bauereiss"
  - "Brian Campbell"
  - "Ohad Kammar"
  - "Jean Pichon-Pharabod"
  - "Peter Sewell"
published: "2024-12-19"
citation_key: "simner-et-al-2024-relaxed-exception-semantics"
container: "arXiv"
edition: "arXiv:2412.15140v1"
isbn: null
doi: null
url: "https://arxiv.org/pdf/2412.15140"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# Relaxed exception semantics for Arm-A (extended version)

## Reference

Ben Simner, Alasdair Armstrong, Thomas Bauereiss, Brian Campbell, Ohad Kammar, Jean Pichon-Pharabod, Peter Sewell. [Relaxed exception semantics for Arm-A (extended version)](https://arxiv.org/pdf/2412.15140). arXiv, 2024-12-19. arXiv:2412.15140v1. Accessed 2026-09-08.

## Research question or contribution

How Arm exceptions interact with relaxed memory and context synchronization.

## Method

Primary formal-model and hardware-litmus research. Read §§1.2, 3.1–3.2, 5.1 and 7.3; the paper reports 61 litmus tests and observations on selected Cortex-A processors.

## Findings

Exception transitions are not general memory barriers. Context synchronization and cross-thread request/acknowledgement ordering need separate treatment, with behavior qualified by architectural features.

## Relevance

Make exception-state preservation and memory-ordering contracts explicit and separate in the entry and remote-event services.

## Limits

The model is not the normative architecture. Its treatment excludes imprecise exceptions and is incomplete for the full interrupt controller and system-register space; tested processors do not represent every implementation.

## Derived work

- [Frame normalization and bounded dispatch](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/frame-normalization-and-dispatch.md) — architecture synthesis constrained by this source.
- [Nested-event and terminal handoff](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/nested-event-and-terminal-handoff.md) — architecture synthesis constrained by this source.
