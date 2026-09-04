---
title: "BEAM, ERTS, and OTP principles for a new operating system"
kind: note
created: "2026-08-28"
maturity: developing
tags:
  - actor-model
  - beam
  - capabilities
  - erts
  - fault-tolerance
  - memory-management
  - operating-systems
  - otp
  - scheduling
  - systems-architecture
aliases:
  - "BEAM and OTP operating-system synthesis"
  - "OTP-inspired kernel architecture"
---

# BEAM, ERTS, and OTP principles for a new operating system

## Conclusion

The project should not treat “put BEAM in the kernel” as its architectural
goal. In current Erlang/OTP, **BEAM**, **ERTS**, and **OTP** are different
layers, and the most valuable operating-system ideas mostly come from the
relationships among them:

1. BEAM supplies a portable, inspectable execution model with explicit safe
   points and a load-time path to native code.
2. ERTS supplies cheap isolated processes, asynchronous signals, mailboxes,
   process-local memory reclamation, reduction-based pre-emption, links,
   monitors, timers, code versions, and runtime observability.
3. OTP supplies policies for structuring services, reporting failure,
   restarting components, packaging applications, and changing a running
   system.

A new system should preserve those principles while strengthening boundaries
that Erlang/OTP deliberately leaves to a host operating system or trusted
deployment. In particular, it needs hardware-enforced privilege, capability
authorization, bounded resource use, native-driver isolation, authenticated
distribution, crash-consistent persistence, and secure update and rollback.

The resulting architecture is layered. A small privileged kernel provides
protection domains, capability-checked endpoints, interrupt and timer delivery,
resource accounting, and the minimum mechanisms needed to contain native
faults. A BEAM-compatible managed layer provides very cheap actors, executes
compiled BEAM modules, and performs automatic process-local tracing garbage
collection inside those domains. OTP-like supervisors and behaviours remain
ordinary services and libraries because restart strategy is policy, not a
privileged kernel mechanism.

This conclusion is a design synthesis, not an implementation result. The
evidence supports the primitives and exposes known failure surfaces, but it
does not yet show that this particular decomposition will boot, meet a latency
target, or satisfy the required versioned BEAM/OTP compatibility profile.

## Separate the three layers

John Högberg's official [BEAM
primer](../30-sources/hogberg-2020-brief-introduction-to-beam.md) states the
terminological boundary plainly: BEAM is the register machine that executes
instructions; it does not itself know about Erlang processes, ports, or ETS.
Those facilities belong to ERTS. OTP is higher again: its behaviours,
supervisors, applications, and releases are Erlang libraries and conventions
built on ERTS process and signal mechanisms.

| Layer | Existing Erlang/OTP role | Potential value to this project | Do not assume |
| --- | --- | --- | --- |
| BEAM | Register instruction set, compiled module format, loader input, interpreter or BeamAsm translation | Required compiled-code compatibility, portable managed code, validation and loading boundary, explicit liveness information, safe points, inspectable artifacts | That the instruction set must be the kernel ABI or that one existing VM implementation must be reused |
| ERTS | Processes, signals, mailboxes, scheduling, heaps and GC, timers, ports/NIFs, ETS, distribution, code loading | Cheap concurrency, failure observation, process-local reclamation, responsive managed execution, versioned code activation | That language-process isolation equals a security boundary or that current hosted internals fit a kernel unchanged |
| OTP | Behaviours, supervision trees, applications, releases, upgrade orchestration, system messages | Uniform service lifecycle, explicit recovery policy, hierarchical failure domains, operations as part of design | That every supervisor policy belongs in privileged code or that restart repairs persistent/correlated faults |

This separation also clarifies what AtomVM contributed to the archive's first
deep dive. AtomVM is one compact implementation of a useful subset of the
combined model. It remains valuable evidence, but the project can compare it
with unmodified ERTS, other BEAM implementations, or a clean-slate runtime
that also implements the required BEAM contract without changing its goal.

## The durable principles

### Isolation should be the default unit of composition

Armstrong's 2003 thesis describes concurrent components as self-contained
processes with private state, location-independent identities, message-based
interaction, and explicit failure detection. The important OS lesson is not
that every component must literally be an Erlang process. It is that the cheap,
ordinary unit of software structure should also be a failure-containment and
resource-ownership unit.

