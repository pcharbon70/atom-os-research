---
title: "Applications and Domain Services"
kind: map
created: "2026-09-05"
tags:
  - application-architecture
  - domain-modeling
  - fault-tolerance
  - operating-systems
aliases:
  - "Layer 5 map"
  - "Applications layer map"
---

# Applications and Domain Services

## Scope

This map covers the fifth layer in the proposed Atom OS decomposition: the
unprivileged applications and domain services that turn lower-layer actor,
capability, persistence, identity, networking, device, lifecycle, and recovery
mechanisms into user-meaningful work.

The route deliberately separates:

- bounded context from package, actor, supervisor, tenant, and protected
  domain;
- durable domain identity from PID, route, storage address, and live authority;
- application-service coordination from domain rules;
- aggregate transaction from cross-aggregate workflow;
- domain event from integration event, WAL record, effect intent, telemetry,
  and audit;
- local commit from external effect completion;
- convergence from intent, invariants, authorization, and effect safety; and
- application-declared semantic policy from lower-layer enforcement.

## Start here

- [Applications and domain services layer](../20-notes/applications-and-domain-services-layer.md) —
  the integrated Layer 5 architecture, shared identity/outcome model, fourteen
  components, cross-layer contract, implementation stages, and falsifiers.
- [Applications and domain services component index](../20-notes/applications-and-domain-services-components/README.md) —
  the complete local inventory of detailed component reports.
- [How should Atom OS structure applications and domain services?](../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) —
  the open operational question, hypotheses, experiments, and evidence gaps.
- [2026-09-05 applications and domain services deep dive](../50-journal/2026-09-05-applications-and-domain-services-deep-dive.md) —
  research method, cross-source synthesis, exact source manifest, and evidence
  boundary.
- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  the original five-layer decomposition.

## Component route

### Composition, meaning, identity, and protocols

- **[1. Application manifest, composition, and authority envelope](../20-notes/applications-and-domain-services-components/application-manifest-composition-and-authority-envelope.md)**
  gives one immutable application generation a declarative graph and one
  explicit composition root, while Layer 4 resolves dependencies and derives
  narrow capabilities.
- **[2. Bounded contexts, domain model, and application services](../20-notes/applications-and-domain-services-components/bounded-contexts-domain-model-and-application-services.md)**
  gives each model a language boundary and separates use-case coordination
  from aggregate and domain-service rules.
- **[3. Durable domain identity, aggregate actors, and lifecycle](../20-notes/applications-and-domain-services-components/durable-domain-identity-aggregate-actors-and-lifecycle.md)**
  maps stable domain references onto replaceable actor activations without
  confusing mailbox serialization with durable atomicity.
- **[4. Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)**
  defines versioned envelopes, behavioral compatibility, explicit generations,
  and honest operation outcomes.

Primary routes:

- [Domain-Driven Design Reference](../30-sources/evans-2015-domain-driven-design-reference.md)
- [On the Criteria To Be Used in Decomposing Systems into Modules](../30-sources/parnas-1972-decomposing-systems-into-modules.md)
- [Statecharts](../30-sources/harel-1987-statecharts.md)
- [Orleans](../30-sources/bernstein-et-al-2014-orleans.md)
- [Typestate](../30-sources/strom-yemini-1986-typestate.md)
- [Multiparty Asynchronous Session Types](../30-sources/honda-et-al-2008-multiparty-asynchronous-session-types.md)
- [A Behavioral Notion of Subtyping](../30-sources/liskov-wing-1994-behavioral-subtyping.md)
- [Protocol Buffers evolution guidance](../30-sources/google-2026-protocol-buffers-evolution.md)

### Invariants, persistence, workflows, and effects

- **[5. Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)**
  starts from explicit invariants, uses aggregate-local serializability by
  default, and removes coordination only with evidence.
- **[6. Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)**
  selects current-state, event-sourced, or replicated persistence per context
  and defines replay, retention, privacy, and projection frontiers.
- **[7. Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)**
  represents long work with durable process identity, explicit states, timers,
  pivots, compensation, and manual repair.
- **[8. External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)**
  keeps infrastructure outside domain logic and exposes admission, ambiguity,
  idempotency, fencing, and endpoint-visible outcomes.

Primary routes:

- [The Transaction Concept](../30-sources/gray-1981-transaction-concept.md)
- [Coordination Avoidance](../30-sources/bailis-et-al-2014-coordination-avoidance.md)
- [Life beyond Distributed Transactions](../30-sources/helland-2007-life-beyond-distributed-transactions.md)
- [Event-sourced systems and schema evolution](../30-sources/overeem-et-al-2021-event-sourced-systems.md)
- [Workflow Patterns](../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md)
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md)
- [Durable Functions semantics](../30-sources/burckhardt-et-al-2021-durable-functions.md)
- [RIFL](../30-sources/lee-et-al-2015-rifl.md)
- [Fault Tolerance via Idempotence](../30-sources/ramalingam-vaswani-2013-fault-tolerance-via-idempotence.md)
- [Transactional Outbox](../30-sources/richardson-2026-transactional-outbox.md)
- [A Note on Distributed Computing](../30-sources/waldo-et-al-1994-distributed-computing.md)

### Presentation, collaboration, and extensions

