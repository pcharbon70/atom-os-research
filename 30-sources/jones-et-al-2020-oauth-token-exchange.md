---
title: "OAuth 2.0 token exchange"
kind: source
created: "2026-09-04"
authors:
  - "Michael B. Jones"
  - "Anthony Nadalin"
  - "Brian Campbell"
  - "John Bradley"
  - "Chuck Mortimore"
published: 2020
citation_key: "jones-et-al-2020-oauth-token-exchange"
container: "RFC 8693"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC8693"
url: "https://www.rfc-editor.org/rfc/rfc8693.html"
accessed: "2026-09-04"
tags:
  - delegation
  - federation
  - oauth
  - token-exchange
aliases:
  - "RFC 8693"
---

# OAuth 2.0 token exchange

## Reference

Michael B. Jones, Anthony Nadalin, Brian Campbell, John Bradley, and Chuck
Mortimore. “[OAuth 2.0 Token
Exchange](https://www.rfc-editor.org/rfc/rfc8693.html).” RFC 8693, January
2020. DOI [10.17487/RFC8693](https://doi.org/10.17487/RFC8693).

## Research question or contribution

RFC 8693 defines a Security Token Service-style OAuth extension for exchanging
one security token for another and representing subject and actor relationships
for delegation and impersonation scenarios.

## Method

This is an IETF Standards Track protocol specification. It defines request and
response parameters, token type identifiers, subject and actor token roles,
and claim structures while deliberately leaving token syntax and deployment
trust relationships to profiles.

## Findings

- The subject of a token and the actor exercising it are different facts;
  nested actor information can preserve a delegation chain.
- Delegation and impersonation have different audit and policy meaning even if
  both result in a new token.
- Requested resource, audience, and scope constrain an exchange but do not by
  themselves prove that the issued token is least-privileged.
- The protocol does not define the security properties of token types, proof of
  possession, or the federation's trust model.

## Relevance

Atom should preserve separate subject, actor, issuer, audience, and bounded
delegation provenance at the federation gateway. Exchange terminates in a new
local policy decision and capability derivation inside a preconfigured issuer
envelope; it is never byte-for-byte conversion of external claims into kernel
authority. Atom must impose a finite chain depth even though RFC 8693 does not.

## Limits

RFC 8693 provides protocol vocabulary, not a complete authorization system.
Unsafe profiles can amplify scope, erase actor provenance, accept bearer replay,
or create delegation loops while remaining syntactically conformant.

## Derived work

- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)
- [Grant compiler and issuer](../20-notes/authentication-and-authorization-components/grant-compiler-and-issuer.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
