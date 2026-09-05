---
title: "2026-09-05 Applications and Domain Services Deep Dive"
kind: journal
created: "2026-09-05"
tags:
  - application-architecture
  - domain-modeling
  - literature-review
  - operating-systems
  - research-method
aliases:
  - "Atom OS Layer 5 research session"
---

# 2026-09-05 Applications and Domain Services Deep Dive

## Observations

This session completed the first research decomposition of the fifth Atom OS
layer. It created an integrated [applications and domain services
report](../20-notes/applications-and-domain-services-layer.md) and fourteen
detailed reports in the [component
directory](../20-notes/applications-and-domain-services-components/README.md).

The strongest result is that a bounded context, aggregate, actor activation,
supervision subtree, business-tenant/security-realm binding, and protected
domain are not the
same boundary. They may coincide after explicit trust, invariant, resource,
failure, and scaling analysis, but no source justifies treating them as
synonyms. One non-reentrant actor per active aggregate is the proposed native
baseline, not a law.

The resulting Layer 5 owns domain meaning: stable domain identity, invariants,
commands, queries, domain facts, business workflows, domain-specific external
effects, semantic views, collaboration rules, application compatibility, and
user-visible outcomes. It declares required authority, budgets, lifecycle,
degradation, tenancy, and recovery topology. Layer 4 still validates and
orchestrates the application, supplies generic identity/policy, persistence,
timers, networking, devices, updates, overload control, telemetry, audit, and
durable outcomes. Layers 2 and 3 enforce and execute the lower mechanisms.

The cross-component protocol uses stable operation IDs and distinguishes
rejection, pre-admission expiry, fencing, durable pending responsibility,
committed, not-committed, domain termination, and indeterminate results. A
timeout, actor crash, or lost reply does not prove noncommit. Transactional
outbox records committed
intent but does not make an arbitrary remote or physical effect exactly once.

Event sourcing, CQRS, coordination-free replication, virtual actors, session
types, protected extension profiles, and hot upgrade were retained as optional
tools. Each applies only when its stated assumptions and costs match the domain.
No one persistence or consistency ideology was promoted to a Layer 5 mandate.

These are literature-derived architectural proposals. No Atom OS Layer 5
implementation, storage engine, protocol model, fault-injection campaign,
benchmark, accessibility evaluation, security test, or user study was
performed during this session.

## Environment

- Repository: `/home/ducky/code/atom-os-research`
- Research date: 2026-09-05
- Host time zone: America/Toronto
- Activity: scientific-paper, standards, official-documentation, engineering-
  article, and practitioner-blog review; independent evidence lanes; cross-
  source reconciliation; archive synthesis
- Architecture scope: unprivileged Layer 5 above the existing hardware/
  architecture, minimal privileged kernel, managed actor runtime, and OTP-like
  system-services layers
- Hardware, simulator, storage engine, runtime implementation, application
  domain, UI toolkit, or external endpoint selected: none
- Local artifacts: one integrated synthesis, fourteen component reports, one
  component index, twenty-nine new source notes, one topic map, one inquiry,
  navigation updates, one corrected reused DOI, and this journal

## Evidence

### Research question and operational standard

For the layer and every component, the research asked:

> What semantic, identity, protocol, authority, persistence, failure, overload,
> evolution, and recovery contract would let an Atom OS application produce
> honest domain outcomes while preserving the four lower-layer boundaries?

A recommendation was retained only when its report:

- states what Layer 5 owns and what remains in Layers 1–4;
- distinguishes DDD model, actor activation, supervision, tenancy, deployment,
  and kernel-enforced protection boundaries;
- names durable and transient identities and generation checks;
- identifies the invariant, transaction, workflow, and external-effect scope;
- distinguishes domain event, integration event, storage log, effect intent,
  telemetry, and audit;
- exposes rejection, acceptance, commit, noncommit proof, domain termination,
  fencing, and uncertainty rather than inferring completion from transport or
  actor survival;
- bounds queues, retries, history, projections, plugins, migration, telemetry,
  and recovery work;
- compares alternatives and preserves negative evidence and scope limits;
- defines implementation stages and experiments that could falsify the
  proposal; and
- remains `maturity: developing` because no Atom OS experiment validated it.

### Search and selection method

The original five-layer document and completed Layers 1–4 defined the boundary.
Three independent evidence lanes examined domain decomposition/actor identity;
transactions/persistence/workflows/effects/collaboration; and application
composition/presentation/extensions/evolution/observability/tenancy. The main
synthesis reconciled overlap and contradictions, then used a targeted second
search for idempotent effects, online schema change, and application
compartmentalization.

