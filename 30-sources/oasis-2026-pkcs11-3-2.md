---
title: "PKCS #11 Specification version 3.2"
kind: source
created: "2026-09-04"
authors:
  - "Dieter Bong"
  - "Greg Scott"
published: 2026
citation_key: "oasis-2026-pkcs11-3-2"
container: "OASIS Standard"
edition: "Version 3.2"
isbn: null
doi: null
url: "https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.2/os/pkcs11-spec-v3.2-os.html"
accessed: "2026-09-04"
tags:
  - cryptography
  - hardware-security-modules
  - key-management
  - standards
aliases:
  - "PKCS #11 3.2"
  - "Cryptoki 3.2"
---

# PKCS #11 Specification version 3.2

## Reference

Dieter Bong and Greg Scott, editors. “[PKCS #11 Specification Version
3.2](https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.2/os/pkcs11-spec-v3.2-os.html).”
OASIS Standard, 3 June 2026.

## Research question or contribution

PKCS #11 defines a portable application interface to cryptographic tokens,
including object handles, token and session objects, attributes, users,
sessions, mechanisms, and cryptographic operations.

## Method

This is a consensus interface specification. The review used its object,
session, attribute, mechanism, and operation model as an engineering precedent
for keeping cryptographic material behind handles; it did not treat every
Cryptoki function as an Atom requirement.

## Findings

- Applications normally refer to keys and other token objects through handles
  and attributes rather than manipulating all protected bytes directly.
- Token objects and session objects have different persistence and visibility
  lifetimes.
- Attributes such as sensitivity and extractability constrain key use, while
  mechanisms identify supported operations and parameters.
- The interface is stateful and exposes a large compatibility surface, so
  authorization, concurrency, cancellation, and error behavior remain critical
  implementation concerns.

## Relevance

The useful Atom precedent is opaque, typed key handles and operation-specific
facets. Atom should use a smaller capability-native service API with explicit
audience, generation, purpose, algorithm, quota, cancellation, and lifecycle
state rather than embedding the full PKCS #11 ABI in the kernel.

## Limits

PKCS #11 defines an API, not a proof that a token is tamper resistant or free
of side channels. Vendor mechanisms, authentication models, and session
semantics vary, and a large general API is unsuitable as Atom's privileged
boundary.

## Derived work

- [Key and secret service](../20-notes/authentication-and-authorization-components/key-and-secret-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
