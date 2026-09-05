---
title: "FATE and DESTINI: A framework for cloud recovery testing"
kind: source
created: "2026-09-05"
authors:
  - "Haryadi S. Gunawi"
  - "Thanh Do"
  - "Pallavi Joshi"
  - "Peter Alvaro"
  - "Joseph M. Hellerstein"
  - "Andrea C. Arpaci-Dusseau"
  - "Remzi H. Arpaci-Dusseau"
  - "Koushik Sen"
  - "Dhruba Borthakur"
published: 2011
citation_key: "gunawi-et-al-2011-fate-destini"
container: "8th USENIX Symposium on Networked Systems Design and Implementation"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/nsdi11/fate-and-destini-framework-cloud-recovery-testing"
accessed: "2026-09-05"
tags:
  - fault-injection
  - recovery
  - testing
aliases:
  - "FATE and DESTINI"
---

# FATE and DESTINI: A framework for cloud recovery testing

## Reference

Haryadi S. Gunawi et al. “FATE and DESTINI: A Framework for Cloud Recovery
Testing.” *8th USENIX Symposium on Networked Systems Design and Implementation
(NSDI '11)*, 2011. [USENIX record and
paper](https://www.usenix.org/conference/nsdi11/fate-and-destini-framework-cloud-recovery-testing).

## Research question or contribution

How can recovery behavior be exercised systematically across combinations of
failure points and checked against explicit, readable expected outcomes?

## Method

FATE assigns stable identifiers to failure scenarios and prioritizes distinct
multi-failure combinations. DESTINI expresses relational recovery
specifications. The authors integrated the tools with several distributed Java
systems, explored more than 40,000 scenarios, wrote 74 specifications, found 16
new bugs, and reproduced 51 known bugs.

## Findings

- Recovery paths need behavioral specifications for intermediate and terminal
  states; a global invariant may be intentionally false while recovery is in
  progress.
- Stable failure identifiers make explored schedules reproducible and allow
  systematic rather than purely random coverage.
- Multiple failures produce a combinatorial explosion, so coverage must be
  stratified and prioritized without pretending it is exhaustive.
- Checking from several views catches contradictions that a single local
  success flag misses.
- Recovery tests are most valuable when the injection service and expected
  outcome language evolve with the system rather than remain ad hoc scripts.

## Relevance

Atom should assign stable IDs to capture phases and injected conditions, derive
deterministic schedules from model counterexamples, and assert both local
record invariants and global quarantine/custody outcomes. The matrix should
include compound failures such as nested entry plus full queue, sink failure
plus missing CPU, and recovery-service restart plus a lost receipt.

## Limits

The evaluated systems are application-level distributed stores, not kernels or
hardware RAS paths. Aspect-oriented I/O injection does not reproduce corrupted
registers, caches, DMA, firmware, power loss, or stack failure. The work
supports the test architecture and coverage discipline, not specific Atom
fault semantics.

## Derived work

- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
- [Architecture faults and diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md)
