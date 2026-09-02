---
title: "Raw time and deadline programming"
kind: note
created: "2026-09-02"
maturity: developing
tags:
  - architecture-support
  - interrupts
  - operating-systems
  - scheduling
  - timekeeping
aliases:
  - "Kernel clock and deadline mechanism"
  - "Architecture time component"
---

# Raw time and deadline programming

The best initial implementation is a **qualified monotonic counter domain plus
one absolute, one-shot `TimerChannel` per online CPU**. Counter conversion is
read-mostly and uses generation-published snapshots while a separate
`ClockEra` changes only on genuine discontinuity. `TimerChannel` state is CPU-local,
generation-tagged, integrated with the interrupt fabric, sticky until consumed,
and explicit about cancellation races. Timer queues, CPU budgets, wall-clock
discipline, and BEAM timer semantics consume this mechanism but do not live
inside it.

This is a proposed design, not an implemented result. The scientific and
engineering evidence supports the decomposition and identifies failure modes;
target measurements must still qualify each counter and timer backend.

## Question, scope, and operational standard

The question is:

> What smallest privileged time mechanism gives the kernel trustworthy
> duration measurement and bounded-programming semantics without embedding
> scheduler, civil-time, or managed-runtime policy?

The component owns:

- discovery and qualification of raw counter sources;
- wrapping-counter extension and checked fixed-point conversion;
- continuity across a permitted source or conversion-state change;
- the distinction between CPU-local and system-comparable time;
- programming, cancelling, and observing one-shot deadline events;
- source/deadline quality and fault telemetry; and
- early-boot bounded delays where no event-driven mechanism is available.

It does not own:

- civil time, time zones, leap seconds, NTP/PTP discipline, or trust in an RTC;
- the data structure that multiplexes many software timers onto one channel;
- scheduler quantum, admission control, or scheduling-context policy;
- BEAM `send_after`, receive timeouts, reduction accounting, or actor mailbox
  ordering;
- CPU-frequency policy, oscillator engineering, or platform power policy; or
- a claim of hard real-time response from timer hardware alone.

A satisfactory implementation must pass this operational standard:

1. A successful `read` never moves backward in its declared `ClockDomain` and
   never silently becomes globally comparable when only CPU-local order is
   known.
2. Counter wrap, conversion publication, CPU migration, and supported
   suspend/resume cannot combine state from different generations.
3. For every successfully armed `DeadlineToken`, the channel publishes exactly
   one sticky terminal variant: `Fired`, `Cancelled`, `Rebased`,
   `RebaseFailed`, `EraDiscontinuity`, or `ChannelFailed`. `Rebased` terminates
   the old token and names a distinct replacement token; an old interrupt can
   never discharge that replacement.
4. A deadline earlier than or too close to the programming instant is handled
   as an immediate due event or a declared `TooClose`; it is never lost because
   the counter passed the compare value during programming.
5. The interface reports precision, resolution, minimum programmable lead,
   range, comparability, suspend behavior, and observed lateness. It does not
   advertise a latency bound that only interrupt and scheduling analysis could
   establish.
6. At least x86-64, AArch64, and RISC-V backends can implement the semantics
   without pretending their firmware and counter guarantees are identical.
7. Model, emulator, and hardware tests cover source change, small-width wrap,
   migration, cancellation/fire races, spurious interrupts, and an unresponsive
   CPU.

## Evidence, synthesis, and proposal

| Status | Claim |
| --- | --- |
| Reported evidence | FreeBSD timecounters use source/anchor/conversion snapshots and generation retry to make the common SMP read path lock-free while supporting wrapping counters and source changes. |
| Reported evidence | Linux separates clock sources, clock events, a fast scheduler clock, and delay timers because their stability, cost, locality, and event behavior differ. |
| Reported evidence | Contemporary RTOS work reports benefits from separating a system timebase from per-CPU preemption timers, while explicitly calling its small-platform measurements preliminary. |
| Normative architecture fact | x86 TSC/deadline facilities, the Arm generic counter/timers, and RISC-V `time` plus `stimecmp` or SBI timer service provide different discovery, access, completion, and virtualization paths. |
| Security evidence | Time protection research shows that precise time and timer delivery participate in timing channels; CPU budgets alone do not produce temporal noninterference. |
| Synthesis | One global-qualified counter domain and CPU-local `TimerChannel` instances form a useful portable semantic split even when both use one physical facility. |
| Project proposal | Publish checked conversion snapshots by generation; give every deadline a generation-tagged token; keep the software timer queue and policy above the architecture component. |
| Unverified | Actual read cost, cross-CPU skew, suspend continuity, minimum reliable lead, late-interrupt distribution, and suitability for BEAM scheduler accounting on chosen targets. |

