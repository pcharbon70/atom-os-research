---
title: "JSON Web Token best current practices"
kind: source
created: "2026-09-04"
authors:
  - "Yaron Sheffer"
  - "Dick Hardt"
  - "Michael B. Jones"
published: 2020
citation_key: "sheffer-et-al-2020-jwt-best-practices"
container: "RFC 8725 / BCP 225"
edition: "Best Current Practice"
isbn: null
doi: "10.17487/RFC8725"
url: "https://www.rfc-editor.org/rfc/rfc8725.html"
accessed: "2026-09-04"
tags:
  - federation
  - jose
  - jwt
  - security
aliases:
  - "RFC 8725"
  - "JWT BCP"
---

# JSON Web Token best current practices

## Reference

Yaron Sheffer, Dick Hardt, and Michael B. Jones. “[JSON Web Token Best Current
Practices](https://www.rfc-editor.org/rfc/rfc8725.html).” RFC 8725 / BCP 225,
February 2020. DOI [10.17487/RFC8725](https://doi.org/10.17487/RFC8725).

## Research question or contribution

The BCP records attacks on JWT implementations and gives minimum validation,
algorithm, typing, issuer/audience, encoding, key, and indirect-input guidance
for safer profiles.

## Method

This is IETF best-current-practice guidance derived from known implementation
and deployment failures. It updates JWT use rather than specifying a complete
authentication or authorization protocol.

## Findings

- Applications must pin acceptable algorithms and verify that the key and
  cryptographic operation use the expected one; an attacker-controlled `alg`
  is not policy.
- Issuer, subject, and audience require application-specific validation.
- Different JWT purposes need explicit types and mutually exclusive validation
  rules to prevent substitution/cross-JWT confusion.
- Untrusted key identifiers and key URLs can cause injection or server-side
  request forgery; remote lookup must be constrained by local configuration.
- JSON encoding, cryptographic-input validation, compression, weak keys, and
  nested protection create additional hazards.

## Relevance

Atom's federation gateway should isolate token types/profiles, allowlist key
sources, pin algorithms, and treat every claim as untrusted until bound to the
configured issuer, audience, subject mapping, proof key, request, and local
policy.

## Limits

This is a point-in-time floor for JWT handling. It does not define OAuth/OIDC
flows, proof of possession, trust-domain relationships, revocation, capability
derivation, or parser confinement.

## Derived work

- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
