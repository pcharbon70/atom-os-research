---
title: "Client-action binding and trusted command admission"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Client-action binding and trusted command admission

This study decomposes [Presentation sessions, semantic views, and user outcomes](../presentation-sessions-semantic-views-and-user-outcomes.md).

Research question: How is a user's action reconciled if the view disappears before learning its operation ID?

## Research basis and status

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [1](../../../30-sources/lee-et-al-2015-rifl.md).

WAI-ARIA defines semantic roles, states and relationships; vocabulary conformance alone does not establish usable or authorized interaction. [2](../../../30-sources/w3c-2023-wai-aria-1-2.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the durable binding from broker-issued client-action ID and request digest to
domain operation ID. The disposable view may hold a cache of this binding but cannot
be its sole owner. Trusted input policy supplies action-specific grants; focus,
visibility and a read facet do not authorize mutation.

### Admission, transitions and completion

Receive an action with logical target, observed revision, view/session and
input-policy generations, current realm binding and parameters. Atomically bind the
client-action identity before dispatching effectful work. Duplicate admission
returns the existing operation binding; changed parameters fail. Fresh authorized
snapshots expose relevant unresolved operations or support lookup by retained broker
identity.

### Failure and adversarial behavior

A lost reply followed by view replacement otherwise invites a fresh operation for
the same click. Replaying raw input is unsafe because its target, context and intent
may have changed. A hostile view can propose different parameters than those
confirmed; the protected ceremony and sink must bind the same digest.

### Alternatives and unresolved tradeoffs

Client-only request IDs are insufficient when the client can lose all state. Broker
retention plus durable application admission adds storage but closes that gap.
Headless automation uses its own scoped intent identity, not forged human focus
evidence.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash the view after admission but before the operation ID returns; a new view must locate the original operation.
- Replay an old gesture against a new session or changed target revision; require current intent and authorization rather than automatic mutation.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Effect reconciliation and unqueryable repair](../external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
2. [WAI-ARIA 1.2](../../../30-sources/w3c-2023-wai-aria-1-2.md).
