---
title: "Interrupt event fabric"
kind: note
created: "2026-09-02"
maturity: developing
tags:
  - architecture-support
  - capabilities
  - event-delivery
  - fault-containment
  - interrupt-controllers
  - interrupts
aliases:
  - "Kernel interrupt-routing component"
  - "Capability-mediated interrupt events"
---

# Interrupt event fabric

The interrupt event fabric should turn controller state into a bounded,
capability-authorized notice while preserving the source's real flow
semantics. A hardware interrupt is not automatically an Erlang message, an
exact occurrence count, or proof that a device operation completed.

The recommended implementation separates controller backends, flow plans, and
typed source, route, and binding views. The hard path claims only the
controller state needed to stabilize the source, updates a preallocated
per-source sticky/counted record, applies one prevalidated kernel debit and its
already selected mask/quarantine transition, signals a bounded notification,
reports counters, performs the flow plan's immediate EOI/deactivation step if
any, and returns. Device-specific cause clearing and queue draining occur in an
unprivileged driver domain. Level, edge, fast-EOI, MSI, per-CPU, and IPI flows
remain distinct state machines behind one event vocabulary.

This note proposes an implementation for component 5 of [Kernel hardware and
architecture support
layer](../kernel-hardware-and-architecture-support-layer.md). Source literature
supports the constraints and precedents; no current experiment verifies the
complete fabric.

## Question, scope, and operational standard

The question is:

> How should the kernel control, route, account for, and revoke interrupt
> sources while letting ordinary driver and runtime services handle events
> outside privileged interrupt context?

This component owns:

- discovery and normalization of interrupt-controller capabilities;
- controller claim, mask, unmask, acknowledgement, EOI, deactivation, pending,
  priority, and routing mechanisms;
- private `ArchInterruptSourceState`, `ArchInterruptRouteState`, and
  `ArchInterruptBindingState` behind kernel-owned typed wrappers;
- flow-specific state machines;
- preallocated hard-path records and bounded notification delivery;
- affinity migration, rebinding, unbinding, and in-flight drainage;
- bounded execution of prevalidated debit, mask, and quarantine transitions,
  plus counter publication; and
- a separate kernel-owned IPI class used by scheduling, translation, code
  publication, and CPU lifecycle.

Drivers own device register protocols and clearing the device-side cause. The
minimal kernel owns privileged hard-path accounts, thresholds, refill rules,
recovery authority, and escalation policy; scheduling-control authority may
configure admitted limits through it. The protected-I/O layer grants MMIO,
DMA, queue, and reset authority. The managed runtime converts driver-service
results into language-level messages. None of that code runs directly in the
hard handler.

The first implementation is adequate only when it demonstrates:

1. Only a holder of source-control authority can bind, route, configure, mask,
   or unmask a source, and only a current binding-completion facet can complete
   deferred service.
2. Every source has a declared flow class whose controller transitions match
   its trigger and backend semantics.
3. The hard path has measured bounds for instructions/time, stack, nesting,
   locks, and memory; it never allocates, blocks on a receiver, or calls driver
   code.
4. Binding generation prevents a late interrupt, completion, or deferred
   record from acting on a replacement binding.
5. Rebinding and CPU-affinity migration stabilize delivery, drain the old
   route, publish the new generation, and only then arm the source.
6. Receiver overload has an explicit coalescing, saturation, masking, or
   quarantine result. No event is silently called lossless.
7. A faulty device or driver cannot consume unbounded uncharged privileged CPU
   time or re-enable itself after quarantine.
8. Device interrupt sources cannot invoke kernel-only IPI operations.
9. The unchanged semantic object model runs over two materially different
   controller families without pretending their identifiers or completion
   rules are identical.

## Evidence and its limits

