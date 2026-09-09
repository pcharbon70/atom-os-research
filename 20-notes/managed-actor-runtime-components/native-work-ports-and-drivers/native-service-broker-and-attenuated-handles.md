---
title: "Native service broker and attenuated handles"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Native service broker and attenuated handles

This study decomposes [Native work, ports and drivers](../native-work-ports-and-drivers.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

A hosted runtime's native interfaces carry dependencies beyond an ABI; ownership queues do not themselves authenticate or authorize a service. [1](../../../30-sources/haecki-et-al-2019-cleanq.md), [2](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Protected service domains are the default native boundary. Regular and dirty NIFs remain inside the runtime memory-failure domain.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a broker table of runtime-epoch/slot/generation handles, allowed operation sets, service incarnations and admission credits. An actor handle designates a mediated service; it contains no raw endpoint selector, file descriptor or arbitrary executable path.

### Admission, transitions and completion

Resolve requests through policy, obtain the narrowly required service grant, reserve handle metadata and publish only after the session is usable. Delegation is explicit and cannot widen rights. Restart invalidates or explicitly rebinds handles under a new generation after policy checks.

### Failure and adversarial behavior

Guessing a table slot, copying handle bits or presenting a stale service incarnation must not acquire authority. A broker accepting an arbitrary shell command would recreate ambient host authority. Compromise of the broker within the runtime exposes its held grants, so high-consequence services need separate domains.

### Alternatives and unresolved tradeoffs

One broker simplifies auditing but can concentrate authority and contention. Separate service-class brokers reduce correlated failure at a crossing/metadata cost. Keep actor-facing protocol stable while partitioning deployment.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Attempt rights escalation through handle copying and operation substitution.
- Restart a service while opening a handle and prohibit silent stale rebinding.
- Inventory all adapter grants reachable through each broker class.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [I/O ownership and terminal completion](../timers-events-and-asynchronous-io-integration/asynchronous-operation-records-and-buffer-completion.md) — a contract this service must compose with.
- [Failure projection without unsafe retry](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md).
2. [Pinned OTP 29.0.5 source audit](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).
