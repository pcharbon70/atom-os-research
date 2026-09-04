---
title: "Argon2 memory-hard function for password hashing"
kind: source
created: "2026-09-04"
authors:
  - "Alex Biryukov"
  - "Daniel Dinu"
  - "Dmitry Khovratovich"
  - "Simon Josefsson"
published: 2021
citation_key: "biryukov-et-al-2021-argon2"
container: "RFC 9106"
edition: "Informational"
isbn: null
doi: "10.17487/RFC9106"
url: "https://www.rfc-editor.org/rfc/rfc9106.html"
accessed: "2026-09-04"
tags:
  - authentication
  - cryptography
  - password-hashing
aliases:
  - "RFC 9106"
---

# Argon2 memory-hard function for password hashing

## Reference

Alex Biryukov, Daniel Dinu, Dmitry Khovratovich, and Simon Josefsson.
“[Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work
Applications](https://www.rfc-editor.org/rfc/rfc9106.html).” RFC 9106,
September 2021. DOI [10.17487/RFC9106](https://doi.org/10.17487/RFC9106).

## Research question or contribution

RFC 9106 gives an implementer-oriented description of Argon2 version 1.3,
including parameter guidance and test vectors, so password hashing can impose
substantial memory as well as computation cost on guessing attacks.

## Method

This CFRG consensus document specifies Argon2d, Argon2i, and Argon2id and
provides test vectors. It summarizes security trade-offs from the underlying
Argon2 research; it is not an evaluation of an OS authentication service.

## Findings

- Argon2id combines data-independent and data-dependent memory access and is
  the mandatory-to-implement variant in the RFC.
- Security depends on salt uniqueness, parameter selection, implementation
  correctness, and sufficient memory/time cost for the deployment.
- The chosen memory and time cost is also paid by the verifier for every
  password attempt.
- Password hashing slows offline guessing but does not provide phishing
  resistance, proof of possession for later requests, or secure recovery.

## Relevance

Passwords should be an explicit compatibility profile in Atom's authentication
verifier, not the root architecture. The verifier should store a versioned
algorithm-and-parameter record, run hashing in a budgeted worker pool, rate
limit and admission-control expensive work where safe, bound concurrency, and
rehash only after successful verification under an authenticated transition.

## Limits

RFC 9106 is informational and assumes a trustworthy implementation and
parameter policy. It does not define credential enrollment, breach detection,
online throttling, secure input, sessions, or authorization.

## Derived work

- [Authentication verifier](../20-notes/authentication-and-authorization-components/authentication-verifier.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
