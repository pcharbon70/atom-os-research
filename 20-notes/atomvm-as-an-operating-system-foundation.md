---
title: "AtomVM as an operating-system foundation"
kind: note
created: "2026-08-28"
maturity: developing
tags:
  - atom-vm
  - beam
  - embedded-systems
  - fault-tolerance
  - memory-management
  - operating-systems
  - scheduling
  - systems-architecture
  - virtual-machines
  - zig
aliases:
  - "AtomVM deep dive"
  - "AtomVM operating-system assessment"
---

# AtomVM as an operating-system foundation

## Conclusion

AtomVM is a credible **execution nucleus** for an experimental, single-purpose
embedded operating system. It is not presently a standalone kernel, a complete
operating system, or a safe multi-tenant boundary.

The strongest design is not to label the VM itself "the OS." It is to make a
small privileged substrate beneath `libAtomVM` explicit, let AtomVM own managed
execution and concurrency, and implement most higher-level system services as
supervised BEAM processes. In that shape:

1. a minimal substrate owns reset-to-entry, clocks, interrupts, allocation,
   timers, atomics or locks, entropy, watchdog/reset, flash primitives, and the
   interrupt-to-event bridge;
2. AtomVM owns BEAM loading, lightweight processes, reductions-based
   pre-emption, mailboxes, timers, per-process garbage collection, monitors,
   links, ports, and supported distribution semantics; and
3. supervised Erlang, Elixir, or Gleam services own device policy, storage,
   networking, configuration, and application lifecycle wherever the native
   boundary does not require privileged or latency-critical code.

That would be closer to an embedded language-based system or a
unikernel-style appliance than to a POSIX general-purpose OS. The distinction
is useful: it keeps AtomVM's actor and supervision model central without
pretending that language-level process separation supplies hardware privilege,
memory protection, a secure boot chain, or crash-safe device drivers.

The new privileged substrate in this architecture is implemented in Zig under
the project's settled [kernel-language
decision](zig-as-the-kernel-implementation-language.md). AtomVM's existing C
core remains an upstream compatibility component behind an explicit Zig/C
boundary; it is not a reason to write new kernel mechanisms in C.

## Evidence boundary and version discipline

AtomVM is moving quickly, so "AtomVM supports X" is incomplete without a
version. This assessment separates three baselines:

| Baseline | State on 2026-08-28 | Appropriate use |
| --- | --- | --- |
| v0.6.6 | Latest stable GitHub release, published 2025-06-23 | Conservative deployment baseline |
| v0.7.0-alpha.1 | Latest published prerelease, published 2026-04-06 | Evaluation of the v0.7 feature wave |
| `main` at `0220c78e` | Reports `0.8.0-dev+git.0220c78e`; changelog also contains an unreleased v0.7.0-beta.0 section | Architecture research only; upstream warns that `main` may be unstable |

The current-architecture claims below were checked against that exact `main`
revision, not inferred from older papers. The two main experimental papers
capture earlier states of the runtime. Their performance results remain useful,
but several feature-gap statements in them are now historical: current
development code includes 256-bit integers, Erlang distribution, Elixir
`GenServer` and `Supervisor`, expanded STM32 and RP2 drivers, ETS, crypto, and
JIT/AOT support. See the [documentation reading
note](../30-sources/atomvm-project-2026-main-documentation.md), [source-tree
audit](../30-sources/atomvm-project-2026-source-tree.md), and [v0.7 release
announcement](../30-sources/atomvm-project-2026-v0-7-alpha0.md).

## What AtomVM already is

AtomVM is a from-scratch, compact implementation of the BEAM execution model.
It consumes ordinary compiled BEAM modules but intentionally implements a
selected instruction and OTP surface suitable for constrained systems. Its
portable core is C; core libraries and its JIT compiler include Erlang and
Elixir code.

The runtime already supplies several facilities conventionally associated with
an OS execution layer:

- lightweight processes with message mailboxes, monitors, links, registered
  names, and timers;
- reductions-based pre-emptive scheduling, with a default quantum of 1,024
  reductions in the inspected source;
- one scheduler per core in SMP builds, started on demand, with a platform
  event poll used both for driver wakeups and idle waiting;
- per-process stack/heap regions and copying garbage collection;
- native ports and NIFs for device and platform integration;
- module and atom tables, reference-counted binaries, limited ETS, and
  distribution connections rooted in a `GlobalContext`;
- emulated, JIT, ahead-of-time native, and hybrid execution strategies; and
- a packbeam format that aggregates BEAM modules and assets into flashable
  `.avm` images.

