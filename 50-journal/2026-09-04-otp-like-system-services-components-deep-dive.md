---
title: "2026-09-04 OTP-like system services components deep dive"
kind: journal
created: "2026-09-04"
tags:
  - literature-review
  - otp
  - research-method
  - service-management
  - system-services
aliases:
  - "OTP-like system services component research session"
---

# 2026-09-04 OTP-like system services components deep dive

## Observations

This session expanded all thirteen proposed components of the [OTP-like system
services layer](../20-notes/otp-like-system-services-layer.md) into detailed
implementation research reports under the [OTP-like system services components
directory](../20-notes/otp-like-system-services-components/README.md).

The shared conclusion is that OTP's supervision and behavior patterns remain
valuable, but an operating-system service layer must expose several boundaries
that conventional application frameworks can leave implicit:

- a stable name, authenticated identity, service incarnation, and invocation
  capability are different things;
- validation, preparation, readiness, publication, and active observation are
  different lifecycle milestones;
- timeout, cancellation, rejection, acceptance, completion, and indeterminate
  outcome are different results;
- restart, durable recovery, retry, and distributed takeover are different
  operations;
- local observation, distributed suspicion, authoritative ownership, lease,
  and sink-enforced fencing are different evidence;
- code rollback, state rollback, compensation, and roll-forward are different
  recovery strategies; and
- lossy telemetry, retained crash evidence, persistent alarms, and durable
  audit require different resource and failure contracts.

The recommended service layer is unprivileged. It consumes protected domains,
capabilities, scheduling contexts, bounded transport, typed faults, and safe
teardown from the minimal kernel, plus machine mechanisms from the architecture
layer and actor execution from the managed runtime. Policy remains in
replaceable service domains with outer recovery holders.

The reports are architectural syntheses. No Atom OS service controller,
behavior engine, supervisor, registry, credential broker, storage engine,
driver service, network stack, coordination cell, updater, resource governor,
or observability pipeline was implemented or executed in this session.

## Environment

- Repository: `atom-os-research`
- Research date: 2026-09-04
- Host time zone: America/Toronto
- Activity: scientific-paper, standards, official-project documentation, and
  engineering-article review; cross-source architecture synthesis; archive
  editing
- Kernel, managed runtime, or service implementation: none
- Emulator or physical target: none
- Storage, device, network, or distributed fault profile exercised: none
- Formal or executable model: none
- Benchmarks and fault injection: none
- Local artifacts: thirteen component reports, sixteen new source notes,
  navigation/inquiry updates, and this evidence record

## Evidence

### Research question and operational standard

For each component, the research asked:

> Which implementation best carries OTP's lightweight process, supervision,
> fault-containment, and message-passing principles into an unprivileged OS
> service while making authority, resources, generations, external effects,
> recovery, overload, and evidence explicit?

A recommendation was retained only when its report:

- distinguishes source-demonstrated behavior from cross-source synthesis and
  proposed Atom OS behavior;
- names the component's privilege and authority boundary;
- defines stable identity, changing generations, lifecycle states, resource
  ownership, and public linearization points;
- states queue-full, deadline, cancellation, crash, retry, replacement, and
  stale-generation behavior;
- identifies which effect outcomes are proved and which remain indeterminate;
- preserves exact OTP semantics only inside a named compatibility profile;
- gives a staged implementation and verification program with falsifiers; and
- keeps limitations, negative results, and unverified assumptions visible.

### Method

The integrated layer supplied the component decomposition and cross-cutting
invariants. Evidence collection used three parallel, independent lanes:

1. bootstrap, behavior engines, supervision, and lifecycle orchestration;
2. naming, configuration/identity/secrets, persistence, devices, and networks;
3. membership/coordination, release and migration, overload governance, and
   observability/audit/operator control.

Primary research papers, standards, and official project documentation were
preferred. Engineering articles were used for operational algorithms and
failure experience where their scope was recorded. Search results located
works but were not used as evidence; the cited works themselves were read for
the claims retained. Current specifications and documentation record their
access date or pinned edition. Existing archive source notes were reused where
they already preserved the needed evidence; sixteen new notes were added for
substantively used work not previously recorded.

### Component reports

#### Bootstrap, behavior, supervision, and lifecycle

