---
title: "2026-09-03 OTP-like system services deep dive"
kind: journal
created: "2026-09-03"
tags:
  - distributed-systems
  - fault-tolerance
  - literature-review
  - operating-systems
  - otp
  - service-management
aliases:
  - "OTP-like services research session"
---

# 2026-09-03 OTP-like system services deep dive

## Observations

The fourth proposed Atom OS layer was researched as ordinary system policy
above the managed actor runtime, not as a larger privileged kernel. The
strongest design is a federation of capability-confined service domains rather
than one immortal application controller. OTP behaviours and supervision
remain the local composition language, while persistence, overload,
distribution, identity, update, and audit each receive an explicit contract.

Several distinctions materially changed the architecture:

- a service name, an actor identifier, an authenticated workload identity, a
  capability, and an ownership fence are different objects;
- a call timeout stops waiting but does not cancel accepted work;
- process or domain restart does not prove persistent recovery or the outcome
  of an external effect;
- health probes and weak membership provide observations, not authoritative
  removal;
- exclusive distributed ownership requires ordered metadata plus fencing at
  every actual effect sink;
- a consensus service should hold small authoritative metadata, not bulk
  application state;
- release rollback can restore code and configuration only while compatible
  data and external effects remain reversible;
- admission and degradation must protect a healthy saturated service before
  supervisors interpret overload as repeated failure; and
- logs, metrics, sampled traces, crash evidence, alarm state, and security
  audit have different loss and integrity requirements.

## Environment

- Research date: 2026-09-03, America/Toronto.
- Repository: `atom-os-research`, local Git worktree.
- Current official baseline reviewed: Erlang/OTP 29.0.6, released 2026-09-01.
- Existing implementation evidence retained: the archive's pinned Erlang/OTP
  29.0.5 source-tree audit.
- Kernel, runtime, storage target, network, simulator, or physical hardware:
  none; this session was literature review and architecture synthesis.
- Host dependencies used for evidence: repository text search and public
  official documentation, publication pages, and papers.
- No service implementation, benchmark, model check, power-loss test, network
  partition, or fault-injection artifact was produced.

## Evidence

### Archive review

Before drafting, the repository instructions, archive guide, schema, templates,
destination indexes, home map, original BEAM/ERTS/OTP synthesis, managed actor
runtime report, minimal privileged-kernel report, and existing source notes
were read.

The original decomposition assigned supervisors, behaviours, device-service
policy, naming, storage, networking, update orchestration, metrics, and
configuration to an “OTP-like system services” layer. Repository searches
found no integrated report, topic map, or open inquiry devoted to that layer.

Existing evidence reused includes:

- Armstrong on fault containment, supervision, stable storage, and software
  change;
- Birrell and Nelson on RPC ambiguity;
- Candea and Fox on crash-only design and microreboots;
- Chandra and Toueg on failure detectors;
- Trinder et al. and PARTISAN on distributed Erlang topology and scale;
- Nooks, driver recovery, and CuriOS on isolated device services;
- DTrace on dynamic observability; and
- the lower-layer Atom OS reports on capability, domain, resource, failure,
  teardown, and runtime contracts.

### Current official OTP documentation

The official OTP 29.0.6 pages were read for:

- `gen_server`, including correlated calls, casts, late replies,
  `terminate`, and code change;
- `gen_statem`, including explicit transitions, postponed events, time-outs,
  and migration;
- `gen_event` and the implications of running handlers through one manager;
- `sys` cooperative suspend, resume, inspect, change-code, and termination;
- supervisor ordering, restart strategies, restart intensity, significant
  children, and automatic shutdown;
- application controller/master, dependency, start type, configuration, and
  distributed-application behavior;
- local names, `via` registries, `global`, and `pg`;
- release staging, `appup`/`relup`, synchronized updates, purge, and
  point-of-no-return behavior;
- Logger handlers, filtering, proxy delivery, and overload modes;
- `proc_lib` crash reports, legacy SASL-compatible event formats, and alarm
  facilities; and
- distributed Erlang, TLS distribution, cookies, trust, and signal loss.

These manuals define supported public behavior, not proof of crash consistency,
resource bounds, security, or representative performance. OTP's “kernel”
application is a package name and was not treated as privileged operating
system code.

### Scientific and systems papers

New evidence records were created for:

- Das, Gupta, and Motivala (2002), SWIM membership and failure detection, DOI
  `10.1109/DSN.2002.1028914`;
- Burrows (2006), Chubby coordination, leases, sessions, invalidation, and
  sequencers;
- Ongaro and Ousterhout (2014), Raft consensus and membership change;
- Welsh et al. (2001), staged event-driven architecture and explicit admission,
  DOI `10.1145/502034.502057`;
- Mohan et al. (1992), ARIES logging and recovery, DOI
  `10.1145/128765.128770`;
- Lee et al. (2015), RIFL retryable request assumptions, DOI
  `10.1145/2815400.2815416`;
- Garcia-Molina and Salem (1987), Sagas and semantic compensation, DOI
  `10.1145/38713.38742`;
- Verma et al. (2015), Borg desired-state cluster management, DOI
  `10.1145/2741948.2741964`;
