---
title: "seL4: From general purpose to a proof of information flow enforcement"
kind: source
created: "2026-08-31"
authors:
  - "Toby Murray"
  - "Daniel Matichuk"
  - "Matthew Brassil"
  - "Peter Gammie"
  - "Timothy Bourke"
  - "Sean Seefried"
  - "Corey Lewis"
  - "Xin Gao"
  - "Gerwin Klein"
published: 2013
citation_key: "murray-et-al-2013-sel4-information-flow"
container: "2013 IEEE Symposium on Security and Privacy"
edition: null
isbn: "978-0-7695-4977-4"
doi: "10.1109/SP.2013.35"
url: "https://sel4.systems/Research/pdfs/sel4-from-general-purpose-to-proof-information-flow-enforcement.pdf"
accessed: "2026-08-31"
tags:
  - capabilities
  - formal-verification
  - information-flow
  - microkernels
aliases:
  - "seL4 information-flow proof"
---

# seL4: From general purpose to a proof of information flow enforcement

## Reference

Toby Murray et al. “seL4: From General Purpose to a Proof of Information Flow
Enforcement.” *2013 IEEE Symposium on Security and Privacy*, pages 415–429.
DOI [10.1109/SP.2013.35](https://doi.org/10.1109/SP.2013.35).
[Open PDF](https://sel4.systems/Research/pdfs/sel4-from-general-purpose-to-proof-information-flow-enforcement.pdf).

## Research question or contribution

Can the implementation of a general-purpose microkernel be shown, by a
machine-checked proof, to enforce a configured information-flow policy?

## Method

The authors formalize a variant of intransitive noninterference, connect it to
seL4's functional-correctness proof, state a threat model and valid kernel
configuration, and prove the property for the kernel's C implementation within
the model.

## Findings

- Capability-mediated kernel objects can be configured as isolated partitions
  with explicitly permitted flows.
- Security depends on system configuration and policy as well as correct kernel
  implementation; a general API does not make every configuration secure.
- The proof covers storage channels in modeled kernel state, but not fine-grain
  hardware timing channels.
- Compiler, assembly, hardware, and boot behavior remain assumptions. The
  evaluated model also imposed strong restrictions on DMA.

## Relevance

The kernel design needs explicit abstract state for capabilities, domains,
calls, budgets, and teardown—not only tests of a concrete implementation. Its
security claim must state the configured authority graph and which architecture,
DMA, boot, timing, and compiler assumptions remain outside the proof.

## Limits

This proof applies to seL4 and its stated model. Similar object names provide no
transferred assurance. The project also requires dynamic restart, generational
IPC cancellation, and BEAM runtime domains, none of which is established by
this result.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
