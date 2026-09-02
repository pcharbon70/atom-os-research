---
title: "Minimal privileged kernel layer"
kind: note
created: "2026-08-31"
maturity: developing
tags:
  - capabilities
  - fault-containment
  - ipc
  - microkernels
  - operating-systems
  - scheduling
aliases:
  - "Capability microkernel layer"
  - "Minimal kernel contract"
---

# Minimal privileged kernel layer

The minimal privileged kernel should be a **capability microkernel**: a small
reference monitor that turns the lower architecture-support mechanisms into
protected domains, explicit authority, bounded communication, enforceable
resource budgets, structured fault delivery, and safe revocation. It should
make failure containment and recovery *possible and auditable* without placing
BEAM actors, mailboxes, garbage collection, service naming, device policy, or
OTP supervision policy in privileged code.

The proposed design has eleven cooperating components:

1. bootstrap and root-authority handoff;
2. typed kernel-object storage and explicit memory accounting;
3. capability spaces, derivation, transfer, and revocation;
4. protection domains, threads, and address-space attachment;
5. bounded invocation, notification, and shared-memory transport;
6. scheduling contexts, budgets, and timeout delivery;
7. memory mappings and architecture-resource bindings;
8. fault capture and containment;
9. failure boundaries and recovery control;
10. split-phase teardown, quiescence, and reclamation; and
11. bounded observability and crash evidence.

This is an architecture proposal derived from literature, not an implemented
kernel or a transferred correctness claim. The cited systems demonstrate
individual mechanisms and trade-offs. They do not establish that this exact
composition is correct, performant, or BEAM-compatible. Executable models,
fault-injection experiments, benchmarks, and eventually proofs are still
required.

## Question and operational standard

The question is:

> What is the smallest privileged contract that can safely host mutually
> distrustful BEAM runtimes and native services while giving unprivileged
> supervisors enough authority and evidence to contain, revoke, replace, and
> reconcile failed components?

“Minimal” is not a line-count target. Following Liedtke's functional
minimality argument, a mechanism belongs in the kernel when leaving it outside
would prevent the kernel from enforcing a required property across mutually
distrustful components. Performance alone does not qualify a mechanism for
privilege. A satisfactory contract must meet all of these tests:

- every privileged operation is reached through an unforgeable, typed,
  rights-limited authority;
- every kernel product preserves the revocation lineage of inputs that supply
  its future-effect authority unless an explicit, consented durable creation
  operation authorizes detachment;
- a domain cannot manufacture authority, escape its address space, consume
  uncharged kernel objects, or run after exhausting its CPU budget;
- a supervisor can retain recovery resources that the supervised domain
  cannot consume or revoke, and takeover can obtain attenuated authority from
  independent escrow without consulting the failed supervisor's table;
- synchronous call, cancellation, peer death, timeout, and reply races have a
  linearizable outcome and return donated resources exactly once; caller-
  funded passive acceptance is finite, preauthorized for its failure scope,
  and never dispatches without a positive handler budget;
- domain closing starts from fixed admission gates and bounded preallocated
  per-CPU stop state before any potentially large cleanup traversal;
- after logical closure is published, acquisitions and invocations whose
  authorization would linearize later are rejected; operations admitted before
  closure remain tracked until CPU, MMU, IRQ, and DMA effects are quiescent or
  quarantined;
- failure records distinguish a proven fault or completed termination from a
  liveness suspicion;
- exceptional paths are bounded and require no ambient allocation;
- stale kernel identifiers and replies cannot mutate a replacement domain's
  objects; user-space service epochs and external-effect reconciliation remain
  separate;
- quarantine globally closes frame mutation authority, and release cannot
  resurrect an old facet or mapping after the backing is retyped;
- the kernel reports whether an invocation was rejected before acceptance,
  received a reply, or lost its reply after acceptance; service protocols keep
  any externally visible effect explicit rather than inventing exactly-once
  behavior;
- the contract composes with the lower hardware and architecture layer on at
  least two materially different ISAs; and
- compiled BEAM code retains BEAM-compatible process isolation, scheduling,
  signalling, and process-local tracing garbage collection in an unprivileged
  managed runtime.

## Exact boundary

The previous [kernel hardware and architecture support
layer](kernel-hardware-and-architecture-support-layer.md) is the lower
semantic mechanism boundary. It performs privileged entry and return, context
sanitization, translation changes, TLB and cache completion, interrupt-source
control, raw counter and deadline access, CPU lifecycle operations, protected
I/O and DMA transitions, and architecture-fault normalization. The minimal
kernel does not duplicate those mechanisms. It decides **who may compose and
invoke them**, accounts for their use, and exposes portable kernel objects.

| Below: architecture support | Inside: minimal privileged kernel | Above: unprivileged system |
| --- | --- | --- |
| Trap entry, validated return, register ownership | System-call dispatch and complete mediation | Runtime and service APIs |
| Page-table primitives, TLB completion, cache/code publication | Address-space and mapping objects, mapping authority | Pagers, allocators, loaders, JIT policy |
| Raw counter, one-shot deadline | Scheduling contexts, budgets, timeout faults | Scheduler and admission policy; BEAM reductions |
| Interrupt mask/acknowledge/EOI and typed events | IRQ bindings and authorized notification | Device protocol and driver policy |
| CPU startup, IPI, freeze, remote quiescence | Domain/thread lifecycle and cross-core stop protocol | Placement and load balancing |
| IOMMU mapping, DMA stop/reset/quarantine | Device/DMA authority, ownership, teardown ledger | Drivers, queues, recovery policy |
| Normalized architecture faults and crash-safe capture | Domain fault state and bounded fault records | Diagnostics, supervision, restart decisions |

The privileged layer should contain only the mechanisms needed to enforce
isolation, authority, bounded resource use, and architectural completion. It
should not contain:

- BEAM processes, PIDs, mailboxes, signals, selective receive, reductions,
  heaps, tracing collection, code loading, or safe points;
- OTP supervisors, restart intensity, one-for-one or rest-for-one policy,
  application trees, or service naming;
- filesystems, storage policy, network stacks, protocol parsers, or ordinary
  device drivers;
- an unbounded message broker, event log, general allocator, object name
  service, or distributed capability protocol; or
- a transparent recovery mechanism that silently substitutes a new service
  incarnation for a failed one.

Those exclusions are safety properties as well as size choices. A parser,
driver, or restart policy in the kernel enlarges the system-wide failure
boundary. A BEAM mailbox in the kernel would also conflate cheap language
processes with expensive hardware protection domains.

## Why a capability microkernel

The literature does not identify one universally best kernel organization.
It does expose the trade-offs relevant to this platform.

| Organization | Strengths for this project | Main liabilities | Decision |
| --- | --- | --- | --- |
| Monolithic or hybrid kernel | Cheap internal calls; mature precedent; flexible shared services | Drivers, protocol stacks, allocators, and policy join the system-wide trust and failure boundary; authority is often implicit | Reject as the default privileged boundary |
| Classic microkernel with identity plus ACL checks | Moves services out of privilege; familiar process identity | Ambient names and global identities make delegation, attenuation, confused-deputy resistance, and selective revocation harder | Use domains, not identity-based ambient authority |
| Capability microkernel | Authority is explicit, delegable, attenuable, inspectable, and object-specific; naturally supports least privilege | Capability derivation, revocation, slot management, and usability require careful semantics | **Adopt as the baseline** |
| Static separation kernel | Strong configuration-time partitions and a small certified core | Rigid for dynamic service creation, supervised replacement, and changing authority graphs | Offer later as a restricted deployment profile |
| Exokernel | Cleanly separates protection from resource policy and makes secure binding/revocation central | Exposing raw hardware contracts can duplicate complexity and weaken portability | Reuse protection and revocation principles, not a raw-hardware ABI |
| Language-safe single address space | Cheap calls and strong protection against many memory errors | Unsafe native code, semantic faults, denial of service, DMA, compiler/runtime compromise, and recovery still cross the boundary | Useful within one runtime domain, not the kernel boundary |
| Hypervisor-first organization | Reuses guest operating systems and supplies coarse VM containment | VM granularity, duplicated kernels, large memory cost, and device virtualization are poor defaults for many small services | Possible compatibility layer, not the base design |

[Saltzer and Schroeder](../30-sources/saltzer-schroeder-1975-protection-information.md)
provide the enduring reference-monitor tests: economy of mechanism, fail-safe
defaults, complete mediation, least privilege, separation of privilege, and
least common mechanism. [Liedtke](../30-sources/liedtke-1995-microkernel-construction.md)
argues that address spaces, threads, and protected communication are the
essential microkernel mechanisms and shows that privilege crossings need not
be inherently slow. [L4 and seL4 experience](../30-sources/elphinstone-heiser-2013-l4-lessons.md)
adds explicit capabilities, user-level policy, bounded kernel paths, and a
small architecture-dependent implementation surface. The [seL4 reference
manual](../30-sources/sel4-foundation-2026-reference-manual.md) supplies a
current, concrete object model against which the proposal can be checked.

The proposal deliberately differs from simply cloning seL4. It adds a
first-class protection-domain lifecycle anchor, generation-aware cancellation,
and a split-phase reaping contract because supervised replacement is a central
platform requirement. These are proposed changes, not criticisms proven by
comparative evaluation.

## Design principles

### Privilege is for enforcement, not policy

The [Exokernel](../30-sources/engler-et-al-1995-exokernel.md) distinction between
protection and management remains useful. The kernel enforces that only an
authorized holder can map a frame, consume CPU time, invoke an endpoint, bind
an IRQ, or initiate teardown. User-space policy chooses which domain receives
those resources, when a failed service is replaced, and how state is rebuilt.

### Authority, identity, ownership, budget, and liveness are different

A capability answers “may this caller attempt this operation on this object?”
It does not by itself answer:

- who conceptually owns or must clean up the object;
- which principal or BEAM process initiated the request;
- which memory and CPU account pays for it;
- whether an asynchronous hardware effect has completed;
- whether the target is alive or merely suspected to have failed; or
- whether an external side effect occurred before a crash.

Keeping these dimensions separate prevents a single integer, task identity, or
“owner” field from silently acquiring several incompatible meanings.

### Every effect has a lifecycle

Removing a capability prevents future authorized invocations. It cannot undo a
packet already transmitted, a flash write already issued, a DMA transaction in
flight, or information already disclosed. Revocation therefore has two
results:

1. **logical invalidation**: once closure is published, no later capability
   lookup or invocation may acquire authority through the closed lineage or
   facet; already admitted operations remain explicit; and
2. **physical quiescence**: all previously admitted CPU, translation, IRQ, and
   device effects have either completed, been cancelled, or been quarantined.

Only the second result permits safe resource reuse.

### Kernel work is bounded, attributable, and interruptible

No system call may recursively walk an unbounded graph, allocate from an
ambient heap, or retain an unbounded kernel stack across a call chain.
Potentially large revocations and teardowns proceed in charged slices and
return progress objects. Queues have declared capacities and overflow
behavior. Exceptional paths use preallocated state.

### Object identity, domain identity, and service epoch are separate

Restart does not resurrect the old execution context, but three different
identities must not be compressed into one “generation”:

- a **kernel-object identity** is `(object_slot, object_generation)`; the
  generation advances only when storage is safely reused for another kernel
  object;
- a **domain identity** is the kernel-object identity of one particular
  `ProtectionDomain`; a replacement is a new domain object `D'`, with no
  required numeric relationship to the failed domain `D`; and
- a **logical-service epoch** is maintained by an unprivileged registry and
  advances when that service publishes a replacement endpoint.

Endpoint sessions, capability slots, reply tokens, mappings, and device
bindings have their own kernel generations. Old software completions must fail
when checked against the current kernel object. Old physical or external
effects are instead fenced by quiescence, quarantine, and service protocol;
changing an integer cannot undo them.

## Threat and failure model

The baseline assumes mutually distrustful unprivileged domains. A domain may
contain memory-unsafe native code, loop indefinitely, exhaust its delegated
objects, send malformed protocol data, retain delegated capabilities, die in
the middle of a call, or program an authorized device incorrectly. User BEAM
code is expected to be memory-safe relative to its runtime, but the runtime,
JIT, native extensions, and drivers are not assumed fault-free.

The kernel and its architecture layer remain in the trusted computing base.
A kernel invariant violation, malicious firmware, compromised boot chain,
uncontained DMA device, uncorrectable hardware error, or hardware behavior
outside the declared architecture contract may remain system-wide. A bounded
crash capsule and reset are appropriate responses to a kernel invariant
failure; “let the kernel thread crash and restart” is not.

The failure model must also distinguish:

- **fault containment**: preventing one domain from directly modifying another
  domain or the kernel;
- **fault detection**: observing a synchronous exception, budget event,
  protocol failure, device error, or timeout suspicion;
- **recovery**: selecting and starting a replacement;
- **state repair**: restoring or reconciling durable and external state; and
- **availability**: ensuring the supervisor and its dependencies have enough
  independent resources to perform recovery.

A protection boundary does not establish all five properties.

## Dependency structure

The components form a directed authority and lifecycle graph rather than a
flat system-call list:

```text
 normalized boot facts + architecture facade
                  |
          bootstrap authority
                  |
       typed object memory store
          /       |        \
 capability   protection   scheduling
   spaces       domains      contexts
      |          /   \          |
      +---- invocation ---- timeouts
      |          |              |
 mappings   IRQ/timer/DMA   fault delivery
      \          |              /
       +---- teardown ledger ---+
                  |
       quiescence + safe reuse
```

The arrows show dependency, not authority inheritance. The IPC component may
need a scheduling context to donate CPU time, but it cannot manufacture one.
The teardown component may invoke architecture quiescence, but it must possess
the relevant domain, mapping, IRQ, or DMA control authority.

## Kernel object model

The first implementation should keep the object vocabulary explicit and typed.
Each object has immutable type, a generation governed by a no-alias reuse
policy, explicit backing memory, a lifecycle state, and object-specific
operations.

| Object | Purpose | Representative rights | Lifetime rule |
| --- | --- | --- | --- |
| `MemoryPool` or `UntypedExtent` | Authority and capacity from which typed objects or frames are created | `Split`, `Retype`, `Inspect`, `Reclaim` | Parent extent cannot be reused until all descendants are reaped |
| `Frame` | Physical memory eligible for mapping or device use | `MapRead`, `MapWrite`, `MapExecute`, `Dma`, `Reclaim` | Every mutating facet carries a protected frame-authority epoch; quarantine permanently stales it, and release destroys the old frame object before retyping the backing as a new generation after quiescence and required zeroing |
| `CapabilityTable` and table node | Protected slots containing capabilities | `Lookup`, `Insert`, `Delete`, `Manage` | Slots carry generations; table destruction invalidates contained selectors |
| `RevocationAnchor` | Accounted, stable logical-close point shared by a bounded capability lineage | `DeriveBelow`, `Close`, `Inspect` | One-way close; backing survives until every protected anchor reference and admitted operation record is drained |
| `AddressSpace` | Translation root and mapping ledger exclusively attached to one baseline domain | `Map`, `Inspect` | Root reuse waits for all mapping and remote TLB completion |
| `Mapping` | Generation-safe relation among one address space, virtual range, frame, admitted frame-authority epoch, rights, and completion epoch | `Protect`, `Unmap`, `Inspect` | Replacement at the same address is a distinct object and waits for old TLB completion; an old frame epoch permits teardown but no new access |
| `ExecutableImage` | Accounted aggregate over existing `Frame` and `Mapping` identities plus one exclusively referenced private `CodePublicationState`; it does not create a second owner for their storage | Attenuated `Write`, `Seal`, `Publish`, `Execute`, `Retire`, `Inspect` facets, with no baseline facet combining write and execute | One `ResourceAccount` pays for the aggregate and one `LifetimeGroup` owns it; destruction waits for writer closure, every publication/retirement ticket, execution quiescence, mapping/TLB completion, and diagnostic or unwind references before releasing the underlying objects |
| `ProtectionDomain` | Coordinated execution-stop and lifecycle anchor | `Inspect`, `Suspend`, `Resume`, `Terminate`, `Reap` | A replacement is a distinct domain object; external effects are tracked separately |
| `Thread` | Kernel-scheduled execution context within a domain, with an optional immutable trusted cancellation-profile binding fixed before start | `Configure`, `Start`, scoped `SelfManage`, scoped `RecoverySuspend`/`RecoveryResume`/`RecoveryTerminate`/`RecoveryReap`, `SetFaultRoutes` | Internal management facets close with the domain gate; every external recovery mutation additionally requires the current sealed domain recovery lease, and removal waits for execution, call, fault-token, and scheduling-binding drainage |
| `Endpoint` | Bounded synchronous invocation rendezvous | `Send`, `Receive`, `Grant`, `Manage`, `Close` | Logical close selects explicit outcomes for blocked calls; caller-funded acceptance additionally requires a bounded admission object |
| `Notification` | Coalescing bit signal or doorbell | `Signal`, `Wait`, `Bind` | Not a lossless queue; overflow is represented by coalescing |
| `CallRecord` and cancel facet | Caller-charged invocation state from pending admission through resource drainage | `Cancel`, `Inspect` | Pre-accept terminal events cannot create a reply token; the record survives until all call resources drain |
| `ReplyToken` | Exact accepted receiver thread's single-use reply authority created at acceptance | `Reply`, `Inspect` | The baseline facet is non-transferable and bound to the receiver thread generation; reply or a competing terminal event wins once, and the token is invalidated before drainage |
| `PassiveCallAdmission` | Server-consented, caller-charged authority and recovery credit for a finite number of caller-funded passive acceptances | `Use`, `Close`, `Inspect` | All capability copies share one protected counter; reservations and cause-specific charge transfers drain before destruction |
| `PassiveAbortPolicy` | Immutable, preauthorized conditional failure scope for one endpoint generation and callee domain, optionally restricted to one trusted receiver-profile binding | `BindAdmission`, `Close`, `Inspect` | Creation requires the actual lifecycle authority; callers receive only bounded admission objects, never general terminate authority |
| `CancellationProfile` | Trusted immutable description of a worker class for which thread-local abort is an accepted user-state boundary | `BindPolicy`, `Inspect` | Installed by the trusted manifest/profile authority; changing assumptions creates a new profile generation |
| `SchedulingContext` | Consumable CPU budget and exclusive binding/donation state | `Bind`, `Donate`, `Manage`, `Inspect` | A donation, when present, returns exactly once on call completion or cancellation; a server-funded acceptance has no incoming donation |
| `SchedulingControl` | Scoped authority to create/configure time budgets | `Create`, `SetPriority`, `SetBudget` | Limited by conserved/admission-checked CPU utilization and a maximum controlled priority |
| `FaultRoute` and resolver token | Typed delivery for one fault class and, when allowed, one-shot resolution | `Receive`, `Resolve`, `Resume`, `TerminateThread`, `Escalate` | Mapping repair, resume, exact-thread termination, device management, fatal lifecycle, and observation are separately attenuated |
| `RecoveryLease` | Epoch-fenced holder authority jointly required for state-changing domain recovery | `Use`, `Release`, `InspectEpoch` | Exactly one non-copyable current `Use` facet can authorize each supervisor-initiated domain recovery mutation, including suspend, resume, terminate, and reap |
| `RecoveryEscrow` | Precommitted attenuated domain-lifecycle, replacement-resource, and protected destination-slot authority for a successor supervisor | `DepositBeforeStart`, `IssueToCurrent`, `Inspect` | Populated without amplification before start and kept outside both the supervised domain and ordinary supervisor subtree |
| `RecoveryControl` | Independent authority to fence a failed recovery holder and issue an escrowed successor authority set | `Install`, `RevokeAndAdvance`, `Inspect` | Kept with the final recovery controller, separately from the current supervisor lease |
| `IRQBinding` | Accounted interrupt aggregate containing the source-generation ledger, current route/binding records, sink reference, preallocated event state, and exclusive link to private controller state | Attenuated `Bind`, `Route`, `Mask`, `Arm`, `Acknowledge`, `Inspect`, `Recover`, `Revoke` facets exposed through typed source, route, and binding views | Views cannot outlive or be reclaimed separately from the aggregate; destruction closes admission, masks/stabilizes delivery, drains late events, hard-path/deferred references and completion facets, then releases sink, CPU-route, device/remapping, and controller-state dependencies |
| `TimerBinding` | Authorized timer-source connection | `Bind`, `Arm`, `Acknowledge`, `Revoke` | Reap waits for late events and timer-channel quiescence |
| `DeviceProfile` | Immutable trusted drain/reset dependency graph and admissible completion evidence for one device class/version | `BindFunction`, `Inspect` | Installed through the trusted boot/hardware manifest; a driver cannot create or alter it |
| `DeviceFunction` | MMIO, configuration, function ownership, and independently resourced management-fault route | `MapMmio`, `Configure`, `BindQueue`, `Inspect` | Closing one function does not imply a shared device reset completed |
| `DmaAddressSpace` | IOMMU translation root for one immutable atomic requester/trust attachment set, with compatible profile authority and management-fault route | `Map`, `Recover`, `Inspect` | Mapping authority covers the whole attachment set; reassignment requires quiescence and a newly created root/generation |
| `DmaMapping` | Generation-safe relation among one DMA space, device-visible range, frame, admitted frame-authority epoch, rights, and completion epoch | `Unmap`, `Invalidate`, `Inspect` | Frames remain pinned through the profile's quiescence/release point; an old frame epoch permits recovery teardown but no new effect |
| `DeviceCompletionToken` | Protected one-shot evidence for one profile step and bounded mapping/queue set | `Consume`, `Inspect` | Bound to profile, reset-control epoch, operation, object generations, and completion epoch; stale evidence cannot release memory |
| `DeviceQueueLease` | Authority to submit to and stop a particular hardware queue | `Submit`, `Doorbell`, `Stop`, `Inspect` | Queue closure follows its device-specific drain/reset sequence |
| `ResetDomain` | Authority, profile, fault route, and independent control epoch for a reset boundary spanning one or more functions | `Reset`, `Quarantine`, `AdvanceLease`, `Inspect` | Shared-reset control remains outside every affected driver and ordinary domain supervisor |
| `ResetLease` | Current epoch-fenced authority jointly required for every replaceable-manager effect on reset/profile state | `Use`, `Release`, `InspectEpoch` | Exactly one non-copyable `Use` facet exists; takeover closes it and advances the reset domain's own epoch |
| `ResetControl` | Independent reset-manager takeover authority plus escrow for attenuated reset/DMA-recovery/completion facets, manager sessions, and destination slots | `Install`, `RevokeAndAdvance`, `Inspect` | Lives outside all affected functions, drivers, and ordinary domain supervisors; takeover fences mediated admission immediately but reports physical fencing only after old direct aliases quiesce |
| `ResourceAccount` | Quota payer for memory, CPU, objects, calls, and teardown work | `Charge`, `AcceptCharge`, `DelegateBudget`, `Inspect`, `MoveCharge` | Each object records one payer; moving it requires both accounts and sufficient destination capacity |
| `LifetimeGroup` | Ownership/revocation root used to enumerate objects for cleanup | `Attach`, `Close`, `Revoke`, `Reclaim` | Shared or client-owned objects may outlive a failed domain and use another group |
| `ReapToken` | Progress and completion for split-phase cleanup | `Advance`, `Wait`, `Inspect` | Completes once; records quarantined resources separately |
| `DebugAuthority` | Access to extended register and diagnostic state | `ReadContext`, `Trace`, `ReadCrashData` | Separated from ordinary recovery and service authority |

