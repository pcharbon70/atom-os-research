---
title: "Meltdown: Reading kernel memory from user space"
kind: source
created: "2026-09-02"
authors:
  - "Moritz Lipp"
  - "Michael Schwarz"
  - "Daniel Gruss"
  - "Thomas Prescher"
  - "Werner Haas"
  - "Anders Fogh"
  - "Jann Horn"
  - "Stefan Mangard"
  - "Paul Kocher"
  - "Daniel Genkin"
  - "Yuval Yarom"
  - "Mike Hamburg"
published: 2018
citation_key: "lipp-et-al-2018-meltdown"
container: "27th USENIX Security Symposium"
edition: null
isbn: "978-1-939133-04-5"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity18/presentation/lipp"
accessed: "2026-09-02"
tags:
  - isolation
  - kernel-memory
  - security
  - speculative-execution
aliases:
  - "Meltdown"
---

# Meltdown: Reading kernel memory from user space

## Reference

Moritz Lipp et al. “Meltdown: Reading Kernel Memory from User Space.” *27th
USENIX Security Symposium*, pages 973–990, 2018.
[USENIX record and open paper](https://www.usenix.org/conference/usenixsecurity18/presentation/lipp).

## Research question or contribution

Can transient out-of-order execution expose supervisor-only mappings to an
unprivileged process despite architectural permission checks?

## Method

The authors construct transient instruction sequences that encode data from
faulting privileged loads into cache state, then recover it through a timing
side channel on affected processors.

## Findings

- The demonstrated attack read kernel and physical-memory mappings from user
  execution on affected machines without exploiting a kernel software bug.
- Merely marking a mapped page supervisor-only did not prevent transient data
  disclosure on the vulnerable implementations.
- The KAISER page-table isolation technique, originally aimed at address-space
  randomization, also impeded the attack by removing most kernel mappings while
  user code executes.
- The results invalidate the assumption that architectural permission checks
  alone describe all confidentiality effects of a privilege transition.

## Relevance

Entry design needs a machine security profile. On affected machines it may
need a minimal user-visible entry trampoline, a page-table switch before
touching secrets, and corresponding return ordering. That mitigation is not a
universal ISA requirement and its cost must be measured separately.

## Limits

Meltdown concerns particular transient-execution behavior and does not show
that every CPU or privilege boundary requires kernel page-table isolation.
KPTI does not address all speculative, cache, predictor, or same-address-space
side channels.

## Derived work

- [Privileged entry, exit, and execution context](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context.md)
