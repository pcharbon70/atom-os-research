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

All fourteen components now have internal-service decompositions: 60 studies
of owned state, authority, transitions, completion, failure and verification.
The [research session](../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md)
records four new and thirty reused sources. These are full-system architecture
proposals, not implementation evidence or proof-of-concept work.

## What belongs here

Put one component-scale synthesis here when it refines a Layer 5 responsibility
into explicit semantic, authority, state, protocol, failure, overload,
evolution, recovery, and verification contracts. Keep primary-source analysis
in `30-sources`, active questions in `40-inquiries`, and dated research evidence
in `50-journal`.

## Index

### Subdirectories

- [Application manifest, composition, and authority envelope](application-manifest-composition-and-authority-envelope/README.md) — 4 internal-service studies. Separate declarative application requirements from recipient-specific authority installation and semantic readiness.
- [Bounded contexts, domain model, and application services](bounded-contexts-domain-model-and-application-services/README.md) — 4 internal-service studies. Decompose semantic ownership, use-case admission, model translation and persistence ports without turning every module into a process.
- [Durable domain identity, aggregate actors, and lifecycle](durable-domain-identity-aggregate-actors-and-lifecycle/README.md) — 4 internal-service studies. Separate durable entity lifetime, recoverable activation, serialized decisions and retirement.
- [Typed commands, queries, events, and protocol contracts](typed-commands-queries-events-and-protocol-contracts/README.md) — 4 internal-service studies. Give decoding, operation outcomes, read frontiers and event histories independent contracts.
- [Invariants, transactions, and concurrency policy](invariants-transactions-and-concurrency-policy/README.md) — 4 internal-service studies. Choose the synchronization mechanism from complete domain properties, not from the presence of actors.
- [Durable state, journals, snapshots, and projections](durable-state-journals-snapshots-and-projections/README.md) — 5 internal-service studies. Separate authoritative persistence choice, deterministic history, checkpoint promotion, derived views and retention.
- [Workflows, process managers, timers, and compensation](workflows-process-managers-timers-and-compensation/README.md) — 5 internal-service studies. Decompose durable control state, step outcomes, timers, compensation and structured concurrent obligations.
- [External effects, ports, adapters, and reconciliation](external-effects-ports-adapters-and-reconciliation/README.md) — 4 internal-service studies. Make endpoint participation, intent publication, constrained authority and ambiguous effect repair explicit.
- [Presentation sessions, semantic views, and user outcomes](presentation-sessions-semantic-views-and-user-outcomes/README.md) — 4 internal-service studies. Separate semantic publication, session transport, trusted action admission and durable user feedback.
- [Offline collaboration, replication, and conflict semantics](offline-collaboration-replication-and-conflict-semantics/README.md) — 5 internal-service studies. Separate convergent content, authority admission, scarce rights, schema meaning and safe history collection.
- [Extension points, plugins, and live-tooling confinement](extension-points-plugins-and-live-tooling-confinement/README.md) — 4 internal-service studies. Distinguish extension admission, proposal validation, live-tool powers and generation retirement.
- [Application evolution, schema compatibility, and migration](application-evolution-schema-compatibility-and-migration/README.md) — 5 internal-service studies. Separate directed compatibility, safe intermediate schemas, private migration, in-flight handoff and irreversible retirement.
- [Semantic observability, testing, and assurance](semantic-observability-testing-and-assurance/README.md) — 4 internal-service studies. Separate user-outcome measurement, disclosure-limited telemetry, executable oracles and implementation fault evidence.
- [Cross-layer placement, tenancy, overload, and recovery topology](cross-layer-placement-tenancy-overload-and-recovery-topology/README.md) — 4 internal-service studies. Map semantic ownership onto enforceable trust, tenant, resource and recovery boundaries.

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
