---
title: "Timers, events, and asynchronous I/O integration"
kind: note
created: "2026-09-03"
maturity: developing
tags:
  - actor-model
  - asynchronous-io
  - beam
  - event-loops
  - timers
aliases:
  - "Managed runtime timers and I/O"
  - "Runtime event integration"
---

# Timers, events, and asynchronous I/O integration

The best initial design uses **sharded hierarchical timing wheels for abundant
coarse actor timers, a small ordered structure for near or high-resolution
deadlines, and a bounded number of kernel deadline channels**. Kernel timer
delivery is a coalescing wakeup, not one privileged object per actor timer. A
runtime scheduler or timer worker reads monotonic time, expires a charged
bounded batch, publishes compatible timeout signals, and rearms the earliest
relevant deadline.

Asynchronous I/O follows the same identity and completion discipline but not
the same semantics as a timer. Polling/completion contexts never execute actor
code. Every request and buffer remains owned by a gateway until exactly one
terminal completion wins. Cancellation is a request that can race with
completion; it is not permission to free memory or claim that a device effect
did not happen.

The wheel/ordered hybrid is a research proposal. Timing-wheel analysis supports
efficient abundant timers, while high-resolution timer experience is negative
evidence against using a coarse wheel for every precision class. The exact
shard count, levels, granularity, crossover, and polling arrangement require
target measurements.

## Question, scope, and operational standard

The question is:

> How can millions of actor timeouts and asynchronous service completions be
> represented cheaply while preserving monotonic-time behavior, generation
> safety, cancellation races, bounded scheduler work, and kernel resource
> ownership?

This component owns:

- actor timer records, references, queues, cancellation, and expiry batching;
- mapping runtime deadlines onto kernel `TimerChannel` objects;
- monotonic time and clock-era adaptation at the runtime boundary;
- readiness/completion poll contexts and one-shot rearm state;
- I/O request identity, buffer/resource retention, terminal arbitration, and
  actor signal translation;
- late/stale completion rejection after actor/service/runtime restart; and
- timer/I/O counts, bytes, lateness, queue depth, cancellation, and overflow
  metrics.

It does not own raw clocks, interrupt delivery, device drivers, networking, or
the application meaning of a timeout. Those are kernel mechanisms, isolated
services, or actor protocols.

An acceptable implementation must satisfy:

1. An accepted timer never delivers before its deadline in the declared
   monotonic domain; lateness is measured and only bounded when the service
   profile supports a bound.
2. A timer or I/O slot is generation stamped, so a stale fire, cancel, or
   completion cannot affect a reused object. PID destinations additionally
   bind an actor generation; registered-name destinations deliberately resolve
   the current local registrant at expiry, as the compatibility profile
   requires.
3. Each timer/request generation has exactly one terminal disposition, while
   the compatibility API preserves any intentionally ambiguous return value.
4. Expiry, cascade, cancellation, completion, and signal publication run in
   bounded charged batches.
5. Logical cancellation never releases a buffer, DMA mapping, endpoint, or
   service lease before terminal ownership is established.
6. A poll or kernel event is a wake hint; canonical operation state remains
   observable despite coalescing, duplication, or ring overflow.
7. Actor scheduler threads never block on a device operation.

## Evidence, synthesis, and proposal

[Varghese and
Lauck](../../30-sources/varghese-lauck-1987-timing-wheels.md) classify timer
structures and show how circular, hashed, and hierarchical wheels can make
common start/stop/maintenance operations constant time under chosen range and
granularity assumptions. They do not bound a bucket containing a burst of
simultaneous expiries or address multicore cancellation.

The official [OTP 29 runtime
documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
states that actor timers use Erlang monotonic time, currently have millisecond
resolution, do not fire early, and may fire late under load. Cancellation/read
results can be ambiguous about whether a timeout message is already queued.
For `start_timer`/`send_after`, a PID destination is automatically cancelled on
target exit, while an atom is resolved as a local registered name at expiry and
is not automatically cancelled. OTP 29 also suspends BIF timers addressed by
PID while that process is suspended; name-addressed timers are unaffected.
Current resolution and internal timer structure are implementation facts, not
the language contract.

The kernel's [raw time and deadline
component](../kernel-hardware-and-architecture-components/raw-time-and-deadline-programming.md)
already separates qualified monotonic counters from one-shot CPU-local
`TimerChannel` mechanisms and represents discontinuity explicitly. The
[interrupt event
fabric](../kernel-hardware-and-architecture-components/interrupt-event-fabric.md)
provides bounded notifications whose sequence/terminal state is stronger than
the wake itself.