The memory design is particularly relevant to a small system. Each Erlang
process begins with an eight-word combined heap/stack block, with heap and
stack growing toward one another. The default heap-growth policy tries to keep
16–32 free terms. Messages are copied into mailbox fragments and migrate to the
receiving heap; large binaries (currently 64 bytes and above) are managed
off-heap by reference count. This makes memory ownership legible, but an
unbounded mailbox can still exhaust the shared native allocator.

AtomVM also demonstrates that a conventional host OS is not a universal
requirement. The ESP32 port runs as an ESP-IDF/FreeRTOS application. In
contrast, the RP2 documentation describes an SMP implementation with no task
runtime, and its entry point calls the VM directly over the Pico SDK. The STM32
entry point initializes the ST HAL, maps an AVM image from flash, creates a
`GlobalContext`, and runs it without FreeRTOS. These are already
near-bare-metal firmware arrangements, although they still rely on vendor boot
paths, HAL/SDK code, a C library, an allocator, linker/startup support, and
native drivers.

## The present system boundary

The source exposes a promising but incomplete port seam. `sys.h` asks each
platform for event polling and signaling, select/listener registration, time,
AVM and module loading, port creation, platform initialization, and native-code
mapping or caching. `smp.h` asks for mutexes, condition variables, read/write
locks, processor discovery, scheduler start/join, and main-thread detection.

That is enough to organize a port, but not yet a complete operating-system
substrate contract. Startup, interrupt configuration, `malloc`, C-library
behavior, panic handling, entropy, watchdogs, flash operations, peripheral
drivers, and power management remain partly implicit or platform-specific.
The first architectural task is therefore to inventory and deliberately name
every dependency below `libAtomVM`, not merely to remove FreeRTOS from the
ESP32 build.

| Responsibility | What exists today | What an AtomVM-based OS must decide or add |
| --- | --- | --- |
| Boot and image loading | Vendor boot ROM/bootloader, linker layout, flash-mapped packbeam; ESP32 explicitly uses the IDF bootloader | Verified image format, recovery path, rollback, ownership of early initialization, and a reproducible reset-to-VM contract |
| CPU, interrupts, and time | Vendor HAL/SDK plus platform `sys_*` functions | Interrupt ownership and prioritization, IRQ-to-message semantics, monotonic guarantees, multicore startup, and power-state interactions |
| Scheduling | AtomVM ready/running/waiting lists, reductions, timers, SMP scheduler threads | Latency budgets, priority policy if any, admission control, overload behavior, and interaction with native work |
| Memory | Per-process copying GC over a shared native allocator; off-heap reference-counted binaries | Global allocator policy, deterministic out-of-memory behavior, quotas, fragmentation measurements, DMA ownership, and optional MPU/PMP protection |
| IPC and faults | Mailboxes, monitors, links, supervisors, distribution | Backpressure, bounded queues or credits, whole-node failure semantics, durable restart state, and driver-failure containment |
| Drivers | Ports/NIFs integrated with platform event polling and vendor APIs | Stable driver ABI, lifecycle and cancellation, interrupt safety, DMA, capability handles, and policy for native versus BEAM drivers |
| Storage | Packbeam, ESP32 NVS/partitions/FAT mounting, Unix files, limited platform-specific persistence | Portable block/storage service, crash consistency, wear policy, namespaces, encryption, and recovery |
| Networking | ESP32 networking, sockets/TLS where built, and partial Erlang distribution over TCP, UART, and USB CDC | Interface management, routing, credentials, secure distribution, update transport, and bounded network buffers |
| Security | Crypto APIs and cookie authentication; NVS is documented as plaintext; distribution TLS is not implemented | Threat model, privilege and capability model, key storage, secure boot, signed update/rollback, native-code trust, and denial-of-service controls |
| Observability | Logs, stack traces, optional crash dumps and line information | Persistent crash records, metrics, tracing under tight memory, remote diagnosis, and safe recovery tooling |
| Compatibility | Standard BEAM bytecode with a selected opcode/OTP surface | Supported profile, conformance suite, behavior of stubs, application packaging, and evolution policy |

## The central isolation problem

AtomVM's shared-nothing process model isolates Erlang state and removes direct
mutable sharing between ordinary BEAM processes. That is valuable fault
containment, but it is not an address-space or privilege boundary.

