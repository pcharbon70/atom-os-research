---
title: "Remote attestation procedures architecture"
kind: source
created: "2026-09-04"
authors:
  - "Henk Birkholz"
  - "Dave Thaler"
  - "Michael Richardson"
  - "Ned Smith"
  - "Wei Pan"
published: 2023
citation_key: "birkholz-et-al-2023-rats-architecture"
container: "RFC 9334"
edition: "Informational"
isbn: null
doi: "10.17487/RFC9334"
url: "https://www.rfc-editor.org/rfc/rfc9334.html"
accessed: "2026-09-04"
tags:
  - attestation
  - device-identity
  - rats
  - trust
aliases:
  - "RATS architecture"
---

# Remote attestation procedures architecture

## Reference

Henk Birkholz, Dave Thaler, Michael Richardson, Ned Smith, and Wei Pan.
“[Remote ATtestation procedureS (RATS) Architecture](https://doi.org/10.17487/RFC9334).”
RFC 9334, January 2023.

## Research question or contribution

RATS defines interoperable roles and artifacts for producing evidence about an
attester, appraising it against reference values and endorsements, and using
the resulting appraisal in a relying party’s application decision.

## Method

This is an IETF architectural and terminology document. Its Attester, Verifier,
Relying Party, owner, Endorser, Reference Value Provider, freshness, layered
attestation, and appraisal-policy boundaries were inspected.

## Findings

- An Attester produces Evidence; a Verifier appraises that evidence and issues
  Attestation Results; a Relying Party applies its own policy to those results.
- Trust is the relying party’s choice, while trustworthiness is a property for
  which evidence may be appraised. Evidence is not self-executing permission.
- Layered attestation can stage measurements from immutable or protected code
  through bootloader, kernel, and application layers.
- Freshness, endorsements, reference values, privacy, and the protection of the
  attesting and verifying environments are security-critical.
- A verifier or root-of-trust compromise can make evidence forgeable; remote
  attestation does not turn a measured component into uncompromised code.

## Relevance

Atom OS should keep measured-boot evidence, verifier appraisal, and
authorization policy as separate artifacts. A service or node may present a
fresh, nonce-bound attestation result, but the policy service must still decide
which resource/action grant, if any, follows, and the kernel must enforce only
the resulting local capabilities.

## Limits

RFC 9334 is informational and intentionally neutral about evidence formats,
roots of trust, protocols, algorithms, and authorization models. Privacy and
endorsement ownership can make attestation unsuitable for some deployments;
absence of an approved measurement is not proof of maliciousness.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
- [2026-09-04 authentication and authorization deep dive](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md)