| Status | Claim |
| --- | --- |
| Algorithm evidence | Hierarchical wheels efficiently cover many coarse deadlines; ordered trees/heaps provide exact minimum selection for a smaller high-resolution set. |
| Compatibility evidence | Actor timers are monotonic, not early, potentially late, and cancellation may race with already queued timeout delivery. |
| Systems evidence | One-shot readiness disable/rearm prevents repeated dispatch before handling; completion I/O retains operation state through asynchronous cancel races. |
| Synthesis | Runtime timers should be cheap user-space objects multiplexed onto a few kernel channels; timer identity and actor/service incarnations must be independent. |
| Project proposal | Per-scheduler/NUMA wheel shards plus near heap/tree, generation-stamped terminal records, bounded expiry, and separate readiness/completion adapters. |
| Unverified | Geometry, precision classes, poller placement, cancellation cost, event batch size, and target lateness. |

## Time domains and timer objects

Actor APIs consume a runtime monotonic domain derived from the kernel's
qualified clock. Civil time and time-zone corrections live in services. The
timer record carries enough provenance to detect a discontinuity:

```text
ActorTimer {
  timer_ref,
  timer_generation,
  owner_actor_generation,
  destination: Actor {
      actor_id,
      actor_generation,
    } | RegisteredName {
      atom_id,
    },
  monotonic_clock_era,
  absolute_deadline,
  suspended_remaining?,
  message_or_action,
  queue_shard_generation,
  charge_reservation,
  state,
}
```

The destination variants have intentionally different lifecycle semantics:

- `Actor` is a PID-like incarnation route. If that actor is already dead or
  exits, the timer is automatically cancelled. If that actor is suspended by
  the compatible process-suspension mechanism, the timer enters a target-
  suspended state until the actor resumes.
- `RegisteredName` stores the atom, not the PID currently behind it. At expiry
  the name registry is consulted once; the timeout goes to the process then
  registered, or is dropped if no process owns the name. Exit of a process that
  happened to own the name earlier does not cancel this timer, and process
  suspension does not pause it.

Name resolution is therefore an explicit compatibility exception to the usual
rule that late events cannot reach a successor actor. It grants only the same
local name-routing behavior as the selected timer API, never kernel authority.

An API timeout expressed as a duration is converted once to a checked absolute
deadline in the active monotonic era. All ordering uses the absolute value;
periodic activity is represented as a sequence of one-shot generations so a
late firing does not silently change the requested cadence policy.

If the kernel reports an era discontinuity, the runtime does not reinterpret
old absolute deadlines through wall time. It seals affected timers with a
declared discontinuity outcome or applies a profile-defined rebasing policy
that creates new timer generations and preserves old-token terminal evidence.

## Hybrid timer data structure

### Coarse hierarchical wheel

Each scheduler or NUMA region owns a wheel shard so the common insert/cancel
path stays local. Levels cover increasing powers of the base tick. A timer is
placed in the level/slot representing the high bits of its remaining interval;
as time advances, distant buckets cascade toward finer levels.

Wheel geometry is immutable for a shard generation:

```text
WheelProfile {
  base_granularity,
  levels[],
  slots_per_level[],
  maximum_interval,
  maximum_expiry_batch,
  cascade_batch,
}
```

A wheel operation is not assumed O(1) merely by name. Metrics include list
length, cascade work, cancellations, empty ticks skipped, and expiry bursts.
A tickless bitmap/index can locate the next nonempty slot without periodic
wakeups, but must be validated against wrap and level-boundary cases.

### Near/high-resolution ordered set

Deadlines closer than a measured horizon or requiring finer resolution enter a
small min-heap or balanced ordered tree. This avoids rounding all precise
timers to the wheel tick and makes the exact next deadline easy to obtain. The
crossover trades ordered insertion cost against cascade and rounding cost and
is runtime policy.

The timer's public semantics do not reveal which structure holds it. Moving a
timer between wheel and near set retains the same generation and charge; the
move is owner-local or protected by one explicit shard protocol.

### Kernel channel multiplexing

One owner computes the minimum active deadline for each admitted runtime
scheduling region and arms a small number of kernel `TimerChannel`s. A channel
token records the timer-queue generation and clock era. When the earliest
deadline changes:

- if it becomes earlier enough to matter beyond minimum lead/rounding, rearm;
- if it becomes later, defer rearm when the currently armed wake is harmless
  and cheaper than cancellation; or
- if cancellation/fire races, inspect the sticky kernel terminal record and
  treat an extra wake as a hint.

No actor timer holds the kernel channel capability. Runtime restart invalidates
the channel binding and all old queue generations.

## Timer state machine

