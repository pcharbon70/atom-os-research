---
title: "Resource accounting and overload control"
kind: note
created: "2026-09-03"
maturity: developing
tags:
  - actor-model
  - beam
  - ets
  - overload-control
  - resource-accounting
aliases:
  - "Managed runtime resource accounting"
  - "Actor overload-control component"
---

# Resource accounting and overload control

The best-supported design is a **hierarchical reserve-before-publish ledger**
covering actor, application/supervision group, runtime domain, and kernel
accounts. Every allocation or deferred operation is charged before it becomes
visible. Work that outlives the initiating actor carries a `ChargeContext`, so
exit cannot turn binaries, timers, table objects, native requests, distribution
buffers, or traces into ownerless consumption.

This report does not propose changing ordinary admitted Erlang sends into
silent drops. Compatibility and containment are reconciled through admission
before publication, receiver/domain failure at declared hard limits, and
explicit bounded-service extensions such as `try_send` or credit-bearing
channels. The particular action is a policy profile, not an accidental allocator
failure.

Shared tables are part of this component because they deliberately break the
private-heap ownership model. They require explicit object identity, owner/heir
state, access rights, generation, memory charge, traversal semantics, and
bounded bulk work.

## Question, scope, and operational standard

The question is:

> How can the runtime keep BEAM actors cheap and compatible while ensuring
> that every finite resource has an accountable owner, an enforceable domain
> ceiling, a bounded overload transition, and enough reserve to fail cleanly?

This component owns:

- actor/application/domain ledgers and reservation transactions;
- attribution of reductions, runtime CPU, heap, stack, queues, binaries,
  timers, relations, tables, code, atoms, native work, distribution, and traces;
- soft-pressure, admission, hard-limit, quarantine, and recovery-reserve state;
- ETS-like table objects, ownership/heir transitions, access policy, and
  per-operation accounting;
- retained/shared-object attribution and reconciliation;
- telemetry for current, peak, reserved, retained, refused, and reclaimed
  consumption; and
- compatibility projections for resource exceptions and actor/domain failure.

The kernel remains authoritative for physical pages, scheduling budgets,
endpoint slots, and domain teardown. OTP-like services choose quotas, priority
classes, shedding/restart strategy, and service-level flow control.

The baseline passes only if:

1. No counted object becomes visible before a matching reservation commits.
2. Every committed charge is owned by exactly one primary account and included
   in every required ancestor account.
3. Actor exit cannot erase charges for resources retained elsewhere or work
   still in flight.
4. Runtime totals reconcile with allocator, scheduler, gateway/service, and
   kernel totals within declared timing and metadata bounds.
5. Ordinary admitted local messages are not silently discarded by quota logic.
6. Control, cleanup, collection, and crash evidence have a capped reserve that
   ordinary work cannot consume.
7. Bulk table, cleanup, receive-scan, and reconciliation work yields in bounded
   slices.

## Evidence, synthesis, and proposal

[Resource Containers](../../30-sources/banga-et-al-1999-resource-containers.md)
shows why resources should follow the activity responsible for them instead of
the incidental execution context. It supports separating resource principals
from threads and carrying attribution across asynchronous work. The paper's
prototype and workloads are from 1999 and do not provide a BEAM actor ledger or
modern multicore allocator design.

[Scheduling-context capabilities](../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)
make CPU time an explicit authority that can be donated across synchronous
server calls. They support kernel-enforced runtime-domain time budgets and
causal charging across bounded IPC. Donation in that design is constrained and
does not justify propagating budget or priority through arbitrary asynchronous
actor messages.

