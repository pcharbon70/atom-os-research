---
title: "What contract should the managed actor runtime provide?"
kind: inquiry
created: "2026-09-02"
status: open
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
  - "Managed-runtime contract inquiry"
---

# What contract should the managed actor runtime provide?

## Why this matters

Atom OS requires compiled-BEAM execution and automatic process-local tracing
collection, but those requirements do not choose a runtime architecture.
Current ERTS combines language execution, process scheduling, signals,
collection, shared tables, timers, ports, native extensions, code loading,
distribution, tracing, and a large host operating-system contract. Moving that
whole implementation into privileged code would enlarge the trusted computing
base. Replacing it with a principles-only actor library would fail the platform
compatibility requirement.

The runtime contract must preserve enough observable behavior for useful BEAM
and OTP software while allowing a new implementation to use Atom OS protection,
budget, publication, and recovery mechanisms. It must also state honestly where
ordinary actors cease to be fault or security boundaries.

## Operational question

Choose and validate the smallest unprivileged runtime interface that meets all
of these conditions:

1. executes every feature in a versioned, machine-readable BEAM/OTP profile;
2. keeps ordinary actor heaps private and performs automatic local reachability
   tracing without kernel term knowledge;
3. preserves declared signal order, selective receive, links, monitors,
   aliases, exit, timer, exception, and code-version behavior;
4. bounds managed safe-point latency and charges language, mailbox, collector,
   trace, and runtime-service work;
5. rolls actor consumption into kernel-enforced domain CPU and memory limits;
6. contains runtime, native service, gateway, driver, and machine failures at
   their actual boundaries and preserves distinguishable evidence;
7. supports deterministic actor-level replay plus kernel/service fault
   injection; and
8. reproduces conformance, latency, scalability, overload, and teardown results
   on an emulator and at least one physical target.

The inquiry is resolved only after an implementation passes the declared
profile and measurements. A detailed design document does not resolve it.

## Working hypotheses

### H1: actors remain runtime objects inside kernel-scheduled domains

A runtime should multiplex many actors over a small number of charged kernel
threads. Reductions decide which actor runs next; kernel scheduling contexts
decide whether the runtime may consume CPU.

Falsifier: kernel-visible actors meet actor creation, switching, send, memory,
capability, and latency targets without material overhead, or the two-level
scheduler cannot prevent priority/budget pathologies with a small interface.

### H2: private generational tracing heaps are the compatible baseline

Each actor should own a moving, automatically collected heap. Ordinary terms
are copied on local send; literals and large immutable binaries are shared with
explicit accounting.

Falsifier: another collector demonstrably improves pause and total cost while
preserving process-local tracing semantics, or a BEAM-compatible ownership
proof safely enables zero-copy transfer without expanding correlated failure.

### H3: physical signal queues can be sharded behind a narrow order contract

The runtime should guarantee order only from one sender to one destination and
may stripe many senders across ingress buffers. The receiver alone owns its
selective mailbox.

Falsifier: the pinned compatibility profile requires a stronger observation,
or sharding creates wakeup, starvation, memory, or tail-latency costs worse than
the contention it removes on representative services.

### H4: reductions need real-time reconciliation

Reduction counting is useful for repeatable actor pre-emption but cannot enforce
CPU authority because operation cost varies. Actor reductions should be paired
with measured kernel execution time and explicit charge for scanning, GC,
signals, tracing, and runtime work.

Falsifier: a calibrated reduction scheme bounds actual consumption and latency
without kernel time, or reconciliation overhead exceeds its containment value.

### H5: ordinary local sends are not silently made lossy

Compatible sends should reserve and publish atomically. Soft thresholds can
trigger supervisor overload policy. Terminating or quarantining an actor at a
hard threshold is a candidate Atom OS resource-profile extension, while a
strict compatibility mode may need bounded buffering, spill, or
distribution-like suspension. New cross-domain/stream protocols may use
explicit credits or refusal.

Falsifier: the selected compatibility profile permits an observable bounded
send failure that is safer and simpler, or termination at the limit causes
worse systemic behavior than a specified buffer/spill or sender-suspension
policy.

### H6: unsafe native code belongs in separate service domains

Ports and bounded service endpoints should be the default native boundary.
In-process NIF support is an explicitly trusted compatibility mode that accepts
runtime-domain-wide corruption and stall risk.

Falsifier: required workloads cannot meet functionality or performance targets
through isolated services, and a verified memory-safe, bounded intrinsic can
satisfy the required in-domain interface.

### H7: distribution is a gateway, not ambient node authority

Actor encoding and link/monitor semantics should sit over authenticated,
capability-scoped, credit-bound network services with node incarnations.
Standard Erlang distribution remains a trusted compatibility adapter.

Falsifier: the gateway cannot reproduce required ordering and failure
observations at useful cost, or its authority model cannot interoperate with the
initial OTP profile without unsafe ambient trust.