The inspected implementation keeps all processes inside one `GlobalContext`
and native address space. Their heaps are allocator-managed blocks, not
hardware-protected domains. NIFs and ports are linked native code; AtomVM has
no dirty schedulers, and its documentation requires native work to return
quickly. A bad pointer, blocked NIF, corrupt driver, allocator failure, or
unhandled native fault can therefore compromise or stop the complete VM.

This implies two honest product shapes:

1. **Single-tenant trusted appliance.** All flashed BEAM and native code is
   trusted. Supervision protects against application faults, while a watchdog
   and redundant nodes handle whole-runtime faults. This is the shortest path
   and may be sufficient for many devices.
2. **Protected language-based OS.** Applications and driver capabilities have
   enforceable resource limits; MPU/PMP or another protection mechanism
   separates native components; system calls or checked handles mediate
   hardware. This is a much larger design and may conflict with AtomVM's small
   footprint unless introduced selectively.

Calling the first shape secure multi-tenancy would be misleading. Requiring the
second shape before any prototype would hide the useful system already within
reach. The inquiry should state which failure and trust model each experiment
targets.

## What measurements say

The best published AtomVM measurements found in this search are narrow but
actionable.

Ferenczi, Ruda, and Tóth used ESP32-S3 boards with 512 KB application RAM and
ran each process-scaling experiment ten times. They fit about 370 unmonitored,
350 monitored, 360 linked, or 195 OTP-supervised workers. Ten workers sampling
every 50 ms could send faster than an aggregator consumed, eventually
exhausting memory; intervals above 300 ms were sustainable in that setup, and
500 ms was their default. Their LoRa tests also exposed driver-sensitive
limits: one-byte transfers were stable at 290 ms, while more than 27 bytes at
that interval lost data until the interval increased to 350 ms. The C++ LoRa
sender left roughly 154 KB more free memory. These are measurements of one
board, workload, radio configuration, and older AtomVM state, not universal
limits. See the [full source
note](../30-sources/ferenczi-ruda-toth-2025-measuring-erlang-scalability.md).

Branch and Weinstock's earlier LoRa–MQTT gateway comparison similarly found
near-complete delivery at 0.5 messages/s on both ESP32 implementations, but
about 70% delivery for AtomVM/Elixir at one message/s and rapidly worsening
behavior above two messages/s. At one message/s they estimated about 0.5 s
latency for the Elixir gateway versus about 0.1 s for C++. They also reported
immature documentation, GPIO/driver friction, and missing libraries. The paper
does not identify the AtomVM revision and did not publish raw data alongside
the article, so its numbers motivate reproduction rather than a current
capacity claim. See the [comparison source
note](../30-sources/branch-weinstock-2024-functional-programming-iot.md).

Together, the experiments support four conclusions:

- the actor model is viable at microcontroller scale;
- supervision and messaging have costs that are small enough to use but too
  large to ignore;
- queue growth and native-driver behavior, not process count alone, are primary
  failure surfaces; and
- every performance claim must pin AtomVM, SDK, board, execution mode, heap
  strategy, workload, and communication driver.

The later Erlang '25 paper proposes measuring the additional cost of redundant
hardware and remote-node monitoring. Its accessible abstract makes that an
important research direction but does not provide enough detail here for a
quantitative claim. See the [abstract-level source
note](../30-sources/ferenczi-ruda-toth-2025-evaluating-atomvm.md).

## What articles, blogs, and forums add

The non-paper literature is useful mainly for evolution and practitioner
priorities.

The project's [v0.7 alpha announcement](../30-sources/atomvm-project-2026-v0-7-alpha0.md)
documents a large compatibility step and explicitly tells stability-sensitive
deployments to remain on v0.6.x. The [v0.7 planning
discussion](../30-sources/atomvm-community-2025-v0-7-priorities.md) identifies
call overhead, ESP32/Pico tooling, Wi-Fi behavior, supervisor completeness,
GPIO consistency, light sleep, and flash layout as community concerns. Several
items later landed, so the discussion is evidence of engineering pressure, not
a current missing-feature list.

Broader posts range from onboarding tutorials to unreplicated claims of
"production-ready" systems. They demonstrate interest and plausible use cases,
but most omit exact AtomVM revisions, source artifacts, long-duration fault
data, or hardware measurements. The research archive should retain them as
leads and compare their claims against pinned source and reproducible tests.
The [journal entry](../50-journal/2026-08-28-atomvm-deep-dive.md) records the
screened official blog, Elixir article, practitioner post, GitHub discussion,
Erlang forum, and Reddit threads.

## Proposed target architecture

The first prototype should deliberately minimize novelty below the VM while
making all remaining dependencies visible.

