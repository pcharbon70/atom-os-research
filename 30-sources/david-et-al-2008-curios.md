---
title: "CuriOS: Improving reliability through operating system structure"
kind: source
created: "2026-08-31"
authors:
  - "Francis M. David"
  - "Ellick M. Chan"
  - "Jeffrey C. Carlyle"
  - "Roy H. Campbell"
published: 2008
citation_key: "david-et-al-2008-curios"
container: "8th USENIX Symposium on Operating Systems Design and Implementation"
edition: null
isbn: "978-1-931971-65-2"
doi: null
url: "https://www.usenix.org/conference/osdi-08/curios-improving-reliability-through-operating-system-structure"
accessed: "2026-08-31"
tags:
  - fault-containment
  - operating-systems
  - recovery
  - state-management
aliases:
  - "CuriOS"
---

# CuriOS: Improving reliability through operating system structure

## Reference

Francis M. David, Ellick M. Chan, Jeffrey C. Carlyle, and Roy H. Campbell.
“CuriOS: Improving Reliability through Operating System Structure.” *OSDI '08*,
pages 59–72.
[USENIX record and paper](https://www.usenix.org/conference/osdi-08/curios-improving-reliability-through-operating-system-structure).

## Research question or contribution

How can a restarted operating-system service preserve necessary client state
without exposing every client's state to every service fault?

## Method

CuriOS decomposes services into protected objects and stores client-associated
state in separate server-state regions. A service sees a client's region only
while handling that client's request. Fault injection targets timer, scheduler,
network, and filesystem services; the work also measures protected-call cost.

## Findings

- Blind restart loses live client state, while preserving an entire service heap
  can preserve the corruption that caused failure.
- Narrow, externally held, client-associated state limits how much one request
  can corrupt and permits selected internal structures to be reconstructed.
- Reported recovery varied by fault and service. Some “successful system
  recovery” cases still terminated one affected network connection.
- Corrupt arguments and results can propagate across a protected boundary even
  when address spaces are isolated.

## Relevance

Restartable services need versioned, validated state outside their executable
domain. A replacement must not inherit the old capability space or arbitrary
heap. Recovery state itself has ownership, visibility, and validation rules;
the kernel only supplies isolation and mapping authority.

## Limits

The prototype used selected services, QEMU and an OMAP1610-era platform, and
hundreds of single-fault injections per service. It did not target malicious
components, some faults escaped detection, and the protected-call and memory
costs are historical. External side effects remain outside its recovery proof.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
