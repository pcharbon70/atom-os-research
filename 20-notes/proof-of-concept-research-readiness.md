---
title: "Proof-of-concept research readiness"
kind: note
created: "2026-09-05"
maturity: developing
tags:
  - beam
  - operating-systems
  - proof-of-concept
  - research-assessment
  - systems-architecture
aliases:
  - "Atom OS implementation readiness"
---

# Proof-of-concept research readiness

The archive contains enough research to start implementing a minimal bootable
Atom OS whose first delivery is an interactive CLI. The user has explicitly
rejected AtomVM and excluded graphical UI from this proof of concept. Its
implementation and validation plan must have no AtomVM dependency, reuse
experiment, or comparison gate.

The archive does not yet contain evidence that the proposed architecture works.
The next investment should be a reproducible CLI boot, executable contracts,
conformance tests, and an integrated boot-and-recovery experiment. Another
broad component survey is unlikely to resolve the most consequential unknowns.

This is a conditional recommendation to begin implementation, not approval of
every proposed mechanism or a claim of complete OS, OTP, security, portability,
or performance readiness. Four work packages should lead implementation:
target/build and CLI bring-up, the project's BEAM compatibility profile, a
minimal cross-layer contract, and measured resource containment and recovery.

## Question, scope, and decision standard

The subsequent [requirement deep dives](proof-of-concept-requirements/README.md)
cover all four work packages, integrated acceptance criteria and six later
capability rows in 19 reports. They compare primary papers, specifications,
implementation articles and blogs, then identify contracts and falsifying tests.
The [2026-09-06 research journal](../50-journal/2026-09-06-proof-of-concept-requirements-deep-dive.md)
records their exact provenance and retrieval limits.

That research preserves this assessment's recommendation to start implementation.
It sharpens four obligations: finite OTP calls may require alias/monitor closure;
fixed-period CPU budgets need an explicit boundary-burst rule; private heaps do
not guarantee same-runtime latency; and safe recovery needs funded cleanup and
quiescence before reuse. No target pin, ABI, compiled corpus or experiment was
produced, so none of M0–M4 is closed by the additional reading.

The corrected [T7500 target](proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) fixes the initial physical machine and Intel x86-64 architecture. It supersedes the AMD-processor assumption without turning any prior research session into a successful boot or complete M0.

