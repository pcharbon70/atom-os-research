---
title: "Capability myths demolished"
kind: source
created: "2026-08-31"
authors:
  - "Mark S. Miller"
  - "Ka-Ping Yee"
  - "Jonathan S. Shapiro"
published: 2003
citation_key: "miller-et-al-2003-capability-myths"
container: "Johns Hopkins University Systems Research Laboratory Technical Report SRL2003-02"
edition: null
isbn: null
doi: null
url: "https://erights.org/talks/myths/index.html"
accessed: "2026-08-31"
tags:
  - capabilities
  - least-privilege
  - revocation
  - security
aliases:
  - "Capability myths"
---

# Capability myths demolished

## Reference

Mark S. Miller, Ka-Ping Yee, and Jonathan S. Shapiro. “Capability Myths
Demolished.” Johns Hopkins University Systems Research Laboratory Technical
Report SRL2003-02, 2003.
[Canonical author-hosted version](https://erights.org/talks/myths/index.html).
[Open PDF mirror](https://cgi.cse.unsw.edu.au/~cs9242/papers/Miller_YS_03.pdf).

## Research question or contribution

The report distinguishes several meanings of “capability” and tests three
recurring claims: that capabilities are merely transposed ACLs, cannot enforce
confinement, and cannot support revocation.

## Method

The authors compare ACL-as-column, capability-as-row, key-like, and object-
capability models using properties such as no ambient authority, designation
with authority, dynamic subject creation, and secure delegation.

## Findings

- Pure object capabilities combine designation and authority, reducing the
  confused-deputy risk created when a name is interpreted under ambient
  privilege.
- Revocation is possible but not free. A delegator can interpose a composed
  forwarder/revoker facet and later disable that indirect path.
- Once unrestricted authority is deliberately transferred outside a revocable
  relationship, revoking its already distributed effects is harder.
- Capability and ACL systems should not be compared solely as static access
  matrices because their delegation and principal-creation behavior differs.

## Relevance

The project must define revocability when a capability is delegated. Combining
the report's indirection pattern with seL4-style kernel-maintained derivation
suggests two different tools: a revocable session/facet for one relationship
and an explicit lineage for descendants of kernel capabilities. Call-scoped
borrowed capabilities should expire with the call. “POSIX capability” bitsets,
numeric object IDs, and signed tokens are not automatically equivalent to
protected object capabilities.

## Limits

The report is a conceptual security analysis rather than a kernel
implementation or performance study. Indirection shifts cost and trust rather
than eliminating them, and revocation cannot undo writes or external effects
that occurred before authority was withdrawn.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
