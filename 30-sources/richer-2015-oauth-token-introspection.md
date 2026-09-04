---
title: "OAuth 2.0 token introspection"
kind: source
created: "2026-09-04"
authors:
  - "Justin Richer"
published: 2015
citation_key: "richer-2015-oauth-token-introspection"
container: "RFC 7662"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC7662"
url: "https://www.rfc-editor.org/rfc/rfc7662.html"
accessed: "2026-09-04"
tags:
  - oauth
  - revocation
  - token-introspection
aliases:
  - "RFC 7662"
---

# OAuth 2.0 token introspection

## Reference

Justin Richer. “[OAuth 2.0 Token
Introspection](https://www.rfc-editor.org/rfc/rfc7662.html).” RFC 7662,
October 2015. DOI [10.17487/RFC7662](https://doi.org/10.17487/RFC7662).

## Research question or contribution

RFC 7662 defines how an authorized protected resource can ask an authorization
server whether a token is currently active and obtain context needed to use it.

## Method

This is an IETF Standards Track specification. It defines the request and
response and discusses endpoint authorization, privacy, caching, and the local
meaning of active state.

## Findings

- `active` is an authorization-server judgment combining recognition, expiry,
  revocation, and context; it is not a universal token property.
- The introspection endpoint itself requires authorization to prevent token
  scanning and unwanted disclosure.
- Caching improves availability and latency but directly creates a window in
  which revoked state may still be accepted.
- An unknown or undisclosable token returns inactive without exposing why.

## Relevance

For critical remote grants, an Atom enforcement point may require an
authenticated freshness check against a named epoch/watermark. The response
must bind the exact audience and token digest, and cache duration must be part
of the stated revocation exposure rather than an invisible implementation
detail.

## Limits

The RFC leaves active-state semantics and cache policy to the deployment. It
does not solve local capability revocation, offline operation, or effect
atomicity and does not make an introspection service highly available.

## Derived work

- [Revocation and epoch service](../20-notes/authentication-and-authorization-components/revocation-and-epoch-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
