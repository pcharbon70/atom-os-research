---
title: "Dune: Safe user-level access to privileged CPU features"
kind: source
created: "2026-08-30"
authors:
  - "Adam Belay"
  - "Andrea Bittau"
  - "Ali Mashtizadeh"
  - "David Terei"
  - "David Mazières"
  - "Christos Kozyrakis"
published: 2012
citation_key: "belay-et-al-2012-dune"
container: "10th USENIX Symposium on Operating Systems Design and Implementation"
edition: null
isbn: "978-1-931971-96-6"
doi: null
url: "https://www.usenix.org/conference/osdi12/technical-sessions/presentation/belay"
accessed: "2026-08-30"
tags:
  - delegation
  - operating-systems
  - privilege
  - protection
  - virtualization
aliases:
  - "Dune"
---

# Dune: Safe user-level access to privileged CPU features

## Reference

Adam Belay et al. “Dune: Safe User-level Access to Privileged CPU Features.”
*OSDI '12*, pages 335–348, 2012.
[USENIX paper and metadata](https://www.usenix.org/conference/osdi12/technical-sessions/presentation/belay).

## Research question or contribution

Can a process directly use privilege modes, page tables, tagged TLBs,
exceptions, and system-call interception without receiving authority over the
host machine?

## Method

Dune uses x86 virtualization to give a Linux process a process-shaped
privileged environment. A kernel module retains the protective second-level
translation and mediates exits; a user library manages the delegated features.
The paper evaluates sandboxing, intra-process privilege separation, and a
garbage collector.

## Findings

- A mechanism conventionally reserved for whole-machine virtualization can be
  used to delegate selected privileged CPU facilities while an underlying
  protection layer retains final authority.
- Direct page-table control is safe only because the kernel-controlled
  translation stage constrains the memory reachable through the process's
  tables.
- Dune exports a narrower process interface rather than emulating a complete
  machine, reducing saved state and implementation obligations.
- The transition into Dune mode and VM exits are explicit lifecycle events;
  unsupported operations fall back to the host rather than being silently
  exposed.

## Relevance

“Privileged instruction” and “kernel policy” need not be synonymous. The
hardware layer can eventually delegate carefully bounded translation,
exception, or runtime facilities to a protected managed domain if a lower
mechanism retains confinement and revocation. Such delegation should be an
optional profile, not the baseline port contract.

## Limits

Dune is a hosted x86/Linux design and assumes working virtualization hardware
and host services. It does not establish a portable interface, handle arbitrary
DMA devices, or eliminate the kernel module and host from the trusted base.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
