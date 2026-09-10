---
title: "User-owned project graph and composition: internal services"
kind: map
created: "2026-09-10"
tags:
  - project-graph
  - visual-computing
  - service-architecture
aliases: []
---

# User-owned project graph and composition: internal services

## Purpose

Separate durable project truth, provider composition, authority rehydration,
replication policy, and portable recovery.

This directory decomposes [User-owned project graph and composition](../user-owned-project-graph-and-composition.md).
These are logical responsibilities, not a requirement for one process per study.

## What belongs here

Keep owned state, authority, transition evidence, failure cases, alternatives,
and unexecuted verification obligations here. This is full-system visual-
computing architecture research, not PoC scope or an implementation plan. The
[session manifest](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md)
records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Project manifest, object identity, and history](project-manifest-object-identity-and-history.md) — What durable record preserves meaning without persisting live execution identity?
- [Provider discovery, binding, and schema negotiation](provider-discovery-binding-and-schema-negotiation.md) — How can replaceable providers attach without monopolizing data interpretation?
- [Authority intent, rehydration, and revocation](authority-intent-rehydration-and-revocation.md) — How can durable delegation intent yield only current attenuated authority?
- [Collaboration, replica membership, and conflict](collaboration-replica-membership-and-conflict.md) — Which state may converge, and which decisions require fenced authority?
- [Export, import, retention, and recovery](export-import-retention-and-recovery.md) — What makes a project portable and recoverable when providers or machines disappear?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map, and inquiry connected when responsibilities change. Decompose according
to distinct state, authority, and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