On 2026-09-08 the user selected **Zig as the kernel language**. The
[language feasibility study](proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
adds limited hosted C-ABI and freestanding-link evidence. It narrows the
remaining M0 choice to a qualified compiler/build profile, not another general
language comparison. It does not supply a boot, accepted toolchain pin or
completed M0–M4 gate.

The assessment asks whether remaining uncertainty can be reduced more
effectively by building a bounded prototype than by further general reading.
The confirmed scope is a bootable OS operated through a CLI, with compiled BEAM,
automatic process-local tracing GC, supervised actor failure, and
protected-domain recovery integrated after the first CLI boot. The initial CLI
may be a small native user-space program. It need not wait for the runtime,
but a native prompt alone does not complete the BEAM-capable proof of concept.

Graphical display, compositor, desktop, and visual-computing work are excluded.
The CLI is the first operator interface and should expose the real mechanisms
as they become available, without simulating unimplemented service state.

Research is sufficient to start when the archive supplies:

1. a defensible division of responsibilities;
2. precedents and explicit limits for the required mechanisms;
3. an achievable subset with named dependencies and exclusions;
4. experiments that can falsify the important assumptions; and
5. a way to recognize success without silently changing the requirements.

The archive substantially supplies the first two and much of the fourth.
This assessment proposes the subset and acceptance framework. Target versions,
the runtime choice, concrete ABI encodings, and numerical operating limits
still need to become executable implementation inputs. Those are first
implementation tasks; they do not justify postponing all coding.

The existing inquiries set standards for the eventual architecture, including
multiple targets, distribution, advanced recovery, and assurance. They should
remain open after a successful first prototype. Passing a smaller milestone
does not resolve their larger operational questions.

## Evidence examined and its limits

At assessed revision `ae3d77d39bca10d2f61e56be975d37e54314be6d`, the archive
contained 103 developing notes, 300 source notes, nine open inquiries, and
sixteen deep-dive journals. The worktree was clean. Structural validation
passed for 455 completed documents, 18 directories, and 4,410 local links.
These are coverage and archive-integrity observations, not measures of
architectural correctness.

The review followed the home map and all nine inquiry workbenches, inspected
the layer conclusions and implementation programs, and examined selected
critical-path component contracts: bootstrap, capabilities and transport,
scheduling, runtime adaptation, compatibility, signals, GC, resource accounting,
reclamation, recovery, storage, and networking. It checked journal evidence and
the tracked artifact inventory. This was not a fresh full-text audit of all
300 primary works or a line-by-line verification of every component report.

The strongest negative evidence is explicit:

- The [runtime inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
  records no runtime prototype, conformance result, GC measurement, or native
  containment experiment.
- The [kernel inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
  records no implemented kernel, executable model, benchmark, or BEAM
  integration result.
- The tracked non-Markdown files are archive validation tooling and metadata;
  the [assets index](../assets/README.md) contains no retained prototype
  artifacts. No successful target boot or experimental implementation was
  found in the assessed checkout. Work elsewhere was not inspected.

Current official documentation was checked for the OTP reference release,
compatibility direction, tracing collection, and the proposed QEMU target.
The earlier pass also inspected AtomVM; its reuse recommendation is withdrawn
following the user's explicit rejection, and those checks survive only in the
historical session record. Existing source audits remain historical evidence;
this session did not rebuild or repeat them. The [assessment
journal](../50-journal/2026-09-05-proof-of-concept-readiness-deep-dive.md)
records the method and exact source manifest.

## Coverage by area

| Area | Research already sufficient to guide a first implementation | Missing decisive artifact | Effect on the first proof of concept |
| --- | --- | --- | --- |
| [Hardware and architecture](kernel-hardware-and-architecture-support-layer.md) | Privilege entry, context isolation, translation, time, events, completion, and fault boundaries | One exact virtual-machine and firmware profile, boot image, serial-input/output path, and trap/MMU/timer tests | First delivery boots to a native user-space CLI; a second ISA is a later portability gate |
| [Minimal kernel](minimal-privileged-kernel-layer.md) | Capability authority, explicit object memory, domains, bounded IPC, temporal accounts, teardown, and recovery topology | A small executable object/ABI specification and bounded lifecycle models | Enough to start; implementing the entire proposed object vocabulary at once would obscure the core experiment |
| [Managed runtime](managed-actor-runtime-layer.md) | BEAM placement, private tracing heaps, signal semantics, reductions, native boundaries, and differential testing | The project's runtime implementation and machine-readable, tested BEAM/OTP profile | Develop after CLI bring-up; required for the completed proof of concept; AtomVM is excluded |
| [System services](otp-like-system-services-layer.md) | Supervision, bootstrap, naming, outcomes, overload, persistence, and update policy | A running supervisor/registry nucleus and independent outer recovery | A small volatile subset is sufficient initially |
| [Storage](otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md) | WAL/checkpoint and request-outcome design, with explicit crash assumptions | A selected block/storage backend and tested durability barrier | Blocks power-loss and durable-state claims, not a volatile boot-and-recovery experiment |
| [Networking](otp-like-system-services-components/network-endpoint-and-protocol-services.md) | Bounded endpoints, session generations, parser isolation, transport/outcome separation | Concrete NIC/stack integration, buffer ownership, secure-channel and interoperability tests | Blocks network/distribution claims; unnecessary for the first local proof |
| [Authentication and authorization](authentication-and-authorization-across-the-five-layer-architecture.md) | Strong authority, identity, policy, revocation, and recovery decomposition | One deployment profile and tested end-to-end authority graph | Static bootstrap grants suffice initially; human login and federation can follow |
| [Applications](applications-and-domain-services-layer.md) and [visual computing](alan-kay-smalltalk-visual-interface-and-modern-desktop.md) | Domain boundaries, semantic identity, presentation recovery, live-tool confinement, and accessibility direction | One CLI-operated workload; visual user evidence belongs to later work | Build the CLI now; graphical UI and desktop are outside the proof of concept |

The distinction is mostly between researched mechanisms and missing
instantiations, measurements, or integration. Storage and networking are not
absent from the archive. Their device-specific implementation choices remain
open, as the reports explicitly acknowledge.

The [milestone coverage mapping](../60-planning/01-proof-of-concept/README.md#coverage-by-area-traceability)
now assigns the in-scope missing artifacts to detailed M0–M4 definitions, each
with required outputs, acceptance cases, dependencies, and completion evidence.
It also preserves the storage/networking and broader deployment deferrals.
The definitions now link 18 draft phase/task plans using the required described
hierarchy and integration gates. They specify what must be delivered; neither
the definitions nor those plans are executable artifacts or evidence that
the gaps are closed. Unresolved decisions block dependent implementation.

## Work package 1: target, bootstrap, CLI, and reproducible build

The hardware inquiry intentionally excluded choosing a board or firmware stack.
That was a reasonable research boundary, but it leaves a real implementation
decision. Freeze one target and document its complete execution environment.

The adopted first physical target is **Dell Precision T7500**, using
**Intel Xeon / Intel 64 (x86-64)**. The [active target and QEMU profile](proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
replaces the provisional RV64/OpenSBI route and the corrected AMD-processor
detour. Start with Nehalem-v1, one virtual CPU, 128 MiB, an explicit PC/firmware
fixture and serial console; the Atom kernel runs at ring 0 and services at
ring 3.

This is a selected machine and architecture, not a binary pin or demonstrated
boot. Exact QEMU/firmware/bootloader/toolchain identities and the installed
T7500's Xeon SKUs, enabled topology, memory and devices remain M0 inputs.
The reported two multicore packages do not require SMP for the first test.
Intel manuals and the actual processor-family errata now guide the backend;
AMD-specific research is no longer an implementation prerequisite.

The first target/build record must specify:

- emulator release, machine/CPU features, RAM, firmware hash, boot entry,
  memory map, timer path, and interrupt configuration;
- selected Zig kernel language, compiler/linker versions, freestanding target ABI,
  linker layout, exception/unwind policy, and all enabled register state;
- how native service images and compiler-produced BEAM modules reach memory;
- the permitted libc, allocator, clock, thread, entropy, and image-loader
  dependencies, including their replacements at the guest boundary; and
- repeatable build/run commands, serial evidence, debugger symbols, timeout
  handling, and a failing exit status for unattended test runs.

The host provides emulation, building, debugging, and evidence capture.
Firmware remains a named higher-privilege dependency. Atom must own the
claimed guest protection, page management, scheduling, IPC, and fault
mechanisms. A runtime running as a Linux process is valuable semantic
evidence but cannot establish those Atom-owned mechanisms.

The proposed initial threat profile trusts the development boot image,
firmware, emulator, and kernel implementation. User domains may crash, loop,
exhaust resources, or deliberately submit unauthorized kernel requests. Actor
isolation within one runtime still trusts that runtime; this experiment does
not establish a sandbox for hostile BEAM modules sharing it. Kernel or outer
recovery failure may escalate to machine reset. Physical attacks, malicious
firmware, and speculative timing channels are outside this first claim.

Start with static images and a bounded boot configuration. Demand paging,
swap, a general dynamic linker, and a package manager are unnecessary for this
milestone. Native image loading and safe user return still require concrete
validation; static packaging does not remove their trust boundary.

### First delivery: boot into the CLI

The first successful boot should follow a reproducible path from the emulator
or firmware entry through the Atom kernel into a native user-mode command loop.
Use serial input/output first, so graphical display, keyboard-device stacks,
and a compositor do not become prerequisites. An early privileged diagnostic
monitor may help bring-up, but the first delivered CLI should cross the real
kernel/user boundary and use a narrow console/system-information interface.

The kernel owns entry, validated return, initial address-space protection,
physical-memory accounting, a clock/timer path, and the minimal syscalls needed
to launch and serve the CLI. Command parsing, line editing, dispatch, and help
belong to the user-space CLI. An ordinary command never receives arbitrary
physical-memory, register, or root-capability access.

Keep the command surface small and staged:

| Available at | Command | Contract |
| --- | --- | --- |
| First CLI boot | `help` | Lists only implemented commands and their syntax |
| First CLI boot | `version` | Reports the actual kernel/CLI build and target identifiers |
| First CLI boot | `uptime` | Reads the kernel's elapsed-time source through the declared interface |
| Protected service nucleus | `mem`, `ps`, `services` | Reports actual accounted memory, execution contexts, and service generations |
| Protected service nucleus | `restart <service>` | Requests the independent recovery service to replace an explicitly permitted service |
| Managed-runtime integration | `beam-profile`, `run <module>` | Reports implemented compatibility and starts a module from the bounded boot bundle |

The first CLI is not a POSIX shell. Pipelines, scripts, environment expansion,
arbitrary filesystem execution, a package manager, and a general language REPL
are later features. Static boot images can supply the CLI and eventual BEAM
modules before writable storage exists. A reset or power command, if added,
must use explicit guest-machine control authority.

First-boot acceptance is concrete:

1. A documented clean build boots the actual kernel and reaches `atom>` in
   user mode, with no guest host OS supplying the kernel mechanisms.
2. A serial test harness submits commands and verifies their responses and
   return to the prompt; a boot banner alone is insufficient.
3. Input length and parser storage are bounded. Blank input, unknown commands,
   invalid arguments, repeated backspace, and overlong lines have defined
   outcomes and cannot corrupt or hang the kernel.
4. The timer continues advancing while the CLI waits for input. Console waits
   follow the chosen scheduler/event contract rather than disabling interrupts
   or blocking the privileged kernel indefinitely.
5. A CLI fault leaves bounded diagnostic evidence and follows an explicit
   initial halt/reset policy. Independent CLI restart becomes mandatory with
   the service/recovery nucleus; it is not pretended to exist at first boot.

Compiler, firmware, linker, serial-device, privilege-entry, and timer details
are the immediate research gaps for this delivery. Broad OTP library coverage
and the full recovery model do not block the first prompt.

## Work package 2: project runtime and compatibility closure

The exact compatibility profile is the most consequential missing input.
“Runs BEAM” must resolve to actual compiler output and observable behavior.
The [loader report](managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier.md)
already provides the right schema outline, but its fields have not become a
conformance-backed profile.

Use the [OTP 29.0.6 documentation
baseline](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
as a proposed reference and record the compiler, runtime, libraries, build
configuration, and hashes actually used. The wider [source
audit](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) is of
OTP 29.0.5. The archive acknowledges this distinction; it is not a defect,
but the prototype must align its own oracle, source, fixtures, and claims.

Freeze supported chunks, opcodes, term forms and limits, BIFs/imports,
exceptions, send/receive ordering, links/monitors, timers, GC-observable
behavior, and the selected library functions. Include aliases, priority
messages, ETS, and other features whenever the actual workload's dependency
closure needs them. Unsupported behavior needs a defined rejection or error
and a negative test. A handwritten list that omits compiler-emitted
instructions or transitive OTP dependencies is insufficient.

Two useful levels keep the claim honest:

- A core execution profile tests compiled modules, long-lived allocation,
  copying send, selective receive, lifecycle, and timers.
- A selected OTP profile additionally tests the exact supervisor/behaviour
  paths exercised by the application. A custom restart loop supports an
  OTP-inspired recovery claim, not compatibility with the full `supervisor`
  module.

The starting implementation recommendation is the small reference interpreter
already proposed in the managed-runtime research: a project-owned loader,
actor state, private heaps, tracing collector, copied messages, reductions,
and capability-kernel adapter for the declared profile. Use pinned upstream OTP
as the semantic oracle and compiler. AtomVM is neither an implementation
candidate nor a required comparison or build dependency.

The broader inquiry retains an ERTS port as an architectural alternative;
rejecting AtomVM does not by itself settle every possible ERTS reuse decision.
The CLI milestone must not wait for that broader comparison. The proof-of-
concept plan proceeds with the independent-interpreter direction unless a
subsequent implementation decision changes it explicitly.

After native CLI bring-up, implement the smallest workload's dependency
closure and test it on a hosted harness and then inside an Atom user domain.
The CLI should start the real workload through `run <module>` and report
unsupported profiles honestly. Long-lived allocation and process-local tracing
GC are required at this runtime milestone. A principles-only actor library
cannot substitute for compiled BEAM support.

## Work package 3: a minimal cross-layer contract

The reports have many useful semantic contracts, but no single executable
version-zero interface binds them together. Start with fixed/preallocated
kernel objects, one address space per domain, finite capability tables,
small server-funded endpoint calls, notifications, timer events, memory/CPU
accounts, fault delivery, and bounded domain destruction. Specify an operation's
rights, payer, identity/generation, linearization, failure result, and reuse
condition before implementing its path.

Avoid nested scheduling-context donation in the initial profile. The detailed
[IPC](minimal-privileged-kernel-components/bounded-invocation-and-transport.md)
and [temporal-authority](minimal-privileged-kernel-components/scheduling-contexts-and-temporal-authority.md)
reports show how much cancellation and recovery machinery it introduces.
Server-funded leaf services let the first experiment test isolation and
bounded waiting while this broader design remains open. Deferring donation
does not permit unbounded kernel sections or blocking unrelated actors on a
runtime scheduler thread.

Model only the selected profile initially. The minimum safety properties are:

- new invocations using ungranted or stale capabilities cannot be admitted;
  effects admitted before revocation remain separately tracked;
- resource reservations conserve capacity, including failure records;
- domain closing prevents new work before cleanup walks begin;
- reply, timeout, cancellation, and peer death select one terminal transport
  disposition and cannot silently redirect an operation to a replacement;
- memory and identifiers are reused only after the profile's required
  execution, translation, and reference quiescence; and
- child exhaustion cannot consume or revoke the outer recovery reserve.

Use bounded state exploration with reproducible counterexamples and small
fake-backend tests. A finite model establishes properties only under its
declared bounds and fairness assumptions; it is not an implementation proof.
Single-core operation reduces the target set but retains interrupt races,
local translation invalidation, user-access safety, and cleanup obligations.

Two navigation/decision issues need explicit resolution in this contract:

1. The early [kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
   emphasizes asynchronous bounded endpoints; the later kernel design selects
   synchronous invocation, notifications, and shared rings. These can compose,
   but the runtime adapter must state how asynchronous actor work maps onto
   the selected transport without blocking its only scheduler.
2. The kernel's full implementation program puts BEAM integration in phase 5,
   after SMP and DMA. That is a broad subsystem program, not the best order
   for this proof of concept. Deliver the native CLI first, then integrate
   managed execution after the protected single-core/time-and-recovery
   nucleus. Test BEAM before expanding into multicore and bus-mastering devices.

These are reasons to consolidate one small implementation profile, not to
rewrite historical research as though all alternatives had been settled.

## Work package 4: resource containment and recovery under load

This is the central empirical risk in the architecture. Kernel pre-emption
can preserve another domain's progress while a monolithic collector or native
loop still stalls every actor using the same runtime scheduler. The [GC
report](managed-actor-runtime-components/terms-private-heaps-shared-binaries-and-tracing-collection.md)
explicitly leaves bounded-pause collection open. Process-local heaps describe
ownership and tracing scope; they do not alone establish a latency bound.

Start with the simple tracing collector proposed in the archive and sweep
live-heap size, allocation rate, mailbox backlog, and kernel budget. Reserve
copying-collection workspace before destructive forwarding begins. Measure
both same-runtime actor delay and independent-domain progress. Introduce
incremental collection only if the declared workload envelope requires it.

Likewise, resolve the [mailbox/resource
profile](managed-actor-runtime-components/resource-accounting-and-overload-control.md)
before advertising bounded resources. Finite memory, an indefinitely
nonreceiving actor, unlimited successful sends, and indefinite survival cannot
all be promised together. Specify which overload action the profile takes,
preserve ordinary send return semantics where claimed, and never hide quota
pressure as silent loss of an admitted local message. Charge atoms, code,
shared binaries, timers, queued messages, and allocator slack as well as heaps.

Recovery must cross a real protection boundary. A BEAM supervisor inside a
failed runtime cannot restart that runtime. Start an unprivileged outer
recovery domain from a checked static authority graph, with memory, time,
replacement capacity, and fault delivery outside the child. Restarted domains
receive new identities; old replies and handles remain stale. The
[recovery-topology report](minimal-privileged-kernel-components/failure-boundaries-and-recovery-topology.md)
provides the larger design.

For the first profile, outer-recovery failure may explicitly escalate to
machine reset. Implementing replacement of the recovery root and all escrow
takeover cases is a later capability. Do not describe this smaller profile as
surviving supervisor failure at every level. Repeated child recovery must
nevertheless reclaim its resources or report bounded quarantine; allocating
fresh domains forever is not a successful restart experiment.

## Integrated CLI-operated operating-system demonstration

After the first native CLI boot, use one virtual machine with a small custom
kernel and four user-mode protection domains:

| Domain | Responsibility | Failure experiment |
| --- | --- | --- |
| CLI | Bounded command parsing and capability-scoped requests to actual system services | Crash or flood the CLI; the kernel and independent recovery service remain available |
| Outer recovery/control service | Static launch graph, child-domain replacement, independent heartbeat and evidence | Exhaust or fault a child; recovery retains authority and capacity |
| Project managed runtime | Compiled BEAM workers, selected supervision behavior, private heaps/GC, messages, timers | Crash an actor; then separately corrupt or stop the whole runtime |
| Native test/I/O service | Bounded echo or counter requests; optionally a narrowly granted non-DMA UART | Crash, loop, delay a reply, and send malformed or stale completions |

A volatile job/counter workload started from the CLI is sufficient. It should
expose one normal request, one actor restart, one native-service restart, one
whole-runtime restart, and recovery of the CLI itself. Its volatile state may
reset after runtime failure; the interface must say so. A response from a
dead generation cannot become a new command,
and timeout after acceptance cannot automatically mean that no effect occurred.

Suggested initial campaign sizes are one virtual CPU, 128 MiB of configured
guest RAM, 128 managed actors, at least one million transient allocations, and
1,000 child-domain restart cycles. These are proposed test inputs, not measured
capacity or performance predictions. Sweep smaller resource limits to exercise
failure paths. Pin CPU periods/budgets, memory partitions, queue sizes, cleanup
reserves, and workload seeds before running the campaign.

| Milestone | Exit evidence |
| --- | --- |
| M0: boot inputs | Adopted T7500 / Intel x86-64 target plus a still-required pinned build/target/firmware record, static CLI image format, minimal console/time ABI, memory limits, and automated boot/command checks; full runtime compatibility need not be complete |
| M1: boot to CLI | The real Atom kernel launches a native user-mode CLI; `help`, `version`, and `uptime` work; bounded serial input, invalid-command handling, and timer progress pass the first-boot criteria |
| M2: protected service nucleus | Capabilities, domains, memory/CPU accounts, bounded transport, fault delivery, and independent recovery work; CLI inspection/control commands report real state; selected lifecycle models and stale-handle tests pass |
| M3: project BEAM runtime | The CLI launches compiler-produced BEAM modules in the unprivileged project runtime; the declared corpus matches pinned OTP; automatic local tracing GC reclaims long-lived-process garbage; all guest substrate calls are inventoried |
| M4: integrated recovery and resource campaign | CLI, actor, native-service, and runtime-domain failure have distinct contained outcomes; predeclared limits hold; repeated restart reclaims clean resources; old generations cannot affect replacements |

M1 is the first delivery. Runtime/profile work can develop alongside later
kernel work, but neither a runtime comparison nor complete OTP coverage blocks
the first prompt. A hosted semantic test is not M3. The minimal BEAM-capable OS
proof of concept is complete only when the integrated M2–M4 evidence exists,
operated through the CLI. No graphical UI milestone is included.

Acceptance must include negative evidence, not just a successful console print:

- Every required compatibility case passes; exclusions and intentional
  resource-profile differences are separately enumerated. Malformed or
  unsupported input cannot publish partial runtime state.
- Reachable terms survive forced collections; transient allocation reaches a
  bounded post-collection steady state under a fixed live set. Runtime-global
  retention is accounted separately.
- Unauthorized memory, mappings, capability guesses, and malformed syscall
  buffers do not alter the kernel or another domain in the test corpus.
- Exhaustion covers pages, kernel slots, calls, faults, mailbox storage, and
  runtime-global resources. Error and teardown paths have funded capacity.
- CPU accounting checks configured budget plus an explicit bounded
  kernel/interrupt overrun rule. A non-yielding child cannot spend the
  supervisor's reserve.
- Declare p99 and maximum-observed CLI response, heartbeat, timer, GC,
  fault-delivery, and recovery targets before the stress run. Record values
  and workload conditions, not only pass/fail. Emulator timing is regression
  evidence, not a physical worst-case execution-time guarantee.
- A second clean build reproduces the artifact identities or explains allowed
  nondeterminism, and an unattended run reproduces the semantic/fault results.

## Capabilities after the minimal CLI-based proof of concept

| Next capability | Focused research or experiment needed before claiming it |
| --- | --- |
| Durable service or application state | Select one block/flash backend and its atomicity, flush, ordering, and corruption model; implement the existing single-writer log/checkpoint design; inject interruption at each persistence boundary, including recovery itself |
| Networked actors | Select one NIC and reusable protocol-stack strategy; audit buffer, timer, entropy, and native dependencies; prove bounded local queues and peer/session identity before adding membership or consensus |
| Isolated DMA driver recovery | Study the actual device/requester/reset scope and IOMMU behavior; test delayed DMA, failed reset, stale completions, and quarantine before reuse |
| Multicore or portability | After the single-CPU proof, add a second Intel x86-64 CPU and test stop/shootdown/publication races, then topology/NUMA as needed and a later second ISA. A physical single-CPU CLI check can follow virtual bring-up earlier; it does not establish SMP or portability |
| Human login, remote administration, or untrusted multi-tenancy | Choose one security deployment profile; specify enrollment/trusted interaction, policy enforcement, entropy/keys, revocation and recovery. Static demo grants do not establish these properties |
| Updates and broader root recovery | Define image selection, trusted artifact verification, data migration and rollback cutoff, plus recovery-controller failure and takeover. Restarting an unchanged volatile service does not establish these properties |

After M4, I would prioritize one durable local service operated through the
CLI: it tests whether OTP-style restart can recover useful state. Networking
can follow according to the first application. Graphical UI remains separate
from this proof-of-concept program.

There is no evidence-based schedule or staffing estimate yet. Runtime
implementation, compatibility breadth, engineering experience, and target
tooling can change the effort substantially. Estimate after the first CLI boot
and runtime-profile experiment rather than extrapolating from document or
component counts.

## Connections

- [M0–M4 milestone definitions](../60-planning/01-proof-of-concept/README.md)
  translate these outcomes into artifact and test obligations for subsequent
  phased implementation planning.
- [Proof-of-concept map](../10-maps/proof-of-concept.md) provides the selective
  implementation-oriented route through existing research.
- [Can a minimal bootable system validate the architecture?](../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md)
  tracks the gates without weakening the larger layer inquiries.
- [Assessment session](../50-journal/2026-09-05-proof-of-concept-readiness-deep-dive.md)
  preserves repository observations, validation, and source provenance.

## Sources

This is primarily an assessment of the archive's syntheses and experimental
record, linked beside each finding. Direct primary-source inputs were:

- [OTP 29.0.6 runtime documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
- [Pinned OTP 29.0.5 source audit](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md)

The RISC-V sources below supported the original candidate evaluation, not the adopted T7500 / Intel x86-64 backend:

- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md)
- [RISC-V SBI](../30-sources/risc-v-international-2025-supervisor-binary-interface.md)
- [QEMU RISC-V virt documentation](../30-sources/qemu-project-2026-risc-v-virt-platform.md)