- **[9. Presentation sessions, semantic views, and user outcomes](../20-notes/applications-and-domain-services-components/presentation-sessions-semantic-views-and-user-outcomes.md)**
  lets disposable visual, accessible, textual, voice, automation, and remote
  views reconnect to durable domain truth.
- **[10. Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics.md)**
  chooses mergeable, escrow, leased, consensus, or online-effect policy per
  type while keeping tentative and committed state visible.
- **[11. Extension points, plugins, and live-tooling confinement](../20-notes/applications-and-domain-services-components/extension-points-plugins-and-live-tooling-confinement.md)**
  confines extension code through narrow protocols, explicit imports, resource
  budgets, and protected domains selected by risk.

Primary routes:

- [Asynchronous FRP for GUIs](../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md)
- [Single Application Model, Multiple Synchronized Views](../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md)
- [WAI-ARIA 1.2](../30-sources/w3c-2023-wai-aria-1-2.md)
- [Managing Update Conflicts in Bayou](../30-sources/terry-et-al-1995-bayou-conflicts.md)
- [Conflict-Free Replicated Data Types](../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md)
- [OpSets](../30-sources/kleppmann-et-al-2018-opsets.md)
- [Local-First Software](../30-sources/kleppmann-et-al-2019-local-first-software.md)
- [WASI Design Principles](../30-sources/wasi-project-2026-design-principles.md)
- [Wedge](../30-sources/bittau-et-al-2008-wedge.md)

### Evolution, assurance, tenancy, overload, and recovery

- **[12. Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)**
  prepares immutable generations, checks directed compatibility, stages state
  transformations, publishes atomically, and marks irreversible boundaries.
- **[13. Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)**
  measures user-relevant semantic outcomes and attaches executable properties,
  models, compatibility histories, and fault scenarios.
- **[14. Cross-layer placement, tenancy, overload, and recovery topology](../20-notes/applications-and-domain-services-components/cross-layer-placement-tenancy-overload-and-recovery-topology.md)**
  maps application declarations onto lower enforcement while preserving tenant
  isolation, bounded work, reserved recovery, and independent failure domains.

Primary routes:

- [Online Schema Change in F1](../30-sources/rae-et-al-2013-online-schema-change-f1.md)
- [Mutatis Mutandis](../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md)
- [QuickCheck](../30-sources/claessen-hughes-2000-quickcheck.md)
- [How AWS Uses Formal Methods](../30-sources/newcombe-et-al-2015-aws-formal-methods.md)
- [Service Level Objectives](../30-sources/jones-et-al-2016-service-level-objectives.md)
- [Architectural Concerns in Multi-Tenant SaaS Applications](../30-sources/krebs-et-al-2012-multi-tenant-saas.md)
- [Crash-Only Software](../30-sources/candea-fox-2003-crash-only-software.md)
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md)
- [SEDA](../30-sources/welsh-et-al-2001-seda.md)
- [Dagor](../30-sources/zhou-et-al-2018-dagor.md)

## Boundary with Layer 4

Layer 5 owns domain identities, schemas, invariants, application use cases,
business workflows, compensation meaning, effect semantics, semantic views,
collaboration policy, and business completion evidence.

Layer 4 owns manifest validation, dependency and application-lifecycle
orchestration, service naming, configuration, identity/policy/grants/secrets,
generic durable stores and outcomes, durable-timer scheduling and retry policy,
device/network providers, distributed membership and coordination, release
activation, hard resource governance, telemetry, audit, and operator control.
Layer 3 supplies the transient actor-lifecycle and timer-delivery mechanisms
that Layer 4 governs.

Examples keep the line concrete:

- an order-fulfilment workflow is Layer 5; a software-release rollout is Layer
  4;
- a payment semantic adapter is Layer 5; the network/TLS endpoint is Layer 4;
- aggregate schema and snapshot policy are Layer 5; WAL and checkpoint mechanics
  are Layer 4;
- an application declares tenant-bound capability needs; Layer 4 derives them
  and Layer 2 enforces them; and
- Layer 5 defines “committed order”; Layer 4 can prove only the generic record
  and operation outcome it was asked to store.

## Key distinctions to preserve

- A PID is not durable identity.
- Actor serialization is not a durable transaction.
- Timeout is not cancellation or proof of noncommit.
- Compensation is not rollback.
- Outbox is not exactly-once remote execution.
- Event sourcing is not required by CQRS or actors.
- A storage log is not automatically a domain event.
- Convergence is not intent, invariant, authorization, or effect correctness.
- Wire compatibility is not behavioral compatibility.
- Supervision is not a protection boundary.
- Telemetry is not audit or durable outcome truth.
- Application-declared budgets are not enforcement until Layers 2–4 admit and
  account them.

## Open questions

- [How should Atom OS structure applications and domain services?](../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md)
- Which storage profile can atomically retain aggregate revision, operation
  outcome, outbox, and workflow records on the first target?
- When does one-aggregate-per-actor outperform a pooled host under constrained
  memory and hot-key load?
- Which protocols justify session-type monitors or explicit model checking?
- Which external endpoints support stable operation lookup, and how should the
  UI represent irreducibly indeterminate effects?
- What offline authorization, revocation, tombstone, and privacy profile is
  feasible?
- What protected-domain granularity gives useful tenant/plugin isolation while
  retaining cheap actor density?
- How will the exact BEAM/OTP application compatibility profile be tested
  through updates and persistent state?
