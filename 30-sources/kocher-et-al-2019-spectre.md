---
title: "Spectre attacks: Exploiting speculative execution"
kind: source
created: "2026-09-02"
authors:
  - "Paul Kocher"
  - "Jann Horn"
  - "Anders Fogh"
  - "Daniel Genkin"
  - "Daniel Gruss"
  - "Werner Haas"
  - "Mike Hamburg"
  - "Moritz Lipp"
  - "Stefan Mangard"
  - "Thomas Prescher"
  - "Michael Schwarz"
  - "Yuval Yarom"
published: 2019
citation_key: "kocher-et-al-2019-spectre"
container: "2019 IEEE Symposium on Security and Privacy"
edition: null
isbn: null
doi: "10.1109/SP.2019.00002"
url: "https://doi.org/10.1109/SP.2019.00002"
accessed: "2026-09-02"
tags:
  - branch-prediction
  - security
  - side-channels
  - speculative-execution
aliases:
  - "Spectre"
---

# Spectre attacks: Exploiting speculative execution

## Reference

Paul Kocher et al. “Spectre Attacks: Exploiting Speculative Execution.” *2019
IEEE Symposium on Security and Privacy*, pages 1–19, 2019. DOI
[10.1109/SP.2019.00002](https://doi.org/10.1109/SP.2019.00002).

## Research question or contribution

Can an attacker mistrain speculative control flow so a victim transiently
executes operations that disclose data through microarchitectural state?

## Method

The paper demonstrates bounds-check bypass and branch-target-injection styles
of attack and recovers transiently accessed data using cache timing.

## Findings

- Speculative execution can perform operations absent from committed program
  behavior while leaving measurable microarchitectural effects.
- Attacks can cross software isolation boundaries that are correct in the
  architectural instruction semantics.
- Branch prediction and shared microarchitectural state make mitigation
  dependent on processor generation, code shape, and isolation boundary.
- General mitigation is not one universal fence; defenses include constraining
  speculation, changing code sequences, partitioning state, and processor or
  microcode support, each with performance and coverage tradeoffs.

## Relevance

Privileged entry and return must apply a pinned mitigation profile rather than
hard-code one folklore barrier. The profile can require predictor controls,
serialization, address-space isolation, or scheduling restrictions, and its
coverage and cost must be testable per machine generation.

## Limits

The original paper establishes an attack class, not a complete current catalog
or permanent mitigation recipe. Later variants and vendor-specific guidance
must be tracked by a concrete port's errata process.

## Derived work

- [Privileged entry, exit, and execution context](../20-notes/privileged-entry-exit-and-execution-context.md)