### Aggregate architecture-facing objects

`ExecutableImage` is an authority and lifetime aggregate, not another copy of
code storage. Its frame and mapping references keep the ordinary `Frame` and
`Mapping` objects authoritative for bytes and translations, while its private
`CodePublicationState` records write/publication generations, target-set
progress, and retirement. `CodeWriteLease`, `SealedCode`, and `PublishedCode`
are state-constrained views of this one aggregate. Creating the image charges
its records and pinned dependencies to one `ResourceAccount`; moving that
charge follows the normal two-account protocol. Closing the image cannot
bypass any dependency named in the table, and failed publication keeps the
underlying storage pinned or explicitly quarantined.

Likewise, `InterruptSource`, `InterruptRoute`, and `InterruptBinding` are
typed public views over one existing `IRQBinding` aggregate and its source and
route records. They are not independently allocated authority objects, cannot
mint rights the aggregate lacks, and share its resource account, lifetime
group, source incarnation, and teardown epoch. A route replacement creates a
new generational record inside the aggregate; a binding view additionally
fixes the destination and completion generation. The management route and its
reserve may belong to a longer-lived supervisor group, but it remains an
explicit destruction dependency rather than an authority hidden in the
driver-owned view.

Files, sockets, BEAM actors, PIDs, service names, mailboxes, supervisor trees,
and wall-clock calendars are deliberately absent. They are user-space
abstractions over these objects.

## Component 0: bootstrap and root-authority handoff

### Responsibility

Convert the immutable facts and mechanism handles supplied by the architecture
layer into the initial authority graph. The kernel must reach a state in which
ordinary policy runs outside privilege without leaving hidden bootstrap
authority behind.

### Internal subcomponents

1. **Kernel image verifier and reservation ledger.** Excludes kernel text,
   data, stacks, crash buffers, architecture tables, and reserved ranges from
   later allocation.
2. **Object-store initializer.** Converts usable extents into root memory-pool
   capabilities without creating user objects implicitly.
3. **Initial-domain constructor.** Builds one address space, capability space,
   scheduling context, typed fault/escalation routes, and entry thread from
   predeclared resources.
4. **Boot manifest loader.** Installs an explicit, versioned initial
   capability manifest; no domain discovers devices or memory by guessing
   numeric identifiers.
5. **Recovery/control escrow installer.** Validates independent ancestor
   lineages, precharges successor destination slots and reserves, installs
   immutable device/cancellation profiles, and creates the initial sealed
   recovery/reset lease-use facets without depending on a replaceable
   supervisor's capability table.
6. **Authority handoff and lock-down.** Revokes or seals temporary bootstrap
   paths after the recovery/root service has acknowledged the manifest.

### Invariants

- Every allocatable byte is either in exactly one pool or charged to one live
  kernel object; overlaps fail closed.
- The initial authority graph is reproducible from a signed or otherwise
  trusted manifest and can be included in crash evidence.
- Root recovery code, its scheduling budget, its fatal-fault route, and its
  memory reserve are not descendants of a component it supervises.
- Each claimed replaceable supervisor or device manager has a populated
  independent escrow and protected successor slots; exactly one sealed current
  use facet is issued for each recovery/reset epoch.
- Post-bootstrap code cannot obtain a capability by enumerating raw physical
  addresses, interrupt numbers, or device identifiers.

The root service is powerful but should not be an ambient omnipotent process.
Creation, inspection, suspension, termination, debug access, device reset, and
service publication can be split among distinct authorities. This applies the
separation-of-privilege principle and makes recovery configurations auditable.

## Component 1: typed object storage and explicit memory

### Responsibility

Represent every user-created kernel object with caller-supplied, charged
memory. This prevents a failed domain from exhausting a hidden privileged heap
and makes resource charges and lifecycle responsibility enumerable without
conflating them.

The [seL4 untyped-memory model](../30-sources/sel4-foundation-2026-reference-manual.md)
is a concrete precedent. The project should retain explicit retyping but make
the lifetime ledger and split-phase reclamation first-class.

### Creation protocol

1. The caller presents a `MemoryPool` capability with `Retype` authority, a
   `ResourceAccount` with enough quota, and an authorized `LifetimeGroup` in
   which to record ownership/reclamation responsibility.
2. The kernel validates alignment, size, type, quota, and that the selected
   extent has no live descendants.
3. The kernel initializes the object completely before publishing a
   capability to it.
4. Publication of the object capability, debit of the account, and attachment
   to the lifetime group are one atomic kernel transition.
5. Failure before publication leaves the extent reusable, account unchanged,
   and lifetime group unattached; failure after publication returns the new
   capability.

The account and lifetime group are deliberately independent. A client may pay
for service state owned by a service-neutral client-state group, and a shared
object may outlive one domain. In the baseline, however, each object has
exactly one recorded payer. Multiple contributors first delegate budget into a
shared account; object creation then performs one debit. Destruction refunds
that account, which cannot itself be destroyed while charges remain unless an
authorized operation presents source `MoveCharge`, destination `AcceptCharge`,
and the relevant object/lifetime authority, proves sufficient destination
capacity, and atomically transfers the debit and payer reference. Failure
leaves both accounts unchanged. Bulk migration is bounded and incremental, and
the old account survives until its last charge moves. Teardown work may be
charged to recovery while ownership remains with the failed domain's group.

### Accounting surface

Kernel accounting must include more than user frames:

- capability slots, derivation metadata, revocation anchors, and protected
  anchor references;
- page-table objects and mapping records;
- endpoints, notification state, reply tokens, and blocked-call records;
- passive-call admission counters, cleanup-credit reservations, and payer
  transfer records;
- scheduling contexts and refill state;
- fault records and timeout delivery;
- IRQ, timer, device-profile, IOMMU, and DMA binding and completion state;
- revocation cursors, teardown ledgers, and completion tokens; and
- per-CPU exceptional-path buffers.

No fault, timeout, or cancellation path may need an uncharged allocation to
make forward progress. Where a record cannot be delivered, a preallocated
coalescing overflow indicator must preserve the fact that evidence was lost.

### Safe reuse

Deletion of the last visible capability is not proof that memory is reusable.
The object store accepts an extent back only after the revocation and teardown
components certify that there are no live descendants, active CPU references,
translations, waiters, reply tokens, event bindings, or DMA effects. The bytes
are then zeroed before reassignment across a confidentiality boundary and the
object generation advances.

## Component 2: capability spaces and authority

### Representation

A user-visible capability selector is only a local designator:

```text
selector = (slot_index, slot_generation)

protected_entry = {
    object_reference,
    object_generation,
    object_type,
    rights,
    badge_or_facet,
    derivation_node_reference: (lineage_id, lineage_generation),
    bounded_anchor_path: [
        (anchor_reference, anchor_generation, observed_epoch), ...
    ],
    local_entry_state
}
```

The integer selector is not authority outside the protected capability table.
The kernel resolves every invocation through one complete-mediation path that
checks the slot generation, object generation, type, requested operation,
rights, lifecycle state, every anchor in the bounded path, and any
facet-specific constraint.

A `RevocationAnchor` is a caller-funded kernel object with a protected state
`OPEN(epoch)` or `CLOSED(close_epoch)`. A capability intended to be a later
selective-revocation root is minted beneath an explicit anchor; this cannot be
retrofitted to an arbitrary lineage at constant cost. Further derivation
copies the protected anchor path and may append a child anchor only up to a
declared maximum depth. Closing an anchor is a one-way, constant-work
linearization that changes its protected state. Any later lookup whose stored
anchor generation/epoch is no longer current fails before object admission.
Derivation records and charged cursors then remove entries incrementally.

Invocation admission atomically validates every anchor as `OPEN` and installs a
bounded admitted-operation pin before releasing the capability/object locks.
Anchor close competes with that transition: if close linearizes first, no pin
is created and the operation is rejected; if admission linearizes first, its
pin and effect ledger survive closure and must drain. Capability derivation and
transfer use the same close-versus-install rule, so they cannot publish a new
descendant after closure.

The anchor's backing memory cannot be reclaimed merely because its closing
capability disappeared. Protected entries hold accounted references, and
already admitted operations are represented by bounded kernel records in the
teardown ledger. Only after those references and records drain may the anchor
be destroyed. This supplies stable storage for instant logical closure without
an unbounded parent walk or a pointer into user memory.

Derivation lineage is likewise not stored as a pointer to a reusable
capability slot. Each installed capability references a charged,
generation-safe lineage node. Copy or mint creates a child node; move preserves
the same node while atomically changing slots; delete removes the slot
reference but retains a tombstone node while any child, revocation cursor,
anchor reference, or admitted operation can name it. Physical descendant
revocation walks these stable nodes. A node is reclaimed and its generation
made reusable only after all such references drain, so deleting and reusing an
ancestor slot cannot orphan descendants or redirect revocation into a new
lineage. The payer and lifetime group of lineage metadata are explicit, and
path/depth/fan-out limits make its incremental traversal accountable.

Generation counters need a no-alias policy. A counter must be wide enough that
wrap is unreachable under the declared lifetime, or the identifier must be
retired before a prior value can become valid again. “Probably not reused” is
not an adequate stale-message defense.

### Capability operations

The ABI should distinguish these operations rather than overloading “copy” or
“close”:

- `copy`: create another reference with the same or fewer rights;
- `mint`: create an attenuated reference with a new badge or object facet;
- `move`: atomically remove one slot and install the reference in another;
- `delete`: remove one local reference without affecting siblings;
- `close_anchor`: logically invalidate capabilities derived beneath an
  explicitly installed revocation anchor;
- `revoke_descendants`: physically remove entries beneath a derivation point
  in bounded slices, using a closed anchor when immediate logical denial was
  required;
- `close_object`: publish a one-way lifecycle closure and reject later object
  operations without changing its generation;
- `close_facet`: invalidate a revocable session or proxy without destroying a
  shared underlying service; and
- `mint_epoch_session`: using a sealed recovery/reset lease plus compatible
  target-service authority, create only a narrow non-lifecycle session facet
  beneath that lease epoch's closable anchor; and
- `destroy`: finish object teardown once ownership and lifecycle conditions are
  satisfied; only later safe backing-storage reuse advances the generation.

`close_object`/`object_close` is an idempotent, type-dispatched logical
transition requiring that object's `Close` or lifecycle-control right. It
rejects new admissions and returns a bounded progress state when existing
relationships must drain; it never aliases `destroy`. `facet_close` closes one
revocable relationship without closing the target object. Final `destroy`
requires the closed object's type-specific drainage and ownership proofs.

`RecoveryLease.Use` and `ResetLease.Use` are sealed facets: generic `copy`,
`mint`, `move`, `Grant`, and transfer reject them. Read-only `InspectEpoch`
facets may be copied. Only the corresponding independent control operation may
atomically close the old use facet, advance the protected epoch, and install
one successor into a pre-reserved protected destination slot. Threads sharing
the holder's capability space may invoke that one facet, and the holder can
still proxy policy requests, but the kernel recognizes one current recovery
principal rather than several independently transferable lease copies.
Session facets for registries or state repair may be derived beneath the lease
anchor only through `mint_epoch_session`. That operation also validates the
target registry, state-repair, device-attestation, or manager facet and cannot
create `Use`, `Reset`, `Terminate`, or any right absent from both inputs. The
sessions are fenced by takeover and never substitute for the sealed use facet
on a kernel lifecycle mutation.

Derivation may only attenuate: child rights are a subset of parent rights, and
facets can narrow but never widen the target. Object types define their own
rights; there is no universal `Admin` bit that silently authorizes unrelated
operations.

### Delegation and transfer

Sending authority requires two independent permissions:

1. the sender holds `Grant` or an operation-specific delegation right; and
2. the receiver has designated a destination slot and has slot and object
   quota.

Installing the receiver's capability and consuming or retaining the sender's
reference is atomic. The initial implementation should transfer at most one
capability per invocation. Multi-capability transfer, if later needed, must be
transactional so quota exhaustion cannot produce a partial authority graph.

Endpoint rights should at least separate `Send`, `Receive`, `Grant`, and
`Manage`. A badge identifies the capability facet used for an invocation, not
the caller's immutable identity: a badge may itself be delegated unless the
specific facet forbids it. Code that interprets a badge as “proof that process
X called” reintroduces the confused-deputy problem.

### Revocation mechanisms

No single revocation mechanism fits every lifetime:

- **derivation records** enumerate attenuated descendants for bounded physical
  removal but do not by themselves make a large traversal instantaneous;
- **accounted revocation anchors and epochs** are held by protected descendant
  entries and checked on invocation, allowing one published close to reject
  later acquisitions before physical traversal completes;
- **slot generations** reject stale local selectors;
- **object lifecycle closure** rejects operations after logical destruction,
  while **object generations** prevent those references from aliasing safely
  reused backing storage;
- **revocable facet or session objects** permit one relationship to be cut
  without destroying a shared service; and
- **memory-pool/lifetime groups** enumerate owned objects for domain teardown.

Delete and revoke are not synonyms. Revoking a domain's capability space
removes its authority but must not destroy a shared object owned by another
domain. Conversely, destroying an object invalidates every reference even if a
holder is outside the failed domain.

Object-producing operations must not launder temporary authority into a
durable relationship. Each ABI operation therefore classifies each input facet
as either **effect-bearing lifetime authority**, an **admission/consumed
guard**, or a resource/placement input. By default, a new `Mapping`,
`DmaMapping`, binding, session, transferred capability, or other product
inherits the bounded, deduplicated union of every effect-bearing input's
revocation-anchor path plus each applicable lifetime-bearing domain gate.
Creation rejects before publication if that dependency vector exceeds the
configured maximum. Closing any inherited anchor immediately rejects new
product operations and places the product on that anchor's charged,
incremental type-specific teardown ledger; already active PTE, TLB, IRQ, or
DMA effects remain pinned until their normal completion or quarantine barrier.
Here “new product operations” means holder-facing operations that create,
extend, redirect, or reactivate an effect. Separately scoped recovery authority
may still advance idempotent `Unmap`, `Invalidate`, drain, and evidence-
inspection transitions through the protected teardown ledger, but cannot
reopen access. The closing operation does not claim that hardware access
vanished at logical publication.

An operation schema may omit an admission-only or one-shot guard from the
product lineage only when separate current lifetime authority independently
authorizes the product and the guard is atomically consumed or recorded in the
transition. For example, a fault resolver token is a one-shot guard envelope
around an attenuated `FaultMap` grant captured from the target address space:
resolution consumes the token identity, while the resulting mapping inherits
the embedded address-space/domain anchor vector plus the current `Frame.Map`
lineage. A permanent capability copy or move preserves the source
capability's lineage, not the transport endpoint's lifetime. A capability
borrowed for a call always adds the call anchor because the borrow itself
supplies future-effect authority for the callee.

Detaching an effect-bearing lifetime dependency is allowed only when the
relevant input carries an explicit type-specific `CreateDurable` right
unavailable on borrowed facets, every affected lifetime authority consents,
and the caller supplies a new authorized lifetime group/anchor and its
charges. This commits a documented lifetime transfer rather than dropping
dependencies accidentally. Deleting an input capability slot does not undo a
committed product, but closing an inherited anchor cannot be escaped by
copying the cap, transferring it, or creating a child kernel object. In
particular, a call-borrowed `Frame.Map` or `Frame.Dma` facet cannot create a
mapping that survives call-lifetime closure unless separately held durable
authority explicitly authorizes that result.

The [Capability Myths
Demolished](../30-sources/miller-et-al-2003-capability-myths.md) analysis is
important here: capability systems can support confinement, revocation, and
usable naming, but only when indirection, derivation, and application protocol
are designed rather than assumed. [Capsicum](../30-sources/watson-et-al-2010-capsicum.md)
provides a pragmatic demonstration that capabilities can be introduced as
rights-limited descriptors and capability mode, while also showing that a
compatibility-oriented process API is not itself a complete kernel object
model.

### Authority invariants

1. **Unforgeability:** no user memory value becomes authority without a valid
   protected table entry.
2. **No amplification:** every derived right is a subset of an existing right
   or comes from an explicitly authorized creation operation.
3. **Complete mediation:** every object operation checks a current capability
   through the same semantic lookup path, including fast paths.
4. **Stale denial:** a mismatched slot, object, domain, endpoint, or reply
   generation fails before changing a current kernel object. This does not undo
   an external effect admitted by an earlier valid invocation.
5. **Fail-safe default:** unknown operation, type mismatch, exhausted quota,
   closing object, or ambiguous state is denied.
6. **No ambient namespace:** names and PIDs may locate a broker, but they never
   substitute for possession of operation authority.

## Component 3: protection domains, threads, and address spaces

### Why `ProtectionDomain` is first-class

