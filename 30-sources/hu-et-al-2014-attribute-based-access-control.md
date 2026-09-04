---
title: "Guide to attribute based access control definition and considerations"
kind: source
created: "2026-09-04"
authors:
  - "Vincent Hu"
  - "David Ferraiolo"
  - "Richard Kuhn"
  - "Adam Schnitzer"
  - "Kenneth Sandlin"
  - "Robert Miller"
  - "Karen Scarfone"
published: 2014
citation_key: "hu-et-al-2014-attribute-based-access-control"
container: "NIST Special Publication 800-162"
edition: "Updated through 2 August 2019"
isbn: null
doi: "10.6028/NIST.SP.800-162"
url: "https://csrc.nist.gov/pubs/sp/800/162/upd2/final"
accessed: "2026-09-04"
tags:
  - abac
  - attributes
  - authorization
  - nist
aliases:
  - "NIST SP 800-162"
---

# Guide to attribute based access control definition and considerations

## Reference

Vincent Hu, David Ferraiolo, Richard Kuhn, Adam Schnitzer, Kenneth Sandlin,
Robert Miller, and Karen Scarfone. “[Guide to Attribute Based Access Control
(ABAC) Definition and Considerations](https://doi.org/10.6028/NIST.SP.800-162).”
NIST Special Publication 800-162, January 2014, updated August 2019.

## Research question or contribution

NIST SP 800-162 defines ABAC and surveys the policy, attribute, administrative,
interoperability, privacy, and deployment considerations needed to use it.

## Method

This is NIST technical guidance and a conceptual reference architecture.
It defines authorization in terms of subject, object, action, and sometimes
environment attributes evaluated against policy, rules, or relationships; it
does not benchmark or formally verify a concrete engine.

## Findings

- Attribute names alone are insufficient: authority, value, scope, semantics,
  and lifecycle determine whether an attribute is trustworthy.
- ABAC can express contextual decisions across organizations, but attribute
  administration and interoperability become part of the trusted system.
- Privacy and minimization matter because collecting more attributes can expose
  sensitive information and create new correlation paths.
- Policy decision and enforcement remain distinct responsibilities.

## Relevance

Atom's attribute authorities should issue typed, provenance-carrying,
short-lived assertions from declared sources. A policy snapshot must record
the issuer, schema, validity interval, and revision used for a decision, while
the kernel sees only the derived capability and never interprets free-form
attributes.

## Limits

The publication is broad guidance for federal information systems. It neither
defines a wire format nor resolves conflicting issuers, offline freshness,
privacy budgets, or the exact composition of ABAC with capabilities and
relationship authorization.

## Derived work

- [Attribute authorities](../20-notes/authentication-and-authorization-components/attribute-authorities.md)
- [Policy decision point](../20-notes/authentication-and-authorization-components/policy-decision-point.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
