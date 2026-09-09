---
title: "2026-09-09 Application and Domain-Service Internal Services"
kind: journal
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - research-method
  - system-architecture
aliases: []
---

# 2026-09-09 Application and Domain-Service Internal Services

## Observations

The user requested the same internal-service research depth used for the
kernel and managed-runtime components. The actual destination is
[applications-and-domain-services-components](../20-notes/applications-and-domain-services-components/README.md),
with plural “applications.” At session start, its fourteen parent reports
existed and none had a component-named decomposition subdirectory.

This session adds 60 service studies, fourteen local directory indexes and
four source notes. It extends the parent reports, directory navigation,
application topic map, home map and existing open inquiry. Counts follow
distinct ownership, transition and completion obligations; a document is not
automatically an actor, protection domain or deployable microservice.

## Environment

- Repository: atom-os-research; starting branch: main.
- Starting revision: ee59c672d47718567e86c213bd2eda93250781ad.
- Initial worktree: clean.
- Research date: 2026-09-09.
- Target: proposed full-system Layer 5, consuming Layers 2–4 enforcement and
  services. No machine, simulator, QEMU fixture or proof-of-concept milestone
  is being implemented or qualified.
- Existing compiled-BEAM and process-local tracing-GC requirements remain
  unchanged. No application language, VM implementation or kernel toolchain
  is selected by this decomposition.
- No commits, pushes, PRs, package installations or external-device writes
  were requested or performed for this session.

## Research method and reading depth

Reviewed the fourteen parent contracts and their existing inquiry, navigation
and source notes, then decomposed independent state owners and handoff
boundaries. Followed the established internal-service report shape: source
basis, owned state, admission and completion, failure, alternatives,
unexecuted falsifiers and cross-component links.

Searches covered scientific and first-party material on numerical invariants,
idempotent APIs, schema evolution, domain boundaries, compartmentalization and
local-first collaboration. Representative queries included “Extending
Eventually Consistent Cloud Databases Enforcing Numeric Invariants,”
“Making retries safe with idempotent APIs,” “Parallel Change,”
“Cambria schema evolution lenses,” “Online, Asynchronous Schema Change in F1,”
“DDD Reference bounded context aggregate” and “Wedge reduced privilege.”
Search results were discovery aids, not evidence for detailed claims.

Fresh primary reading:

- Bounded-counter conference paper: system model, algorithm, middleware,
  fault assumptions and evaluation setup. The institutional record verified
  venue, DOI and the seven-author conference version. The eight-author arXiv
  record found during search was not silently conflated with that version.
- Featonby's article: request identity, atomic recording, response meaning,
  late arrivals, retention and changed-parameter behavior; AWS's announcement
  supplied the publication date.
- Sato's complete practitioner post: interface expansion, migration,
  contraction, examples and limitations. Its broad permissive-parsing advice
  is not adopted for critical application meanings.
- Cambria's prototype account: schema examples, read-time translation,
  semantic mapping failures and explicit research/performance limitations.
  No claim is made about the current library's production readiness.
- Reused RIFL paper: completion-record and reclamation sections; reused
  invariant-confluence paper: theorem, common-ancestor condition and model
  limits; reused F1 paper: store assumptions, intermediate schema transitions,
  version lag and write fencing.
- WASI design-principles body: explicit handles, link-time interposition and
  the host compatibility boundary. This confirms a design principle, not a
  security evaluation or a pinned executable ABI.

The other reused works were reviewed through their existing evidence-focused
archive notes and the parent synthesis. Their prior access dates and provenance
remain intact; this journal does not claim a fresh cover-to-cover reading of
all thirty reused originals. In particular, historical Orleans, Elm, NixOS and
SEDA findings are not current product or Atom OS performance claims.