## Why “the timer” is the wrong abstraction

A physical timer block may contain a counter, comparator, interrupt source, and
frequency register, but those mechanisms serve distinct contracts:

| Mechanism | Required semantic property | Typical consumer |
| --- | --- | --- |
| Raw counter | monotonic count with declared width, rate, scope, and stability | accounting and duration measurement |
| Monotonic synthesis | continuous non-decreasing value in a named domain | portable kernel code |
| Deadline comparator | one event at or after an absolute target | timer-queue head and budget expiry |
| Fast scheduler sample | very cheap local elapsed-time estimate | optional scheduler optimization |
| Delay source | bounded busy wait before sleep/event service exists | early bring-up only |
| Civil-time source | externally disciplined date/time with trust and uncertainty | service above the kernel |

Combining these behind one unqualified `timer_read()` invites errors. A cheap
per-CPU cycle count may not be comparable after migration. A high-quality
clocksource may be too expensive for every scheduling boundary. A comparator
may share the same count but still have different range, race, and interrupt
properties. The interface therefore names domains and channels rather than
hardware devices.

## Recommended semantic model

### Clock domains and quality

The common layer should expose an immutable `ClockProfile`, a continuity
`ClockEra`, and independently published conversion snapshots:

```text
ClockProfile {
  source_id,
  counter_width,
  nominal_frequency,
  read_cost_class,
  scope: CpuLocal | Package | System,
  comparability: Unqualified | MonotonicLocal | GlobalBoundedSkew(max),
  rate: Variable | Stable | ArchitecturallyInvariant,
  suspend: Stops | Continues | Unknown,
  virtualization: Native | Offset | Trapped | Unknown,
  observation_order,
}
```

The words are promises, not hints:

- `MonotonicLocal` permits elapsed-time comparisons only on the originating
  CPU and generation.
- `GlobalBoundedSkew(max)` permits cross-CPU comparison only within the stated
  uncertainty; qualification records the method and platform revision.
- `Unqualified` is usable during controlled bring-up but cannot back scheduler
  accounting or timeout correctness.
- `ArchitecturallyInvariant` describes rate, not necessarily reset value,
  cross-socket synchronization, suspend continuity, or virtualization honesty.

If no fast source qualifies globally, retain a CPU-local fast sample for local
accounting and use a slower system counter for portable monotonic time. Do not
clamp divergent CPU-local readings into a fake global clock: clamping hides a
source defect and can accumulate unbounded error.

### Instant types

Use distinct opaque values rather than naked nanoseconds:

```text
RawTicks(source, cpu_or_scope, source_generation, value)
MonotonicInstant(domain, clock_era, nanoseconds)
Duration(nanoseconds)
DeadlineTarget(domain, clock_era, instant)
```

Arithmetic is intentionally narrow:

- subtract two compatible instants to obtain a checked duration;
- add a bounded duration to an instant to obtain a target;
- reject cross-domain or stale-era comparison unless an explicit
  conversion snapshot covers both; and
- saturate or return overflow instead of wrapping a public duration silently.

A counter read is not a memory fence. The backend states whether the sample is
ordered with earlier/later execution and provides a separately named ordered
read when accounting needs a causal boundary around context entry or exit.

### Generation-published conversion snapshot

The preferred read path adapts the timecounter/timehands idea to the
implementation language's memory model:

```text
ConversionSnapshot {
  snapshot_generation,
  clock_era,
  source_generation,
  base_ticks,
  base_nanoseconds,
  mask,
  multiplier,
  shift,
  valid_until,
}
```

A reader:

1. acquires a pointer/version to one immutable snapshot;
2. reads the counter specified by that snapshot;
3. computes `delta = (ticks - base_ticks) & mask`;
4. computes the checked fixed-point product and shift;
5. revalidates the snapshot generation; and
6. retries if publication raced, the snapshot expired, or the source reported
   an impossible delta.

Use a widened intermediate—native 128-bit arithmetic where available or a
proved multiword operation—and calculate multiplier/shift error bounds at
initialization. The maximum interval between anchor updates must be comfortably
shorter than the ambiguity interval implied by source width and rate. A model
backend with an 8- or 12-bit counter should make wrap bugs routine to test.

Writers are rare. A recalibration or qualified source replacement samples the
old monotonic value, samples the new source under its required ordering, builds
a complete new snapshot whose base preserves continuity, and publishes a new
`ConversionSnapshotGeneration` without changing `ClockEra`. A reader never
observes a new source with old scale data. Only a proven discontinuity advances
`ClockEra`; that transaction seals `EraDiscontinuity` for every still-open
old-era deadline token.

### Monotonic floors

For a genuinely shared, globally ordered counter, the snapshot calculation is
enough. A per-domain atomic “last returned” floor should not be added by
default: it would introduce a contended cache line and can mask faulty
hardware. Use a floor only at an explicit compatibility boundary, record every
clamp as a quality fault, and fail the source if clamps exceed a small
qualification threshold.

### Suspend and reset

Define at least two potential time domains above raw counts:

- `ActiveMonotonic`, which may pause while the machine is suspended; and
- `ContinuousMonotonic`, which includes suspend only when the platform supplies
  a counter or authenticated resume delta with that guarantee.

The mandatory baseline needs `ActiveMonotonic`. Continuous time is an optional
profile. Resume publishes a new conversion snapshot when continuity remains
proved. If continuity cannot be proved, it advances `ClockEra` and seals an
`EraDiscontinuity` terminal record for each still-open old-era token rather than
silently inventing elapsed time.

## `TimerChannel` contract

### Token and state

Each online CPU owns one baseline channel. It is programmed only on its owner
CPU; a remote request is delivered through the CPU-request mechanism. State is
preallocated and protected by local interrupt exclusion or a small proven
atomic protocol:

```text
TimerChannelState:
  Idle(channel_generation)
    -> Armed(token, absolute_target)
    -> DuePending(token, observed_time)
    -> Idle(next_generation)

  Armed(old_token)
    -> RebaseClaimed(old_token, prepared_new_token)
       -> Armed(new_token) | DuePending(new_token) | Idle | Failed

  Armed(token)
    -> CancelClaimed(token) -> Idle | Failed

  Idle/Armed/DuePending/RebaseClaimed/CancelClaimed
    -> Failed(reason) -> Disabled(next_generation)

DeadlineTokenState:
  Open(token)
    -> Terminal(
         Fired(observed_time, late_by)
       | Cancelled
       | Rebased(new_token, effective_target, conversion_generation)
       | RebaseFailed(reason, channel_post_state)
       | EraDiscontinuity(old_era, new_era, evidence)
       | ChannelFailed(reason, channel_post_state))
    -> Consumed(terminal_generation)
```

Channel health and accepted-token evidence are separate. Every accepted token
has a preallocated terminal slot. All fire, cancel, rebase, discontinuity, and
failure paths compete to change that slot exactly once from `Open` to one
closed `DeadlineTerminal` variant. A failure may disable future programming,
but it cannot overwrite a sealed terminal record; the record remains immutable
and pollable until its consumer explicitly acknowledges it. Interrupt-event
notification is a bounded hint that a terminal record is ready, not another
completion outcome.

`DeadlineToken` contains the channel identity, CPU generation, channel
programming generation, clock era, source generation, conversion-snapshot
generation used to derive the compare, and an opaque caller-operation
generation. It does not expose or depend on a software timer-queue head.
Numeric hardware compare values are not authority and are never accepted as
completion handles.

Comparator/token state belongs to this component. Its timer interrupt source,
controller flow, route, binding generation, and bounded `EventSink` belong to
the [interrupt event fabric](interrupt-event-fabric.md). A `TimerChannel`
therefore retains the current interrupt-binding generation but does not perform
controller transitions itself.

