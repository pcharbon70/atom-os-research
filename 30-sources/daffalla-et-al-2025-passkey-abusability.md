---
title: "A framework for abusability analysis: the case of passkeys in interpersonal threat models"
kind: source
created: "2026-09-04"
authors:
  - "Alaa Daffalla"
  - "Arkaprabha Bhattacharya"
  - "Jacob Wilder"
  - "Rahul Chatterjee"
  - "Nicola Dell"
  - "Rosanna Bellini"
  - "Thomas Ristenpart"
published: 2025
citation_key: "daffalla-et-al-2025-passkey-abusability"
container: "34th USENIX Security Symposium, 7819–7838"
edition: null
isbn: "978-1-939133-52-6"
doi: null
url: "https://www.usenix.org/system/files/usenixsecurity25-daffalla.pdf"
accessed: "2026-09-04"
tags:
  - account-recovery
  - interpersonal-threats
  - passkeys
  - usable-security
aliases:
  - "Passkey abusability analysis"
---

# A framework for abusability analysis: the case of passkeys in interpersonal threat models

## Reference

Alaa Daffalla et al. “[A Framework for Abusability Analysis: The Case of
Passkeys in Interpersonal Threat Models](https://www.usenix.org/system/files/usenixsecurity25-daffalla.pdf).”
*34th USENIX Security Symposium*, pages 7819–7838, August 2025.

## Research question or contribution

The paper develops a structured abusability-analysis method and applies it to
passkeys where an interpersonal adversary may have periodic physical access,
know or compel disclosure of a device PIN, or exploit normal account-security
interfaces.

## Method

The authors derive threat models from prior literature, inspect common
functions in six services, and execute step-through protocols across 19
passkey-supporting services to validate hypothesized abuse vectors.

## Findings

- Some studied services allowed an adversarial passkey to retain access in
  ways that were difficult or impossible for a victim to discover and remove.
- Passkey features could support account denial and manipulation as well as
  unauthorized login under the studied physical/coercive threats.
- Cryptographic phishing resistance does not guarantee a safe credential
  inventory, notification, removal, synchronization, or recovery interface.

## Relevance

Atom OS must expose every bound authenticator and session with provenance,
exportability or synchronization status, last use, assurance ceiling, and
revocation state. Removal must close future sessions and trigger independent
notification. Recovery and ownership transfer must consider coercion and
periodic unlocked-device access, not only remote attackers.

## Limits

The study evaluates early deployments and application UX, not WebAuthn’s
cryptography or every service. Results are scoped to its threat models and
testing dates. Atom OS still needs its own user studies and red-team exercises.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
