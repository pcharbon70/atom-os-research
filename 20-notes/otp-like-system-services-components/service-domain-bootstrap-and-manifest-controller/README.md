---
title: "Service-domain bootstrap and manifest controller: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Service-domain bootstrap and manifest controller: internal services

## Purpose

Separate pure desired-state compilation, constrained preparation, public selection
and recovery of the controller itself.

This directory decomposes [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller.md).
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

- [Bounded manifest decoding and plan normalization](bounded-manifest-decoding-and-plan-normalization.md) — How can service desired state be interpreted without acquiring authority or producing partial effects?
- [Service-envelope reservation and private preparation](service-envelope-reservation-and-private-preparation.md) — How are resources and authority reserved without making preparation a second root of privilege?
- [Generation publication and reconciliation](generation-publication-and-reconciliation.md) — What does one public generation switch guarantee when services continue executing independently?
- [Controller replacement and bootstrap dependency cuts](controller-replacement-and-bootstrap-dependency-cuts.md) — How can the service controller be replaced when its normal storage, naming or identity dependencies are unavailable?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
