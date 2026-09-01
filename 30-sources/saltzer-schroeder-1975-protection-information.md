---
title: "The protection of information in computer systems"
kind: source
created: "2026-08-31"
authors:
  - "Jerome H. Saltzer"
  - "Michael D. Schroeder"
published: 1975
citation_key: "saltzer-schroeder-1975-protection-information"
container: "Proceedings of the IEEE 63(9), 1278–1308"
edition: null
isbn: null
doi: "10.1109/PROC.1975.9939"
url: "https://web.mit.edu/Saltzer/www/publications/protection/Basic.html"
accessed: "2026-08-31"
tags:
  - access-control
  - least-privilege
  - operating-systems
  - security
aliases:
  - "Saltzer and Schroeder protection principles"
---

# The protection of information in computer systems

## Reference

Jerome H. Saltzer and Michael D. Schroeder. “The Protection of Information in
Computer Systems.” *Proceedings of the IEEE* 63(9), pages 1278–1308, September
1975. DOI [10.1109/PROC.1975.9939](https://doi.org/10.1109/PROC.1975.9939).
[Author-hosted HTML](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## Research question or contribution

The article systematizes protection objectives, mechanisms, and design
principles for multi-user computer systems. Its enduring contribution is not a
particular access-control representation, but a set of tests for whether a
protection mechanism is likely to remain understandable and effective.

## Method

This is a tutorial synthesis grounded in contemporary protection systems and
known failure patterns, not a controlled security evaluation.

## Findings

- Economy of mechanism argues for small, simple protection mechanisms.
- Fail-safe defaults require permission to be granted explicitly rather than
  inferred from the absence of a prohibition.
- Complete mediation requires authority to be checked on every access path,
  which in turn requires references that cannot bypass the reference monitor.
- Least privilege and least common mechanism reduce both the damage available
  to a fault and the amount of shared state through which faults can spread.
- Separation of privilege supports splitting unusually powerful operations
  across independent authorities.
- Psychological acceptability matters because an unusable protection model is
  routinely bypassed or misconfigured.

## Relevance

These principles become concrete kernel invariants: no ambient post-bootstrap
authority, operation-specific capability rights, explicit recovery and debug
authority, bounded kernel mechanisms, and denial by default. They also warn
against an omnipotent supervisor capability when observation, suspension,
revocation, device reset, replacement creation, and publication can be
separated.

## Limits

The paper predates modern multicore systems, IOMMUs, speculative side channels,
and current capability kernels. The principles identify design pressure; they
do not select a data structure, prove complete mediation, or establish that a
small interface is usable.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