### Public interface and sticky observation

`TimerChannel` is the only public channel object name; no second deadline-
channel type or alias exists. The semantic interface is:

```text
timer_arm_absolute(channel, target)
  -> Rejected(ArmError, unchanged_channel)
   | Accepted(DeadlineToken, effective_target, rounding)

deadline_poll(token)
  -> Pending(Armed | DuePending | RebaseClaimed | CancelClaimed)
   | Terminal(DeadlineTerminal, terminal_generation)
   | StaleToken

deadline_cancel(token)
  -> Terminal(Cancelled, terminal_generation)
   | PendingTerminal(DuePending | RebaseClaimed | CancelClaimed)
   | AlreadyTerminal(DeadlineTerminal, terminal_generation)
   | StaleToken

deadline_consume(token, terminal_generation)
  -> Consumed | Pending | StaleToken
```

Admission reserves the token's terminal slot before the first hardware or
channel-state mutation. `Rejected` therefore creates no token. Once accepted,
`deadline_poll` never returns an arming or rebase error: it observes the same
sticky terminal record until `deadline_consume` acknowledges the matching
terminal generation. Consumption permits slot reuse and makes later uses of
the old token stale; notification delivery never consumes a terminal record.

### Programming algorithm

The normalized `timer_arm_absolute(channel, target)` operation should:

1. validate the target domain and CPU/channel generation;
2. read `now` using the backend's required ordering;
3. if the target is already due, seal the same terminal `Fired` state
   and request notification without relying on a past compare match;
4. reject or round an interval smaller than the measured safe programming lead
   according to declared policy;
5. publish the new software token before enabling the hardware event;
6. program the absolute target or a checked relative equivalent;
7. re-read status/time if the hardware does not guarantee that a passed target
   becomes pending; and
8. self-trigger the event path if the race window crossed the target.

The success result contains the token, effective target, resolution rounding,
and programming generation. It does not promise an upper latency bound.

### Conversion update with an armed channel

A continuity-preserving conversion/source update freezes new channel
programming long enough to classify every armed token before publishing the
new snapshot. An unchanged hardware compare may remain armed only when the
backend produces a `CompareContinuityProof(old_token, new_snapshot_generation)`
showing that it still denotes the same monotonic target. The token stays open
and retains both its original derivation and that explicit proof.

When the compare must change, rebase is not a second public operation. The
owner CPU performs this exact atomic replacement protocol under the channel's
interrupt-exclusion or equivalent proven serialization:

1. Before mutation, prepare the new compare, a fresh channel/programming
   generation, a distinct `DeadlineToken`, and its terminal slot. Failure here
   leaves the old token armed and returns no replacement.
2. Revalidate the old token, CPU/clock generations, and source snapshot, then
   atomically claim `Armed(old_token) -> RebaseClaimed(old_token,
   prepared_new_token)`. This claim is the arbitration point against fire and
   cancellation. If either already claimed or terminalized the token, rebase
   preserves that result and creates no replacement.
3. Disarm or supersede the old hardware compare and account for any pending old
   interrupt. The old programming generation can complete only its historical
   interrupt-flow record; it cannot address the prepared token.
4. Publish the prepared token's software state before enabling its compare,
   program the replacement, and perform the same passed-target recheck as a new
   arm. If the target became due, seal `Fired` for the new token rather than
   losing the deadline.
5. In one versioned release publication, expose the replacement channel state
   and seal the old token as
   `Rebased(new_token, effective_target, new_snapshot_generation)`. A poll of
   the old token now returns that terminal record; the new token independently
   receives exactly one later terminal variant.
6. If safe replacement cannot be established after the claim, publish one
   atomic fallback state: the old token becomes
   `RebaseFailed(reason, Idle | Failed)`, no replacement token is exposed, and
   the channel is disabled when old-compare quiescence is uncertain.

The conversion snapshot is published only after every affected channel has
recorded a continuity proof, committed a replacement, or reached a terminal
failure. An unreachable owner CPU aborts a still-optional update; it cannot be
silently skipped.

