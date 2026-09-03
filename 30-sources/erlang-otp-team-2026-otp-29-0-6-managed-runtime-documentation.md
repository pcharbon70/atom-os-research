---
title: "Erlang/OTP 29.0.6 managed-runtime documentation"
kind: source
created: "2026-09-02"
authors:
  - "Erlang/OTP contributors"
published: "2026-09-01"
citation_key: "erlang-otp-docs-29.0.6-managed-runtime"
container: "Erlang/OTP System and ERTS Documentation"
edition: "OTP 29.0.6; ERTS 17.0.6; stdlib 8.0.4"
isbn: null
doi: null
url: "https://www.erlang.org/patches/OTP-29.0.6"
accessed: "2026-09-02"
tags:
  - beam
  - code-loading
  - erlang
  - erts
  - garbage-collection
  - mailboxes
  - scheduling
  - source-documentation
aliases:
  - "OTP 29.0.6 runtime documentation"
---

# Erlang/OTP 29.0.6 managed-runtime documentation

## Reference

Erlang/OTP contributors. *Erlang/OTP System and ERTS Documentation*, OTP
29.0.6, ERTS 17.0.6, stdlib 8.0.4, released 2026-09-01. [Official patch
record](https://www.erlang.org/patches/OTP-29.0.6) and [documentation
root](https://www.erlang.org/doc/). Accessed 2026-09-02.

The managed-runtime reading covered the official pages for [support and
compatibility](https://www.erlang.org/doc/system/misc.html),
[processes](https://www.erlang.org/doc/system/ref_man_processes.html),
[communication](https://www.erlang.org/doc/apps/erts/communication.html),
[the `erlang` module](https://www.erlang.org/doc/apps/erts/erlang.html),
[garbage collection](https://www.erlang.org/doc/apps/erts/garbagecollection.html),
[code loading](https://www.erlang.org/doc/system/code_loading.html),
[BeamAsm](https://www.erlang.org/doc/apps/erts/beamasm.html), [time
correction](https://www.erlang.org/doc/apps/erts/time_correction.html),
[ETS](https://www.erlang.org/doc/apps/stdlib/ets.html),
[tracing](https://www.erlang.org/doc/apps/kernel/trace.html),
[ports](https://www.erlang.org/doc/system/ports.html), and
[NIFs](https://www.erlang.org/doc/apps/erts/erl_nif.html).

## Research question or contribution

This reading establishes the most recent public behavior relevant to a
BEAM-compatible actor layer while separating supported contracts from current
ERTS implementation details. It updates the documentation baseline without
changing the archive’s separately pinned OTP 29.0.5 source-tree audit.

## Method

The patch record and rendered manuals were checked on 2026-09-02. Public
reference and system documentation was treated as contract evidence. Pages
labeled internal documentation, source files, configuration defaults, and
engineering explanations were treated as implementation evidence only. The
purge behavior was cross-checked against the exact OTP-29.0.6 tag at commit
[`e07fd07837e5aa845657f5fa340637121e451d47`](https://github.com/erlang/otp/tree/e07fd07837e5aa845657f5fa340637121e451d47),
including `erts_code_purger.erl`, `beam_bif_load.c`, and `erl_fun.c`. Where some
subsystem pages still displayed 29.0.5/ERTS 17.0.5 during rollout, no
patch-specific change was inferred without the patch record or matching
source.

## Findings

### Compatibility and BEAM loading

- OTP releases are tested combinations of application versions. Arbitrary
  mixtures are not an equivalent supported release.
- Erlang distribution is intended to interoperate across at least two earlier
  and two later major releases. Compiled BEAM, NIF libraries, and drivers are
  intended to load on at least two later releases; loading newer artifacts on
  an older runtime is unsupported.
- External generic BEAM instructions form a compiler/loader boundary. Internal
  generic and loader-selected specific instructions can change independently
  and are not a kernel ABI.
- Loading a `.beam` container proves much less than OTP compatibility: BIFs,
  terms, exceptions, signals, code versions, distribution, and library behavior
  also matter.

### Actors, signals, and scheduling

- Erlang processes are lightweight runtime entities communicating through
  asynchronous signals. If one sender sends `S1` and then `S2` to one
  destination, `S1` cannot arrive after `S2`, although `S1` can be lost. No
  cross-sender total order or bounded delay is promised.
- `receive` searches the receiver-private message queue for the first matching
  message. Search cost grows with preceding unmatched messages; compiler-known
  unique references can establish a later starting point.
- Priority messages, available since OTP 28, occupy a priority partition ahead
  of ordinary messages. A later signal sent through a priority alias never
  overtakes an earlier ordinary message signal in signal delivery, but the
  resulting priority message can be inserted ahead of the earlier ordinary
  message in the combined mailbox.
- `Dest ! Msg` and `erlang:send/2` return `Msg`; `erlang:send/3` returns only
  `ok`, `nosuspend`, or `noconnect`. None is a delivery-completion result.
- External remote PIDs encode node, identifier, serial, and node creation;
  references likewise carry node creation and identifier words. Transport
  reconnect does not itself create a new term identity, while broken links and
  monitors still report connection loss and are not automatically restored.
- Normal scheduling is pre-emptive at reduction-budget boundaries. The current
  default maximum slice is 4,000 reductions, but weights, slice size, queue
  topology, balancing, and affinity are implementation details rather than
  BEAM compatibility promises.
- Normal scheduler queues and dirty CPU/I/O work classes protect responsiveness
  from some long native work. They do not create memory protection or a hard
  real-time guarantee.

### Memory and shared state

- Current ERTS uses per-process generational semispace copying collection plus
  a global large-object area. Registers and stack contribute roots; collection
  is automatic reachability tracing.
- Ordinary same-node term graphs are copied between process domains, while
  literals and reference-counted large binaries are shared exceptions. The
  current large-binary threshold and heap layout are implementation details.
- On-heap and off-heap queued messages trade delivery cost, receiver
  contention, collection scanning, and retained memory.
- ETS is explicit node-local shared term storage with owners, access rights,
  heirs, and copy-in/out behavior. It is not an ordinary shared actor heap and
  does not promise general transactions or snapshot traversal.
- ETS owner-death behavior distinguishes `{heir, Pid}` (silent transfer),
  `{heir, Pid, HeirData}` (transfer plus `ETS-TRANSFER`), and no live heir
  (destruction). Successful `give_away/3` always sends `ETS-TRANSFER` and does
  not change the table's configured heir.

### Code, time, tracing, and native work

- A module can have current and old executable versions. Loading a third
  version requires old-code purge and can terminate actors still executing it.
- In OTP 29.0.6, `check_process_code/3` and `code:soft_purge/1` treat only
  direct process references to old executable code as lingering. Indirect
  references through local funs are ignored and raise an exception if invoked
  after successful purge; literal references are handled by later copying.
  Fun-only and literal-only holders therefore neither fail a soft purge nor,
  by themselves, cause termination during a hard purge.
- The tagged implementation scans the process instruction pointer, saved
  native-call state, and stack continuation pointers. It marks old fun entries
  pending/unloaded during purge, removes executable code on completion, and
  queues the old literal area for a separate per-process copy and thread-progress
  reclamation protocol. Logical purge eligibility and final physical retention
  are consequently distinct implementation states.
- Code preparation and validation precede an atomic publication step; internal
  code indexes and thread-progress machinery are not language-visible module
  versions.
- Actor timers use monotonic time and may fire late but not early. Cancellation
  races with expiry and delivery, so a failed cancellation does not prove no
  timeout message is queued.
- Trace sessions can observe calls, messages, scheduling, collection, ports,
  and related events, but trace work perturbs the observed runtime and must be
  bounded in a new design.
- Linked drivers and NIFs execute within the VM’s native trust boundary. Dirty
  scheduling protects normal scheduler availability, not memory safety; native
  corruption can still compromise the whole runtime.
- NIF scheduling class is declared per `ErlNifFunc` name/arity entry, not once
  for a whole module. `enif_schedule_nif` can also reschedule and reclassify
  alternating CPU- and I/O-bound work.
- Process exit reasons can be arbitrary Erlang terms. Compatible exit, link,
  and monitor paths preserve those terms except for the transformations the
  process semantics explicitly document, such as an untrappable explicit
  `kill` causing the receiver to terminate with `killed`.

## Relevance

This source supplies the current semantic reference for the [managed actor
runtime layer](../20-notes/managed-actor-runtime-layer.md). It supports a
versioned compatibility manifest, per-sender signal ordering, selective
mailboxes, process-local tracing collection, reduction safe points, staged code
publication, monotonic timers, explicit shared tables, and isolated native
services. It also identifies which attractive ERTS choices must remain runtime
implementation details rather than kernel contracts.

## Limits

The manuals are authoritative operational documentation, not one formal
semantics. Scheduler behavior, collector layout, signal queues, JIT templates,
timer structures, and internal code indexes may change. Patch rollout briefly
left some rendered pages on the previous version. No local build, benchmark,
fault injection, conformance run, or source diff between 29.0.5 and 29.0.6 was
performed for this note.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Managed actor runtime component deep dives](../20-notes/managed-actor-runtime-components/README.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
