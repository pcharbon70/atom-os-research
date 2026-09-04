---
title: "The Entity Attestation Token"
kind: source
created: "2026-09-04"
authors:
  - "Laurence Lundblade"
  - "Giridhar Mandyam"
  - "John O'Donoghue"
  - "Carl Wallace"
published: 2025
citation_key: "lundblade-et-al-2025-entity-attestation-token"
container: "RFC 9711"
edition: "Proposed Standard"
isbn: null
doi: "10.17487/RFC9711"
url: "https://www.rfc-editor.org/rfc/rfc9711.html"
accessed: "2026-09-04"
tags:
  - attestation
  - eat
  - protocol-security
  - rats
aliases:
  - "EAT"
---

# The Entity Attestation Token

## Reference

Laurence Lundblade, Giridhar Mandyam, John O’Donoghue, and Carl Wallace. “[The
Entity Attestation Token (EAT)](https://doi.org/10.17487/RFC9711).” RFC 9711,
April 2025.

## Research question or contribution

EAT defines a profileable framework for conveying attestation-oriented claims
about devices, hardware, software, or processes in authenticity-protected CWT
or JWT structures.

## Method

This is a normative IETF specification. The common claims, nonce freshness,
profiles, nesting, detached claims, privacy, verifier/relying-party boundaries,
and inherited CWT/JWT properties were reviewed.

## Findings

- EAT can carry software identity or version, measurements, boot and debug
  state, manifests, device identifiers, nonces, and nested submodules.
- It is a framework, not a complete token profile: a deployment must select
  claims, encodings, algorithms, validation, and privacy rules.
- Evidence and attestation results can both use EAT, but the verifier’s policy
  determines how evidence is transformed, checked, summarized, or redacted.
- Attestation has a different security model from user or server
  authentication, and an EAT does not imply an authorization decision.

## Relevance

Atom OS should define one compact, versioned CBOR/COSE EAT profile for boot and
workload evidence at network boundaries. Applications should receive a
privacy-minimized verifier result or its digest, not raw PCR logs or an open
bag of claims, and policy should bind that result to a fresh session grant.

## Limits

No common EAT claim is mandatory, unknown claims may be ignored, and algorithm
flexibility creates downgrade and interoperability risk without a strict
profile. EAT does not establish measurement truth, reference-value governance,
runtime integrity, identity proofing, or authorization.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
