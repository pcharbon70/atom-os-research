---
title: "Durable timer meaning and retry budgets"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Durable timer meaning and retry budgets

This study decomposes [Workflows, process managers, timers, and compensation](../workflows-process-managers-timers-and-compensation.md).

Research question: What does a timer firing mean after restart, clock change or delayed delivery?

## Research basis and status

Durable Functions formalizes restricted history replay; arbitrary nondeterminism and external effects remain outside that abstraction. [1](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).

DAGOR propagates admission priorities through request paths; its empirical policy is neither a hard resource ceiling nor universal fairness. [2](../../../30-sources/zhou-et-al-2018-dagor.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own logical deadline, timer generation, expected workflow state and revision,
lateness policy, retry budget and next eligible action. Layer 4 schedules durable
timers; Layer 3 delivers transient timer events. A clock observation is not itself a
business transition.

### Admission, transitions and completion

Commit timer intent with the state that creates it. On delivery validate identity,
generation and still-applicable condition; commit the resulting transition before
scheduling its successor. Retry attempts consume one retained budget with bounded
backoff and fan-out. Restarts do not renew the budget. Specify whether deadlines are
calendar-based or elapsed durations and what reboot uncertainty permits.

### Failure and adversarial behavior

A canceled timer can still arrive. Clock rollback can duplicate eligibility; clock
jumps can expire many timers simultaneously. A deadline passed after an external
step was accepted cannot prove noncommit. Preserve pending state and reconcile
rather than treating timeout as a universal abort.

### Alternatives and unresolved tradeoffs

Periodic polling simplifies the delivery substrate but increases scan cost and
expiry latency. Dedicated durable timers improve precision while adding metadata.
Neither gives a hard response bound without reserved execution capacity and a
qualified clock model.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Restart across clock discontinuities and deliver every timer twice; at most one applicable transition commits.
- Exhaust retry budget then restart repeatedly; no new attempts may be minted, while authorized status lookup remains possible.

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
2. [DAGOR](../../../30-sources/zhou-et-al-2018-dagor.md).
