---
title: "Vulnerabilities in synchronous IPC designs"
kind: source
created: "2026-08-31"
authors:
  - "Jonathan S. Shapiro"
published: 2003
citation_key: "shapiro-2003-synchronous-ipc-vulnerabilities"
container: "Proceedings of the 2003 IEEE Symposium on Security and Privacy"
edition: null
isbn: null
doi: "10.1109/SECPRI.2003.1199341"
url: "https://doi.org/10.1109/SECPRI.2003.1199341"
accessed: "2026-08-31"
tags:
  - capabilities
  - denial-of-service
  - interprocess-communication
  - microkernels
  - operating-systems
aliases:
  - "Synchronous IPC vulnerabilities paper"
---

# Vulnerabilities in synchronous IPC designs

## Reference

Jonathan S. Shapiro. “Vulnerabilities in Synchronous IPC Designs.” In
*Proceedings of the 2003 IEEE Symposium on Security and Privacy*, 251–262,
2003. DOI
[10.1109/SECPRI.2003.1199341](https://doi.org/10.1109/SECPRI.2003.1199341).

## Research question or contribution

Can thread-migrating synchronous IPC retain its performance while supporting
asymmetric trust, reproducible behaviour, and dynamically sized payloads
without allowing one party to pin another or exhaust global resources?

## Method

Shapiro performs an adversarial architectural analysis of documented L4 and
EROS IPC semantics. The paper follows blocking, page-fault, buffering,
multithreading, truncation, and timeout cases across sender and receiver trust
boundaries, then proposes the next-generation EROS trusted buffer object as a
general solution for large replies.

## Findings

- Synchronous IPC is not safe merely because the kernel transfer is fast and
  atomic. Sender blocking, user-level paging, and dynamically sized strings
  create authority and resource-accounting questions across asymmetric trust
  boundaries.
- An unprotected recipient name lets arbitrary senders flood a service.
  Assigning a server thread per client consumes more resources and moves the
  attack into thread and scheduling state rather than eliminating it.
- A hostile client can make a replying server block by failing to receive or by
  arranging a non-returning page fault during string transfer. Kernel buffering
  can instead turn the local problem into system-wide kernel-memory exhaustion.
- IPC timeouts do not supply a principled general bound when workload and
  queueing behaviour are unknown. They undermine reproducibility and can let a
  few clients repeatedly occupy a shared server until each timeout expires.
- A safe response should be prompt: an untrusted party must not be able to
  prevent its completion. For an unbounded reply, the proposed trusted buffer
  object executes trusted code while charging storage to the client, so the
  server need not donate its own or kernel memory.
- The paper's design objectives are to put the cost of defection on the
  defecting client and to avoid converting a local loss of service into a
  global one.

## Relevance

The project's privileged IPC contract should use protected endpoint authority,
small bounded control messages, and explicit caller-funded resources. A reply
or donated scheduling context needs a kernel-enforced cancellation and return
path if either side fails. Large BEAM payloads should use bounded shared-memory
or buffer objects managed above the kernel, with ownership and charging made
explicit; they should not make the kernel fault through arbitrary user pages or
allocate an unbounded queue. Budget exhaustion is a deterministic resource
event for a supervisor to handle, not a generic wall-clock IPC timeout whose
meaning changes with system load.

## Limits

The work analyses 2003-era L4 and EROS designs and proposes EROS-specific
mechanisms; it is not a formal proof or a broad workload evaluation. A trusted
buffer object depends on trustworthy construction, authentication, storage
accounting, and prompt execution support. Its critique of arbitrary IPC
timeouts does not imply that explicit scheduling budgets or externally
specified device deadlines are unsound. The project still needs to define how
cancellation, donated time, reply authority, and partial bulk-transfer state
compose under multicore execution.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
