---
title: "OTP-like system services"
kind: map
created: "2026-09-03"
tags:
  - distributed-systems
  - fault-tolerance
  - operating-systems
  - otp
  - service-management
  - supervision
aliases:
  - "System services layer"
  - "OTP-like services map"
---

# OTP-like system services

## Scope

This map covers the fourth layer in the proposed Atom OS decomposition:
unprivileged operational policy built over the managed actor runtime and the
minimal capability kernel. It includes behaviours, supervision, application
lifecycle, naming, configuration and identity, durable state, device and
network service policy, distributed control, updates, overload, telemetry,
audit, and operator control.

The map deliberately separates four things often hidden behind “service
management”:

- observation of actor, domain, device, or peer behavior;
- authority to name, configure, replace, or operate a resource;
- durable evidence about accepted work and committed state; and
- recovery policy after a declared failure.

All components remain ordinary services or libraries. Authority does not imply
CPU privilege, and a service that supervises others still needs an independent
holder outside its own failure boundary.

## Start here

- [OTP-like system services layer: architecture, evidence, and implementation
  plan](../20-notes/otp-like-system-services-layer.md) — the integrated
  synthesis, thirteen-component architecture, lifecycle and failure
  invariants, implementation stages, and evaluation matrix.
- [What contract should the OTP-like system-services layer
  provide?](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
  — the operational standard, hypotheses, falsifiers, prototype program, and
  remaining evidence gaps.
- [2026-09-03 OTP-like system services deep
  dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md) —
  research scope, current documentation baseline, primary-source selection,
  synthesis method, and limitations.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
  — the original decomposition that placed OTP-style policy above the managed
  runtime.

## Component route

### Lifecycle and local composition

- **0. Service-domain bootstrap and manifest controller** validates immutable
  desired state, reserves resources, prepares services privately, and
  atomically publishes generations.
- **1. Behaviour engines and management protocol** preserve reusable
  server/state-machine patterns while making management capability-gated and
  bounded.
- **2. Supervision and recovery policy** adds typed evidence, restart budgets,
  backoff, recovery reserve, state recovery, and escalation to OTP's
  hierarchical policy.
- **3. Application lifecycle and dependency orchestration** turns dependency,
  readiness, drain, and stop rules into explicit transactional state machines.

Primary routes:

- [OTP 29.0.6 system-services
  documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)
- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md)
- [Microreboots](../30-sources/candea-et-al-2004-microreboot.md)
- [Borg](../30-sources/verma-et-al-2015-borg.md)

### Names, configuration, identity, and durable outcomes

- **4. Naming, registry, and local discovery** maps stable names to
  incarnation-aware, attenuated handles and separates unique ownership from
  eventual groups.
- **5. Configuration, workload identity, and secrets** publishes immutable
  validated snapshots and rotates short-lived identity material through a
  separate least-authority channel.
- **6. Durable state and outcome recovery** uses a simple WAL/checkpoint
  baseline with ordered replay cuts, explicit operation IDs, proved commit
  points, and semantic compensation for selected workflows.

Primary routes:

- [ARIES](../30-sources/mohan-et-al-1992-aries.md)
- [RIFL](../30-sources/lee-et-al-2015-rifl.md)
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md)
- [Remote procedure calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md)
- [SPIFFE Workload API](../30-sources/spiffe-project-2026-workload-api.md)

### Devices, networking, and distributed authority

- **7. Device-service policy and management** gives isolated drivers
  generation-bound operations, reset policy, and indeterminate-completion
  ledgers over lower-layer device capabilities.
- **8. Network endpoint and protocol services** gives capability-scoped local
  endpoints, authenticated peers, bounded flow control, and explicit
  acceptance/outcome semantics.
- **9. Distributed membership, discovery, and coordination** separates an
  available observational plane from quorum-backed authoritative metadata,
  leases, and sink-enforced fencing.

Primary routes:

- [Nooks](../30-sources/swift-et-al-2003-nooks.md)
- [Recovering device drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md)
- [CuriOS](../30-sources/david-et-al-2008-curios.md)
- [Unreliable failure
  detectors](../30-sources/chandra-toueg-1996-failure-detectors.md)
