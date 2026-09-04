---
title: "2026-09-02 managed actor runtime deep dive"
kind: journal
created: "2026-09-02"
tags:
  - actor-model
  - beam
  - erlang
  - erts
  - literature-review
  - runtime-systems
aliases:
  - "Managed actor runtime research session"
---

# 2026-09-02 managed actor runtime deep dive

## Observations

The third proposed Atom OS layer was researched as a managed runtime, not as a
second kernel. The strongest synthesis is a BEAM-first hybrid: retain the
observable process, signal, mailbox, collection, failure, and code behavior
needed by a declared compatibility profile while adopting actor-runtime
research only where its proof assumptions survive.

Several distinctions changed the design materially:

- reductions are a runtime fairness measure, while kernel scheduling contexts
  are temporal authority;
- process-local heaps limit most collector interference, while large binaries,
  atoms, code, ETS, allocators, and native resources remain shared runtime
  state;
- per-sender signal order permits a striped many-to-one implementation without
  defining a global message order;
- selective receive makes backlog shape and scan work part of latency;
- Pony/Orca zero-copy results depend on reference-capability guarantees absent
  from arbitrary compiled BEAM code;
- dirty schedulers isolate classes of long work but do not contain native
  memory corruption;
- links and monitors report failure observations, not durable or exactly-once
  distributed outcomes; and
- supervision inside one runtime cannot recover that runtime’s corruption.

## Environment

- Research date: 2026-09-02, America/Toronto.
- Repository: `atom-os-research`, local Git worktree.
- Current official baseline observed: Erlang/OTP 29.0.6, released 2026-09-01,
  with ERTS 17.0.6 and stdlib 8.0.4.
- Pinned implementation evidence already in the archive: Erlang/OTP 29.0.5,
  revision `5cf5f9725452f4e1b6a4890e8ff0305d76924b98`.
- Target runtime, kernel, hardware, or simulator: none; this was literature and
  architecture research.
- Host dependencies used for evidence: repository text search and public web
  pages/PDFs. No OTP build, benchmark, conformance run, or fault injection was
  performed.

## Evidence

### Archive review

The existing BEAM/ERTS/OTP synthesis, map, kernel-placement inquiry, minimal
privileged-kernel report, templates, schema, indexes, and relevant source notes
were read before writing. Existing evidence reused includes Armstrong’s
reliability thesis, current OTP documentation and source audit, BEAM and JIT
engineering histories, process-local memory research, Erlang many-core work,
Scalable Distributed Erlang, and scheduler activations.

Repository searches checked for an existing managed-runtime document and for
incoming concepts that needed body links. No dedicated managed-runtime note,
map, or inquiry existed.

### Current primary documentation

The official OTP patch record and current pages were checked for:

- support and BEAM compatibility;
- processes, signals, aliases, priority messages, and selective receive;
- normal and dirty scheduling, reductions, and native-yield guidance;
- tracing garbage collection and on/off-heap messages;
- code loading, current/old versions, BeamAsm, and thread-progress publication;
- timers and monotonic time;
- trace sessions;
- ETS ownership and consistency;
- ports, drivers, and NIF failure scope; and
- distribution trust and failure ambiguity.

The rendered documentation had advanced to OTP 29.0.6/ERTS 17.0.6 for the key
pages. Some subsystem search results still displayed 29.0.5 during rollout, so
implementation statements remain pinned to the separate 29.0.5 source audit.

### Scientific papers

New primary research records were created for:

- Aronis et al. (2012), Bencherl and multidimensional Erlang scalability
  measurement, DOI `10.1145/2364489.2364495`;
- Barghi and Karsten (2018), locality-aware actor work stealing on NUMA
  systems, DOI `10.1109/IPDPS.2018.00058`;
- Claessen et al. (2009), QuickCheck and PULSE controlled scheduling, DOI
  `10.1145/1596550.1596574`; and
- Clebsch et al. (2017), Orca actor GC and reference-capability co-design, DOI
  `10.1145/3133896`.

The comparative search also examined classic work stealing, CAF, Pony, Akka,
Kilim, Reactive Streams, NUMA-aware Erlang, actor record/replay, Concuerror,
real-time actor analysis, Savina, and reliability benchmarks. These works
provided corroborating or alternative mechanisms. They were not all used as
substantive evidence in the synthesis, because several assume run-to-completion
actors, JVM or C++ memory, FIFO mailboxes, restricted ownership types, or
fully-strict task graphs that do not establish BEAM behavior.

### Engineering articles

Two official Erlang/OTP engineering articles received source records:

- John Högberg (2021), message copying, signal/message queue separation,
  per-sender order, and selective-receive optimization; and
- Kjell Winblad (2021), adaptive sender-striped signal ingress and its focused
  many-to-one benchmark.

Their implementation descriptions are maintainer evidence, not stable public
ABI or representative application benchmarks. Current public semantics were
checked independently in the OTP 29.0.6 manuals.

### Synthesis method

Claims were grouped as:

1. public compatibility behavior;
2. current ERTS implementation;
3. historical or alternative runtime evidence;
4. cross-source interpretation; and
5. proposed Atom OS architecture requiring experiments.

The resulting note defines a compatibility manifest, thirteen runtime
components, local send/activation/collection/cross-domain critical paths,
implementation stages, an evaluation matrix, provisional decisions, and
explicit falsifiers.

## Source manifest

The classification records the session in which each source note first entered
the archive. A source note that already existed and was used substantively in
this session is listed as reused even when its external publication was newly
rechecked.

### Newly introduced sources

- [Erlang/OTP 29.0.6 managed-runtime
  documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
  — current public process, signal, scheduling, memory, timer, code, ETS,
  tracing, native-work, and distribution semantics.
- [A few notes on message
  passing](../30-sources/hogberg-2021-message-passing.md) — maintainer account
  of signal queues, message copying, per-sender order, and selective receive.
- [The Many-to-One Parallel Signal Sending
  Optimization](../30-sources/winblad-2021-parallel-signal-sending.md) —
  adaptive sender-striped signal ingress and its focused benchmark.
- [Orca: GC and Type System Co-Design for Actor
  Languages](../30-sources/clebsch-et-al-2017-orca.md) — zero-copy actor
  collection results and the ownership assumptions they require.
- [Work-Stealing, Locality-Aware Actor
  Scheduling](../30-sources/barghi-karsten-2018-locality-aware-actor-scheduling.md)
  — NUMA-sensitive actor placement and stealing evidence.
- [A scalability benchmark suite for
  Erlang/OTP](../30-sources/aronis-et-al-2012-scalability-benchmark-suite-erlang-otp.md)
  — multidimensional runtime-scaling methodology and benchmark coverage.
- [Finding Race Conditions in Erlang with QuickCheck and
  PULSE](../30-sources/claessen-et-al-2009-quickcheck-pulse.md) — controlled
  scheduling as a concurrency-testing method.

### Reused sources

- [Erlang/OTP 29.0.5 system
  documentation](../30-sources/erlang-otp-team-2026-otp-29-documentation.md)
  — the preceding documented compatibility baseline.
- [Erlang/OTP source tree at
  5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) —
  pinned ERTS implementation evidence kept separate from public semantics.
- [A brief introduction to
  BEAM](../30-sources/hogberg-2020-brief-introduction-to-beam.md) — BEAM
  execution, register, frame, and liveness background.
- [The Road to the
  JIT](../30-sources/gustavsson-2020-road-to-the-jit.md) — BeamAsm publication
  and implementation history.
- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
  — actor isolation, failure signaling, supervision, and reliability baseline.
- [Efficient memory management for concurrent programs that use message
  passing](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md)
  — process-local heaps, tracing collection, and message-copying trade-offs.
- [Scheduler
  activations](../30-sources/anderson-et-al-1992-scheduler-activations.md) —
  separation of kernel processor allocation from user-level scheduling.
- [Characterizing the scalability of Erlang VM on many-core
  processors](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md) —
  historical shared-runtime bottlenecks and many-core measurements.
- [Scaling Reliably: Improving the Scalability of the Erlang Distributed Actor
  Platform](../30-sources/trinder-et-al-2017-scaling-reliably.md) — distributed
  Erlang topology, scale, and reliability evidence.

## Threads

- [Managed actor runtime layer: evidence, contract, and implementation
  plan](../20-notes/managed-actor-runtime-layer.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [What contract should the managed actor runtime
  provide?](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)

## Follow-ups

- Pin and audit OTP 29.0.6 source before making implementation claims specific
  to that patch.
- Turn the compatibility manifest into a schema and enumerate the initial
  opcode, BIF, signal, table, NIF/port, tooling, and OTP-library surface.
- Build executable models for signal order, mailbox admission, actor exit,
  code publication, and stale runtime/node incarnations.
- Prototype the deterministic interpreter and process-local collector before
  multicore or JIT work.
- Preserve raw benchmark data and fault traces when implementation begins;
  none were produced in this research session.
- Add source notes for comparative systems only when their mechanisms become
  substantive design dependencies rather than contextual contrasts.
