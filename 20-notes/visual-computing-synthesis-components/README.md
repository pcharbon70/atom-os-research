---
title: "Visual Computing Synthesis Components"
kind: map
created: "2026-09-04"
tags:
  - directory-index
  - human-computer-interaction
  - visual-computing
aliases:
  - "Atom OS visual-computing component reports"
---

# Visual Computing Synthesis Components

## Purpose

This directory contains the detailed implementation research for the seven
aspects of the Atom OS visual-computing synthesis proposed in [Alan Kay's
Smalltalk visual interface and the modern
desktop](../alan-kay-smalltalk-visual-interface-and-modern-desktop.md). Each
report turns one design direction into explicit objects, protocols, layer
placements, authority and failure boundaries, implementation stages, and
falsifiable experiments.

## What belongs here

Put component-level visual-computing syntheses here when they preserve a clear
connection to the existing hardware, privileged-kernel, managed-runtime,
OTP-like service, and application boundaries. Broad historical comparison
belongs in the parent synthesis; source-specific evidence belongs in
`30-sources`.

## Index

### Subdirectories

- None yet.

### Documents

- [User-owned project graph and composition](user-owned-project-graph-and-composition.md) —
  defines the durable unit of work, graph schema, provider composition,
  collaboration, ownership, and persistence boundary.
- [Durable semantic actors and disposable presentation](durable-semantic-actors-and-disposable-presentation.md) —
  separates application meaning from semantic views, renderer caches,
  compositor state, and recoverable surface leases.
- [Semantics-first accessible UI protocol](semantics-first-accessible-ui-protocol.md) —
  specifies a native semantic record and ordered update protocol shared by
  visual, assistive, automation, and remote projections.
- [Input, focus, and trusted-interaction authority](input-focus-and-trusted-interaction-authority.md) —
  treats user interaction as authenticated, short-lived, generation-bound
  authority rather than ambient access.
- [Capability-scoped live tools and transactional evolution](capability-scoped-live-tools-and-transactional-evolution.md) —
  confines inspection, evaluation, tracing, editing, migration, publication,
  rollback, and reusable-tool release.
- [Cross-layer placement and recovery topology](cross-layer-placement-and-recovery-topology.md) —
  assigns every visual-computing mechanism and policy to the existing Atom OS
  architecture and defines its failure and restart dependencies.
- [Plural representations and cross-view consistency](plural-representations-and-cross-view-consistency.md) —
  supports coexisting visual, textual, programmatic, voice, assistive, and
  remote views without making any one projection authoritative.

## Maintaining this index

Index every direct report, update the parent note and visual-computing map when
a component changes, and preserve the distinction between source evidence,
proposed architecture, and behavior demonstrated by a prototype. Use Mermaid
for architecture and state diagrams.
