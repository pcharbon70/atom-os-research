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
