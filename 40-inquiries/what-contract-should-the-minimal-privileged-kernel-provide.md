---
title: "What contract should the minimal privileged kernel provide?"
kind: inquiry
created: "2026-08-31"
status: open
tags:
  - capabilities
  - fault-containment
  - ipc
  - microkernels
  - operating-systems
aliases:
  - "Minimal privileged-kernel contract"
---

# What contract should the minimal privileged kernel provide?

## Why this matters

The platform needs a privileged enforcement layer between architecture
mechanisms and the managed BEAM runtime. If the layer is too weak, a driver,
runtime, or native service can forge authority, monopolize time, retain stale
access after restart, or corrupt a replacement through late CPU and device
effects. If it is too broad, BEAM semantics, driver policy, storage, naming,
and OTP supervision enter the system-wide trusted and failure boundary.

Capabilities and failure domains are also easy to specify incompletely. A
capability can authorize an operation without proving who owns cleanup or
whether a prior hardware effect has stopped. A stopped domain can still have
live calls, donated CPU budget, remote translations, interrupts, and DMA. The
contract must cover those intersections rather than list isolated mechanisms.

## Operational question

Which kernel objects, operations, rights, lifecycle states, and completion
conditions are necessary and sufficient to host mutually distrustful managed
runtimes and native services while preserving BEAM compatibility and allowing
unprivileged, independently resourced supervisors to recover them?

The proposed contract is acceptable only when evidence supports every row:

| Criterion | Required evidence |
| --- | --- |
| Complete mediation | Every privileged fast and slow path resolves a current typed capability; adversarial type and bypass tests find no alternate path |
| Authority confinement | An executable model and implementation tests show derivation cannot amplify rights, products preserve every effect-bearing input anchor unless separately authorized lifetime consent permits detachment, stable revocation anchors reject later admission without an unbounded walk, and stale generations cannot act |
| Explicit resources | Every user-created kernel object and exceptional-path record has one explicit payer and supplied capacity; exhaustion cannot consume an unrelated recovery reserve |
| Spatial isolation | A hostile domain cannot read, write, execute, map, or DMA to ungranted memory under the declared hardware model; address- and capability-space roots are exclusive or explicitly form one correlated boundary |
| Temporal isolation | CPU budgets are conserved and enforced; admitted kernel work has a bounded reserve/overrun rule, caller-funded nested calls return donated scheduling contexts exactly once under every terminal race, acceptance never dispatches without positive handler budget, and server-funded acceptance has no incoming donation to return to its outer caller |
| Bounded communication | Endpoint, call-chain, reply, notification, and shared-ring capacity and overflow behavior are explicit and measured |
| Failure containment | Domain closing freezes a fixed admitted membership set, atomically closes fixed root gates, creates a stop epoch, and dispatches bounded per-CPU stop requests before any object walk; suspend and stop publish completion only after every target leaves user and kernel execution with checkpoint postconditions, while a missing acknowledgement produces a typed failed state or node reset |
| Safe revocation | A published revocation anchor rejects later acquisitions; operations admitted earlier and physical cleanup remain tracked through capability, CPU, TLB, IRQ, IOMMU, DMA, and zeroing completion or explicit quarantine |
| Recovery independence | A non-donatable supervisor CPU reserve, memory, protected destination slots, fault path, sealed non-copyable lease-use facet, and independently derived `RecoveryEscrow`/`ResetControl` authority remain outside both the child and replaceable supervisor; registry and state-repair mutations reject a stale epoch |
| Honest operation outcome | Cancellation and peer failure distinguish not-accepted, replied, and accepted-without-reply transport states; external effects are refined only by protocol evidence |
| Incarnation safety | Old calls, replies, notifications, mappings, and software completions cannot mutate a distinct replacement domain; user-space service epochs and kernel object generations remain separate, while external effects require protocol reconciliation |
| Device containment | DMA authority is conjunctive over an immutable atomic requester/trust attachment set; driver and replaceable-manager submission/configuration aliases are completely revoked; IOVAs remain reserved through quiescence; every mediated manager effect and reset operation is fenced by independent escrowed reset control; quarantine globally denies new CPU/DMA access and permanently stales every old mutating frame facet; frame release requires current custodian authority plus matching generation- and epoch-bound completion evidence before retyping |
| Configuration security | A checked boot manifest demonstrates the intended initial capability/recovery graph and immutable trusted device profiles rather than assuming safe deployment |
| Architecture composition | One virtual target and a materially different second ISA implement the same semantic postconditions without hidden lowest-common-denominator gaps |
| BEAM compatibility | A runtime executes the declared compiled-BEAM profile with BEAM actors, signals, reductions, and process-local tracing GC remaining outside the kernel |
| Assurance honesty | Functional, security, availability, temporal, teardown, timing-channel, and configuration claims state distinct assumptions and evidence |
| Performance viability | Tail latency and throughput for IPC, revocation, faults, teardown, drivers, and BEAM workloads meet declared budgets on named targets |