Search snippets and secondary summaries were used only for discovery. Detailed
claims were checked against complete primary papers, normative specifications,
official project documentation, or first-party engineering material.
Practitioner articles and blogs were used where they defined an influential
implemented pattern; their lack of independent or formal validation is stated.
Current living documents were pinned by access date.

### Component reports

1. [Application manifest, composition, and authority envelope](../20-notes/applications-and-domain-services-components/application-manifest-composition-and-authority-envelope.md)
2. [Bounded contexts, domain model, and application services](../20-notes/applications-and-domain-services-components/bounded-contexts-domain-model-and-application-services.md)
3. [Durable domain identity, aggregate actors, and lifecycle](../20-notes/applications-and-domain-services-components/durable-domain-identity-aggregate-actors-and-lifecycle.md)
4. [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
5. [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)
6. [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
7. [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
8. [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
9. [Presentation sessions, semantic views, and user outcomes](../20-notes/applications-and-domain-services-components/presentation-sessions-semantic-views-and-user-outcomes.md)
10. [Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics.md)
11. [Extension points, plugins, and live-tooling confinement](../20-notes/applications-and-domain-services-components/extension-points-plugins-and-live-tooling-confinement.md)
12. [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
13. [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
14. [Cross-layer placement, tenancy, overload, and recovery topology](../20-notes/applications-and-domain-services-components/cross-layer-placement-tenancy-overload-and-recovery-topology.md)

### Strongest cross-component conclusions

1. **Layer 5 owns meaning, not generic infrastructure.** Persistence mechanism,
   timers, identity/policy, network/device services, release orchestration,
   resource enforcement, and audit remain below it.
2. **Durable identity is not live authority.** `DomainRef` survives activations;
   PIDs, routes, leases, capabilities, view sessions, and native pointers do not
   enter durable domain records.
3. **The invariant selects consistency.** Aggregate-local serializable commit is
   conservative; coordination freedom requires evidence for the exact invariant
   and merge model.
4. **Actor serialization is narrower than a transaction.** It does not prove
   durable commit, unique activation under partition, projection freshness, or
   external exactly-once effects.
5. **Operation outcomes carry uncertainty honestly.** Stable IDs and durable
   result rendezvous make retries safer, but a nonparticipating endpoint can
   still leave `Indeterminate`.
6. **Workflows own long-lived responsibility.** Waiting, timers, pivots,
   compensation, and manual repair are explicit durable states; aggregate actors
   do not block across them.
7. **Event sourcing is optional.** It offers history and replay while carrying
   measured evolution, privacy, projection, tooling, and expertise costs.
8. **Presentation is reconstructible.** A desktop or accessibility bridge can
   restart from current semantic truth and reconcile operation IDs without
   replaying raw input.
9. **Convergence is not complete correctness.** Collaboration separately
   specifies intent, invariant, authorization, privacy, and effect safety.
10. **Extensions receive explicit imports.** Untrusted and native code use risk-
    selected protected domains; inspection, change, publication, and effects
    are different powers.
11. **Compatibility is behavioral.** Successful decode does not establish old/
    new invariant, outcome, workflow, redaction, or effect compatibility.
12. **Recovery and overload are cross-layer contracts.** Layer 5 declares
    semantic priority/degradation while lower layers enforce finite resources
    and retain protected outcome/audit/reconciliation/recovery reserve.

### Contradictions and resolutions

- Because “service layer” can ambiguously name either use-case orchestration or
  domain rules, the synthesis uses explicit terms: application services
  coordinate use cases; domain services contain rules not naturally owned by
  one aggregate.
- Strong local transactions and coordination avoidance are not universal
  rivals. The former is the conservative profile; the latter is selected only
  when the declared invariant and merge procedure satisfy its assumptions.
- Event-sourcing advocacy emphasizes replay and auditability, while empirical
  work reports evolution, rebuild, privacy, tooling, and learning costs. The
  result is a context-specific option rather than a mandate.
- Sagas improve long-work availability but do not recreate outer isolation or
  rollback. Compensation remains a separately authorized, fallible action.
- CRDT research proves convergence under exact conditions, while editing work
  shows convergent histories can preserve poor intent. Both properties are
  tested separately.
- Immutable generation systems make code rollback tractable, but do not reverse
  mutable data or observed effects. Rollback therefore stops at an explicit
  semantic boundary.

### Evidence gaps and falsifiers

The central gaps are a chosen application domain and invariant catalog; an
atomic Layer 4 state/outcome/outbox/workflow store profile; actor-host memory and
hot-key measurements; external endpoint stable-ID participation; usability of
indeterminate outcomes; event-history privacy and erasure; offline revocation
and tombstone collection; extension-domain overhead; mixed-version BEAM/OTP
application behavior; semantic presentation accessibility evidence; and full
recovery/overload experiments.

The synthesis is falsified by an implementation that:

- serializes PIDs, live capabilities, routes, focus tokens, or native pointers
  as durable domain identity;
- lets two authoritative activations commit the same lifecycle generation;
- calls actor serialization or snapshot isolation sufficient for every
  invariant;
- reports a timeout or lost reply as proven noncommit;
- calls outbox delivery or message deduplication exactly-once external effect;
- performs effects during event replay, migration validation, or projection
  rebuild;
- calls compensation rollback or code rollback data/effect rollback;
- accepts a wire-compatible change that violates behavioral history;
- merges unauthorized offline work merely because replicas converge;
- lets an extension enumerate ambient resources or turn inspection into
  publication/effect authority;
- treats telemetry as authoritative audit/outcome evidence;
- requires domain state to restart with the desktop by construction; or
- lets Layer 5 publish, grant, resource, or recover itself without independent
  lower-layer control.

### Evidence boundary

Formal results apply only to their stated models. System evaluations apply only
to their implementations, workloads, and hardware. Practitioner patterns are
design evidence, not proof. No external result transfers automatically to Atom
OS, and no experiment in this session demonstrated the proposed guarantees.

## Source manifest

### Newly introduced sources

- [Coordination Avoidance in Database Systems](../30-sources/bailis-et-al-2014-coordination-avoidance.md) — invariant-confluence criterion and scoped coordination-avoidance evaluation.
- [Wedge: Splitting Applications into Reduced-Privilege Compartments](../30-sources/bittau-et-al-2008-wedge.md) — default-deny compartmentalization and application partitioning evidence.
- [Durable Functions: Semantics for Stateful Serverless](../30-sources/burckhardt-et-al-2021-durable-functions.md) — formal replay-backed actor/workflow semantics and history-growth constraints.
- [QuickCheck](../30-sources/claessen-hughes-2000-quickcheck.md) — executable properties, generated inputs, and counterexample shrinking.
- [Hexagonal Architecture](../30-sources/cockburn-2005-hexagonal-architecture.md) — practitioner port/adapter separation of domain logic from technologies.
- [Asynchronous Functional Reactive Programming for GUIs](../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md) — compositional asynchronous presentation precedent and scope limits.
- [Domain-Driven Design Reference](../30-sources/evans-2015-domain-driven-design-reference.md) — bounded contexts, aggregates, services, events, and layered domain vocabulary.
- [Event Sourcing](../30-sources/fowler-2005-event-sourcing.md) — practitioner replay/history pattern and external-query cautions.
- [Protocol Buffers Language Guide and Schema Evolution Practices](../30-sources/google-2026-protocol-buffers-evolution.md) — concrete stable-field and unknown-data evolution rules.
- [The Transaction Concept](../30-sources/gray-1981-transaction-concept.md) — transaction properties, state transformations, and long-work limitations.
- [Statecharts](../30-sources/harel-1987-statecharts.md) — explicit hierarchical/concurrent lifecycle modeling.
- [Life beyond Distributed Transactions](../30-sources/helland-2007-life-beyond-distributed-transactions.md) — entity-local transactions, messages, and distributed uncertainty argument.
- [Multiparty Asynchronous Session Types](../30-sources/honda-et-al-2008-multiparty-asynchronous-session-types.md) — global-to-endpoint protocol checking under formal assumptions.
- [Service Level Objectives](../30-sources/jones-et-al-2016-service-level-objectives.md) — user-relevant indicators, objectives, and measurement conditions.
- [OpSets](../30-sources/kleppmann-et-al-2018-opsets.md) — sequential replicated-datatype specifications and convergent intent anomalies.
- [Architectural Concerns in Multi-Tenant SaaS Applications](../30-sources/krebs-et-al-2012-multi-tenant-saas.md) — tenancy across data, configuration, QoS, performance, and placement.
- [A Behavioral Notion of Subtyping](../30-sources/liskov-wing-1994-behavioral-subtyping.md) — compatibility through invariants, pre/postconditions, and histories rather than shape alone.
- [How Amazon Web Services Uses Formal Methods](../30-sources/newcombe-et-al-2015-aws-formal-methods.md) — first-party evidence for small executable distributed-system models.
- [An Empirical Characterization of Event Sourced Systems and Their Schema Evolution: Lessons from Industry](../30-sources/overeem-et-al-2021-event-sourced-systems.md) — industry benefits, costs, and schema-evolution tactics from 25 engineers and 19 systems.
- [On the Criteria To Be Used in Decomposing Systems into Modules](../30-sources/parnas-1972-decomposing-systems-into-modules.md) — information hiding and change-oriented module boundaries.
- [Online, Asynchronous Schema Change in F1](../30-sources/rae-et-al-2013-online-schema-change-f1.md) — compatible intermediate schemas and mixed-version corruption evidence.
- [Fault Tolerance via Idempotence](../30-sources/ramalingam-vaswani-2013-fault-tolerance-via-idempotence.md) — formal duplicate/failure semantics and idempotent workflow composition.
- [Transactional Outbox](../30-sources/richardson-2026-transactional-outbox.md) — practitioner atomic-intent pattern and explicit duplicate-relay limitation.
- [Typestate](../30-sources/strom-yemini-1986-typestate.md) — state-constrained operations and static protocol-misuse prevention.
- [Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System](../30-sources/terry-et-al-1995-bayou-conflicts.md) — tentative state and application-specific conflict detection/resolution.
- [Maintaining Robust Protocols](../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md) — explicit extension and validation guidance against permissive ambiguity.
- [Workflow Patterns](../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md) — precise branching, joining, instance, and cancellation vocabulary.
- [A Note on Distributed Computing](../30-sources/waldo-et-al-1994-distributed-computing.md) — irreducible latency, concurrency, memory, and partial-failure differences.
- [WASI Design Principles](../30-sources/wasi-project-2026-design-principles.md) — explicit capability imports and portable host-boundary design.

### Reused sources

- [An Approach to Persistent Programming](../30-sources/atkinson-et-al-1983-persistent-programming.md) — typed rooted persistence precedent and authority/retention limits.
- [Actor Record and Replay](../30-sources/aumayr-et-al-2018-actor-record-replay.md) — deterministic actor replay and instrumentation-cost evidence.
- [Resource Containers](../30-sources/banga-et-al-1999-resource-containers.md) — hierarchical resource attribution across application work.
- [Orleans](../30-sources/bernstein-et-al-2014-orleans.md) — stable virtual-actor identity over replaceable activations.
- [Implementing Remote Procedure Calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md) — request identity, retry, stale reply, and ambiguous completion precedent.
- [Exponential Backoff and Jitter](../30-sources/brooker-2015-exponential-backoff-jitter.md) — bounded retry desynchronization and contention amplification.
- [The Chubby Lock Service](../30-sources/burrows-2006-chubby.md) — leases, sessions, authoritative naming, and distributed ownership limits.
- [A Unifying Reference Framework for Multi-Target User Interfaces](../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md) — separation of task/domain, abstract, concrete, and final presentation models.
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md) — fine-grained recovery dependent on explicit state/retry boundaries.
- [Crash-Only Software](../30-sources/candea-fox-2003-crash-only-software.md) — one restart path and externalized-state recovery precedent.
- [Dynamic Instrumentation of Production Systems](../30-sources/cantrill-et-al-2004-dtrace.md) — bounded, verifier-controlled probes and aggregation.
- [FSCQ](../30-sources/chen-et-al-2015-fscq.md) — formally specified crash-consistent storage precedent.
- [Access Control for Collaborative Editors](../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md) — explicit composition of collaboration and access control.
- [Concuerror](../30-sources/christakis-et-al-2013-concuerror.md) — stateless schedule exploration for Erlang concurrency defects.
- [QuickCheck and PULSE](../30-sources/claessen-et-al-2009-quickcheck-pulse.md) — controlled Erlang scheduling, property testing, and race shrinking.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — immutable deployment closures, generations, and rollback scope.
- [From L3 to seL4](../30-sources/elphinstone-heiser-2013-l4-lessons.md) — minimal privileged mechanism and user-space policy placement.
- [OTP Managed Runtime Documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) — current BEAM actor, code-generation, and native-boundary behavior.
- [OTP System Services Documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) — application, supervision, release, and service-policy baseline.
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md) — committed subtransactions, weaker outer isolation, and compensation semantics.
- [The Confused Deputy](../30-sources/hardy-1988-confused-deputy.md) — ambient-authority failure when callers control names used by a deputy.
- [seL4 Design Principles](../30-sources/heiser-2020-sel4-design-principles.md) — small privileged enforcement and explicit assurance boundary.
- [Single Application Model, Multiple Synchronized Views](../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md) — one model driving structurally different visual and speech views.
- [A Conflict-Free Replicated JSON Datatype](../30-sources/kleppmann-beresford-2017-conflict-free-json.md) — structured convergent data with explicit datatype limits.
- [Local-First Software](../30-sources/kleppmann-et-al-2019-local-first-software.md) — offline use, collaboration, user ownership, and unresolved policy issues.
- [Smalltalk-80 MVC](../30-sources/krasner-pope-1988-mvc-smalltalk-80.md) — historical model/view/controller separation and multi-view precedent.
- [RIFL](../30-sources/lee-et-al-2015-rifl.md) — durable request result rendezvous, migration, and safe reclamation.
- [Capability Myths Demolished](../30-sources/miller-et-al-2003-capability-myths.md) — designation, delegation, attenuation, and revocation through object capabilities.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — write-ahead logging, recovery, and precise transaction commit boundaries.
- [TOSCA 2.0](../30-sources/oasis-2025-tosca-2.md) — typed dependency/capability graph and parser/resolver/orchestrator separation.
- [OpenTelemetry Specification](../30-sources/opentelemetry-project-2026-specification-1-60.md) — bounded telemetry and shared correlation semantics with completeness limits.
- [Live Objects All The Way Down](../30-sources/pimas-et-al-2023-live-objects-all-the-way-down.md) — reflective live-object systems and metacircular trade-offs.
- [User-Driven Access Control](../30-sources/roesner-et-al-2012-user-driven-access-control.md) — user-mediated resource designation and authority precedent.
- [End-to-End Arguments in System Design](../30-sources/saltzer-et-al-1984-end-to-end-arguments.md) — application-endpoint placement of semantic correctness checks.
- [Conflict-Free Replicated Data Types](../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md) — formal convergence conditions and limited semantic scope.
- [Dapper](../30-sources/sigelman-et-al-2010-dapper.md) — distributed trace propagation, sampling, and causal-correlation precedent.
- [Mutatis Mutandis](../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md) — safe points, type-directed update, and explicit live-state transformation.
- [Achieving Convergence, Causality Preservation, and Intention Preservation](../30-sources/sun-et-al-1998-cooperative-editing-consistency.md) — separation of collaborative correctness dimensions.
- [Timing Wheels](../30-sources/varghese-lauck-1987-timing-wheels.md) — scalable timer mechanism beneath application timer meaning.
- [WAI-ARIA 1.2](../30-sources/w3c-2023-wai-aria-1-2.md) — semantic role, state, relation, action, and accessibility-tree contract.
- [Core Accessibility API Mappings 1.2](../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md) — platform mapping evidence for structurally different semantic views.
- [Capsicum](../30-sources/watson-et-al-2010-capsicum.md) — practical descriptor-rights attenuation and capability mode.
- [SEDA](../30-sources/welsh-et-al-2001-seda.md) — staged finite queues, admission, and overload behavior.
- [Dagor](../30-sources/zhou-et-al-2018-dagor.md) — overload admission and service-protection evidence at scale.

## Threads

- [Applications and domain services map](../10-maps/applications-and-domain-services.md)
- [How should Atom OS structure applications and domain services?](../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md)
- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)

## Follow-ups

- Select one narrow application domain and write a complete vocabulary,
  invariant catalog, command/outcome schema, and threat model.
- Build executable models for domain-reference activation, aggregate commit,
  workflow/effect reconciliation, collaboration, and application migration.
- Select or implement a Layer 4 transaction profile capable of atomic state,
  outcome, outbox, and workflow-intent persistence, then inject power loss.
- Compare one-actor-per-aggregate with pooled hosts under cold-object density,
  hot-key load, tenant fairness, migration, and recovery.
- Implement two independent semantic presentation adapters and restart them
  throughout pending and indeterminate command histories.
- Evaluate offline revocation, tombstone collection, privacy, and malicious
  replica behavior for one mergeable and one scarce datatype.
- Compare trusted BEAM callbacks, isolated BEAM domains, WASI-like modules, and
  native domains for authority, compatibility, latency, memory, and teardown.
- Define the exact application-facing BEAM/OTP compatibility profile and a
  permanent old/new conformance corpus.