A thread and an address space are not enough to express a coordinated
execution stop. On an SMP machine, a runtime or driver may have multiple
threads running on several CPUs, outstanding calls, donated scheduling
contexts, shared mappings, and hardware bindings. Constructing “stop this
component” by walking unrelated thread objects creates races with creation,
migration, and fault handling.

The domain object makes thread admission and execution-stop publication one
kernel lifecycle. It does not make shared memory, device state, durable state,
or external output fail-stop. Those effects remain in the teardown and service
protocols.

The kernel should therefore make `ProtectionDomain` a small lifecycle anchor
containing exactly:

- one kernel domain-object identity;
- one capability-space root;
- one address-space root;
- an exact, kernel-maintained set of member threads;
- typed fault routes for resolvable thread faults, budget events, fatal
  lifecycle events, and bounded diagnostic observers;
- one current recovery-lease epoch plus an explicit fallback/escalation route;
- references to a default resource account and a domain lifetime group, while
  allowing individually shared or client-charged objects to use different
  accounts and lifetime groups; and
- a lifecycle state and teardown ledger.

It does **not** contain a service name, BEAM actor list, supervisor strategy,
restart count, or application policy.

In the baseline, a domain's address-space root and capability-space root are
exclusive and immutable after start; no second domain can attach either root.
Shared memory is expressed by separately authorized `Mapping` objects over the
same `Frame`, and shared authority by capability delegation into separate
tables. A future profile that shares an address-space or capability-space root
must treat every attached domain as one correlated security, stop, and reaping
group; it cannot continue to claim mutual domain isolation.

Domain configuration installs one fixed-size root-gate vector: an execution
gate; a relationship/lifetime-derivation gate inherited by domain-bound
products and descendants; an outbound-call gate inherited by call origins;
and a session gate inherited by domain-scoped sessions. “Domain-root gates”
below always means this complete already-installed vector. Per-thread and
per-object gates refine it but do not replace it. Closing the vector is
constant work and immediately denies every later root admission; enumerating
its previously admitted descendants remains charged incremental work.

### Domain lifecycle

```text
DEFINED -> STARTING -> RUNNING
RUNNING -> SUSPENDING(suspend_epoch) -> ADMIN_SUSPENDED
SUSPENDING -> SUSPEND_FAILED
SUSPEND_FAILED --late checkpoint acknowledgement with full postconditions-->
  ADMIN_SUSPENDED
ADMIN_SUSPENDED --authorized resume--> RUNNING

DEFINED -------------------------------> CLOSING(no_stop) -> STOPPED
STARTING | RUNNING | SUSPENDING | SUSPEND_FAILED | ADMIN_SUSPENDED
                         -> CLOSING(stop_epoch) -> STOPPING(stop_epoch)
                                                       |-> STOPPED
                                                       `-> STOP_FAILED

STOP_FAILED --late checkpoint acknowledgement with full postconditions--> STOPPED

STOPPED -> DRAINING
DRAINING -> QUIESCENT -> SANITIZING_REUSABLE_SET
                         -> REAPED_CLEAN -> DEAD
DRAINING -> QUARANTINING -> SANITIZING_NONQUARANTINED_SET
                            -> REAPED_WITH_QUARANTINE -> DEAD

DEAD --destroy/retype after object-specific completion--> backing extent
                                                          reusable under a
                                                          non-aliasing generation
```

This is the authoritative domain lifecycle. Entry into observable `CLOSING`
is the termination linearization point. In one bounded transition it freezes
membership, closes new execution admission, atomically publishes closure of
the fixed-size, already installed domain-root gate vector,
creates `stop_epoch`, and dispatches
stop requests to the maintained bounded running-CPU mask. It does not walk
capability slots or owned objects first. Active pins, mappings, scheduling
bindings, and other resources needed by an executing thread remain retained.
The kernel promptly enters `STOPPING`; bulk or type-specific invalidation runs
in charged slices concurrently where safe or after `STOPPED`, and physical
drainage follows the stop proof. A domain that never left `DEFINED` uses
`CLOSING(no_stop)` because it has no execution to
stop and may enter `STOPPED` after the kernel verifies empty active-CPU and
in-kernel activation sets; configured never-run member threads remain owned
objects and are drained normally. A domain that could have executed must
complete the stop epoch. `STOP_FAILED` cannot advance through teardown until a
late acknowledgement proves the same checkpoint, lock-release,
reference-release, and operation postconditions as an on-time acknowledgement.
Merely halting or resetting a CPU proves that execution ceased, not that an
interrupted kernel activation left shared kernel state consistent; without a
separately verified CPU-recovery protocol, that case is a node-level kernel
failure and reset.

Liveness suspicion is monitor state orthogonal to this kernel lifecycle. A
suspected domain can remain `RUNNING`, be probed and cleared, be
administratively suspended and resumed, or be explicitly terminated. A missed
heartbeat does not transition it to `STOPPED`.

A resolvable page or thread fault is also not automatically a domain state.
The affected thread transitions from `FAULT_BLOCKED` to either `RUNNABLE` after
a valid one-shot resolution or `THREAD_TERMINATING`; other domain threads can
continue unless policy or fault class requests a domain stop. `STOPPED` only
states that no member thread is executing. It is not `REAPED_CLEAN`: remote
translations, calls, IRQ events, shared aliases, and DMA may remain live.

Every operation that creates a new relationship into a domain validates its
fixed root admission gate at the same linearization point, even when an
external principal owns or pays for the new object. This includes thread/member
attachment, address-space mappings, capability-table insertion, scheduling and
fault-route bindings, endpoint receiver admission, IRQ/timer/device bindings,
and attachment to a domain-owned lifetime group. `CLOSING` therefore prevents
an authorized pager, scheduler, broker, or device manager from extending the
domain behind the reaper. Relationships admitted before closure retain pins
and drain normally; unrelated shared objects are not destroyed merely because
one domain's attachment closed.

Domain control authority must be split into at least `Inspect`, `Suspend`,
`Resume`, `Terminate`, and `Reap`. A monitor need not be able to restart or
debug. A debug service need not be able to terminate. The recovery owner's
state-changing operations also present the current `RecoveryLease` epoch. Its
control capabilities and resources must live outside the child's derivation
and lifetime subtree.

Thread control has the same provenance distinction. A runtime may receive
domain-internal `SelfManage` facets derived beneath that domain's root gates;
invocation also checks that the caller is executing in that same domain, and
the facet cannot be exported as cross-domain authority. It is unusable once
the domain closes and is never presented as recovery authority. Every external
supervisor/recovery facet is explicitly tagged
`Recovery*` for the target domain and every invocation additionally presents
that domain's current sealed `RecoveryLease.Use`. Takeover therefore fences an
old supervisor's retained `Thread` selectors just as it fences domain-wide
control. No unqualified thread-control facet is issued across that boundary.

### Threads and cross-core freeze

A thread is a kernel scheduling and architectural context, not a BEAM process.
The kernel owns its membership relation, run state, current CPU, optional
scheduling-context binding, active invocation, and typed fault routes. Moving a
thread between domains is initially forbidden; creating a new thread in a
domain is explicit and charged.

Administrative suspension is a resumable freeze, not a label change. It closes
new member execution admission under `suspend_epoch`, uses the same bounded
cross-core checkpoint and acknowledgement discipline as terminal stop, and
publishes `ADMIN_SUSPENDED` only when every member is off-CPU and retains no
in-kernel activation. It does not close lifetime anchors or imply call, IRQ, or
DMA quiescence. A missing acknowledgement produces `SUSPEND_FAILED`, never a
false suspended state. Authorized resume atomically reopens execution admission
and enters `RUNNING`; a terminal decision instead enters `CLOSING` and runs a
fresh stop epoch.

Individual thread termination has its own lifecycle, serialized with the
domain membership and stop epochs:

```text
NEW -> CONFIGURED -> RUNNABLE <-> RUNNING
RUNNING -> BLOCKED -> RUNNABLE
RUNNING -> FAULT_BLOCKED -> RUNNABLE
RUNNING --server-funded endpoint_receive waits-->
  RECEIVE_BLOCKED(endpoint_epoch, server_context_bound)
RECEIVE_BLOCKED --accept wins--> READY(RequestAccepted, server_context_bound)
RECEIVE_BLOCKED --endpoint close drains--> READY(ReceiveClosed, server_context_bound)
READY --positive dispatch budget and execution admission open--> RUNNABLE
RUNNING --terminal passive receive--> PARKED_RECEIVE(endpoint_epoch, unbound)
PARKED_RECEIVE --compatible caller-funded acceptance-->
  READY(RequestAccepted, donated_context_bound)
PARKED_RECEIVE --endpoint close wins--> RECEIVE_CLOSED(endpoint_epoch, unbound)
RUNNING --reply_and_receive commits-->
  PARKING_RECEIVE(call_id, endpoint_epoch, close_pending=false, donation_bound)
PARKING_RECEIVE --drain, endpoint still open--> PARKED_RECEIVE(endpoint_epoch, unbound)
PARKING_RECEIVE --drain, close_pending--> RECEIVE_CLOSED(endpoint_epoch, unbound)

RUNNABLE | RUNNING | BLOCKED | FAULT_BLOCKED | READY | RECEIVE_BLOCKED |
PARKING_RECEIVE | PARKED_RECEIVE
  -> THREAD_SUSPENDING(suspend_epoch, saved_state)
  -> THREAD_SUSPENDED(saved_state) | THREAD_SUSPEND_FAILED(progress)
THREAD_SUSPEND_FAILED --late checkpoint acknowledgement with full postconditions-->
  THREAD_SUSPENDED(saved_state)
THREAD_SUSPENDED(saved_state) --authorized resume wins-->
  saved_state adjusted by any event that won while frozen

validated thread-local caller-funded handler --failure and checkpoint drain-->
  CALL_ABORTED(call_id, outcome, saved_state, unbound)
generic caller-funded handler --failure selection-->
  ABORT_PENDING + domain CLOSING(stop_epoch) -> domain terminal path

NEW | CONFIGURED | RUNNABLE | RUNNING | BLOCKED | FAULT_BLOCKED |
THREAD_SUSPENDING | THREAD_SUSPENDED | THREAD_SUSPEND_FAILED |
READY | RECEIVE_BLOCKED | PARKING_RECEIVE | PARKED_RECEIVE |
RECEIVE_CLOSED | CALL_ABORTED
  -> THREAD_TERMINATING(thread_stop_epoch)
  -> THREAD_STOPPED
  -> THREAD_DRAINING
  -> THREAD_DEAD