```text
Free(g)
  -> Reserved(g)
  -> Armed(g, destination, deadline, location)
  -> TargetSuspended(g, remaining) -> ArmedAfterResume(g, deadline, location)
  -> ExpiryClaimed(g)
       -> PidTargetValidated(g) -> TimeoutSignalPublished(g)
       -> NameResolvedAtExpiry(g) -> TimeoutSignalPublishedOrDropped(g)
  -> AutoCancelledTargetExit(g)
  -> CancelClaimed(g) -> Cancelled(g)
  -> EraFailed(g)
  -> Retired(g+1)
```

Expiry and cancel compete for one terminal record. A strong internal cancel
that wins before signal publication guarantees no later publication for that
generation. The public OTP-compatible operation may still return an ambiguous
`false` where the reference runtime does: it can mean expired, already
cancelled, nonexistent, or already queued. The implementation does not weaken
its internal state merely because the API combines outcomes.

Actor exit automatically claims PID-targeted timer generations for cancellation
and reclamation in bounded batches. An expiry already published to that PID is
owned by old-generation mailbox cleanup and cannot reach a replacement actor.
A registered-name timer is independent of the old registrant: it remains armed
and resolves the name at expiry, even if that routes to a later registrant.

Suspension/resume is a generation-checked timer transition, not merely a
scheduler flag. For the OTP 29 compatibility profile, PID-targeted BIF timers
do not progress to timeout delivery while the target is suspended and resume
with the reference behavior. Registered-name timers remain active. `read_timer`
and `cancel_timer` results during these races are included in the differential
suite rather than inferred from one queue layout.

## Bounded expiry and lateness

On wake:

1. read ordered monotonic time and verify clock era;
2. claim at most the expiry/cascade work budget;
3. move due records to an owner-local ready list;
4. validate a PID generation or resolve a registered name at expiry, then
   reserve/publish any resulting timeout signal through ordinary message
   admission;
5. record `deadline`, `observed_due`, `published`, and `actor_consumed` times;
6. yield if more due work remains and schedule immediate continuation; and
7. rearm the kernel channel for the next valid deadline.

One million equal deadlines therefore create backlog telemetry and multiple
bounded activations rather than one unbounded pause. They cannot all be
delivered at the exact instant; the service profile publishes the resulting
lateness distribution and saturation behavior.

Timeout construction is charged to the owner/application account. A small
system reserve ensures timer cleanup and control deadlines can progress under
ordinary pressure, but it is finite and cannot carry unbounded application
timers.

## Asynchronous I/O model

I/O is normally performed by isolated services. The runtime sees a typed
gateway request and a bounded completion endpoint:

```text
IoOperation {
  operation_id,
  operation_generation,
  caller_actor_generation,
  service_incarnation,
  endpoint_generation,
  buffer_leases[],
  charge_reservation,
  state,
}
```

### Readiness versus completion

- A readiness API says an operation may make progress. Notification is
  one-shot; the gateway drains/attempts work and explicitly rearms after
  acknowledging the observed generation.
- A completion API says a submitted operation reached a terminal status. The
  request and its buffers remain retained until that terminal result is
  consumed, even if cancellation was requested.

Normalizing both to an actor signal is valid only after the gateway respects
their different ownership rules. A readiness hint is not a completed read; a
cancel acknowledgement is not necessarily the original operation's terminal
completion.

### Completion state machine

```text
New
  -> ResourcesReserved
  -> Submitted(service_incarnation, operation_generation)
  -> Completing | CancelRequested
  -> Completed(result) | CancelledBeforeEffect | Indeterminate(reason)
  -> SignalPublishedOrActorGone
  -> ResourcesReleased
```

Cancel and original completion may arrive in either order. Both address the
same terminal slot; the loser becomes supplemental evidence. Buffers, endpoint
credits, DMA mappings, and service leases release exactly once after terminal
ownership and any device-specific quiescence are established.

The actor-visible reply includes a correlation reference and relevant service
incarnation. Late completions for a dead actor are accounted and discarded;
they never route by slot alone. A service restart makes unresolved operations
`Indeterminate` unless the service produces durable `NotExecuted` or completed
evidence.

## Poller placement

Start with one or a small number of dedicated poll/completion contexts per
runtime or service gateway. They block in kernel wait without occupying actor
schedulers and publish bounded batches into runtime signal ingress.

A single poller can become a bottleneck. Later options include:

- sharding by endpoint/NUMA region;
- moving very active endpoints to scheduler-local poll sets;
- dedicating service-domain completion threads; or
- kernel completion rings with one coalescing notification per shard.

Every option retains the same operation record. Scheduler-integrated polling
is allowed only within a bounded poll budget so hot I/O cannot consume all actor
execution time.

## Failure, security, and resource analysis