| Evidence | Supported conclusion | What remains unproved |
| --- | --- | --- |
| [Linux generic interrupt handling](../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) | Separating generic edge, level, fast-EOI, simple, and per-CPU flow from controller-chip operations reduces duplicated and unsafe folklore | Linux's descriptor model and broad compatibility surface are not a minimal API for this kernel |
| [Arm GICv3/v4 overview](../../30-sources/arm-2019-gicv3-v4-software-overview.md) | Pending, active, active-and-pending, acknowledgement, priority drop, deactivation, trigger mode, and routing are observable controller state | The guide covers a selected configuration and does not define this capability lifecycle |
| [RISC-V AIA](../../30-sources/risc-v-international-2023-advanced-interrupt-architecture.md) and [PLIC](../../30-sources/risc-v-international-2023-platform-level-interrupt-controller.md) | Wired PLIC/APLIC paths, per-hart MSI interrupt files, privilege contexts, claim/completion, identities, and eventual state visibility cannot be reduced to one global IRQ integer | A concrete platform topology, driver protocol, or implementation correctness |
| [Intel system programming manual](../../30-sources/intel-2026-system-programming-documentation.md) | Local APIC, IPI, IOAPIC, and MSI-like mechanisms have distinct delivery and routing roles | A portable flow model or device-side correctness |
| [L4 lessons](../../30-sources/elphinstone-heiser-2013-l4-lessons.md) | Interrupts can become asynchronous notifications to user-level services while a small privileged mechanism retains controller control | This project's accounting, restart, and generation scheme |
| [seL4 reference manual](../../30-sources/sel4-foundation-2026-reference-manual.md) and [verification overview](../../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md) | Interrupt authority can be capability-mediated and delivery can use bounded notification objects | Similar objects do not transfer seL4's proofs; notification coalescing is not a general lossless queue |
| [When poll is better than interrupt](../../30-sources/yang-et-al-2012-when-poll-is-better-than-interrupt.md) | For selected very low-latency I/O, budgeted polling can outperform interrupts | Polling is not universally better and does not remove source-control or recovery obligations |
| [Time protection](../../30-sources/ge-et-al-2019-time-protection.md) | Interrupt routing and partitioning affect timing-channel isolation, not only availability | The baseline fabric does not by itself close all timing channels |

The useful synthesis is narrower than copying any one system: retain Linux's
flow/backend split, L4/seL4's notification boundary and authority mediation,
controller-specific state from current architecture specifications, and this
project's explicit generations, budgets, and failure routes.

## Recommended structure

```text
boot controller descriptors + feature profile
                 |
       controller-instance backends
                 |
        typed InterruptSource
                 |
        selected FlowPlan  <----- protected-I/O device profile
                 |
       InterruptRoute(target CPU/context)
                 |
       InterruptBinding(generation)
          /                    \
 hard-path event record      management/fault route
          |                    |
 bounded EventSink       storm/quarantine supervisor
          |
 unprivileged driver service
          |
 device registers, queues, DMA; then ordinary runtime/OTP messages
```

The flow plan is data chosen from a closed set after validating controller and
device-profile compatibility. It is not a callback supplied by the driver.

## Object and authority model

The minimal kernel allocates and accounts one `IRQBinding` aggregate. The
names `InterruptSource`, `InterruptRoute`, and `InterruptBinding` below denote
attenuated typed views over that aggregate's source-generation ledger and
source/route/binding records, not three independently allocated authority
objects. Every view shares the aggregate's resource account, lifetime group,
source incarnation, and teardown epoch. This architecture component holds
only the exclusively referenced private `ArchInterrupt*State` needed to
realize those records in a controller.

### `InterruptController`

One object represents one discovered controller instance and its immutable
profile: identifier namespace, trigger support, priority width, target model,
MSI capabilities, virtualization context, claim/EOI/deactivation behavior,
register access method, and errata. Raw registers remain backend-private.

### `InterruptSource` view

A source records:

- stable object identity, controller identity, backend-local identifier, and
  source generation;
- source class: wired, MSI, per-CPU, local error, timer, or kernel IPI;
- trigger and polarity where meaningful;
- flow-plan family and controller chain;
- immutable priority ceiling and allowed affinity set;
- current mask, pending/active summary, route, binding, and storm state; and
- a management route outside the ordinary driver's failure subtree.

An MSI identity is scoped to its controller or per-hart interrupt file. A GIC
INTID, x86 vector, RISC-V major cause, IMSIC minor identity, and PLIC source are
not interchangeable integers. The source record preserves their namespace.

### Authority facets

Separate capabilities prevent a driver from becoming its own supervisor:

| Facet | Authority |
| --- | --- |
| `SourceConfigure` | Select allowed trigger/priority/profile before binding |
| `SourceBind` | Create or replace a binding to an authorized destination |
| `SourceRoute` | Choose a target within the source and domain affinity ceilings |
| `SourceMask` | Mask for ordinary service or teardown |
| `BindingComplete` | Complete one current delivered generation and request re-arm when the flow allows |
| `SourceInspect` | Read counters, generations, pending state, and fault evidence |
| `SourceRecover` | Ask the minimal kernel to validate recovery policy and produce a bounded re-enable transition after management preconditions |
| `SourceDestroy` | Permanently close the enclosing `IRQBinding` aggregate where the platform permits |

The ordinary driver typically receives `BindingComplete` and inspect rights,
not `SourceRecover` or an unconstrained route facet. A reset-domain manager may
hold a kernel-minted recovery facet; the minimal kernel still validates the
current authority and policy before admitting a re-enable transition.

