---
title: "Arrakis: The operating system is the control plane"
kind: source
created: "2026-08-30"
authors:
  - "Simon Peter"
  - "Jialin Li"
  - "Irene Zhang"
  - "Dan R. K. Ports"
  - "Doug Woos"
  - "Arvind Krishnamurthy"
  - "Thomas Anderson"
  - "Timothy Roscoe"
published: 2014
citation_key: "peter-et-al-2014-arrakis"
container: "11th USENIX Symposium on Operating Systems Design and Implementation"
edition: null
isbn: "978-1-931971-16-4"
doi: null
url: "https://www.usenix.org/conference/osdi14/technical-sessions/presentation/peter"
accessed: "2026-08-30"
tags:
  - dma
  - io
  - iommu
  - operating-systems
  - virtualization
aliases:
  - "Arrakis control plane"
---

# Arrakis: The operating system is the control plane

## Reference

Simon Peter et al. “Arrakis: The Operating System Is the Control Plane.” *11th
USENIX Symposium on Operating Systems Design and Implementation*, pages 1–16,
2014. [USENIX paper and metadata](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/peter).

## Research question or contribution

Can applications obtain direct data-plane access to virtualized I/O while the
kernel remains the control plane enforcing isolation, naming, and resource
limits?

## Method

Arrakis modifies Barrelfish to assign virtualized network and storage
interfaces, configures IOMMU and device filters in the control plane, and
evaluates application latency and throughput on commercial hardware.

## Findings

- Kernel mediation of every I/O operation is not required when hardware queues,
  DMA translation, and filters enforce the boundary established by the kernel.
- The paper reports two-to-five-fold latency improvement and ninefold throughput
  improvement for a selected persistent NoSQL workload relative to its tuned
  Linux baseline; those numbers are workload and hardware specific.
- Direct access transfers responsibility rather than removing it: queue
  protocol, buffer ownership, revocation, reset, naming, and denial-of-service
  controls must remain correct.
- A control-plane/data-plane split can keep policy changes and slow resource
  reconfiguration privileged while moving high-rate queue operations out of
  the kernel.

## Relevance

The protected-I/O component should provide a mediated baseline and an optional
delegated queue path with the same ownership contract. Delegation must bind a
DMA domain, queue memory, interrupts, MMIO subset, quotas, and reset authority
as one revocable transaction.

## Limits

Arrakis depends on virtualizable I/O hardware and modified applications or
libraries. Its evaluation does not cover every device, malicious firmware,
all reset races, or systems without suitable IOMMU and queue facilities.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
