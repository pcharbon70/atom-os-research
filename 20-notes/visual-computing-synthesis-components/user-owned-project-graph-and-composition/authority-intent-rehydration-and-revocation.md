---
title: "Authority intent, rehydration, and revocation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - capability-security
  - project-graph
  - visual-computing
aliases: []
---

# Authority intent, rehydration, and revocation

This study decomposes [User-owned project graph and composition](../user-owned-project-graph-and-composition.md).

Research question: How can a durable project remember intended delegation
without serializing a replayable bearer capability?

## Research basis and status

Capability-based OS design shows how explicit kernel objects can carry
delegated authority; capability-security analysis emphasizes that authority
follows reachable references rather than names. User-driven access control
shows how current interaction can help select a narrow object grant.
[1](../../../30-sources/parmer-2016-capability-based-os-design.md)
[2](../../../30-sources/miller-et-al-2003-capability-myths.md)
[3](../../../30-sources/roesner-et-al-2012-user-driven-access-control.md)

Atom OS rehydration and revocation semantics remain proposed.

## Development

### Owned state and trust boundary

Durable records store policy identifiers, delegation lineage, intended object
scope, operation ceilings, audience class, and last known revocation epoch.
The authority service owns live derivation and revocation. Project storage
cannot mint a capability, and a provider cannot follow transitive references
outside the explicitly derived facet.

### Admission, transitions, and completion

On open, the resolver authenticates the principal and session, loads current
policy and revocation state, compares object and binding generations, and asks
for a short-lived audience-bound grant. Derivation is recorded with a grant ID.
Revocation advances an epoch, closes relevant sessions, and requires
receiver-side epoch or generation enforcement.

### Failure and adversarial behavior

Restored backups may contain obsolete grants; offline replicas may miss
membership revocation; confused deputies may exchange authority-bearing
handles. Rehydration always evaluates current state, sealed values are
non-transferable to unlisted audiences, and recovered services start with no
inherited live grants.

### Alternatives and unresolved tradeoffs

Persisting encrypted capabilities still makes key recovery and replay policy
part of authority. Reauthorization on every operation is safer but harms
offline use. Expiring session grants with sink-side fencing are preferred; the
offline read/edit ceiling and revocation-latency profile require qualification.

## Verification obligations

- Restore a project backup from before revocation and prove reopening cannot
  recreate the withdrawn grant.
- Crash resolver and provider during derivation, revoke concurrently, and
  enumerate all surviving references after restart.
- Attempt provider-to-provider and project-to-project capability laundering;
  every receiver must enforce audience and delegation ceiling.

## Connections

- [Internal-service index](README.md) — project-level authority context.
- [Trusted interaction services](../input-focus-and-trusted-interaction-authority/README.md) — supplies current user-selected intent.
- [Authentication and authorization](../../authentication-and-authorization-across-the-five-layer-architecture.md) — enclosing authority model.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence boundary.

## Sources

1. [Capability-based OS design](../../../30-sources/parmer-2016-capability-based-os-design.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
3. [User-driven access control](../../../30-sources/roesner-et-al-2012-user-driven-access-control.md).