```

`THREAD_SUSPENDED(saved_state)` is published only after that thread is off-CPU
and has left its in-kernel activation at a bounded checkpoint. Suspension is a
freeze overlay, not destruction of the underlying wait: a blocked thread
normally resumes blocked. If its reply, timeout, fault resolution, or other
event wins while frozen, the protected saved state changes according to that
event and resume observes the resulting state. Suspension does not drain calls
or external effects. A never-configured `NEW` thread may take the terminal path
without a CPU stop, but its charged object and membership record still drain.
A missing acknowledgement returns `THREAD_SUSPEND_FAILED(progress)`, never a
false suspended state; a late complete acknowledgement may finish it, while a
terminal decision escalates through thread termination and, if necessary, a
domain stop.

Suspension is a product overlay for receive states. It atomically closes the
thread's receive-admission gate against endpoint acceptance. A bound
`RECEIVE_BLOCKED` or `READY` state is saved; accepted request or close events
can update that saved readiness while dispatch stays forbidden. An already
off-CPU `PARKED_RECEIVE` remains parked but ineligible for acceptance until
resume. `PARKING_RECEIVE` must finish or checkpoint its in-kernel drainage
before suspension acknowledges. `RECEIVE_CLOSED` and `CALL_ABORTED` are
nonresumable and take only terminal teardown, not the suspension path.

`thread_resume` requires the applicable domain-internal `SelfManage` authority
or both `Thread.RecoveryResume` and current `RecoveryLease.Use`, a `RUNNING`
domain, a current saved-state epoch, and no caller-funded `ABORT_PENDING` call
tag. Resume
competes atomically with `thread_terminate`, passive-call failure selection,
and the domain's transition to `CLOSING`: if a terminal or abort transition
wins, resume is rejected; if resume wins first, it restores the event-adjusted
saved state but remains subject to any later failure checkpoint or domain stop.

`CALL_ABORTED` is deliberately not resumable and exists only for an admission
bound to a trusted `CancellationProfile`. It records a caller-funded handler
that was stopped at a safe kernel/scheduling checkpoint after a post-accept
failure and then lost the donated scheduling binding. Its saved user
continuation may be in the middle of a handler, so it is neither
receive-eligible nor eligible for `thread_resume`, `sched_bind`, or another
endpoint acceptance. The profile must establish that terminal thread reap and
replacement does not violate untracked shared user-state invariants. Without
that profile, failure remains `ABORT_PENDING` only until the simultaneously
selected domain `CLOSING` moves the thread into its terminal lifecycle; generic
mode never publishes `CALL_ABORTED`. A future recovery-trampoline extension
would require a separately specified entry point, authority, independent
budget, and proof that arbitrary saved continuations cannot be re-entered.

The active-call tag is orthogonal to ordinary run, wait, fault, and suspension
state. For a caller-funded passive handler, a post-accept failure atomically
changes that tag from `ACTIVE` to
`ABORT_PENDING(call_id, reason)` at outcome selection, before any potentially
split-phase drainage. Scheduler dispatch, wakeup, `thread_resume`,
fault-resolver `Resume`, and endpoint acceptance all reject a thread with that
tag. A running handler receives a checkpoint request; an off-CPU handler stays
off-CPU. For the generic recovery scope, the same outcome transition invokes a
preauthorized fatal policy and atomically starts domain
`CLOSING(stop_epoch)`, closing new admission and promptly requesting peer
checkpoints to bound further propagation. Peers may already have observed
partial user state or issued admitted effects before the stop; the kernel
records those outcomes as indeterminate for protocol reconciliation rather
than claiming rollback.
Only an admission bound to a validated cancellation-safe worker profile may
leave the domain running and later publish thread-local `CALL_ABORTED`. If
resume or dispatch linearized first, the later failure still sets the gate and
requests the ordinary checkpoint. Such a profiled nonterminal handler may
reach `CALL_ABORTED`
from `READY`, `RUNNABLE`, `RUNNING`, `BLOCKED`, `FAULT_BLOCKED`, or a completed
suspension checkpoint. Drainage invalidates any outstanding resolver token and
preserves its fault evidence. If `THREAD_SUSPENDING` or
`THREAD_SUSPEND_FAILED` lacks a complete checkpoint acknowledgement, neither
`CALL_ABORTED` nor donation return may be published; the operation reports
progress and joins a late acknowledgement or escalates through terminal thread
and domain stop. If callee termination or domain `CLOSING` wins first, the
thread remains on `THREAD_TERMINATING`/domain-stop state instead of being
rewritten to `CALL_ABORTED`; the terminal path subsumes call drainage and
performs the single return of any donation.

The success branch clears the same tag explicitly. Reply selection atomically
changes `ACTIVE(call_id)` to `REPLY_DRAINING(call_id)` and wins the call
outcome; later cancel or close cannot reinterpret it as failure. Only after
call descendants have drained and the donation has returned exactly once does
completion clear the tag and publish `PARKED_RECEIVE` or
`RECEIVE_CLOSED`. `reply_and_terminate` lets terminal thread drainage clear the
tag instead. No reusable receive state may coexist with `ACTIVE`,
`REPLY_DRAINING`, or `ABORT_PENDING`.

`PARKING_RECEIVE` is an internal product state: reply and the next receive-slot
reservation committed atomically, but the kernel activation still holds the
donated context while call state drains. Endpoint close may set
`close_pending` and unlink that reservation, but cannot claim the thread is
unbound. `PARKED_RECEIVE` and `RECEIVE_CLOSED` are published only after the
checkpoint and donation return make that true. The former is eligible only for
one compatible caller-funded acceptance. The latter records that endpoint
closure won while the thread was safely between handlers; it holds no endpoint
reference, cannot accept or resume, and is inspectable only before terminal
thread teardown. This baseline intentionally requires a supervisor to reap it
rather than inventing CPU authority with which it could return from the
terminal park syscall.

Acceptance never makes either funding mode immediately runnable. For a
caller-funded request, one linearizable commit installs
`ACTIVE(call_id)`, binds the donated context, changes the `CallRecord` to
accepted, activates the reply token and policy pin, consumes the admission
reservation, and publishes
`READY(RequestAccepted, donated_context_bound)`. A server-funded acceptance
analogously commits the accepted record, token/pin, and
`READY(RequestAccepted, server_context_bound)` without an active-donation tag.
A competing cancel, close, lifecycle, or peer-failure transition orders wholly
before or after that commit. Dispatch then independently checks
that the bound context has a positive handler-budget quantum and that thread,
domain, and scheduler admission remain open. An exhausted donated context
therefore stays `READY` until a permitted refill; acceptance cannot smuggle an
unbudgeted passive handler into execution merely because the caller retained
enough reserve for the kernel acceptance prefix.

Thread termination similarly requires domain-internal `SelfManage` while its
root gate is open, a one-shot manifest-authorized fault token for the exact
thread, or both `Thread.RecoveryTerminate` and current
`RecoveryLease.Use`; external possession of a stale generic selector is never
sufficient. Termination first closes that thread's fixed outbound-call gate, then closes
new wakeup, endpoint acceptance, and user entry for that thread; removes or
interrupts it on its current CPU; and waits for a bounded
kernel checkpoint before publishing `THREAD_STOPPED`. It then cancels and
drains the thread's call records and reply tokens, closes call-lifetime
anchors, invalidates any one-shot fault-resolver token, detaches its bounded
fault record into the domain evidence ledger, returns or unbinds its
scheduling-context state exactly once, and removes the thread from domain
membership only when no execution or kernel reference remains. A late
`fault_resolve` then fails before dereferencing the dead thread. `thread_reap`
performs this work in bounded charged slices.
A missing CPU acknowledgement cannot produce `THREAD_DEAD`; it escalates to a
domain stop, and failure of that stop is a node-reset condition under the
baseline. Domain teardown may drive the same thread substates in bulk, but
cannot bypass them. A resolvable fault token may choose `Resolve`/`Resume` or
this termination path only when it carries the separately attenuable
`TerminateThread` right for that exact thread; otherwise it must escalate to a
holder of `Thread.RecoveryTerminate` presenting the current
`RecoveryLease.Use` while peer threads continue.

That authority proves permission to stop execution, not that thread-only
recovery is semantically safe. `TerminateThread` is enabled only for a
manifest-declared isolated/reconstructible thread class whose user-space locks
and shared-state obligations are explicit. An ERTS scheduler, JIT, in-process
NIF, or generic native thread that may hold runtime-wide state defaults to a
domain-fatal route. Ordinary BEAM actor failure remains a runtime event instead
of becoming kernel thread termination.

Stopping a multicore domain is a protocol:

1. for a supervisor-initiated termination, validate the current recovery
   epoch; for a configured fatal fault, use the preauthorized fatal policy and
   snapshot the current recovery operation record. Atomically enter
   `CLOSING(stop_epoch)`: freeze membership; close new thread creation, start,
   resume, migration, endpoint acceptance by member threads, wakeup, and user
   entry; publish closure of the fixed domain-root admission gates; initialize the
   preallocated acknowledgement slots for the kernel-maintained bounded mask
   of CPUs running a member; and immediately send each request carrying the
   domain identity and stop epoch. Then enter `STOPPING(stop_epoch)` without
   waiting for per-object invalidation or drainage;
2. use the frozen, epoch-tagged membership ledger without copying an unbounded
   member list or allocating stop metadata. An IPI handler validates its
   carried epoch against the domain and records only
   `STOP_REQUESTED`/`STOP_PENDING` in the already initialized CPU slot. It may
   record `ACKNOWLEDGED` only after that CPU has no member user execution and
   every member kernel activation on it has completed the checkpoint
   postconditions in steps 4 and 6; configured domain/thread limits and
   preallocated membership records bound later enumeration work;
3. interrupt members in user mode, while kernel activations proceed to an
   explicit bounded stop checkpoint;
4. at that checkpoint, each activation either commits an operation whose
   linearization point it already passed or aborts before its linearization
   point, then releases temporary locks and references and records any admitted
   effect in the teardown ledger;
5. mark incoming and outgoing calls against the stop epoch, prevent member
   re-entry, and request cancellation; downstream drainage and return of
   donated scheduling bindings remain explicit teardown work rather than a
   precondition for execution stop;
6. save and sanitize complete architecture contexts and acknowledge the stop
   epoch from every participating CPU; and
7. publish `STOPPED` only after every member is off-CPU and no member retains an
   in-kernel activation.

Privileged execution is never cancelled at an arbitrary instruction boundary:
it may hold locks, temporary object references, or a partially published
operation. Every syscall and fault path therefore needs a declared
linearization point, abort path, and bounded stop checkpoint.

The lower architecture layer supplies IPI, context, and CPU-quiescence
mechanisms. The domain component supplies membership, authority, state, and
completion semantics.

If any CPU fails to acknowledge the stop epoch, the kernel publishes
`STOP_FAILED`, not `STOPPED`, `REAPED_CLEAN`, or reuse. Recovery escalates to
node failure/reset under the baseline. CPU offlining is sufficient only in a
future profile with a separately verified protocol proving that no interrupted
kernel activation retained a lock, reference, or partial operation. A timeout
is evidence that stop completion is unavailable, not permission to assume the
old execution ended.

## Component 4: bounded invocation and transport

### Synchronous endpoints

The primary protected communication primitive should be a small synchronous
endpoint: a rendezvous or protected procedure call carrying a fixed-size
register payload and at most one explicitly typed capability transfer
initially. The first profile rejects raw out-of-line `(address, length)`
descriptors: caller death, cancellation, remapping, and concurrent writes would
otherwise make lifetime and snapshot semantics ambiguous. Larger traffic uses
the bounded shared-memory protocol below. A later zero-copy call extension
would require a caller-charged `BufferLease` naming exact frame/mapping
identities, generations, rights, byte range, ownership state, and a
call-lifetime pin; drainage would have to prevent unmap/reuse until every
callee access ended. The kernel does not hold an arbitrary message queue.

Synchronous IPC makes server work and client waiting explicit and enables CPU
budget donation. It is not automatically safe. Shapiro's analysis of
[synchronous IPC vulnerabilities](../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md)
shows how dependency chains, priority inversion, server failure, and resource
retention can become availability problems. Therefore the call state must be a
kernel object, not an implicit stack convention.

An endpoint declares whether accepted work is caller-funded or server-funded.
A funding mode is immutable for the endpoint's generation; changing it requires
closing and draining that endpoint and creating a new one. Pending call records
and parked receivers retain the endpoint generation, so acceptance cannot pair
a stale funding assumption with a receiver in the other binding mode.
A server-funded receiver remains bound to its own context and receives no
donation. A caller-funded passive receiver must be parked on the endpoint with
no context bound; acceptance atomically transfers the caller's exclusive
donation binding and can occur only on a CPU allowed by that context's affinity.
If placement is incompatible and no authorized atomic migration is possible,
the call remains unaccepted or returns a typed pre-accept rejection.

Caller-funded cancellation is also authority to consume one passive handler:
after acceptance, cancel, timeout, caller death, or endpoint close can force
that handler out of service and, in the generic profile, terminate and replace
its whole domain; only a validated cancellation-safe profile stops at
thread-local `CALL_ABORTED`. Ordinary reusable `Send` is
therefore insufficient. The caller must present a capability to a
`PassiveCallAdmission` object created with endpoint `Manage` consent and a
current `PassiveAbortPolicy`, and bound to that endpoint identity/generation,
callee domain, and policy generation. A domain-fatal policy is created only by
presenting endpoint `Manage`, the exact domain's `Terminate` facet, and its
current `RecoveryLease`; it stores only the conditional authority to enter
`CLOSING` after a kernel-proven accepted passive failure. A thread-local policy
instead requires the permitted thread authority and a trusted immutable
`CancellationProfile` generation. Creating either policy is an explicit
authorized configuration transition; the caller receives only admission
`Use`, never a general lifecycle capability. The caller supplies its backing memory,
a finite acceptance/abort-use count, a server-approved minimum remaining
deadline and donated handler-budget quantum, a source account with
`MoveCharge`, and a server-selected abort-work account whose `AcceptCharge`
consent and exact maximum amount are captured at creation. Capability copies
name the same protected counter and cannot multiply uses or credit. Creating
and enqueueing a `PENDING` caller-funded call atomically pins the admission and
reserves one finite use plus the declared cause-specific recovery capacity for
the receiver-recovery scope—normally whole-domain stop, reap, and replacement.
Acceptance revalidates the reservation, deadline floor, and handler budget and
consumes that reservation in its single commit; every pre-accept terminal path
returns it. Clean reply returns the consumed use according to the facet's
policy. Outcome selection chooses exactly one cleanup payer: caller cancel,
deadline, or caller death consumes the caller/session credit; callee death uses
the server's configured recovery account; endpoint revocation uses the closer's
optional accepted charge only as reimbursement, while correctness always uses
the endpoint generation's precommitted close/teardown reserve. Every path still
requires reserved capacity before acceptance, and no path may fall back to the supervisor's
non-donatable emergency reserve. Exhaustion rejects the call before acceptance,
and replenishment or a new admission object requires `Endpoint.Manage` and
fresh bilateral account consent. Endpoint or admission close rejects new uses
and drains reservations in charged slices. The maximum outstanding
credits is backed by preallocated replacement capacity and a dedicated
abort-work scheduling budget. Until this attribution is modeled and
implemented, mutually untrusted reusable clients must use server-funded active
handlers; caller-funded passive mode is limited to one-shot or explicitly
bounded-trust sessions in disposable service domains.

`PassiveAbortPolicy` is an accounted immutable object, not an endpoint badge.
It records the exact endpoint/domain generations, failure scope, payer routes,
and optional trusted `CancellationProfile` identity, generation, and manifest
hash. For thread-local scope, thread configuration immutably binds either an
exact thread generation or, for a worker pool, that trusted profile
identity/generation before start. Acceptance compares the selected receiver's
protected binding with the policy; endpoint/domain/profile equality without a
matching receiver binding is insufficient. Each admission object holds a
protected policy reference. Policy close is a one-way gate that rejects later
acceptance, but an accepted call holds an admitted policy pin so later close
cannot erase its conditional stop action or reserved payer. Policy destruction
waits for every admission reference and active pin. A cancellation profile is
installed only by the trusted manifest/profile authority; changing its
assumptions creates a new generation, and old policies cannot silently follow
it.

### One-shot reply authority

Before endpoint admission, the caller supplies a charged `CallRecord` and
receives or designates its cancel facet. The record contains the caller,
originating domain identity, a bounded origin-gate vector containing the
domain outbound-call anchor/epoch, caller-thread outbound-call gate/epoch, and
for a nested call its parent call-lifetime anchor/epoch, endpoint
identity/generation and funding mode, request identifier, deadline,
payload/capability reservations, optional `PassiveCallAdmission`
identity/generation/reservation, any explicit transfer descriptor, and
`PENDING` state. The cancel facet may be held by another thread or an
authorized supervisor; domain stop closes the outbound-call anchor and can
request cancellation through the domain lifecycle authority. No reply
authority exists yet.

For a caller-funded call, `endpoint_call` also requires the invoking thread to
be the scheduling context's exact current `active_thread` (the home thread for
an outer call or the current donated server for a nested call). It atomically
blocks that thread and places the exclusive context binding in
`PENDING_DONATION(prior_binding, blocked_thread_generation, call_id)`; mere
possession of `SchedulingContext.Donate` by a sibling cannot donate or steal a
context on which another thread is active. The `CallRecord` stores that exact
thread, context, binding generation, home thread, and prior call-chain
identity. Every pre-accept terminal transition revalidates the exact prior
frame before restoring it. For `prior=BOUND`, a live exact home thread with an
unchanged binding and open execution gates returns to `BOUND` and `READY`; it
needs no caller-funded parent tag. For `prior=DONATED`, the exact previous
server must still carry the recorded parent `ACTIVE` tag before the popped
donation and `READY` state can be restored. If either valid predecessor is
administratively suspended, the binding is restored and its protected saved
state becomes `READY` without dispatch. A donated predecessor in
`ABORT_PENDING` or `REPLY_DRAINING` instead receives the returned binding
directly into parent failure/success drainage without dispatch. A terminal
predecessor or closing domain continues the ordinary unwind and may leave an
outermost context `UNBOUND` rather than rebinding it to a dead thread.

Acceptance atomically revalidates every origin gate and endpoint generation.
For caller funding it also revalidates the exact recorded caller/active-thread,
home-thread, scheduling-context binding generation, call-chain, and
`PENDING_DONATION` state; for server funding it verifies the caller's wait and
that no incoming donation reservation exists. It then checks the immutable
funding mode, receiver state, passive-admission reservation, referenced abort-policy
`OPEN` state/generation and, for thread-local abort, the selected receiver's
exact immutable cancellation-profile binding, all capability-transfer
reservations, and any donation binding. In the same commit
it installs the policy pin, changes the call record to `ACCEPTED`, commits the
transport and capability-transfer facts, activates a preallocated
`ReplyToken`, and publishes the funding-mode-specific `READY` state and (only
for caller funding) the `ACTIVE(call_id)` tag and donation binding. The token
contains:

- caller, exact accepted receiver thread, receiver domain, endpoint, and all
  relevant object generations;
- the funding mode, an optional donation binding, and call-chain depth;
- a bounded request identifier and deadline;
- the current outcome state; and
- any call-scoped borrowed capability facets.

The baseline reply facet is non-copyable and non-transferable, and every
baseline `Reply` checks that the invoking thread is the recorded receiver
generation. A caller-funded reply additionally checks that the receiver is
still bound to this call's donated context and carries `ACTIVE(call_id)`;
reply selection atomically changes that same thread to
`REPLY_DRAINING`/`PARKING_RECEIVE` or its terminal path. A sibling sharing the
capability table cannot reply while the accepted handler continues or cause
another handler's donation to return. Server-funded delegation, if later
needed, uses a distinct explicitly transferable reply facet with no incoming
donation and separately modeled handler ownership; it is not the baseline
`ReplyToken` behavior.

The optional binding is present exactly for a caller-funded acceptance and
absent for a server-funded acceptance. Absence is a first-class state, not a
null value that a common return path may interpret as a context: acceptance and
drainage of that server-funded call never treat the server's scheduling
context as an incoming donation or return it to the outer caller. A nested
caller-funded call may independently donate that same server-owned context;
its own reply token and drainage unwind the binding back to the server home
thread, or to `UNBOUND` if that thread became terminal.

Acceptance, outcome selection, and resource drainage are separate transitions:

```text
PENDING --accept wins--> ACCEPTED
PENDING --pre-accept cancellation wins-->
  DRAINING_PREACCEPT(CANCELLED_BEFORE_ACCEPT) -> CANCELLED_BEFORE_ACCEPT
PENDING --deadline wins-->
  DRAINING_PREACCEPT(TIMED_OUT_BEFORE_ACCEPT) -> TIMED_OUT_BEFORE_ACCEPT
PENDING --caller death wins-->
  DRAINING_PREACCEPT(CALLER_DIED_BEFORE_ACCEPT) -> CALLER_DIED_BEFORE_ACCEPT
PENDING --origin call-anchor close wins-->
  DRAINING_PREACCEPT(ORIGIN_CLOSED_BEFORE_ACCEPT) -> ORIGIN_CLOSED_BEFORE_ACCEPT
PENDING --parent call-anchor close wins-->
  DRAINING_PREACCEPT(PARENT_CALL_CLOSED_BEFORE_ACCEPT) -> PARENT_CALL_CLOSED_BEFORE_ACCEPT
PENDING --passive admission or abort-policy close wins-->
  DRAINING_PREACCEPT(PASSIVE_AUTHORITY_CLOSED_BEFORE_ACCEPT)
    -> PASSIVE_AUTHORITY_CLOSED_BEFORE_ACCEPT
PENDING --endpoint close wins-->
  DRAINING_PREACCEPT(ENDPOINT_CLOSED_BEFORE_ACCEPT) -> ENDPOINT_CLOSED_BEFORE_ACCEPT

ACCEPTED --reply wins--> REPLY_COMMITTED --> DRAINING_SUCCESS --> REPLIED
ACCEPTED --cancel wins--> DRAINING_FAILURE(CANCELLED) -----------> CANCELLED
ACCEPTED --timeout wins--> DRAINING_FAILURE(TIMED_OUT) ----------> TIMED_OUT
ACCEPTED --caller death wins--> DRAINING_FAILURE(CALLER_DIED) ---> CALLER_DIED
ACCEPTED --callee death wins--> DRAINING_FAILURE(CALLEE_DIED) ---> CALLEE_DIED
ACCEPTED --endpoint close wins--> DRAINING_FAILURE(ENDPOINT_REVOKED) --> ENDPOINT_REVOKED
```

Before a pre-accept terminal state is published, `DRAINING_PREACCEPT(reason)`
atomically unlinks the endpoint waiter and deadline, returns payload,
capability-slot, and accounting reservations exactly once, and only then wakes
any surviving observer. The seven resulting states all mean `NotAccepted`: no
reply token or donation was created and this invocation did not cross endpoint
acceptance.
Exactly one post-accept reply-or-failure outcome wins at its declared
linearization point, but selecting either path is not yet resource completion.
`REPLY_COMMITTED` invalidates further reply/cancel selection, publishes closure
of the call-lifetime anchor, and drains nested work and borrowed facets. For a
caller-funded call, it additionally waits until no callee or nested call can
execute on the optional donation binding and returns the still-existing
scheduling context to its prior owner exactly once. For a server-funded call,
there is no incoming-donation facet to return to the outer caller. Independently
recorded nested donations still unwind under their own records before the
applicable outer obligations finish. Only then does the record reach `REPLIED`
and wake the caller with `ReplyReceived`.

A winning post-accept failure follows the same funding-mode distinction. In a
server-funded call, closing the reply token and call-lifetime anchor prevents
new call-scoped work, admitted operations and nested calls drain in dependency
order, and any nested outgoing donation returns to the server's context lineage
rather than to the outer caller. A still-live handler may continue on its
server-owned context and will observe failure from invalidated nested
operations or from a late reply. If callee termination or domain stop won, its
terminal lifecycle—not call drainage—unbinds or reclaims that context, and no
handler continues. In either case the caller receives
`AcceptedNoReply(reason)`, never a claim that application effects were rolled
back or that the server stopped.

In a caller-funded passive call, the binding cannot be returned while the
callee might execute on it. Failure selection therefore first publishes its
`ABORT_PENDING` no-entry gate while atomically closing the reply token and
call-lifetime anchor. It prevents new nested work, brings the callee to a safe
scheduling/kernel checkpoint, drains nested bindings and admitted operations,
and only then returns the donated context. If the authorized policy is
thread-local and the callee remains nonterminal, it is published as
`CALL_ABORTED(call_id, reason, saved_state, unbound)`: it
cannot resume the middle of the handler, park itself implicitly, or accept
another call. If thread termination or domain stop won, the callee remains in
that terminal lifecycle and the same terminal drainage performs the one
donation return; failure handling never rewrites it to `CALL_ABORTED`. The
profiled branch permits a supervisor to inspect, terminally reap, and replace
that isolated worker. Generic domain-fatal policy instead starts `CLOSING` at
failure selection and replaces the whole domain. This cost is intentional:
arbitrary mid-handler continuation is not a valid failure boundary.

When present, the reply token owns a **donation binding**, not the scheduling
context itself. It never destroys a caller-owned scheduling context merely
because the token was replied, cancelled, or revoked. Common drainage code
must branch on the recorded funding mode, so an absent binding cannot trigger
a fictitious return and a server-owned context cannot be mistaken for a
donation.

### Capability carriage and commit

The initial call ABI permits at most one request-direction capability
descriptor and requires it to declare exactly one mode:

- **permanent copy** retains the source and installs an equal-or-attenuated
  capability in the reserved receiver slot;
- **permanent move** atomically removes the exact source slot generation and
  installs that capability in the reserved receiver slot; or
- **borrow** installs only an attenuated, non-transferable facet derived below
  the call-lifetime anchor.

Acceptance is the commit point for all three. It atomically revalidates the
source capability and lineage, delegation right, source/destination slot
generations, receiver quota, origin call gate, endpoint generation, and
funding mode. A pre-accept failure leaves a move source untouched, installs no
destination, and returns every reservation. Once acceptance commits, a
permanent copy or move is an admitted effect: it survives
`AcceptedNoReply(reason)` and is later removed only by ordinary capability or
receiver-domain teardown. Cancellation never tries to reconstruct the old
source slot. A borrow instead closes with the call anchor, and all of its
descendants and admitted uses must drain before terminal call completion.

Replies in the first profile carry bounded data but no capability. A later
reply-capability extension must pre-reserve a caller destination and define a
separate receiver-owned session lifetime; reusing the just-closed call anchor
would make a borrowed reply invalid on arrival. An untagged “capability
transfer” that leaves copy, move, borrow, or commit timing implicit is not a
valid ABI request.

Borrowed capability facets are non-transferable, every capability descendant
is derived beneath a call-lifetime `RevocationAnchor`, and every kernel object
created with the facet inherits that anchor as a product dependency. Both
reply and failure selection publish closure of the anchor before bounded
descendant/product traversal and type-specific mapping or binding teardown.
A cancellation request returns a progress state while draining; a surviving
waiter receives a terminal typed result only when the promised resource-return
conditions hold. A late reply using the closed token or old generation then
fails without changing current kernel state.

Server death or endpoint revocation must not leave callers asleep forever.
Cancellation also cannot assume the service did nothing: if the request
crossed the endpoint before failure, the kernel reports `AcceptedNoReply` until
an end-to-end protocol supplies stronger evidence.

`endpoint_close` is the object-specific logical-close operation. Its
linearization is one constant-work `CLOSED(endpoint_epoch)` publication. It
rejects later admissions and competes with acceptance, reply, and cancellation;
pending records now select `ENDPOINT_CLOSED_BEFORE_ACCEPT` when visited.
Charged drainage slices unlink `PARKED_RECEIVE` waiters and move each thread to
`RECEIVE_CLOSED(endpoint_epoch, unbound)`, releasing its endpoint reference
without inventing a scheduling context. A `PARKING_RECEIVE` observes the closed
epoch as `close_pending`; its reserved waiter is unlinked in a slice, but final
`RECEIVE_CLOSED(..., unbound)` publication waits for in-kernel drainage and
donation return. Close versus acceptance still has one order:
if close wins, no reply token or donation exists; if acceptance wins, the call
uses its normal post-accept failure path. It returns bounded drainage progress
until call waiters, receiver references, reply tokens, any present
donation bindings, and call-lifetime anchors reach their terminal states; only
then can `object_destroy` reclaim the endpoint's backing object.

A server-funded receiver blocked in `endpoint_receive` is a different branch.
A close-drain slice unlinks its receive reference and, if its thread/domain
lifecycle remains live, makes it `READY(ReceiveClosed)` on the same server-owned
scheduling context. It becomes `RUNNABLE` only when that context has budget and
thread/domain execution admission is open; a suspension overlay preserves the
event without dispatch. If terminal lifecycle won, it joins that teardown
instead. Endpoint close never unbinds, returns, or relabels this context as a
donation.

A persistent passive server enters its first wait with
`endpoint_park_receive`: while running on an initialization context, the kernel
atomically records the receive wait, unbinds/returns that context, and blocks
the thread without returning to user mode. After handling a call,
`reply_and_receive` atomically selects the reply and reserves the same thread's
next receive slot, changes `ACTIVE(call_id)` to
`REPLY_DRAINING(call_id)`, then enters `PARKING_RECEIVE` while it drains
call-scoped state and returns the donated context home. Only after that work
does it clear the active-call tag and publish the unbound `PARKED_RECEIVE` and
receive eligibility. The thread runs again only when a compatible later
donation is accepted.
Reply, park, and endpoint close share an endpoint-epoch ordering. If close wins
the accepted call's reply race first, the passive failure path publishes
`ABORT_PENDING` and takes its configured thread-local or domain-fatal branch.
If reply commits first but close prevents or later removes the park, reply
drainage marks `close_pending`, returns the donation, and only then makes the
now-between-handlers thread `RECEIVE_CLOSED`, with no stale receive reference.
Thus a close after any
successful `reply_and_receive` also resolves the unbound parked thread.
`reply_and_terminate` provides the corresponding successful one-shot terminal
path. Both terminal operations require the exact receiver thread generation
recorded at acceptance. Plain `reply_send` may return to the exact
server-funded handler, but is rejected
for a caller-funded passive handler because returning the donation would leave
that thread executing without a context. None of these success paths applies
after a failure winner: the passive thread enters `ABORT_PENDING` and then
either profiled `CALL_ABORTED` or domain terminal state. These terminal syscalls
avoid requiring an unbound thread to
execute `endpoint_receive`, resuming an interrupted handler, or giving one
thread two contexts.

### Bounded call chains

The kernel should impose and charge limits on:

- nested synchronous call depth;
- outstanding calls per domain and endpoint;
- blocked threads;
- call-record and reply-token objects;
- transferred capabilities; and
- cancellation work per system call.

For caller-funded endpoints those limits also include accepted aborts per
`PassiveCallAdmission`, endpoint-wide outstanding handler-recovery credits, and
the dedicated cleanup budget. Concurrency bounds alone are insufficient
because a hostile client can otherwise consume workers sequentially.

Each domain-fatal `PassiveAbortPolicy` is also an explicit conditional
failure-propagation edge from caller/session to callee domain: caller cancel,
death, or deadline can stop the callee, whose teardown can fail other calls.
The endpoint generation's `Close` authority lineage and automatic owner-
lifetime closure are additional trigger nodes because an accepted
`ENDPOINT_REVOKED` outcome takes the same passive abort path. The endpoint's
precommitted close reserve, not an arbitrary later holder's solvency, funds
that branch. Delegating `Endpoint.Close` changes who can reach the existing
trigger and must remain visible in the authority graph; it cannot erase the
edge, payer, or bound policy set.

The boot/configuration audit must expose all of these edges, bound path depth
and total reserved recovery work, reject an unacknowledged cycle or collapse
its strongly connected component into one declared recovery group, and report
blast radius. Kernel credits bound work but do not promise that a permitted
cascade is available. Server-funded IPC breaks the caller-triggered edge and
is the default across mutually untrusted reusable services. This authority is
closer to an explicit failure link than to ordinary BEAM message send.

It must not preserve nested calls by retaining an unbounded privileged stack.
The call graph should be represented as bounded objects so teardown can walk it
incrementally and detect cycles or excessive depth.

### Notifications and asynchronous data

A `Notification` is a bitwise coalescing doorbell. Multiple signals may become
one observed bit. It is suitable for “work may be available,” timeout, and IRQ
notification, not for lossless records.

Bulk and asynchronous traffic should use a bounded shared-memory ring plus a
notification. The ring protocol, not the kernel, expresses:

- capacity and credits;
- buffer ownership and transfer;
- producer/consumer ordering;
- cancellation and reset epochs;
- drop, retry, and backpressure behavior; and
- integrity checks for mutually distrustful peers.

The [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) ownership model is a
useful foundation for these rings. Cross-core service paths should initially
prefer per-direction rings and doorbells rather than assuming a universally
cheap cross-core rendezvous; the [Multikernel](../30-sources/baumann-et-al-2009-multikernel.md)
work motivates making such communication explicit.

### Operation outcomes

The kernel can state transport facts, not arbitrary service or physical-world
facts. A recoverable invocation should first preserve this classification:

- `NotAccepted`: endpoint acceptance did not occur, so this invocation could
  not have caused an effect through that call;
- `ReplyReceived(result)`: the target returned a protocol response; whether the
  response proves an external effect depends on the target's trust and protocol;
- `AcceptedNoReply(token)`: the target accepted the request but no valid reply
  survived, so downstream effects remain unknown; and
- `MechanismRejected(reason)`: capability, quota, lifecycle, or mapping checks
  rejected the operation before the stated mechanism transition.

An end-to-end service protocol may refine `AcceptedNoReply` to
`FailedBeforeEffect`, `Completed`, or `Indeterminate` only when a durable log,
device status, transaction record, or other trusted evidence supports the
claim. Exactly-once effects require durable intent, idempotency keys,
deduplication, transactions, or reconciliation with the device or remote peer.
The kernel cannot manufacture exactly-once semantics from IPC delivery alone.

## Component 5: scheduling contexts and temporal authority

Spatial capabilities do not prevent a domain from consuming all CPU time.
The kernel should make CPU budget a first-class, delegable object following the
[scheduling-context capability](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)
model.

A `SchedulingContext` should contain at least:

```text
{
    home_core_or_affinity,
    budget,
    period,
    refill_capacity,
    refill_entries[refill_capacity],
    refill_count,
    consumed_time,
    priority_ceiling,
    timeout_route,
    generation
}
```

Binding state and budget availability are separate state machines. The initial
binding contract is deliberately restrictive:

```text
UNBOUND --bind--> BOUND(home_thread, active_thread=home_thread)
BOUND --caller invokes pending call-->
  PENDING_DONATION(prior=BOUND, blocked_caller, call_id)