### `InterruptRoute` view

A route binds controller delivery to a logical CPU and privilege/event context,
not merely a hardware number. It carries a CPU-lifecycle generation and, for
MSI, the protected-I/O/IOMMU interrupt-remapping generation where available.
CPU removal or device reassignment closes the route before either identifier
can be reused.

### `InterruptBinding` view

A binding contains:

```text
(source identity and generation,
 destination EventSink identity and generation,
 flow plan,
 delivery semantics,
 route generation,
 hard-path account identity and debit-plan generation,
 completion authority generation,
 teardown epoch)
```

Its state and event record are preallocated before the source can be armed.
Binding memory remains pinned while the hard path or deferred work can
reference it.

## Event semantics

The fabric delivers a *notice to inspect and service a source*, not an
unqualified occurrence.

### Delivery classes

| Class | Meaning | Suitable sources |
| --- | --- | --- |
| `ConditionSticky` | At least one service condition was observed; repeated assertions may coalesce until the driver drains the device | Level-triggered lines, queue-not-empty conditions |
| `ObservedCount` | The hard path observed `n` claims/messages since the last drain, up to saturation; hardware or device may already have coalesced earlier events | Edge, MSI, or message identities where each controller observation is useful |
| `BitsetSticky` | One or more source bits are pending in a bounded shared sink | Low-rate notifications and seL4-like event aggregation |
| `KernelRequest` | A generation-tagged, kernel-owned cross-CPU operation with its own completion slot | TLB shootdown, reschedule, code publication, CPU stop |

`ObservedCount` is never described as the number of device operations unless
the device specification proves that equivalence. Saturation sets an overflow
flag. The driver then drains authoritative device queues or status registers.

### Event record

A preallocated record can contain:

```text
InterruptNotice {
  source_id,
  source_generation,
  binding_generation,
  route_generation,
  observed_sequence,
  saturated_count,
  flags: sticky | overflow | masked | quarantined | spurious,
  optional_raw_timestamp
}
```

The `EventSink` notification may coalesce wakeups. The monotonically advancing
sequence lets the driver detect work since its last snapshot; wrap is handled
by modular-distance rules with a bound on outstanding observations. Detailed
device completions live in shared queues governed by the DMA protocol, not in
the interrupt record.

## Source lifecycle

```text
DiscoveredMasked
  -> ConfiguredMasked(source_generation)
  -> BoundMasked(binding_generation)
  -> RoutePublished(route_generation)
  -> Armed
  -> Claimed(flow_token)
  -> NoticePublished(observed_sequence)
  -> AwaitingDriverCompletion      [only for deferred-completion flows]
  -> ControllerCompleted
  -> Armed

Any live binding state -> ClosingBinding(new binding generation)
ClosingBinding -> DrainingBinding(old route and hard-path references)
DrainingBinding -> BoundMasked | DiscoveredMasked
DiscoveredMasked -> DestroyingSource(new source generation) -> Dead

Any live state -> StormMasked -> Quarantined
Quarantined -> BoundMasked only through SourceRecover
```

Controller hardware may contain its own pending/active substates. The common
state does not pretend to replace them; the flow token records the backend
state that must be completed.

## Flow-specific protocols

### Wired level condition

1. The controller indicates a pending source and the hard path claims it.
2. The flow plan masks or otherwise prevents uncontrolled redelivery while
   preserving the asserted condition.
3. The hard path publishes `ConditionSticky`, performs any immediate priority
   drop required by the backend, and returns.
4. The unprivileged driver reads device status, drains or repairs the cause,
   and makes the device deassert its line.
5. The driver presents the current `BindingComplete` token.
6. The fabric validates generations, performs deferred controller
   completion/deactivation, checks pending state as the profile requires, and
   re-arms. A still-asserted condition produces another notice.

The device deassertion in step 4 and controller completion in step 6 are
different operations. Swapping their order blindly can create a storm or lose
work.

### Edge source

The hard path claims/acknowledges the latched edge according to the controller,
increments `ObservedCount`, and normally performs EOI promptly. If another edge
arrives while service is pending, the controller or hard-path counter may
coalesce it. When the backend cannot preserve edges while masked, the flow plan
uses its documented pending/retrigger mechanism or rejects deferred masking.

The driver drains its device queue to determine real work. It does not assume
one notice equals one packet or completion.

### MSI or MSI-X source

