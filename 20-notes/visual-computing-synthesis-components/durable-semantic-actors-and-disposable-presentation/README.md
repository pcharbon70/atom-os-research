---
title: "Durable semantic actors and disposable presentation: internal services"
kind: map
created: "2026-09-10"
tags:
  - actor-model
  - fault-tolerance
  - visual-computing
aliases: []
---

# Durable semantic actors and disposable presentation: internal services

## Purpose

Separate durable model activation, semantic publication, rendering leases, and
bounded presentation reconstruction.

This directory decomposes [Durable semantic actors and disposable presentation](../durable-semantic-actors-and-disposable-presentation.md).
These are logical responsibilities, not a process-count prescription.

## What belongs here

Keep state ownership, transition protocols, failure boundaries, alternatives,
and unexecuted falsifiers here. Presentation mechanisms remain unprivileged and
recoverable; this research does not claim an implementation. The [session
manifest](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md)
records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Model activation, durable identity, and effect outcomes](model-activation-durable-identity-and-effect-outcomes.md) — How does one logical model survive actor replacement without duplicating effects?
- [Semantic observation and view-generation publication](semantic-observation-and-view-generation-publication.md) — How is current meaning published without making a view authoritative?
- [Renderer, surface, buffer, and device leases](renderer-surface-buffer-and-device-leases.md) — Which presentation resources are disposable, and who proves their release?
- [Restart, resynchronization, and presentation backpressure](restart-resynchronization-and-presentation-backpressure.md) — How does a replacement presentation become current under loss and overload?

## Maintaining this index

Inventory every direct child and keep the parent, component index, map, and
inquiry connected. Adjust decomposition only when state or trust boundaries
require it; no document count is normative.
