---
title: "OpenTelemetry specification 1.60.0"
kind: source
created: "2026-09-04"
authors:
  - "OpenTelemetry Project"
published: 2025
citation_key: "opentelemetry-project-2026-specification-1-60"
container: "Cloud Native Computing Foundation"
edition: "OpenTelemetry specification 1.60.0; OTLP 1.11.0"
isbn: null
doi: null
url: "https://opentelemetry.io/docs/specs/otel/"
accessed: "2026-09-04"
tags:
  - metrics
  - observability
  - telemetry
  - tracing
aliases:
  - "OpenTelemetry 1.60.0"
  - "OTel specification"
---

# OpenTelemetry specification 1.60.0

## Reference

OpenTelemetry Project. “[OpenTelemetry Specification
1.60.0](https://opentelemetry.io/docs/specs/otel/).” Cloud Native Computing
Foundation, accessed 2026-09-04. The reading set included the
[overview](https://opentelemetry.io/docs/specs/otel/overview/),
[performance and blocking
rules](https://opentelemetry.io/docs/specs/otel/performance/),
[tracing SDK](https://opentelemetry.io/docs/specs/otel/trace/sdk/),
[metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/),
and [logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/).
The rendered specification index identifies OpenTelemetry 1.60.0 and OTLP
1.11.0.

## Research question or contribution

OpenTelemetry defines cross-language APIs, SDK behavior, data models,
propagation, processing, and export for traces, metrics, and logs. For Atom OS,
the key contribution is not one backend format but an explicit separation of
signals, correlation context, sampling, finite collection limits, and exporter
behavior under overload.

## Method

This is a normative interoperability specification assembled by an open
standards project. The selected sections were read for stable data-model fields,
resource and trace correlation, signal-specific limits, sampling, batching,
drop behavior, blocking, and shutdown. Status labels were retained: different
parts of the specification can be stable, mixed, or under development. No SDK
implementation was benchmarked or audited.

## Findings

- Traces, metrics, and logs share resource and instrumentation-scope context
  but retain distinct data models. Logs can carry trace and span identifiers,
  enabling correlation without pretending every log record is a span.
- Sampling is an explicit information-loss decision. A span can be dropped,
  recorded without export, or recorded and sampled; exporters and downstream
  analysis must not infer that an absent span proves an event did not occur.
- SDKs may cap attributes, events, and links and must expose dropped counts for
  relevant entities. The standard batch span processor uses a finite queue;
  once full, new spans are dropped rather than allocating unbounded memory.
- The performance rules say telemetry APIs should not block application work
  by default or consume unbounded memory. Where preserving every record would
  conflict with nonblocking operation, implementations should expose policy,
  thresholds, warnings, and useful loss measurements.
- Explicit flush and shutdown may block to reduce information loss and should
  have configurable timeouts. Operational control paths therefore require
  different budgets from ordinary emission.
- Metric streams include temporality and reset/gap semantics. A counter value
  without its start time, reset information, and writer identity can be
  misleading after service restart or failover.

## Relevance

Atom OS can use a small OTel-compatible projection at its export boundary while
keeping native evidence generation simpler. Every service-domain incarnation
should supply stable service identity, actor or operation correlation, boot and
configuration generations, and explicit loss counters. High-volume telemetry
uses finite per-domain buffers, sampling, aggregation, and bounded exporters;
it must remain unable to exhaust the service it observes.

The specification also demonstrates why telemetry cannot double as the
security audit ledger. Sampling and full-queue drops are legitimate telemetry
behaviors. Audit intent, effect, and outcome records instead require a separate
admission, durability, integrity, export, and failure policy. Correlation IDs
may connect the two planes without equalizing their guarantees.

## Limits

OpenTelemetry standardizes interfaces and data, not the truth or completeness
of instrumentation. It does not prove bounded execution time, durable export,
tamper evidence, clock correctness, low cardinality, or safe operator actions.
Resource and attribute data can leak secrets if producers fail to classify it.
The specification is living and contains sections with different stability
levels; an Atom OS compatibility profile must pin exact signal and protocol
versions rather than claim generic compatibility.

## Derived work

- [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