- [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md)
- [Behaviour engines and capability-gated management](../20-notes/otp-like-system-services-components/behaviour-engines-and-capability-gated-management.md)
- [Supervision and recovery policy](../20-notes/otp-like-system-services-components/supervision-and-recovery-policy.md)
- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)

#### Local state, identity, devices, and networks

- [Naming, registry, and local discovery](../20-notes/otp-like-system-services-components/naming-registry-and-local-discovery.md)
- [Configuration, workload identity, and secrets](../20-notes/otp-like-system-services-components/configuration-workload-identity-and-secrets.md)
- [Durable state, transactions, and outcome recovery](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md)
- [Device-service policy and management](../20-notes/otp-like-system-services-components/device-service-policy-and-management.md)
- [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md)

#### Distributed authority, change, overload, and operations

- [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination.md)
- [Release, update, rollback, and state migration](../20-notes/otp-like-system-services-components/release-update-rollback-and-state-migration.md)
- [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)

### Strongest cross-component conclusions

1. **Controllers reconcile immutable desired state.** Pure validation precedes
   effects; preparation is private; one generation root publishes a complete
   result; persistent one-effect steps permit restart and convergence.
2. **OTP compatibility and native safety are named profiles.** Strict adapters
   preserve documented call, behavior, supervisor, significant-child, and
   application semantics. Native finite queues, readiness, jitter, resource
   policy, and forceful replacement remain visible extensions.
3. **Recovery begins with fencing.** Supervisors, devices, sessions, leases,
   updates, and operators all close old admission and reject stale generations
   before publishing a successor. Quiescence and reclamation remain separate.
4. **Discovery is not authority.** Local names resolve to generation-bound
   attenuated handles; distributed gossip yields candidate observations;
   exclusive ownership requires quorum evidence, a lease or barrier, and a
   fence enforced at every effect sink.
5. **Configuration and credentials are separate.** Configuration is a typed
   immutable snapshot whose validation and active adoption differ. Identity is
   derived from protected workload evidence; secrets use least-scope,
   short-lived handles and explicit issuer-outage policy.
6. **Durability has a named proof point.** A framed single-writer WAL and
   immutable checkpoint are the simplest initial contract. Result records can
   make a narrow operation retryable only when mutation and result share the
   same durable transaction and retention rules.
7. **I/O outcomes are layered.** Device descriptor consumption, transport ACK,
   peer acceptance, application commit, and physical durability are different
   proof points. Unknown external effects remain indeterminate.
8. **Update is not one signature check.** Artifact approval, provenance,
   compatibility, private rollout, migration, activation, observation, and
   rollback/roll-forward are separate evidence and authority stages.
9. **Overload is an API result.** Every asynchronous boundary has finite
   capacity, causal charging, and a declared reject/wait/shed/coalesce/degrade
   action. Retry and recovery consume separate bounded budgets.
10. **Operational evidence has multiple contracts.** Routine telemetry may
    drop; crash evidence is small and retained; alarms are durable state;
    security audit is integrity-protected and externally witnessed but cannot
    prove a compromised producer told the truth.

### Evidence gaps and falsifiers

The most important unverified composition points are:

- eventual stable reconciliation with finite local resource and boot-deadline
  bounds;
- OTP differential conformance under bounded native mailboxes;
- exact domain, actor, service, device, session, lease, and release generation
  relationships;
- persistent intent/outcome recovery across lost replies and power cuts;
- safe device quiescence, reset, DMA fencing, and completion classification for
  each concrete device class;
- application-level outcome lookup across reconnect and service replacement;
- measured clock/pause bounds or a lease-free coordination profile;
- sink-enforced fencing across storage, device, network, and update targets;
- state migration compatibility and irreversible-transition recovery;
- conserved causal resource accounting across actors, continuations, and
  services; and
- audit completeness, privacy, external witnessing, and survival under storage
  or identity-service failure.

Any prototype that equates timeout with absence, makes a stale name/capability
refer to a replacement, publishes partial generations, retries an indeterminate
effect, acknowledges durability before its device profile permits, lets
gossip transfer ownership, allows ordinary load to consume all recovery
capacity, or calls sampled telemetry a complete audit trail falsifies the
baseline architecture.

### Evidence boundary

This session did not:

- implement, boot, or benchmark any Atom OS layer;
- run BEAM bytecode or OTP applications over the proposed services;
- execute a controller, supervisor, registry, credential, storage, device,
  network, consensus, updater, overload, or audit state machine;
