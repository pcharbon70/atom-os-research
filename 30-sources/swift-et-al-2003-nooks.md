---
title: "Improving the reliability of commodity operating systems"
kind: source
created: "2026-08-31"
authors:
  - "Michael M. Swift"
  - "Brian N. Bershad"
  - "Henry M. Levy"
published: 2003
citation_key: "swift-et-al-2003-nooks"
container: "Proceedings of the 19th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "1-58113-757-5"
doi: "10.1145/945445.945466"
url: "https://nooks.cs.washington.edu/nooks-sosp.pdf"
accessed: "2026-08-31"
tags:
  - device-drivers
  - fault-containment
  - operating-systems
  - recovery
aliases:
  - "Nooks"
---

# Improving the reliability of commodity operating systems

## Reference

Michael M. Swift, Brian N. Bershad, and Henry M. Levy. “Improving the
Reliability of Commodity Operating Systems.” *SOSP '03*, pages 207–222. DOI
[10.1145/945445.945466](https://doi.org/10.1145/945445.945466).
[Project PDF](https://nooks.cs.washington.edu/nooks-sosp.pdf).

## Research question or contribution

Can existing in-kernel extensions be isolated and recovered with minimal source
change, even when full microkernel separation is not adopted?

## Method

Nooks inserts a reliability layer around Linux extensions. Lightweight
protection domains restrict writes, wrappers interpose calls, an object tracker
records resources, and a recovery manager unloads and reloads extensions. The
evaluation includes 2,000 synthetic fault-injection trials across five
extensions on Linux 2.4.18.

## Findings

- Isolation alone was insufficient; interposition and typed resource tracking
  were needed to validate cross-boundary changes and clean up after failure.
- Of 317 injected faults that crashed native Linux, Nooks eliminated 313. This
  is the source of the reported 99% result, not a general reliability rate.
- Recovery effectiveness and cost varied with the extension and call rate.
- Filesystem recovery exposed persistent-state damage even when the kernel
  survived, showing that containment does not restore external invariants.

## Relevance

Every kernel domain needs a typed ledger of owned objects, mappings, calls,
budgets, IRQ routes, and DMA leases. Teardown must invoke type-specific closure
and quiescence rather than merely free memory associated with a numeric domain
ID.

## Limits

Nooks explicitly targets mistakes rather than malicious code. Extensions remain
privileged, infinite loops and semantic errors are incompletely detected, DMA
was not isolated, and only safely restartable extensions were supported. The
fault-injection model and old uniprocessor Linux configuration bound all
reported results.

## Derived work

- [Native work, ports, and drivers](../20-notes/managed-actor-runtime-components/native-work-ports-and-drivers.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
