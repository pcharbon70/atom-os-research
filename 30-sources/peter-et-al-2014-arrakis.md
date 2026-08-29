---
title: "Arrakis: The operating system is the control plane"
kind: source
created: "2026-08-29"
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
accessed: "2026-08-29"
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
kernel remains the control plane that enforces isolation, naming, and resource
limits?

## Method

Arrakis modifies Barrelfish to assign virtualized network and storage
interfaces, configures IOMMU and device filters in the control plane, and
evaluates application latency and throughput on commercial hardware.

## Findings

- Kernel mediation of every I/O operation is not required when hardware queues,
  DMA translation, and filters enforce the same boundary at setup time.
- The reported workloads obtained substantial latency and throughput gains,
  but depended on capable virtualizable devices and application/runtime
  changes.
- Direct access transfers responsibility: queue protocol, buffer ownership,
  revocation, reset, and denial-of-service controls must still be correct.
- A control-plane/data-plane split can preserve a small privileged policy
  surface while allowing high-rate I/O outside the kernel.

## Relevance

The new OS can expose device queues to isolated driver or service domains only
after a capability transaction binds MMIO, interrupts, DMA mappings, queue
memory, quotas, and reset authority. The simple path can remain mediated; the
direct path is an optimization with the same observable ownership contract.

## Limits

Results are workload- and hardware-specific and do not cover malicious device
firmware, all reset races, or constrained systems without an IOMMU and
virtualizable queues.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
