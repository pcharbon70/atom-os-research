---
title: "Telemetry redaction and evidence-channel separation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Telemetry redaction and evidence-channel separation

This study decomposes [Semantic observability, testing, and assurance](../semantic-observability-testing-and-assurance.md).

Research question: How can operators diagnose failures without treating diagnostics as authority or exposing domain secrets?

## Research basis and status

Google SRE guidance starts indicators from user-relevant behavior and explicit measurement populations, not process uptime alone. [1](../../../30-sources/jones-et-al-2016-service-level-objectives.md).

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs. [2](../../../30-sources/bittau-et-al-2008-wedge.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own domain-specific diagnostic fields, redaction rules, sampling expectations and
links to protected outcome or audit records. Metrics, traces, logs, crash evidence,
audit and operation truth have separate retention and completeness contracts. Trace
IDs are untrusted correlation hints.

### Admission, transitions and completion

Validate or replace external trace context, apply current scope and redaction
policy, enforce cardinality and byte budgets, then publish through narrow diagnostic
facets. A tool seeking detailed operation evidence must perform a separately
authorized lookup. Recovery and audit capacity are reserved independently from
verbose debugging.

### Failure and adversarial behavior

A log line saying committed can be emitted before storage succeeds or forged by
compromised code. Missing telemetry cannot negate a durable receipt. Heap dumps can
expose secrets outside a tenant's intended scope. Redaction itself must be tested
across error paths and old schema readers.

### Alternatives and unresolved tradeoffs

Rich tracing speeds diagnosis but increases cost and disclosure. Minimal counters
reduce exposure but may make ambiguous effects hard to investigate. Preserve the
smallest durable accountability record needed for the domain and use sampled
diagnostics for performance exploration.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Inject secret-bearing malformed requests and crashes; inspect every diagnostic channel for unauthorized disclosure.
- Forge and drop trace spans while querying the outcome ledger; semantic truth must remain independent of trace contents.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Semantic admission classes and protected recovery reserve](../cross-layer-placement-tenancy-overload-and-recovery-topology/semantic-admission-classes-and-protected-recovery-reserve.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Service Level Objectives](../../../30-sources/jones-et-al-2016-service-level-objectives.md).
2. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
