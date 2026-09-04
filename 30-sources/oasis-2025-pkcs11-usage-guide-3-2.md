---
title: "PKCS #11 Cryptographic Token Interface Usage Guide version 3.2"
kind: source
created: "2026-09-04"
authors:
  - "Dieter Bong"
published: 2025
citation_key: "oasis-2025-pkcs11-usage-guide-3-2"
container: "OASIS Committee Note 01"
edition: "Version 3.2"
isbn: null
doi: null
url: "https://docs.oasis-open.org/pkcs11/pkcs11-ug/v3.2/cn01/pkcs11-ug-v3.2-cn01.html"
accessed: "2026-09-04"
tags:
  - cryptography
  - hardware-security-modules
  - key-management
  - standards
aliases:
  - "PKCS #11 usage guide 3.2"
---

# PKCS #11 Cryptographic Token Interface Usage Guide version 3.2

## Reference

Dieter Bong, editor. “[PKCS #11 Cryptographic Token Interface Usage Guide
Version
3.2](https://docs.oasis-open.org/pkcs11/pkcs11-ug/v3.2/cn01/pkcs11-ug-v3.2-cn01.html).”
OASIS Committee Note 01, 15 April 2025.

## Research question or contribution

The guide explains the PKCS #11 application/token/session/user model and gives
security and concurrency guidance for using the v3.2 interface.

## Method

This is a non-standards-track first-party companion to the PKCS #11
specification. The review focused on login scope, session/object handles,
sensitive/extractable behavior, application sharing, operation state, and the
trust placed in the host OS.

## Findings

- Sensitive keys cannot be exported in plaintext; unextractable keys cannot
  leave even in encrypted form but remain usable through token operations.
- For a given application and token, login/logout state is shared across its
  sessions, and a logged-in read/write user session has broad object access.
- Threads in an application have equal access to its session handles; the API
  is not an object-capability isolation boundary among those callers.
- A compromised host OS can capture activation input or alter commands, while
  a token can still become a signing/decryption oracle.

## Relevance

Atom needs a broker that translates narrow capabilities into one key/object/
operation call, rather than handing applications a globally logged-in token
session. Non-exportability is useful but insufficient without input schemas,
audience, rate limits, and caller-incarnation binding.

## Limits

The guide describes Cryptoki rather than proving a device implementation
secure. Token vendors, mechanisms, threading, authentication, physical
security, and side channels vary.

## Derived work

- [Key and secret service](../20-notes/authentication-and-authorization-components/key-and-secret-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