A true continuity loss instead freezes arming and advances `ClockEra` only
after every still-open old-era token has atomically competed for
`EraDiscontinuity(old_era, new_era, evidence)`, or CPU lifecycle proves its
owner cannot execute. A token whose `Fired`, `Cancelled`, or `Rebased` record
was already sealed keeps that record; discontinuity never overwrites it. Thus
era change, fire, cancellation, and rebase still choose one terminal variant
per token.

### Fire and cancellation race

The interrupt fabric claims and masks/acknowledges the timer source according
to its controller flow, then invokes this component with both the interrupt-
binding and channel-programming generations. This component samples time and
atomically seals a preallocated terminal `Fired` record before the
fabric attempts a bounded notification. The event includes:

- token and channel/CPU generation;
- requested and effective target;
- observed interrupt-entry time;
- `late_by = max(0, observed - effective_target)`; and
- flags for spurious, reprogrammed, or source-quality anomalies.

If the destination sink is full, the terminal fired record remains sticky and
inspectable until consumed; later notices may coalesce, but the accepted
token cannot lose its one terminal outcome. A stale interrupt
binding or channel generation can complete only its historical flow token and
cannot fire a replacement deadline.

Cancellation returns one of:

```text
Terminal(Cancelled, terminal_generation)
PendingTerminal(DuePending | RebaseClaimed | CancelClaimed)
AlreadyTerminal(DeadlineTerminal, terminal_generation)
StaleToken
```

Cancellation first claims `Armed(token) -> CancelClaimed(token)`, then disarms
or supersedes the compare and seals `Cancelled` only after an old-generation
interrupt cannot win the token. An unprovable disarm seals `ChannelFailed`
instead. It never returns an ambiguous Boolean. If cancellation loses to fire, rebase,
era discontinuity, or channel failure, `deadline_poll` exposes the winner's
sticky record. If rebase claimed first, the caller follows the old token's
`Rebased` result and may separately cancel the replacement token. This provides
exactly one terminal result per accepted token at the software boundary even
when hardware can produce a late or spurious interrupt; it does not claim that
the physical interrupt occurs exactly once.

### Multiplexing stays above

The scheduler/timer service maintains a queue of software deadlines and arms
the channel only for the earliest effective target. It decides:

- coalescing and slack;
- timer priority and budget;
- periodic rescheduling;
- cancellation ownership;
- actor-facing timeout semantics; and
- whether a missed deadline causes a wakeup, timeout fault, or degraded mode.

The architecture component sees one token at a time. This keeps red-black
trees, timing wheels, BEAM timer wheels, and policy-specific batching out of
the privileged architecture backend.

## Cross-ISA realization

| Concern | x86-64 | AArch64 | RISC-V |
| --- | --- | --- | --- |
| Preferred counter | invariant TSC only after CPUID/platform qualification and cross-CPU checks | architectural system counter through the permitted physical or virtual count view | `time` counter when access, rate, and scope are established by the platform profile |
| Preferred deadline | per-logical-processor local APIC TSC-deadline mode | per-PE generic timer compare/value register | direct `stimecmp` with Sstc; otherwise SBI TIME absolute programming |
| Arm/disarm shape | nonzero absolute TSC value arms; zero disarms; firing clears the MSR | compare/value plus enable/mask/status controls | compare becomes pending when `time >= stimecmp`; far-future compare or interrupt mask cancels; SBI TIME normalizes through firmware |
| Important caveat | invariant rate does not alone prove socket synchronization, suspend continuity, or honest virtual TSC | access level, selected physical/virtual view, counter frequency, and suspend behavior are profile facts | base ISA does not guarantee the whole supervisor timer path; Sstc and SBI are discovered dependencies |
| Spurious/race handling | account for non-serializing writes and APIC delivery latency | account for enable/compare ordering and interrupt-controller latency | software must tolerate eventual pending-bit updates and an occasional spurious interrupt after advancing `stimecmp` |

### x86-64 backend

Use TSC only after checking the documented invariant property, discovering or
calibrating frequency, testing every participating logical CPU, and recording
virtualization/firmware assumptions. Boot qualification should sample
cross-CPU offsets repeatedly under controlled rendezvous and retain a maximum
observed skew; multi-socket acceptance needs a stricter platform rule than
single-package development hardware.