Current ERTS realizes much of this economically: processes are lightweight,
grow and shrink dynamically, have private heaps, and release directly owned
runtime resources when they terminate. Immutable Erlang terms and message
semantics reduce accidental shared-state coupling. Per-process garbage
collection lets most collection work proceed without stopping unrelated
processes.

The boundary is not complete. All Erlang processes in one runtime normally
share a native address space, allocator infrastructure, atom table, code
tables, large binaries, ETS, ports, and VM fate. The official security guide
says all loaded code is trusted and that the runtime has no sandbox for
untrusted Erlang code. A malicious loaded module, a bad NIF, or a faulty linked
driver can affect the complete runtime. Process isolation is therefore an
excellent software-structure boundary but not, by itself, a kernel security
boundary.

For the new system, isolation should have two scales:

- **managed actors** should remain extremely cheap and own private logical
  state, mailboxes, budgets, and failure identity;
- **protected domains** should use MMU, MPU, PMP, or equivalent enforcement to
  contain native code, drivers, mutually untrusted applications, and runtime
  failures.

Cross-domain handles should be unforgeable capabilities, not ambient names.
Within one trusted domain, a runtime may use cheaper actor identifiers while
preserving the same protocol shape.

### Messages need contracts, not just queues

ERTS communication is asynchronous. Signals may arrive independently of a
process executing a receive expression, and a synchronous call is constructed
as request and reply signals. Ordering is deliberately narrow: signals from
one sender to the same receiver are ordered, while arrival time is not
specified and distribution failures can lose signals. Links and monitors add
failure signals; process aliases provide a revocable reply destination that can
discard a late response after a timeout.

These are strong design materials for a kernel IPC model:

- make asynchronous delivery the primitive and build synchronous protocols on
  top;
- specify ordering per sender and endpoint instead of promising global order;
- represent failure and cancellation explicitly;
- make reply authority revocable, as aliases demonstrate; and
- keep location and transport details out of application protocols where that
  does not weaken security or failure semantics.

The current mailbox model is also a warning. A process can receive faster than
it consumes, selective receive can scan past many unmatched messages, and
resource exhaustion is not prevented by default. Copying terms protects
ownership but consumes CPU and memory; shared reference-counted binaries avoid
some copies but create shared lifetime and accounting questions. Distributed
send can block under transport flow control, while asynchronous distribution
moves the burden to application-level backpressure and can consume excessive
memory.

The new system should treat an endpoint as a resource with:

- byte and message limits;
- explicit overflow behavior;
- sender credits, admission control, or another backpressure protocol;
- separate accounting for copied and shared payloads;
- cancellation and deadline metadata where required; and
- observability for queue age, depth, scan cost, drops, and blocked producers.

Unbounded mailboxes can remain an opt-in policy for trusted workloads, but they
should not be the only system primitive.

### Scheduling should charge work at controlled safe points

ERTS normally gives a runnable Erlang process a reduction budget, pre-empts it
after that budget is spent, and schedules another process. At the pinned OTP
29.0.5 revision the default context budget constant is 4,000 reductions.
Reductions approximate work rather than time: instructions and runtime
operations charge different amounts, and the mapping can evolve. Current ERTS
has four process priorities, per-scheduler run queues, load balancing and work
migration, and separate dirty CPU and dirty I/O schedulers for native work that
would otherwise monopolize normal schedulers.

The transferable principle is **cooperative implementation with pre-emptive
semantics at audited safe points**. The system can preserve runtime invariants,
avoid arbitrary interruption inside every operation, and still prevent a
managed actor from running indefinitely. It can also make work accounting
visible to schedulers and diagnostics.

The limits matter more for kernel design than the exact reduction constant:

- a reduction is not a time guarantee;
- a long or incorrectly classified NIF can make the runtime unresponsive;
- dirty work still consumes finite threads and can delay process suspension,
  collection, or termination;
- priority scheduling has no automatic solution to every priority-inversion or
  starvation case;
- multicore ERTS relies on host threads and the host OS ultimately places those
  scheduler threads on CPUs; and
- runtime-global locks, allocators, tables, and recovery data can limit scaling
  even when the language exposes no shared mutable state.

