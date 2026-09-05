---
title: "How Should Atom OS Structure Applications and Domain Services?"
kind: inquiry
created: "2026-09-05"
status: open
tags:
  - application-architecture
  - domain-modeling
  - fault-tolerance
  - operating-systems
aliases:
  - "Layer 5 contract inquiry"
---

# How Should Atom OS Structure Applications and Domain Services?

## Why this matters

The first four Atom OS layers now have detailed research contracts for
hardware/architecture mechanisms, a minimal privileged capability kernel, a
BEAM-compatible managed actor runtime, and OTP-like system policy. Without an
equally explicit fifth layer, applications could collapse these distinctions:
PIDs could become durable identity, actor turns could be called transactions,
every message could be called an event, a desktop could own domain truth, or an
application could build private copies of identity, persistence, networking,
update, and resource-control services.

Layer 5 is where technical completion becomes user and domain meaning. A
generic durable store can prove bytes committed; only an application can state
that an order, edit, payment, publication, or device action is valid and
complete. The application must do that without gaining ambient authority or
depending on one immortal monolith.

## Operational question

Choose and validate the smallest unprivileged application architecture that:

1. organizes domain meaning into explicit bounded contexts without equating
   them automatically with actors, packages, tenants, or protected domains;
2. keeps stable domain identity independent of transient PIDs, routes,
   capability handles, storage addresses, and presentation sessions;
3. preserves each declared invariant under concurrency, crash, partition,
   retry, migration, and mixed-version operation;
4. gives every state-changing operation a stable identity and honest rejected,
   expired-before-admission, pending, committed, not-committed, terminated,
   fenced, or indeterminate outcome;
5. selects current-state, event-sourced, collaborative, or coordinated
   persistence per context with bounded replay, retention, privacy, and
   projection contracts;
6. represents long cross-aggregate work as durable workflows with explicit
   timers, pivots, compensation, and manual repair;
7. contains external effects behind typed ports whose sinks participate in
   stable-ID reconciliation or expose unavoidable uncertainty;
8. allows visual, accessible, textual, voice, automation, and remote
   presentations to restart without owning domain truth;
9. confines plugins, native code, adapters, and live tools with explicit
   imports, separate powers, and enforceable budgets;
10. evolves through immutable generations, behavioral compatibility,
    resumable migration, atomic publication, and honest rollback cutoffs;
11. measures semantic user outcomes and verifies them with executable models,
    properties, compatibility histories, and fault injection; and
12. declares tenant, supervision, protection, overload, degradation, and
    recovery topology while relying on Layers 2–4 to validate and enforce it.

The inquiry remains open until those contracts are implemented, measured, and
attacked. The current literature-derived architecture is not resolution.

## Working hypotheses

### H1: six boundaries must remain independent

Bounded context, aggregate, actor activation, supervision subtree, tenant/
security realm, and protected domain should be designed independently and
coincide only when trust, invariant, resource, scaling, and recovery analysis
supports it.

Falsifier: a simpler common boundary gives equal semantic modularity, actor
density, fault recovery, resource control, and security across representative
applications without hidden coupling or unacceptable cost.

### H2: one aggregate actor is the useful native baseline

One non-reentrant actor per active aggregate should align mailbox serialization
with one local invariant boundary while stable `DomainRef` remains independent
of activation. Cold objects may passivate and pooled hosts may be an optimized
profile.

Falsifier: measurements show pooled or functional state-machine hosting is
consistently simpler and cheaper without weakening fairness, isolation,
recovery, migration, or stale-generation safety; or split-brain handling makes
the actor mapping misleading.

### H3: serializable aggregate commit is conservative; coordination freedom is proved

Non-mergeable invariants should use one serializable local commit by default.
Offline or coordination-free operations require an explicit invariant-
confluence, commutativity, monotonicity, escrow, or equivalent argument.

Falsifier: a weaker default preserves all declared invariants in generated and
real histories with materially lower cost and equally understandable failure
semantics, or the proof burden makes valid collaborative applications
impractical.

### H4: stable operation identity plus durable outcomes is the retry boundary

