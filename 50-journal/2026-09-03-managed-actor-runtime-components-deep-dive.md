---
title: "2026-09-03 managed actor runtime components deep dive"
kind: journal
created: "2026-09-03"
tags:
  - actor-model
  - beam
  - literature-review
  - research-method
  - virtual-machines
aliases:
  - "Managed actor runtime component research session"
---

# 2026-09-03 managed actor runtime components deep dive

## Observations

This session expanded all thirteen proposed components in the [managed actor
runtime layer](../20-notes/managed-actor-runtime-layer.md) into individual
implementation research reports under the [managed actor runtime components
directory](../20-notes/managed-actor-runtime-components/README.md).

The common result is a two-level, incarnation-safe architecture. The kernel
enforces native domains, capabilities, memory, scheduling time, endpoints, and
teardown. The unprivileged runtime implements actors, BEAM execution, terms,
process-local tracing collection, signal semantics, reductions, timers, code,
and runtime evidence. OTP-like services remain responsible for supervision,
application policy, durable recovery, naming, and distribution policy.

The strongest cross-component conclusions are:

- bootstrap, code loading, spawn, signal admission, timers, native requests,
  gateway sends, and resource allocation all need explicit prepare/reserve,
  publish, terminal, rollback, and generation rules;
- BEAM compatibility is a versioned behavioral profile, not the `.beam` suffix
  or current ERTS's internal instruction/data structures;
- actor identity is a route and incarnation, not a kernel capability;
- private actor heaps with automatic local tracing collection and ordinary
  message copying remain the compatible baseline; zero-copy extensions require
  stronger immutable/ownership evidence;
- reductions select actor activations, while kernel-accounted time enforces
  domain authority and exposes expensive BIF, GC, signal, trace, and cleanup
  paths;
- timers and asynchronous I/O require generation-safe terminal arbitration;
  cancellation cannot be assumed to remove an operation already in flight;
- an interpreter-first implementation offers the clearest conformance oracle;
  load-time native lowering follows only after exact safe-point/root metadata
  and W^X publication are working;
- native code and drivers belong in protected, budgeted service domains by
  default; dirty scheduling is not memory or authority isolation;
- distribution belongs behind authenticated, attenuated, credit-bound gateway
  sessions whose epochs delimit ordering and failure knowledge;
- the runtime publishes typed evidence and bounded cleanup, OTP-like services
  choose restart policy, and an outer service restarts a failed runtime domain;
- resource control requires hierarchical reserve-before-publish ledgers that
  include shared tables, binaries, deferred work, tracing, and fragmentation,
  not only per-process heap limits; and
- production traces, deterministic test schedules, and crash evidence have
  different completeness contracts, with kernel-owned minimum evidence outside
  the runtime's failure boundary.

These are research proposals. No runtime component was implemented, executed,
benchmarked, model-checked, or compared experimentally with ERTS in this
session.

## Environment

- Repository: `atom-os-research`
- Research date: 2026-09-03
- Host time zone: America/Toronto
- Activity: scientific-paper, official-documentation, article/blog review,
  synthesis, and archive editing
- Compatibility reference reviewed: Erlang/OTP 29.0.6, ERTS 17.0.6, released
  2026-09-01
- Pinned implementation audit already in the archive: Erlang/OTP 29.0.5 / ERTS
  17.0.5 at source revision `5cf5f9725452`
- Runtime prototype: none built or executed
- Kernel, emulator, and physical target: none used
- Native service, device, and network target: none used
- Local experiments: none
- Local artifacts: Markdown reports, source records, maps, inquiry updates, and
  this journal entry

The one-patch difference between the current documentation baseline and the
pinned source audit is kept explicit. Public OTP 29.0.6 behavior informs the
proposed profile; internal implementation claims remain tied to the 29.0.5
audit until the newer source tree is independently pinned and examined.

## Evidence

### Research question and standard

For every component, the operational question was:

> Which implementation best preserves the declared BEAM/ERTS behavior while
> keeping the runtime unprivileged, actor work pre-emptible and accountable,
> service authority attenuated, failure evidence honest, and the whole design
> testable against one pinned profile?