| Layer | Proposed role |
| --- | --- |
| Boot and recovery | Select and authenticate an image, expose rollback state, initialize only the hardware needed to enter the substrate, and retain a recovery path |
| Minimal privileged substrate | Startup, vector/interrupt control, allocator and OOM policy, monotonic time, timers, atomics/locks, core startup, entropy, watchdog/reset, console, flash/block primitives, power hooks, and event delivery |
| AtomVM core | BEAM loading/execution, process scheduling, mailboxes, per-process GC, timers, monitors/links, native-port dispatch, and the supported distribution profile |
| Supervised system services | Device managers, storage, network configuration, naming, logging, metrics, update orchestration, and policy expressed as BEAM processes |
| Applications | Packaged BEAM components with declared capabilities and resource budgets appropriate to the chosen trust model |

The substrate interface should be smaller and more explicit than any current
platform port. Existing `sys.h` and `smp.h` are the starting point, not the
finished specification. Direct calls from VM or drivers into libc, ESP-IDF,
Pico SDK, or STM32 HAL should either be admitted as part of the target's trusted
computing base or moved behind a named contract.

## Research program

The next work should proceed by falsification rather than feature accumulation:

1. **Dependency census.** Trace a cold STM32 and RP2 boot from reset to the
   first BEAM instruction. List every boot ROM, startup file, HAL, libc,
   allocator, synchronization, timer, interrupt, and flash dependency.
2. **Reproducible baseline.** Build and run pinned AtomVM on generic Unix and
   one MCU or emulator. Record binary size, idle memory, first-process memory,
   boot time, scheduler count, and execution mode.
3. **Substrate extraction.** Turn the census into a small versioned interface
   with a conformance harness. Demonstrate it on two materially different
   targets before calling it portable.
4. **Pressure tests.** Reproduce process/supervision counts, mailbox overload,
   timer jitter, binary traffic, allocation failure, and driver backpressure
   across emulated and native/AOT modes.
5. **Fault injection.** Crash ordinary processes, port processes, NIFs, driver
   callbacks, storage operations, and a complete node. Record which failures
   supervision contains and which require watchdog or peer recovery.
6. **Trust model.** Choose trusted single-tenant firmware or protected
   components. For the latter, prototype capabilities, quotas, and one
   hardware-protected native boundary before designing a broad API.
7. **Lifecycle.** Add signed image selection, atomic update/rollback,
   crash-consistent persistence, and retained diagnostics. A bootable VM
   without recovery is firmware, not yet a dependable OS foundation.

These steps are maintained as an open [operational
inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md).

## Confidence and unresolved points

Confidence is high in the current source-level architecture and platform
dependency assessment because it was checked at a pinned revision. Confidence
is moderate in the performance risk assessment because two peer-reviewed
studies point in the same direction but use older runtime states and narrow
hardware/workloads. Confidence is low in production-readiness claims from
blogs and forum posts without pinned artifacts or long-duration data.

No local MCU, simulator, or successful AtomVM executable was used in this
research pass. CMake configuration completed on the host, but compilation
stopped because `gperf` was absent and the installed ASDF shims had no selected
Erlang/rebar versions. That is an environment failure, not evidence for or
against AtomVM. The exact commands and output are preserved in the [research
journal](../50-journal/2026-08-28-atomvm-deep-dive.md).

## Connections

- [AtomVM foundation map](../10-maps/atomvm-foundation.md) provides the
  selective route through this bundle.
- [The kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
  defines the evidence needed to strengthen or falsify this assessment.
- [The source audit journal](../50-journal/2026-08-28-atomvm-deep-dive.md)
  records local evidence and search coverage.

## Sources

- [AtomVM main documentation](../30-sources/atomvm-project-2026-main-documentation.md)
- [AtomVM source tree at `0220c78e`](../30-sources/atomvm-project-2026-source-tree.md)
- [AtomVM v0.7.0-alpha.0 announcement](../30-sources/atomvm-project-2026-v0-7-alpha0.md)
- [Measuring Erlang-Based Scalability and Fault Tolerance on the Edge](../30-sources/ferenczi-ruda-toth-2025-measuring-erlang-scalability.md)
- [Functional Programming for the Internet of Things](../30-sources/branch-weinstock-2024-functional-programming-iot.md)
- [Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems](../30-sources/ferenczi-ruda-toth-2025-evaluating-atomvm.md)
- [What's on your mind for AtomVM v0.7?](../30-sources/atomvm-community-2025-v0-7-priorities.md)
