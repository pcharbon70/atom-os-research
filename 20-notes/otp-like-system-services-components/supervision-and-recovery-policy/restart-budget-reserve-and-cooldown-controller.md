---
title: "Restart budget, reserve, and cooldown controller"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Restart budget, reserve, and cooldown controller

This study decomposes [Supervision and recovery policy](../supervision-and-recovery-policy.md).

Research question: How can many legal restart policies coexist without exhausting recovery capacity?

## Research basis and status

Jitter reduces synchronized contention in Brooker's simulation; it does not reserve
capacity or prove controller stability. [1](../../../30-sources/brooker-2015-exponential-backoff-jitter.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The admission controller owns weighted attempt histories, concurrent-recovery
permits, protected reserve and cooldown state. It meters a complete recovery
attempt, including teardown, replay, preparation and evidence, rather than merely
counting process creation.

### Admission, transitions and completion

Estimate and reserve the attempt's maximum required resources before fencing useful
work. Charge failed private successors as well as public failures. Use bounded
randomized delay and gradual budget restoration only after a stable observation
window. Persist enough history that supervisor restart cannot reset a storm budget.

### Failure and adversarial behavior

Simultaneous sibling failures can each satisfy a local rule while exceeding the
system limit. A parent storm budget and nonborrowable minimum reserve constrain the
aggregate. Clock discontinuity or lost counters must select conservative policy
rather than unlimited immediate retry.

### Alternatives and unresolved tradeoffs

Static reserve costs idle capacity; controlled borrowing needs a reclamation bound
that still permits emergency recovery. OTP restart intensity is a different
compatibility rule; place this native admission outside a strict subtree instead of
modifying its visible semantics.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Fail many unrelated children concurrently and measure peak recovery resources, useful throughput and control latency.
- Restart the supervisor during backoff; attempts must not regain a fresh unlimited budget.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance/README.md) — budgets retained work, retries and recovery.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Exponential backoff and jitter](../../../30-sources/brooker-2015-exponential-backoff-jitter.md).
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