An MSI is a configured device memory write into an interrupt-controller path.
The hard path claims the resulting identity and updates an observed counter.
Routing or rebinding may require coordinated changes to device MSI address/data,
interrupt remapping/IOMMU state, controller state, and target CPU. Those
changes form one protected-I/O transaction; the fabric alone cannot safely
rewrite a live device's message.

Per-vector masking is used when the device and controller support it. Otherwise
the enclosing device profile declares the larger queue, function, or reset
boundary required to stop messages.

### Fast-EOI and controller-completed sources

Some controllers require only an EOI after capturing the event; some claim
operations clear pending state immediately. A closed flow plan can complete in
the hard path and use the driver's later action only to drain device work. The
binding still has generation, overflow, and storm semantics.

### Per-CPU local source

Per-CPU sources avoid a global route lock but are bound to a CPU-lifecycle
generation. Their state is migrated, disabled, or reconstructed before that
CPU goes offline. Local timer and fatal architecture events may use specialized
facades rather than ordinary driver bindings.

### Kernel IPI

IPIs use dedicated vectors/identities, CPU-local preallocated mailboxes, and a
closed request enum. Device source capabilities cannot name this class. Each
request carries subsystem generation and completion storage. The hard path
performs only bounded actions such as local TLB invalidation, code-fetch
synchronization, reschedule marking, or CPU-stop entry.

General user events never share the IPI dispatch table, even if the same
physical controller delivers both.

### NMI-like and fatal events

Non-maskable and machine-fault paths are not ordinary bindable sources. They
enter the architecture-fault component through preallocated crash state and a
more restrictive nesting contract. Treating them as driver notifications would
let ordinary backpressure block machine survival evidence.

## Hard-path algorithm

The baseline hard handler is generated or selected from a closed flow-plan
table:

1. Enter through the normalized interrupt frame and CPU-local interrupt stack.
2. Claim/read the backend identity and validate it against the immutable
   controller table.
3. Acquire the current binding reference with IRQ-safe acquire semantics; if
   absent or stale, execute the source's safe spurious/unbound flow.
4. Apply the flow plan's bounded stabilize operation: claim, mask/ack, priority
   drop, or equivalent.
5. Update the CPU-local or source-local event sequence, saturating count, and
   sticky flags without an unbounded remote lock.
6. Atomically apply the current kernel-validated debit plan to its referenced
   hard-path account, execute only the plan's bounded keep-armed, mask, or
   quarantine result, and publish the resulting counters.
7. Signal the bounded `EventSink`; a full or already-signalled sink merely
   preserves sticky state.
8. Perform the flow plan's immediate EOI/deactivation step, if any.
9. Release the binding reference and return through normalized exit.

The path contains no allocator, pageable memory, ordinary endpoint send,
driver callback, capability-tree traversal, log formatting, or unbounded retry.
The first profile disables ordinary IRQ nesting while inside this path;
NMI-like events remain separately bounded. Later priority nesting requires an
explicit stack and lock analysis.

## Binding, migration, and teardown

### Initial binding

1. Validate source, destination, route, flow, priority, and authority.
2. Allocate and initialize the binding, event record, quota, completion facet,
   and management route while the source remains masked.
3. Clear or classify inherited pending state according to the device profile;
   never discard a level condition merely to make the controller look idle.
4. Program the route and confirm its backend-defined visibility.
5. Publish the binding generation with release ordering.
6. Arm/unmask the source.

### Affinity migration

1. Close new delivery on the old binding generation and mask/stabilize the
   source.
2. Wait for hard-path references and deferred flow tokens on the old CPU set.
3. For MSI, coordinate device message and interrupt-remapping changes with the
   protected-I/O layer.
4. Program the new controller route and target CPU context.
5. Increment route and binding generations, publish the new target, and make
   the target CPU observe the generation before eligibility.
6. Re-arm only after the source/device profile says pending state is safe.

If a controller cannot move a live active source, the transaction waits for
driver completion or escalates to device reset/quarantine. CPU hot-unplug must
complete this migration for every routed source before declaring the CPU
offline.

### Unbind and driver death

Unbind first advances the binding generation, or a dedicated delivery-admission
epoch, so no new event can acquire the old binding. It masks or stabilizes the
source, drains all CPU-local references, resolves or quarantines outstanding
flow tokens, disconnects the sink, and only then frees binding memory. The
source generation is its incarnation and advances only when that source record
is retired and recreated inside the aggregate. A late `BindingComplete` can finish an old
teardown record but cannot unmask a replacement.

