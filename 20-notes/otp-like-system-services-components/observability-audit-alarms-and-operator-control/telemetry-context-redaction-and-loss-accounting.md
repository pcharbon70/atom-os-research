---
title: "Telemetry context, redaction, and loss accounting"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Telemetry context, redaction, and loss accounting

This study decomposes [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control.md).

Research question: How can causal diagnostics remain useful while explicitly incomplete and untrusted?

## Research basis and status

Dapper samples correlated traces and excludes payloads by default; bounded emission
needs explicit loss policy. [1](../../../30-sources/sigelman-et-al-2010-dapper.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The telemetry service owns schemas, sampling, bounded cardinality, redaction, export
queues and drop summaries. Trace IDs are correlation data, not authentication,
priority or permission. Resource accounts and trusted producer identity are
independently bound.

### Admission, transitions and completion

Project allowed fields before export and normalize remote context into an
authenticated local envelope with optional causal links. Separate queue wait,
execution, dependency wait and reconciliation spans. Charge instrumentation and
export; use preallocated or bounded nonblocking emission on critical paths.

### Failure and adversarial behavior

A stalled exporter must not block recovery. High-cardinality labels and
secret-bearing baggage can exhaust or disclose state even when payloads are absent.
Dropped or sampled events prevent complete-history claims; record sampling and loss
metadata outside the saturated detailed path.

### Alternatives and unresolved tradeoffs

Head sampling is cheap but misses rare failures; richer tail decisions retain more
data and need finite windows. Durable audit must use a separate protocol.
Cross-machine timestamp ordering requires clock uncertainty, not visual sorting
alone.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Stall exporters and inject unique attacker-controlled labels; producer cost and retained memory must remain bounded.
- Send forged trace priority and secret baggage; neither may alter authority or escape through the approved export schema.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets/README.md) — supplies configuration adoption and credential-generation evidence.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Dapper](../../../30-sources/sigelman-et-al-2010-dapper.md).
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