A guessed F1 PDF path was unavailable; search located the publisher's
[correct paper](https://www.vldb.org/pvldb/vol6/p1045-rae.pdf), which was read.
The GitHub WASI page initially showed navigation and a loading warning, but
its extracted body contained the relevant design principles. No paywalled
abstract was used as sole support for an algorithmic claim. No cited experiment
was reproduced locally.

## Decomposition inventory

| Parent component | New studies | Distinct research scope |
| --- | --- | --- |
| [Application manifest, composition, and authority envelope](../20-notes/applications-and-domain-services-components/application-manifest-composition-and-authority-envelope/README.md) | 4 | Separate declarative application requirements from recipient-specific authority installation and semantic readiness. |
| [Bounded contexts, domain model, and application services](../20-notes/applications-and-domain-services-components/bounded-contexts-domain-model-and-application-services/README.md) | 4 | Decompose semantic ownership, use-case admission, model translation and persistence ports without turning every module into a process. |
| [Durable domain identity, aggregate actors, and lifecycle](../20-notes/applications-and-domain-services-components/durable-domain-identity-aggregate-actors-and-lifecycle/README.md) | 4 | Separate durable entity lifetime, recoverable activation, serialized decisions and retirement. |
| [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts/README.md) | 4 | Give decoding, operation outcomes, read frontiers and event histories independent contracts. |
| [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy/README.md) | 4 | Choose the synchronization mechanism from complete domain properties, not from the presence of actors. |
| [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections/README.md) | 5 | Separate authoritative persistence choice, deterministic history, checkpoint promotion, derived views and retention. |
| [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation/README.md) | 5 | Decompose durable control state, step outcomes, timers, compensation and structured concurrent obligations. |
| [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation/README.md) | 4 | Make endpoint participation, intent publication, constrained authority and ambiguous effect repair explicit. |
| [Presentation sessions, semantic views, and user outcomes](../20-notes/applications-and-domain-services-components/presentation-sessions-semantic-views-and-user-outcomes/README.md) | 4 | Separate semantic publication, session transport, trusted action admission and durable user feedback. |
| [Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics/README.md) | 5 | Separate convergent content, authority admission, scarce rights, schema meaning and safe history collection. |
| [Extension points, plugins, and live-tooling confinement](../20-notes/applications-and-domain-services-components/extension-points-plugins-and-live-tooling-confinement/README.md) | 4 | Distinguish extension admission, proposal validation, live-tool powers and generation retirement. |
| [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration/README.md) | 5 | Separate directed compatibility, safe intermediate schemas, private migration, in-flight handoff and irreversible retirement. |
| [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance/README.md) | 4 | Separate user-outcome measurement, disclosure-limited telemetry, executable oracles and implementation fault evidence. |
| [Cross-layer placement, tenancy, overload, and recovery topology](../20-notes/applications-and-domain-services-components/cross-layer-placement-tenancy-overload-and-recovery-topology/README.md) | 4 | Map semantic ownership onto enforceable trust, tenant, resource and recovery boundaries. |

## Cross-source synthesis and limits

The source works support narrower claims than the complete architecture.
Their composition below is our proposed design and still needs models,
implementation evidence and adversarial evaluation.

- Logical identity survives activation; accepted responsibility additionally
  requires retained operation identity and recoverable outcomes.
- Actor serialization, storage commit, event publication and external effect
  completion are distinct boundaries.
- Convergent data does not establish current authority, conserved scarce
  rights, user intent or safe external execution.
- Schema conversion is not domain-action equivalence; mixed-version histories
  and stale writers matter beyond static decoding.
- Compensation preserves an amended history rather than erasing earlier
  observations. Old definitions and repair authority are durable dependencies.
- A disposable view still needs a recoverable action-to-operation binding;
  replaying raw input is not session recovery.
- Overload control must distinguish refusal before admission from unresolved
  accepted work. Recovery reserve needs lower-layer enforcement.
- Snapshot pruning can promote a derived artifact to authority, changing its
  deletion and backup obligations.

### Bounded consistency repair

The external-effects parent previously stated that adapter compromise could
not mint new effects. This was too strong without a participating enforcement
boundary. The parent now distinguishes protected memory and narrowed imports
from misuse of credentials an adapter legitimately holds. The new
[intent-bound grant study](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation/intent-bound-grants-and-compromised-adapter-containment.md)
requires sink validation or an independent non-bypassable broker; otherwise
the adapter remains trusted within the provider credential's effect scope.

This clarification does not assert an implemented security mechanism. It makes
an existing architecture claim conditional and testable.

## Evidence

Local work consists of archive inspection and document changes only. The
studies' verification obligations are proposed cases, not executable test
results. There are no new latency, memory, power-loss, fault-containment,
usability or invariant-preservation measurements.

Structural verification is separate from architectural qualification:

- `python3 validate_archive.py` passed: 891 completed documents, 76 directories,
  9177 local links and 383 source notes; 27 deep-dive manifests classify 371
  introduced and 502 reused source uses, with twelve pre-manifest source notes.
- `git diff --check` passed for tracked changes.
- Each of the 79 new files passed `git diff --no-index --check` against
  `/dev/null` and a final-newline check.
- Reviewed the 60 study contracts, fourteen parent-to-child inventories,
  cross-component routes, four new bibliographic records and exact manifest.
  The only non-navigation change to a parent contract is the adapter-trust
  qualification described above.
- Validator code and schema did not change; their unit tests were not rerun.
- Final scope: 79 new files and 22 modified tracked documents, left uncommitted.

These checks validate archive structure and editorial consistency. They do
not demonstrate the proposed OS contracts.

## Source manifest

### Newly introduced sources

- [Bounded counters](../30-sources/balegas-et-al-2015-bounded-counters.md) — Bounded counters conserve distributed numeric rights under crash and intact-storage assumptions; Byzantine double spending is outside the paper's model.
- [Idempotent APIs](../30-sources/featonby-2021-idempotent-apis.md) — Featonby's operational account uses caller request identity, parameter checks and retained results; retention and endpoint participation remain explicit limits.
- [Parallel Change](../30-sources/sato-2014-parallel-change.md) — Sato separates interface expansion, client migration and contraction; the pattern is not a distributed correctness proof.
- [Project Cambria](../30-sources/litt-et-al-2020-cambria.md) — Cambria demonstrates schema lenses but explicitly leaves semantic reassignment and missing external data beyond mechanical translation.

### Reused sources

- [TOSCA 2.0](../30-sources/oasis-2025-tosca-2.md) — TOSCA separates typed requirements, graph resolution and lifecycle actions; a graph does not establish authority or truthful readiness.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — NixOS separates immutable configuration generations from mutable activation effects; selecting an old generation does not undo domain state.
- [WASI Design Principles](../30-sources/wasi-project-2026-design-principles.md) — The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed.
- [Wedge](../30-sources/bittau-et-al-2008-wedge.md) — Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs.
- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md) — Crash-only design puts authoritative state outside replaceable components; restarting cannot repair every corruption or ambiguous effect.
- [DDD Reference](../30-sources/evans-2015-domain-driven-design-reference.md) — Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof.
- [Behavioral subtyping](../30-sources/liskov-wing-1994-behavioral-subtyping.md) — Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation.
- [RIFL](../30-sources/lee-et-al-2015-rifl.md) — RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity.
- [Hexagonal Architecture](../30-sources/cockburn-2005-hexagonal-architecture.md) — Cockburn places technology adapters outside semantic ports; the pattern does not guarantee effect safety.
- [Event-sourced systems study](../30-sources/overeem-et-al-2021-event-sourced-systems.md) — Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits.
- [Orleans virtual actors](../30-sources/bernstein-et-al-2014-orleans.md) — The 2014 Orleans report separates logical actor identity from activation; its cloud model is not the BEAM process contract.
- [RFC 9413](../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md) — RFC 9413 warns that indiscriminate permissive parsing can preserve ambiguity and obstruct protocol evolution.
- [WAI-ARIA 1.2](../30-sources/w3c-2023-wai-aria-1-2.md) — WAI-ARIA defines semantic roles, states and relationships; vocabulary conformance alone does not establish usable or authorized interaction.
- [Coordination Avoidance](../30-sources/bailis-et-al-2014-coordination-avoidance.md) — Invariant confluence relates coordination freedom to the exact operations, invariant and merge model.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — ARIES makes recovery depend on durable ordering metadata; its storage log is not a domain-event model.
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md) — Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation.
- [Durable Functions semantics](../30-sources/burckhardt-et-al-2021-durable-functions.md) — Durable Functions formalizes restricted history replay; arbitrary nondeterminism and external effects remain outside that abstraction.
- [Asynchronous FRP](../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md) — The early Elm paper demonstrates asynchronous view composition, not durable application outcomes or protected presentation.
- [Local-First Software](../30-sources/kleppmann-et-al-2019-local-first-software.md) — Local-first research argues for locally usable user-owned documents; its scope is not arbitrary scarce-resource or external-effect transactions.
- [Workflow Patterns](../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md) — Workflow Patterns distinguishes branch, join and cancellation semantics; it does not provide durable effect execution.
- [DAGOR](../30-sources/zhou-et-al-2018-dagor.md) — DAGOR propagates admission priorities through request paths; its empirical policy is neither a hard resource ceiling nor universal fairness.
- [SEDA](../30-sources/welsh-et-al-2001-seda.md) — SEDA exposes staged queues and admission control; its evaluation also documents missed latency targets and initially unbounded queues.
- [Service Level Objectives](../30-sources/jones-et-al-2016-service-level-objectives.md) — Google SRE guidance starts indicators from user-relevant behavior and explicit measurement populations, not process uptime alone.
- [CRDTs](../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md) — CRDT convergence follows stated algebra and delivery assumptions, not arbitrary invariant or authorization correctness.
- [OpSets](../30-sources/kleppmann-et-al-2018-opsets.md) — OpSets makes replicated meaning explicit through sequential interpretation; convergence can still permit undesirable user-visible ordering.
- [Mutatis Mutandis](../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md) — Proteus relates update safety to code, data and update points; type safety is weaker than domain or effect safety.
- [F1 schema evolution](../30-sources/rae-et-al-2013-online-schema-change-f1.md) — F1 uses safe intermediate schemas under a bounded version-lag assumption; arbitrary actor upgrades do not inherit its proof.
- [QuickCheck](../30-sources/claessen-hughes-2000-quickcheck.md) — QuickCheck supplies generated properties and shrinking; an incomplete oracle or input distribution can miss failures.
- [AWS formal methods](../30-sources/newcombe-et-al-2015-aws-formal-methods.md) — AWS reports design errors found with small executable specifications; models remain distinct from implementation evidence.
- [Multi-tenant SaaS concerns](../30-sources/krebs-et-al-2012-multi-tenant-saas.md) — The SaaS concern model spans data, customization, placement and performance; one tenant label is not physical isolation.

## Threads

Continue through the [application topic map](../10-maps/applications-and-domain-services.md#internal-service-research-routes)
and [open application inquiry](../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md).
Source notes and the manifest provide provenance; neither closes that inquiry.

## Follow-ups

The highest-value next research is an executable composition model spanning
client-action identity, aggregate commit, outbox, endpoint receipt, retention
and migration. Compare counterexamples with a second model for offline rights,
revocation and peer retirement. These models are research proposals, not an
authorization to implement them.

Search also located the [Keyhive access-control project](https://www.inkandswitch.com/project/keyhive/)
as a prospective comparison for offline policy. Its protocol was not assessed
in this session and supports no conclusion here. A future study should compare
its revocation and conflict semantics with our explicitly chosen reconnect
policy instead of assuming a universal local-first authorization model.

Additional open evidence includes user understanding of indeterminate outcomes,
real endpoint qualification, physical durability, extension containment costs,
old-reader retention, mixed-generation workflow histories and bounded recovery
under overload.