DONATED --active server invokes nested pending call-->
  PENDING_DONATION(prior=DONATED, blocked_caller, call_id)
PENDING_DONATION --pre-accept terminal--> revalidate prior frame
  prior BOUND + exact live/open home -> BOUND + READY(NotAccepted)
  prior DONATED + matching parent ACTIVE + live/open predecessor
    -> popped DONATED binding + READY(NotAccepted)
  valid suspended predecessor (prior BOUND, or DONATED + parent ACTIVE)
    -> restore binding + saved READY, no dispatch
  parent ABORT_PENDING | REPLY_DRAINING -> popped binding to drainage, no dispatch
  terminal predecessor | closing domain -> predecessor unwind or UNBOUND
PENDING_DONATION --accept-->
  DONATED(home_thread, extended_chain, accepted_receiver)
DONATED(depth > 1) --inner drainage--> revalidate previous frame
  matching parent ACTIVE + live/open previous server
    -> DONATED(home_thread, popped_chain, previous_server) + predecessor READY
  matching parent ACTIVE + valid suspended previous server
    -> popped DONATED binding + saved READY, no dispatch
  parent ABORT_PENDING | REPLY_DRAINING
    -> popped binding to parent drainage, no dispatch
  terminal predecessor | closing domain -> continue unwind
DONATED(depth = 1) --outer drainage--> revalidate home frame
  live/open home -> BOUND(home_thread, active_thread=home_thread) + home READY
  valid suspended home -> BOUND + saved READY, no dispatch
  terminal home | closing domain -> UNBOUND
BOUND --unbind--> UNBOUND

budget: AVAILABLE <-> EXHAUSTED
```

Exactly one thread is active on a scheduling context, while
`PENDING_DONATION` names one exact blocked predecessor and permits no execution
or competing donation on that binding. Bind, reserve, donate, nested donate,
return, and unbind are linearizable; donation is authorized by the invoking
active thread, the context's `Donate` right, and endpoint acceptance, not by
copying the context.
Every return revalidates the exact predecessor thread generation, parent call
tag, suspension overlay, and domain lifecycle. An `ACTIVE`, open predecessor is
made ready; a suspended one receives the same readiness only in saved state;
an `ABORT_PENDING` or `REPLY_DRAINING` parent receives the popped binding in
its drainage without user dispatch. If a previous server is terminal or its
domain closing, unwinding continues to the next frame. If the home thread is
terminal, the context becomes `UNBOUND` under its surviving owner/account
authority rather than binding CPU authority to a dead thread.
Changing budget, period, priority ceiling, or affinity initially requires both
`Manage` authority for an `UNBOUND` context and a `SchedulingControl`
capability whose conserved CPU-time and priority envelope includes the new
configuration. Configuration races with bind or donation therefore select one
transition rather than changing a live call chain.

Refill storage is caller-funded and fixed-capacity. Configuration and run/call
admission reserve every refill entry the selected sporadic/periodic policy may
need before consuming budget. Eligible adjacent entries may be merged only by
a rule that preserves total budget and eligibility time; if no such merge or
reserved slot exists, the operation is rejected before admission or the
context remains `EXHAUSTED` until an existing refill matures. The kernel never
allocates an overflow node, silently drops debt/credit, or walks an unbounded
refill list.

A thread is runnable only while bound to a context with budget. A passive
server can execute on the caller's donated context during a synchronous call,
so service work is charged to the initiating workload instead of a server or
supervisor reserve. In the baseline, the accepting passive-server thread must
have no context bound. Acceptance atomically binds the donated context to that
thread; inner donation moves the same exclusive binding; draining the outermost
call makes the server thread unbound and returns the context to its home thread.
An active server thread with its own context cannot simultaneously accept a
donation; it needs a distinct passive receive thread. Donation is bounded by
call depth, follows the reply token, and is returned exactly once only when
reply completes or cancellation has reached its drained terminal state.
Cancellation of an accepted passive call publishes `ABORT_PENDING`; only a
trusted worker profile may finish in unbound, non-resumable `CALL_ABORTED`,
while the generic policy stops the domain. Successful persistence requires the
atomic `reply_and_receive` path rather than implicit reuse of a saved handler.

Budget exhaustion generates a typed timeout fault or notification; it does not
make the kernel decide whether to kill, throttle, replenish, or restart the
domain. Scheduling-control capabilities limit which budgets, affinities, and
priorities a user scheduler may configure. Conserved or admission-checked
aggregate CPU utilization prevents a delegated scheduler from manufacturing
more budget than it received; a maximum-controlled-priority rule additionally
prevents it from outranking its delegated ceiling. Priority restriction is not
a substitute for budget conservation.

Budget exhaustion cannot asynchronously cancel privileged code. Before an ABI
operation crosses its linearization point, entry admission reserves from the
active context the declared maximum charge for its bounded non-preemptible
prefix, cleanup, and return path. Potentially larger work is split at explicit
lock-free preemption checkpoints. If the hardware timer expires inside an
admitted critical prefix, the kernel completes at most its declared overrun
allowance, records that time as debt against the same context, and permits no
further user execution on it until replenishment repays the debt. Exhaustion
notification is published at the safe checkpoint. Exceeding the configured
critical-section ceiling is a kernel timing-invariant failure, not permission
to consume an unbounded global reserve; the response is crash containment and
reset under the kernel failure model. These ceilings require target-specific
measurement and, for a claimed real-time profile, timing analysis.

### Recovery reserve

A supervisor that shares the exhausted child's scheduling context cannot
recover it. Each recovery tier therefore needs:

- an independently replenished scheduling context;
- precommitted memory and capability slots;
- independently reachable fatal-fault and escalation routes;
- a current recovery lease or independent recovery-control path;
- bounded teardown capacity; and
- any required device-manager or reset-domain authority.

These reserved resources must not be borrowed or delegated to the supervised
domain.
At least one recovery scheduling context and its fault/teardown reserve are
non-donatable and never delegated to a supervised child. A supervisor uses a
separate, bounded operational context for calls into that child. Repeated
requests from the child are admission- and rate-limited so they cannot consume
each replenishment of the recovery reserve indirectly. Recovery independence
is a kernel-enforced resource-topology property, not merely a supervisor-tree
convention.

### Charge privileged and interrupt work

Temporal isolation also needs an accounting rule for time spent inside the
kernel:

- a system call and its bounded validation work are charged to the active or
  donated scheduling context;
- endpoint service work follows the donated context through the call chain;
- the hard IRQ path is charged to a source-specific account or bounded system
  interrupt reserve, while deferred protocol work runs on the driver domain's
  context;
- ordinary fault containment first consumes a precommitted fault allowance for
  the failed domain, and continued teardown is charged to an authorized
  recovery account; and
- unavoidable architecture-fault and kernel-crash capture uses a small global
  emergency reserve that no unprivileged domain can allocate from.

Without these rules, a domain or device can evade its budget by causing
expensive system calls, page faults, interrupt storms, or revocation work. The
exact charge points and maximum exceptional cost remain prototype and timing-
analysis questions.

### Budget isolation is not time protection

Budgets bound processor consumption but do not eliminate timing channels
through caches, TLBs, predictors, interrupts, kernel data, or interconnects.
The [time-protection](../30-sources/ge-et-al-2019-time-protection.md) work shows
that a stronger security profile needs spatial partitioning or flushing,
interrupt isolation, and padding of variable cleanup time. Those mechanisms
depend on hardware and may reduce utilization.

The baseline therefore claims temporal resource isolation, not timing-channel
noninterference. A later high-security profile may request explicit partition,
flush, and padded-switch operations from the architecture layer and must state
which hardware channels remain uncontrolled.

## Component 6: memory mappings and architecture-resource bindings

### Address spaces and mappings

The kernel owns typed `AddressSpace` objects and validates mapping authority.
User-level memory managers choose layout and replacement policy. Mapping a
frame requires compatible authority over the address space and frame; rights
are the intersection of both authorities and architecture support.

A successful map creates a caller-funded `Mapping` object and returns its
capability. The protected object records the address-space identity, virtual
range, frame identity and offset, admitted frame-authority epoch, effective
rights, mapping generation, an immutable maximum-rights ceiling derived from
the original address-space and frame authorities, lifecycle, and current
completion epoch. `Protect` and every operation that could add or reactivate
CPU access revalidate the recorded frame-authority epoch; after quarantine
they fail immediately even if incremental traversal has not reached this
mapping. Recovery-scoped `Unmap` remains available so the old effect can be
removed. `Protect` also requires requested rights to fit both the immutable
ceiling and the attenuated ceiling on the presented `Mapping` capability; it
cannot manufacture write or execute authority after the original capabilities
disappear. Adding execute requires the lower code-publication protocol.
`Protect` and `Unmap` require this current mapping capability rather than only
`(address_space, virtual_address)`.
After unmap publication, a later map at the same virtual address creates a
distinct mapping identity; a delayed protect, unmap, or completion for the old
identity fails before touching the replacement.

Map, protect, and unmap operations return semantic completion rather than
merely reporting that a page-table entry was written. The lower architecture
layer supplies local and remote translation completion. The kernel associates
that completion with the mapping generation and teardown ledger. Execute
permission also requires the lower code-publication protocol.

The [least-privilege memory protection
model](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
warns that authority to configure translation and authority to access memory
must remain distinct across CPUs and devices. Page-table memory is a typed
kernel object, not a writable user frame that bypasses mapping checks.

### IRQ and timer bindings

Raw interrupt numbers and timer registers are not user APIs. An authorized
control service configures an accounted `IRQBinding` aggregate and receives
attenuated `InterruptSource`, `InterruptRoute`, or `InterruptBinding` views
over its source/route records; those views are not separately allocated
authority. Binding connects the typed source view to a notification and, where
required, a designated acknowledgement authority. The aggregate records source
generation, destination generation, trigger/flow semantics, CPU route, mask
state, teardown epoch, and an independently resourced device-management fault
route outside the ordinary driver subtree.

The hard interrupt path does bounded work: validate the binding generation,
mask or acknowledge according to the lower-layer flow contract, apply one
prevalidated debit to the kernel-owned hard-path account, execute its already
selected mask/quarantine transition if a threshold is crossed, set a
notification bit, publish the resulting counters, and return. The architecture
mechanism does not choose the budget, threshold, refill rule, or recovery
policy. Device-specific register access and protocol recovery occur in the
driver domain.

That path uses IRQ-safe atomics and preallocated per-CPU/source records, or a
locally masked nonblocking lock whose maximum acquisition/hold cost is part of
the target timing contract. It never waits on an ordinary endpoint, object,
lifecycle, or teardown lock and never spins behind an unbounded remote holder.
If detailed deferred state is full, it sets the sticky/coalesced condition and
returns. Binding teardown publishes a new epoch, lets deferred work drain, and
waits for every per-CPU reference before reclaiming the binding.

Each source also has a kernel-owned privileged hard-path account and rate
window. The minimal kernel owns its budget, threshold, refill schedule,
escalation choice, and the authority that can approve recovery. At admission it
passes the architecture fabric only a bounded debit-and-transition plan. A
threshold crossing under that plan automatically masks a maskable source,
coalesces a typed `InterruptStorm` event on the management route, and leaves a
sticky inspectable storm flag in the aggregate even if delivery is full.
Replenishment and re-enable require the manager's separate authority and any
`DeviceProfile` recovery preconditions; when that manager is replaceable or
the source belongs to a `ResetDomain`, the operation additionally validates
current `ResetLease.Use` or a narrow manager session beneath its closable epoch
anchor. Only after this policy-side validation does the architecture fabric
execute a preselected unmask/re-arm mechanism. The failed driver or a stale
manager cannot re-enable itself. The route, its bounded record, and the
manager's scheduling reserve are outside the driver lifetime/resource subtree.
A source that cannot be masked or isolated has a larger declared
reset/escalation boundary; repeated delivery can force device, CPU, or node
quarantine. Charging interrupts without an enforced threshold would let a
faulty device consume CPU outside the driver's scheduling context.

### Device and DMA authority

A driver receives only its `DeviceFunction` MMIO/configuration facets, IRQ
facets, `DmaAddressSpace`, queue leases, and frames. Reset is separate: an
exclusive function may receive a narrow reset facet, but authority over a
reset boundary shared by functions or drivers normally remains with a
supervisor/device manager. Ordinary drivers remain outside privilege. Nooks
showed that compatibility wrappers can recover from some driver failures, but
its [same-address-space protection](../30-sources/swift-et-al-2003-nooks.md)
was partial and kept extensions privileged. [MINIX
3](../30-sources/herder-et-al-2006-dependable-operating-system.md), [recovering
device drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md),
and [CuriOS](../30-sources/david-et-al-2008-curios.md) provide stronger
motivation for separate driver/service domains and explicit client-associated
state.

Direct MMIO facets respect the architecture's mapping granularity. If one
page exposes registers outside the delegated function/queue rights, that page
is not mapped writable; access is mediated by profile-limited
`device_config_read`/`device_config_write` operations or a trusted device
manager. Every replaceable-manager operation that can alter reset/profile
state—including IRQ mask/re-enable, mediated configuration, queue control,
DMA recovery, reset, quarantine, and completion attestation—also validates the
current `ResetLease.Use` or a purpose-specific session derived beneath its
closable epoch anchor. A nominal register-range capability cannot hide page-
level authority.

A reset-domain mutation requires both its scoped `Reset`/`Quarantine`
capability and the current `ResetLease(reset_domain, reset_epoch)`. The epoch is
independent of every `ProtectionDomain` recovery epoch. A reset-control facet
held outside all affected drivers uses a `ResetControl` escrow populated at
configuration from preexisting, attenuated `Reset`/`Quarantine`, affected
`DmaAddressSpace.Recover`, and completion-consumption authority
minted from an independent ancestor lineage whose anchor path excludes every
affected driver, ordinary supervisor, and replaceable manager. Copying a facet
from below an old manager's closable anchor is rejected because it would leave
the escrow semantically dead after takeover. Its
protected successor slots and manager resources also remain outside the old
manager. Takeover atomically closes a stale lease and the anchor for its
attestation/session facets, advances the reset-control epoch, and installs one
new sealed lease-use facet plus the escrowed scoped operation facets. It cannot
mint rights absent from the escrow. Consequently, the recovery holder for one
failed function cannot reset healthy siblings merely by presenting that
function's domain lease; it must request the independently fenced device
manager, whose profile enumerates every affected function and whose policy
coordinates their stop and reconciliation.

Lease takeover is only the logical manager fence. Any writable MMIO,
configuration, queue, doorbell, or ring alias held by the old manager remains
a possible admitted physical effect until it is closed. The immutable profile
must enumerate those aliases exactly as it does driver submission aliases.
Before the successor may issue a new reset, verify completion, re-enable an
interrupt, or release a frame, recovery must either terminally stop the old
manager with no resume path, or close every such mapping/facet and complete all
required remote TLB invalidations; already admitted mediated operations join
the immutable recovery ledger. If neither path completes, the reset domain
remains manager-fence-pending and escalates or stays quarantined. A direct
alias that is not profile-complete and revocable excludes the manager from the
recoverable isolation profile.

The `ResetDomain` serializes one protected operation state machine:

```text
control overlay:
CURRENT(e) --takeover/close mediated epoch-->
  CURRENT(e+1, MANAGER_FENCE_PENDING)
