---
title: "Memoir: Practical state continuity for protected modules"
kind: source
created: "2026-09-05"
authors:
  - "Bryan Parno"
  - "Jacob R. Lorch"
  - "John R. Douceur"
  - "James Mickens"
  - "Jonathan M. McCune"
published: 2011
citation_key: "parno-et-al-2011-memoir"
container: "2011 IEEE Symposium on Security and Privacy"
edition: null
isbn: null
doi: "10.1109/SP.2011.38"
url: "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/memoir.pdf"
accessed: "2026-09-05"
tags:
  - persistent-state
  - replay-protection
  - security
aliases:
  - "Memoir state continuity"
---

# Memoir: Practical state continuity for protected modules

## Reference

Bryan Parno, Jacob R. Lorch, John R. Douceur, James Mickens, and Jonathan M.
McCune. “Memoir: Practical State Continuity for Protected Modules.” *2011 IEEE
Symposium on Security and Privacy*, 2011. [Author-hosted
paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/memoir.pdf).
DOI [10.1109/SP.2011.38](https://doi.org/10.1109/SP.2011.38).

## Research question or contribution

How can a protected module detect rollback to an old but cryptographically
valid state when ordinary storage is controlled by an adversary?

## Method

Memoir combines protected execution, sealed state, a concise request-history
construction, and a small amount of trusted nonvolatile state. The protocol is
modeled in TLA+ and evaluated with TPM-backed storage constraints.

## Findings

- Integrity authentication alone does not establish freshness: an adversary
  can replay a previously valid state unless continuity is anchored elsewhere.
- A small trusted nonvolatile value can bind a much larger untrusted snapshot
  to the current request history and detect rollback.
- Crash windows between updating the trusted anchor and external state require
  explicit protocol states and recovery logic.
- Trusted NVRAM is slow, capacity-limited, and wear-sensitive, so the protocol
  minimizes writes rather than treating it as ordinary storage.
- Security depends on the protected module, platform root, key lifecycle, and
  exact reset/adversary assumptions.

## Relevance

A crash record can be encrypted and authenticated yet still be stale. Atom's
sink metadata should separate `integrity`, `confidentiality`, and `freshness`.
If a platform monotonic anchor is unavailable or unsafe in fatal context, the
record must say `freshness = unverified` and rely on boot generation plus later
correlation rather than overclaim rollback resistance.

## Limits

Memoir protects modules against software-controlled persistent storage; it is
not a crash logger and does not prove record capture under machine corruption.
Its TPM assumptions and performance do not transfer automatically to every
Atom target.

## Derived work

- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
