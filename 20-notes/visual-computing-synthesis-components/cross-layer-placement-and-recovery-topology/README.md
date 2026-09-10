---
title: "Cross-layer placement and recovery topology: internal services"
kind: map
created: "2026-09-10"
tags:
  - fault-tolerance
  - system-architecture
  - visual-computing
aliases: []
---

# Cross-layer placement and recovery topology: internal services

## Purpose

Separate layer ownership, end-to-end fencing, recovery boot paths, restart
groups, and reserved-resource policy.

This directory decomposes [Cross-layer placement and recovery topology](../cross-layer-placement-and-recovery-topology.md).

## What belongs here

Keep placement arguments, dependency cuts, recovery authority, resource
profiles, failure cases, and unexecuted topology tests here. Trust does not by
itself justify kernel placement. The [session
manifest](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md)
records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Layer ownership, service domains, and trust boundaries](layer-ownership-service-domains-and-trust-boundaries.md) — Which layer can enforce each visual-computing guarantee?
- [Generation propagation, fencing, and revocation](generation-propagation-fencing-and-revocation.md) — How do restarted layers reject stale cross-domain resources and messages?
- [Headless boot, dependency cuts, and recovery console](headless-boot-dependency-cuts-and-recovery-console.md) — What minimum path restores control without depending on the failed desktop?
- [Restart groups, compositor recovery, and state reconstruction](restart-groups-compositor-recovery-and-state-reconstruction.md) — Which services restart together and which truth must survive them?
- [Resource reserve, overload, and fault containment](resource-reserve-overload-and-fault-containment.md) — How does recovery remain possible when presentation exhausts resources?

## Maintaining this index

Inventory every direct child and keep layer maps, parent reports, and recovery
assumptions connected. Revisit placement when measured dependency or trust
evidence changes.
