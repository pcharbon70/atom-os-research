---
title: "Workflow definitions and durable control state"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Workflow definitions and durable control state

This study decomposes [Workflows, process managers, timers, and compensation](../workflows-process-managers-timers-and-compensation.md).

Research question: What survives when the actor coordinating a long use case disappears?

## Research basis and status

Durable Functions formalizes restricted history replay; arbitrary nondeterminism and external effects remain outside that abstraction. [1](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).

Workflow Patterns distinguishes branch, join and cancellation semantics; it does not provide durable effect execution. [2](../../../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own stable workflow identity, pinned definition generation, revision, current state,
initiating subject reference, participants and outstanding responsibilities.
Business-tenant identity is durable; current security-realm and grant bindings are
reacquired. Never use a saved PID or code pointer as the workflow definition.

### Admission, transitions and completion

Atomically accept a workflow and its first intent, then drive explicit transitions
from durable inputs. Each transition records the expected workflow revision and
definition. Recovery loads the same state machine and reconciles unresolved steps
before dispatching new work. A runtime supervisor restores execution; it does not
decide whether a business obligation is complete.

### Failure and adversarial behavior

Code deletion can strand a perfectly intact workflow journal. Replaying with a
changed branch condition may skip compensation or repeat a prior effect. Bound
history and checkpoint cost; continuation-as-new must preserve operation lineage and
pending obligations rather than resetting their identity.

### Alternatives and unresolved tradeoffs

Explicit state machines provide inspectable recovery at the cost of more declared
states. Replay-based orchestration reduces boilerplate but requires a stricter
deterministic programming profile. Choreography is suitable where independent
consumers genuinely own independent work, not where it hides a global obligation.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Kill the coordinator after each state transition and recover the same participant and operation identities.
- Remove an old definition while it has live instances; retention or quarantine must prevent reinterpretation under current code.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Effect reconciliation and unqueryable repair](../external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Durable Functions semantics](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).
2. [Workflow Patterns](../../../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md).
