---
title: "On micro-kernel construction"
kind: source
created: "2026-08-31"
authors:
  - "Jochen Liedtke"
published: 1995
citation_key: "liedtke-1995-microkernel-construction"
container: "Proceedings of the 15th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "0-89791-715-4"
doi: "10.1145/224056.224075"
url: "https://os.itec.kit.edu/deutsch/1030.php"
accessed: "2026-08-31"
tags:
  - ipc
  - microkernels
  - operating-systems
  - protection-domains
aliases:
  - "On μ-kernel construction"
---

# On micro-kernel construction

## Reference

Jochen Liedtke. “On Micro-Kernel Construction.” *SOSP '95*, pages 237–250,
1995. DOI [10.1145/224056.224075](https://doi.org/10.1145/224056.224075).
[Open PDF](https://os.itec.kit.edu/deutsch/1030.php).

## Research question or contribution

Which mechanisms are functionally unavoidable in a protected microkernel, and
which performance and implementation choices caused earlier microkernels to be
slow or inflexible?

## Method

The paper derives primitives from isolation and communication requirements,
then analyzes L3/L4 implementation paths and historical measurements.

## Findings

- A mechanism belongs in the kernel only when moving it out would make a
  required system property impossible, not merely slower or less convenient.
- Address-space protection, threads, protected communication, and a minimal
  way to establish identity are presented as foundational mechanisms; paging,
  memory-management policy, naming, and higher abstractions can remain above.
- The independence requirement says one subsystem must be able to make
  guarantees without another subsystem corrupting it. Integrity additionally
  requires a protected communication path whose endpoints cannot be silently
  substituted or observed by an unrelated subsystem.
- Fast IPC depends on small working sets, careful fast paths, and architecture-
  aware implementation. A microkernel can improve whole-system portability
  while remaining processor-dependent itself.

## Relevance

The inclusion test is the right standard for this project's privileged layer.
Protected domains, capability-checked invocation, address-space transitions,
and bounded scheduling enforcement qualify; BEAM mailboxes, OTP restart
strategy, service names, storage, drivers, and policy do not.

## Limits

The evaluated processors and absolute timings are historical. The paper does
not provide a modern capability model, multicore revocation protocol, DMA
containment, temporal budgets, or recovery semantics. Its primitives are a
minimality argument, not a complete design for this platform.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
