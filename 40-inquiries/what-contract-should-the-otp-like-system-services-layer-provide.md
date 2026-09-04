---
title: "What contract should the OTP-like system-services layer provide?"
kind: inquiry
created: "2026-09-03"
status: open
tags:
  - distributed-systems
  - fault-tolerance
  - operating-systems
  - otp
  - service-management
  - supervision
aliases:
  - "OTP-like services contract inquiry"
---

# What contract should the OTP-like system-services layer provide?

## Why this matters

The proposed Atom OS architecture deliberately keeps BEAM execution and
process-local tracing collection in an unprivileged managed runtime while a
minimal capability kernel enforces protection and resources. That leaves a
fourth layer responsible for the policy that makes an operating system usable:
behaviours, supervision, application lifecycle, naming, configuration,
persistence, device and network service management, distributed coordination,
updates, overload response, and operations.

Calling that layer “OTP-like” does not define its contract. Existing OTP gives
excellent local composition but does not by itself provide durable request
outcomes, capability-safe naming, resource containment, authenticated
least-authority distribution, consensus-backed ownership, sink-enforced
fencing, crash-consistent cluster updates, or a durable audit trail. Putting
all those jobs into one immortal manager would recreate a large correlated
failure and authority boundary above the microkernel.

## Operational question

Choose and validate the smallest unprivileged service architecture that:

1. preserves the selected OTP behaviour, supervision, application, and release
   semantics required by the declared compatibility profile;
2. starts from an immutable desired-service manifest that binds dependencies,
   delegated capabilities, resource budgets, recovery reserves, configuration,
   and artifacts without changing the separate boot-authority envelope;
3. atomically publishes generation-bound service handles without treating a
   name, actor identifier, or authenticated identity as authority;
4. distinguishes rejection, acceptance, commit, abort, cancellation, and
   indeterminate outcomes for effectful operations;
5. reconstructs declared durable state after process, domain, machine, and
   power failure under explicit storage assumptions;
6. keeps local failure observation, remote suspicion, distributed membership,
   authoritative metadata, leases, and fencing as distinct evidence;
7. prevents overload, telemetry, health checks, retries, and restarts from
   amplifying failure;
8. stages signed updates through compatibility, quiescence, migration,
   activation, and an honest point of no return; and
9. survives failure of its own registry, supervisor, identity, storage,
   coordination, update, and operations services through recovery authority
   outside each failed boundary.

The inquiry remains open until the contract is executable and measured. A
literature-derived architecture does not resolve it.

## Working hypotheses

### H1: the layer is a federation of confined service domains

Critical services should run as ordinary managed actors or isolated service
domains, each with narrow capabilities, bounded resources, and an independent
recovery holder. A small root controller reconciles a sealed desired-state
manifest within a boot-manifest-bound delegation envelope but is neither
privileged nor able to repair its own runtime.

Falsifier: a single service domain demonstrates a materially smaller,
auditable design without unacceptable correlated failure, authority, latency,
or recovery risk; or the proposed federation cannot bootstrap without circular
dependencies and duplicated policy.

### H2: one generation-safe lifecycle can govern all publication

Service creation, registry binding, configuration activation, driver
replacement, remote ownership, and update rollout can share the
reserve–prepare–publish–drain–retire pattern while retaining type-specific
generations and effect rules.

Falsifier: a required component cannot expose one atomic publication point, or
the common lifecycle hides a domain-specific safety transition such as device
reset, storage commit, or consensus reconfiguration.

### H3: supervision remains policy and gains recovery budgets

OTP-style hierarchical restart scope, ordered shutdown, and intensity limits
remain useful, but restart attempts should consume explicit recovery resources,
use bounded backoff, and require recovered or clean state before successor
publication.

Falsifier: model and workload tests show a different non-hierarchical recovery
model gives clearer failure scope and lower tail latency, or fixed recovery
reserves cause worse availability than controlled borrowing without weakening
containment.

### H4: durable operations expose uncertainty instead of hiding it

An effectful service call should return or later reconcile one of rejected,
accepted, committed, aborted, cancelled-before-commit, indeterminate, or
fenced. `CancelRequested` is nonterminal until a commit/cancel race produces
one of those proved outcomes. Exactly-once retry is offered only when a stable
logical request ID is bound to the authenticated principal, operation, request
digest, and generation; the effect and result share a proved durable
transaction boundary; retries rendezvous with the result after placement
change; and result reclamation waits for acknowledgement or safe client-lease
expiry.

