---
title: "Applications and domain services components"
kind: map
created: "2026-09-05"
tags:
  - application-architecture
  - archive-navigation
  - directory-index
  - domain-modeling
aliases:
  - "Layer 5 component index"
---

# Applications and domain services components

## Purpose

This directory contains the detailed evidence and implementation syntheses for
the fourteen components proposed by the [applications and domain services
layer](../applications-and-domain-services-layer.md).

## What belongs here

Put one component-scale synthesis here when it refines a Layer 5 responsibility
into explicit semantic, authority, state, protocol, failure, overload,
evolution, recovery, and verification contracts. Keep primary-source analysis
in `30-sources`, active questions in `40-inquiries`, and dated research evidence
in `50-journal`.

## Index

### Subdirectories

- None yet.

### Documents

- [Application manifest, composition, and authority envelope](application-manifest-composition-and-authority-envelope.md) —
  defines the declarative application contract, explicit composition root,
  capability imports, budgets, dependencies, publication participation, and
  the boundary between Layer 5 intent and Layer 4 orchestration.
- [Bounded contexts, domain model, and application services](bounded-contexts-domain-model-and-application-services.md) —
  separates semantic contexts, application use-case coordination, domain
  rules, context translation, and infrastructure adapters.
- [Durable domain identity, aggregate actors, and lifecycle](durable-domain-identity-aggregate-actors-and-lifecycle.md) —
  maps durable entity and aggregate identity onto replaceable actor
  activations without confusing semantic, routing, supervision, or protection
  boundaries.
- [Typed commands, queries, events, and protocol contracts](typed-commands-queries-events-and-protocol-contracts.md) —
  specifies versioned envelopes, behavioral contracts, outcome types,
  protocol state, and the distinct meanings of commands, queries, and events.
- [Invariants, transactions, and concurrency policy](invariants-transactions-and-concurrency-policy.md) —
  chooses atomic boundaries and consistency from declared invariants, using
  serialization or coordination by default and avoiding it only with evidence.
- [Durable state, journals, snapshots, and projections](durable-state-journals-snapshots-and-projections.md) —
  compares current-state and event-sourced persistence and defines replay,
  snapshots, projections, retention, privacy, and recovery contracts.
- [Workflows, process managers, timers, and compensation](workflows-process-managers-timers-and-compensation.md) —
  models long-running cross-aggregate work with durable identities, explicit
  states, timers, retries, pivots, compensation, cancellation, and terminal
  evidence.
- [External effects, ports, adapters, and reconciliation](external-effects-ports-adapters-and-reconciliation.md) —
  contains storage, network, device, payment, and other effects behind typed
  ports that expose partial failure, idempotency, fencing, and unknown outcomes.
- [Presentation sessions, semantic views, and user outcomes](presentation-sessions-semantic-views-and-user-outcomes.md) —
  keeps durable domain state independent of disposable visual, accessible,
  textual, voice, automation, and remote presentations.
- [Offline collaboration, replication, and conflict semantics](offline-collaboration-replication-and-conflict-semantics.md) —
  separates convergence, intent, invariants, authorization, and external-effect
  safety and selects replication policy per domain type.
- [Extension points, plugins, and live-tooling confinement](extension-points-plugins-and-live-tooling-confinement.md) —
  defines narrow extension contracts, explicit imports, protected-domain
  escalation, live inspection/change facets, and revocable resource budgets.
- [Application evolution, schema compatibility, and migration](application-evolution-schema-compatibility-and-migration.md) —
  stages immutable generations, mixed-version compatibility, durable-state
  transformation, publication, rollback cutoffs, and roll-forward repair.
- [Semantic observability, testing, and assurance](semantic-observability-testing-and-assurance.md) —
  connects user-relevant outcomes to bounded telemetry, executable properties,
  model checking, deterministic schedules, compatibility fixtures, and fault
  injection without confusing telemetry with audit truth.
- [Cross-layer placement, tenancy, overload, and recovery topology](cross-layer-placement-tenancy-overload-and-recovery-topology.md) —
  assigns responsibilities across all five layers and separates bounded
  contexts, aggregates, actors, supervisors, tenants, and protected domains
  under failure and resource pressure.

## Maintaining this index

Index every direct component report and keep its description aligned with the
integrated layer. When a component boundary changes, update this index, the
parent notes index, the topic map, the inquiry, the research journal, and every
meaningful incoming body link in the same change.