- [SWIM](../30-sources/das-et-al-2002-swim.md)
- [Chubby](../30-sources/burrows-2006-chubby.md)
- [Raft](../30-sources/ongaro-ousterhout-2014-raft.md)
- [PARTISAN](../30-sources/meiklejohn-et-al-2019-partisan.md)
- [Scaling Reliably](../30-sources/trinder-et-al-2017-scaling-reliably.md)

### Change, overload, and operations

- **10. Release, update, rollback, and state migration** authenticates
  immutable artifacts and records freshness, preparation, canary, quiescence,
  resumable shadow migration, atomic publication, compatibility, commit, and
  rollback boundaries.
- **11. Admission, overload, and service-resource governance** uses finite
  queues, server-derived classes, fairness rules, budgets, backpressure,
  shedding, degradation, retry limits, and protected control reserves.
- **12. Observability, audit, alarms, and operator control** separates lossy
  telemetry, bounded crash evidence, persistent alarm state, and durable
  tamper-evident intent/effect/outcome audit.

Primary routes:

- [SEDA](../30-sources/welsh-et-al-2001-seda.md)
- [DAGOR](../30-sources/zhou-et-al-2018-dagor.md)
- [Practical dynamic software updating with
  Ginseng](../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md)
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md)
- [The Update Framework](../30-sources/samuel-et-al-2010-tuf.md)
- [Dapper](../30-sources/sigelman-et-al-2010-dapper.md)
- [Secure audit logs](../30-sources/schneier-kelsey-1999-secure-audit-logs.md)
- [DTrace](../30-sources/cantrill-et-al-2004-dtrace.md)

## Architectural boundaries

### Below this layer

- [Managed actor runtime](managed-actor-runtime.md) owns BEAM execution,
  lightweight actors, process-local tracing collection, signals, mailboxes,
  timers, links, monitors, aliases, code versions, and runtime-level evidence.
- [Minimal privileged kernel](minimal-privileged-kernel.md) enforces protected
  domains, capabilities, bounded IPC, scheduling budgets, faults, revocation,
  and safe teardown.
- [Kernel hardware and architecture
  support](kernel-hardware-and-architecture-support.md) owns privileged entry,
  translation, interrupts, raw time, CPU coordination, DMA, and architecture
  fault capture.

The services layer consumes those mechanisms. It does not redefine them or
move supervision, registries, storage policy, release logic, or remote trust
into privileged code.

### Above this layer

Applications supply domain-specific protocols, persistent schemas,
compensating actions, and business correctness. A generic saga engine cannot
invent a safe compensation, and a generic supervisor cannot decide whether an
application effect is semantically valid.

## Key distinctions to preserve

- Process exit is an observation; restart is policy; durable recovery is a
  separate proof.
- A call timeout ends waiting; it does not cancel accepted work.
- A name is not identity; authenticated identity is not authority.
- Weak membership suspicion is not authoritative removal.
- A consensus leader is not an exclusive effect owner unless sinks validate
  its fencing generation.
- Replicated metadata is not bulk storage or application transaction logic.
- Code/configuration rollback does not reverse migrated data or external
  effects.
- Sampled or lossy telemetry is not an audit ledger.
- A health probe is not a correctness or authorization oracle.
- Reserved recovery capacity is not spare application capacity.

## Open questions

- [What contract should the OTP-like system-services layer
  provide?](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- Which exact OTP 29.0.6 behavior and application semantics form the first
  compatibility profile?
- Can one small manifest schema express authority, resource, lifecycle,
  recovery, update, and evidence requirements without becoming an unsafe
  universal policy language?
- What storage profile is sufficient for the first persistent services on
  target hardware?
- Which replicated-state-machine implementation has acceptable proof,
  footprint, stable-storage behavior, and reconfiguration semantics?
- Can every storage, device, network, and update effect sink enforce a
  monotonic fence?
- Which services remain available during loss of configuration, identity,
  audit, or coordination dependencies?
- How should explicit indeterminate outcomes be exposed to ordinary BEAM/OTP
  applications without encouraging unsafe retry?
- What is the minimum operator authority needed to diagnose and recover a
  service while preserving audit and tenant isolation?