The proposed system should therefore combine two mechanisms. The kernel should
enforce wall-time, interrupt, and protected-domain budgets. The managed runtime
may use reduction-like accounting for cheap actor fairness within an admitted
domain. Every native or privileged operation must be short, yieldable,
asynchronous, or executed in a separately budgeted worker domain.

### Memory ownership should align with failure ownership

Current ERTS uses a generational copying collector per process, with a global
large-object space and other shared runtime structures. A process starts with a
small combined heap-and-stack region; in OTP 29.0.5 the default minimum is 233
machine words. The heap and stack grow toward one another. Most messages are
copied between process heaps, while some binaries and literals are shared.

The [Sagonas and Wilhelmsson
study](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md)
shows that message semantics allow several implementations: process-local
heaps simplify independent collection and exit-time reclamation but require
copying; a communal heap can share messages cheaply but introduces global
collection and synchronization; a hybrid can move messages into a shared area
but adds analysis and collector complexity. Its historical measurements do not
describe current OTP 29, but the trade-off remains fundamental.

The kernel-level principle is to make ownership, charging, and reclamation
follow failure domains. A terminated actor or protected service should release
its private resources without tracing the whole system. Shared buffers should
have explicit owners, lenders, or reference accounting. DMA memory, persistent
objects, code, atoms or interned names, and zero-copy network buffers need
separate policies because they outlive or bypass an ordinary actor heap.

For every allocation class, the design must answer:

1. Which domain is charged?
2. What is the hard limit?
3. Can allocation block, fail, or trigger collection?
4. What is reclaimed automatically on actor, service, or node failure?
5. Can another actor prolong the allocation's lifetime?
6. What diagnostic survives an out-of-memory termination?

This is stronger than relying on garbage collection alone. It turns memory
pressure into an explicit protocol and containment decision.

#### Adopted compatibility rule: automatic process-local tracing collection

The platform will follow BEAM's managed-memory contract for ordinary BEAM
processes. A process may allocate immutable terms without explicit
deallocation, and unreachable terms must be reclaimed automatically while the
process remains alive. A process-lifetime arena with reclamation only at exit
does not satisfy this requirement: long-running servers and allocation loops
would exhaust their budgets even after discarding old state.

The required baseline is therefore:

- each ordinary BEAM process has private logical heap state and a traceable
  root set;
- the runtime honors allocation checks, safe points, and live-value metadata in
  compiled BEAM code;
- tracing and reclamation are process-local so collecting one ordinary process
  does not become a whole-system stop-the-world operation;
- process termination still bulk-reclaims all remaining private heap and
  runtime state;
- shared binaries, literals, code, messages, native resources, and interned
  data retain explicit non-heap lifetime and accounting rules; and
- heap limits and collection failure produce defined BEAM-compatible process
  behavior plus resource evidence for supervision.

“BEAM-compatible” constrains observable allocation, liveness, exception,
message, process-information, explicit collection-request, and resource
lifetime behavior. It does not require copying exactly one ERTS collector
implementation. A new runtime may use a different process-local tracing
algorithm only if the declared compatibility suite and pause/resource budgets
continue to pass.

This rule applies to the managed runtime, not the privileged kernel. The
kernel allocates and accounts for pages or larger extents owned by a protected
runtime domain; it does not trace BEAM terms, scan process roots, or schedule a
collection. Ordinary term allocation and most collections must not require a
page-table change, TLB shootdown, global kernel allocation, or privilege
transition. Runtime allocators should obtain memory in batches and perform the
high-frequency heap operations inside their domain.

Many BEAM processes should still share one hardware-protected runtime domain.
Giving every BEAM process an MMU address space would replace cheap process
switches with page-table, translation-cache, and kernel-scheduler costs. Use
separate protected domains for trust boundaries, native services, drivers, or
resource containment—not as the default representation of every lightweight
BEAM process.

### Failure observation is mechanism; restart is policy

Links and monitors let a process observe another process's termination. OTP
supervisors turn that mechanism into structured policy. Workers perform domain
work; supervisors start, stop, monitor, and conditionally restart children.
The standard strategies—one-for-one, one-for-all, and rest-for-one—encode
different dependency assumptions. Restart intensity bounds repeated failure;
when the bound is exceeded, the supervisor terminates and propagates the
failure upward.

