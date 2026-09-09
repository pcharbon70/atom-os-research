---
title: "Operation identity and honest outcome ledgers"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Operation identity and honest outcome ledgers

This study decomposes [Typed commands, queries, events, and protocol contracts](../typed-commands-queries-events-and-protocol-contracts.md).

Research question: What can a caller safely conclude after a timeout, duplicate request or lost response?

## Research basis and status

Featonby's operational account uses caller request identity, parameter checks and retained results; retention and endpoint participation remain explicit limits. [1](../../../30-sources/featonby-2021-idempotent-apis.md).

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [2](../../../30-sources/lee-et-al-2015-rifl.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the semantic mapping from caller-scoped operation ID and request digest to
durable responsibility and monotone progress. Layer 4 provides the storage
substrate. Outcomes distinguish pre-admission refusal, accepted pending, committed
with named evidence, proven not committed, termination with surviving effects,
fenced and indeterminate.

### Admission, transitions and completion

Bind identity atomically with admission or mutation as the selected transaction
profile requires. The same ID and digest recovers one logical execution; a changed
digest is a conflict. Pending may become committed, not committed or an explicitly
unresolved repair state. A deadline observed after admission is a fact about
usefulness, not proof that execution stopped.

### Failure and adversarial behavior

Deleting a result because it is old permits a delayed retry to duplicate work unless
the protocol can reject its expired identity. Losing the client response also loses
its operation ID unless a recoverable client-action binding exists. Neither an actor
crash nor transport refusal proves a previously accepted effect absent.

### Alternatives and unresolved tradeoffs

Returning a permanently frozen first response is inappropriate when that response
was pending. Returning a new execution for every retry destroys reconciliation.
Select one logical execution with advancing status and a stable terminal meaning;
state precisely how long status can be recovered.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash before and after admission, mutation and response; enumerate permitted outcomes at each point.
- Retry after retention expiry and with changed payload; require safe refusal or retained proof, never implicit new execution.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Semantic port profiles and endpoint qualification](../external-effects-ports-adapters-and-reconciliation/semantic-port-profiles-and-endpoint-qualification.md) — a cross-component contract this service must preserve.
- [Directed compatibility and behavioral fixture matrices](../application-evolution-schema-compatibility-and-migration/directed-compatibility-and-behavioral-fixture-matrices.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Idempotent APIs](../../../30-sources/featonby-2021-idempotent-apis.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
