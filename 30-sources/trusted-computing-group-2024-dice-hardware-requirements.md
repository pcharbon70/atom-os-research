---
title: "Hardware requirements for a Device Identifier Composition Engine"
kind: source
created: "2026-09-04"
authors:
  - "Trusted Computing Group"
published: 2024
citation_key: "trusted-computing-group-2024-dice-hardware-requirements"
container: "Trusted Computing Group specification"
edition: "Version 1.0, Revision 0.91"
isbn: null
doi: null
url: "https://trustedcomputinggroup.org/wp-content/uploads/Hardware-Requirements-for-a-Device-Identifier-Composition-Engine-Version-1.0-Revision-0.91_pub.pdf"
accessed: "2026-09-04"
tags:
  - device-identity
  - dice
  - hardware-root-of-trust
  - measured-boot
aliases:
  - "DICE hardware requirements"
---

# Hardware requirements for a Device Identifier Composition Engine

## Reference

Trusted Computing Group. “[Hardware Requirements for a Device Identifier
Composition Engine](https://trustedcomputinggroup.org/wp-content/uploads/Hardware-Requirements-for-a-Device-Identifier-Composition-Engine-Version-1.0-Revision-0.91_pub.pdf).”
Version 1.0, Revision 0.91, published 8 August 2024.

## Research question or contribution

The specification defines a compact hardware root for platforms without a TPM:
an exclusive Unique Device Secret (UDS) is cryptographically combined with the
measurement and relevant state of the first measured code to produce a
Compound Device Identifier (CDI).

## Method

This is a normative hardware specification. Its scope, secret properties,
measurement transition, debug behavior, update trust, and explicit exclusions
were inspected directly.

## Findings

- The UDS must be statistically unique, reserved for DICE, and accessible only
  to the DICE execution step.
- Any change to the measured first code or included configuration produces a
  different CDI, so later code cannot recover the earlier software identity.
- The UDS is blocked and remnants erased before control passes to measured
  code; debug mode must not reveal it.
- DICE’s own implementation and update path are inherently trusted and are not
  represented in the CDI it computes.
- Protecting and using the CDI after derivation is partly outside this hardware
  specification.

## Relevance

DICE is a plausible embedded Atom OS profile: derive boot-instance key material
from hardware secret plus the measured loader/kernel, then hand only an opaque
derivation or signing context to the next trusted layer. It can ground device
and boot identity without turning a human account, service name, or measurement
hash into authority.

## Limits

The specification does not define the complete certificate, endorsement,
attestation, authorization, revocation, update, or recovery protocol. The DICE
implementation, measurement correctness, debug controls, manufacturing secret,
and post-derivation CDI protection remain roots of trust. Software updates
legitimately change derived identity and require continuity policy.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