The management route and its scheduling reserve are outside the failed driver
domain. Driver death therefore produces an inspectable masked or quarantined
source rather than an interrupt with nowhere safe to go. Destruction of the
accounted `IRQBinding` aggregate closes new delivery, masks or stabilizes the
source, drains controller and CPU-local hard-path references, deferred records,
and completion facets, then releases its `EventSink`, CPU-route,
device/remapping, management-route, and private controller-state dependencies.
No source, route, or binding view is reclaimed independently.

## Backpressure and storm containment

Every source has both a delivery-capacity policy and a kernel-owned privileged
hard-path account. Those are minimal-kernel policy state, not architecture
fabric authority.

### Receiver backpressure

The hard path never waits for a receiver. Depending on the declared class it:

- leaves `ConditionSticky` set;
- increments a saturating observed count;
- sets `overflow` when precision is exhausted;
- keeps a level source masked pending driver completion; or
- automatically masks a maskable high-rate source.

The driver drains device state and then atomically reads/clears the notice up
to an observed sequence. A new event racing with the clear remains visible by
sequence or sticky state.

### Storm policy

The minimal kernel owns the per-source token bucket or fixed window, threshold,
refill schedule, and escalation policy. Admission installs a generation-tagged
`HardPathDebitPlan` containing only the account reference, finite debit, and
one closed-set action for each result. The architecture hard path may apply
that plan and report counters; it cannot change a threshold, refill an account,
or choose a recovery outcome. When the admitted plan reports its limit:

1. a maskable source enters `StormMasked`;
2. a sticky `InterruptStorm` record captures counts, time window, source and
   binding generations, CPU, and last controller state;
3. the separate management route is signalled using reserved capacity; and
4. only the minimal kernel can validate `SourceRecover`, refill or replace the
   account generation, and issue a bounded re-arm transition after driver
   drain, device reset, or another profile-specific precondition; the fabric
   executes that transition but does not approve it.

An unmaskable source declares a larger escalation boundary: device function,
reset domain, CPU, or machine. The minimal kernel still accounts and selects
the escalation while this component captures counters and executes the
available controller transition; neither layer claims isolation the hardware
cannot provide.

The source's hard-path cost is charged even when the destination is already
signalled. Otherwise a malicious device could consume kernel CPU outside every
scheduling context.

## Polling as an optional service mode

Polling is a driver policy, not a replacement for the fabric. For a suitable
queue, a manager asks the minimal kernel to create a funded, capability-backed
`PollingLease`. The event fabric performs only the interrupt-side transition:

```text
ArmedInterrupt
  -> MaskAndDrain(old binding generation)
  -> InterruptPollingTransition(masked binding generation)
  -> [kernel-owned PollingLease(driver domain, queue, budget, deadline)]
  -> ReturnAndReconcile
  -> ArmedInterrupt(new binding generation)
```

The polling thread and lease are owned by the minimal kernel/driver domain and
consume that domain's scheduling budget; they are not architecture objects.
The source remains typed, masked, inspectable, and recoverable. Lease expiry or
driver death returns control to the manager. The device profile defines how
completions that race the mode switch are reconciled.

This lets measured low-latency queues use polling without making all devices
spin, executing polling in the kernel, or losing the ability to recover a
failed driver.

## Cross-controller realization

| Concern | x86-64 APIC/MSI family | Arm GICv3/v4 family | RISC-V PLIC/AIA family | Common contract |
| --- | --- | --- | --- | --- |
| Identity | CPU vector plus IOAPIC/MSI source and remapping context | INTID class: SGI, PPI, SPI, LPI, plus security/virtualization context | Major cause plus PLIC/APLIC source or per-hart IMSIC minor identity | Typed source identity scoped to controller/context |
| Claim | Vector entry and controller/device-specific pending state | Interrupt acknowledge selects pending INTID and makes it active | PLIC claim/complete or IMSIC top-pending claim; APLIC path may feed IMSI | Flow-token creation, not a universal register operation |
| Trigger | IOAPIC wired edge/level; MSI is a message write | Wired edge/level; SGI and LPI/message classes differ | PLIC/APLIC wired source modes; IMSIC records MSI pending bits | Closed flow-plan family with feature data |
| Completion | Local APIC EOI plus IOAPIC/device behavior as configured | Priority drop and deactivation may be combined or split | PLIC completion differs from IMSIC pending-bit claim and APLIC delivery | Named immediate or deferred controller-completion plan |
| Routing | APIC destination/vector, MSI address/data, optional interrupt remapping | Affinity routing, redistributors, ITS for LPIs | PLIC contexts or APLIC/IMSIC hart and privilege interrupt file | Generational `InterruptRoute` composed with CPU/device lifecycle |
| Capacity/priority | Feature and controller dependent | Implementation priority bits, INTID ranges, 1-of-N options | Implemented sources, identities, thresholds, and contexts vary | Discovered immutable profile; no guessed constants |

