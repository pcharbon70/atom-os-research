---
title: "Observability, deterministic testing, and crash evidence"
kind: note
created: "2026-09-03"
maturity: developing
tags:
  - actor-model
  - crash-analysis
  - deterministic-testing
  - observability
  - tracing
aliases:
  - "Managed runtime observability component"
  - "Actor replay and crash evidence component"
---

# Observability, deterministic testing, and crash evidence

The runtime should combine three related but distinct mechanisms:

1. **bounded production observability** using charged per-scheduler rings and
   explicit loss records;
2. **a deterministic test mode** that controls and records actor-level choice
   points for exploration, shrinking, and replay; and
3. **crash evidence outside the runtime domain**, written through preallocated
   bounded channels that remain available when the runtime is corrupt.

Production tracing is not deterministic replay. A lossy metrics stream may be
excellent for operations while omitting the one scheduling or timer choice
needed to reproduce a race. Conversely, recording every nondeterministic input
and memory interaction in production can impose unacceptable cost and expose
sensitive data. The modes need separate contracts and a shared event vocabulary.

## Question, scope, and operational standard

The question is:

> What minimum event model and evidence path can make actor scheduling,
> messages, timers, failures, code generations, and resource pressure
> explainable and reproducible without introducing an unbounded observer or
> trusting a crashed runtime to describe itself correctly?

This component owns:

- event schemas, sequence/causality fields, time bases, and profile hashes;
- per-scheduler trace buffers, subscriptions, sampling, filtering, and loss
  accounting;
- actor-level deterministic scheduling hooks and replay validation;
- bounded snapshots of actor/runtime state at safe points;
- watchdog progress counters and safe-point latency evidence;
- the runtime side of crash freeze, seal, and evidence export; and
- privacy, authority, and quota checks for diagnostic access.

It does not own long-term storage, fleet telemetry policy, user-interface
queries, kernel fault capture, device register collection, or a promise to
replay arbitrary native/distributed side effects. Those belong to services
outside the runtime and must declare their own evidence guarantees.

The baseline must guarantee:

1. Observability work and storage are charged and bounded; a stalled consumer
   cannot consume unbounded runtime memory.
2. Every dropped event is represented by a sequence gap or explicit loss
   summary with cause and count.
3. Trace publication never blocks an ordinary scheduler indefinitely or holds
   runtime locks across an external wait.
4. Deterministic mode records or controls every declared actor-level choice
   point and refuses replay when code/profile/input identities differ.
5. Crash records contain kernel-authenticated domain/fault context even if the
   runtime contributes nothing.
6. Evidence is generation-bound, integrity-protected, privacy-filtered, and
   accessible only through attenuated diagnostic authority.
7. Diagnostic instrumentation preserves required actor semantics; any timing
   perturbation and unsupported replay boundary is disclosed.

## Evidence, synthesis, and proposal

