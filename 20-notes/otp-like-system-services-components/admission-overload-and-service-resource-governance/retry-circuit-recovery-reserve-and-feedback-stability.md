---
title: "Retry circuits, recovery reserve, and feedback stability"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Retry circuits, recovery reserve, and feedback stability

This study decomposes [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance.md).

Research question: How can retries and restarts avoid multiplying load across a dependency graph?

## Research basis and status

Randomized backoff reduces contention, while propagated admission can avoid wasted
paths; neither removes the need for retry budgets. [1](../../../30-sources/brooker-2015-exponential-backoff-jitter.md) [2](../../../30-sources/zhou-et-al-2018-dagor.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The controller owns retry lineage, per-dependency token budgets, circuit state,
probe allowances and a separate supervisor recovery reserve. Request retry and
service replacement are different actions, with different effect and resource
preconditions.

### Admission, transitions and completion

Classify retry safety before spending a token. Preserve logical identity for
deduplicated work and reconcile indeterminate outcomes. Cap backoff by remaining
valid waiting budget; half-open probes are few and authenticated. Restore
concurrency gradually after sustained healthy evidence.

### Failure and adversarial behavior

Independent retries at each hop can multiply one request into a storm. Rebooting a
circuit controller must not reset all budgets. Remote monotonic clocks are
incomparable: without bounded delay/clock conversion, a transmitted timeout is a
per-hop budget, not a proved end-to-end deadline.

### Alternatives and unresolved tradeoffs

Circuits protect resources but can delay recovery or deny rare critical work. Shared
dependency budgets constrain amplification while increasing coordination. Reserve
management must preserve failure-report and fencing capacity during the worst
admitted storm, not just normal traffic.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Fail the last stage of a fanout graph and verify total attempts stay within the original authorized retry lineage.
- Recover briefly then fail again; hysteresis must prevent a synchronized release of all queued retries.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Network endpoint and protocol services](../network-endpoint-and-protocol-services/README.md) — separates transport session state from application outcomes.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Exponential backoff and jitter](../../../30-sources/brooker-2015-exponential-backoff-jitter.md).
2. [DAGOR](../../../30-sources/zhou-et-al-2018-dagor.md).
