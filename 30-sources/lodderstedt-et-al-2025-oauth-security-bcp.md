---
title: "Best current practice for OAuth 2.0 security"
kind: source
created: "2026-09-04"
authors:
  - "Torsten Lodderstedt"
  - "John Bradley"
  - "Andrey Labunets"
  - "Daniel Fett"
published: 2025
citation_key: "lodderstedt-et-al-2025-oauth-security-bcp"
container: "RFC 9700; BCP 240"
edition: "Best Current Practice"
isbn: null
doi: "10.17487/RFC9700"
url: "https://www.rfc-editor.org/rfc/rfc9700.html"
accessed: "2026-09-04"
tags:
  - authorization
  - oauth
  - protocol-security
  - token-security
aliases:
  - "OAuth 2.0 Security BCP"
---

# Best current practice for OAuth 2.0 security

## Reference

Torsten Lodderstedt, John Bradley, Andrey Labunets, and Daniel Fett. “[Best
Current Practice for OAuth 2.0 Security](https://doi.org/10.17487/RFC9700).”
RFC 9700, BCP 240, January 2025.

## Research question or contribution

The BCP updates OAuth 2.0’s attacker model and operational guidance from years
of deployment, deprecating unsafe flows and addressing code interception,
mix-up, redirect, token injection, leakage, and replay.

## Method

This is an IETF consensus Best Current Practice. The attacker model and
recommendations for authorization-code flows, PKCE, exact redirect validation,
metadata, asymmetric client authentication, audience restriction, TLS, and
sender-constrained tokens were reviewed.

## Findings

- Authorization servers must support PKCE and prevent downgrade; the implicit
  and resource-owner-password flows are no longer safe baseline choices.
- Redirect URI matching, issuer binding, and explicit client identity are
  necessary to prevent authorization response and mix-up attacks.
- Access tokens should be audience-restricted and sender-constrained with
  mutual TLS or DPoP so theft is less readily replayed.
- Tokens must not travel in URLs, and asymmetric client authentication avoids a
  shared client secret at the authorization server where feasible.

## Relevance

OAuth may be useful at Atom OS web/federation gateways, never as the local
kernel authority model. A gateway must terminate and validate the complete
protocol, bind the result to its issuer, audience, client key, session, request,
and policy revision, then mint a shorter-lived local capability. Raw access or
refresh tokens must not enter actor messages, logs, command history, or kernel
capability tables.

## Limits

The BCP assumes the OAuth ecosystem and does not provide OS login, local
process attribution, secure attention, application policy, capability
revocation, or a trusted UI. Correct conformance still depends on transport,
browser, client, authorization-server, and resource-server implementations.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