- Dolstra et al. (2008), NixOS declarative immutable system closures and atomic
  profile generation selection;
- Neamtiu et al. (2006), Ginseng safe points and state transformation, DOI
  `10.1145/1133981.1133991`;
- Samuel et al. (2010), compromise-resilient software update metadata;
- Zhou et al. (2018), DAGOR overload control, DOI
  `10.1145/3267809.3267823`;
- Sigelman et al. (2010), Dapper distributed tracing; and
- Schneier and Kelsey (1999), forward-integrity protection for audit logs.

The substantive claims are linked from the synthesis to the relevant source
records.

### Official standards and engineering material

The current official SPIFFE Workload API standard was reviewed at repository
revision `99470b9abc825f14aa364dfa2c3b53b02ba5db5b` for local workload
credential delivery, caller attribution, update streaming, private-key
handling, and trust-bundle distribution. Its authenticated identity contract
was kept separate from authorization, attestation policy, issuer availability,
and Atom OS capability derivation.

The Update Framework paper and project model informed signed artifact metadata,
threshold roles, version/freshness checks, and compromise recovery. Current OTP
engineering documentation and source-backed archive notes supplied the
practitioner view of supervision, logging, releases, distribution, and
operational trade-offs.

Two official engineering blog posts were also read for historical motivation:
Lukas Larsson's [“Erlang/OTP 24
Highlights”](../30-sources/larsson-2021-erlang-otp-24-highlights.md)
(2021-05-12) describes process aliases and supervisor automatic shutdown, and
Isabell Huang's [“Erlang/OTP 28
Highlights”](../30-sources/huang-2025-erlang-otp-28-highlights.md)
(2025-05-20) uses Logger mailbox overload to motivate priority messages. They
were treated as maintainer context; normative behavior came from the current
manuals.

### Search and selection method

Searches combined the layer name with terms including:

- supervisor semantics, restart intensity, crash-only, microreboot, recovery
  reserve, and desired-state reconciliation;
- application lifecycle, dependency graph, configuration snapshot, workload
  identity, secret rotation, and registry consistency;
- write-ahead logging, checkpoints, exactly-once RPC, idempotency, sagas, and
  crash-consistent state;
- driver restart, device reset, indeterminate I/O, remote procedure calls, and
  reconnect semantics;
- failure detector, SWIM, lease, fencing token, consensus, Raft, Chubby,
  Erlang distribution, PARTISAN, and split brain;
- dynamic software update, transactional deployment, NixOS, TUF, state
  migration, quiescence, and rollback;
- SEDA, overload control, backpressure, retry storm, admission, and DAGOR; and
- distributed tracing, Dapper, secure audit logging, forward integrity,
  alarms, and DTrace.

Primary papers, official specifications, official project documentation, and
author-hosted copies were preferred. Surveys, secondary explanations, and
search snippets were used to discover sources but not as evidence for detailed
claims. Papers were excluded from substantive citation when their mechanism
did not affect the proposed contract or when only a search result was
available.

### Synthesis method

Each claim was classified as:

1. durable OTP/actor-system principle;
2. behavior of current Erlang/OTP;
3. result reported by a primary research source;
4. assumption required by that result;
5. cross-source interpretation; or
6. proposed Atom OS design requiring tests.

The component boundary was then checked against the existing architecture:

- privileged enforcement stays in the hardware/architecture and minimal-kernel
  layers;
- BEAM execution, actor memory, scheduling, mailboxes, signals, timers, links,
  monitors, aliases, and code mechanisms stay in the managed runtime;
- lifecycle, naming, storage, device/network policy, distribution trust,
  updates, and operations stay here; and
- application-specific schemas, protocols, and compensations remain in
  applications.

The result is one integrated report with thirteen components, reusable
generation and publication invariants, effect-outcome states, failure
propagation rules, implementation stages, an evaluation matrix, provisional
decisions, and falsifiers.

### Post-synthesis review

Independent semantic passes checked current OTP compatibility, persistence and
operations, and distributed safety. They caused the final report to separate
strict OTP adapters from native readiness, supervisor, event, Logger, and
release extensions; to specify authoritative registry reads and scoped
restart-safe fencing; and to narrow retryable-operation claims.

The storage proposal was also strengthened with ordered LSNs, explicit commit
framing, a checkpoint replay cut, and atomic checkpoint-pointer publication.
Update migration now targets a resumable shadow generation and requires
trusted freshness/anti-rollback state. Sensitive control now uses a durable
audit-intent gate followed by a correlated outcome, while acknowledging that
an external effect can remain indeterminate across a crash. These are design
corrections from review, not implementation evidence.

Bibliographic review corrected the SEDA and Ginseng proceedings metadata,
kept the 2008 Nix store characterization input-addressed, and added dedicated
source notes for the two official Erlang/OTP engineering articles.

## Source manifest

The classification records the session in which each source note first entered
the archive. Sources introduced by the managed-runtime component session
earlier on the same date are therefore reused here.

### Newly introduced sources

- [Erlang/OTP 29.0.6 system-services
  documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)
  — current behaviours, supervision, applications, naming, releases, logging,
  alarms, and distribution semantics.
