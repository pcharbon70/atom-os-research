---
title: "Protection in operating systems"
kind: source
created: "2026-09-04"
authors:
  - "Michael A. Harrison"
  - "Walter L. Ruzzo"
  - "Jeffrey D. Ullman"
published: 1976
citation_key: "harrison-et-al-1976-protection-in-operating-systems"
container: "Communications of the ACM 19(8), 461–471"
edition: null
isbn: null
doi: "10.1145/360303.360333"
url: "https://doi.org/10.1145/360303.360333"
accessed: "2026-09-04"
tags:
  - access-control
  - decidability
  - formal-models
  - policy
aliases:
  - "HRU safety result"
---

# Protection in operating systems

## Reference

Michael A. Harrison, Walter L. Ruzzo, and Jeffrey D. Ullman. “[Protection in
Operating Systems](https://doi.org/10.1145/360303.360333).” *Communications of
the ACM* 19(8), pages 461–471, August 1976.

## Research question or contribution

The paper formalizes a protection system whose commands can change an access
matrix and asks the safety question: can a subject ever acquire a specified
right to an object?

## Method

The authors define formal command systems, prove decidability for restricted
forms, and show undecidability for the general model under weak assumptions.

## Findings

- A flexible administrative language can make the future leakage of authority
  undecidable in general.
- Useful restricted models have decidable safety questions, so the result is a
  design argument for constraining transitions rather than abandoning analysis.
- Authorization correctness includes the rules that create subjects, objects,
  and rights, not only the evaluator used for one current request.

## Relevance

Atom OS should deliberately restrict its policy and grant language: finite
typed actions, monotonic attenuation, bounded delegation depth, explicit
revocation anchors, no evaluator I/O, and a small set of analyzable authority
transitions. A general scripting language with authority-changing callbacks is
incompatible with the project’s assurance goal.

## Limits

Undecidability in the general HRU model is not evidence that every practical
policy question is undecidable or that capabilities are unsafe. It does not
model cryptographic credentials, user intent, distributed consistency, or
resource exhaustion.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
