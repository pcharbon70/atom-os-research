---
title: "Formally verified system initialisation"
kind: source
created: "2026-09-03"
authors:
  - "Andrew Boyton"
  - "June Andronick"
  - "Callum Bannister"
  - "Matthew Fernandez"
  - "Xin Gao"
  - "David Greenaway"
  - "Gerwin Klein"
  - "Corey Lewis"
  - "Thomas Sewell"
published: 2013
citation_key: "boyton-et-al-2013-verified-system-initialisation"
container: "International Conference on Formal Engineering Methods (ICFEM)"
edition: null
isbn: null
doi: "10.1007/978-3-642-41202-8_6"
url: "https://trustworthy.systems/publications/nicta_full_text/7047.pdf"
accessed: "2026-09-03"
tags:
  - boot
  - capabilities
  - configuration
  - formal-verification
  - sel4
aliases:
  - "Verified seL4 initialiser"
---

# Formally verified system initialisation

## Reference

Andrew Boyton, June Andronick, Callum Bannister, Matthew Fernandez, Xin Gao,
David Greenaway, Gerwin Klein, Corey Lewis, and Thomas Sewell. “Formally
Verified System Initialisation.” *International Conference on Formal
Engineering Methods*, LNCS 8144, 2013, pp. 70–85. DOI
[10.1007/978-3-642-41202-8_6](https://doi.org/10.1007/978-3-642-41202-8_6).
[Author-hosted paper](https://trustworthy.systems/publications/nicta_full_text/7047.pdf)
and [publication record](https://trustworthy.systems/publications/nictaabstracts/Boyton_ABFGGKLS_13.abstract).

## Research question or contribution

Can a general-purpose capability microkernel initialise a component system
automatically while providing a machine-checked connection between the desired
capability configuration and the state reached by the initialiser?

## Method

The work defines a formal model of the desired capDL system state and a model
of an initialisation algorithm, then proves in Isabelle/HOL that the algorithm
reaches a state conforming to the description. It separates specification of
the authority graph from the procedural steps that allocate objects and install
capabilities.

## Findings

- Automatic initialisation can replace hand-written sequences whose partial
  failures and capability-installation order are difficult to audit.
- A declarative configuration supplies a stable target against which the
  final installed system can be related formally.
- The proof establishes the stated conformance result for the formal model,
  including treatment of additional inert capability state needed by the
  initialiser.
- The result is a necessary bridge between kernel access-control properties
  and system-wide reasoning: a secure kernel cannot compensate for an
  incorrectly installed initial authority graph.

## Relevance

Atom OS should treat bootstrap as a transaction from validated architecture
facts and a trusted manifest to an inspectable authority graph. The design can
borrow the paper's declarative target and refinement structure while extending
the configuration with resource accounts, CPU reserves, recovery/reset escrow,
failure routes, and hardware-lifetime profiles. A postcondition should state
exactly which temporary capabilities remain and why each is inert or sealed.

## Limits

The published result is about a particular formal model and initialiser for
seL4 component systems. It does not verify this project's boot parser,
architecture adapter, generated binary, manifest signature path, hardware
state, handoff acknowledgement, or recovery-escrow extensions. The current
capDL loader documentation also distinguishes verified model results from
implementation and feature coverage. Atom OS must preserve that distinction
and cannot inherit the proof by using a similar manifest.

## Derived work

- [Bootstrap and root-authority handoff](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