The inquiry remains open until the contract survives modeling and at least the
first implementation experiments. A complete literature synthesis is not a
resolution.

## Working hypotheses

### H1: a capability microkernel is the right baseline

Typed, rights-limited capabilities can unify protected object invocation,
delegation, resource control, and revocation more cleanly than ambient names
plus global identities. A static separation profile and exokernel-like secure
bindings may be useful configurations, but neither should replace dynamic
capability delegation as the baseline.

### H2: a protection domain must be a first-class object

One domain object should anchor exclusive capability- and address-space roots,
exact thread membership, typed fault routes, a recovery-lease epoch, references
to separate quota accounts and lifetime groups, one kernel object identity, and
a lifecycle. Otherwise SMP suspend, stop, and teardown race with independent
thread and mapping operations. Shared roots would explicitly merge the attached
domains into one correlated boundary. The object should remain smaller than a
“process” in a hosted OS and contain no service or supervision policy. It is an
execution-stop anchor, not a claim that shared, device, durable, or external
state is fail-stop. Every relationship that could extend the domain must pass a
fixed root admission gate; entering `CLOSING` closes those gates and starts its
bounded stop protocol before traversing the potentially large object graph.

### H3: capability validity and effect completion must be separate

Publishing one-way closure of an accounted, stable `RevocationAnchor` shared
by a bounded capability path should reject acquisitions and invocations that
linearize later. Protected entries keep the anchor alive through physical
traversal. Operations admitted before closure remain possible old effects.
Each product must retain the stable anchors of the inputs that supply its
future-effect authority. Admission-only or consumed guards may be excluded
only by an operation schema that independently checks the product's lifetime
authority and atomically consumes or records the guard; detaching an
effect-bearing anchor requires explicit durable-creation authority and consent.
Reclamation must wait for old CPU
references, translations, waiters, replies, interrupts, and DMA to quiesce or
be confined to a precisely owned quarantine set. A `ReapToken` should expose
bounded progress without bypassing recovery-lease fencing.

### H4: scheduling contexts are needed in addition to spatial capabilities

An independently replenished CPU-budget object, donated along bounded
synchronous call chains, can prevent one domain from stealing ordinary service
time. Recovery additionally needs a non-donatable scheduling context and
precommitted fault/teardown reserve outside the child.
Accepting a caller-funded handler first enters a non-executing ready state;
dispatch requires a positive handler-budget quantum on the donated context and
all current thread/domain admission gates.
BEAM reductions remain runtime scheduling units; the kernel enforces coarser
CPU execution-time budgets for runtime and service domains. Wall-clock response
bounds additionally require deadlines plus scheduling, interrupt, and hardware
assumptions.

### H5: the kernel should contain failure, not choose restart strategy

