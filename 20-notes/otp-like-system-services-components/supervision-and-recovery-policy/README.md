---
title: "Supervision and recovery policy: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Supervision and recovery policy: internal services

## Purpose

Separate evidence classification, restart admission, state recovery and escalation
outside the failed subtree.

This directory decomposes [Supervision and recovery policy](../supervision-and-recovery-policy.md).
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

- [Failure evidence and recovery-scope selection](failure-evidence-and-recovery-scope-selection.md) — When does an observation justify restarting an actor, runtime domain or device group?
- [Restart budget, reserve, and cooldown controller](restart-budget-reserve-and-cooldown-controller.md) — How can many legal restart policies coexist without exhausting recovery capacity?
- [Fence, settle, recover, and successor readiness](fence-settle-recover-and-successor-readiness.md) — What distinguishes a restarted process from a recovered service?
- [Quarantine, escalation, and supervisor replacement](quarantine-escalation-and-supervisor-replacement.md) — Who retains responsibility when local recovery cannot safely complete?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