TSC-deadline mode is attractive because it accepts an absolute value in the
same counter domain and is one-shot. The backend still needs explicit ordering
around the MSR write where required and must measure the minimum dependable
lead. A platform without a qualifying TSC can fall back to a slower discovered
system counter; it must not keep the same “fast global” quality label.

### AArch64 backend

The generic timer naturally separates a system counter from per-PE timer
views. Choose one privileged physical or virtual domain for kernel use and
record its frequency and offset assumptions. The compare-value form is the
preferred absolute interface. Required instruction synchronization around
control changes belongs in the backend.

The architecture supplies mechanisms, but the concrete platform profile must
still state whether the system counter continues in relevant low-power states,
whether all PEs observe the same count, and what a hypervisor may virtualize.

### RISC-V backend

Treat RISC-V as the portability test. `time` is a clock input, not necessarily
a per-hart cycle counter, but access and platform properties are profile facts.
On an Sstc system, program `stimecmp` directly. On another system, use the
ratified SBI TIME extension and include firmware call latency in the channel
quality.

The Sstc pending signal may update eventually rather than immediately, and the
specification warns software to tolerate a spurious timer interrupt after
advancing the compare. The common token check therefore is required even on a
conforming implementation.

## Interaction with the capability microkernel and managed runtime

The architecture layer's timer channel is not delegated directly to an
ordinary BEAM process. The privileged scheduler/budget mechanism holds channel
authority, multiplexes kernel obligations, and delivers bounded events to
policy. A user-level time service can expose attenuated clocks and software
timers through ordinary capabilities.

The BEAM-compatible runtime then preserves its own semantics:

- reduction accounting remains runtime policy and is not defined by raw ticks;
- scheduler threads may use kernel accounting and deadlines but do not program
  hardware registers;
- receive timeouts and timer messages are generated by a runtime/system timer
  service with its documented ordering and cancellation rules;
- process-local tracing garbage collection is unaffected and remains outside
  the privileged kernel; and
- supervisors observe timeout or timer-service failure as structured service
  failures, not as fabricated actor messages from hard interrupt context.

Runtime timers can be numerous. Their scalability depends on the timer queue
and distribution policy above this component; one one-shot channel per CPU is
not one hardware object per actor.

## Safety, security, and failure analysis

### Counter failure

Detect and record:

- backward raw samples outside permitted wrap arithmetic;
- a delta larger than the snapshot's safe ambiguity interval;
- cross-CPU offset or drift exceeding the qualified bound;
- source frequency disagreement with a reference beyond tolerance;
- counter stop in a state declared continuous;
- a firmware or hypervisor source-generation change; and
- read faults or unavailable counter access.

On failure, stop using the source for protection decisions, switch only through
the continuity transaction if a qualified fallback exists, and mark affected
accounting intervals uncertain. A scheduler cannot safely charge time it
cannot measure; recovery policy may need to stop admission or the machine.

### Deadline failure

Failures include a compare write fault, impossible status, event before the
permitted rounding window, extreme lateness, repeated spurious delivery, and a
CPU going offline with an armed token. The channel enters `Failed` or is
transferred through the CPU-offline protocol. Outstanding upper timers receive
their token's explicit `Rebased`, `RebaseFailed`, `EraDiscontinuity`, or
`ChannelFailed` terminal outcome; failure cannot overwrite an already sealed
`Fired` or `Cancelled` record.

Timer hardware cannot prove response time. An interrupt can be delayed by
masking, a higher-priority event, firmware, a stalled CPU, or kernel critical
section; the intended thread can then wait for scheduling budget. A hard bound
requires the interrupt, kernel, and scheduler analyses in addition to this
component's minimum lead and programming cost.

### Timing channels and clock authority

Fine clocks make many microarchitectural channels easier to measure, but hiding
one clock does not remove alternate clocks or contention. Keep full-resolution
time for kernel correctness. User-facing services can apply capability-
controlled precision, jitter, or virtual domains as part of an explicit threat
profile. A high-security time-protection profile additionally needs cache and
interrupt partition/flush/padding mechanisms; this component alone cannot
claim temporal noninterference.

### Denial of service

