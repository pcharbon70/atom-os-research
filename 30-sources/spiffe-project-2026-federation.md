---
title: "SPIFFE Federation"
kind: source
created: "2026-09-04"
authors:
  - "SPIFFE Project"
published: null
citation_key: "spiffe-project-2026-federation"
container: "SPIFFE standards repository"
edition: "Pinned revision 99470b9abc825f14aa364dfa2c3b53b02ba5db5b"
isbn: null
doi: null
url: "https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/SPIFFE_Federation.md"
accessed: "2026-09-04"
tags:
  - federation
  - spiffe
  - trust-bundles
  - workload-identity
aliases:
  - "SPIFFE federation specification"
---

# SPIFFE Federation

## Reference

SPIFFE Project. “[SPIFFE
Federation](https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/SPIFFE_Federation.md).”
Pinned revision `99470b9abc825f14aa364dfa2c3b53b02ba5db5b`, accessed 4
September 2026.

## Research question or contribution

The specification defines how one SPIFFE trust domain obtains and refreshes
another domain's trust bundle so workloads can authenticate across explicitly
configured domain boundaries.

## Method

This is a living first-party SPIFFE standard inspected at an immutable
revision. The review focused on directional relationships, endpoint/profile
configuration, bundle separation, refresh/retry, rotation overlap, and
relationship removal.

## Findings

- Federation relationships are one-way and explicitly configure the foreign
  trust domain, bundle endpoint, and endpoint profile.
- Foreign bundles must remain separate rather than being merged into the local
  trust bundle.
- New keys should be published for several refresh intervals before use to
  permit overlap; failed polls should not become aggressive retry storms.
- Terminating a relationship removes the bundle and propagates removal to
  validators, subject to implementation timing.
- Federation provides cross-domain authentication, not application
  authorization or transitive trust.

## Relevance

Atom's gateway should represent every peer as a directional, versioned
relationship with a separate bundle and namespace, controlled rotation, and an
explicit deletion/revocation bound. A validated SPIFFE ID remains evidence for
the local PDP, never a kernel capability.

## Limits

The living specification leaves application authorization, refresh timing,
storage rollback, hostile endpoints, and availability to implementations. Its
host/platform trust assumptions do not automatically match Atom.

## Derived work

- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)
- [Workload identity issuer](../20-notes/authentication-and-authorization-components/workload-identity-issuer.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
