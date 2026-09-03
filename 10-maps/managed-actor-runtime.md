---
title: "Managed actor runtime"
kind: map
created: "2026-09-02"
tags:
  - actor-model
  - beam
  - erlang
  - erts
  - garbage-collection
  - message-passing
  - scheduling
  - virtual-machines
aliases:
  - "Managed runtime layer"
  - "BEAM-compatible runtime map"
---

# Managed actor runtime

## Scope

This map covers the third layer in the proposed Atom OS decomposition: an
unprivileged runtime that executes a declared compiled-BEAM profile and owns
cheap actors, term memory, process-local tracing collection, signal and mailbox
semantics, reduction scheduling, timers, shared tables, code loading, and
runtime observability.

The layer is above the minimal capability kernel and below OTP-like system
services. It is one native protection domain unless a deployment deliberately
uses several runtime domains. Actor separation within one domain is a managed
language invariant; it is not page-table isolation from a compromised runtime,
JIT, or in-process NIF.

## Start here

- [Managed actor runtime layer: evidence, contract, and implementation
  plan](../20-notes/managed-actor-runtime-layer.md) — the detailed synthesis,
  proposed component model, critical paths, implementation stages, and
  evaluation matrix.
- [Managed actor runtime component
  index](../20-notes/managed-actor-runtime-components/README.md) — the complete
  local inventory of the thirteen implementation deep dives.
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
  — the open decisions, falsifiers, and minimum experiments.
- [2026-09-02 managed actor runtime deep
  dive](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md) — current
  release, search coverage, source-selection method, and research limitations.
- [2026-09-03 managed actor runtime components deep
  dive](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md) —
  expanded source search, shared implementation criteria, component results,
  and the explicit boundary between research synthesis and tested evidence.

## Component implementation deep dives

The runtime is decomposed into thirteen components numbered 0 through 12. Each
report recommends an implementation while preserving the same unprivileged
runtime, capability-kernel, and OTP-policy boundaries.

### Domain, compatibility, identity, and memory

- [0. Runtime-domain bootstrap and kernel
  adapter](../20-notes/managed-actor-runtime-components/runtime-domain-bootstrap-and-kernel-adapter.md) —
  defines the only kernel-ABI consumer as a transactional, generation-safe,
  idempotent adapter with bounded teardown.
- [1. Compatibility manifest, BEAM loader, and
  verifier](../20-notes/managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier.md) —
  defines precise profiles, private staged parsing, structural and policy
  validation, immutable lowering, and atomic publication.
- [2. Actor identity, lifecycle, and process
  state](../20-notes/managed-actor-runtime-components/actor-identity-lifecycle-and-process-state.md) —
  develops incarnation-safe routing identities, transactional spawn, and
  resumable exit/relation cleanup.
- [3. Terms, private heaps, shared binaries, and tracing
  collection](../20-notes/managed-actor-runtime-components/terms-private-heaps-shared-binaries-and-tracing-collection.md) —
  selects private generational tracing heaps and copy-by-default messages while
  making shared-object retention and collector reserve explicit.

### Signals, scheduling, time, and execution

- [4. Signal ingress, mailboxes, and selective
  receive](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive.md) —
  separates striped physical ingress from logical mailbox order and gives
  admission, scanning, correlation, and overload precise rules.
- [5. Reduction scheduler and kernel scheduling
  contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md) —
  composes reduction pre-emption and adaptive local-first stealing with
  kernel-enforced CPU authority and measured NUMA hints.
- [6. Timers, events, and asynchronous I/O
  integration](../20-notes/managed-actor-runtime-components/timers-events-and-asynchronous-io-integration.md) —
  develops hybrid timer structures, bounded expiry, one-shot events, and
  generation-safe cancellation/completion arbitration.
- [7. Code execution, safe points, and version
  publication](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication.md) —
  defines an interpreter-first path, exact root/safe-point metadata, staged W^X
  code publication, and epoch-based old-code reclamation.

### Services, distribution, failure, resources, and evidence

- [8. Native work, ports, and
  drivers](../20-notes/managed-actor-runtime-components/native-work-ports-and-drivers.md) —
  makes protected service domains the native default and limits in-process
  native code to an explicitly trusted compatibility profile.
- [9. Distribution gateway and remote actor
  semantics](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics.md) —
  defines authenticated, attenuated, credit-bound session epochs without
  fabricating global order or exactly-once effects.