Untrusted callers must not force a hardware reprogram on every tiny timer
change. The upper timer service should bound outstanding timers, charge queue
memory and reprogram work, enforce a minimum deadline lead, and coalesce within
delegated slack. Recovery and budget-expiry timers retain reserved capacity so
ordinary actor load cannot starve supervision.

## Verification strategy

### Executable model

Model the counter and channel separately, then compose them with CPU lifecycle.
Use deliberately adversarial behavior:

- 8-bit wrapping counter with arbitrary preemption between read steps;
- conversion publication during every reader step;
- old/new source changes with offset and frequency differences;
- counter read on the wrong CPU after migration;
- compare target crossed before, during, and after programming;
- delayed pending-bit clear and one extra spurious interrupt;
- cancellation and fire concurrent with every rebase step;
- continuity loss concurrent with fire, cancellation, and a prepared rebase;
- CPU offline after token publication; and
- deadline interrupt delivered with an old CPU generation.

Safety properties should include monotonicity within a domain, no accepted
event for a stale token, exactly one terminal variant per accepted token, a
`Rebased` old token naming exactly one distinct replacement, no replacement
after `RebaseFailed` or `EraDiscontinuity`, and no online CPU without an enabled
channel. Repeated polls must return the same terminal generation until explicit
consumption. Liveness is conditional on a progressing CPU and functioning
interrupt path.

### Arithmetic and memory-model proof obligations

- Prove multiplier/shift error and maximum input range.
- Prove wrap subtraction is unambiguous inside `valid_until`.
- Prove snapshot publication cannot mix fields under the implementation
  language memory model.
- Inspect generated backend code for the required counter-read and comparator-
  write ordering.
- Use property tests against arbitrary-precision reference arithmetic.

### Emulator and hardware fault tests

- Skew one virtual CPU's counter and confirm it is rejected from the global
  domain.
- Change a virtual counter rate or offset across suspend/resume.
- Inject delayed, duplicated, and dropped timer interrupts.
- Reprogram and cancel at every instruction-sized offset around a target.
- Rebase across every supported source/conversion change and inject failure at
  every replacement step; poll both old and replacement tokens.
- Force an era discontinuity against each open/claimed/terminal token state.
- Offline a CPU with an armed timer and verify transfer/failure semantics.
- Run with interrupts masked near the permitted maximum and verify lateness is
  reported rather than concealed.

### Benchmarks

Report distributions and configuration, not a single average:

- raw read and converted-read cycles;
- publication retry frequency under forced source updates;
- cross-CPU skew distribution and drift over temperature/power states;
- arm, cancel, and re-arm cost;
- minimum reliable lead time;
- interrupt-entry and eventual-thread-wakeup lateness at median, p99, p99.9,
  p99.99, and observed maximum;
- behavior under IPC, TLB-shootdown, interrupt, DMA, and BEAM scheduler load;
- idle residency and interrupt reduction compared with a periodic tick; and
- timer-queue reprogram rate for representative actor timeout workloads.

All results must name machine, firmware/hypervisor, CPU topology, counter
source, timer backend, frequency policy, interrupt priority, and kernel build.

## Staged implementation

### Stage 0: model backend

Implement narrow wrapping counters, controllable skew, source changes, and a
deadline device that can be late, duplicated, or lost. Complete the state-
machine and arithmetic tests before hardware code.

### Stage 1: uniprocessor bring-up

Support one raw source, one absolute one-shot channel, generation tokens, and
observed lateness. Use busy waits only in bounded early boot. The first port
may use the architecture's simplest dependable counter/timer pair.

### Stage 2: static SMP

Qualify comparability, add per-CPU channels, remote programming through the
CPU mailbox, and timer transfer during logical CPU parking. Integrate the
software timer queue and CPU-budget expiry above the facade.

### Stage 3: source quality and suspend

Add drift monitoring, fallback-source continuity transactions, active versus
continuous domains, suspend/resume generations, and hypervisor profile tests.

### Stage 4: performance and security profiles

Only after measurement, consider a separate cheap local scheduler clock,
user-visible coarse/virtual clocks, coalescing policies, and time-protection
integration. None should weaken the baseline correctness clock.

## Alternatives and tradeoffs

