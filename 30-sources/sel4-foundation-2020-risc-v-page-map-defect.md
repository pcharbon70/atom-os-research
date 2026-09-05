---
title: "seL4 12.0.0 RISC-V page-map defect notice"
kind: source
created: "2026-09-04"
authors:
  - "seL4 Foundation"
published: 2020
citation_key: "sel4-foundation-2020-risc-v-page-map-defect"
container: "seL4 12.0.0 release notes"
edition: "12.0.0"
isbn: null
doi: null
url: "https://docs.sel4.systems/releases/sel4/12.0.0.html"
accessed: "2026-09-04"
tags:
  - capabilities
  - memory-protection
  - risc-v
  - security
  - virtual-memory
aliases:
  - "seL4 RISC-V rights-masking bug"
---

# seL4 12.0.0 RISC-V page-map defect notice

## Reference

seL4 Foundation. *seL4 Version 12.0.0 Release*, 21 October 2020, RISC-V “Fix
page map bug” notice.
[Versioned release note](https://docs.sel4.systems/releases/sel4/12.0.0.html).

## Documented defect

The release notes describe a defect in `decodeRISCVFrameInvocation`: after
requested R/W/X rights were masked with a frame capability's rights, they could
become `000`. With the valid bit set, RISC-V interprets `R=W=X=0` as a next-
level page-table pointer rather than a leaf frame mapping; `V=0` is invalid
regardless of those rights. The malformed valid entry allowed a user to
construct nearly arbitrary mappings, including kernel code and data. C
verification of the RISC-V port discovered the defect.

## Findings

- Capability attenuation can change the semantic *kind* of a raw descriptor,
  not only its access rights.
- Validating a requested leaf before rights masking is insufficient; the final
  effective semantic object must still be a legal leaf.
- Context-dependent bit encodings make typed `LeafSpec` and `TableLinkSpec`
  inputs safer than one flags word used for both.
- Verification found a vulnerability in a mature high-assurance codebase,
  reinforcing the need for backend-specific and post-transform checks.

## Relevance

Atom's validator should construct a typed effective mapping after all
authority intersections. Its encoder should accept distinct leaf and table-
link types, set contextual bits itself, and decode/assert the resulting entry
in tests. An empty rights intersection is a rejection, never an implicit
table-link encoding.

## Limits

This is a concise official release notice, not a full incident or proof report.
It concerns one historical RISC-V implementation bug. The recommended Atom
type structure and decode-after-encode check are deductions, not seL4 API
requirements.

## Derived work

- [Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md)
- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