MANAGER_FENCE_PENDING --terminal old-manager stop or alias/TLB completion-->
  MANAGER_FENCED

operation state (new issue/verification/release requires MANAGER_FENCED):
IDLE -> REQUESTED(reset_operation_id, admitted_control_epoch, profile_generation)
     -> QUIESCING -> RESET_ISSUED -> COMPLETION_RECORDED -> VERIFYING
VERIFYING -> COMPLETE -> seal ledger, advance operation generation -> IDLE
REQUESTED | QUIESCING -> SAFELY_ABORTED_BEFORE_EFFECT
                       -> seal ledger, advance operation generation -> IDLE
QUIESCING | RESET_ISSUED | COMPLETION_RECORDED | VERIFYING
  -> RESET_FAILED_PINNED -> QUARANTINED
QUARANTINED --higher-boundary reset and complete reinitialization--> IDLE
```

Reset-control takeover does not erase or duplicate an admitted operation. It
immediately fences the old manager's later mediated admissions, records later
hardware completions against the immutable `reset_operation_id`, and lets the
new current lease adopt the ledger entry. It reports physical manager fencing
only after the profile's terminal-stop or direct-alias closure and translation-
completion barrier above.
Only `COMPLETE`, a profile-proved abort before any effect, or completed
higher-boundary reset can restore operational `IDLE`. `RESET_FAILED_PINNED`
retains mappings, buffers, and queue denial until it becomes a precisely scoped
`QUARANTINED` state or a higher boundary completes reset; `QUARANTINED` is
sticky and cannot silently reopen admission. No overlapping reset may enter
`REQUESTED` while such state remains. Manager attestations from the old control
epoch are invalid; lower-mechanism completions remain facts but must match the
operation, profile generation, affected object generations, and completion
epochs before the successor can verify them.

Every `DeviceFunction`, `DmaAddressSpace`, and `ResetDomain` names an
independently resourced device-management route and a fallback escalation route
at creation; related objects may share the same route when they share a reset
boundary. This covers polling devices and IOMMU/reset faults that have no IRQ
binding. Delivery overflow leaves a sticky typed fault on the originating
object and coalesces the fallback signal, so an authorized manager can inspect
the condition even if the ordinary driver and its notification path failed.

Creation of a `DmaAddressSpace` binds an immutable attachment-set generation
containing every hardware requester/function that the IOMMU can distinguish
only as one translation or isolation group, plus each compatible trusted
profile. A mapping makes its frame reachable by **every** requester in that
set. `DmaAddressSpace.Map` is therefore group authority: it may be delegated to
an individual driver only when the set is a single trust boundary, and mapping
admission validates compatible authority and rights for the complete set. Two
mutually distrustful drivers in an inseparable requester group cannot claim
direct-DMA isolation from each other; they need a trusted mediated/bounce-buffer
service or a larger shared failure boundary. A reset domain may be broader or
narrower for individual operations, but each DMA address space binds one
aggregate recovery/reset domain whose scope covers the complete attachment
set. Only that aggregate domain's current lease can authorize frame release
after it verifies every required constituent reset; a narrower function reset
cannot do so alone. The aggregate `ResetControl` escrow receives the
`DmaAddressSpace.Recover` and completion-consumption facets when the DMA space
is configured. The baseline has no live attach/detach operation: reassignment closes queues and the root,
quiesces every mapping/requester and IOTLB, destroys the old address space, and
creates a new root with a new attachment-set generation.

Creating a DMA mapping requires current, compatible capabilities for
`Frame.Dma`, group-scoped `DmaAddressSpace.Map`, and every profile/function in
the immutable attachment set; a raw physical address, frame number, or I/O
virtual address is never sufficient. The effective direction and access rights
are their intersection. Success returns a caller-funded `DmaMapping`
capability carrying the DMA-space, attachment-set generation, device-visible
range, frame, admitted frame-authority epoch, all profile/binding generations,
and completion epoch. Any operation that could add, redirect, or reactivate
device access revalidates that epoch and fails after frame quarantine;
recovery-scoped unmap/invalidate remains valid for removing the old effect.
The same atomic creation installs a protected mapping identity and attenuated
teardown entry in the DMA-space/reset recovery ledger outside the driver. Thus
driver capability-space destruction cannot strand unmap authority. A current
manager uses escrowed `DmaAddressSpace.Recover`, the current `ResetLease`, and
that ledger entry for bounded unmap/invalidate/completion work; it does not
depend on recovering the driver's `DmaMapping` capability.
Unmap and invalidate operate on that object, so a delayed operation or IOTLB
completion for an old mapping cannot alter a later mapping that reuses the same
device-visible address.

Unmap publication also reserves the old device-visible range and keeps its
frame pinned. No overlapping `DmaMapping` may reuse that IOVA until IOTLB
invalidation and the profile's device-quiescence/release evidence complete;
otherwise a stale device translation could target a new frame even though the
kernel object identity was safe. A hardware request-generation fence may
substitute only when the profile states and tests that stale requests are
rejected across every relevant device and IOMMU cache.

The kernel delegates protected I/O through the lower architecture layer. An
IOMMU mapping is necessary but not sufficient. [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md)
demonstrates that shared buffers, transition windows, and device behavior can
still violate isolation.

`DeviceQueueLease.Submit` and `.Doorbell` are enforceable only when submission
is a mediated kernel operation. A higher-performance direct ring or MMIO path
instead requires the `DeviceProfile` to classify every writable alias that can
submit work or reconfigure DMA: rings, doorbells, queue-base registers,
descriptor limits, enable bits, and relevant function configuration—not only
the nominal submission register. Those aliases are attenuated facets bound to
the queue/reset lease rather than an unrestricted function mapping. Queue
closure first publishes `CLOSED`, then either revokes every classified alias
from every holder and completes remote TLB invalidation, or proves that all
holders reached terminal `STOPPED` and cannot resume before those aliases are
removed. Resumable `ADMIN_SUSPENDED` alone is insufficient. Only then may the
plan claim that no later software submission or redirection is possible.
Posted writes and descriptors visible before that point remain admitted effects
and must drain or be quarantined. A polling device that can consume ring entries
without a doorbell requires the same write-alias closure; merely revoking a
capability selector does not stop user-memory or MMIO stores. Raw writable
submission/configuration paths not governed by mediated operations or a
profile-complete revocable alias set are excluded from the isolation profile.

There is no safe universal DMA teardown order. Each
function is therefore bound to an immutable `DeviceProfile` selected through
the trusted boot/hardware manifest. The profile identifies the device
class/version and supplies a finite kernel-checked quiescence state machine;
the untrusted driver can request transitions but cannot install, weaken, or
self-certify the plan. It names:

1. the linearization point after which new queue submissions and mappings are
   rejected;
2. whether interrupts are masked before drain, remain enabled to report drain
   completion, or are replaced by polling;
3. whether the queue can drain normally, needs a function-level reset, or
   shares a reset domain with other functions;
4. which buffers and IOMMU mappings must remain pinned until drain or reset
   completes;
5. when device fences, cache/DMA visibility operations, IOTLB invalidation,
   and interrupt drainage occur;
6. which trusted mechanism event or completion token proves that the device
   can no longer access the frames; and
7. which device, functions, mappings, and frames enter quarantine if any
   required transition cannot complete.

Some devices require mappings to stay present until reset/drain finishes;
others use early IOMMU removal to block further access and tolerate resulting
faults. The kernel executes only a declared legal plan and returns frames only
after its release point. Release requires a protected one-shot
`DeviceCompletionToken` naming the device-profile identity/generation,
reset-domain identity and control epoch, quiescence-operation identifier,
attachment-set generation, queue and `DmaMapping` identities/generations,
mapping completion epoch, and evidence class. Consumption presents the current
`ResetLease`, escrowed completion authority, and protected current recovery
ledger entries; every field must still match. It never depends on a mapping cap
stranded in a dead driver's table.

The lower architecture/IOMMU/reset mechanism can produce the underlying
completion record. If a separately identified trusted device manager must
interpret device status, it presents an attestation facet derived beneath the
current reset lease's anchor and the kernel mints the protected token; an
ordinary driver report or user-crafted tuple is never sufficient. Reset-control
takeover closes that facet and invalidates unconsumed manager attestations from
the old epoch. A late hardware completion remains a ledger fact for its original
operation, but the successor must adopt/revalidate it under its current lease
before memory release. If correctness depends on the manager, the manager and
profile are explicit assumptions for that reset domain. A device that can lie
about idleness, bypass its IOMMU, or lacks an enforceable stop/reset contract
must use permanently pinned or bounce-buffer memory, remain exclusively
assigned, be quarantined until platform reset, or be excluded from the
isolation profile.

Quarantine is a global `Frame` lifecycle state, not a tag in the failed
driver's ownership ledger. Publishing
`QUARANTINED(effect_id, custodian, scope)` atomically denies new CPU mappings,
new DMA mappings, and capability copy/transfer that would convey any mutating
frame right. The same transition closes the current protected frame-authority
epoch; every previously delegated `Map*`, `Dma`, `Reclaim`, or other mutating
facet permanently becomes stale and may at most inspect its historical
identity. Every old-epoch `Mapping` and `DmaMapping` rejects new access but
retains recovery-only teardown operations. Existing admitted mapping
records and pins survive under the teardown ledger so closure cannot erase an
old physical effect. The quarantine ledger enumerates every existing CPU and
device mapping regardless of payer or lifetime group. Recovery stops or
notifies all affected domains, removes every CPU alias incompatible with
quarantine and completes their TLB invalidations, while keeping device
mappings and frames pinned as required to confine the outstanding effect. If
an outside alias cannot be closed, the recovery group expands to its holder or
the failure escalates—`REAPED_WITH_QUARANTINE` is forbidden.

Only higher-boundary quiescence/reset plus current custodian authority may
release the global frame gate. Release requires every old-epoch CPU and DMA
mapping and every other physical access path to be closed, removed, and proved
quiescent; a surviving unquiesced mapping or effect keeps the frame and backing
pinned in `QUARANTINED` and forbids release. A historical tombstone may remain
only after the physical path has quiesced. Release never reopens the epoch that
existed before quarantine. After completion-ledger consumption and required
zeroing, the old `Frame` object is destroyed and its backing is explicitly
retyped as a new object generation; only current allocation/custodian
authority can mint its new mutating facets. Every old selector remains stale
even when its rights bits include `Reclaim`. Shared or client-owned status
never permits another principal to map a frame while stale DMA can still reach
it.

The kernel enforces authority and lifecycle. A user-level driver supervisor
knows whether device reset loses configuration, whether requests can be
replayed, and how clients should reconcile indeterminate operations.

## Component 7: fault capture and containment

### Fault taxonomy

One undifferentiated “process died” event is inadequate. The kernel should
normalize at least:

| Class | Evidence status | Typical response owner |
| --- | --- | --- |
| Explicit termination | Definite after cross-core stop completes | Domain supervisor |
| Synchronous execution fault | Definite for the faulting thread; domain containment is definite only after a configured fatal stop completes | Runtime, pager, or supervisor |
| Page or protection fault | Definite event; potentially resolvable | Authorized pager or runtime |
| CPU-budget exhaustion | Definite budget event, not proof of semantic failure | Scheduler/supervisor |
| Heartbeat or deadline miss | Suspicion dependent on time and scheduling assumptions | Liveness monitor |
| IPC protocol or integrity fault | Definite detector observation; cause may remain uncertain | Endpoint owner/supervisor |
| Memory or kernel-object quota exhaustion | Definite resource event | Allocator/admission policy |
| IRQ, IOMMU, DMA, or device-reset fault | Definite mechanism report; containment may be incomplete | Driver supervisor/root recovery |
| Kernel invariant or fatal architecture fault | System-wide TCB failure | Crash capture and reset |

The distinction between proof and suspicion follows [Chandra and
Toueg](../30-sources/chandra-toueg-1996-failure-detectors.md): timeout accuracy
depends on timing assumptions. A local heartbeat can still be delayed by CPU
starvation, interrupt loss, or a failed clock. Reserved supervisor budgets and
monotonic-time guarantees improve the detector; they do not turn suspicion
into proof.

### Bounded fault record

A fixed-size fault record should include:

- kernel domain and thread object identities;
- class, subtype, detector, and proof-versus-suspicion flag;
- fault address, access type, and architecture-normalized reason when relevant;
- bounded register/context digest, with extended state gated by
  `DebugAuthority`;
- monotonic timestamp and current budget/deadline state;
- current endpoint, reply, or operation token;
- lifecycle state reached by containment; and
- explicit truncation, coalescing, or evidence-loss flags.

Fault routing is typed rather than one universal handler:

- a pager or runtime resolver receives a one-shot token for a declared class
  of resolvable thread fault and may perform only its permitted mapping,
  register, `Resolve`, or `Resume` operation; exact-thread termination is
  available only on a separately minted `TerminateThread` facet and a matching
  manifest-declared isolated/reconstructible thread profile. Shared-state ERTS,
  JIT, NIF, and generic native-thread faults default to domain-fatal. The token is
  bound to the exact thread, fault epoch, address/range, and permitted state
  change. For a mapping repair, token creation captures an attenuated one-shot
  `FaultMap` grant and the target address-space/domain lifetime anchors;
  resolution consumes the token envelope, requires compatible current frame
  authority, and installs those captured anchors plus the frame lineage on the
  resulting `Mapping` rather than making it depend on the already consumed
  token identity;
- a timeout route receives budget events and can act only through separately
  held scheduling-control authority;
- a device-management route receives sticky IRQ-storm, IOMMU, DMA, and reset
  failures and is backed by resources outside the affected driver; acting on
  them still requires the relevant binding, profile, or reset-domain authority;
- a fatal lifecycle route notifies the current recovery-lease holder, while
  suspension, termination, and reaping still require the matching domain and
  recovery-epoch authority; and
- diagnostic observers receive nonblocking, bounded, redacted copies and
  cannot resolve, resume, or delay containment.

Each domain configuration names an explicit fallback/escalation endpoint
capability outside the child's subtree; the kernel assumes no parent/child
supervision relation. If a resolvable route is absent or full, the affected
thread remains `FAULT_BLOCKED`, a sticky unresolved-fault flag is recorded on
the thread/domain, and a coalesced event goes to that independently resourced
fallback route. If a fatal or device-management route fails, the domain or
device object likewise retains its typed sticky fault while the fallback is
signalled. Route capacity exhaustion can lose per-event detail, which is
reported by an evidence-loss flag, but cannot silently clear the condition.
The kernel never resumes a faulted thread by default.

### Containment protocol

For a fault class configured as fatal to the domain, the kernel:

1. records the cause and atomically enters `CLOSING(stop_epoch)`, publishing
   the fixed domain-root authority closures, closing new domain execution
   admission, freezing membership, and dispatching stop requests without a
   per-object walk;
2. runs the bounded cross-core stop protocol, allowing in-kernel activations to
   commit or abort only at defined points;
3. captures bounded evidence before mutable state is reclaimed;
4. requests cancellation and drainage of outstanding invocations, preserving
   `AcceptedNoReply` where downstream effect is unknown;
5. delivers the fault record to the holder of the current recovery lease or
   the configured escalation route; and
6. waits for a correctly epoch-authorized unprivileged decision to inspect,
   advance reaping, construct a replacement, or escalate the node.

Choosing a fault class as domain-fatal is an irreversible configuration
decision for that occurrence: by this point `CLOSING` and terminal stop have
already selected termination, so the supervisor cannot resume the old domain
or “terminate it again.” A nonfatal fault or liveness suspicion uses the
resolvable-thread or administrative-suspension path when policy still needs a
resume-versus-terminate choice.

Kernel detection is intentionally separate from restart. The [microreboot
work](../30-sources/candea-et-al-2004-microreboot.md) supports fine-grained,
fast component replacement when state and dependencies are designed for it,
but it does not justify automatic restart of arbitrary stateful services.

## Component 8: failure boundaries and recovery topology

### Boundary hierarchy

The platform should support several nested but non-identical failure scopes:

1. **BEAM actor.** The managed runtime contains ordinary exceptions, links,
   monitors, and configured per-process heap-limit termination. Runtime
   allocator exhaustion, heap corruption, and unsafe native failure are not
   assumed actor-local.
2. **BEAM runtime instance / protection domain.** A runtime, JIT, native helper,
   or runtime-wide invariant failure can terminate the whole instance.
3. **Native service or driver domain.** Unsafe code and hardware protocol state
   are isolated from the managed runtime and other drivers.
4. **User-defined recovery group.** A supervisor may replace a related set of
   domains together, but the grouping is user-space policy.
5. **System partition or node.** Correlated kernel, hardware, loss of all
   independent root-recovery paths, or unreconcilable persistent-state failure
   requires reboot or external failover.
6. **Kernel and final recovery-control infrastructure.** Failure of this last
   trusted boundary remains system-wide under the baseline design. One
   ordinary root-supervisor incarnation is still a replaceable domain when an
   independent fenced recovery controller survives.

A security boundary, scheduling boundary, state-ownership boundary, restart
unit, and escalation unit need not coincide. For example, three driver domains
may share one controller reset boundary; a fault in one can require restarting
all three without granting them mutual memory authority.

### Recovery ownership

Each domain has one current `RecoveryLease(domain, recovery_epoch)` to avoid
competing state-changing actions. Inspection and diagnostic observers are
separate. Suspecting that the holder failed does not authorize a second holder.
At domain configuration, the creator must populate a `RecoveryEscrow` by
minting already held, attenuated `Domain.Suspend`, `Resume`, `Terminate`,
`Reap`, and manifest-specific replacement-resource facets from an independent
ancestor/root lineage into protected storage. The kernel rejects an escrow
facet whose bounded anchor path includes the child, current lease, or any
replaceable supervisor, because those closures would also invalidate the
escrow. The escrow reserves and charges the successor's destination slots.
Stable lifecycle facets remain in the escrow; expendable
memory, scheduling, registry, and state-repair sessions are issued beneath the
current lease anchor so takeover fences old copies. This transaction cannot
amplify the creator's authority.

An independent recovery-control authority must atomically close the old sealed
lease-use facet, close the revocation anchor beneath which its issued recovery
and session facets were derived, advance `recovery_epoch`, install one
replacement lease in its pre-reserved slot, and issue the escrowed attenuated
authority set to that successor. A lease without escrowed domain rights is
insufficient, and a domain right held by the old supervisor is insufficient
with a stale lease. Every
new supervisor-initiated suspend, resume, terminate, and reaping mutation checks
that epoch at admission; a resumed old supervisor receives
`StaleRecoveryEpoch`. An admitted operation gets an immutable `suspend_epoch`,
`stop_epoch`, or teardown-operation identity. CPU and kernel completions match
that operation identity and are recorded even if recovery ownership changes;
the successor uses its current lease to adopt or continue the ledger entry.
Recovery-lease turnover therefore cannot discard a valid late stop
acknowledgement, while the old supervisor still cannot initiate another
mutation. Shared device reset is separately fenced by its `ResetLease`, never
inferred from one domain's recovery lease.

The current recovery holder needs separately scoped capabilities to inspect
bounded state, terminate, advance teardown, create a replacement from a
manifest, and invoke the user-space publication service; takeover obtains these
only from the configured escrow and never from the failed supervisor's
capability table. It receives no implicit authority over unrelated siblings. A
`ReapToken` records progress but does not bypass recovery fencing: control of
it is atomically moved to, or revalidated by, the current recovery epoch before
work continues. A domain lacking an independently resourced controller,
escrow, and protected destination path is not recoverable after its supervisor
fails; its documented escalation boundary is a higher controller or node
reset.

Kernel fencing alone is insufficient. Every registry, state-repair service,
and device manager used by recovery must either validate the current live
`RecoveryLease(domain, recovery_epoch)` on each mutation or accept only a
session capability derived beneath that lease's now-closable anchor. Publication
uses an epoch-aware compare-and-swap over both the old logical-service epoch
and the current `(recovery_lease_object, recovery_epoch)` fencing token.
Takeover therefore rejects a later mutation from a resumed old supervisor;
operations admitted before takeover remain explicit
and must be reconciled. A durable store, remote peer, or physical device that
cannot validate fencing tokens, revoke its session, or provide idempotent
reconciliation is outside the recoverable boundary and may force external
failover. The kernel does not claim to revoke such an external effect.

There is no kernel-encoded parent/child supervision tree. User-space can
implement one-for-one, one-for-all, rest-for-one, escalation, retry intensity,
backoff, circuit breaking, or placement policy. The kernel enforces only that
the selected recovery authority is valid and independently resourced.

This keeps [Armstrong's supervision
principles](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
above the privileged boundary while strengthening their substrate: a failed
native service cannot corrupt its supervisor's memory or spend its reserved
CPU and object quota.

### State classes and restart safety

Before a service can be called restartable, its state must be classified:

| State class | Recovery rule |
| --- | --- |
| Ephemeral computation state | Discard with the old domain |
| Client-associated protected state | Keep in a narrow external object or reconstruct from the client; generation-check ownership |
| Durable transactional state | Recover through log/transaction semantics outside the kernel |
| Discardable cache | Invalidate and rebuild |
| Shared mutable state | Quiesce every writer or use a protocol that tolerates one writer's failure |
| External or irreversible state | Reconcile with the device, peer, or physical world; expose indeterminate outcomes |

[CuriOS](../30-sources/david-et-al-2008-curios.md) is useful evidence for
isolating client-associated service state so one service failure need not
destroy every client's recoverable state. EROS demonstrates that transparent
persistence can coexist with capabilities, but [persisting an entire object
world](../30-sources/shapiro-et-al-1999-eros.md) could also preserve corrupted
runtime state. This platform should keep persistence policy outside the
kernel and require explicit recovery formats.

### Replacement protocol

An unprivileged supervisor performs replacement as an explicit transaction:

1. receive and classify the fault or suspicion;
2. choose whether to wait, probe, freeze, terminate, degrade, or escalate;
3. advance the old domain through teardown and await `REAPED_CLEAN` or accept
   `REAPED_WITH_QUARANTINE` with recovery infrastructure taking custody of the
   quarantine set;
4. construct a new domain from a versioned manifest, not by copying the old
   capability table or failed heap;
5. restore only classified state through a protocol that validates the current
   recovery epoch or a session facet derived beneath it;
6. establish new endpoints and health checks;
7. use the registry's epoch-aware compare-and-swap
   `compare(old_service_epoch, old_domain_current_recovery_fence)` to install
   `(logical_service_id, new_service_epoch, domain_id_D', endpoint_to_D',
   D'_current_recovery_fence)`. The compared fence belongs to the failed
   incarnation; the installed lease object/epoch belongs to `D'`, and the two
   are never represented by one unlabeled field; and
8. let clients retry or reconcile according to the operation outcome.

Pending endpoint calls are not silently redirected to the replacement. A
client that looked up service epoch `e` must observe that `e` failed and decide
whether its request is safe to submit to a later epoch. The new kernel domain
identity `D'` and the service epoch are related by the registry record, not by
numeric equality.

### Root-supervisor failure

The kernel should expose a bounded, read-only ledger of live domains, resource
accounts, lifetime groups, recovery epochs, lifecycle states, and teardown
tokens to an authorized replacement root service. That permits a restarted
supervisor to reconcile kernel state. It does not preserve arbitrary
supervisor policy memory. An independently
bootstrappable recovery controller must first revoke the old root's recovery
leases and anchored recovery sessions, advance their epochs, and fence the
registry and recovery-service mutations before the replacement acts. It then
issues the new root only the attenuated lifecycle and replacement-resource
facets held in independent `RecoveryEscrow` objects, into pre-reserved slots;
it never depends on reading authority out of the failed root's table. Mere
suspicion never creates two roots. If an escrow, protected destination path, or
end-to-end fenced recovery service is unavailable, the next boundary is
controlled node reset and external orchestration.

## Component 9: teardown, revocation, and safe reclamation

Teardown is where capability correctness, failure containment, the architecture
contract, and driver recovery meet. The domain states are the single
authoritative lifecycle defined in Component 3; this component does not define
a competing `ACTIVE`-to-`DEAD` machine. Instead, the teardown ledger refines
the domain's `CLOSING`, `DRAINING`, `QUIESCENT`, sanitizing, and reaped states
with one product-state record per capability lineage, call, mapping, IRQ,
queue, DMA lease, frame, and owned object:

```text
OPEN -> CLOSED_PUBLISHED -> QUIESCING -> QUIESCENT -> SANITIZED_OR_RELEASED
                                  `----> QUARANTINED(custodian, reason, scope)
```

The domain may publish `REAPED_CLEAN` only when every reusable record reached
`SANITIZED_OR_RELEASED` and no quarantine record exists. It may publish
`REAPED_WITH_QUARANTINE` only when every reusable record is released and each
remaining record has a precise scope and an independently authorized
custodian. A never-started `DEFINED` domain still traverses its object and
capability records, but its execution-stop proof is the empty activation set.

### Required teardown order

1. Enter `CLOSING`. Publish logical closure of the complete fixed domain-root
   execution, relationship/lifetime-derivation, outbound-call, and session
   gate vector, freeze membership, create the stop
   epoch, and dispatch stop requests in the same bounded transition before any
   object traversal begins.
   Descendant capability lookup must check that shared anchor, so a capability
   delegated into another capability space cannot start a later operation.
2. If `STOPPED` was not already proved by the never-started empty-activation
   fast path, promptly enter the already dispatched `STOPPING` protocol and
   wait for `STOPPED`; no slot, call, or object walk may delay the stop IPIs.
   `STOP_FAILED` escalates; teardown cannot assume a non-acknowledging CPU
   stopped.
3. After `STOPPED`, select and advance type-specific invalidation for local
   slots, reply authority, and owned objects in charged slices. Retain every
   admitted-operation pin and every active mapping, IRQ, DMA, or call binding
   until its later completion step. Advance an object generation only when its
   safely quiesced backing storage is retyped or reused after destruction;
   closing domain `D` does not invent a generation for unrelated shared
   objects.
4. Request cancellation of blocked and active calls. Drain callees and nested
   calls to safe checkpoints, close call-lifetime descendants, and return
   donated scheduling bindings only after no execution can use them.
5. Unbind permanent scheduling contexts and account their remaining CPU time.
6. Close CPU mappings to be removed and start remote invalidation. Retain
   frames until every relevant CPU acknowledgement arrives.
7. Execute each IRQ/queue/DMA binding's declared device quiescence plan. For a
   direct queue, first terminally stop every holder without a resume path, or
   revoke and complete TLB invalidation for every device-consumed ring,
   doorbell, and DMA-reconfiguration alias identified by its profile; all
   aliases are removed before any later resume. The remaining dependency order
   determines interrupt masking or polling, queue drain, pinned mappings, reset, IOTLB
   invalidation, and buffer release.
8. Traverse and remove logically closed capability descendants, mappings,
   waiters, and bindings from active lookup/PTE/dispatch membership in bounded
   charged slices. Retain a charged tombstone/teardown record with identity,
   generation, completion epoch, pins, and expected acknowledgements; no record
   backing is freed while a late completion can still reference it.
9. Wait for every required TLB, IOTLB, interrupt, cross-core, call-drain, and
   device completion. Anything that cannot complete must be confined to an
   explicit quarantine set by the lower architecture/device contract. Each
   affected frame first enters the global deny-new-map/transfer/DMA state, and
   all incompatible CPU aliases are removed with completed TLB invalidation;
   otherwise quarantine is not a valid containment result.
10. Revoke every remaining non-device writable shared-ring alias before
    considering its frames for reuse; device-consumed aliases were prerequisites
    of step 7. The kernel records kernel calls and device tokens only; peers and
    service protocols reconcile user-space ring epochs, buffer ownership, and
    requests that existed solely in ring metadata.
11. After step 9 consumed every required completion, destroy tombstones and
    owned typed objects in dependency order. Shared or client-owned objects
    survive under their own lifetime groups. Zero confidential memory only
    after all access paths to that memory are quiescent.
12. Publish `REAPED_CLEAN` when all resources are quiescent and reclaimable, or
    `REAPED_WITH_QUARANTINE` only after recovery infrastructure has accepted
    custody of a precisely bounded device/frame/resource set that remains
    inaccessible to new principals.

Steps may proceed concurrently when their dependency graph allows. Only
`REAPED_CLEAN` is a barrier proving that every old effect relevant to the
returned resources stopped. `REAPED_WITH_QUARANTINE` proves containment and
custody transfer for the listed set, not that its underlying effect stopped.
If a running CPU or device effect cannot be bounded by quarantine, reaping does
not complete and recovery escalates to the node boundary.

### Bounded progress

Large capability trees, mappings, or waiter sets cannot be processed in one
uninterruptible system call. `reap(domain, budget)` performs at most a declared
amount of work and returns a `ReapToken` containing the phase, cursor, charged
account, remaining work estimate if known, and quarantine set. Repeating the
operation is idempotent. If the recovery service crashes, a successor can
resume without replaying completed destructive steps only after atomic
recovery-lease takeover and token revalidation at the new recovery epoch.

The kernel reserves enough metadata to complete teardown before admitting the
domain. Otherwise admission could create an object graph the system lacks
resources to revoke—a recovery form of overcommit.

### Publication versus quiescence

The lower architecture-layer research distinguishes publication from
completion. The minimal kernel carries that distinction upward:

- a mapping removal is *published* when no new lookup can acquire it;
- it is *quiescent* after every relevant CPU has completed invalidation;
- an IRQ binding is *closed* when no new delivery can be admitted;
- it is *quiescent* after controller and in-flight event epochs drain;
- a DMA lease is *revoked* when new submissions fail;
- its frames are *reusable* only after device and IOMMU quiescence.

If a device cannot be stopped or reset with the documented contract, its
reachable device/functions, mappings, and frames may be quarantined only when
the architecture layer can prove the effect is confined to that set. Otherwise
the failure escalates to CPU, partition, or node reset. In neither case may the
affected memory be optimistically reused for a new principal.

## Component 10: observability and crash evidence

Observability belongs in the kernel only where user space cannot reconstruct
state after a fault. The kernel should expose bounded snapshots of:

- object identity, type, lifecycle, lifetime-group membership, and resource
  charges as separate fields;
- capability-derivation counts and active revocation phase, subject to debug
  authority;
- domain members, CPU stop acknowledgements, and scheduling-context state;
- endpoint waiters, active reply-token outcome, and cancellation state;
- mapping, IRQ, timer, and DMA teardown epochs;
- fault records and evidence-loss flags; and
- boot manifest identity and declared architecture feature profile.

Tracing buffers are fixed-size and overwrite or coalesce under declared rules.
An observer cannot hold a kernel lock, block a faulting CPU, or force allocation
on an exceptional path. Sensitive register, address, capability-graph, and
cross-domain data requires `DebugAuthority` distinct from ordinary health
inspection.

For a kernel invariant failure, a preallocated crash capsule records the
minimum architecture state, last bounded events, boot and kernel identity, and
reason before reset. Continuing normal execution after corruption of the
reference monitor is outside the baseline failure model.

## System-call and ABI shape

The first ABI should expose object operations rather than a wide POSIX-like
surface. A representative—not final—set is:

```text
pool_split, object_create, object_close, object_destroy
resource_account_delegate, resource_account_move_charge, resource_account_inspect
lifetime_group_create, lifetime_group_close
anchor_create, anchor_close, cap_revoke_advance
cap_copy, cap_mint, cap_move, cap_delete, facet_close
domain_create, domain_configure, domain_start
domain_suspend, domain_resume, domain_terminate, domain_reap
recovery_escrow_create, recovery_escrow_deposit, recovery_control_install
recovery_control_takeover, recovery_lease_inspect
recovery_session_mint
thread_create, thread_configure, thread_start, thread_suspend, thread_resume
thread_terminate, thread_reap
frame_map, mapping_protect, mapping_unmap
frame_quarantine, frame_quarantine_advance, frame_retype
endpoint_call, endpoint_receive, endpoint_park_receive, endpoint_close
passive_abort_policy_create, passive_abort_policy_close
passive_admission_create, passive_admission_close
cancellation_profile_install
reply_send, reply_and_receive, reply_and_terminate, call_cancel
notification_signal, notification_wait
sched_create, sched_configure, sched_bind, sched_unbind
irq_bind, irq_mask, irq_acknowledge, irq_storm_replenish, irq_reenable
timer_arm, event_unbind
dma_space_create, dma_map, dma_unmap, dma_invalidate
dma_reap_advance
device_profile_bind, device_mmio_map, device_config_read, device_config_write
device_queue_bind, device_queue_submit, device_queue_doorbell, device_queue_stop
reset_control_install, reset_control_takeover, reset_request
reset_attestation_session_mint
device_completion_attest, device_completion_consume
fault_receive, fault_resolve
object_inspect, reap_advance
```

Each operation specifies:

- required capability types and rights;
- which inputs supply effect-bearing product lifetime, which are consumed
  guards, and whether any explicitly authorized durable detachment occurs;
- memory and CPU charge;
- whether it may block;
- maximum kernel work or returned progress token;
- linearization point;
- success postcondition;
- cancellation and concurrent-revocation result;
- stale-generation behavior;
- recovery-mode lease and policy-profile checks, where applicable;
- architecture completion required before return; and
- observable fault and audit record.

“Returns zero” is not a sufficient semantic contract for an operation with
remote or device-visible effects.

## Concurrency model

The kernel must not hide one global authority and lifecycle lock behind a
capability API. An initial implementation can use coarse locks while the
abstract model is stabilized, but the contract should permit:

- per-core run queues and scheduling state;
- read-mostly or partitioned capability lookup with serialized mutation of a
  table lineage;
- per-object lifecycle locks or compare-and-transition state;
- explicit cross-core messages for freeze, TLB completion, and cancellation;
- per-direction IPC rings for bulk cross-core traffic; and
- epoch-based completion for references held temporarily by CPUs.

Lock order must follow the object dependency graph. No kernel lock—including a
prototype big lock—may be held across an endpoint wait, scheduling block,
return to user code, cross-core acknowledgement, TLB/IOTLB completion, or
interrupt/device-progress wait. The kernel first pins charged references and
publishes an epoch/state transition, releases locks, waits, then reacquires and
revalidates the epoch before committing the next transition. No fault path
waits on a lock owned by the faulted user domain; user code never runs while a
kernel lock is held. Revocation and teardown do not wait synchronously for
arbitrary unprivileged cooperation. Lock-class order and permitted blocking
points belong in the executable model and lock-dependency tests.

Hard IRQ and IPI context is a separate nonblocking lock class. It may touch
only IRQ-safe atomic or per-CPU state, or bounded locally masked locks that
ordinary kernel paths cannot hold while interrupts are enabled. It never
acquires a general object/coarse lifecycle lock; deferred kernel work performs
those transitions and joins teardown through binding/CPU epochs.

The [big-lock microkernel
study](../30-sources/peters-et-al-2015-big-lock-microkernel.md) supports a
measured, conditional starting point: one lock can outperform more complex
locking on modest tightly coupled cores when kernel sections are short, while
pathological entry-heavy workloads still expose a scaling ceiling. The initial
lock strategy is therefore a hypothesis to benchmark under BEAM scheduling,
fault, IPC, and teardown loads, not a permanent architectural promise.

The [Hive](../30-sources/chapin-et-al-1995-hive.md) experience with fault
containment on shared-memory multiprocessors is a warning: hardware protection
regions do not eliminate shared-state corruption or correlated failure. The
kernel should minimize writable cross-domain shared memory, validate shared
protocols at boundaries, and record which resources create a larger correlated
failure region.

## BEAM and OTP compatibility

### Two levels of process and scheduling

A BEAM process remains a managed-runtime object with a small heap, mailbox,
signal queues, reductions, links, monitors, and process-local tracing garbage
collection. It is neither a kernel `Thread` nor a `ProtectionDomain`.
The pinned [Erlang/OTP 29 source-tree
audit](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) also shows that
these cheap language processes depend on shared runtime schedulers, allocators,
code, tables, ports, and native substrate state. The kernel boundary therefore
contains a compromised ERTS instance as a domain; it does not pretend that its
internal objects are mutually hardware-isolated.

A runtime domain contains many BEAM processes and a small number of
kernel-scheduled runtime threads. The kernel charges CPU execution time through
scheduling contexts; the runtime distributes that budget among actors using
reductions and its own scheduler rules. This preserves cheap actor creation and
message passing while preventing a whole runtime from starving drivers or its
supervisor.

[Scheduler activations](../30-sources/anderson-et-al-1992-scheduler-activations.md)
provide historical evidence for this many-to-few division: the kernel can
allocate processors and report blocking/preemption events while a runtime owns
fine-grained thread scheduling. Their expensive upcall path and reentrant
scheduler complexity warn against copying the interface unchanged; the useful
principle is the division of responsibility.

Automatic process-local tracing GC stays entirely in the unprivileged runtime.
The kernel maps and charges pages in batches; it does not inspect terms or
collect individual actor heaps. Shared-memory or external resources referenced
from BEAM terms require explicit lease objects and deterministic close paths;
garbage-collector finalization alone is not a security revocation guarantee.

### Actor authority

A BEAM PID is routing identity, not kernel authority. Kernel capability
selectors must never be serialized directly in the Erlang External Term Format
or treated as globally meaningful integers.

A `PassiveCallAdmission` with domain-fatal policy must likewise never be
presented as ordinary actor send authority: it conditionally authorizes a
runtime-domain stop. ERTS scheduler, dirty scheduler, JIT, and in-process NIF
threads use server-funded endpoints or a separate disposable service domain;
they do not opt into arbitrary thread-level passive cancellation. Any mapping
from OTP links to kernel failure-propagation policies is explicit system
configuration, not automatic PID semantics.

Within one trusted managed runtime, the runtime can enforce actor-specific
authority by storing opaque language-level references and mediating them
through a capability broker. The underlying kernel capability resides in the
runtime domain's protected capability space; the runtime records which actor
may request which operation. This protects actors from ordinary BEAM code but
does not protect them from a compromised runtime or unsafe native extension.
An in-process Erlang NIF necessarily shares the ERTS address space and joins
the runtime domain's failure and authority boundary; the kernel cannot move it
out-of-process while preserving ordinary NIF semantics. Where the declared
compatibility profile permits, privileged or untrusted native functionality
should instead be exposed as a port, separate service domain, or compatibility
shim over bounded endpoints. Where an in-process NIF is required, its authority
must be minimized and runtime-domain-wide failure accepted explicitly.

Across runtime domains, a gateway translates a language-level reference into a
specific attenuated endpoint facet. Transfer is explicit, bounded, and subject
to the receiver's quota. Revocation invalidates the gateway/session
generation; it does not search arbitrary serialized terms.

### Failure translation

The runtime handles ordinary actor failures using BEAM links, monitors, exit
signals, and OTP supervisors. Kernel involvement begins when the runtime
domain itself faults, exhausts a hard budget, violates a mapping, or loses a
native dependency.

An outer system supervisor then receives a domain fault record. It may start a
new runtime domain `D'` and publish a later logical-service epoch. BEAM
distribution or an application protocol reports broken connections and decides
which messages can be resent. The kernel must not fabricate actor exit reasons
for state it cannot observe or replay an old mailbox into a new runtime without
a declared durable protocol.

### Failure-boundary scenarios

| Scenario | Containment boundary | Required mechanism | Recovery policy location |
| --- | --- | --- | --- |
| One BEAM process raises an exception | Actor | Runtime process isolation, links/monitors, local tracing GC | OTP supervisor in runtime |
| One pure BEAM process loops | Actor | Runtime reduction pre-emption | Runtime scheduler/OTP policy |
| Native, dirty, or compromised runtime work fails to yield | Runtime domain | Runtime safeguards plus kernel scheduling-context budget | Outer supervisor if the runtime becomes unhealthy |
| Runtime allocator exhaustion or heap corruption | Runtime domain unless the runtime proves a narrower configured limit | Domain memory quota, fault record, stop and teardown | Outer system supervisor |
| Runtime JIT or native helper corrupts memory | Runtime domain | MMU isolation, domain freeze, fault record, teardown | Outer system supervisor |
| Driver dereferences invalid memory | Driver domain | Separate address/capability space, IRQ/DMA teardown | Driver supervisor |
| Driver dies after submitting I/O | Driver plus device recovery group | Indeterminate outcome, DMA/IRQ quiescence, device reset | Driver protocol and clients |
| Supervisor misses a heartbeat | Suspicion boundary | Reserved budget, monotonic timer, explicit suspicion record | Parent monitor policy |
| Kernel invariant fails | Node | Bounded crash capsule, reset | Boot recovery/external orchestrator |

## Assurance strategy

Formal verification results do not transfer by architectural resemblance.
[seL4's comprehensive verification](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
and [information-flow proof](../30-sources/murray-et-al-2013-sel4-information-flow.md)
show both what is possible and how important the assumptions, configuration,
compiler, architecture, DMA, and timing boundaries are. [CertiKOS](../30-sources/gu-et-al-2016-certikos.md)
provides a complementary layered-refinement method. [Rushby's separation
kernel](../30-sources/rushby-1981-design-verification-secure-systems.md)
work motivates an explicit abstract machine and information-flow policy rather
than testing implementation behavior alone.

Assurance should proceed through distinct claims:

1. **Functional refinement:** each ABI operation implements its abstract state
   transition.
2. **Memory and type safety:** kernel code cannot violate object bounds or use
   the wrong object type.
3. **Authority confinement:** capabilities are unforgeable and derivation never
   amplifies rights.
4. **Integrity and confidentiality:** one configured domain cannot modify or
   read another except through authorized flows.
5. **Availability and bounded work:** a domain cannot create unbounded kernel
   work or consume another domain's reserved resources.
6. **Temporal isolation:** scheduling contexts enforce declared CPU budgets.
7. **Teardown safety:** no object or frame is reused before all old CPU and
   device effects are quiescent.
8. **Configuration correctness:** the boot manifest and supervisor authority
   graph actually satisfy the intended policy.
9. **Time protection:** only for a separately declared hardware/profile model,
   never inferred from budget enforcement.

[Binary-level timing analysis of
seL4](../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)
shows that boundedness is itself an assurance claim. Kernel configuration,
permitted calls, executable paths, cache/pipeline model, and target processor
all affect a safe response-time bound. The study also found lifecycle paths
that needed preemption points. This supports incremental revocation and reaping
but does not transfer its numerical bounds to this kernel.

### Executable models before kernel code

Model the following in TLA+, Alloy, Lean, Isabelle/HOL, or another appropriate
tool before optimizing implementation paths:

- capability derivation, effect-bearing product lineage, consumed guards,
  explicitly authorized durable detachment, atomic anchor admission/closure,
  physical traversal, charge movement, and safe object-generation reuse;
- pending-call origin gates, finite `PassiveCallAdmission` credits,
  `PassiveAbortPolicy` scope, caller- versus server-funded atomic acceptance,
  exact-caller `PENDING_DONATION`, `READY`/`ACTIVE` publication,
  receiver-bound reply authority, `REPLY_DRAINING`, reply, success/failure
  drainage, timeout, peer-death, passive receive, `ABORT_PENDING`, generic
  domain-fatal versus profiled `CALL_ABORTED`, and endpoint-close races;
- nested scheduling-context donation, terminal predecessor unwinding, refill
  capacity, ready-before-dispatch budget checks, and exact release;
- thread/domain suspend, fixed-gate bounded SMP stop, termination, teardown,
  quarantine, and replacement;
- CPU and DMA mapping removal, frame-authority epochs, address-range reuse, and
  completion epochs;
- immutable DMA requester sets, IRQ closure, serialized reset operations,
  reset-manager mediated and direct-alias fencing, device attestations, late
  completion, and permanent quarantine; and
- sealed lease-use takeover, independent recovery/reset escrow, and
  reconciliation across the kernel ledger, registry, and abstract
  state-repair services.

Useful safety properties include:

```text
NoAuthorityAmplification
NoInvocationWithoutCurrentCapability
NoAdmissionBelowClosedAnchor
NoRevocationLaunderingThroughDerivedProduct
NoProductOutlivesEffectBearingAnchorWithoutConsent
NoStaleIdentifierChangesCurrentKernelObject
AtMostOneReplyOutcome
NoSiblingReplyReturnsAnotherHandlersDonation
OnlyActiveThreadCanReserveItsSchedulingContext
NoPreacceptWakeIntoParentDrainOrTerminalState
NoDonationReturnDispatchesDrainingOrTerminalPredecessor
CallerFundedAcceptancePublishesReadyActiveAndDonationAtomically
NoAcceptedHandlerDispatchWithoutPositiveBudget
NoReusableReceiverWithActiveCallTag
ActiveCallTagClearedExactlyOnce
DonationBindingReleasedExactlyOnce
ServerFundedAcceptanceHasNoIncomingDonation
NoAbortedPassiveHandlerReentered
NoUserReentryAfterPassiveFailureSelection
NoSchedulingContextBoundToTerminalThread
NoRunningThreadInStoppedDomain
NoRunningThreadInSuspendedDomain
NoNewDomainRelationshipAfterClosing
NoReuseBeforeQuiescence
NoIovaReuseBeforeDeviceRelease
NoNewAuthorityToQuarantinedFrame
NoPreQuarantineFrameFacetReactivated
NoDmaMapWithoutWholeAttachmentSetAuthority
AtMostOneResetOperationPerResetDomain
NoStaleManagerMediatedEffectAfterResetTakeover
NoResetVerificationOrReleaseBeforeOldManagerAliasFence
NoStaleCompletionReleasesCurrentFrame
NoStaleRecoveryMutation
AtMostOneCurrentRecoveryOrResetUseFacet
NoChargeMoveWithoutDestinationConsent
NoRecoveryResourceInChildSubtree
NoCallerConsumesUnreservedPassiveRecovery
PassiveAdmissionCopiesDoNotMultiplyCredit
NoPassiveFailureScopeWithoutPreauthorizedPolicy
GenericPassiveFailureStartsDomainClosing
NoUnboundedPassiveFailurePropagationPath
NoUnmodeledEndpointCloseFailureEdge
NoThreadOnlyRecoveryWithoutCancellationSafeManifest
NoHiddenObjectAllocation
AcceptedInvocationNeverReportedNotAccepted
NoCallAcceptanceAfterAnyOriginGateCloses
```

`NoStaleIdentifierChangesCurrentKernelObject` is deliberately scoped to
kernel-mediated state. It says an old selector, reply, mapping completion, or
binding event cannot mutate a current object after validation. It says nothing
about undoing a packet, device write, or disclosure already admitted; those
remain protocol outcomes, and reusable protected resources still require
quiescence.

Liveness properties need explicit fairness and hardware assumptions. A model
cannot prove device quiescence if the platform contract provides no way to
stop the device.

### Adversarial tests

The implementation test matrix should include:

- all capability operations across rights subsets and type confusion attempts;
- transfer concurrent with delete, revoke, domain death, and receiver quota
  exhaustion;
- slot, object, domain, endpoint, and reply generation reuse pressure;
- reply versus cancel, timeout, caller death, callee death, and endpoint
  revocation on every interleaving, including close during
  `REPLY_DRAINING`, in both caller- and server-funded modes;
- sibling-thread attempts to donate another thread's context or use, copy,
  transfer, or race the exact receiver's reply facet while that receiver is
  running on a donated context;
- copied and exhausted passive admissions, unreserved caller-induced aborts,
  policy close/replacement, minimum-deadline enforcement, and cyclic or broad
  conditional failure graphs, including delegated endpoint-close and automatic
  endpoint-owner teardown triggers;
- nested donation, priority inversion, call-depth exhaustion, acceptance with
  only the kernel reserve left, cancellation while `READY`, a server that never
  replies, parent reply/abort/termination racing a nested preaccept return, and
  attempted reuse of a `CALL_ABORTED` passive handler;
- capability-slot, reply-token, passive-recovery-credit, page-table,
  fault-record, and teardown-metadata exhaustion;
- simultaneous faults on multiple CPUs while threads enter and leave the
  domain;
- late TLB acknowledgement, interrupt delivery, DMA completion, and device
  reset failure after a replacement starts;
- quarantine release followed by attempted use, copy, or transfer of every
  pre-quarantine frame facet and attempted `Mapping.Protect`, including facets
  and mappings held outside the failed lifetime group;
- recovery-owner death during every teardown phase, destruction of its
  capability table, stale sealed-use attempts after takeover, and missing or
  exhausted escrow destination slots;
- a malicious driver with forged ring indices, repeated interrupts, stale
  buffers, inseparable requester aliases, and non-quiescing DMA;
- a replaced device manager that resumes mediated configuration calls, writes
  every profile-declared direct alias, or supplies old-epoch attestation while
  takeover, TLB invalidation, reset, and completion verification race;
- BEAM actor failure, runtime-wide failure, driver failure during BEAM I/O, and
  supervisor-budget exhaustion; and
- boot manifests with overlapping memory, cyclic authority, excessive
  privilege, and no independent recovery reserve.

### Measurements

Measure distributions and tail latency, not only best-case cycles:

- system-call entry and capability lookup;
- same-core and cross-core call, notification, and capability transfer;
- scheduling-context switch, donation, timeout, and cancellation;
- domain creation, start, cross-core freeze, and complete reaping;
- revocation work per slice and total graph cleanup;
- mapping change through completed TLB epoch;
- IRQ delivery/unbind and DMA stop through IOTLB/device quiescence;
- fault detection through recovery-owner delivery;
- supervisor restart through healthy endpoint publication; and
- BEAM process throughput, latency, GC pause distribution, and scheduler
  utilization above the kernel.

Performance comparisons need declared hardware, architecture profile, core
placement, cache state, payload, protection transition, compiler, build, and
measurement method. Historical microkernel timings are evidence that design
matters, not performance predictions for this platform.

## Implementation sequence

### Phase 0: abstract contract

- Define the object, capability, call, scheduling, fault, and teardown state
  machines.
- Model the invariants and race outcomes.
- Specify the initial authority manifest and recovery-resource topology.
- Bind every semantic completion to the lower architecture-layer contract.

Exit condition: executable models find no counterexample within declared
bounds, every operation has rights, charges, linearization, and failure
semantics, and open assumptions are explicit.

### Phase 1: single-core protected core

- Bootstrap explicit object memory and capability tables.
- Implement domains, address spaces, threads, mapping, and small endpoints.
- Use fixed/preallocated kernel storage on one virtual target.
- Add structured synchronous faults and generation-safe object destruction.

Exit condition: hostile domains cannot forge authority, escape mappings, or
exhaust uncharged kernel memory under fault injection.

### Phase 2: time and recovery

- Add scheduling contexts, timeout delivery, passive-server donation, and
  cancellation with finite passive admission, preauthorized abort policy, and
  trusted receiver profiles.
- Implement first-class domain freeze and split-phase reaping.
- Start a recovery service with a non-donatable reserve and epoch-fenced
  registry/state-repair sessions, sealed lease use, and independent recovery
  escrow from a manifest.

Exit condition: a looping or dying server cannot strand caller budget, and a
replacement domain receives no stale call, reply authority, or session
authority from the failed domain.

### Phase 3: multicore completion

- Add per-core scheduling, migration constraints, stop epochs, cross-core call
  paths, and completed TLB/mapping teardown.
- Stress every freeze, revoke, reply, and CPU-offline interleaving.

Exit condition: `STOPPED`, `QUIESCENT`, `REAPED_CLEAN`, and
`REAPED_WITH_QUARANTINE` remain distinguishable and correct under SMP fault
injection.

### Phase 4: isolated drivers and DMA

- Add IRQ/timer bindings, DMA address spaces, immutable device profiles,
  immutable requester/trust attachment sets, device queue leases, bounded
  shared rings, escrowed reset-lease control, split logical/physical manager
  fencing, and global frame quarantine with non-resurrecting authority.
- Place the first real or emulated driver outside the kernel.
- Preserve operation outcome and client reconciliation across driver restart.

Exit condition: driver compromise cannot reach ungranted frames, and no frame
is reused after failed quiescence.

### Phase 5: BEAM runtime integration

- Run a compatible runtime domain with many BEAM processes and process-local
  tracing GC.
- Implement opaque actor-level resource references, move eligible untrusted
  native work to services/ports, and test required in-process NIFs as part of
  the runtime failure boundary.
- Compare actor scheduling under runtime reductions with enforced kernel
  budgets and outer supervision.

Exit condition: ordinary actor failure remains runtime-local; runtime and
driver failure are contained as domains; compiled BEAM behavior is preserved
for the declared compatibility profile.

### Phase 6: second ISA and assurance ladder

- Port only the architecture facade and declared architecture obligations to a
  materially different ISA.
- Repeat fault, teardown, timing, and BEAM workloads.
- Refine the model-to-implementation proof boundary and audit boot
  configuration.

Exit condition: portability claims are based on two working backends rather
than interface aesthetics, and each assurance claim states its remaining
trusted assumptions.

## Decisions made by this research

The following are recommended architectural commitments for the next design
and prototype work:

- use a capability microkernel as the baseline privileged organization;
- treat `ProtectionDomain` as a first-class coordinated execution-stop and
  lifecycle boundary without claiming external state is fail-stop;
- use explicit caller-supplied memory for every user-created kernel object;
- represent CPU time with scheduling-context capabilities and non-donatable
  recovery reserves;
- use small synchronous invocation plus caller-funded call records, one-shot
  reply tokens with explicit caller/server funding modes, finite
  server-consented passive admissions and preauthorized failure scope,
  terminal passive-call paths, bounded notification, and shared-memory rings
  rather than kernel mailboxes; default untrusted clients to server funding;
- distinguish authority, ownership, identity, budget, completion, and
  liveness;
- publish logical closure before bounded physical revocation, rejecting later
  acquisitions through stable accounted anchors while tracking already
  admitted effects to quiescence or quarantine;
- preserve the stable lineage of every effect-bearing input on kernel products
  unless explicit durable-creation authority and lifetime consent authorize
  detachment;
- keep fault detection and containment in the kernel while leaving restart and
  state-repair policy in unprivileged supervisors whose mutation sessions are
  fenced by a sealed current recovery lease and whose successor authority is
  precommitted in independent escrow;
- bind device functions to immutable trusted quiescence profiles, bind each DMA
  space to one immutable atomic requester/trust set, fence shared reset
  boundaries with independently escrowed leases, and never reactivate old
  frame authority after quarantine;
- assign every replacement a distinct kernel domain identity, advance its
  logical-service epoch only in user space, and never transparently redirect
  pending work;
- keep ordinary drivers, native extensions, BEAM actors, mailboxes, scheduling,
  heaps, and tracing GC outside privilege; and
- treat kernel failure as node failure, with bounded crash capture followed by
  reset or external recovery.

## Open design questions

The architecture is not ready to call stable. The most consequential questions
are:

- Can derivation-tree revocation and lifetime-group teardown remain bounded
  enough for the expected number of runtime and driver objects, or should all
  revocable relationships use explicit proxy/facet objects?
- Should a protection domain own exactly one address space and capability
  space permanently, or may either root be replaced while stopped?
- Can cross-core synchronous calls satisfy bounded donation and cancellation,
  including passive-failure policy graphs and ready-before-dispatch budget
  checks, or should the first multicore design restrict synchronous call
  chains to one core?
- What is the smallest resource ledger that permits root-supervisor
  reconciliation without becoming a general privileged database?
- Which device classes can provide provable quiescence, which require reset,
  which expose inseparable requester groups, and which must be permanently
  assigned or quarantined?
- How should an actor-level capability broker preserve least privilege without
  making the whole BEAM runtime a confused deputy?
- Which BEAM/OTP compatibility profile is required for the first prototype,
  especially distribution, code loading, native interfaces, and persistent
  resources?
- What timing-channel profile is realistic on the first two target
  architectures?
- Which invariant should be proved first, and what compiler, assembly, boot,
  and architecture assumptions remain outside that proof?

These remain tracked by the [minimal privileged-kernel contract
inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md).

## Connections

- [Kernel hardware and architecture support
  layer](kernel-hardware-and-architecture-support-layer.md) provides the lower
  mechanisms and completion semantics this layer authorizes and composes.
- [BEAM, ERTS, and OTP principles for a new operating
  system](beam-erts-and-otp-principles-for-a-new-operating-system.md) defines the
  system decomposition and the managed semantics that must remain above the
  kernel.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
  provides routes through capability, IPC, scheduling, recovery, and assurance
  evidence.
- [Minimal privileged-kernel deep-dive
  journal](../50-journal/2026-08-31-minimal-privileged-kernel-deep-dive.md)
  records the research method and evidence boundary for this synthesis.

## Sources

### Protection, capability, and microkernel foundations

- [The protection of information in computer
  systems](../30-sources/saltzer-schroeder-1975-protection-information.md)
- [On micro-kernel
  construction](../30-sources/liedtke-1995-microkernel-construction.md)
- [From L3 to seL4](../30-sources/elphinstone-heiser-2013-l4-lessons.md)
- [seL4 reference manual, version
  16.0.0](../30-sources/sel4-foundation-2026-reference-manual.md)
- [EROS: A fast capability system](../30-sources/shapiro-et-al-1999-eros.md)
- [Capability myths demolished](../30-sources/miller-et-al-2003-capability-myths.md)
- [Capsicum](../30-sources/watson-et-al-2010-capsicum.md)
- [Exokernel](../30-sources/engler-et-al-1995-exokernel.md)
- [seL4 design principles](../30-sources/heiser-2020-sel4-design-principles.md)

### Scheduling, information flow, and assurance

- [Timing analysis of a protected operating-system
  kernel](../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)
- [Scheduling-context
  capabilities](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)
- [Time protection](../30-sources/ge-et-al-2019-time-protection.md)
- [seL4 information-flow
  enforcement](../30-sources/murray-et-al-2013-sel4-information-flow.md)
- [Comprehensive formal verification of an OS
  microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
- [CertiKOS](../30-sources/gu-et-al-2016-certikos.md)
- [Design and verification of secure
  systems](../30-sources/rushby-1981-design-verification-secure-systems.md)
- [Kernel design for isolation and assurance of physical
  memory](../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md)
- [A least-privilege memory protection model for modern
  hardware](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)

### IPC, containment, and recovery

- [Vulnerabilities in synchronous IPC
  designs](../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md)
- [Construction of a highly dependable operating
  system](../30-sources/herder-et-al-2006-dependable-operating-system.md)
- [Nooks](../30-sources/swift-et-al-2003-nooks.md)
- [Recovering device
  drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md)
- [CuriOS](../30-sources/david-et-al-2008-curios.md)
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md)
- [Hive](../30-sources/chapin-et-al-1995-hive.md)
- [Unreliable failure
  detectors](../30-sources/chandra-toueg-1996-failure-detectors.md)
- [Tolerating malicious device drivers in
  Linux](../30-sources/boyd-wickizer-zeldovich-2010-malicious-device-drivers.md)

### Adjacent architecture and runtime evidence

- [Scheduler activations](../30-sources/anderson-et-al-1992-scheduler-activations.md)
- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md)
- [For a microkernel, a big lock is
  fine](../30-sources/peters-et-al-2015-big-lock-microkernel.md)
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md)
- [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md)
- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
- [Erlang/OTP 29.0.5 system
  documentation](../30-sources/erlang-otp-team-2026-otp-29-documentation.md)
- [Erlang/OTP source tree at
  5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md)