This is more important than the slogan “let it crash.” Expected errors still
need explicit handling. Crashing is appropriate when the component cannot
repair its own state and when all of the following are true:

- the failure is contained;
- required state is reconstructible or durably externalized;
- owned resources are reclaimed;
- the restart rate is bounded;
- the cause is not guaranteed to recur after restart;
- dependent components have a defined response; and
- a higher-level failure domain remains available to decide what happens next.

The kernel should provide termination, cleanup, observation, and stable failure
identity. It may provide a root service contract needed to bring the system up.
It should not encode application-specific restart strategy. OTP-like
supervisors belong in ordinary, replaceable system services where their policy
can be inspected, upgraded, and tested.

Supervision also stops at the boundary of its failure domain. A supervisor in
one ERTS instance cannot recover that instance after native memory corruption,
runtime abort, CPU reset, loss of power, or failure of the storage containing
its restart state. The wider OS needs watchdog, boot-recovery, peer-recovery,
and durable-state layers that use the same hierarchical reasoning at larger
scales.

### Live change requires versioning, quiescence, and state transition

Erlang code loading retains a current and an old version of a module. A fully
qualified call enters the current version; local calls and return addresses can
keep a process in the old one. Before loading a third version, the oldest must
be purged, and processes still referring to it may be terminated. OTP release
handling adds application instructions and state transformation through
callbacks such as code_change.

ERTS has loaded code without stopping the whole VM since OTP R16. The loader
prepares code away from the active view, updates replicated access structures,
waits for thread progress, and atomically publishes the staged view. The source
currently uses three code indexes to reuse access structures efficiently. That
implementation detail is separate from the language's two simultaneously
usable module versions.

The general OS pattern is valuable:

1. validate and prepare a new version without mutating the active system;
2. publish a complete new view atomically;
3. let existing work quiesce or cross an explicit version boundary;
4. transform application state under a declared protocol;
5. retain a known-good version until rollback is no longer required; and
6. reclaim old code and state only after references are gone or forcibly
   terminated under policy.

Hot code loading alone does not supply authenticity, durable rollback, crash
consistency, driver compatibility, or correct state migration. A new OS should
apply the versioned-publication pattern to services, endpoints, schemas, and
system images, then add signatures, boot selection, journaled state transition,
and power-loss recovery.

### Distribution should preserve failure semantics, not ambient trust

Erlang makes local and remote process interaction deliberately similar, which
encourages protocol-oriented design. That is useful, but current distributed
Erlang is not an appropriate security boundary for a new kernel. Official
guidance treats every connected node as fully trusted. The default cookie is a
cluster-mixing guard rather than strong authentication; untrusted networks
require TLS with client certificate verification. Global names and default
full-mesh connectivity also create scale and coordination costs.

The [Scaling Reliably
study](../30-sources/trinder-et-al-2017-scaling-reliably.md) demonstrated on a
historical Erlang/OTP baseline that partitioning network connections,
namespaces, and recovery data into scalable groups improved selected workloads
through 256 hosts and 6,144 cores. The result does not define a current OTP
limit, but it supports a durable principle: global coordination state and
fully connected topology work against failure containment and scale.

The new distribution layer should preserve asynchronous protocols, explicit
node-down information, and location-independent service interfaces while
replacing ambient trust with:

- cryptographic node and service identities;
- capability-authorized endpoints;
- authenticated and encrypted transports;
- explicit namespaces and failure domains;
- declared delivery, retry, deduplication, and ordering semantics;
- backpressure and admission control across the network boundary; and
- partition-aware recovery state rather than mandatory global membership.

Local and remote calls may share an interface, but they should not pretend to
have identical latency, loss, security, or failure behavior.

## What the existing implementation teaches

The pinned [OTP 29.0.5 source
audit](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) provides a
useful reality check.

The direct ERTS emulator C and header files exceed a quarter-million lines,
before architecture-specific system code, the Erlang libraries, crypto,
networking, build logic, and optional applications are considered. This is an
orientation count, not a trusted-computing-base measurement, but it shows why
porting all of ERTS beneath a new kernel is different from extracting its
principles.