- [10. Failure translation and the OTP
  boundary](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary.md) —
  separates typed observations and bounded cleanup from OTP restart policy and
  moves runtime-domain recovery outside the failed domain.
- [11. Resource accounting and overload
  control](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control.md) —
  develops hierarchical reserve-before-publish ledgers, explicit overload
  states, retained-resource attribution, and bounded ETS-like tables.
- [12. Observability, deterministic testing, and crash
  evidence](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md) —
  separates bounded production tracing, complete declared test schedules, and
  kernel-anchored crash capture outside the runtime failure boundary.

## Trails

### Compatibility and current ERTS behavior

- [Erlang/OTP 29.0.6 managed-runtime
  documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
  records the current public behavior and distinguishes it from private ERTS
  machinery.
- [Erlang/OTP 29.0.5 system
  documentation](../30-sources/erlang-otp-team-2026-otp-29-documentation.md)
  provides the prior deep documentation pass aligned with the pinned source
  audit.
- [Erlang/OTP source tree at
  5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md)
  inventories the actual hosted-runtime dependencies and implementation at OTP
  29.0.5.
- [A brief introduction to
  BEAM](../30-sources/hogberg-2020-brief-introduction-to-beam.md) separates the
  instruction machine from ERTS process, port, and table services.
- [Proof-carrying code](../30-sources/necula-1997-proof-carrying-code.md)
  supplies a verifier architecture precedent while leaving the actual BEAM
  safety policy and proof producer as explicit open work.

### Signals, mailboxes, and overload

- [A few notes on message
  passing](../30-sources/hogberg-2021-message-passing.md) explains per-sender
  signal order, copying, queue separation, and selective-receive scan cost.
- [The Many-to-One Parallel Signal Sending
  Optimization](../30-sources/winblad-2021-parallel-signal-sending.md) shows how
  sender-striped ingress can remove one contention point without inventing a
  cross-sender order.
- [Michael–Scott concurrent
  queues](../30-sources/michael-scott-1996-concurrent-queue-algorithms.md)
  provide a queue primitive candidate while making reclamation and actor-level
  ordering separate obligations.
- [Mailbox types](../30-sources/fowler-et-al-2023-mailbox-types.md) show how an
  optional typed profile can prevent protocol mismatches without redefining
  untyped BEAM compatibility.
- The main synthesis connects mailbox bytes, queue age, scan work, aliases,
  actor termination, and explicit cross-domain credits without silently
  changing ordinary local send behavior.

### Memory ownership and collection

- [Efficient memory management for concurrent programs that use message
  passing](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md)
  compares private, communal, and hybrid heaps and evaluates incremental
  collection.
- [Orca: GC and Type System Co-Design for Actor
  Languages](../30-sources/clebsch-et-al-2017-orca.md) demonstrates zero-copy
  actor memory under Pony reference-capability proofs and explains why those
  conclusions do not transfer automatically to unrestricted BEAM terms.
- The runtime report selects private generational tracing heaps, ordinary term
  copy, explicit immutable sharing, and kernel-agnostic collection as the
  initial compatible baseline.

### Scheduling and multicore behavior

- [Work-Stealing, Locality-Aware Actor
  Scheduling](../30-sources/barghi-karsten-2018-locality-aware-actor-scheduling.md)
  supports local-first stealing while documenting workload-dependent affinity
  failures.
- [Work-stealing theory](../30-sources/blumofe-leiserson-1999-work-stealing.md)
  supplies bounds for fully strict computations and clearly limits their
  transfer to long-lived actor systems.
- [A NUMA-aware actor
  runtime](../30-sources/francesquini-et-al-2013-numa-aware-actor-runtime.md)
  demonstrates topology-sensitive gains and workload/hardware dependence.
- [Scheduler
  activations](../30-sources/anderson-et-al-1992-scheduler-activations.md)
  motivates the division between kernel processor allocation and fine-grained
  runtime scheduling.
- [Characterizing the scalability of Erlang VM on many-core
  processors](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md)
  warns that share-nothing application semantics do not remove shared runtime
  locks, allocators, and metadata.

### Execution, code change, and native boundaries

- [A high performance Erlang
  system](../30-sources/johansson-et-al-2000-high-performance-erlang.md) ties
  native execution to precise runtime stack, root, exception, and collection
  conventions.
- [The Road to the
  JIT](../30-sources/gustavsson-2020-road-to-the-jit.md) explains why simple
  load-time native translation can fit BEAM’s scheduling, hot-loading, and
  tracing constraints better than a complex tracing JIT.
- [HiPErJiT](../30-sources/kallas-sagonas-2018-hiperjit.md) records the
  workload, warmup, code-size, and compilation costs of a profile-driven
  alternative.
- [Hashed and hierarchical timing
  wheels](../30-sources/varghese-lauck-1987-timing-wheels.md) support abundant
  coarse timers while leaving precision, cancellation races, and bucket bursts
  to the runtime design.
- The pinned source audit distinguishes two language-visible module versions
  from internal code indexes and records the large POSIX host contract current
  ERTS consumes.
- The runtime report uses interpreter-first conformance, staged W^X
  publication, epoch reclamation, and separate native service domains.

### Testing, scalability, and distribution

- [A scalability benchmark suite for
  Erlang/OTP](../30-sources/aronis-et-al-2012-scalability-benchmark-suite-erlang-otp.md)
  supplies a multidimensional evaluation method rather than one throughput
  point.
- [Finding Race Conditions in Erlang with QuickCheck and
  PULSE](../30-sources/claessen-et-al-2009-quickcheck-pulse.md) motivates
  deterministic actor-level schedules, generated histories, shrinking, and
  replay.
- [Concuerror](../30-sources/christakis-et-al-2013-concuerror.md) supplies an
  independent systematic Erlang exploration approach, bounded by its supported
  runtime interactions.
- [Actor record and
  replay](../30-sources/aumayr-et-al-2018-actor-record-replay.md) demonstrates
  compact actor-level nondeterminism logs while requiring new evaluation for
  BEAM semantics.
- [Scaling Reliably](../30-sources/trinder-et-al-2017-scaling-reliably.md)
  demonstrates the costs of full-mesh node topology, global naming, and global
  recovery state.
- [PARTISAN](../30-sources/meiklejohn-et-al-2019-partisan.md) supports
  replaceable topology and channel policy rather than embedding one full mesh
  in the actor contract.
- [Implementing remote procedure
  calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md) grounds
  request identity and duplicate suppression while preserving indeterminate
  outcomes after connection loss.

### Failure, resources, and shared tables

- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md)
  supports external restart control and explicit state/retry assumptions.
