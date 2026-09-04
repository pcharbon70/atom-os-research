---
title: "eXtensible Access Control Markup Language version 3.0 plus Errata 01"
kind: source
created: "2026-09-04"
authors:
  - "Erik Rissanen"
published: 2017
citation_key: "oasis-2017-xacml-3-0"
container: "OASIS Standard"
edition: "Version 3.0 Plus Errata 01"
isbn: null
doi: null
url: "https://docs.oasis-open.org/xacml/3.0/errata01/os/xacml-3.0-core-spec-errata01-os-complete.html"
accessed: "2026-09-04"
tags:
  - authorization
  - policy
  - standards
  - xacml
aliases:
  - "XACML 3.0"
---

# eXtensible Access Control Markup Language version 3.0 plus Errata 01

## Reference

Erik Rissanen, editor. “[eXtensible Access Control Markup Language (XACML)
Version 3.0 Plus Errata
01](https://docs.oasis-open.org/xacml/3.0/errata01/os/xacml-3.0-core-spec-errata01-os-complete.html).”
OASIS Standard incorporating Approved Errata, 12 July 2017.

## Research question or contribution

XACML standardizes a policy language, request/response model, combining
algorithms, and reference architecture for separating policy administration,
decision, information, and enforcement points.

## Method

This is a consensus specification. The review focused on its architectural
roles, attribute categories and issuers, multi-valued decisions, missing-data
behavior, combining algorithms, obligations, advice, and security
considerations—not on adopting its XML representation.

## Findings

- PAP, PDP, PIP, context handler, and PEP are distinct roles, making input
  acquisition and effect enforcement visible rather than hidden inside an
  evaluator.
- Decisions include `Permit`, `Deny`, `Indeterminate`, and `NotApplicable`;
  missing or erroneous input can be represented explicitly as
  `Indeterminate` rather than hidden as a boolean result.
- Combining algorithms are semantic choices whose order and error behavior can
  change a result.
- Obligations must be discharged for a decision to remain valid, whereas advice
  may be ignored; confusing the two can broaden access.

## Relevance

Atom should preserve the role separation and typed outcome discipline while
using a smaller bounded language and canonical binary request form. Attribute
resolution happens before the pure PDP call; the resource-side admission path
must treat every non-`Permit` outcome as fail-closed and either atomically
enforce declared obligations or reject the grant.

## Limits

XACML is large, extensible, and XML-oriented. Its flexibility can make
evaluation, canonicalization, and interoperability complex, and the standard
does not provide kernel capabilities, causal relation storage, or an assurance
proof for a concrete implementation.

## Derived work

- [Attribute authorities](../20-notes/authentication-and-authorization-components/attribute-authorities.md)
- [Policy decision point](../20-notes/authentication-and-authorization-components/policy-decision-point.md)
- [Grant compiler and issuer](../20-notes/authentication-and-authorization-components/grant-compiler-and-issuer.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