The backend exposes feature limits and flow-plan implementations. Portable code
never writes a raw EOI register or assumes that claim clears pending state.

## Interaction with the capability microkernel

The [minimal privileged kernel](../minimal-privileged-kernel-layer.md) already
requires typed IRQ bindings, bounded notifications, hard-path accounting, a
separate management fault route, generation-safe teardown, and quarantine.
This component realizes the controller side of that design.

The division is:

- the capability kernel owns and accounts the single `IRQBinding` aggregate,
  exposes `InterruptSource`, `InterruptRoute`, and `InterruptBinding` as typed
  views over its records, creates their completion and recovery facets, and
  controls dependency-ordered destruction;
- the capability kernel also owns every hard-path account, threshold, refill
  rule, recovery authorization, and escalation policy, and admits only bounded
  generation-tagged debit or recovery transitions to this component;
- this architecture component owns the exclusively referenced
  `ArchInterrupt*State` records, applies admitted debit/mask/quarantine or
  re-arm transitions, executes controller mechanisms, advances their
  generations, and publishes counters and hard-path records;
- the scheduling component supplies ordinary driver and management execution
  budgets, which remain distinct from the kernel's interrupt hard-path account;
- the protected-I/O component composes MSI routing, MMIO, DMA, queue, and reset
  leases; and
- domain teardown waits for binding drainage before reclaiming either source
  state or destination memory.

An interrupt notification is a bounded wakeup mechanism, not kernel IPC with
an arbitrary payload. Detailed data stays in driver-owned queues protected by
the relevant mapping and DMA leases.

## Interaction with OTP and BEAM

The fabric preserves OTP-like principles without pretending hardware is BEAM:

- privileged entry does bounded work and isolates failure-prone driver logic;
- an unprivileged driver service can be supervised and restarted;
- source, binding, and driver incarnations prevent messages from an old driver
  being attributed to its replacement;
- overflow and quarantine become explicit failure signals; and
- management authority remains outside the failed subtree.

The driver or I/O service converts a kernel notice and drained device records
into ordinary application or BEAM messages. It may use a mailbox, selective
receive, correlation identifiers, and OTP supervision at that layer. The hard
handler does not allocate BEAM terms, enter an ERTS scheduler, inspect a
mailbox, or depend on process-local tracing GC.

A BEAM PID is routing identity, not interrupt authority. A runtime broker may
hold an attenuated event endpoint on behalf of an actor, but the kernel binding
belongs to the runtime or driver protection domain and its capability space.

## Safety and security analysis

### Stale completion and rebind

`BindingComplete` names source, binding, route, and delivery generations plus
the flow token. If any differ, completion can close only the historical
teardown record; it cannot EOI, deactivate, or unmask current state.

### Shared wired lines

When hardware shares one line among devices, the source view represents that
larger fault and service boundary. A privileged or isolated demultiplexing
service probes authorized devices and produces secondary events. The kernel
does not mint falsely independent source capabilities that cannot be masked or
acknowledged independently.

### MSI forgery and remapping

A device capable of arbitrary MSI writes can target interrupt-controller
addresses. Where an IOMMU/interrupt-remapping unit exists, the protected-I/O
profile constrains requester, address, data, target, and vector. Without it,
the system honestly records a larger trust boundary and may withhold direct
device assignment.

### Priority abuse

Drivers cannot select arbitrary hardware priority. Source configuration fixes
a ceiling, and the kernel reserves higher classes for fatal events, clock/CPU
coordination, and bounded recovery. Priority does not replace scheduling
budget: deferred driver service is charged normally.

### Spurious and unbound interrupts

Unknown or stale identities follow a controller-specific safe flow, increment
an inspectable spurious counter, and remain bounded. Repetition triggers mask
or controller-level quarantine when possible. Logging is deferred; the hard
path never formats diagnostic text.

### Receiver compromise

A malicious receiver can ignore notices or present bad completion tokens. Its
source stays masked, accumulates sticky evidence, or reaches a bounded storm
state. It cannot write controller registers, select an IPI vector, route to a
different domain, or re-enable after its completion authority is revoked.

### Timing channels

Affinity and priority isolation reduce interference but do not prove timing
noninterference. Shared controller queues, CPU entry paths, caches, and
interconnect remain possible channels. A time-protection profile may dedicate
sources/CPUs, partition priorities, and pad transitions at a utilization cost.

## Verification strategy

### Executable state machines

Model source, binding, route, CPU lifecycle, and controller flow as a product
state. Check that:

