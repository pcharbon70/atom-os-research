---
title: "capDL: A language for describing capability-based systems"
kind: source
created: "2026-09-03"
authors:
  - "Ihor Kuz"
  - "Gerwin Klein"
  - "Corey Lewis"
  - "Adam Christopher Walker"
published: 2010
citation_key: "kuz-et-al-2010-capdl"
container: "Asia-Pacific Workshop on Systems (APSys)"
edition: null
isbn: null
doi: "10.1145/1851276.1851284"
url: "https://trustworthy.systems/publications/nicta_full_text/3679.pdf"
accessed: "2026-09-03"
tags:
  - capabilities
  - configuration
  - formal-methods
  - microkernels
  - sel4
aliases:
  - "capDL paper"
---

# capDL: A language for describing capability-based systems

## Reference

Ihor Kuz, Gerwin Klein, Corey Lewis, and Adam Christopher Walker. “capDL: A
Language for Describing Capability-Based Systems.” *Asia-Pacific Workshop on
Systems (APSys)*, New Delhi, 2010, pp. 31–35. DOI
[10.1145/1851276.1851284](https://doi.org/10.1145/1851276.1851284).
[Author-hosted paper](https://trustworthy.systems/publications/nicta_full_text/3679.pdf)
and [publication record](https://trustworthy.systems/publications/nictaabstracts/Kuz_KLW_10.abstract).

## Research question or contribution

How can a capability system describe the concrete objects, capabilities, and
capability distribution from which system-level isolation and information-flow
claims are made? The paper introduces capDL, a declarative language for seL4
system configurations, with a syntax and semantics intended to connect a
designed authority graph to the graph installed in the running system.

## Method

The authors identify the object and capability information needed to describe
an seL4 system, define the language's principal constructs and semantics, and
work through a small example. This is a design and modelling paper rather than
a performance evaluation or an end-to-end verification of a production boot
path.

## Findings

- Capability-based isolation depends on the actual distribution of authority,
  not only on the kernel's capability rules. That distribution therefore needs
  an explicit, analysable description.
- A declarative model can name kernel objects, capability slots, rights, and
  relationships without embedding the configuration in ad hoc initialisation
  code.
- The same description can support configuration generation and higher-level
  reasoning about isolation and permitted information flow.
- Capability names in the description are modelling designators; the security
  result still depends on the kernel objects and capability graph installed at
  runtime matching that description.

## Relevance

The minimal kernel should accept a versioned initial-authority manifest whose
normal form can be audited, hashed into crash evidence, and checked before
temporary bootstrap authority is sealed. capDL provides the strongest direct
precedent for making that authority graph data rather than implicit boot code.
It also motivates comparing the manifest's desired graph with a post-handoff
enumeration from protected kernel state.

The Atom OS manifest must additionally describe resource accounts, scheduling
reserves, recovery escrows, hardware profiles, and lifecycle gates. Those are
project proposals rather than capDL results.

## Limits

The paper is short and focuses on expressing capability distributions. It does
not prove that an arbitrary description is safe, that the C initialiser installs
it correctly, or that all surrounding boot firmware and hardware are trusted.
It does not specify the proposed one-way handoff acknowledgement, independent
recovery escrow, quota conservation, or rollback behaviour. A manifest can
faithfully describe a dangerous authority graph; separate policy checks and a
verified installer remain necessary.

## Derived work

- [Bootstrap and root-authority handoff](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff.md)
- [Capability spaces and authority](../20-notes/minimal-privileged-kernel-components/capability-spaces-and-authority.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