The Unix port calls into POSIX threads and locks, virtual-memory mapping,
dynamic loading, sockets and event polling, clocks, files, libc, and Linux
facilities such as /proc. ERTS is a sophisticated hosted runtime. Running it on
a new kernel would require either a substantial compatibility substrate or a
deliberate port that replaces those facilities. The host currently supplies
privilege separation, address spaces, virtual memory, device drivers,
persistent files, process lifecycle, executable loading, and much of the
security perimeter.

Native extensions are especially revealing. Normal NIF work is expected to be
very short; long work must yield or use dirty schedulers. Drivers and NIFs
remain native code in the runtime's trust boundary. ERTS engineering has added
dirty schedulers and even a source transformer for yieldable C routines because
native work can otherwise defeat process fairness. A kernel inspired by the
model should make unsafe work a separate protected service by default instead
of relying only on programmer discipline.

The [many-core thesis](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md)
adds historical evidence: on a 64-core platform, runtime synchronization around
allocators, process tables, statistics, and queues constrained scaling even
though Erlang programs did not share ordinary mutable state. Specific locks and
numbers from 2011 are obsolete, but the architectural warning remains. A
share-nothing API does not remove shared implementation bottlenecks underneath
it.

## Proposed system decomposition

The following is a hypothesis to test, not a settled design:

| Layer | Responsibilities | Failure boundary |
| --- | --- | --- |
| [Kernel hardware and architecture support](kernel-hardware-and-architecture-support-layer.md) | Privileged entry and context, protection transitions, ordering and code publication, interrupt events, raw time, logical-CPU coordination, protected I/O, and architecture faults | Architecture and privilege boundary; port-specific mechanism without board bring-up or device policy |
| [Minimal privileged kernel](minimal-privileged-kernel-layer.md) | Typed capability spaces, explicit kernel-object memory, first-class protection domains, address spaces and mappings, bounded invocation, scheduling-context budgets, authorized IRQ/timer/DMA bindings, structured faults, and quiescence-gated reaping | A domain provides coordinated execution stop and lifecycle isolation; shared state, device reset, and external effects may have larger recovery boundaries; kernel failure remains system-wide |
| [Managed actor runtime](managed-actor-runtime-layer.md) | Term representation, very lightweight actors, process heaps and GC, reduction accounting, signal protocols, mailbox implementation, loader and safe points, runtime tracing | One protected runtime domain; ordinary actor failures contained within it |
| [OTP-like system services](otp-like-system-services-layer.md) | Supervisors, behaviours, lifecycle, device-service policy, naming, configuration and identity, durable state, networking, distributed coordination, update orchestration, overload control, metrics, and audit | Supervision tree or protected service domain; unprivileged and replaceable without kernel change |
| Applications | Domain protocols and state machines, organized as supervised trees with declared capabilities and budgets | Application subtree or protected application domain |

This shape intentionally has both kernel scheduling and runtime scheduling. The
kernel schedules protected domains and enforces hard resource limits; the
runtime schedules far cheaper actors within a domain. An experiment may show
that making every actor kernel-visible is affordable, but that should be
measured rather than assumed. The two-level design preserves cheap concurrency
without asking every actor context switch or mailbox operation to cross a
privilege boundary.

The runtime- and service-facing kernel interface could start with only:

- create, start, suspend, terminate, and reap a protected domain with a
  distinct kernel object identity; user space separately assigns any logical
  service epoch;
- create typed kernel objects from explicit, charged memory;
- derive, attenuate, transfer, delete, and revoke capabilities without ambient
  namespaces;
- invoke a bounded endpoint, transfer one-shot reply authority, cancel a call,
  and signal a coalescing notification;
- map, lend, revoke, and reclaim memory only after CPU and device-visible
  quiescence;
- bind scheduling contexts, budgets, interrupts, timers, and DMA authority;
- charge CPU, memory, capability slots, calls, teardown work, and device use to
  resource accounts; and
- retrieve structured fault, termination, quarantine, and boot-recovery
  evidence.

Service naming and atomic publication remain unprivileged policy over these
mechanisms. A BEAM PID is routing identity rather than kernel authority, and an
ordinary BEAM process is not a kernel thread or protection domain. The managed
runtime multiplexes many actors over a small number of kernel-scheduled threads
and mediates opaque actor-level resource references. A compromised runtime,
JIT, native helper, or driver is contained only at the surrounding kernel
domain boundary.

