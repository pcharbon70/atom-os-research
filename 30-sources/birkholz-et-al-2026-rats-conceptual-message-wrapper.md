---
title: "Remote ATtestation procedureS (RATS) Conceptual Message Wrapper"
kind: source
created: "2026-09-04"
authors:
  - "Henk Birkholz"
  - "Ned Smith"
  - "Thomas Fossati"
  - "Hannes Tschofenig"
published: 2026
citation_key: "birkholz-et-al-2026-rats-conceptual-message-wrapper"
container: "RFC 9999"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC9999"
url: "https://www.rfc-editor.org/rfc/rfc9999.html"
accessed: "2026-09-04"
tags:
  - attestation
  - cbor
  - rats
  - security
aliases:
  - "RFC 9999"
  - "RATS CMW"
---

# Remote ATtestation procedureS (RATS) Conceptual Message Wrapper

## Reference

Henk Birkholz, Ned Smith, Thomas Fossati, and Hannes Tschofenig. “[Remote
ATtestation procedureS (RATS) Conceptual Message Wrapper
(CMW)](https://www.rfc-editor.org/rfc/rfc9999.html).” RFC 9999, July 2026.
DOI [10.17487/RFC9999](https://doi.org/10.17487/RFC9999).

## Research question or contribution

RFC 9999 defines explicit wrappers for RATS conceptual messages across CBOR,
JSON, JWT, CWT, X.509, media types, and collections so message role and inner
encoding do not depend only on an outer transport.

## Method

This is an IETF Standards Track format specification. It defines record, tag,
and collection wrappers, type indicators, demultiplexing, and optional
cryptographic protection, then analyzes composite/layered and protocol-use
risks.

## Findings

- Evidence, Attestation Results, Endorsements, Reference Values, and Appraisal
  Policies remain distinct conceptual message types even when transported in
  diverse containers.
- Wrappers can make handler selection explicit but provide no authenticity,
  integrity, or confidentiality merely by being present.
- Collection wrappers are recursive, and implementations may limit nesting
  depth.
- Composite evidence requires cryptographic binding among the components;
  collection adjacency is not proof that claims describe the same attester.

## Relevance

Atom's RATS verifier should pin accepted conceptual types and inner profiles,
dispatch opaque bounded payloads to confined handlers, and reject unsupported
or ambiguously protected collections. Its Atom profile should impose hard
depth, item-count, and byte-size limits. Explicit typing is a parser boundary,
not an authorization result.

## Limits

The RFC supplies encapsulation and interoperability, not a complete evidence
profile, trust model, appraisal policy, freshness protocol, resource bounds, or
authorization decision.

## Derived work

- [RATS Verifier and Appraisal Policy](../20-notes/authentication-and-authorization-components/rats-verifier-and-appraisal-policy.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
