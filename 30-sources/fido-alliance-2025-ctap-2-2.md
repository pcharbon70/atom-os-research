---
title: "Client to Authenticator Protocol 2.2"
kind: source
created: "2026-09-04"
authors:
  - "FIDO Alliance"
published: 2025
citation_key: "fido-alliance-2025-ctap-2-2"
container: "FIDO Alliance specification"
edition: "Proposed Standard, 14 July 2025"
isbn: null
doi: null
url: "https://fidoalliance.org/specs/fido-v2.2-ps-20250714/fido-client-to-authenticator-protocol-v2.2-ps-20250714.html"
accessed: "2026-09-04"
tags:
  - authentication
  - ctap
  - fido2
  - hardware-authenticator
aliases:
  - "CTAP 2.2"
---

# Client to Authenticator Protocol 2.2

## Reference

FIDO Alliance. “[Client to Authenticator Protocol
2.2](https://fidoalliance.org/specs/fido-v2.2-ps-20250714/fido-client-to-authenticator-protocol-v2.2-ps-20250714.html).”
Proposed Standard, 14 July 2025.

## Research question or contribution

CTAP specifies communication between a platform client and platform or roaming
authenticators for discovery, credential creation and assertion, user presence
or verification, PIN/UV protocols, authenticator configuration, and credential
management.

## Method

This is a normative interoperability specification. The command surface,
transport-independent framing, version negotiation, PIN/UV, token permissions,
credential management, reset, and security considerations were reviewed.

## Findings

- CTAP supplies the local half of FIDO2; WebAuthn alone does not define how an
  OS client talks to a USB, NFC, BLE, or platform authenticator.
- User presence, user verification, and token permissions are distinct signals
  and must be validated for the requested operation.
- Authenticator-management and reset commands are more powerful than ordinary
  assertions and require separate policy and trusted interaction.
- The protocol evolves through versions and optional capabilities, so robust
  implementations must negotiate and reject unsupported or ambiguous states.

## Relevance

Atom OS should implement CTAP in an isolated authenticator service behind
exclusive, capability-gated device access. The kernel should provide bounded
USB/NFC/BLE device and secure-input mechanisms but should not parse CBOR,
authenticator metadata, PIN/UV, or future CTAP extensions. Local login needs an
explicit domain-separated relying-party profile above this service.

## Limits

CTAP 2.2 is a Proposed Standard and is only one part of the end-to-end FIDO2
ceremony. A conforming authenticator, transport, client, or driver may still be
compromised. The specification is not an application authorization model and
does not define OS session or capability semantics.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
