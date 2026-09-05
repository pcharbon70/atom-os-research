---
title: "seL4 reference manual, version 16.0.0"
kind: source
created: "2026-08-31"
authors:
  - "Matthew Grosvenor"
  - "Adam Walker"
published: 2026
citation_key: "sel4-foundation-2026-reference-manual"
container: "seL4 technical documentation"
edition: "16.0.0"
isbn: null
doi: null
url: "https://sel4.systems/Info/Docs/seL4-manual-16.0.0.pdf"
accessed: "2026-08-31"
tags:
  - capabilities
  - ipc
  - microkernels
  - operating-systems
  - scheduling
  - virtual-memory
aliases:
  - "seL4 manual version 16.0.0"
---

# seL4 reference manual, version 16.0.0

## Reference

Matthew Grosvenor and Adam Walker. *seL4 Reference Manual*, version 16.0.0,
22 July 2026.
[Versioned manual](https://sel4.systems/Info/Docs/seL4-manual-16.0.0.pdf).
Supplementary mechanism checks also used the separately maintained official
[capability](https://docs.sel4.systems/Tutorials/capabilities.html),
[untyped memory](https://docs.sel4.systems/Tutorials/untyped.html),
[IPC](https://docs.sel4.systems/Tutorials/ipc),
[fault handling](https://docs.sel4.systems/Tutorials/fault-handlers.html), and
[MCS](https://docs.sel4.systems/Tutorials/mcs.html) tutorials.

## Documented mechanism

The manual documents the current kernel object model, capability spaces,
derivation and revocation, explicit kernel-object memory, IPC and notification
objects, execution contexts, MCS scheduling contexts, fault delivery, virtual
memory, interrupts, and boot authority.

## Findings

- Capabilities are kernel-protected references that combine an object with
  rights; CNodes store capabilities and form each thread's capability space.
- Copying and minting can preserve or attenuate rights. The kernel tracks
  derivation, and revoke removes descendants of a selected capability.
- Almost all post-boot physical memory is represented by untyped-memory
  capabilities. Retyping creates kernel objects; safe reuse requires removing
  derived objects first.
- Endpoints implement rendezvous IPC and capability transfer. MCS reply objects
  hold single-use reply authority; notifications provide bounded, coalescing
  signalling rather than general message queues.
- Scheduling contexts hold consumable CPU budget and can be donated to passive
  servers along synchronous IPC paths. A server that never replies can retain
  the donated context, so donation is a trust and cancellation concern.
- A fault suspends the thread and is delivered as a structured message to its
  configured handler. Missing fault handling leaves the thread suspended; the
  kernel does not choose a restart policy.
- The manual's object model and virtual-memory chapter allow one VSpace to be
  associated with one or more threads. User frames may be mapped into several
  VSpaces, while intermediate paging structures are not shared between
  VSpaces.
- Section 7.1.2 states that mapping rights requested at invocation are reduced
  by the rights on the frame capability. Callers therefore must account for
  the final effective rights, not only the requested mask.

## Relevance

This is the most concrete precedent for typed capability tables, explicit
object backing, small IPC, first-class time authority, fault endpoints, and
user-level policy. It also exposes edge cases the proposed design must specify:
large revocations, unreachable capability subtrees, call cancellation, donated
budgets, reply authority, shared-thread VSpace activation, effective mapping
rights, and reclaiming mappings separately from capabilities.

## Limits

Documentation describes seL4, not this kernel. Adopting similar objects would
not inherit seL4's proofs, and a reference manual does not itself establish the
verification status of every configuration. Some semantics vary with
configuration and architecture. The separately maintained tutorials were
accessed on 2026-08-31 and do not share the manual's version identifier. The
project additionally proposes a first-class protection-domain lifecycle anchor
and incarnation-aware cancellation, which are not claims about the seL4 API.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
- [Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md)
- [Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md)
- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