- only an `Armed` current generation can deliver to its current sink;
- each claim has at most one valid controller-completion path;
- a stale token never unmasks or completes a later binding;
- binding memory is not reclaimed while a CPU-local reference exists;
- CPU offline cannot finish while a live route still targets it;
- overflow is always visible or causes mask/quarantine; and
- every post-claim failure reaches completed, masked, or quarantined state.

Instantiate separate models for level, edge, fast-EOI, PLIC-like
claim/complete, GIC split-deactivate, and MSI paths. A single abstract handler
would hide the very differences under test.

### Model controller backend

Build a deterministic software controller that can:

- assert and deassert level sources at any step;
- inject multiple edges while masked or active;
- delay route visibility, EOI, deactivation, and MSI arrival;
- coalesce or drop events only according to its declared profile;
- return spurious or out-of-range identities;
- race CPU offline and affinity migration; and
- fail mask, route, or completion operations.

Run the portable fabric unchanged against this backend before hardware.

### Hardware and emulator tests

- Verify every supported trigger/flow combination on the concrete controller.
- Inject an interrupt at every binding and migration transition.
- Kill and restart the driver while the source is pending, active, and
  active-and-pending.
- Saturate the event sink and hard-path budget.
- Reuse source/vector numbers and deliver delayed old events.
- Exercise MSI remapping and device reset races.
- Offline a target CPU under load.
- Compare emulator and hardware behavior; controller timing and pending-state
  details may be simplified in emulators.

### Performance and boundedness

Measure distributions for:

- exception entry to hard-path record publication;
- hard-path cycles and stack by flow plan;
- notice-to-driver wake latency under idle and loaded schedulers;
- level-source completion and re-arm;
- edge/MSI rate until coalescing, saturation, and storm masking;
- affinity migration and unbind drainage;
- IPI request and acknowledgement for TLB, code publication, and CPU stop;
- interrupt versus polling crossover for representative queues; and
- interference with BEAM actor latency, runtime scheduling, and process-local
  garbage collection.

Publish maximum observed nesting and lock hold times with the machine profile.
Average interrupt latency alone is not a responsiveness or containment result.

## Staged implementation

### Stage 1: one controller, masked lifecycle

- Discover one controller instance and create typed sources.
- Implement mask, unmask, one safe priority, one target CPU, spurious handling,
  and source inspection while all drivers remain synthetic.

### Stage 2: bounded event delivery

- Add preallocated bindings, `ConditionSticky`, saturating observed counts,
  notification sinks, generation validation, and application of a
  kernel-provided debit plan with counter reporting.
- Implement one level and one edge/MSI flow with a model device.

### Stage 3: restart and storm containment

- Add binding completion facets, driver-death unbind, management routes,
  kernel-owned storm accounts and refill/recovery authority, architecture-side
  mask/quarantine transitions, and reserved recovery capacity.
- Exit when a failed driver cannot retain unmask or route authority.

### Stage 4: multicore routes and IPIs

- Add affinity migration, CPU-lifecycle generations, kernel-only IPI
  mailboxes, and route drainage.
- Integrate translation shootdown and code-publication requests.

### Stage 5: second controller family and protected MSI

- Port the unchanged object and event contract to a materially different
  controller family.
- Compose device MSI programming with IOMMU/interrupt-remapping and reset
  profiles.

### Stage 6: supervised drivers and optional polling

- Run real drivers in unprivileged domains, restart them under injected faults,
  and translate notices into ordinary runtime events.
- Add polling leases only for queues whose measurements justify them.

## Alternatives and tradeoffs

### Run driver handlers in hard interrupt context

This minimizes one wakeup but imports driver bugs, unbounded loops, allocation,
and device policy into privilege. It also frustrates restart and accounting.
The baseline pays a bounded notification cost to preserve containment.

### One universal `ack/handler/eoi` sequence

The sequence is simple and wrong for meaningful combinations of level, edge,
fast-EOI, split deactivation, PLIC claim/complete, and MSI behavior. Closed
flow-plan families retain clarity without exposing controller registers to
every driver.

### Queue every interrupt losslessly

Many controllers already coalesce conditions or bound pending bits, and an
unbounded kernel queue is a denial-of-service mechanism. Sticky state plus a
saturating observed count and authoritative device queues is honest and
bounded. A device that provides a lossless completion ring should use that
ring under the DMA protocol.

### Coalesced bit only

A single bit is very cheap and matches level conditions, but hides how often
the hard path ran and weakens storm diagnosis. The recommended record keeps a
saturating observed sequence even when wakeups coalesce.

### Per-interrupt kernel threads

