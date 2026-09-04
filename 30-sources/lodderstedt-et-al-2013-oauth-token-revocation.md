---
title: "OAuth 2.0 token revocation"
kind: source
created: "2026-09-04"
authors:
  - "Torsten Lodderstedt"
  - "Stephen Dronia"
  - "Marius Scurtescu"
published: 2013
citation_key: "lodderstedt-et-al-2013-oauth-token-revocation"
container: "RFC 7009"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC7009"
url: "https://www.rfc-editor.org/rfc/rfc7009.html"
accessed: "2026-09-04"
tags:
  - oauth
  - revocation
  - security
aliases:
  - "RFC 7009"
---

# OAuth 2.0 token revocation

## Reference

Torsten Lodderstedt, editor, Stephen Dronia, and Marius Scurtescu. “[OAuth 2.0 Token
Revocation](https://www.rfc-editor.org/rfc/rfc7009.html).” RFC 7009, August
2013. DOI [10.17487/RFC7009](https://doi.org/10.17487/RFC7009).

## Research question or contribution

RFC 7009 defines a client-facing endpoint for invalidating OAuth access or
refresh tokens and discusses related-token invalidation and propagation.

## Method

This is an IETF Standards Track protocol specification. The analysis used its
failure, propagation, and token-type trade-offs as distributed-revocation
evidence, not as an Atom wire-protocol choice.

## Findings

- An authorization server may revoke related tokens and the grant from which a
  token was derived, so lineage is part of revocation semantics.
- Distributed systems can have a propagation delay between revocation and
  enforcement; short-lived access tokens bound the exposure when immediate
  propagation is unavailable.
- A service-unavailable response does not mean revocation succeeded; the client
  must assume the token may remain usable.
- Reference tokens enable online state checks while self-contained tokens trade
  that immediacy for local validation and bounded lifetime.

## Relevance

Atom should expose separate committed, distributed, enforced, quiesced, and
sanitized revocation stages and measure the maximum use window. It must never
report a network request as completed revocation before local enforcement
points have advanced to the required watermark.

## Limits

The RFC concerns OAuth tokens and intentionally permits deployment-specific
propagation. It does not define capability-tree traversal, durable epochs,
in-flight effect cancellation, offline authority, or byzantine faults.

## Derived work

- [Revocation and epoch service](../20-notes/authentication-and-authorization-components/revocation-and-epoch-service.md)
- [Session service](../20-notes/authentication-and-authorization-components/session-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