Official [OTP 29.0.6 managed-runtime
documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
documents tracing, process/system monitors, scheduler and process statistics,
`process_info`, stack/backtrace facilities, crash dumps, and many observable
runtime states. These interfaces are a compatibility reference, not a bounded
telemetry architecture. Some tracing combinations are expensive, tracing can
perturb scheduling, and a crash dump produced by a failing VM cannot be the
only trusted evidence source.

[QuickCheck and PULSE](../../30-sources/claessen-et-al-2009-quickcheck-pulse.md)
demonstrates generated concurrent tests, a controlled user-level scheduler,
and shrinking of failing schedules for Erlang programs. The work motivates
recording scheduler choices and message-delivery decisions, but applies to an
instrumented testing environment rather than transparent production replay.

[Concuerror](../../30-sources/christakis-et-al-2013-concuerror.md) explores
alternative Erlang process schedules using stateless techniques and reports
concurrency errors with reproducible interleavings. Its supported language and
runtime interactions are necessarily bounded; dynamic native, timing, and
distributed effects prevent a claim of exhaustive exploration for arbitrary
OTP applications.

[Actor record/replay research](../../30-sources/aumayr-et-al-2018-actor-record-replay.md)
shows that actor-language replay can focus on ordering nondeterministic actor
events rather than recording every instruction. The evaluated language/runtime
and actor semantics differ from BEAM, so the exact logged choices and overhead
must be established for Atom OS.

[Kdump](../../30-sources/goyal-et-al-2005-kdump.md) demonstrates a valuable
systems pattern: preserve failed-system memory and use a separate, freshly
booted capture environment to write evidence. Atom OS should adopt the boundary
principle, not Linux-specific machinery. The kernel and an outer evidence
service must retain the minimal fault record and immutable mappings after a
runtime fault.

## One event vocabulary, three contracts

```text
RuntimeEvent {
  schema_version,
  runtime_epoch,
  scheduler_id,
  scheduler_sequence,
  monotonic_timestamp,
  event_kind,
  actor_or_object_generation?,
  causal_id?,
  code_generation?,
  charge_context?,
  payload_class,
  payload_or_digest,
}
```

The schema is versioned with the compatibility profile. Unknown event kinds
are length-delimited and skippable. Sequence numbers are local to a declared
stream; the system does not fabricate one global total order. Causal IDs join
explicit relations such as send/publication/receive, request/completion, timer
arm/fire, and actor exit/`DOWN`.

The three contracts use the schema differently:

| Mode | Completeness | Backpressure | Payload | Intended use |
| --- | --- | --- | --- | --- |
| Production metrics/trace | Selected and possibly lossy, with explicit gaps | Never unbounded on actor schedulers | Aggregates, metadata, sampled/digested terms | Operations and performance diagnosis |
| Deterministic test | Complete for declared choice points or test fails | Test scheduler may slow execution within quota | Inputs, choices, digests, optional bounded values | Race exploration, replay, conformance |
| Crash evidence | Best-effort runtime contribution plus mandatory kernel minimum | Preallocated one-way seal | Fault/progress/resource/code identities and bounded samples | Post-mortem containment and reconstruction |

## Production trace architecture

Each scheduler writes a single-producer ring or another bounded local structure
without taking a global trace lock on the hot path. A charged drain service
merges streams only when a consumer requests a view.

```text
Disabled
  -> Active(buffer_generation, filter, quota)
  -> Saturated(loss_epoch)
  -> Draining
  -> Closed
```

On saturation, the declared mode either overwrites oldest records, drops new
records, samples, or closes the subscription. It always emits/retains a compact
`TraceLoss` containing stream, first/last lost sequence if known, count or
lower bound, cause, and time range. “Lossless” tracing is allowed only in a
dedicated test/diagnostic profile whose backpressure and resource consequences
are explicit; it cannot secretly suspend unrelated production actors.

Filters compile into bounded predicates over metadata. Arbitrary user code
does not run in the scheduler trace path. Term payloads default to type/size/
digest or policy-approved redaction. Capturing full terms performs a charged
copy into an authorized evidence domain.

## Required operational signals

The runtime should expose at least:

- actor runnable/waiting/exiting transitions and activation reductions/time;
- safe-point interval and maximum non-yielding fragment;
- per-queue length, bytes, oldest age, ingress contention, and receive scans;
- heap/stack/live/allocated bytes, GC type/work/pause, and shared retention;
- timer lateness, event batch size, cancellation races, and I/O outcomes;
- code profile/generation, loader rejection, publication and reclamation;
- native/gateway request phase, credits, service/session incarnations, and
  indeterminate outcomes;
- resource reservations, refusals, pressure-state transitions, reserve use,
  reconciliation gaps, and table contention;
- actor/service/runtime faults and relation-cleanup progress; and
- trace loss, watchdog lapse, evidence seal, and missing-section bitmap.

Metrics report distributions, including p99.9/p99.99 and worst observed where
sample size permits, not just averages. Histograms and sampling policy are
versioned because changing them changes the interpretation of a report.

## Deterministic test mode

The initial deterministic boundary is one runtime domain with simulated or
recorded external services. Choice points include:

- which runnable actor receives the next activation;
- which eligible signal becomes visible when independent senders race;
- timer expiration order when deadlines are equal or the runtime observes
  several expired timers together;
- completion, cancellation, actor exit, and relation-event races;
- work stealing and actor migration decisions relevant to visible behavior;
- injected allocation refusal, kernel preemption, service loss, and domain
  fault; and
- explicit nondeterministic BIF/service results such as time, randomness, and
  external input.

Pure internal operations between choice points execute normally. The harness
records a compact decision:

```text
Choice {
  choice_index,
  runnable_or_enabled_set_digest,
  selected_operation,
  selected_generation,
  input_digest?,
  resulting_state_digest?,
}
```

Replay checks the enabled-set digest before applying the choice. A mismatch
freezes with a divergence record; it never silently selects a different actor.

```text
Created
  -> InputsVerified
  -> Executing
  -> Passed | Failed | Diverged
  -> Frozen
```

A replay manifest binds runtime/OTP profile, module/code hashes, native/service
models, initial durable inputs, topology, quota policy, random seed, and choice
log schema. Real network peers, uncontrolled NIFs, physical devices, wall-clock
time, and external durable services are outside the deterministic claim unless
fronted by a recorded deterministic adapter.

Exploration uses preemption bounding, partial-order reduction, targeted fault
choices, and property-based input generation. Those techniques reduce the
search; they do not prove all schedules were explored unless the bounded model
and state space are explicitly complete.

## Crash evidence architecture

The kernel reserves a small immutable crash header and grants an outer evidence
service read-only access to selected frozen mappings. The runtime pre-registers
bounded descriptor pages while healthy. On fault:

```text
Armed
  -> FaultObserved
  -> DomainFrozen
  -> KernelHeaderSealed
  -> OptionalRuntimeSectionsCaptured
  -> ManifestSealed
  -> ExportedOrExpired
```

The kernel header includes domain identity/epoch, fault class, architecture
record reference, scheduling-context and budget state, faulting thread/context,
monotonic time/era, mapping manifest, and integrity metadata. The runtime may
contribute:

- compatibility/profile and code-generation hashes;
- scheduler progress counters and last safe points;
- actor table generations and compact status/resource summaries;
- queue/timer/native/gateway high-water marks;
- recent bounded trace tails and loss summaries;
- loader/GC/code-publication phase; and
- a missing/invalid-section bitmap.

Every section is independently length-bounded and checksummed. The consumer
treats runtime-written fields as untrusted after a corruption fault, correlates
them with kernel-owned evidence, and never executes pointers or terms from the
dump. A failure to capture one section cannot prevent sealing the rest.

Full memory capture is an opt-in diagnostic policy with explicit privacy,
storage, and exposure consequences. The default record favors identities,
digests, counters, bounded stacks, and recent event tails.

## Watchdogs and progress evidence

Each runtime scheduler publishes a monotonic progress counter and current
bounded phase at safe points without requiring an external reader lock. The
kernel/outer service can distinguish:

- runnable domain receiving no kernel budget;
- scheduler receiving budget but making no safe-point progress;
- actor/native fragment exceeding its declared non-yielding limit;
- global runtime thread-progress barrier stuck on one participant; and
- ordinary idle wait with no admitted work.

Threshold crossing first produces `LivenessSuspected` with budget/timing
evidence. Policy may then sample, freeze, or terminate. A watchdog is not proof
of root cause, and instrumentation itself must not reset progress falsely.

## Privacy, security, and authority

- Diagnostic access is an attenuated capability scoped by runtime, event
  class, payload policy, retention, and rate.
- Actor terms are redacted/digested by default; secrets, credentials, binary
  bodies, and message content require separate authorization.
- Code hashes and manifests are safe identifiers; executable code pages are
  not automatically exported.
- A malicious actor cannot choose another actor's trace target or charge its
  trace to a victim.
- Remote telemetry is treated as untrusted input and bounded like any external
  term.
- Crash evidence is encrypted/authenticated at rest or transit by the outer
  service; the runtime never receives storage credentials merely to emit a
  record.
- Trace control cannot disable mandatory kernel fault or resource-limit
  evidence.

## Alternatives and trade-offs

### One global lossless event log

It simplifies ordering but introduces contention, unbounded backpressure, and
a new failure dependency. Per-scheduler sequences plus causal links preserve
the relationships the runtime can actually justify.

### Sampling only

Cheap enough for production performance analysis but unable to reproduce rare
ordering races. Pair it with a complete declared choice log in test mode.

### Record every instruction or memory access

Potentially stronger replay, but incompatible with the initial overhead and
volume target and unnecessary for actor-level schedule exploration. Reserve it
for specialized hardware/debug modes if later justified.

### Let the failed runtime write its own dump

It may add useful semantic context, but can deadlock, corrupt, omit, or forge
that context. The kernel minimum and outer sealing path must succeed without it.

## Implementation program

### Stage 0: schema and observability budget

- Define versioned events, stream sequences, loss records, payload classes,
  and diagnostic capability scopes.
- Measure a no-op/hot-path instrumentation baseline and set explicit overhead
  targets.

### Stage 1: bounded production telemetry

- Add per-scheduler rings, drain service, histograms, progress counters, and
  pressure/loss evidence.
- Stress stalled and malicious consumers.

### Stage 2: deterministic single-domain harness

- Control actor selection, message/timer races, recorded BIF inputs, and fault
  injection.
- Integrate property generation, schedule shrinking, and divergence checks.

### Stage 3: external crash capture

- Pre-register descriptor pages, freeze domains, seal kernel minimum records,
  capture independently bounded semantic sections, and verify offline parsers.
- Add recorded service/gateway adapters only after the local deterministic
  boundary is stable.

## Verification and measurements

- Generate workloads with known event counts; fill, wrap, drain, disable, and
  destroy subscriptions while proving loss records explain every sequence gap.
- Measure throughput and p99.99 actor/safe-point latency with tracing disabled,
  metadata-only, sampled, and full authorized payload modes.
- Reproduce known mailbox, timer, link/monitor, ETS, and code-loading races;
  shrink each to a stable choice log and replay it repeatedly.
- Mutate code/profile/input hashes and enabled sets; replay must stop at the
  first divergence with a precise record.
- Crash or corrupt the runtime during every capture phase, including while a
  trace ring or GC heap is inconsistent; the kernel header and manifest still
  seal with missing sections marked.
- Fuzz the offline dump and trace parsers with lengths, checksums, cycles,
  hostile terms, and unknown schema versions.
- Attempt unauthorized cross-actor tracing, payload capture, and charge
  transfer; verify rejection before publication and audit evidence.
- Compare production behavior with instrumentation on/off to quantify probe
  effect rather than claiming it absent.

## Supported decisions and open questions

Evidence supports controlled actor-level schedule exploration, explicit replay
logs, bounded local trace buffers, explicit loss, and crash capture outside the
failed boundary. It does not establish complete replay of arbitrary BEAM
programs with real NIFs, devices, networks, or durable services; nor does it
select final buffer sizes, sampling policy, or privacy defaults.

The design is falsified if a trace consumer can exhaust the runtime, if a gap
can occur without loss evidence, if replay silently proceeds after an enabled-
set mismatch, if crash capture requires cooperation from the corrupted domain,
or if diagnostic authority allows arbitrary actor-state disclosure.

## Connections

- [Managed actor runtime layer](../managed-actor-runtime-layer.md)
- [Reduction scheduler and kernel scheduling contexts](reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Timers, events, and asynchronous I/O integration](timers-events-and-asynchronous-io-integration.md)
- [Failure translation and the OTP boundary](failure-translation-and-the-otp-boundary.md)
- [Resource accounting and overload control](resource-accounting-and-overload-control.md)
- [Runtime-domain bootstrap and kernel adapter](runtime-domain-bootstrap-and-kernel-adapter.md)
- [Managed-runtime contract inquiry](../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)

## Sources

- [OTP 29.0.6 managed-runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
- [Finding Race Conditions in Erlang with QuickCheck and PULSE](../../30-sources/claessen-et-al-2009-quickcheck-pulse.md)
- [Concuerror](../../30-sources/christakis-et-al-2013-concuerror.md)
- [Efficient and Deterministic Record & Replay for Actor Languages](../../30-sources/aumayr-et-al-2018-actor-record-replay.md)
- [Kdump](../../30-sources/goyal-et-al-2005-kdump.md)
