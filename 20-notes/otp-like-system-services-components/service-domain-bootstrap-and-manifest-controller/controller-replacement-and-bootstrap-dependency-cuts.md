---
title: "Controller replacement and bootstrap dependency cuts"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Controller replacement and bootstrap dependency cuts

This study decomposes [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller.md).

Research question: How can the service controller be replaced when its normal storage, naming or identity dependencies are unavailable?

## Research basis and status

Controller liveness and fine-grained restart both depend on external services and
recovery assumptions; neither supplies an immortal recovery root. [1](../../../30-sources/sun-et-al-2024-anvil.md) [2](../../../30-sources/candea-et-al-2004-microreboot.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The replacement holder owns sealed controller-start authority and a bounded recovery
capsule outside the controller's destruction boundary. The capsule identifies the
delegation envelope, last accepted plan, durable-state locator and a constrained
observation path.

### Admission, transitions and completion

Construct a dependency cut that can locate and recover required storage without
consulting the failed registry, and authenticate recovery without a credential
issued only by the failed broker. Fence the old controller before installing
successor management facets. Reconcile surviving services from authoritative
receipts rather than stopping all of them.

### Failure and adversarial behavior

Corrupt or unavailable metadata prohibits fresh irreversible work. Existing
published services may continue only within their original grants and expiry
policies. A total loss of the recovery capsule invokes an explicitly wider recovery
boundary, not self-appointment by an ordinary service.

### Alternatives and unresolved tradeoffs

A static recovery nucleus has limited flexibility but makes the bootstrap cycle
reviewable. A replicated manager improves availability only after its own trust and
storage bootstrap are solved. Capsule retention and compromise recovery remain
architecture choices.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Disable controller, registry and issuer together; the declared independent path must still identify its bounded recovery inputs.
- Verify replacement does not revoke unrelated healthy grants or reconstruct broader authority from service-reported names.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Naming, registry, and local discovery](../naming-registry-and-local-discovery/README.md) — publishes current bindings and watch revisions.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Anvil](../../../30-sources/sun-et-al-2024-anvil.md).
2. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