Kernel threads can provide blocking contexts and priority control but enlarge
kernel objects and scheduling policy. Unprivileged driver threads already
provide those properties under capability and scheduling budgets. A small
kernel deferred-work executor is reserved for architecture-owned completion,
not arbitrary device handlers.

### Direct user-level interrupt delivery

Hardware virtualization can inject interrupts directly and reduce latency.
It also complicates revocation, storm accounting, CPU migration, and recovery.
A later delegated profile may bind a virtual interrupt context directly to a
driver domain while retaining a kernel control plane and reset path. The
mediated fabric is the correctness baseline.

### Poll everything

Polling avoids entry overhead at high rate but consumes CPU during idle
periods, obscures work attribution if run in privilege, and can harm unrelated
actor responsiveness. Capability-controlled, budgeted polling leases preserve
it as a measured per-queue option.

### Dynamic hardware priority from driver requests

Fine priority tuning can reduce latency but gives a compromised driver a
machine-wide interference control. The baseline uses profile-fixed ceilings
and scheduler budgets. A trusted system manager may change priority only
through a masked reconfiguration lifecycle.

## Unresolved questions

- Which first two controller families best falsify the flow-plan abstraction:
  x86 APIC/MSI plus Arm GIC, or Arm GIC plus RISC-V PLIC/AIA?
- Is a per-source record or per-CPU record the better cache and teardown tradeoff
  for expected core and source counts?
- What exact modular bound makes an observed sequence safe across saturation
  and delayed drivers?
- Which flows can perform controller completion in the hard path, and which
  must retain a completion token until the device condition is cleared?
- How should a shared wired line be represented when probing one failed device
  can block unrelated devices on the line?
- What interrupt-rate budget and window protect actor responsiveness without
  masking legitimate bursts?
- Which controllers and IOMMUs can constrain MSI address/data strongly enough
  for direct driver assignment?
- Can high-priority nested interrupts be supported without unbounded stack or
  lock interactions, and is the latency gain necessary for the first target?
- Which runtime event modes—sticky condition, observed count, or a device
  completion ring—are needed by initial OTP-style services?
- At what measured device latency and load should the system switch between
  interrupts, coalescing, and a polling lease?
- What controller state can be preserved across driver restart, and which
  profiles require a device or reset-domain reset?

## Connections

- [Kernel hardware and architecture support
  layer](../kernel-hardware-and-architecture-support-layer.md) defines the
  component boundary and its dependencies on entry, CPU lifecycle, time, and
  protected I/O.
- [Address translation and protection
  transitions](address-translation-and-protection-transitions.md) uses the
  kernel-only IPI class for remote invalidation and supplies route-memory
  lifetime guarantees.
- [Ordering, coherence, and code
  publication](ordering-coherence-and-code-publication.md) supplies IRQ-safe
  atomic publication, typed MMIO ordering, and remote code-sync requests.
- [Minimal privileged kernel layer](../minimal-privileged-kernel-layer.md)
  supplies IRQ capabilities, bounded notifications, scheduling charges,
  reset authority, teardown generations, and quarantine.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../beam-erts-and-otp-principles-for-a-new-operating-system.md) explains
  how supervised services and ordinary actor messages remain above this
  bounded hardware-notice boundary.
- [Kernel hardware-contract
  inquiry](../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  retains the experiments needed before this proposed fabric can be treated as
  adequate.

## Sources

- [Linux kernel low-level core APIs](../../30-sources/linux-kernel-community-2026-low-level-core-apis.md)
- [Arm CoreLink GICv3 and GICv4 software overview](../../30-sources/arm-2019-gicv3-v4-software-overview.md)
- [RISC-V advanced interrupt architecture](../../30-sources/risc-v-international-2023-advanced-interrupt-architecture.md)
- [RISC-V platform-level interrupt controller](../../30-sources/risc-v-international-2023-platform-level-interrupt-controller.md)
- [Arm A-profile system architecture documentation](../../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [Intel 64 and IA-32 system programming documentation](../../30-sources/intel-2026-system-programming-documentation.md)
- [RISC-V privileged architecture](../../30-sources/risc-v-international-2026-privileged-architecture.md)
- [From L3 to seL4](../../30-sources/elphinstone-heiser-2013-l4-lessons.md)
- [seL4 reference manual](../../30-sources/sel4-foundation-2026-reference-manual.md)
- [Comprehensive formal verification of an OS microkernel](../../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
- [When poll is better than interrupt](../../30-sources/yang-et-al-2012-when-poll-is-better-than-interrupt.md)
- [Time protection](../../30-sources/ge-et-al-2019-time-protection.md)