| Alternative | Advantage | Rejected or deferred because |
| --- | --- | --- |
| Mandatory periodic tick | simple scheduler integration | couples precision to interrupt cost, creates idle noise, and hides the one-shot mechanism upper layers need |
| One global hardware timer interrupt | simple global queue | becomes a routing/bottleneck dependency and complicates CPU failure; per-CPU channels localize wakeups |
| Raw cycles as portable time | extremely cheap | frequency, migration, wrap, and virtualization make them an unsafe common unit |
| Always serialize through a global lock | simple publication argument | turns a ubiquitous read into shared contention; generation snapshots fit the read-mostly workload |
| Clamp every backward sample | preserves a non-decreasing API superficially | hides skew/source failure and can distort budgets indefinitely |
| Require one globally synchronized fast counter on every platform | simple type surface | excludes valid systems and encourages false qualification; explicit local domains are safer |
| Put the timer wheel in the architecture backend | fewer layers | embeds scheduler/runtime policy and makes backend verification much larger |
| Allow direct actor access to timer hardware | potentially low latency | bypasses authority, accounting, reserved recovery capacity, and bounded hard-path delivery |
| Enable advanced virtual/precise clocks immediately | richer API | increases side-channel and virtualization assumptions before the baseline is measured |

## Unresolved questions

- Which first hardware target offers the clearest globally comparable counter
  and one-shot channel with accessible fault injection?
- What skew bound is acceptable for migration-sensitive CPU budget accounting,
  and must multi-socket systems use a slower shared source?
- Does the implementation language provide a suitable seqlock/epoch pattern,
  or should conversion snapshots be immutable pointer swaps with reclamation?
- Which deadlines must survive suspend, and what higher-layer semantics apply
  when continuous time cannot be reconstructed?
- What minimum lead and coalescing slack preserve BEAM responsiveness without
  allowing reprogramming denial of service?
- Should the baseline expose an ordered clock read, or should every accounting
  call pair an ordinary read with an explicit architecture barrier?
- How will deterministic replay record clock reads and deadline delivery
  without making raw time part of a stable kernel ABI?
- What clock precision should untrusted actor domains receive under the
  high-security time-protection profile?

## Connections

- [Kernel hardware and architecture support layer](kernel-hardware-and-architecture-support-layer.md) — defines this component's place between raw architecture mechanisms and timer/scheduler policy.
- [Typed kernel-facing architecture facade](typed-kernel-facing-architecture-facade.md) — supplies the typed object and split-phase completion vocabulary used here.
- [Logical-CPU coordination and lifecycle](logical-cpu-coordination-and-lifecycle.md) — owns channel creation, transfer, and failure during CPU start and removal.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) — consumes deadlines for budgets, bounded IPC, recovery, and fault handling.
- [BEAM, ERTS, and OTP principles for a new operating system](beam-erts-and-otp-principles-for-a-new-operating-system.md) — keeps actor timers, reductions, and supervision above raw hardware time.
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — remains open until these semantics and bounds are exercised on real ports.

## Sources

- [Timecounters: Efficient and precise timekeeping in SMP kernels](../30-sources/kamp-2002-timecounters.md) — generation-published conversion state, wrap constraints, and source switching.
- [Efficient design of high-resolution timekeeping in real-time operating systems](../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md) — current evidence for global-time/per-CPU-deadline separation and tickless tradeoffs.
- [Linux kernel low-level core API documentation](../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — mature separation of clock sources, clock events, scheduler clocks, and delay timers.
- [Intel 64 and IA-32 system programming documentation](../30-sources/intel-2026-system-programming-documentation.md) — TSC discovery, invariance constraints, and TSC-deadline mechanism.
- [Arm A-profile system architecture documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — architectural generic counter and timer semantics.
- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md) — `time`, supervisor timer, and privilege/environment dependencies.
- [RISC-V supervisor binary interface](../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — the higher-privilege TIME boundary plus fallible HSM, IPI, and remote-fence services in the underlying specification.
- [Scheduling-context capabilities](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — shows how a deadline mechanism is consumed by explicit CPU-budget authority rather than becoming scheduling policy itself.
- [Time protection: The missing OS abstraction](../30-sources/ge-et-al-2019-time-protection.md) — bounds claims about clocks, budgets, and timing-channel isolation.
