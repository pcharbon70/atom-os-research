---
title: "Practical dynamic software updating for C"
kind: source
created: "2026-09-03"
authors:
  - "Iulian Neamtiu"
  - "Michael Hicks"
  - "Gareth Stoyle"
  - "Manuel Oriol"
published: 2006
citation_key: "neamtiu-et-al-2006-practical-dynamic-software-updating"
container: "Proceedings of the 2006 ACM SIGPLAN Conference on Programming Language Design and Implementation"
edition: "PLDI '06, 72–83"
isbn: "1-59593-320-4"
doi: "10.1145/1133981.1133991"
url: "https://mhicks.me/papers/ginseng.pdf"
accessed: "2026-09-03"
tags:
  - dynamic-software-updating
  - release-management
  - state-migration
aliases:
  - "Ginseng"
---

# Practical dynamic software updating for C

## Reference

Iulian Neamtiu, Michael Hicks, Gareth Stoyle, and Manuel Oriol. “[Practical
Dynamic Software Updating for C](https://mhicks.me/papers/ginseng.pdf).”
*PLDI '06*, pages 72–83. DOI
[10.1145/1133981.1133991](https://doi.org/10.1145/1133981.1133991).

## Research question or contribution

Can a compiler, patch generator, and small runtime make substantial,
representation-changing updates to long-running C servers while preserving
type safety and application state?

## Method

Ginseng adds function indirection, type wrappers, state transformers, update
points, and static analyses. The authors applied real release changes spanning
about three years to single-threaded versions of vsftpd, OpenSSH `sshd`, and
GNU Zebra, then measured update latency and steady-state overhead.

## Findings

- Code replacement alone is not a complete update protocol: changed function
  interfaces and data representations require compatibility constraints and
  explicit state transformation.
- Safe update timing depends on assumptions in the continuation at an update
  point. Analyses can rule out some unsafe times, but programmers still need a
  whole-system view of component interactions and invariants.
- The evaluated patches applied in under 5 ms; measured throughput overhead
  ranged from zero to 32 percent across the selected servers and workloads.
- Quiescence and redirection are viable alternatives to changing active state
  in place. Both still need an explicit decision about in-flight work.

## Relevance

Atom OS release orchestration should model compatibility, quiescence, state
migration, publication, and rollback as separate stages. BEAM hot code loading
reduces some code-redirection work but does not solve durable schema changes,
multi-service protocol skew, irreversible effects, or distributed rollout.

## Limits

The evaluated programs were single-threaded C servers, not BEAM supervision
trees, distributed clusters, kernels, or storage engines. Type safety is
narrower than application correctness, and the reported performance ranges
cannot be projected to Atom OS. The work does not provide signed supply-chain
verification, crash-safe rollout, or automatic rollback across irreversible
state changes.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
