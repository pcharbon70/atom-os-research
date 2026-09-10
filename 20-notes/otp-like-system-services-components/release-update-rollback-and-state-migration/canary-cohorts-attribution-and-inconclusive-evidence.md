---
title: "Canary cohorts, attribution, and inconclusive evidence"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Canary cohorts, attribution, and inconclusive evidence

This study decomposes [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration.md).

Research question: What observation is strong enough to expand a release without mistaking missing or biased data for success?

## Research basis and status

Google's canary guidance stresses representative attributed metrics; sampled traces
cannot establish complete outcome coverage. [1](../../../30-sources/warner-davidovic-2018-canarying-releases.md) [2](../../../30-sources/sigelman-et-al-2010-dapper.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The canary controller owns cohort assignment, version labels, exposure budget,
decision rules, observation window and evidence completeness. Effect sinks enforce
cohort/resource scope. A shadow candidate has no external-effect authority unless a
separately safe protocol permits it.

### Admission, transitions and completion

Define metrics and decision criteria before exposure. Compare contemporaneous
candidate/control behavior with absolute service invariants, stratified by relevant
workload classes. Keep attribution through complete asynchronous work units. Emit
Pass, Fail or Inconclusive; insufficient traffic, missing telemetry or overlapping
experiments cannot become Pass.

### Failure and adversarial behavior

Aggregate metrics can conceal severe minority failures; shared dependencies can
contaminate both cohorts. A canary that passes cannot prove absence of rare security
faults or guarantee rollback. Stop further expansion when scope, resource reserve or
observation quality is violated.

### Alternatives and unresolved tradeoffs

Fixed-duration observation is predictable but may lack representative samples.
Sequential decisions need a declared statistical method and error control. This
study identifies those requirements without choosing a universal significance
threshold or claiming the cited chapter supplies a full statistical proof.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Suppress candidate telemetry while control remains healthy; the gate must become Inconclusive, not green.
- Inject a fault affecting a small workload class and verify cohort/stratum metrics expose it before expanding authority.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Canarying releases](../../../30-sources/warner-davidovic-2018-canarying-releases.md).
2. [Dapper](../../../30-sources/sigelman-et-al-2010-dapper.md).
