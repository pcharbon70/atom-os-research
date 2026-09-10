---
title: "Behaviour engines and capability-gated management: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Behaviour engines and capability-gated management: internal services

## Purpose

Distinguish serialized requests, state-machine scheduling, event delivery,
cooperative management and callback evolution.

This directory decomposes [Behaviour engines and capability-gated management](../behaviour-engines-and-capability-gated-management.md).
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

- [Serialized calls and outcome correlation](serialized-calls-and-outcome-correlation.md) — Which operation state survives a caller timeout or late reply?
- [State-machine events, postponement, and timer generations](state-machine-events-postponement-and-timer-generations.md) — How can state-machine features remain bounded without claiming invisible OTP compatibility?
- [Event-router subscriber isolation and delivery classes](event-router-subscriber-isolation-and-delivery-classes.md) — What does event publication mean when subscribers have different failure and loss contracts?
- [Management facets, suspension, and outer termination](management-facets-suspension-and-outer-termination.md) — How can management remain useful without becoming unrestricted inspection or relying on cooperation for containment?
- [Callback transition and compatibility trace boundaries](callback-transition-and-compatibility-trace-boundaries.md) — Which evidence is needed before replacing an engine callback and its state schema?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
