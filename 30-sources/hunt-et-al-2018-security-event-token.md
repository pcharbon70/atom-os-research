---
title: "Security Event Token (SET)"
kind: source
created: "2026-09-04"
authors:
  - "Phil Hunt"
  - "Michael B. Jones"
  - "William Denniss"
  - "Morteza Ansari"
published: 2018
citation_key: "hunt-et-al-2018-security-event-token"
container: "RFC 8417"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC8417"
url: "https://www.rfc-editor.org/rfc/rfc8417.html"
accessed: "2026-09-04"
tags:
  - eventing
  - federation
  - revocation
  - security
aliases:
  - "RFC 8417"
  - "SET"
---

# Security Event Token (SET)

## Reference

Phil Hunt, editor, Michael B. Jones, William Denniss, and Morteza Ansari. “[Security
Event Token](https://www.rfc-editor.org/rfc/rfc8417.html).” RFC 8417, July
2018. DOI [10.17487/RFC8417](https://doi.org/10.17487/RFC8417).

## Research question or contribution

RFC 8417 defines a signed and optionally encrypted container for statements
about security events exchanged between cooperating systems.

## Method

This is an IETF Standards Track token-format specification. It defines event
claims, issuer/audience/time identifiers, subject representation, and security
and privacy considerations but delegates delivery reliability and event-
specific semantics to profiles.

## Findings

- A security event is an issuer's statement of fact, not an executable command;
  the receiver applies its own validation and policy.
- Asynchronous receipt may occur before or after related business processing,
  so timestamps alone cannot establish causal or total order.
- Event identifiers support deduplication, while issuer and audience binding
  prevent accepting a structurally valid statement from the wrong authority.
- Sensitive event content and correlation identifiers create privacy risks.

## Relevance

Atom's revocation service should deliver authenticated, sequence-bearing facts
that receivers validate and apply idempotently, then acknowledge with
watermarks. Gaps require snapshot recovery; a signed event must never invoke
authority merely because it arrived.

## Limits

The base RFC does not define reliable delivery, ordering, replay stores,
revocation semantics, convergence, or service-level bounds. JWT security still
depends on profiles, algorithms, key distribution, and parser correctness.

## Derived work

- [Revocation and epoch service](../20-notes/authentication-and-authorization-components/revocation-and-epoch-service.md)
- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