- model-check a lifecycle, lease, fencing, migration, or retry protocol;
- perform crash, power-cut, corruption, partition, clock, DMA, driver, parser,
  credential, overload, or operator fault injection;
- reproduce any paper's experiment or transfer its proof to Atom OS; or
- select a final hardware target, storage profile, network stack, consensus
  library, cryptosystem, or compatibility release.

Consequently, measurements remain properties of the cited evaluated systems;
living specifications remain behavior contracts rather than independent
evidence; and every component report retains `maturity: developing`.

## Source manifest

### Newly introduced sources

- [Exponential backoff and jitter](../30-sources/brooker-2015-exponential-backoff-jitter.md)
  — capped randomized retry scheduling and its operational limitations.
- [The Erlang start phase](../30-sources/burcsi-et-al-2010-erlang-start-phase.md)
  — dependency-aware parallel startup evidence and benchmark limits.
- [FSCQ](../30-sources/chen-et-al-2015-fscq.md) — crash-specified
  write-ahead logging, recovery, and proof-boundary lessons.
- [etcd API guarantees](../30-sources/etcd-project-2026-api-guarantees.md) —
  revisioned publication, consistency classes, watches, and resnapshot.
- [xDS REST and gRPC protocol](../30-sources/envoy-project-2026-xds-protocol.md)
  — version/nonce separation and the distinction between ACK and activation.
- [Leases](../30-sources/gray-cheriton-1989-leases.md) — time-bounded cache and
  authority tradeoffs under explicit timing assumptions.
- [Vault secrets, leases, and security model](../30-sources/hashicorp-2026-vault-secrets-and-leases.md)
  — dynamic-secret lifetime, renewal, revocation lineage, and threat limits.
- [sDDF design](../30-sources/heiser-et-al-2026-sddf-design.md) — isolated
  driver/virtualizer components, bounded ownership queues, and selective DMA
  mappings.
- [Gray failure](../30-sources/huang-et-al-2017-gray-failure.md) —
  perspective-dependent partial failure and multi-signal diagnosis.
- [QUIC](../30-sources/iyengar-thomson-2021-quic.md) — secure multiplexed
  transport, credits, migration, generations, and 0-RTT replay limits.
- [A global name service for a highly decentralized system](../30-sources/lampson-1986-global-name-service.md)
  — stable names, changing locations, caching, and administrative structure.
- [TOSCA 2.0](../30-sources/oasis-2025-tosca-2.md) — typed service graphs,
  representation resolution, and orchestration vocabulary.
- [OpenTelemetry specification 1.60](../30-sources/opentelemetry-project-2026-specification-1-60.md)
  — current trace, metric, log, context, sampling, and limit semantics.
- [End-to-end arguments in system design](../30-sources/saltzer-et-al-1984-end-to-end-arguments.md)
  — application-level verification beyond lower-layer delivery evidence.
- [Omega](../30-sources/schwarzkopf-et-al-2013-omega.md) — snapshot planning,
  optimistic version-checked commit, and shared-state scheduler tradeoffs.
- [Anvil](../30-sources/sun-et-al-2024-anvil.md) — eventually stable
  reconciliation, single-effect steps, and verified-controller limits.

### Reused sources

- [Making reliable distributed systems](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
  — isolated processes, links, monitors, supervision, and fault boundaries.
- [Resource containers](../30-sources/banga-et-al-1999-resource-containers.md)
  — charging resource use to causal activity across execution contexts.
- [Implementing remote procedure calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md)
  — request identity, retransmission, duplicate suppression, and uncertainty.
- [Formally verified system initialisation](../30-sources/boyton-et-al-2013-verified-system-initialisation.md)
  — declarative bootstrap and proof-scope precedent.
- [Chubby](../30-sources/burrows-2006-chubby.md) — coarse coordination,
  sessions, cache invalidation, sequencers, and operational uncertainty.
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md) — small recovery
  units and state/request placement constraints.
- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md) —
  uniform start/recover paths and externally preserved state.
- [DTrace](../30-sources/cantrill-et-al-2004-dtrace.md) — production dynamic
  probes, bounded actions, aggregation, and disabled-probe considerations.
- [Unreliable failure detectors](../30-sources/chandra-toueg-1996-failure-detectors.md)
  — suspicion and consensus under explicit timing/accuracy assumptions.
