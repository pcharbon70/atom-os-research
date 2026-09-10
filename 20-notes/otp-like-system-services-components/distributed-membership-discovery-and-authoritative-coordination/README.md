---
title: "Distributed membership, discovery, and authoritative coordination: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Distributed membership, discovery, and authoritative coordination: internal services

## Purpose

Separate observer health, replay-resistant membership, quorum metadata and
effect-sink ownership.

This directory decomposes [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination.md).
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

- [Observer health and adaptive failure suspicion](observer-health-and-adaptive-failure-suspicion.md) — How can a slow failure detector avoid blaming healthy peers?
- [Membership epochs, tombstones, and federated candidates](membership-epochs-tombstones-and-federated-candidates.md) — How can delayed advertisements remain harmless across reboot, removal and cell boundaries?
- [Quorum metadata, reconfiguration, and disaster recovery](quorum-metadata-reconfiguration-and-disaster-recovery.md) — Which durable assumptions preserve one authoritative control history?
- [Lease jeopardy and effect-sink fence installation](lease-jeopardy-and-effect-sink-fence-installation.md) — When is a successor entitled to perform effects that an old owner may still attempt?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