Falsifier: a simpler API preserves all required safety and retry behavior
through crashes and disconnects, or the richer outcome states cannot be used
correctly by realistic supervised applications.

### H5: discovery and authority use different distributed planes

Weakly consistent membership and group discovery should remain available and
mergeable under partition. Exclusive service ownership and configuration
changes should use quorum-backed ordered metadata, leases, and monotonically
increasing fencing values validated at every effect sink. Fence proofs bind
issuer, coordination cell, resource, owner, lease, configuration, and
generation; sinks retain their accepted high-water generation across restart.
A lease permits continued work without a quorum only under explicit
clock-drift, scheduling-pause, and expiry bounds; otherwise authoritative
operations fail closed or consult a quorum each time.

Falsifier: a single protocol meets both availability and exclusivity needs
under the declared partition model with lower complexity, or target hardware
cannot support a quorum control plane and an alternative can prove equivalent
single-owner safety.

### H6: immutable configuration and artifacts are the recoverable baseline

Configuration, service manifests, and release artifacts should be
content-addressed and immutable. Activation changes one ordered reference after
validation and preparation. Credentials use a separate short-lived identity
channel rather than being embedded in ordinary configuration.

Falsifier: storage or footprint measurements show immutable snapshots are
untenable on target systems and an in-place scheme gives equally strong
atomicity, provenance, rollback, and secret-isolation guarantees.

### H7: admission control is a sibling of supervision

Finite queues, deadline-aware admission, backpressure, shedding, degradation,
and retry budgets should keep a healthy but saturated service running.
Supervision acts on failed invariants, not ordinary excess demand.

Falsifier: representative workloads cannot expose useful admission classes, or
the control overhead and false rejection exceed the tail-latency and recovery
benefits.

### H8: telemetry, crash evidence, alarms, and audit require separate contracts

High-volume logs, metrics, and traces can be sampled or dropped under declared
policy. Crash evidence needs bounded protected capture. Alarm state needs
deduplication and lifecycle. Security and control audit needs durable,
tamper-evident recording and independently protected export.

Falsifier: one pipeline satisfies the strongest durability and integrity
contract while meeting telemetry cost and availability targets, or the
separate pipelines cannot preserve causal identifiers well enough for
diagnosis.

## Paths to explore

### Component implementation reports

The current evidence and proposed implementation contracts are decomposed into
thirteen reports in the [OTP-like system services component
index](../20-notes/otp-like-system-services-components/README.md):

- [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md)
- [Behaviour engines and capability-gated management](../20-notes/otp-like-system-services-components/behaviour-engines-and-capability-gated-management.md)
- [Supervision and recovery policy](../20-notes/otp-like-system-services-components/supervision-and-recovery-policy.md)
- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)
- [Naming, registry, and local discovery](../20-notes/otp-like-system-services-components/naming-registry-and-local-discovery.md)
- [Configuration, workload identity, and secrets](../20-notes/otp-like-system-services-components/configuration-workload-identity-and-secrets.md)
- [Durable state, transactions, and outcome recovery](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md)
- [Device-service policy and management](../20-notes/otp-like-system-services-components/device-service-policy-and-management.md)
- [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md)
- [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination.md)
- [Release, update, rollback, and state migration](../20-notes/otp-like-system-services-components/release-update-rollback-and-state-migration.md)
- [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)

### Formal and executable models

- Service lifecycle with controller crash before and after publication.
- Supervisor escalation with child, supervisor, runtime-domain, and recovery
  holder failures.
- Request acceptance, cancel/commit races, result loss, same-ID/different-body
  replay, migration, client-state loss, and idempotency-record garbage
  collection.
- Registry revision, candidate versus authoritative reads, owner death, stale
  handles, and an atomic snapshot-plus-watch cursor through overflow/reconnect.
- WAL/checkpoint recovery with ordered LSNs, transaction commit framing,
  checkpoint replay cuts, atomic pointer publication, and a torn write at each
  persistence boundary.
- Membership suspicion, authenticated boot/incarnation tuples, tombstone and
  authorized rejoin, lease jeopardy/expiry, quorum loss, scoped fencing,
  sink-high-water recovery, and delayed old messages.
- Update acquisition, trusted freshness/anti-rollback state, resumable shadow
  migration, atomic publication, rollback, commit, and updater crash.