- [SWIM](../30-sources/das-et-al-2002-swim.md) — scalable weak membership and
  failure-detection observations rather than authoritative removal.
- [The Chubby lock
  service](../30-sources/burrows-2006-chubby.md) — leases, sessions,
  invalidation, sequencers, and effect-side fencing.
- [In search of an understandable consensus
  algorithm](../30-sources/ongaro-ousterhout-2014-raft.md) — replicated metadata
  consensus and membership-change constraints.
- [SEDA](../30-sources/welsh-et-al-2001-seda.md) — explicit stage admission,
  queueing, and overload boundaries.
- [Overload control for scaling WeChat
  microservices](../30-sources/zhou-et-al-2018-dagor.md) — call-graph-aware
  admission and overload propagation control.
- [Large-scale cluster management at Google with
  Borg](../30-sources/verma-et-al-2015-borg.md) — desired-state reconciliation,
  placement, health, and controller recovery.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — write-ahead logging,
  checkpoint, analysis, redo, and undo recovery structure.
- [Implementing linearizability at large scale and low
  latency](../30-sources/lee-et-al-2015-rifl.md) — retryable-request identifiers,
  result retention, and restricted exactly-once assumptions.
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md) — durable multi-step
  progress with application-defined compensation.
- [The SPIFFE Workload
  API](../30-sources/spiffe-project-2026-workload-api.md) — authenticated local
  workload credential delivery, rotation streams, and trust-bundle updates.
- [Practical dynamic software updating for
  C](../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md) —
  safe-point update and explicit state transformation constraints.
- [NixOS: A Purely Functional Linux
  Distribution](../30-sources/dolstra-et-al-2008-nixos.md) — immutable closures
  and atomic profile-generation selection.
- [Survivable key compromise in software update
  systems](../30-sources/samuel-et-al-2010-tuf.md) — threshold roles, freshness,
  rollback resistance, and compromise recovery for updates.
- [Dapper](../30-sources/sigelman-et-al-2010-dapper.md) — low-overhead
  cross-service trace correlation and sampling limits.
- [Secure audit logs to support computer
  forensics](../30-sources/schneier-kelsey-1999-secure-audit-logs.md) —
  forward-integrity protection and its completeness limits.
- [Erlang/OTP 24
  Highlights](../30-sources/larsson-2021-erlang-otp-24-highlights.md) —
  maintainer context for aliases, late replies, and supervisor automatic
  shutdown.
- [Erlang/OTP 28
  Highlights](../30-sources/huang-2025-erlang-otp-28-highlights.md) — maintainer
  context for priority messages and Logger mailbox overload.

### Reused sources

- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
  — fault containment, supervision, stable storage, and software change.
- [Implementing remote procedure
  calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md) — ambiguous
  outcomes across call timeouts and communication failure.
- [Crash-only
  software](../30-sources/candea-fox-2003-crash-only-software.md) — cheap restart
  boundaries and externally coordinated recovery.
- [Microreboot—A technique for cheap
  recovery](../30-sources/candea-et-al-2004-microreboot.md) — selective service
  restart and recovery reserves.
- [Unreliable failure detectors for reliable distributed
  systems](../30-sources/chandra-toueg-1996-failure-detectors.md) — formal limits
  on interpreting suspicion as failure knowledge.
- [PARTISAN: Scaling the distributed actor
  runtime](../30-sources/meiklejohn-et-al-2019-partisan.md) — alternative
  distributed-actor topologies and connection policies.
- [Scaling Reliably: Improving the Scalability of the Erlang Distributed Actor
  Platform](../30-sources/trinder-et-al-2017-scaling-reliably.md) — distributed
  Erlang scale, topology, and fault behavior.
- [Improving the reliability of commodity operating
  systems](../30-sources/swift-et-al-2003-nooks.md) — device-driver isolation and
  its shared-kernel limits.
- [Recovering device
  drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md) — device
  reset, state reconstruction, and uncertain I/O outcomes.
- [CuriOS](../30-sources/david-et-al-2008-curios.md) — isolated device-service
  state and restart structure.
- [Dynamic instrumentation of production
  systems](../30-sources/cantrill-et-al-2004-dtrace.md) — safe dynamic
  observability and production tracing boundaries.

## Threads

- [OTP-like system services layer: architecture, evidence, and implementation
  plan](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [What contract should the OTP-like system-services layer
  provide?](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)

## Follow-ups

- Preserve every DOI and immutable version pin when refreshing a source note;
  never rely on the compact journal bibliography alone.
- Turn service references, operation outcomes, manifests, publications,
  leases, fences, updates, and audit records into schemas.
- Model check the lifecycle, supervisor, request, registry, lease, update, and
  audit state machines.
- Select a storage profile and replicated-state-machine implementation only
  after auditing their stable-storage and recovery behavior.
- Create differential OTP behavior tests for the declared compatibility
  surface.
- Implement and measure one deterministic single-node nucleus before
  introducing cluster topology.
- Preserve raw model, benchmark, power-loss, partition, and fault artifacts in
  future journal entries; none exist from this literature-only session.
