---
title: "OAuth 2.0 demonstrating proof of possession"
kind: source
created: "2026-09-04"
authors:
  - "Daniel Fett"
  - "Brian Campbell"
  - "John Bradley"
  - "Torsten Lodderstedt"
  - "Michael B. Jones"
  - "David Waite"
published: 2023
citation_key: "fett-et-al-2023-dpop"
container: "RFC 9449"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC9449"
url: "https://www.rfc-editor.org/rfc/rfc9449.html"
accessed: "2026-09-04"
tags:
  - oauth
  - proof-of-possession
  - replay-resistance
  - token-security
aliases:
  - "DPoP"
---

# OAuth 2.0 demonstrating proof of possession

## Reference

Daniel Fett, Brian Campbell, John Bradley, Torsten Lodderstedt, Michael B.
Jones, and David Waite. “[OAuth 2.0 Demonstrating Proof of Possession
(DPoP)](https://doi.org/10.17487/RFC9449).” RFC 9449, September 2023.

## Research question or contribution

DPoP defines application-layer proof-of-possession for OAuth tokens by binding
an access token to a client-held public key and requiring a signed proof for a
particular HTTP method, URI, issuance time, and unique identifier.

## Method

This is a normative protocol specification. Proof construction, access-token
binding, nonce and replay handling, validation, and security limitations were
reviewed.

## Findings

- A stolen sender-constrained token is insufficient without the corresponding
  private key and a valid request proof.
- Method, target URI, token hash, issuance time, and unique identifier narrow
  where a proof can be replayed; server nonces can further strengthen freshness.
- Proof verification requires bounded replay-state, clock policy, URI
  canonicalization, algorithm restrictions, and key protection.
- DPoP is neither user authentication nor authorization by itself; the server
  must still validate the token and apply resource policy.

## Relevance

The remote Atom OS gateway should use holder-of-key credentials, mTLS, or a
DPoP-like request binding rather than unrestricted bearer tokens. The validated
proof should be consumed at the gateway and converted to an operation-specific
local grant; it should never be mistaken for a kernel capability or evidence
that the client process is uncompromised.

## Limits

DPoP is HTTP- and OAuth-specific and does not prevent misuse by a process that
can invoke the legitimate key, compromise of the client, authorization-server
errors, phishing of the user, or resource-side time-of-check/time-of-use races.
Replay caches and nonces introduce availability and state-management costs.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