Each logical command/effect should retain one operation ID and request digest
across retries. State, result, outbox, and workflow intent should commit
atomically where they share a store. Unknown external results should remain
`Indeterminate` until endpoint lookup, compensation, or repair.

Falsifier: a simpler protocol prevents duplicate semantic effects and false
failure through every crash/lost-reply history, or realistic clients cannot
use explicit uncertainty safely.

### H5: event sourcing and CQRS are optional profiles

Current-state persistence should remain the ordinary baseline. Event sourcing
is selected only when intrinsic history, temporal reconstruction, and multiple
projections justify evolution, privacy, replay, rebuild, and tooling cost.
Separate read models are chosen independently.

Falsifier: measured applications show one event-sourced profile gives lower
total complexity and stronger recovery across nearly all contexts, or current-
state storage cannot support the required audit and evolution properties.

### H6: business workflows are durable process managers, not blocked calls

Cross-aggregate and long external work should use one durable workflow identity
with explicit states, timers, retries, pivots, compensations, and terminal
evidence. Compensation is a fallible new effect.

Falsifier: choreography or a different abstraction gives clearer ownership,
lower state cost, and equal failure/update observability for consequential
workflows; or a centralized process manager becomes an unacceptable hotspot.

### H7: presentation is disposable relative to domain truth

Applications should publish semantic snapshots/deltas and accept typed actions
so desktops and modality adapters can restart independently. User-visible
pending and terminal states derive from durable outcomes, never frames or
focus.

Falsifier: representative applications cannot preserve usable interaction
without keeping presentation and domain state in one failure domain, or the
semantic protocol imposes prohibitive latency/complexity.

### H8: extensions require explicit imports and risk-selected domains

Pure trusted rules can run in-process; untrusted BEAM, portable bytecode,
native code, parsers, GPU work, and live tools should receive narrow facets and
separate protection according to risk. Inspection, editing, migration,
publication, and effects remain separate powers.

Falsifier: a verified language/runtime profile safely supports untrusted code
with materially less isolation cost and equivalent authority/resource control,
or protected-domain overhead makes useful extension density impossible.

### H9: immutable generation replacement is safer than routine hot mutation

Private preparation, compatibility checks, shadow migration, canary, atomic
publication, drain, and retirement should be the default. Hot update is a
special safe-point profile; rollback stops after unreadable data or irreversible
effects.

Falsifier: routine hot conversion demonstrates equal invariant, workflow,
authority, and effect safety with lower downtime and complexity, or immutable
double-running generations exceed target resource limits without an adequate
staged alternative.

### H10: semantic policy belongs in Layer 5; enforcement remains below

Layer 5 should decide command priority, graceful degradation, tenant/business
scope, and user outcomes. Layer 4 validates/orchestrates and provides generic
services; Layers 2–3 enforce resources and execute actors.

Falsifier: the split causes unavoidable duplicated state or circular recovery,
or a smaller shared lower contract can safely express domain behavior without
putting application semantics into privileged code.

## Paths to explore

### Component reports

The current proposed contracts are inventoried in the [applications and domain
services component index](../20-notes/applications-and-domain-services-components/README.md):

