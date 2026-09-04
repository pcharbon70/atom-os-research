---
title: "OTP-like system services components"
kind: map
created: "2026-09-04"
tags:
  - archive-navigation
  - directory-index
  - otp
  - service-management
aliases:
  - "System services component index"
---

# OTP-like system services components

## Purpose

This directory contains the detailed evidence and implementation syntheses for
the thirteen unprivileged policy components proposed by the
[OTP-like system services layer](../otp-like-system-services-layer.md).

## What belongs here

Put one component-scale synthesis here when it refines a service-layer
responsibility into explicit objects, authority, lifecycle, recovery,
overload, security, implementation, and verification contracts. Keep source
analysis in `30-sources`, active questions in `40-inquiries`, and dated research
evidence in `50-journal`.

## Index

### Subdirectories

- None yet.

### Documents

- [Service-domain bootstrap and manifest controller](service-domain-bootstrap-and-manifest-controller.md) —
  defines validated desired state, capability and resource reservation,
  private preparation, generation publication, reconciliation, and independent
  recovery of the service root.
- [Behaviour engines and capability-gated management](behaviour-engines-and-capability-gated-management.md) —
  separates reusable OTP-compatible protocol engines from callbacks and adds
  bounded, capability-scoped inspection, suspension, replacement, and
  termination.
- [Supervision and recovery policy](supervision-and-recovery-policy.md) —
  combines hierarchical OTP restart policy with typed evidence, recovery
  budgets, backoff, protected reserve, recovered-state gates, and escalation.
- [Application lifecycle and dependency orchestration](application-lifecycle-and-dependency-orchestration.md) —
  models dependency validation, preparation, readiness, atomic publication,
  drain, ordered stop, rollback, and explicit external-effect limits.
- [Naming, registry, and local discovery](naming-registry-and-local-discovery.md) —
  provides stable names, incarnation-aware handles, atomic snapshot/watch,
  bounded caches, sharding, and separate unique-binding and eventual-group
  semantics.
- [Configuration, workload identity, and secrets](configuration-workload-identity-and-secrets.md) —
  separates immutable configuration snapshots from short-lived identity and
  secret delivery, with staged adoption, rotation, redaction, and outage
  policy.
- [Durable state, transactions, and outcome recovery](durable-state-transactions-and-outcome-recovery.md) —
  specifies a small WAL/checkpoint substrate, explicit commit and crash states,
  durable request outcomes, idempotent recovery, retention, and compensation.
- [Device-service policy and management](device-service-policy-and-management.md) —
  governs isolated drivers through generation-bound sessions, finite queues,
  reset/fence policy, completion ledgers, replacement, and quarantine.
- [Network endpoint and protocol services](network-endpoint-and-protocol-services.md) —
  defines capability-scoped endpoints, isolated protocol engines,
  authenticated sessions, finite flow control, reconnect, and honest remote
  outcome semantics.
- [Distributed membership, discovery, and authoritative coordination](distributed-membership-discovery-and-authoritative-coordination.md) —
  separates weak observation from quorum-backed metadata, then binds leases
  and monotonically increasing fences to every exclusive effect sink.
- [Release, update, rollback, and state migration](release-update-rollback-and-state-migration.md) —
  authenticates immutable release graphs and stages compatibility, canary,
  quiescence, shadow migration, atomic activation, rollback, and commit.
- [Admission, overload, and service-resource governance](admission-overload-and-service-resource-governance.md) —
  coordinates finite queues, deadlines, quotas, fairness, backpressure,
  shedding, retry budgets, degradation, and protected control/recovery
  reserves.
- [Observability, audit, alarms, and operator control](observability-audit-alarms-and-operator-control.md) —
  separates lossy telemetry, bounded crash evidence, persistent alarms,
  tamper-evident audit, and least-authority operator actions while preserving
  causal correlation.

## Maintaining this index

Index every direct component report and keep its description aligned with the
integrated layer. When a component boundary changes, update this index, the
parent notes index, the topic map, the inquiry, and every meaningful incoming
body link in the same change.
