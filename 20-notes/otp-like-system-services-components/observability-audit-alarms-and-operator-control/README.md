---
title: "Observability, audit, alarms, and operator control: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Observability, audit, alarms, and operator control: internal services

## Purpose

Separate lossy telemetry, retained crash facts, persistent alarm state,
integrity-protected audit and bounded operator/probe authority.

This directory decomposes [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control.md).
These are logical responsibilities, not a requirement for one process per study.

## What belongs here

Keep owned state, authority, transition evidence, failure cases, alternatives
and unexecuted verification obligations here. This is full-system Layer 4
architecture research, not a PoC, QEMU profile or implementation plan. Layers
2–3 supply enforcement and managed execution; Layer 5 supplies domain meaning.
The [session manifest](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Telemetry context, redaction, and loss accounting](telemetry-context-redaction-and-loss-accounting.md) — How can causal diagnostics remain useful while explicitly incomplete and untrusted?
- [Crash-capsule custody and evidence retention](crash-capsule-custody-and-evidence-retention.md) — What evidence can survive a failed runtime without trusting its normal logger?
- [Persistent alarm state, acknowledgement, and clearance](persistent-alarm-state-acknowledgement-and-clearance.md) — How can operators acknowledge an incident without erasing an unresolved condition?
- [Audit intent/outcome integrity and witness progress](audit-intent-outcome-integrity-and-witness-progress.md) — Which tampering and omission can a security audit trail actually detect?
- [Operator-action facets, probe bounds, and break-glass](operator-action-facets-probe-bounds-and-break-glass.md) — How can recovery tooling remain powerful without becoming permanent ambient privilege?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