- [Application manifest, composition, and authority envelope](../20-notes/applications-and-domain-services-components/application-manifest-composition-and-authority-envelope.md)
- [Bounded contexts, domain model, and application services](../20-notes/applications-and-domain-services-components/bounded-contexts-domain-model-and-application-services.md)
- [Durable domain identity, aggregate actors, and lifecycle](../20-notes/applications-and-domain-services-components/durable-domain-identity-aggregate-actors-and-lifecycle.md)
- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
- [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)
- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
- [Presentation sessions, semantic views, and user outcomes](../20-notes/applications-and-domain-services-components/presentation-sessions-semantic-views-and-user-outcomes.md)
- [Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics.md)
- [Extension points, plugins, and live-tooling confinement](../20-notes/applications-and-domain-services-components/extension-points-plugins-and-live-tooling-confinement.md)
- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
- [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
- [Cross-layer placement, tenancy, overload, and recovery topology](../20-notes/applications-and-domain-services-components/cross-layer-placement-tenancy-overload-and-recovery-topology.md)

### Executable protocol models

- Domain reference resolution, activation, passivation, lifecycle-generation
  reuse, lease/fence, and split-brain rejection.
- Command admission, expected revision, operation deduplication, local commit,
  reply loss, result retention, and client-state loss.
- Workflow acceptance, timers, duplicate signals, cancellation, pivot,
  compensation failure, indeterminate effect, and manual repair.
- Outbox/inbox relay with crash at each state/intent/publication/receipt point.
- Semantic snapshot/delta/action protocol with view restart and stale grants.
- Offline operation merge, revocation during partition, tombstone collection,
  malicious causal metadata, and online-only effects.
- Old/new application, state, event, projection, adapter, and workflow
  generations through migration, publication, drain, rollback, and repair.

### Measured prototypes

1. One current-state aggregate actor and one application service on the managed
   runtime.
2. One event-sourced aggregate and two rebuildable projections for comparison.
3. One durable process manager connected to a deliberately unreliable external
   endpoint.
4. Two presentation modalities that restart independently of the model.
5. One mergeable document type and one escrowed scarce counter.
6. Trusted callback, isolated BEAM, WASI-like, and native extension profiles.
7. Two tenants across shared and separated protected domains under data and
   resource attacks.
8. One immutable old/new generation migration with a deliberately irreversible
   effect boundary.

### Compatibility and assurance

- Pin the initial BEAM bytecode and OTP application/behaviour compatibility
  profile.
- Differentially test actor/process semantics where compatibility is promised.
- Preserve permanent old/new wire, event, state, snapshot, projection, and
  workflow fixture corpora.
- Require properties and shrinkers for invariants and operation outcomes.
- Use model checking for selected lease/fence, workflow, collaboration, and
  migration protocols.
- Inject real storage, power, native, device, network, CPU, memory, mailbox,
  and telemetry failures beyond the pure actor simulator.

## Findings

### Supported provisional conclusions

- Domain semantics, not packages or screens, define Layer 5 structure.
- Durable domain identity must be independent of actor activation and live
  authority.
- Application services coordinate use cases; aggregate/domain services own
  business rules.
- Aggregate-local transactions and explicit workflows give a clearer baseline
  than hidden distributed transactions.
- Lost replies and external partial failure require stable operation identity
  and explicit uncertainty.
- Event sourcing, CQRS, CRDTs, session types, virtual activation, and hot update
  are optional profiles, not universal requirements.
- Presentation, collaboration, extensions, evolution, observability, tenancy,
  and overload all require domain semantics plus lower-layer enforcement.

These are synthesized in the [applications and domain services
layer](../20-notes/applications-and-domain-services-layer.md).

### Evidence still missing

- Actor-host memory, latency, fairness, and migration measurements on a
  constrained target.
- A Layer 4 storage profile proven to atomically retain state/outcome/outbox/
  workflow records through power failure.
- End-to-end sink participation for exactly-once semantic effects, or usability
  evidence for indeterminate repair where it is impossible.
- A realistic invariant catalog and coordination analysis from several
  application domains.
- Event-sourcing recovery/evolution/privacy cost compared with current-state
  persistence on Atom OS.
- Offline authorization, revocation, tombstone, metadata-privacy, and malicious-
  replica experiments.
- Protected-domain and extension-host security/performance measurements.
- Behavioral compatibility and workflow migration through mixed BEAM/OTP code
  generations.
- Accessibility and multi-view user evidence for the semantic presentation
  protocol.
- Recovery exercises in which the failed component is the application root,
  adapter, store, policy service, runtime domain, or recovery manager.

## Outcome

The inquiry remains open. The current best candidate is the fourteen-component
architecture in the [integrated report](../20-notes/applications-and-domain-services-layer.md),
routed by the [topic map](../10-maps/applications-and-domain-services.md) and
recorded in the [2026-09-05 research session](../50-journal/2026-09-05-applications-and-domain-services-deep-dive.md).
It remains a developing proposal until executable models, prototypes,
compatibility tests, attacks, and failure experiments satisfy the operational
question.