A recommendation was accepted only when the report:

- separated normative behavior, current implementation, research evidence,
  architecture synthesis, and unverified proposal;
- identified object ownership, authority, generations, publication and
  terminal points, failure modes, and bounded work;
- compared material alternatives and retained negative evidence;
- stated at least one falsifier or decisive experiment; and
- remained consistent with the already researched architecture-support and
  minimal-kernel layers.

### Method

The existing thirteen-component decomposition supplied the scope. Source work
was divided into three evidence passes:

1. bootstrap/adapter, loader/verifier, actor lifecycle, and term memory/GC;
2. signals/mailboxes, scheduling, timers/I/O, and code execution/publication;
3. native work, distribution, failure translation, resource control/tables,
   and observability/replay/crash evidence.

Each pass sought primary papers and official project documentation first, then
maintainer articles or engineering blogs for implementation detail and
negative operational evidence. Search snippets and abstracts located sources
but were not used to support detailed conclusions. A claim/source ledger was
kept during synthesis, and every substantively used new primary work received
an individual note in the [source index](../30-sources/README.md).

Existing source records were reused for current ERTS behavior, scheduler
activations, scheduling-context capabilities, message passing, garbage
collection, locality-aware scheduling, driver containment, failure detection,
microreboot, distribution scaling, deterministic testing, and crash capture.

### Component reports

#### Domain, compatibility, identity, and memory

- [Runtime-domain bootstrap and kernel adapter](../20-notes/managed-actor-runtime-components/runtime-domain-bootstrap-and-kernel-adapter.md)
- [Compatibility manifest, BEAM loader, and verifier](../20-notes/managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier.md)
- [Actor identity, lifecycle, and process state](../20-notes/managed-actor-runtime-components/actor-identity-lifecycle-and-process-state.md)
- [Terms, private heaps, shared binaries, and tracing collection](../20-notes/managed-actor-runtime-components/terms-private-heaps-shared-binaries-and-tracing-collection.md)

#### Signals, scheduling, time, and execution

- [Signal ingress, mailboxes, and selective receive](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive.md)
- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Timers, events, and asynchronous I/O integration](../20-notes/managed-actor-runtime-components/timers-events-and-asynchronous-io-integration.md)
- [Code execution, safe points, and version publication](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication.md)

#### Services, distribution, failure, resources, and evidence

- [Native work, ports, and drivers](../20-notes/managed-actor-runtime-components/native-work-ports-and-drivers.md)
- [Distribution gateway and remote actor semantics](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics.md)
- [Failure translation and the OTP boundary](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary.md)
- [Resource accounting and overload control](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control.md)
- [Observability, deterministic testing, and crash evidence](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md)

### Newly preserved primary sources

This session added individual records for:

- proof-carrying code and consumer-side validation;
- Michael–Scott concurrent queues and the limits of queue-level linearizability;
- Blumofe–Leiserson work stealing and its fully strict computation assumptions;
- Varghese–Lauck timing wheels and their granularity/burst trade-offs;
- HiPErJiT and profile-driven Erlang JIT compilation;
- resource containers and causal resource attribution;
- contention-adapting ordered sets and workload-sensitive shared tables;
- Concuerror and systematic Erlang schedule exploration;
- deterministic actor-language record/replay;
- Orleans virtual actors and stable logical identity as a higher service model;
- crash-only software and externally coordinated restart;
- a NUMA-aware actor runtime and topology-sensitive scheduling;
- PARTISAN and replaceable distributed-actor topologies;
- mailbox types and optional statically checked protocol profiles;
- ETS scalability and table-structure contention;
- Birrell–Nelson RPC and ambiguous failure outcomes; and
- HiPE's integrated native Erlang execution conventions.

### Shared review questions

Every report was challenged with the same questions:

- What behavior is promised by the selected OTP/BEAM profile, and what is only
  current ERTS machinery?
- Which object owns every mutable byte, queue position, relation, request,
  timer, code generation, and charge?
- Which generation or epoch prevents late work from reaching a replacement?
- What is reserved before work, where is the publication point, and what
  terminal evidence permits release?
