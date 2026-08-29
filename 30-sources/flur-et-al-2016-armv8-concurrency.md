---
title: "Modelling the ARMv8 architecture, operationally: Concurrency and ISA"
kind: source
created: "2026-08-29"
authors:
  - "Shaked Flur"
  - "Kathryn Gray"
  - "Christopher Pulte"
  - "Susmit Sarkar"
  - "Ali Sezgin"
  - "Luc Maranget"
  - "Will Deacon"
  - "Peter Sewell"
published: 2016
citation_key: "flur-et-al-2016-armv8-concurrency"
container: "Proceedings of the 43rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages"
edition: null
isbn: null
doi: "10.1145/2837614.2837615"
url: "https://research-repository.st-andrews.ac.uk/handle/10023/8431"
accessed: "2026-08-29"
tags:
  - aarch64
  - arm
  - concurrency
  - formal-methods
  - memory-models
aliases:
  - "Operational ARMv8 model"
---

# Modelling the ARMv8 architecture, operationally: Concurrency and ISA

## Reference

Shaked Flur et al. “Modelling the ARMv8 Architecture, Operationally:
Concurrency and ISA.” *POPL '16*, pages 608–621, 2016. DOI
[10.1145/2837614.2837615](https://doi.org/10.1145/2837614.2837615).
[Institutional record and accepted manuscript](https://research-repository.st-andrews.ac.uk/handle/10023/8431).

## Research question or contribution

What executions may Armv8 hardware expose to concurrent software, and can an
operational model clarify that contract sufficiently for testing and
verification?

## Method

The authors develop executable semantics for the application-level ISA and
concurrency model through collaboration with Arm, litmus testing, and formal
comparison with architectural intent.

## Findings

- Weak-memory behavior is an architectural contract, not merely an
  implementation accident. Dependencies, acquire/release operations, and
  barriers have precise but non-interchangeable effects.
- Establishing a trustworthy model required iteration between prose,
  architects, executable semantics, and hardware observations.
- Correct concurrent abstractions need compiler and ISA mappings as well as a
  source-language model.
- The paper's application-level focus leaves translation, exceptions, I/O, and
  full system-state interaction to further work.

## Relevance

AArch64 is valuable as a second target because it forces kernel queues,
ownership transitions, IRQ handoff, and publication protocols to state their
ordering. Architecture-specific barriers should implement architecture-neutral
invariants, never leak as ad hoc caller knowledge.

## Limits

This 2016 model is not the latest normative Arm specification and intentionally
does not cover the entire privileged architecture or microarchitectural side
channels.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