## Paths to explore

### Compatibility work

- Pin OTP 29.0.6 and enumerate accepted BEAM chunks, external generic
  instructions, BIFs, terms, exceptions, signals, code behavior, External Term
  Format, NIF/driver surface, OTP applications, and tools.
- Generate differential programs and malformed modules against the reference
  runtime. Include OTP 27 and 28 artifacts only if claiming the documented
  forward-loading window.
- Separate required behavior from the current ERTS collector, queues, scheduler
  topology, JIT templates, internal code indexes, and POSIX substrate.

### Prototype experiments

1. Build a deterministic one-thread interpreter with copying sends, selective
   receive, automatic tracing GC, links, monitors, aliases, timers, and replay.
2. Place it in one Atom OS domain and remove every undeclared host-service
   dependency.
3. Add kernel-charged scheduler threads and compare one queue, local queues,
   random stealing, and local-first hierarchical stealing.
4. Compare one ingress queue with adaptive sender-striped ingress under fan-in,
   unmatched-message scans, actor exit, and overload.
5. Sweep actor heap sizes, live ratios, message placement, shared binaries, and
   full collection while measuring pause and total work.
6. Stage, seal, publish, retain, purge, and retire code while actors execute old
   frames and tracing is active.
7. Crash and stall isolated native services and a deliberately unsafe
   in-process extension; confirm the predicted different failure scopes.
8. Partition, delay, duplicate, reconnect, and restart authenticated gateways
   before admission, after admission, and before reply.

### Evidence to add

- Current research on pre-emptible or incremental actor-local collection with
  exact root maps.
- Modern measurements of Erlang/OTP on NUMA hardware and under CPU quotas.
- Formal or executable signal/link/monitor/alias state machines including OTP
  28+ priority messages.
- Mailbox overload studies that preserve ordinary Erlang send behavior.
- Capability-safe shared-buffer protocols and verified BEAM loaders.
- Actor-level deterministic replay for selective receive, native results, and
  distributed failure.

## Findings

The [managed actor runtime synthesis](../20-notes/managed-actor-runtime-layer.md)
and its [thirteen component implementation deep
dives](../20-notes/managed-actor-runtime-components/README.md) currently support
all seven hypotheses but do not settle them experimentally:

- current OTP 29.0.6 distinguishes public external BEAM behavior from internal
  loader-selected instructions and runtime machinery;
- current ERTS uses reductions for pre-emption, but their weights and the
  current 4,000-reduction slice are implementation details rather than time;
- signal order is per sender-destination pair, which permits striped ingress,
  while priority-message reception qualifies simple mailbox-order statements;
- process-local heaps confine most collection, but shared binaries, atoms,
  code, tables, allocators, and native resources remain wider domains;
- Pony/Orca demonstrates safe zero-copy sharing only with stronger static
  reference-capability facts than ordinary BEAM supplies;
- locality-aware actor scheduling improves some workloads and creates severe
  contention tails in others, so topology policy must remain adaptive and
  measured;
- compiler-known references reduce some selective-receive scans, but no general
  index eliminates arbitrary pattern matching over backlog;
- dirty scheduler classes do not protect ERTS from native memory corruption;
- full-mesh distribution, global names, and global recovery state constrain
  scale; and
- controlled scheduling and property-based shrinking find useful actor races,
  but kernel, native, network, and power faults require additional models.

The component research adds a common implementation discipline:

- every externally visible object follows reserve, private preparation,
  generation-checked publication, terminal disposition, and rollback rules;
- every asynchronous request binds actor, runtime, service/gateway, and object
  incarnations, and reports `Indeterminate` when loss occurs after acceptance
  without stronger completion evidence;
- resource accounting follows deferred work through actor, application, domain,
  and kernel levels and reserves bounded cleanup/collection/evidence progress;
- actor exit and runtime mechanics are distinct from OTP supervisor policy,
  while an outer service owns whole-runtime restart; and
- production telemetry, deterministic test schedules, and crash capture use a
  shared vocabulary but make different completeness and trust claims.

The [2026-09-03 component research
session](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
records the expanded primary-source search, negative evidence, cross-component
review questions, and exact absence of executable results.

No runtime prototype, conformance result, GC measurement, mailbox-overload
experiment, or native-domain fault test has yet been performed in this archive.

## Outcome

Open. The leading design is a BEAM-first, unprivileged runtime domain with
private actor heaps, automatic tracing GC, copy-by-default messages,
sender-ordered striped signals, reduction safe points reconciled with kernel
time, staged W^X code publication, explicit runtime-global resource accounting,
isolated native services, authenticated bounded gateways, and actor-level
deterministic testing. The thirteen detailed reports now define proposed state
machines, negative cases, implementation stages, and falsifiers for those
mechanisms. The inquiry remains open until executable models and prototypes
reproduce the required compatibility, containment, responsiveness, overload,
and recovery claims.