- **Timer flood:** reserve timer objects and queue bytes before publication;
  expose owner counts and reject/terminate according to the declared profile.
- **Expiry storm:** bounded batch/cascade, backlog age, and immediate
  continuation preserve unrelated scheduler progress.
- **Clock discontinuity:** seal or explicitly rebase old-era timers; never map
  them through mutable civil time silently.
- **Stale cancel/fire:** generation and queue-shard epoch reject it.
- **I/O buffer use-after-free:** retain until terminal completion and service/
  device ownership proof; poison in tests.
- **Malicious completion:** validate service incarnation, operation ID, length,
  buffer range, and result type before actor term construction.
- **Poller failure:** canonical operation state remains in gateway/service;
  outer supervision replaces the poller and reports gaps/indeterminate work.

## Alternatives and trade-offs

### One kernel timer per actor timer

It makes cancellation direct but moves millions of policy objects into the
kernel and wastes privileged memory/authority. Multiplex in user space.

### Wheel only

Efficient for coarse abundant timers but forces precision/rounding trade-offs
and can burst during cascade. Retain an ordered near set.

### Heap/tree only

Simple exact minimum and good high resolution; logarithmic operations and a
shared hot structure can cost more for millions of coarse timers. It is a
useful baseline and may win on small targets.

### Poll in every scheduler

Can reduce hot-endpoint latency but couples I/O load to actor service and
duplicates poll state. Begin dedicated and add measured local polling.

## Implementation program

### Stage 0: deterministic virtual time

- Implement timer identity/state and a simple ordered queue under a virtual
  monotonic clock.
- Model cancel/fire/actor-exit/reuse and compatibility return values.

### Stage 1: kernel channel integration

- Map the ordered queue onto one `TimerChannel`, handle sticky outcomes and
  era changes, and measure wake/program cost.

### Stage 2: wheel shards and bounded expiry

- Add wheel profile, cascade, near set, shard ownership, and migration.
- Keep a heap-only mode as oracle/performance baseline.

### Stage 3: service completion gateway

- Implement readiness and completion adapters, buffer leases, cancellation,
  stale-incarnation checks, and actor signal translation.
- Add poller sharding only after one-poller measurements.

## Verification and measurements

- Compare heap/tree, wheel, and hybrid with millions of uniform, heavy-tailed,
  clustered, long-range, and mass-cancelled timers; record operation cost,
  memory, wakeups, cascade size, and p99.99 lateness.
- Exhaustively race cancel, expiry, signal publication, PID-target exit,
  suspend/resume, runtime restart, and slot reuse; assert one terminal timer
  disposition.
- Test PID and registered-name destinations separately, including unregistered
  names, name transfer/re-registration before expiry, former registrant exit,
  and OTP 29 PID-only timer suspension.
- Inject wall-clock jumps, monotonic correction, suspend/resume, and a true
  clock-era discontinuity.
- Race I/O completion, cancel, endpoint revocation, service crash, and actor
  restart while poisoning freed buffers.
- Compare dedicated versus sharded/local pollers under cold, hot, and bursty
  endpoints; include CPU, actor latency, backlog, and cross-NUMA traffic.
- Exhaust timer/endpoint budgets and prove cleanup and recovery reserve still
  progresses.

## Supported decisions and open questions

Evidence supports user-space multiplexing, monotonic deadlines, generation
tokens, non-early delivery, explicit lateness, bounded expiry, and
completion-owned resources. The hybrid structure and poller organization are
not yet proven best.

Open choices include timer resolution classes, wheel geometry, shard mapping,
near-set structure, rearm hysteresis, compatibility behavior under domain
pressure, poller count, and which operations can provide `NotExecuted` rather
than `Indeterminate`. Target measurements decide them.

## Connections

- [Managed actor runtime layer](../managed-actor-runtime-layer.md)
- [Raw time and deadline programming](../kernel-hardware-and-architecture-components/raw-time-and-deadline-programming.md)
- [Interrupt event fabric](../kernel-hardware-and-architecture-components/interrupt-event-fabric.md)
- [Signal ingress, mailboxes, and selective receive](signal-ingress-mailboxes-and-selective-receive.md)
- [Native work, ports, and drivers](native-work-ports-and-drivers.md)
- [Resource accounting and overload control](resource-accounting-and-overload-control.md)

## Sources

- [Hashed and hierarchical timing wheels](../../30-sources/varghese-lauck-1987-timing-wheels.md)
- [OTP 29.0.6 managed-runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
- [High-resolution timekeeping](../../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md)
- [CleanQ](../../30-sources/haecki-et-al-2019-cleanq.md)
- [Recovering Device Drivers](../../30-sources/swift-et-al-2004-recovering-device-drivers.md)