- Audit intent/effect/outcome pairing, crash between each pair, storage or
  export interruption, key evolution, truncation, and recovery.

### Single-node prototypes

1. Implement compatible server and state-machine behaviours with explicit
   deadlines, late replies, and cooperative management.
2. Build a supervisor and desired-state controller over the deterministic
   managed runtime.
3. Add a sharded generation-aware registry and immutable configuration
   service.
4. Implement a finite-queue admission policy and measure control latency,
   starvation, priority inversion, false caller priority/cost claims, and retry
   amplification under overload.
5. Add a simple append-only log and immutable checkpoint store; inject power
   failure after every write step.
6. Split one driver and one network protocol into protected service domains,
   then exercise crash, reconnect, reset, and indeterminate completion.
7. Separate bounded telemetry from a small durable audit ledger.

### Distributed prototypes

1. Implement scoped weak membership and eventual group discovery.
2. Select and pin a replicated-state-machine implementation; audit its stable
   storage, membership change, snapshot, and recovery paths.
3. Issue scoped authenticated lease/fence proofs, define conservative holder
   and grantor deadlines, enter jeopardy before renewal becomes unsafe, and
   atomically recover sink high-water state at storage, device, network, and
   update boundaries.
4. Partition the network asymmetrically, delay old traffic, pause CPUs, change
   clock rate, lose quorum, and reconfigure membership during recovery.
5. Rotate workload credentials while the issuer is unavailable and document
   fail-open or fail-closed behavior per operation class.
6. Roll out mixed versions through a cell while old and new protocol profiles
   coexist.

### Compatibility work

- Pin OTP 29.0.6 behaviour, supervisor, application, registry, configuration,
  Logger, distribution-gateway, and release features that the first profile
  promises.
- Differentially test success, exit reasons, ordering, late replies, timeout,
  automatic shutdown, dependency handling, code change, and logging adapter
  behavior against the reference runtime.
- Treat standard distributed Erlang as an explicitly trusted compatibility
  adapter, not the default authority model.
- Identify intentional differences such as bounded fanout queues,
  capability-gated `sys` operations, immutable configuration, and
  least-authority remote operations.

## Findings

### Supported provisional conclusions

- Behaviours and supervision should remain unprivileged libraries and service
  actors.
- Restart is not durable recovery, timeout is not cancellation, and a new
  process generation does not resolve accepted external effects.
- Names, workload identity, actor identity, capability authority, metadata
  revision, and recovery fencing must remain distinct.
- A weak membership detector cannot directly revoke authoritative ownership.
- A quorum metadata service should coordinate small control state, not become
  the bulk data plane.
- Every exclusive takeover needs a monotonically increasing fence checked at
  the actual effect sink; the proof is scoped and authenticated, and the sink's
  high-water generation survives restart.
- Signed code rollback cannot undo migrated durable data or effects already
  visible outside the controlled system.
- Lossy telemetry cannot serve as a complete audit log.

These conclusions are synthesized in the [OTP-like system services
layer](../20-notes/otp-like-system-services-layer.md).

### Evidence still missing

- A complete executable service-manifest schema and bootstrap authority audit.
- A proved cancellation and accepted-operation state machine across runtime,
  device, network, and storage boundaries.
- Storage-medium measurements and power-loss behavior on target hardware.
- A selected replicated-state-machine implementation and reproducible
  fault-injection results.
- Clock and pause bounds sufficient for safe lease use.
- Embedded footprint and scheduling-interference measurements for membership,
  consensus, identity, logging, and update services.
- An OTP compatibility matrix backed by differential tests.
- Usability evidence that applications handle explicit uncertainty and
  overload states correctly.
- Recovery exercises in which the failing component is the root controller,
  registry, storage service, credential issuer, updater, or audit sink.

## Outcome

No architecture has yet satisfied the operational question. The current best
candidate is the thirteen-component, unprivileged federation developed in the
[detailed report](../20-notes/otp-like-system-services-layer.md), with
component details inventoried by the [component
index](../20-notes/otp-like-system-services-components/README.md), and
supporting evidence routed by the [topic
map](../10-maps/otp-like-system-services.md). The [2026-09-04 component
research session](../50-journal/2026-09-04-otp-like-system-services-components-deep-dive.md)
records exact source provenance and evidence limits. The architecture remains
a proposal until the models, prototypes, conformance tests, and failure
experiments above succeed.
