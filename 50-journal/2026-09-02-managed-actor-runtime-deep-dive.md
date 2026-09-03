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