Everything else must justify privileged placement. A useful rule is: a feature
belongs in the kernel only when it is required to enforce isolation or resource
ownership across mutually distrustful components, to control hardware safely,
or to recover the machine before ordinary services can run.

## Implementation strategies under the compatibility requirement

### Port unmodified or lightly modified ERTS

Build enough of a kernel compatibility layer to run upstream ERTS and reuse the
Erlang and OTP ecosystem.

**Advantages:** the best semantic compatibility, mature tooling, extensive test
suites, and a strong reference implementation.

**Costs:** a large host contract, a large native trust boundary, tension between
ERTS scheduling and kernel scheduling, and inherited assumptions about trusted
code, distribution, files, dynamic loading, and native extensions.

This is a candidate implementation strategy and a valuable control experiment
even if it is not the final architecture.
Contemporary projects such as Tyn and embedded platforms such as GRiSP make the
porting path a concrete research lead, but their claims need independent audit
and reproduction.

### Implement BEAM compatibility over a new runtime

Write a runtime that accepts a chosen BEAM profile and maps its semantics onto
new kernel primitives.

**Advantages:** access to existing compilers and some libraries while allowing
the runtime and kernel boundary to be redesigned.

**Costs:** instruction, loader, term, exception, process, signal, BIF, NIF,
code-loading, and OTP compatibility become a long-term product contract. A VM
can execute BEAM modules yet still fail to support the OTP behavior users
expect.

This path should begin with an explicit compatibility matrix and conformance
suite, not a claim that “BEAM support” is one feature. The matrix must include
process-local tracing collection and long-lived allocation/reclamation
behavior, not only opcode decoding.

### Build a principles-only clean-slate runtime

Design a new managed instruction or language layer around cheap actors,
capabilities, supervision-friendly failure, bounded messages, and versioned
services, without promising BEAM compatibility.

**Advantages:** the system can make security, overload, persistence, and native
isolation first-class rather than retrofit them. Kernel and runtime mechanisms
can co-evolve.

**Costs:** it gives up immediate OTP ecosystem compatibility and must build a
compiler, debugger, tracing model, libraries, protocols, packaging, and
operational culture. Recreating syntax without the tooling and runtime
semantics would miss much of OTP's value.

This strategy no longer satisfies the platform goal and cannot be the primary
runtime. It remains useful only as a research comparison or as an optional
non-BEAM service environment.

The open implementation decision is now between porting a pinned ERTS and
building a new runtime that implements a declared, progressively expanding
BEAM/OTP compatibility profile. Both must retain automatic process-local
tracing collection. Measurements may choose between those implementations;
they may not silently replace the compatibility requirement with a
principles-only runtime.

## Design rules carried forward

1. **Make failure domains visible.** Name which faults kill an actor, runtime
   domain, driver domain, node, or machine.
2. **Make ownership follow failure.** Private memory and handles should be
   reclaimed when their owner terminates; shared resources need explicit
   lifetime and charging.
3. **Observe failure asynchronously.** Do not conflate notification with
   recovery policy or guaranteed delivery.
4. **Bound restart and overload.** Supervisors need intensity limits; endpoints
   need capacity and backpressure; domains need CPU and memory budgets.
5. **Keep unsafe work outside the cheap-actor trust boundary.** Drivers and FFI
   code should be isolated services or narrowly audited privileged code.
6. **Treat upgrades as transactions.** Prepare, validate, publish atomically,
   migrate state, retain rollback, and reclaim only after quiescence.
7. **Prefer local coordination.** Partition namespaces, recovery data, and
   supervision domains; avoid global state as the default.
8. **Design observability with the mechanism.** Scheduling, queues, crashes,
   capabilities, resource pressure, and version changes need structured traces.
9. **Do not hide the substrate.** Every prototype must state the host, privilege
   level, boot chain, drivers, allocator, clocks, persistence, and network
   services it inherits.
10. **Measure semantics, not slogans.** “Soft real time,” “let it crash,”
    “share nothing,” and “hot upgrade” are hypotheses with failure conditions,
    not completed features.

## Research program

The next experiments should compare mechanisms rather than begin with a broad
OS implementation:

1. **Bounded actor endpoint.** Implement a mailbox with byte and message
   limits, capability-scoped send rights, credits, cancellation, and queue
   telemetry. Test burst traffic, slow consumers, selective receive, sender
   death, and cross-domain payload ownership.
2. **Dual-level scheduler.** Run many reduction-accounted actors inside a
   kernel-scheduled domain. Measure fairness, tail latency, timer jitter,
   interrupt load, GC pauses, priority inversion, and a non-yielding native
   worker.
3. **Failure and cleanup.** Crash an actor, supervisor, runtime domain, and
   driver domain independently. Verify memory, endpoints, DMA buffers,
   interrupts, and persistent failure evidence after each event.
4. **Versioned service publication.** Prepare and atomically switch a service
   endpoint while requests are in flight. Exercise old-version quiescence,
   state transformation, incompatible clients, failed migration, rollback, and
   simulated power loss.
5. **Authenticated distribution.** Connect two nodes using cryptographic
   identities and delegated service capabilities. Test partition, replay,
   duplication, node compromise, backpressure, and loss of recovery state.
6. **Compatibility comparison.** Run the same actor/supervision workload on
   upstream OTP 29, AtomVM, and the candidate BEAM-compatible runtime, with a
   principles-only runtime as an optional research control. Include long-lived
   allocation, minor/full collection, mailbox, shared-binary, code-loading,
   exception, and process-information behavior. Record semantic differences
   separately from performance.
7. **Boot proof.** On a named emulator or board, trace reset to the first
   managed actor and inventory every inherited firmware, bootloader, libc,
   allocator, interrupt, clock, storage, and network dependency.

The [kernel-placement
inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
turns these into operational decision criteria.

## Confidence and limits

Confidence is high in the description of current OTP 29.0.5 semantics and
implementation boundaries because it is supported by the matching official
manual and a pinned source checkout. Confidence is high that OTP supervision is
policy layered over ERTS mechanisms, and that ordinary ERTS process isolation
is not a hardware security boundary.

Confidence is moderate in the generalized memory and scalability lessons. The
papers expose durable trade-offs, but their exact implementations, hardware,
and measurements are historical. Current OTP has evolved substantially.

Confidence is low in claims about the effort or performance of a new kernel.
No kernel code, ERTS port, BEAM-compatible runtime, target boot, fault-injection
campaign, or comparative benchmark was produced in this research pass. Blog,
book, project, mailing-list, and forum sources were used to find terminology,
failure reports, and implementation leads; self-reported claims were not
treated as proof.

## Connections

- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md) is the selective
  route through this research bundle.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) refines
  the capability, domain, IPC, scheduling, fault, teardown, and recovery
  contract immediately below the managed runtime.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
  connects that proposal to its protection, IPC, failure, driver, and assurance
  evidence.
- [OTP-like system services layer](otp-like-system-services-layer.md) develops
  the unprivileged lifecycle, supervision, naming, durable-state, I/O-policy,
  distribution, update, overload, and operations layer proposed here.
- [OTP-like system services map](../10-maps/otp-like-system-services.md) routes
  through that report, its open contract inquiry, research journal, and
  primary evidence.
- [Which principles belong in the
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
  keeps the architectural placement decision open.
- [The research journal](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md)
  records the exact revision, commands, searches, contextual sources, and
  limitations.
- [AtomVM as an operating-system
  foundation](atomvm-as-an-operating-system-foundation.md) supplies one compact
  implementation case to compare with the broader model.

## Sources

- [Erlang/OTP 29.0.5 system documentation](../30-sources/erlang-otp-team-2026-otp-29-documentation.md)
- [Erlang/OTP source tree at 5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md)
- [A brief introduction to BEAM](../30-sources/hogberg-2020-brief-introduction-to-beam.md)
- [The Road to the JIT](../30-sources/gustavsson-2020-road-to-the-jit.md)
- [The BEAM Book](../30-sources/stenman-2025-beam-book.md)
- [Making reliable distributed systems in the presence of software errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
- [A History of Erlang](../30-sources/armstrong-2007-history-of-erlang.md)
- [Efficient memory management for concurrent programs that use message passing](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md)
- [Characterizing the scalability of Erlang VM on many-core processors](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md)
- [Scaling Reliably](../30-sources/trinder-et-al-2017-scaling-reliably.md)