- Which loops and slow paths can allocate, block, scan, collect, compile,
  reclaim, or wait without a safe point?
- Which failure is local actor exit, runtime corruption, service loss,
  connection loss, kernel fault, resource refusal, or only liveness suspicion?
- What authority crosses the boundary, and can a PID, term, module, remote
  frame, NIF, or diagnostic request manufacture kernel authority?
- What happens when cancellation races with completion, exit, restart,
  reconnect, code replacement, table transfer, or resource exhaustion?
- Which measurement would falsify the preferred implementation?
- Does the proposal accidentally move OTP policy into the runtime or ERTS
  internals into the kernel ABI?

This review produced a common vocabulary of private staging, hierarchical
reservation, immutable publication, incarnation-bound identities, terminal
arbitration, safe-point progress, recovery reserve, typed uncertainty, and
bounded external evidence.

### Post-merge semantic correction audit

A later line-by-line comparison against the OTP 29.0.6 manuals found several
places where the initial synthesis accidentally promoted an Atom OS mechanism
to an OTP promise or carried forward older ERTS behavior. The corrective pass
used the current `erlang`, `erl_nif`, `ets`, process, and external-term-format
documentation and made these distinctions explicit:

- logical old-code purge checks direct executable references; local funs and
  literals require invalidation/copy handling but are not OTP 29 purge blockers;
- dirty classification is per NIF name/arity entry and can change when a job is
  rescheduled, rather than being one immutable module-wide class;
- Atom OS request outcomes are an extension beneath the OTP send API, not new
  return values from `!/2`, `send/2`, or `send/3`;
- standard remote PIDs and references are tied to node creation and identifier
  fields, not to one transport session, even though links and monitors break on
  a connection failure;
- the compatible failure path preserves exact Erlang exit reasons;
- timer cleanup follows the timer destination rather than its creator; and
- ETS owner death, heir data, notification, and explicit `give_away/3` remain
  observably distinct operations.

No executable conformance test accompanied this correction. The amended
reports therefore add focused differential tests for each distinction.

### Evidence boundary

This work did not:

- parse or execute a BEAM module;
- run an OTP conformance or differential test;
- implement a process heap, collector, signal queue, scheduler, timer, table,
  loader, interpreter, JIT, gateway, native service, or crash recorder;
- measure throughput, latency, GC pauses, fairness, NUMA traffic, overload,
  trace overhead, restart, or teardown;
- model-check any proposed state machine;
- fuzz a loader, external-term decoder, trace/dump parser, or cancellation
  protocol;
- inject a native, device, network, runtime, kernel, or power fault; or
- demonstrate the declared compatibility profile on Atom OS hardware.

Therefore paper measurements apply only to their evaluated systems and
workloads; current OTP documentation is normative only for the documented
release; maintainer articles explain implementations but are not formal
specifications; and every “best implementation” in these notes is a bounded
cross-source recommendation awaiting the stated experiments.

## Source manifest

The classification records the session in which each source note first entered
the archive. Sources introduced by the preceding managed-runtime synthesis are
therefore reused here even though both sessions were committed together later.

### Newly introduced sources

- [Proof-carrying
  code](../30-sources/necula-1997-proof-carrying-code.md) — producer-side proof
  generation with a smaller consumer-side validation boundary.
- [Simple, fast, and practical non-blocking and blocking concurrent queue
  algorithms](../30-sources/michael-scott-1996-concurrent-queue-algorithms.md)
  — queue linearizability and the limits of a queue-level guarantee.
- [Scheduling multithreaded computations by work
  stealing](../30-sources/blumofe-leiserson-1999-work-stealing.md) — formal
  work-stealing bounds and their fully strict computation assumptions.
- [Hashed and hierarchical timing
  wheels](../30-sources/varghese-lauck-1987-timing-wheels.md) — timer structure,
  granularity, and expiration-burst trade-offs.
- [HiPErJiT: A profile-driven just-in-time compiler for
  Erlang](../30-sources/kallas-sagonas-2018-hiperjit.md) — profile-directed
  native compilation evidence and deoptimization constraints.
