---
title: "Kernel design for isolation and assurance of physical memory"
kind: source
created: "2026-08-31"
authors:
  - "Dhammika Elkaduwe"
  - "Philip Derrin"
  - "Kevin Elphinstone"
published: "2008-04-01"
citation_key: "elkaduwe-et-al-2008-kernel-memory-isolation"
container: "Proceedings of the 1st Workshop on Isolation and Integration in Embedded Systems"
edition: null
isbn: "978-1-60558-126-2"
doi: "10.1145/1435458.1435465"
url: "https://trustworthy.systems/publications/nicta_full_text/848.pdf"
accessed: "2026-08-31"
tags:
  - capabilities
  - formal-verification
  - memory-management
  - microkernels
  - operating-systems
  - sel4
aliases:
  - "seL4 physical-memory isolation paper"
---

# Kernel design for isolation and assurance of physical memory

## Reference

Dhammika Elkaduwe, Philip Derrin, and Kevin Elphinstone. “Kernel Design
for Isolation and Assurance of Physical Memory.” In *Proceedings of the 1st
Workshop on Isolation and Integration in Embedded Systems (IIES '08)*,
35–40. Glasgow, United Kingdom, April 1, 2008. DOI
[10.1145/1435458.1435465](https://doi.org/10.1145/1435458.1435465).
[Open author PDF](https://trustworthy.systems/publications/nicta_full_text/848.pdf).

## Research question or contribution

How can a minimal kernel provide a precise, analysable bound on all physical
memory a component may consume, including memory consumed indirectly as kernel
metadata, while leaving allocation policy outside the kernel?

## Method

The authors design a capability-mediated kernel-memory model, formalise the
associated protection model in Isabelle/HOL, and report a machine-checked
isolation result for valid initial configurations. They implement the model in
the experimental ARM11 seL4::Pistachio kernel, run a paravirtualised Linux 2.6
system called Wombat, and compare lmbench results with L4/Iguana on a 532 MHz
ARM1136 system with 128 MiB of RAM.

## Findings

- A memory bound must include both frames directly assigned to a component and
  kernel bookkeeping allocated on its behalf. Quotas over only user-visible
  pages leave an indirect exhaustion channel.
- The design eliminates implicit kernel metadata allocation. Thread-control
  blocks, page tables, capability storage, and their bookkeeping become
  explicit first-class kernel objects.
- An untyped-memory capability names a power-of-two-sized, aligned physical
  region and authorises retyping it into non-overlapping child objects,
  including smaller untyped regions. The untyped authority therefore bounds
  both direct and indirect memory consumption.
- Capability derivation records support delegation and recursive revocation.
  Memory cannot be safely reused until revocation establishes that the untyped
  ancestor has no remaining children; the potentially long operation is
  preemptible.
- The proved physical-isolation configuration forbids cross-domain sharing of
  writable page tables and capability nodes, grant-capable IPC across the
  boundary, and cross-domain authority over thread-control blocks.
- Decentralised object allocation removed an Iguana mediation round trip and
  improved allocation-sensitive benchmarks. Other benchmark differences were
  smaller and partly reflected different exception-IPC implementations.

## Relevance

The project should make memory for every kernel object explicit, caller-funded,
and capability-authorised. A supervisor can receive an untyped-memory subtree,
delegate bounded subtrees to runtime domains or user-space services, and revoke
the subtree during teardown without trusting the failed component to
cooperate. Capability transfer must be distinct from ordinary message transfer:
an endpoint that carries data but cannot grant authority is a stronger failure
boundary. Reclamation should be resumable and budgeted so a large revocation
cannot monopolise the kernel. BEAM heaps and tracing collection remain
user-level runtime concerns; only the frames and kernel objects backing their
domains cross this privileged contract.

## Limits

The assurance claim covers physical-memory isolation, not complete functional
correctness, temporal isolation, device DMA, confidentiality, or every kernel
resource. The design assumes an MMU and the evaluation uses an early seL4
prototype, historical ARM11 hardware, and a paravirtualised Linux workload.
The authors explicitly note that the exception-IPC comparison favours
seL4::Pistachio's hand-optimised assembly path over L4's C path. Capability
revocation can be long-running, and power-of-two objects introduce internal
fragmentation and allocator-policy questions that the paper does not resolve
for this project's workload.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
