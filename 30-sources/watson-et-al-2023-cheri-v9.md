---
title: "Capability Hardware Enhanced RISC Instructions: CHERI Instruction-Set Architecture, version 9"
kind: source
created: "2026-08-29"
authors:
  - "Robert N. M. Watson"
  - "Peter G. Neumann"
  - "Jonathan Woodruff"
  - "Michael Roe"
  - "Hesham Almatary"
  - "Jonathan Anderson"
  - "John Baldwin"
  - "Graeme Barnes"
  - "David Chisnall"
  - "Jessica Clarke"
  - "Brooks Davis"
  - "Lee Eisen"
  - "Nathaniel Wesley Filardo"
  - "Franz A. Fuchs"
  - "Richard Grisenthwaite"
  - "Alexandre Joannou"
  - "Ben Laurie"
  - "A. Theodore Markettos"
  - "Simon W. Moore"
  - "Steven J. Murdoch"
  - "Kyndylan Nienhuis"
  - "Robert Norton"
  - "Alexander Richardson"
  - "Peter Rugg"
  - "Peter Sewell"
  - "Stacey Son"
  - "Hongyan Xia"
published: 2023
citation_key: "watson-et-al-2023-cheri-v9"
container: "University of Cambridge Technical Report UCAM-CL-TR-987"
edition: "Version 9"
isbn: null
doi: "10.48456/tr-987"
url: "https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-987.html"
accessed: "2026-08-29"
tags:
  - capabilities
  - compartmentalization
  - hardware-security
  - memory-safety
  - operating-systems
aliases:
  - "CHERI ISAv9"
---

# Capability Hardware Enhanced RISC Instructions: CHERI Instruction-Set Architecture, version 9

## Reference

Robert N. M. Watson et al. *Capability Hardware Enhanced RISC Instructions:
CHERI Instruction-Set Architecture (Version 9).* UCAM-CL-TR-987, University of
Cambridge, September 2023. DOI
[10.48456/tr-987](https://doi.org/10.48456/tr-987). [Report page and
PDF](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-987.html).

## Research question or contribution

Can tagged, bounded, permission-bearing hardware capabilities add fine-grained
memory safety and scalable compartmentalization while composing with
conventional ISAs, MMUs, and incremental software adoption?

## Method

The report specifies the cross-architecture protection model and concrete
CHERI-RISC-V, Morello/Arm, and sketched x86 mappings, informed by formal models,
toolchains, FPGA and silicon implementations, operating systems, and
applications developed over thirteen years.

## Findings

- CHERI capabilities bind address, bounds, permissions, provenance, sealing,
  and a protected tag. Derivation is monotonic and supports least authority
  within an address space.
- CHERI complements rather than eliminates page-based virtual memory: MMUs
  still provide allocation, coarse isolation, and virtualization.
- Hybrid modes ease adoption; pure-capability designs obtain stronger
  invariants but impose ABI, representation, toolchain, and porting costs.
- Capability revocation and temporal safety are not free consequences of
  spatial bounds; system policy and allocation discipline remain necessary.

## Relevance

The software capability model should not depend on CHERI, but resource handles
should be designed so a future CHERI target can reinforce them. CHERI is a
promising hardening profile, not a prerequisite for the first kernel or a
replacement for IOMMU/device capabilities.

## Limits

CHERI hardware and toolchain availability is narrower than conventional RV64
or AArch64, and this project's chosen Zig version must be evaluated separately
for capability-aware code generation and ABI support. The report is not a
performance guarantee for this design.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
