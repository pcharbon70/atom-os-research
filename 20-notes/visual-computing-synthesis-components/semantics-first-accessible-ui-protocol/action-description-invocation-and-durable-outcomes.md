---
title: "Action description, invocation, and durable outcomes"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - accessibility
  - capability-security
  - semantic-ui
aliases: []
---

# Action description, invocation, and durable outcomes

This study decomposes [Semantics-first accessible UI protocol](../semantics-first-accessible-ui-protocol.md).

Research question: How are discoverable semantic actions separated from
authority, command admission, and durable effect completion?

## Research basis and status

WAI-ARIA and AccessKit associate actions with semantic nodes, while
user-driven access control binds sensitive resource selection to authentic
interaction. RPC and RIFL establish that delivery and outcome are separate
questions across failure.
[1](../../../30-sources/w3c-2023-wai-aria-1-2.md)
[2](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)
[3](../../../30-sources/roesner-et-al-2012-user-driven-access-control.md)
[4](../../../30-sources/lee-et-al-2015-rifl.md)

The common Atom command-outcome profile remains proposed.

## Development

### Owned state and trust boundary

A semantic publisher may advertise action kind, parameter schema, consequence,
confirmation profile, and required capability type. It does not grant that
capability. The interaction broker owns client action identity and evidence;
the domain service owns admission, invariants, operation identity, effects, and
terminal outcome.

### Admission, transitions, and completion

Invocation names target logical identity, lifecycle and state revisions,
action ID, typed arguments, client action ID, and presented authority. The
domain boundary atomically binds effectful work to an operation ID. After
admission, deadline expiry does not authorize retry; clients query the existing
operation until committed, not committed, terminated, or indeterminate.

### Failure and adversarial behavior

Stale semantic trees, replayed gestures, hidden parameter substitution,
duplicate assistive events, and lost replies can misdirect effects. Exact
revision checks, one-use interaction grants, canonical request digests, durable
result retention, and sink-side idempotency/fencing address the declared
profile.

### Alternatives and unresolved tradeoffs

Embedding bearer grants in the tree eases invocation but leaks authority.
Treating every action as ephemeral prevents durable workflows. Descriptor-only
discovery plus separate grant/admission is preferred; safe retention periods
and consequence taxonomy need empirical refinement.

## Verification obligations

- Invoke every action with stale node, object, and policy generations and prove
  no current effect occurs.
- Lose each reply before and after admission and ensure clients reconcile one
  operation rather than retry blindly.
- Run the same task through pointer, keyboard, screen reader, voice, and
  automation clients and compare model outcomes, not event shapes.

## Connections

- [Internal-service index](README.md) — semantic action context.
- [Trusted input services](../input-focus-and-trusted-interaction-authority/README.md) — interaction-derived grants.
- [Model outcomes](../durable-semantic-actors-and-disposable-presentation/model-activation-durable-identity-and-effect-outcomes.md) — durable sink semantics.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence limits.

## Sources

1. [WAI-ARIA 1.2](../../../30-sources/w3c-2023-wai-aria-1-2.md).
2. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
3. [User-driven access control](../../../30-sources/roesner-et-al-2012-user-driven-access-control.md).
4. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
