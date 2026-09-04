---
title: "OAuth 2.0 mutual-TLS client authentication and certificate-bound access tokens"
kind: source
created: "2026-09-04"
authors:
  - "Brian Campbell"
  - "John Bradley"
  - "Nat Sakimura"
  - "Torsten Lodderstedt"
published: 2020
citation_key: "campbell-et-al-2020-oauth-mutual-tls"
container: "RFC 8705"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC8705"
url: "https://www.rfc-editor.org/rfc/rfc8705.html"
accessed: "2026-09-04"
tags:
  - federation
  - mutual-tls
  - oauth
  - proof-of-possession
aliases:
  - "RFC 8705"
---

# OAuth 2.0 mutual-TLS client authentication and certificate-bound access tokens

## Reference

Brian Campbell, John Bradley, Nat Sakimura, and Torsten Lodderstedt. “[OAuth
2.0 Mutual-TLS Client Authentication and Certificate-Bound Access
Tokens](https://www.rfc-editor.org/rfc/rfc8705.html).” RFC 8705, February
2020. DOI [10.17487/RFC8705](https://doi.org/10.17487/RFC8705).

## Research question or contribution

RFC 8705 defines mutual-TLS client authentication for OAuth endpoints and a
method for binding access and refresh tokens to the certificate whose private
key the client proves it holds.

## Method

This is an IETF Standards Track protocol specification. It defines PKI and
self-signed certificate authentication profiles, confirmation data, resource-
server validation, metadata, and security considerations.

## Findings

- Client authentication at the authorization server and proof-of-possession
  binding at the resource server are distinct but complementary mechanisms.
- A resource server must obtain the certificate from the actual TLS layer and
  compare it with the token binding; a claim supplied by an untrusted proxy is
  not equivalent.
- `client_id` must be bound to the expected certificate or subject, not inferred
  merely from a successful TLS handshake.
- X.509 parsing, chain validation, rotation, expiry, revocation, and TLS
  termination introduce deployment-specific trust boundaries.

## Relevance

Atom's federation gateway may accept certificate-bound external tokens or use
mutual TLS between gateways, but it should terminate the protocol and derive a
new local, audience- and operation-bound grant. The local resource must never
trust network location or a serialized kernel handle.

## Limits

The RFC does not define application authorization policy, token-exchange trust,
gateway confinement, certificate-revocation policy, or Atom's capability
semantics. Certificate-bound tokens limit token replay; they do not make a
compromised client trustworthy.

## Derived work

- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)
- [Grant compiler and issuer](../20-notes/authentication-and-authorization-components/grant-compiler-and-issuer.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