- [SWIM](../30-sources/das-et-al-2002-swim.md) — scalable randomized probing,
  suspicion, dissemination, and weakly consistent membership.
- [CuriOS](../30-sources/david-et-al-2008-curios.md) — isolated restartable
  services and client-state placement.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — immutable dependency
  closures, generation selection, and live-activation limits.
- [OTP 29 system-services documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)
  — the pinned behavior, supervisor, application, registry, and management
  compatibility contract.
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md) — explicit semantic
  compensation for committed multi-step workflows.
- [RIFL](../30-sources/lee-et-al-2015-rifl.md) — retained durable results and
  the narrow conditions for retryable operations.
- [PARTISAN](../30-sources/meiklejohn-et-al-2019-partisan.md) — explicit
  distributed topologies and pluggable communication rather than one implicit
  full mesh.
- [Capability myths demolished](../30-sources/miller-et-al-2003-capability-myths.md)
  — attenuation, delegation, confinement, and naming/authority separation.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — write-ahead logging,
  commit, redo/undo, and the complexity of concurrent in-place state.
- [Practical dynamic software updating for C](../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md)
  — explicit update points, transformation, and compatibility constraints.
- [Raft](../30-sources/ongaro-ousterhout-2014-raft.md) — replicated-log safety,
  leader election, commitment, and membership-change structure.
- [The Update Framework](../30-sources/samuel-et-al-2010-tuf.md) —
  role-separated update metadata and rollback/freeze resistance.
- [Secure audit logs](../30-sources/schneier-kelsey-1999-secure-audit-logs.md)
  — forward-integrity structures and the limits of cryptographic audit.
- [Dapper](../30-sources/sigelman-et-al-2010-dapper.md) — low-overhead sampled
  causal tracing at distributed-service scale.
- [SPIFFE Workload API](../30-sources/spiffe-project-2026-workload-api.md) —
  out-of-band workload identity and complete credential-update snapshots.
- [Scaling Reliably](../30-sources/trinder-et-al-2017-scaling-reliably.md) —
  empirical distributed-Erlang topology, scalability, and reliability limits.
- [Nooks](../30-sources/swift-et-al-2003-nooks.md) — driver isolation,
  recovery, and the limits of same-kernel containment.
- [Recovering device drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md)
  — shadow state, driver restart, and device-specific recovery limits.
- [Borg](../30-sources/verma-et-al-2015-borg.md) — declarative desired state,
  reconciliation, admission, and controller/agent separation.
- [SEDA](../30-sources/welsh-et-al-2001-seda.md) — explicit stages, finite
  queues, and load conditioning.
- [DAGOR](../30-sources/zhou-et-al-2018-dagor.md) — server-observed overload,
  coordinated shedding, and authenticated business-priority lessons.

## Threads

- [OTP-like system services map](../10-maps/otp-like-system-services.md) routes
  from the integrated layer through every component report and major evidence
  family.
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
  remains open and now names component-specific prototypes and falsifiers.
- [Minimal privileged kernel](../20-notes/minimal-privileged-kernel-layer.md)
  owns protected objects, authority, bounded invocation, temporal capacity,
  faults, and safe teardown consumed by these services.
- [Managed actor runtime](../20-notes/managed-actor-runtime-layer.md) executes
  actors and BEAM code while these services supply higher-level policy.

## Follow-ups

1. Specify the common identity/generation/outcome/resource-context schema once
   and generate component API types from it.
2. Build executable models for manifest reconciliation, supervisor recovery,
   local registry snapshot/watch, WAL recovery, device fencing, leases, and
   release activation before selecting production data structures.
3. Implement a deterministic single-node nucleus with manifest controller,
   strict/native behavior engines, supervisor, registry, configuration store,
   and in-memory durable-state simulator.
4. Connect one isolated synthetic device and one loopback network protocol to
   exercise buffer ownership, credits, crash recovery, and indeterminate
   outcomes.
5. Differentially test the pinned OTP compatibility profile while measuring
   and documenting each bounded-resource divergence.
6. Add a three-node coordination experiment only after one local fenced effect
   sink exists, then inject partitions, pauses, stale owners, and membership
   changes.
7. Exercise release and state migration with power cuts, rollback-incompatible
   schema changes, overload, telemetry loss, durable audit, and operator
   recovery.
