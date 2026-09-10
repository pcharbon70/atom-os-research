---
title: "Model activation, durable identity, and effect outcomes"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - actor-model
  - persistence
  - visual-computing
aliases: []
---

# Model activation, durable identity, and effect outcomes

This study decomposes [Durable semantic actors and disposable presentation](../durable-semantic-actors-and-disposable-presentation.md).

Research question: How can one logical model survive actor replacement without
replaying commands or confusing activation identity with durable identity?

## Research basis and status

Orleans demonstrates stable logical actors over replaceable activations. RPC
research establishes reply-loss ambiguity, while RIFL supplies durable request
identity and result lookup in a defined distributed model.
[1](../../../30-sources/bernstein-et-al-2014-orleans.md)
[2](../../../30-sources/birrell-nelson-1984-remote-procedure-calls.md)
[3](../../../30-sources/lee-et-al-2015-rifl.md)

The Atom OS activation and effect protocol remains unimplemented.

## Development

### Owned state and trust boundary

The model service owns logical object identity, lifecycle generation, state
revision, command admission, domain invariants, and durable operation outcomes.
The runtime owns an activation ID and execution resources. Views know a logical
reference and current revision, never a PID or mailbox address as durable
meaning.

### Admission, transitions, and completion

Activation loads one committed object frontier, acquires fenced ownership, and
publishes readiness only after recovery completes. A command is durably bound
to an operation ID before effects. Replacement reconciles pending IDs and
advances activation generation; replies from the predecessor cannot complete a
successor's operation without matching durable evidence.

### Failure and adversarial behavior

Duplicate messages, lost replies, split ownership, stale activation caches, and
external effects during crash are explicit states. Sink-side fencing prevents
old activations from committing; indeterminate effects remain queryable or
quarantined. Presentation never infers completion from a frame or actor death.

### Alternatives and unresolved tradeoffs

Persisting every mailbox simplifies replay but can repeat effects and preserve
obsolete work. Stateless recreation loses in-flight outcomes. Durable command
identity plus selective model state is preferred; retention duration and
external-sink reconciliation profiles remain open.

## Verification obligations

- Crash before and after admission, state commit, external effect, result
  persistence, and reply; reconcile each operation to one honest outcome.
- Run two activations concurrently and prove fencing permits at most one
  current mutation lineage.
- Reuse runtime identifiers and mailboxes; stale commands must not target the
  new lifecycle.

## Connections

- [Internal-service index](README.md) — sibling presentation responsibilities.
- [Project identity and history](../user-owned-project-graph-and-composition/project-manifest-object-identity-and-history.md) — durable graph context.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence boundary.

## Sources

1. [Orleans](../../../30-sources/bernstein-et-al-2014-orleans.md).
2. [Implementing remote procedure calls](../../../30-sources/birrell-nelson-1984-remote-procedure-calls.md).
3. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