The kernel should classify faults, route resolvable thread faults separately,
stop domains for fatal classes, preserve bounded evidence, drain calls, and
expose teardown. An unprivileged supervisor with independent resources and the
current fenced recovery lease should select restart group, retry, backoff,
state recovery, and endpoint publication. The lease-use facet alone is
insufficient: successor lifecycle authority, replacement resources, and
protected destination slots must come from a precommitted `RecoveryEscrow`
derived independently of the child and replaceable supervisor. The registry
and recovery services must validate that epoch or a narrow session closed by
takeover; unfenceable external effects remain outside the recovery guarantee.
Definite faults and liveness suspicions must remain distinct.

### H6: synchronous IPC needs explicit admission and cancellation authority

Small synchronous invocation plus caller-funded pending `CallRecord` objects,
accept-time one-shot reply tokens, and scheduling-context donation can be
efficient, but only if reply, cancel, timeout, caller death, callee death, and
endpoint revocation select one tagged outcome and both success and failure
drain before any present donated time and borrowed authority return. The
reply-token funding mode must make donation optional: a server-funded handler
retains its own context. Caller-funded acceptance additionally requires a
finite, shared-counter `PassiveCallAdmission` carrying cleanup credits and a
server-preauthorized immutable `PassiveAbortPolicy`; copying the admission
must not multiply its uses. A post-accept failure installs an `ABORT_PENDING`
no-entry gate before drainage. The generic result starts domain-fatal closing;
only a trusted immutable `CancellationProfile` for an isolated,
reconstructible worker permits terminal thread-local `CALL_ABORTED`. This
conditional failure-authority graph includes caller/session cancellation,
endpoint-close authority and automatic owner teardown; it must be checked for
cycles, funding, and blast radius. Ordinary untrusted clients should use server-funded endpoints unless
the caller-attributed recovery contract is deliberately installed. The
successful branch must likewise pass through `REPLY_DRAINING` and clear its
active-call tag only after descendants drain and donation returns; reusable
receive state cannot coexist with an active, reply-draining, or aborting call.
Bulk
asynchronous work belongs in bounded shared rings with notifications and its
own epoch/ownership reconciliation.

### H7: a BEAM actor should not be a kernel object

Mapping each actor to a kernel thread, domain, endpoint, or capability table
would sacrifice the cheap isolation and scheduling scale of BEAM. The runtime
should multiplex actors within a domain and mediate opaque actor-level
authority. An in-process NIF remains inside the runtime failure boundary;
where the declared compatibility profile allows, untrusted or privileged
native work should instead use a port, service domain, or compatibility shim.

### H8: device recovery needs trusted profiles and independent fencing

IOMMU mappings and driver-domain isolation do not establish queue closure or
reset completion. Each function should bind to an immutable trusted profile
that classifies all submission/DMA-reconfiguration aliases and admissible
completion evidence. Device-management routes and budgets must survive driver
failure, while a reset boundary shared by functions needs its own current
`ResetLease` rather than authority inherited from one domain's recovery lease.
Each DMA translation root must cover one immutable atomic requester/trust set;
inseparable mutually distrustful requesters cannot be advertised as isolated.
An independently derived `ResetControl` escrow must issue successor sealed
lease and recovery facets without reading them from a dead manager. Takeover
immediately fences later mediated manager calls, but it may claim physical
fencing only after terminally stopping the old manager or revoking every
profile-declared direct alias and completing translation invalidation.

## Paths to explore

### Formal and executable models

- Model capability derivation, attenuation, transfer, deletion, bounded anchor
  paths, product dependence on each effect-bearing input anchor, consumed
  admission guards, explicitly authorized durable detachment, one-way anchor
  closure, physical traversal, object closure, and safe generation rollover.
- Model pre-accept call records, origin-gate validation, caller- and
  server-funded reply-token creation, finite passive-admission counters,
  policy-authorized abort scope, reply, cancellation, timeout, caller/callee
  death, atomic `READY`/`ACTIVE`, `REPLY_DRAINING`, `ABORT_PENDING`,
  domain-fatal versus profiled thread-local drainage, non-reuse of aborted
  handlers, exact active-thread donation reservation, receiver-bound
  non-transferable reply authority, nested budget donation, exhausted donated
  contexts at acceptance, and teardown on all interleavings.