- [Resource containers](../30-sources/banga-et-al-1999-resource-containers.md)
  — request-causal resource attribution beyond process ownership.
- [A contention adapting approach to concurrent ordered
  sets](../30-sources/sagonas-winblad-2018-contention-adapting-ordered-sets.md)
  — workload-sensitive shared-table adaptation.
- [Systematic testing for detecting concurrency errors in Erlang
  programs](../30-sources/christakis-et-al-2013-concuerror.md) — stateless
  schedule exploration for Erlang concurrency.
- [Efficient and deterministic record and replay for actor
  languages](../30-sources/aumayr-et-al-2018-actor-record-replay.md) — actor
  record/replay design and event-capture requirements.
- [Orleans: Distributed virtual actors for programmability and
  scalability](../30-sources/bernstein-et-al-2014-orleans.md) — stable logical
  actor identity as a higher-level service model.
- [Crash-only
  software](../30-sources/candea-fox-2003-crash-only-software.md) — externally
  coordinated restart and crash-oriented component boundaries.
- [A NUMA-aware runtime environment for the actor
  model](../30-sources/francesquini-et-al-2013-numa-aware-actor-runtime.md) —
  topology-aware scheduling and memory placement.
- [PARTISAN: Scaling the distributed actor
  runtime](../30-sources/meiklejohn-et-al-2019-partisan.md) — replaceable
  distributed-actor topologies and connection structure.
- [Special delivery: Programming with mailbox
  types](../30-sources/fowler-et-al-2023-mailbox-types.md) — optional static
  protocol checking without redefining ordinary BEAM mailboxes.
- [On the scalability of the Erlang Term
  Storage](../30-sources/klaftenegger-et-al-2013-ets-scalability.md) — ETS
  contention and table-structure scaling evidence.
- [Implementing remote procedure
  calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md) — ambiguous
  remote outcomes and call/reply protocol foundations.
- [A high performance Erlang
  system](../30-sources/johansson-et-al-2000-high-performance-erlang.md) — HiPE's
  integrated native execution and runtime conventions.

### Reused sources

- [Scheduler
  activations](../30-sources/anderson-et-al-1992-scheduler-activations.md) —
  two-level scheduling and kernel-to-runtime processor-allocation boundaries.
- [Erlang/OTP 29.0.6 managed-runtime
  documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
  — current public behavior for all thirteen component contracts.
- [Erlang/OTP source tree at
  5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) —
  pinned implementation dependencies and ERTS mechanisms.
- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
  — actor lifecycle, failure signaling, and supervision principles.
- [A History of
  Erlang](../30-sources/armstrong-2007-history-of-erlang.md) — historical
  process, VM, distribution, and operational design constraints.
- [A scalability benchmark suite for
  Erlang/OTP](../30-sources/aronis-et-al-2012-scalability-benchmark-suite-erlang-otp.md)
  — multidimensional evaluation design.
- [Work-Stealing, Locality-Aware Actor
  Scheduling](../30-sources/barghi-karsten-2018-locality-aware-actor-scheduling.md)
  — actor locality and NUMA-sensitive stealing.
- [Tolerating malicious device
  drivers](../30-sources/boyd-wickizer-zeldovich-2010-malicious-device-drivers.md)
  — containment limits under actively hostile native services.
- [Microreboot—A technique for cheap
  recovery](../30-sources/candea-et-al-2004-microreboot.md) — selective restart
  and outer recovery coordination.
- [Unreliable failure detectors for reliable distributed
  systems](../30-sources/chandra-toueg-1996-failure-detectors.md) — separation of
  suspicion from authoritative failure knowledge.
- [Finding Race Conditions in Erlang with QuickCheck and
  PULSE](../30-sources/claessen-et-al-2009-quickcheck-pulse.md) — controlled
  schedules for differential concurrency tests.
- [Orca: GC and Type System Co-Design for Actor
  Languages](../30-sources/clebsch-et-al-2017-orca.md) — ownership assumptions
  required by zero-copy collection.
- [Secure Virtual
  Architecture](../30-sources/criswell-et-al-2007-secure-virtual-architecture.md)
  — typed execution and consumer-side validation boundaries.
- [Exokernel](../30-sources/engler-et-al-1995-exokernel.md) — separation of
  privileged protection/revocation from runtime resource policy.
- [Kdump](../30-sources/goyal-et-al-2005-kdump.md) — failure-isolated crash
  capture and preservation.
- [The Road to the
  JIT](../30-sources/gustavsson-2020-road-to-the-jit.md) — BeamAsm code
  publication and implementation history.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) — explicit queue ownership
  and data-path state transitions.
