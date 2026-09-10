---
title: "Admission, overload, and service-resource governance: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Admission, overload, and service-resource governance: internal services

## Purpose

Separate causal accounting, pressure-based admission, queue-credit conservation and
bounded retry/recovery feedback.

This directory decomposes [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance.md).
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

- [Causal resource accounts and fanout reservations](causal-resource-accounts-and-fanout-reservations.md) — How does asynchronous work remain charged to an authenticated owner?
- [Pressure observation, fair admission, and degradation](pressure-observation-fair-admission-and-degradation.md) — How can the system reject excess demand without confusing overload with service failure?
- [Queue age, credit return, and backlog isolation](queue-age-credit-return-and-backlog-isolation.md) — How can backlog recovery preserve fresh work without silently discarding accepted obligations?
- [Retry circuits, recovery reserve, and feedback stability](retry-circuit-recovery-reserve-and-feedback-stability.md) — How can retries and restarts avoid multiplying load across a dependency graph?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