- Model thread/domain membership, suspend failure, terminal stop, resolver-token
  invalidation, and reaping concurrent with creation, migration, system calls,
  and faults.
- Model sealed recovery/reset lease-use takeover while an old supervisor is
  merely suspected, blocked, or resumes after the epoch changes, including
  independently derived escrow, protected destination-slot loss,
  compare-and-swap in the publication registry, and session fencing in
  state-repair services.
- Model logical revocation separately from CPU, TLB, IRQ, IOMMU, DMA, and
  zeroing completion.
- Model immutable requester/trust attachment sets and device-profile
  drain/reset dependency graphs, serialized reset operations, fenced
  completion tokens, IOVA non-reuse, mediated versus direct queue closure,
  reset-manager lease takeover versus direct-alias quiescence, permanent
  invalidation of pre-quarantine frame facets, and the distinction between
  clean reaping and custody of a bounded quarantine set.
- Generate unsafe boot authority graphs and determine which policy checks are
  decidable and usable.

### Prototype experiments

- Implement explicit object memory, typed capability tables, domains, and
  small endpoints on a single-core virtual target.
- Measure same-core call paths with and without capability transfer and
  scheduling-context donation.
- Inject object, cap-slot, revocation-anchor, call-record, reply-token,
  passive-admission/recovery-credit, mapping-object, page-table, fault-buffer,
  and teardown-metadata exhaustion.
- Add SMP, force failure on every instruction boundary around freeze and call
  cancellation, and detect attempts by stale kernel identities or service
  epochs to affect replacements.
- Build one isolated emulated driver with an IOMMU/DMA model, delayed
  completions, stuck interrupts, and failed reset.
- Run a BEAM-compatible runtime domain and compare actor latency, GC behavior,
  and scheduler utilization under kernel budgets.

### Configuration and recovery experiments

- Construct a root supervisor whose reserved time and memory cannot be reached
  by the child, then exhaust every child resource.
- Kill the supervisor during each teardown phase, let the old incarnation
  resume after takeover, and verify that kernel, registry, and state-repair
  mutations reject its stale epoch.
- Destroy or exhaust the replaceable supervisor's capability table and show
  that the successor receives only the precommitted attenuated authority and
  slots held by the independent recovery escrow.
- Recover ephemeral, client-associated, durable, shared, and externally
  visible service state separately.
- Verify that pending calls are not silently redirected to a replacement and
  that clients observe failure of the old service epoch.
- Corrupt or omit recovery manifests and ensure creation fails closed.

### Literature and implementation comparisons

- Compare seL4/MCS object and cancellation semantics with the proposed
  first-class domain and `ReapToken`.
- Compare static separation-kernel configurations with dynamic capability
  lifecycles for high-assurance deployments.
- Compare synchronous call chains with cross-core ring/doorbell services for
  BEAM runtime and driver workloads.
- Study production capability-system revocation patterns and root-service
  recovery beyond the sources already recorded.
- Review device-class reset and quiescence contracts before selecting hardware
  for the DMA prototype.

## Findings

### Literature synthesis

The current [minimal privileged kernel synthesis](../20-notes/minimal-privileged-kernel-layer.md)
recommends a
capability microkernel with explicit object memory, first-class protection
domains, bounded synchronous invocation, one-shot replies, scheduling-context
budgets, structured fault delivery, and split-phase reaping. It places BEAM
actors and OTP recovery policy above the privileged boundary.

The main evidence trails are curated by the [minimal privileged kernel
map](../10-maps/minimal-privileged-kernel.md). The original [layer research
journal](../50-journal/2026-08-31-minimal-privileged-kernel-deep-dive.md)
records how the baseline sources were selected, while the [component research
journal](../50-journal/2026-09-03-minimal-privileged-kernel-components-deep-dive.md)
records the expanded evidence review, common implementation standard,
falsifiers, and limits of the eleven-report pass.

