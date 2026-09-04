---
title: "Web Authentication: an API for accessing public key credentials — Level 3"
kind: source
created: "2026-09-04"
authors:
  - "W3C Web Authentication Working Group"
published: 2026
citation_key: "w3c-2026-webauthn-level-3"
container: "W3C Recommendation"
edition: "25 August 2026"
isbn: null
doi: null
url: "https://www.w3.org/TR/webauthn-3/"
accessed: "2026-09-04"
tags:
  - authentication
  - passkeys
  - phishing-resistance
  - webauthn
aliases:
  - "WebAuthn Level 3"
---

# Web Authentication: an API for accessing public key credentials — Level 3

## Reference

W3C Web Authentication Working Group. “[Web Authentication: An API for
Accessing Public Key Credentials — Level 3](https://www.w3.org/TR/webauthn-3/).”
W3C Recommendation, 25 August 2026. Editors: Tim Cappalli, Akshay Kumar, Emil
Lundberg, Matthew Miller, Pascoe, and Nina Satragno.

## Research question or contribution

WebAuthn defines how a relying party creates and uses scoped public-key
credentials through a user agent and authenticator while binding ceremonies to
the relying party, origin, challenge, and authenticator-produced signature.

## Method

This is a normative interoperability specification. Its credential model,
registration and assertion ceremonies, scoping, user presence or verification,
attestation, security considerations, and privacy boundaries were reviewed.

## Findings

- Credentials are scoped to a relying party; the authenticator signs fresh
  challenge-bound data rather than releasing a shared password to the verifier.
- The user agent mediates authenticator use, and the authenticator reports user
  presence or verification and can require an explicit authorization gesture.
- Attestation can communicate authenticator properties, but relying parties
  must balance assurance against identification and privacy risks.
- Multi-device and single-device credentials serve different portability and
  key-confinement goals; deployment policy must not collapse them into one
  assurance class.
- End-to-end security depends on the relying party, client, authenticator,
  origin validation, transport, and UI—not on the signature primitive alone.

## Relevance

The Atom OS authenticator service should implement a WebAuthn-compatible
ceremony for remote relying parties and reuse its core properties locally:
fresh challenge, verifier or operation binding, explicit user gesture, scoped
keys, and no disclosure of a reusable OS password. A native local protocol can
bind the challenge to a trusted interaction surface and a proposed authority
grant rather than to a spoofable application window.

## Limits

WebAuthn is a web authentication protocol, not a general OS authorization or
capability protocol. It does not decide what an authenticated principal may do,
make a compromised client trustworthy, guarantee a trusted local display, or
define session revocation and break-glass recovery. Attestation metadata also
creates operational and privacy obligations.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
