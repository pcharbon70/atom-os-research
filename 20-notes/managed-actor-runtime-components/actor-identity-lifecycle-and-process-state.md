---
title: "Actor identity, lifecycle, and process state"
kind: note
created: "2026-09-03"
maturity: developing
tags:
  - actor-model
  - beam
  - erlang
  - fault-containment
  - process-lifecycle
aliases:
  - "Actor lifecycle component"
  - "Runtime process state"
---

# Actor identity, lifecycle, and process state

The recommended design uses an **opaque, generation-stamped routing identity
and transactionally published actor record**. Internally a local actor identity
contains at least a runtime-domain incarnation, table slot, and slot
generation. A PID resolves only to a message route and current incarnation; it
does not grant a page, device, service, kernel, or native authority.

Spawn reserves all mandatory state and installs the requested atomic link or
monitor relation before the PID becomes visible. Exit makes the actor
nonexecuting, releases directly visible resources, publishes compatible exit
and `DOWN` signals, and then drains remaining heap, signal, binary, code, and
native state in bounded cleanup slices. A slot is not reusable until every
route and retained reference to the old generation is gone.

OTP specifies important observable ordering but not this exact internal
layout, generation width, or reservation protocol. Those are Atom OS
strengthenings intended to make stale-reference and partial-creation failures
explicit.

## Question, scope, and operational standard

The question is:

> How can millions of lightweight actors be created, addressed, observed, and
> reclaimed without stale identity reuse, partial spawn visibility, unbounded
> exit pauses, or confusion between actor reachability and system authority?

This component owns:

- local actor-table slots, PIDs, references, aliases, and incarnation checks;
- the actor control block and language execution-state ownership;
- spawn, publish, suspend, wait, wake, exit, and final reclamation states;
- link and monitor relation records and their lifecycle ordering;
- registration hooks and actor-visible resource-handle ownership;
- process information snapshots and lifecycle telemetry; and
- bounded cleanup worklists.

It does not own message queue mechanics, garbage-collector algorithms,
scheduler selection, service resource policy, distributed routing, or OTP
restart strategy, though it supplies the identities and transition events they
consume.

The initial implementation must satisfy:

1. A delayed signal for an old slot generation can never reach a replacement
   actor.
2. A published PID always resolves to a fully initialized actor whose requested
   atomic spawn relation already exists.
3. At most one scheduler owns and executes the actor's language state.
4. Once an actor enters `Exiting`, it executes no further BEAM instructions.
5. Exit/`DOWN` evidence caused by termination is emitted only after directly
   visible runtime resources reach their declared disposition.
6. Cleanup fan-out is resumable and cannot monopolize one scheduler activation.
7. PID slot reuse occurs only after pending signals, heap/native retention,
   relation records, timers, code references, and diagnostic readers release
   the old generation.

## Evidence and boundary choices

