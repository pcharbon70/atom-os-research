---
title: "Exokernel: An operating system architecture for application-level resource management"
kind: source
created: "2026-08-30"
authors:
  - "Dawson R. Engler"
  - "M. Frans Kaashoek"
  - "James O'Toole Jr."
published: 1995
citation_key: "engler-et-al-1995-exokernel"
container: "Proceedings of the 15th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "0-89791-715-4"
doi: "10.1145/224056.224076"
url: "https://pdos.csail.mit.edu/6.828/2008/readings/engler95exokernel.pdf"
accessed: "2026-08-30"
tags:
  - exokernels
  - operating-systems
  - policy-mechanism-separation
  - protection
  - resource-management
aliases:
  - "Exokernel"
---

# Exokernel: An operating system architecture for application-level resource management

## Reference

Dawson R. Engler, M. Frans Kaashoek, and James O'Toole Jr. “Exokernel: An
Operating System Architecture for Application-Level Resource Management.”
*SOSP '95*, pages 251–266, 1995. DOI
[10.1145/224056.224076](https://doi.org/10.1145/224056.224076).
[Author-hosted copy](https://pdos.csail.mit.edu/6.828/2008/readings/engler95exokernel.pdf).

## Research question or contribution

Can a small kernel securely expose low-level resources while moving most
resource-management abstractions and policy into untrusted library operating
systems?

## Method

The paper defines secure bindings, visible revocation, and abort protocols,
implements them in Aegis with the ExOS library, and evaluates low-level kernel
operations and application-specific virtual-memory and IPC paths.

## Findings

- Protection can be separated from management, but the kernel still has to
  track ownership, guard binding or use points, arbitrate allocation, and
  revoke uncooperative clients.
- A low-level interface can expose exceptions, address-translation resources,
  privileged operations, and device capabilities without granting arbitrary
  authority. Each operation remains checked against resource ownership.
- Visible revocation lets a cooperative client choose how to relinquish a
  resource; a forced abort path is still required for failure or hostility.
- The prototype's performance results demonstrate feasibility on its hardware,
  not a timeless guarantee. Its physical-resource naming and application-level
  policy also trade portability and simplicity for control.

## Relevance

The hardware layer should not absorb scheduler, pager, driver, or runtime
policy merely because it controls the corresponding mechanism. It should expose
capability-checked bindings and explicit revocation protocols. Every delegated
page-table, interrupt, timer, or DMA facility needs a forceful recovery path;
cooperative release alone is not a protection boundary.

## Limits

The work predates current multicore, IOMMU, speculative-execution, and device
queue designs. Its prototype exported unusually low-level resources and does
not prove that every such detail should be public in this kernel.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