The official [OTP 29.0.6 managed-runtime
documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
documents per-process reductions and memory information, process heap limits,
mailbox modes, allocator classes, binaries, timers, ports, ETS, atoms, and
system limits. It also supplies negative evidence: `max_heap_size` is checked
at garbage collection and is not a complete continuous quota over shared,
global, native, or deferred resources.

[ETS scalability research](../../30-sources/klaftenegger-et-al-2013-ets-scalability.md)
shows that centralized metadata and table structures can bottleneck highly
concurrent Erlang workloads and that table options change the trade-off. The
evaluation targets a historical VM and specific microbenchmarks, so it does not
select one structure for all workloads.

[Contention-adapting search trees](../../30-sources/sagonas-winblad-2018-contention-adapting-ordered-sets.md)
show that ordered-set representation can adapt between coarse and finer
locking based on measured contention. This supports workload-sensitive table
implementations, not a claim that the published CA tree is universally best or
that its exact design is suitable for every Atom OS table type.

[HiPE's high-performance Erlang work](../../30-sources/johansson-et-al-2000-high-performance-erlang.md)
is evidence that native code, garbage collection, exceptions, and runtime
services must share precise stack/root and process conventions. It is also a
warning that execution optimization creates accounting paths outside the
interpreter unless every slow path and native fragment is instrumented.

## Accounting hierarchy

```text
kernel domain account
  └─ runtime domain ledger
       ├─ recovery/system reserve
       ├─ application or supervision-group account
       │    └─ actor account
       ├─ shared-object pools
       ├─ native-service/gateway routes
       └─ runtime-global metadata
```

The runtime ledger is an auditable semantic partition beneath the hard kernel
domain account. It cannot promise more memory or CPU than the kernel grants.
Ancestor checks are atomic from the operation's perspective: either the full
path reserves or none does.

```text
ChargeContext {
  runtime_epoch,
  primary_account,
  application_account,
  domain_account,
  resource_class,
  operation_id,
  reservation_generation,
  policy_profile,
}
```

The context follows message copying, asynchronous I/O, native work, timer
delivery, distribution encoding, tracing, code publication, GC, cleanup, and
deferred reclamation. It is not actor-visible authority and cannot be forged by
a BEAM term.

## Reservation protocol

```text
Proposed(amount, class)
  -> AncestorsChecked
  -> Reserved
  -> Materialized
  -> Published
  -> Committed

Proposed | Reserved | Materialized
  -> RejectedOrCancelled
  -> RolledBack
```

Publication is the linearization point for an actor-visible object. If physical
allocation succeeds but publication fails, the reservation and memory are
released. If publication succeeds, the committed charge persists until a
generation-correct terminal release.

Reservations themselves are bounded and expire or are cancelled when their
operation generation ends. A recovery scan can reconstruct them from compact
operation records; hidden per-thread reservations are forbidden.

## Resource classes

At minimum, the ledger distinguishes:

| Class | Primary measurement | Important retained/deferred case |
| --- | --- | --- |
| Actor execution | Reductions and kernel CPU time | BIF, GC, signal, cleanup, and JIT slow paths |
| Private memory | Heap, stack, heap fragments, collector reserve | Old-generation retention and failed GC |
| Mailbox/signals | Envelope count, payload/fragment bytes, oldest age | Skipped selective-receive candidates |
| Shared binary | Allocated bytes and references/slices | Tiny slice retaining a large parent |
| Code/literals | Module generation and mapped bytes | Old code pinned by stacks/funs/literals |
| Atoms/global IDs | Entry and byte count | Permanent admission from external input |
| Timers/relations | Object count and delivery/cleanup work | Cancel/exit races and large fan-out |
| Tables | Metadata, buckets/tree nodes, entries, payloads | Owner death, heir transfer, snapshots |
| Native/gateway | Requests, buffers, mappings, endpoint slots, bytes | Cancelled but still executing/in hardware |
| Observability | Events, samples, buffers, crash pages | Trace consumer stall or crash storm |
| Fragmentation | Reserved versus live allocator pages | Empty arenas not yet returned to kernel |

Counts and bytes are both needed. A million zero-payload timers or links can
exhaust metadata and cleanup time even if their nominal payload bytes are
small.

## Shared and retained object attribution

Exact economic attribution of a shared binary has no uniquely correct answer.
The runtime therefore records two independent facts:

- **physical ownership:** one pool/account holds the full allocated bytes; and
- **retention attribution:** actors/applications that keep references expose
  retained parent bytes, slice bytes, and reference count.

Policy profiles can charge the creator, a shared application pool, or a
documented proportional scheme. They cannot make the allocation disappear
from the domain total. Moving primary ownership is a generation-checked ledger
transaction and never changes the physical total.

Reconciliation periodically compares reference metadata, allocator live
objects, pool totals, and domain pages. It is incremental and separately
charged. A mismatch above tolerance freezes new admission for the affected
class and emits evidence; it does not silently repair an arbitrary counter.

## CPU and work accounting

Reductions remain the actor-visible scheduling unit, but they are not a measure
of actual CPU time. Each runtime activation records:

```text
ActivationCharge {
  actor,
  reductions,
  kernel_time_start,
  kernel_time_end,
  signal_work,
  receive_candidates,
  allocated_bytes,
  gc_work,
  system_work_class?,
}
```

Large copies, hashing, map/table operations, BIFs, JIT helpers, GC, tracing,
and cleanup use bounded chunks and explicit work units. Kernel scheduling
contexts enforce domain time; runtime ledgers allocate responsibility within
that domain. Ordinary asynchronous messages do not transfer CPU authority.

Work that has no surviving actor owner is charged to the causative application
when known, otherwise to a capped runtime-system class. A “system” label is not
an unlimited sink.

## Pressure and overload states

```text
Normal
  -> SoftPressure
  -> AdmissionClosed
  -> RecoveryReserveOnly
  -> QuarantinedOrTerminating

SoftPressure -> Normal only below a lower hysteresis threshold
```

- `SoftPressure` increases telemetry, asks OTP-like policy to shed work, and
  may reduce optional caches/tracing.
- `AdmissionClosed` rejects operations at their pre-publication boundary or
  applies the profile's documented actor action.
- `RecoveryReserveOnly` permits only bounded cleanup, collection needed to
  release memory, failure publication, and crash evidence.
- `QuarantinedOrTerminating` stops ordinary scheduling when accounting
  integrity or forward progress cannot be guaranteed.

Thresholds cover more than fullness: allocation rate, oldest queue age,
selective-receive scan work, timer burst, cleanup backlog, and retained shared
bytes reveal overload before the final byte is exhausted.

## Compatibility and admission policy

For each operation, the profile states the hard action:

| Operation | Before publication | After publication |
| --- | --- | --- |
| Spawn | Return/raise compatible system-limit failure; no PID visible | Actor exists and receives normal lifecycle handling |
| Local ordinary send | Reserve envelope/payload or take declared receiver/domain action | Never silently retract the admitted message |
| `try_send` extension | Return explicit refusal | Accepted message follows normal semantics |
| Timer/relation/table create | Return compatible limit/resource error | Object has a committed owner and terminal cleanup |
| Native/remote request | `NotAccepted` and rollback | Terminal result or `Indeterminate` according to protocol |
| Trace event | Follow declared lossy/lossless observability mode | Loss is counted explicitly; ordinary actors do not pay unbounded trace debt |

Where OTP leaves behavior implementation-dependent, Atom OS still documents
and tests its choice. Resource refusal is not allowed to corrupt an object or
create a half-visible relation.

## Shared table object model

```text
Table {
  table_id,
  generation,
  type,
  access_profile,
  owner,
  heir?,
  ledger_account,
  implementation_generation,
  snapshot_epoch?,
}
```

Lifecycle:

```text
Reserved -> Owned
Owned -> Transferring -> Owned(new_owner)
Owned -> Destroying -> Retired
```

Owner death chooses exactly one generation-correct transfer or destruction.
No actor can observe a table under both owners or mutate a retired generation.

The compatibility floor preserves every atomicity and isolation guarantee that
the selected OTP profile documents. That includes single-object/key operations
and whole-operation semantics for `delete_all_objects/1`, list `insert/2`, and
list `insert_new/2`. Traversals are weakly consistent only where OTP documents
that behavior; a stronger snapshot requires an explicit, charged protocol.
Long operations may prepare, scan, resize, rehash, or reclaim in bounded
slices, but an operation specified as atomic has one visible commit point and
never exposes its partial mutation.

Implementation is selected per table type and workload:

- sharded or split-ordered hashing for high-concurrency sets/bags;
- an adaptive ordered structure such as a contention-adapting tree for
  `ordered_set` candidates;
- read/write concurrency options as declared compatibility hints; and
- immutable snapshot structures only when their copying/retention cost is
  explicitly charged.

No benchmark justifies one structure for every mix of reads, writes, scans,
keys, sizes, NUMA placement, and actor ownership.

## Failure, security, and resource analysis

- **Counter wrap/underflow:** checked arithmetic, wide counters, generation
  tokens, and stop-admission on invariant failure.
- **Charge laundering:** charge contexts are runtime objects; actor-provided
  account IDs are resolved through supervisor policy, never trusted directly.
- **Exit evasion:** deferred resources retain the old charge context until
  terminal disposition.
- **Shared-object abuse:** expose creator, physical owner, retainers, parent
  bytes, and retention age; apply pool ceilings.
- **Reconciliation storm:** incremental scans with their own budget and bounded
  evidence on mismatch.
- **Table hot key:** contention/queue-time telemetry and adaptive structure or
  service partitioning; no hidden global lock.
- **Priority escape:** control/recovery reserve is fixed and cannot be expanded
  by actor priority or message class.

## Alternatives and trade-offs

### Per-actor heap limits only

Simple and compatible with existing controls, but ignores shared binaries,
tables, atoms, code, ports, deferred operations, queues, and allocator
fragmentation. It is a useful local signal, not domain containment.

### Charge everything to the creator forever

Stable and inexpensive, but can punish actors after ownership legitimately
moves and obscures current retainers. Keep stable physical ownership plus
separate retention attribution and explicit transfers.

### Exact proportional sharing

Looks fair but requires high-frequency reference accounting and still embeds a
policy choice. Treat it as an optional policy after measuring its overhead.

### Block a sender at a full local mailbox

Provides feedback but changes ordinary asynchronous send, can create cyclic
deadlock, and lets one blocked send stall unrelated actor work. Prefer explicit
credit APIs or a declared receiver/domain terminal action.

## Implementation program

### Stage 0: model and inventory

- Enumerate every allocator/object/work path and its reserve, publish, commit,
  transfer, and release points.
- Model tiny ancestor ledgers, actor exit, cancellation, transfer, and counter
  exhaustion.

### Stage 1: domain and actor ledger

- Implement private heap, mailbox, actor, timer, relation, and code charges.
- Reconcile reductions with kernel CPU time and allocator pages.

### Stage 2: shared and deferred resources

- Add shared binaries, native/gateway operations, trace buffers, atoms, and
  retained-attribution reports.
- Exercise exit/restart while every operation is in flight.

### Stage 3: tables and policy profiles

- Implement bounded ETS-like operations and generation-correct heir transfer.
- Compare data structures and overload policies with representative services.

## Verification and measurements

- Property-test reserve/commit/release transactions under allocation failure,
  cancellation, actor exit, and domain restart; totals never go negative or
  exceed ancestors.
- Reconcile runtime live bytes, reserved bytes, allocator arenas, and kernel
  pages under randomized allocation/collection and intentional fragmentation.
- Fan out large binaries, retain tiny slices, transfer table ownership, and
  hold native/DMA requests after caller exit; verify charges remain visible.
- Cross every soft/hard threshold concurrently; prove each operation is either
  rejected before publication or committed exactly once.
- Benchmark table types across read/write/scan mixes, hot keys, ownership
  transfer, NUMA placement, and resize; publish p50/p99.99 latency and memory,
  not throughput alone.
- Compare unbounded compatibility, receiver termination, explicit `try_send`,
  and credit channels under cyclic dependencies and control traffic.
- Exhaust ordinary budgets and verify GC, cleanup, failure signals, and crash
  evidence still make progress within the fixed recovery reserve.

## Supported decisions and open questions

Evidence supports hierarchical causal accounting, kernel-enforced domain
ceilings, reserve-before-publication, separate shared-resource tracking,
explicit overload policy, and workload-sensitive table structures. It does not
choose fair shared-binary attribution, exact thresholds, table implementation,
or the application policy for every rejected operation.

The design is falsified if any resource is absent from both a primary and
domain total, if actor exit drops a live deferred charge, if a hard limit is
enforced only after partial publication, if an ordinary admitted message is
silently discarded, or if recovery can consume unbounded “system” resources.

## Connections

- [Managed actor runtime layer](../managed-actor-runtime-layer.md)
- [Terms, private heaps, shared binaries, and tracing collection](terms-private-heaps-shared-binaries-and-tracing-collection.md)
- [Signal ingress, mailboxes, and selective receive](signal-ingress-mailboxes-and-selective-receive.md)
- [Reduction scheduler and kernel scheduling contexts](reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Native work, ports, and drivers](native-work-ports-and-drivers.md)
- [Failure translation and the OTP boundary](failure-translation-and-the-otp-boundary.md)
- [Observability, deterministic testing, and crash evidence](observability-deterministic-testing-and-crash-evidence.md)

## Sources

- [Resource Containers](../../30-sources/banga-et-al-1999-resource-containers.md)
- [Scheduling-context capabilities](../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)
- [OTP 29.0.6 managed-runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
- [ETS scalability](../../30-sources/klaftenegger-et-al-2013-ets-scalability.md)
- [Contention-adapting search trees](../../30-sources/sagonas-winblad-2018-contention-adapting-ordered-sets.md)
- [A High Performance Erlang System](../../30-sources/johansson-et-al-2000-high-performance-erlang.md)
