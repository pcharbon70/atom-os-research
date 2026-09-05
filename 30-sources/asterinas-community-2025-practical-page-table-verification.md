---
title: "Towards practical formal verification for a general-purpose OS in Rust"
kind: source
created: "2026-09-04"
authors:
  - "CertiK"
  - "Hongliang Tian"
published: 2025
citation_key: "asterinas-community-2025-practical-page-table-verification"
container: "Asterinas blog"
edition: null
isbn: null
doi: null
url: "https://asterinas.github.io/2025/02/13/towards-practical-formal-verification-for-a-general-purpose-os-in-rust.html"
accessed: "2026-09-04"
tags:
  - formal-methods
  - operating-systems
  - page-tables
  - rust
  - virtual-memory
aliases:
  - "Asterinas page-table verification report"
---

# Towards practical formal verification for a general-purpose OS in Rust

## Reference

CertiK and Hongliang Tian. “Towards Practical Formal Verification for a
General-Purpose OS in Rust.” *Asterinas Blog*, 13 February 2025.
[First-party engineering report](https://asterinas.github.io/2025/02/13/towards-practical-formal-verification-for-a-general-purpose-os-in-rust.html).

## Research question or contribution

How can a general-purpose Rust OS structure and verify the unsafe page and
page-table core beneath a safe virtual-memory interface?

## Method

The post reports an ongoing Verus effort over Asterinas's page-management TCB.
It presents typed `VmSpace`, `PageTable`, `PageTableNode`, and physical-page
objects, cursor-based locking, abstract tree and flat models, and a relational
refinement workflow. It gives progress counts and examples rather than a
peer-reviewed end-to-end proof.

## Findings

- User and kernel virtual spaces, table mode, entry encoding, paging constants,
  and physical-page purpose are represented in types rather than raw pointers.
- Range cursors lock the relevant table node and ancestors instead of the
  entire page table, creating an explicit unit for navigation and mutation.
- The project reported 11 of 14 high-priority targets verified, with about
  6,000 lines of specification, 2,000 lines of proof, and 2,000 lines of
  executable code at publication time.
- Verification exposed a race that could prematurely free a page-table node,
  directly illustrating the importance of making table-node lifetime a proof
  obligation.

## Relevance

This is practical evidence for typed page-table pages, mode-specific roots,
range-scoped mutation objects, and a refinement relation from hardware trees
to a flat semantic mapping ledger. The discovered lifetime race is a useful
falsifier for Atom's encoder and reclamation design.

## Limits

This is a first-party work-in-progress report, not a peer-reviewed completed
verification. Three listed targets, concurrency reasoning, and reliable
linkage between verified artifacts and the evolving kernel remained open. Its
claims do not establish Atom memory safety or hardware-level TLB completion.

## Derived work

- [Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md)
- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
- [Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
