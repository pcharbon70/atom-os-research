---
title: "A realistic evaluation of memory hardware errors and software system susceptibility"
kind: source
created: "2026-09-05"
authors:
  - "Xin Li"
  - "Michael C. Huang"
  - "Kai Shen"
  - "Lingkun Chu"
published: 2010
citation_key: "li-et-al-2010-realistic-memory-error-evaluation"
container: "2010 USENIX Annual Technical Conference"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/usenix-atc-10/realistic-evaluation-memory-hardware-errors-and-software-system"
accessed: "2026-09-05"
tags:
  - fault-injection
  - hardware-errors
  - memory
  - reliability
aliases:
  - "Realistic memory-error evaluation"
---

# A realistic evaluation of memory hardware errors and software system susceptibility

## Reference

Xin Li, Michael C. Huang, Kai Shen, and Lingkun Chu. “A Realistic Evaluation
of Memory Hardware Errors and Software System Susceptibility.” *2010 USENIX
Annual Technical Conference*. [USENIX record and
paper](https://www.usenix.org/conference/usenix-atc-10/realistic-evaluation-memory-hardware-errors-and-software-system).

## Research question or contribution

How do conclusions about system susceptibility change when fault injection is
driven by observed multi-bit, row, column, chip, transient, and recurring
memory-error patterns rather than only isolated random bit flips?

## Method

The authors monitored production systems totaling more than 800 GB of memory
for roughly nine months, collected address-level error traces, built a trace-
driven injector outside the guest in a virtual-machine monitor, and compared
application/OS manifestations with simpler injection models.

## Findings

- Field errors include significant nontransient and spatially correlated
  patterns; independent single-bit injection can understate system impact.
- Application and OS outcomes differ materially with the error model and the
  location of corrupted data.
- Placing the injector outside the target reduces the chance that corrupting
  the subject also destroys the test controller and observation path.
- An observed clean exit or continued operation is not proof that no silent
  corruption occurred; the evaluation needs external correctness oracles.
- Representative traces improve a campaign but still do not reproduce every
  controller, firmware, poison-propagation, timing, or power condition.

## Relevance

Atom's fake backend should cover every raw-bit combination, while emulator and
hardware campaigns should include spatially correlated, recurring, and
multi-component scenarios. Test control and outcome oracles should run outside
the faulted domain. Classifier validation must include silent-corruption and
wrong-scope outcomes, not only crash/no-crash.

## Limits

The system and traces are historical, and virtualization-mediated injection is
not equivalent to faulty silicon. The paper evaluates susceptibility and error
models, not Atom's proposed capture or containment protocol.

## Derived work

- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
