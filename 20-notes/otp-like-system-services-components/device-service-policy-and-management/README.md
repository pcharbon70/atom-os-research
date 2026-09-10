---
title: "Device-service policy and management: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Device-service policy and management: internal services

## Purpose

Separate inventory/reset scope, client virtualization, issue outcomes and safe
replacement.

This directory decomposes [Device-service policy and management](../device-service-policy-and-management.md).
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

- [Device inventory, reset domains, and driver admission](device-inventory-reset-domains-and-driver-admission.md) — Which hardware resources can actually be managed and reset independently?
- [Class virtualization, queue credits, and buffer custody](class-virtualization-queue-credits-and-buffer-custody.md) — How can untrusted clients share I/O without forging descriptors or duplicating buffer ownership?
- [Issue intent, completion proof, and device outcomes](issue-intent-completion-proof-and-device-outcomes.md) — What can software honestly conclude after a driver crashes near a hardware command?
- [Device fencing, reset, and quarantine release](device-fencing-reset-and-quarantine-release.md) — When is old device activity unable to corrupt a replacement's resources?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
