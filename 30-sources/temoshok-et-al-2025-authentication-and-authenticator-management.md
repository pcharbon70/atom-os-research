---
title: "Digital identity guidelines: authentication and authenticator management"
kind: source
created: "2026-09-04"
authors:
  - "David Temoshok"
  - "Yee-Yin Choong"
  - "Andrew Regenscheid"
  - "Ryan Galluzzo"
  - "James L. Fenton"
  - "Justin Richer"
  - "Naomi Lefkovitz"
published: 2025
citation_key: "temoshok-et-al-2025-authentication-and-authenticator-management"
container: "NIST Special Publication 800-63B-4"
edition: "Revision 4"
isbn: null
doi: "10.6028/NIST.SP.800-63B-4"
url: "https://pages.nist.gov/800-63-4/sp800-63b.html"
accessed: "2026-09-04"
tags:
  - authentication
  - credentials
  - digital-identity
  - recovery
aliases:
  - "NIST SP 800-63B-4"
---

# Digital identity guidelines: authentication and authenticator management

## Reference

David Temoshok, Yee-Yin Choong, Andrew Regenscheid, Ryan Galluzzo, James L.
Fenton, Justin Richer, and Naomi Lefkovitz. “[Digital Identity Guidelines:
Authentication and Authenticator Management](https://doi.org/10.6028/NIST.SP.800-63B-4).”
NIST Special Publication 800-63B-4, August 2025. The navigable
[official HTML](https://pages.nist.gov/800-63-4/sp800-63b.html) was used for
section-level verification.

## Research question or contribution

The guideline specifies authenticator, verifier, session, binding, recovery,
and lifecycle requirements at three authentication assurance levels (AALs).

## Method

This is normative U.S. federal guidance developed through NIST’s public process,
not an Atom OS threat model or an authorization specification. Requirements for
AALs, phishing resistance, password verification, authenticator binding,
recovery, and session timeouts were inspected directly.

## Findings

- AAL2 requires multi-factor authentication and at least one replay-resistant
  authenticator; verifiers must offer a phishing-resistant option. AAL3 requires
  phishing-resistant public-key authentication with a non-exportable private
  key in a hardware-protected isolated environment.
- Syncable authenticators are exportable and therefore cannot satisfy AAL3,
  although they can support lower assurance profiles.
- Passwords are not phishing-resistant. Where retained, verifiers must use a
  protected channel, rate limiting, compromised-password blocklists, and salted
  costed password hashing; a separately protected keyed operation is advised.
- A biometric is not an authenticator by itself; local biometric comparison can
  activate a physical cryptographic authenticator.
- Providers must support multiple bound authenticators. Adding an authenticator
  requires appropriate authentication and an independent notification.
- Sessions require definite reauthentication limits. Recovery and authenticator
  replacement are security events, not support-channel exceptions.

## Relevance

Atom OS should make phishing-resistant public-key authenticators the normal
human-authentication path and a hardware-bound, non-exportable authenticator the
high-assurance path. Assurance must be recorded in authentication evidence and
checked by policy for each sensitive grant; “logged in” is too coarse. Passwords
should be optional compatibility or recovery mechanisms confined to the trusted
interaction path, never accepted by arbitrary applications.

## Limits

The guideline targets networked digital identity and U.S. federal use. It does
not prescribe an OS capability model, kernel interface, workload identity,
device attestation architecture, application authorization language, or
recovery availability policy. Compliance also does not prove that a particular
authenticator, UI, verifier, or supply chain is secure.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
- [2026-09-04 authentication and authorization deep dive](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md)