### Component deep-dive refinement

The [component index](../20-notes/minimal-privileged-kernel-components/README.md)
now expands every numbered component into an independent report. Together they
refine the hypotheses into a staged implementation and verification program:

- [bootstrap](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff.md),
  [explicit object storage](../20-notes/minimal-privileged-kernel-components/typed-object-storage-and-explicit-memory.md),
  and [capability authority](../20-notes/minimal-privileged-kernel-components/capability-spaces-and-authority.md)
  define how authority and resources become protected state;
- [domains](../20-notes/minimal-privileged-kernel-components/protection-domains-threads-and-address-spaces.md),
  [bounded invocation](../20-notes/minimal-privileged-kernel-components/bounded-invocation-and-transport.md),
  and [temporal authority](../20-notes/minimal-privileged-kernel-components/scheduling-contexts-and-temporal-authority.md)
  define how work is admitted, funded, stopped, and given an honest terminal
  outcome;
- [architecture-resource bindings](../20-notes/minimal-privileged-kernel-components/memory-mappings-and-architecture-resource-bindings.md)
  and [fault containment](../20-notes/minimal-privileged-kernel-components/fault-capture-and-containment.md)
  carry generations, completion evidence, certainty, and quarantine across the
  lower hardware contract; and
- [recovery topology](../20-notes/minimal-privileged-kernel-components/failure-boundaries-and-recovery-topology.md),
  [safe reclamation](../20-notes/minimal-privileged-kernel-components/teardown-revocation-and-safe-reclamation.md),
  and [crash evidence](../20-notes/minimal-privileged-kernel-components/observability-and-crash-evidence.md)
  define independent takeover, split-phase cleanup, and bounded evidence when
  ordinary services cannot continue.

The reports strengthen the inquiry's operational standard but do not satisfy
it. In particular, fixed-depth revocation anchors, product-lineage inheritance,
whole-domain SMP stop, exact scheduling-context unwind, recovery escrow, unified
quiescence ledgers, and cross-layer crash-evidence survival remain Atom OS
proposals rather than transferred results from the cited systems.

### Important negative findings

- Capability possession does not establish ownership, identity, resource
  capacity, current liveness, or completion of earlier effects.
- Revoking an input does not revoke a longer-lived product unless that product
  retains every effect-bearing input's stable lifetime dependency.
- A stopped execution context is not a safely reclaimable domain.
- CPU-budget isolation is not protection from microarchitectural timing
  channels.
- IOMMU mapping alone does not make a mutually shared DMA protocol safe.
- A quarantined frame cannot be safely released by reopening its old object:
  every old mutating facet and mapping must remain stale across retyping.
- Restart does not repair durable, shared, or externally visible state.
- A heartbeat timeout is a suspicion, not proof of failure.
- Microkernel structure or a memory-safe implementation language does not
  inherit another kernel's formal verification.
- Language-level actor isolation does not contain a compromised runtime, JIT,
  native extension, driver, or DMA-capable device.

### Evidence gaps

No kernel implementation, executable model, hardware experiment, benchmark,
or BEAM runtime integration was produced during either literature pass. The
specific object vocabulary, rights, generation widths, revocation-anchor depth,
product-lineage algebra, call-depth and replenishment bounds, stop/checkpoint
latency, recovery ledger, device-quiescence profile, quarantine proof, and
crash-evidence schema remain proposals. The new component reports identify
tests for each gap but do not provide their results.

## Outcome

Open. The research has selected a baseline direction and made its contracts
testable, but it has not demonstrated them. Resolve only after an executable
model and prototype establish capability confinement, bounded cancellation,
SMP stop semantics, quiescence-gated reuse, independently resourced recovery,
and the declared BEAM compatibility profile on named targets.