- [Dependable operating-system
  construction](../30-sources/herder-et-al-2006-dependable-operating-system.md)
  — isolated driver services and recovery boundaries.
- [A brief introduction to
  BEAM](../30-sources/hogberg-2020-brief-introduction-to-beam.md) — instruction,
  register, frame, and safe-point background.
- [A few notes on message
  passing](../30-sources/hogberg-2021-message-passing.md) — signal queues,
  message copying, ordering, and selective receive.
- [Scheduling-context
  capabilities](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)
  — kernel-accounted temporal authority delegated to runtime schedulers.
- [Arrakis](../30-sources/peter-et-al-2014-arrakis.md) — delegated data paths and
  their protection/management boundary.
- [Efficient memory management for concurrent programs that use message
  passing](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md)
  — private heaps, tracing collection, and message copying.
- [seL4 Reference
  Manual](../30-sources/sel4-foundation-2026-reference-manual.md) — concrete
  capability, protection-domain, and invocation mechanics.
- [Translation validation for a verified OS
  kernel](../30-sources/sewell-et-al-2013-translation-validation.md) — validating
  generated low-level artifacts outside the producer.
- [Improving the reliability of commodity operating
  systems](../30-sources/swift-et-al-2003-nooks.md) — driver isolation benefits
  and shared-kernel containment limits.
- [Recovering device
  drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md) — device
  state recovery and restart limits.
- [High-resolution
  timekeeping](../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md)
  — raw-clock conversion and precision trade-offs beneath runtime timers.
- [Scaling Reliably: Improving the Scalability of the Erlang Distributed Actor
  Platform](../30-sources/trinder-et-al-2017-scaling-reliably.md) — distributed
  Erlang topology and scaling limits.
- [The Many-to-One Parallel Signal Sending
  Optimization](../30-sources/winblad-2021-parallel-signal-sending.md) —
  adaptive sender-striped signal ingress.
- [Characterizing the scalability of Erlang VM on many-core
  processors](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md) —
  scheduler and shared-runtime bottleneck evidence.

## Threads

- [Managed actor runtime map](../10-maps/managed-actor-runtime.md) now routes
  through the thirteen detailed reports and their evidence families.
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
  remains open because no compatibility, latency, resource, native-fault,
  distribution, replay, or recovery experiment has been completed.
- [Minimal privileged kernel](../20-notes/minimal-privileged-kernel-layer.md)
  owns the capabilities, domains, scheduling contexts, bounded IPC, fault
  routes, and teardown mechanisms consumed by these designs.
- [Kernel hardware and architecture support](../20-notes/kernel-hardware-and-architecture-support-layer.md)
  owns the privileged machine protocols beneath that kernel.

## Follow-ups

1. Pin and audit the OTP 29.0.6 source tree, then turn the compatibility
   manifest into executable data.
2. Implement the smallest deterministic interpreter covering spawn, private
   heaps, tracing collection, copy send, selective receive, links, monitors,
   aliases, exceptions, and timers.
3. Build executable state models for spawn/exit, signal publication, timer/I/O
   cancellation, code publication/reclamation, native requests, gateway epochs,
   resource reservations, and crash sealing.
4. Differentially test the profile against OTP 29.0.6 and preserve every
   mismatch as a minimized fixture.
5. Measure safe-point, scheduling, receive-scan, GC, timer, native/gateway,
   table, tracing, overload, restart, and teardown tails under kernel quotas.
6. Keep the inquiry open until those artifacts, commands, configurations, and
   raw results are recorded in later journal entries.