The official [OTP 29.0.6 runtime
documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
defines lightweight processes, atomic spawn-and-link/monitor operations,
links, monitors, aliases, process states, and ordering of termination-related
signals after directly visible resources are released. It also permits eventual
PID reuse; a PID is unique for the relevant live node incarnation, not a
timeless global identity.

[Armstrong's thesis](../../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
supports private process state, asynchronous PID-addressed communication, and
separating a failing worker from the actor that decides recovery. The thesis is
architectural evidence, not a modern capability or multicore implementation
proof.

The external term and distribution model carries node-incarnation information,
showing why an identifier needs a creation epoch across restart. [Orleans
virtual actors](../../30-sources/bernstein-et-al-2014-orleans.md) provide a
useful contrast: stable logical service identity and automatically recreated
activations can simplify a different service model, but must not cause an
expired BEAM PID to resolve silently to a successor incarnation.

The synthesis is:

| Concern | Compatibility floor | Atom OS strengthening |
| --- | --- | --- |
| PID meaning | Identifies a process route in a node incarnation | Explicit runtime epoch and slot generation checked on every resolution |
| Spawn relation | `spawn_link`/`spawn_monitor` provide atomic observable relation | Reserve all mandatory memory/queue/account state before publication |
| Exit | No more actor code; release and signal ordering is observable | Resumable cleanup worklist plus exact disposition records |
| Reuse | Eventually permitted after old process state is gone | Generation change and quarantine before wrap/reuse |
| Authority | Erlang PID supports signaling | No kernel/service capability derivable from PID bits |
| Logical service name | Registration/service mechanisms above PID | Explicit name-to-current-incarnation service with stale-route failure |

## Actor control block

The control block should be divided by ownership and access frequency rather
than becoming one contended structure:

```text
ActorIdentity {
  runtime_epoch,
  slot,
  generation,
}

ActorExecution {                 // owning scheduler only
  status,
  current_module_generation,
  instruction_pointer,
  x_registers,
  stack_and_y_roots,
  exception_state,
  reduction_balance,
  safe_point_epoch,
}

ActorMemory {                    // mutator/collector handoff
  young_space,
  old_space,
  heap_fragments,
  off_heap_list,
  collector_reserve,
}

ActorCommunication {             // concurrent ingress, owner drain
  signal_ingress,
  mailbox,
  receive_cursor,
  links,
  monitors_in,
  monitors_out,
  aliases,
  timers,
}

ActorLedger {
  resource_account,
  queued_bytes,
  retained_shared_bytes,
  table_and_service_handles,
  trace_budget,
}
```

Hot scheduler status and reductions should not share cache lines with
many-producer ingress heads or rarely changed diagnostics. This is a layout
proposal; actor-visible `process_info` fields are derived snapshots, not direct
access to mutable internals.

## Identity allocation and reuse

### Local identity

PID terms should encode or indirectly reference `{runtime_epoch, slot,
generation}` with enough width that accidental wrap is infeasible during the
declared lifetime. The runtime maintains a bounded table whose entry state is:

```text
Free(g)
  -> Reserved(g)
  -> Constructing(g)
  -> Published(g)
  -> Exiting(g)
  -> Retiring(g)
  -> Free(g + 1)
```

A fast lookup reads the entry generation and state, then pins or validates it
before publishing a signal. It never obtains a raw pointer and later assumes
that a recycled entry is the same actor. On a target with small term space,
the PID can point to a level of indirection; compatibility encoding and
internal lookup need not be identical.

Generation wrap is handled as an engineering boundary, not waved away. A
small model must exhaust the generation space and demonstrate quarantine or
runtime-epoch rollover. Production widths should make rollover far beyond the
declared maximum creation rate and uptime, but the terminal behavior remains
specified.

### References and aliases

Unique references carry a runtime epoch and counter/random component sufficient
for the profile. Monitor references identify independent relations. An alias
also binds to its creating actor generation and can be deactivated only under
the compatible rules. Alias validity is rechecked when a signal would enter the
mailbox: deactivation may discard a signal already in flight, while a message
that has already entered the mailbox is not recalled.

Aliases improve request cancellation and mailbox hygiene but do not cancel an
external effect. A service correlation record separately states whether an
operation was not accepted, completed, or remains indeterminate.

## Transactional spawn

```text
Requested
  -> CapacityReserved
  -> ActorConstructed
  -> InitialFrameInstalled
  -> RelationsInstalled
  -> PIDPublished
  -> Runnable
```

1. Reserve a table slot, minimum heap/stack, queue head, actor ledger, and
   scheduling admission against the parent/application account.
2. Copy or validate initial arguments into the new private heap.
3. Construct the initial call frame and error/exception state.
4. If requested, install the link or monitor relation with an explicit
   linearization point visible to both participants.
5. Publish the slot and PID with release ordering.
6. Place the actor on exactly one scheduler queue.

Failure before publication rolls back silently except for the documented
spawn result. Once published, failure is actor termination and follows ordinary
exit semantics. The runtime must not return a PID whose actor could never have
run because a later mandatory reservation failed.

Concurrent parent exit is part of the relation protocol. For `spawn_link`, the
outcome must match the pinned reference behavior: the child cannot escape a
link that was promised atomically, and no relation can target a recycled
participant. Model tests should treat publication, relation installation, and
exit signal generation as explicit choice points.

## Scheduling lifecycle

The semantic states are narrower than implementation flags:

```text
Runnable(owner_queue)
  -> Running(owner_scheduler)
  -> Runnable | Waiting(reason) | Suspended(reason) | Exiting(reason)

Waiting -> Runnable             // one successful wake publication
Suspended -> Runnable|Waiting   // authorized resume
```

Only the owner scheduler touches instruction state, stack, or actor heap.
Concurrent senders publish signal nodes. A wake operation atomically changes
the actor from a nonrunnable state or observes that it is already runnable or
running; duplicate wake hints do not create duplicate queue ownership.

Migration is an ownership transfer while runnable, not while executing. The
old queue removes or marks the actor, the transfer record names the destination
and generation, and only the destination may publish it runnable. Topology
hints never alter PID or message semantics.

## Exit and reclamation

```text
Alive
  -> ExitClaimed(reason, evidence)
  -> LanguageStopped
  -> VisibleResourcesReleasing
  -> DeathSignalsPublishing
  -> ResidualStateDraining
  -> SlotRetired
```

Exactly one exit claimant seals the primary reason. Later faults can append
evidence but cannot replace it with a generic reason. Untrappable kill,
uncaught exception, normal return, link exit, resource termination, and domain
fault remain distinguishable at the boundary allowed by the compatibility
profile.

Directly visible resources include registration and table ownership/heir
effects, active aliases, link/monitor state, and port/service relationships as
defined by the profile. Their terminal dispositions are established before
termination-caused exit and `DOWN` signals are exposed.

Large fan-out becomes a cleanup worklist:

- detach at most `N` relation records per cleanup slice;
- publish at most a charged signal batch;
- yield with the actor permanently nonexecuting;
- retain the slot generation until all work and delayed readers finish; and
- run cleanup from a capped reserve that ordinary actors cannot exhaust.

Heap destruction is normally wholesale after shared binary, literal, native,
and table references are reconciled. A dirty in-process NIF can delay final
control-block reclamation in a compatibility profile, which is another reason
to isolate native work by default.

## Links, monitors, and registration

- A link is one symmetric relation per actor pair. Both endpoints hold or can
  derive one relation generation; link/unlink races preserve sender-order rules.
- Monitors are unilateral and independently referenced. Repeated monitors are
  distinct and each has one terminal `DOWN` or explicit demonitor disposition.
- Registered names are runtime/service mappings to one PID generation. Actor
  exit removes the name before termination evidence required by the profile.
- A name lookup followed by send is not magically atomic with name rebinding;
  protocols needing that property use a generation-bearing service handle.

No relation is a proof of cause. A remote monitor can report connection loss,
not that a particular remote actor definitely executed or died. The
distribution gateway preserves that uncertainty.

## Failure, security, and resource analysis

- **PID guessing:** ordinary PID possession grants signaling reachability under
  runtime policy, not service or kernel authority; restricted profiles may add
  send scopes above compatibility semantics.
- **Slot exhaustion:** spawn refuses before publication and reports the actor
  and parent account; it never reuses a live/retiring slot early.
- **Generation attack:** every signal, timer, service reply, and diagnostic
  request revalidates runtime and actor generations.
- **Exit storm:** cleanup is batched, charged, and protected by a finite reserve;
  telemetry records backlog and oldest cleanup age.
- **Process-info races:** snapshots carry actor generation and completeness;
  a reader sees a coherent subset or `exited`, never fields from a successor.
- **Runtime corruption:** actor isolation is lost; the kernel freezes the
  domain and the outer recovery service creates a new runtime epoch.

## Alternatives and trade-offs

### Reuse ERTS PID packing exactly

This may ease term compatibility but would freeze a current implementation
choice into the new runtime. Preserve external encodings where required while
using a generation-safe internal route table.

### Make PIDs object capabilities

This gives strong designation semantics in some systems, but it conflates
ordinary Erlang messaging with kernel/device authority and makes serialization
dangerous. Keep actor routing and system authority separate.

### Stable virtual actors as the baseline

Automatic reactivation is useful for a service layer, as Orleans demonstrates,
but changes explicit Erlang process lifetime, volatile state, links, and PID
incarnation. Implement it above the runtime through named services and durable
state, not by silently resurrecting PIDs.

## Implementation program

### Stage 0: formalized bounded model

- Model tiny actor, slot, generation, reference, link, and monitor spaces.
- Explore spawn/link/monitor, immediate exit, unlink/demonitor, alias
  deactivation, delayed signal, and slot reuse races.
- Derive state-machine fixtures from every counterexample.

### Stage 1: deterministic single-scheduler lifecycle

- Implement identity table, spawn, wait/wake, exit, links, monitors, aliases,
  registration, and bounded cleanup.
- Differentially compare externally visible results with OTP 29.0.6.
- Force GC and actor exit at every transition.

### Stage 2: concurrent ingress and multicore ownership

- Add atomic route lookup/pinning, cross-scheduler wake, migration, and
  concurrent relation operations.
- Run stress tests under scheduler pre-emption and context revocation.

### Stage 3: domain restart and services

- Propagate runtime epochs through gateways, native-service handles, crash
  records, and external PID encoding.
- Verify complete rejection of old-incarnation routes after restart.

## Verification and measurements

- Exhaustively wrap a tiny PID generation space with delayed messages and
  diagnostic readers.
- Race `spawn_link`, `spawn_monitor`, immediate child exit, parent exit,
  registration, unlink, and demonitor against the reference runtime.
- Exit actors with 1 through 1,000,000 links/monitors; report per-slice work,
  total cleanup time, unrelated p99.9 scheduling latency, and reserve use.
- Terminate actors owning tables, aliases, timers, binaries, ports, code
  generations, and native requests; verify disposition-before-death ordering.
- Randomly revoke scheduler contexts during run/wake/migration transitions and
  assert one owner and no lost runnable actor.
- Fuzz `process_info` and trace snapshots during reuse to detect mixed
  generations.

## Supported decisions and open questions

Evidence supports explicit actor incarnations, atomic spawn relations, no
language execution after exit, resource-disposition ordering, and keeping PID
reachability distinct from authority. Generation width, slot-table layout,
pinning/reclamation method, exact cleanup batch size, and which snapshots need
linearizability remain implementation experiments.

The key falsifier is stale delivery: any test in which a delayed message,
timer, `DOWN`, service completion, trace event, or process-info request is
accepted by a successor actor invalidates the identity design.

## Connections

- [Managed actor runtime layer](../managed-actor-runtime-layer.md)
- [Signal ingress, mailboxes, and selective receive](signal-ingress-mailboxes-and-selective-receive.md) —
  consumes generation-safe routes and lifecycle states.
- [Terms, private heaps, shared binaries, and tracing collection](terms-private-heaps-shared-binaries-and-tracing-collection.md) —
  owns private execution memory retained by actor state.
- [Failure translation and the OTP boundary](failure-translation-and-the-otp-boundary.md) —
  interprets sealed exit evidence and runtime-epoch changes.
- [Resource accounting and overload control](resource-accounting-and-overload-control.md) —
  admits and charges actor creation and cleanup.

## Sources

- [OTP 29.0.6 managed-runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
- [Making reliable distributed systems](../../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
- [A History of Erlang](../../30-sources/armstrong-2007-history-of-erlang.md)
- [Orleans virtual actors](../../30-sources/bernstein-et-al-2014-orleans.md)
- [Crash-only software](../../30-sources/candea-fox-2003-crash-only-software.md)