- [Resource containers](../30-sources/banga-et-al-1999-resource-containers.md)
  separates resource principals from execution contexts and motivates charge
  propagation through deferred work.
- [ETS scalability](../30-sources/klaftenegger-et-al-2013-ets-scalability.md)
  exposes shared-table contention beneath share-nothing actor semantics.
- [Contention-adapting ordered
  sets](../30-sources/sagonas-winblad-2018-contention-adapting-ordered-sets.md)
  provide one measured adaptive candidate rather than a universal table
  structure.

### Adjacent architecture layers

- [BEAM, ERTS, and OTP](beam-erts-and-otp.md) supplies the broader conceptual
  map and fixed compiled-BEAM requirement.
- [Minimal privileged kernel](minimal-privileged-kernel.md) defines the bounded
  capabilities, protection domains, scheduling contexts, transport, faults,
  and teardown beneath the runtime.
- [Kernel hardware and architecture
  support](kernel-hardware-and-architecture-support.md) defines the privileged
  mechanisms beneath that kernel.

## Open questions

- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [Which BEAM, ERTS, and OTP principles belong in a new
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
- Which exact OTP 29.0.6 BIF, library, NIF/port, ETS, tracing, and distribution
  surface is the first supported profile?
- What mailbox limit policy preserves required local semantics while keeping a
  hard runtime-domain memory ceiling?
- Can process-local full collection meet the safe-point target, or must the
  collector perform bounded incremental actor-local work?
- How should shared binary slices be charged without making sharing either
  free or unusably expensive?
- Which kernel-to-runtime scheduling feedback is necessary beyond charged
  threads, budget exhaustion, wakeups, and optional topology hints?
- Does topology-aware placement improve representative supervised service
  workloads after tail latency and recovery cost are included?
- Which native interfaces truly require an in-process NIF failure boundary?
- Can an authenticated, credit-bound gateway preserve the required Erlang
  distribution semantics without inheriting ambient node trust and global
  topology?
