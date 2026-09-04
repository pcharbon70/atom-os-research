---
title: "The NIST model for role-based access control"
kind: source
created: "2026-09-04"
authors:
  - "Ravi Sandhu"
  - "David Ferraiolo"
  - "Richard Kuhn"
published: 2000
citation_key: "sandhu-et-al-2000-nist-rbac-model"
container: "Proceedings of the Fifth ACM Workshop on Role-Based Access Control (RBAC '00)"
edition: null
isbn: null
doi: "10.1145/344287.344301"
url: "https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard"
accessed: "2026-09-04"
tags:
  - authorization
  - rbac
  - security-models
aliases:
  - "NIST RBAC model"
---

# The NIST model for role-based access control

## Reference

Ravi Sandhu, David Ferraiolo, and Richard Kuhn. “[The NIST Model for
Role-Based Access Control: Towards a Unified
Standard](https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard).”
*Proceedings of the Fifth ACM Workshop on Role-Based Access Control*, 2000.
DOI [10.1145/344287.344301](https://doi.org/10.1145/344287.344301).

## Research question or contribution

The paper unifies common RBAC ideas into a reference model with cumulative
flat, hierarchical, constrained, and symmetric levels, while identifying
features for which no consensus model yet existed.

## Method

The authors synthesize earlier formal models, research prototypes, and
commercial practice into sets, relations, and required operations intended to
support a later standard. This is a model and consensus proposal, not a
comparative security or performance evaluation.

## Findings

- Users, roles, permissions, sessions, and their assignment relations are
  separate objects; a session activates only a subset of a user's assigned
  roles.
- Role hierarchies and constraints add semantics beyond simple group labels.
- Static and dynamic separation of duty are explicit constraints, not an
  accidental consequence of role naming.
- Administrative review of assignments is part of an RBAC system's contract.

## Relevance

Atom can use roles as policy input for job functions and separation of duty,
but the relationship or attribute authority must not turn a role string into a
kernel power. The policy decision point evaluates versioned role facts and the
grant issuer compiles only the permitted subset into an attenuated capability.

## Limits

RBAC does not by itself model object relationships, device posture,
proof-of-possession, distributed freshness, capabilities, or information flow.
The paper deliberately excludes unsettled features and does not establish that
every role engineering practice is safe.

## Derived work

- [Relationship authority](../20-notes/authentication-and-authorization-components/relationship-authority.md)
- [Policy decision point](../20-notes/authentication-and-authorization-components/policy-decision-point.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
