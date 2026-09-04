---
title: "Certificate Transparency version 2.0"
kind: source
created: "2026-09-04"
authors:
  - "Ben Laurie"
  - "Eran Messeri"
  - "Rob Stradling"
published: 2021
citation_key: "laurie-et-al-2021-certificate-transparency-v2"
container: "RFC 9162"
edition: "Experimental"
isbn: null
doi: "10.17487/RFC9162"
url: "https://www.rfc-editor.org/rfc/rfc9162.html"
accessed: "2026-09-04"
tags:
  - audit
  - certificate-transparency
  - merkle-trees
  - transparency
aliases:
  - "RFC 9162"
---

# Certificate Transparency version 2.0

## Reference

Ben Laurie, Eran Messeri, and Rob Stradling. “[Certificate Transparency
Version 2.0](https://www.rfc-editor.org/rfc/rfc9162.html).” RFC 9162, December
2021. DOI [10.17487/RFC9162](https://doi.org/10.17487/RFC9162).

## Research question or contribution

RFC 9162 specifies append-only public logs, signed tree heads, inclusion and
consistency proofs, and submitter, log, monitor, and auditor roles for making
certificate issuance visible and externally checkable.

## Method

This is an IETF experimental protocol specification. It defines Merkle-tree
commitments and role interactions; it does not empirically establish that all
deployments detect equivocation or certificate abuse.

## Findings

- Inclusion proofs show that a leaf belongs to a committed tree; consistency
  proofs show that a later tree extends an earlier one.
- A signed tree head is only one view. Independent monitors, auditors, and
  exchange of commitments are needed to detect omission or split views.
- Append-only integrity does not prove that submitted statements are true or
  that every event that should have been submitted was logged.
- Availability and maximum merge delay remain operational properties.

## Relevance

Atom's audit service can use periodic Merkle commitments and independent
witnesses to make post-commit deletion or equivocation detectable. Resource
servers still need bounded local admission and explicit loss markers when the
audit path is unavailable; transparency is not synchronous authorization.

## Limits

Certificate Transparency is designed for public certificate ecosystems. Atom
may require confidential event payloads, selective disclosure, retention, and
redaction, so it can reuse commitment structures and role separation without
publishing sensitive logs.

## Derived work

- [Audit and witness services](../20-notes/authentication-and-authorization-components/audit-and-witness-services.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
