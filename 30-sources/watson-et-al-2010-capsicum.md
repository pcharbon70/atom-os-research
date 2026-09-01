---
title: "Capsicum: Practical capabilities for UNIX"
kind: source
created: "2026-08-31"
authors:
  - "Robert N. M. Watson"
  - "Jonathan Anderson"
  - "Ben Laurie"
  - "Kris Kennaway"
published: 2010
citation_key: "watson-et-al-2010-capsicum"
container: "19th USENIX Security Symposium"
edition: null
isbn: "978-1-931971-77-5"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity10/capsicum-practical-capabilities-unix"
accessed: "2026-08-31"
tags:
  - capabilities
  - compartmentalization
  - least-privilege
  - operating-systems
aliases:
  - "Capsicum paper"
---

# Capsicum: Practical capabilities for UNIX

## Reference

Robert N. M. Watson, Jonathan Anderson, Ben Laurie, and Kris Kennaway.
“Capsicum: Practical Capabilities for UNIX.” *19th USENIX Security Symposium*,
pages 29–46, 2010.
[USENIX record and paper](https://www.usenix.org/conference/usenixsecurity10/capsicum-practical-capabilities-unix).

## Research question or contribution

Can capability-oriented application compartmentalization be added to a
conventional UNIX system without replacing its API or kernel architecture?

## Method

Capsicum adds irreversible capability mode, rights-limited file descriptors,
and constrained namespace operations to FreeBSD. The authors adapt command-line
utilities and Chromium, compare sandboxing effort, and measure selected costs.

## Findings

- Entering capability mode removes access to ambient global namespaces while
  preserving already delegated descriptors.
- Descriptor capabilities carry object-specific rights that can be narrowed
  but not broadened. Descriptor-to-object resolution is mediated through the
  kernel's `fget` path, while global pathname lookup is separately mediated
  through `namei` and restricted in capability mode.
- Directory capabilities and relative lookup can delegate a namespace subtree
  without granting the global filesystem namespace.
- Existing applications can be decomposed incrementally, illustrating that
  capability usability and compatibility are part of effective least privilege.

## Relevance

The narrow descriptor-resolution choke point, monotonic rights attenuation,
receiver-visible handles, and absence of ambient post-bootstrap namespaces are
appropriate for the new kernel. Capability use must also be ergonomic enough
that service and runtime authors do not request broad authority as a
workaround.

## Limits

Capsicum is a hybrid extension to UNIX rather than a pure capability
microkernel. Existing descriptors and memory remain available after entering
capability mode, and UNIX process, filesystem, and lifecycle assumptions remain.
Its low overhead does not predict cross-domain IPC or this project's object
model.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
