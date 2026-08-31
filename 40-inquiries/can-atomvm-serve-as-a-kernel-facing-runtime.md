---
title: "Can AtomVM serve as the kernel-facing runtime of a new embedded operating system?"
kind: inquiry
created: "2026-08-28"
status: open
tags:
  - atom-vm
  - embedded-systems
  - operating-systems
  - research-program
  - systems-architecture
aliases:
  - "AtomVM foundational-runtime inquiry"
---

# Can AtomVM serve as the kernel-facing runtime of a new embedded operating system?

## Why this matters

AtomVM already owns managed processes, pre-emptive scheduling, mailboxes,
timers, garbage collection, monitors, links, and a native driver interface on
small MCUs. If those facilities can sit over a small, explicit hardware
substrate, most system policy could be written as supervised BEAM services
instead of a conventional C kernel and userland.

The idea fails, however, if hidden host dependencies remain large, overload
cannot be bounded, native drivers erase the promised fault isolation, or a
credible boot/update/security lifecycle costs more than the runtime saves.

## Operational question

For a named MCU and trust model, can a pinned AtomVM revision:

1. cold-boot from reset into a packaged BEAM system without a general-purpose
   host OS, with every remaining boot ROM, HAL, SDK, libc, allocator, and
   native-driver dependency enumerated;
2. use a small versioned substrate contract that is implemented on at least
   two materially different targets;
3. meet declared memory and scheduling bounds under process, mailbox, timer,
   binary, storage, and driver pressure;
4. recover ordinary BEAM service failures without rebooting the VM and state
   exactly which native or hardware failures require watchdog or peer-node
   recovery;
5. enforce the chosen trust boundary—either explicitly trusted single-tenant
   firmware or hardware-backed protection and resource capabilities; and
6. boot, update, roll back, persist state, and retain diagnostics through
   interrupted or failed operations?

A positive answer requires reproducible artifacts and measurements for all six
criteria. A boot demo alone is insufficient. A negative answer to one criterion
should narrow the intended system class rather than automatically reject
AtomVM for every embedded design.

## Working hypotheses

- **H1 — viable nucleus:** the STM32 and RP2 ports show that AtomVM can run
  without a conventional task OS, so an explicit small substrate is feasible.
- **H2 — single-tenant first:** a trusted appliance/unikernel model is viable
  sooner than protected multi-tenancy because all BEAM processes, ports, and
  NIFs currently share a native address space.
- **H3 — overload is the main managed failure:** mailbox growth, allocation
  exhaustion, and native-driver backpressure will limit dependability before
  raw process count does.
- **H4 — portability seam needs expansion:** `sys.h` and `smp.h` are a useful
  base, but the actual trusted substrate also includes startup, libc,
  allocation, interrupts, entropy, flash, watchdog, power, and vendor APIs.
- **H5 — recovery defines the OS boundary:** secure boot, update/rollback,
  crash-consistent persistence, and retained diagnosis will require at least as
  much architectural care as the scheduler and VM port.

## Paths to explore

### Baseline and dependency census

- Reproduce the official generic-Unix build with pinned Erlang, rebar3,
  `gperf`, Mbed TLS, and zlib.
- Build the same revision for one STM32 and one RP2 target or supported
  simulator. Trace reset, startup, HAL/SDK entry, `globalcontext_new`, module
  load, and the first BEAM instruction.
- Use link maps, undefined-symbol lists, and call tracing to inventory the
  actual substrate rather than inferring it only from `sys.h`.

### Resource and timing experiments

- Measure boot time, image size, idle memory, per-process cost, supervisor
  cost, message-copy cost, binary thresholds, GC pauses, scheduler latency,
  timer jitter, and power by execution mode and heap-growth strategy.
- Reproduce the 2024–2025 process, mailbox, and LoRa results on current stable,
  v0.7 prerelease, and pinned main where hardware permits.
- Add bounded queues, credits, or admission control and determine whether they
  can prevent global OOM without undermining ordinary BEAM semantics.

### Native and whole-node failure

- Inject crashes, hangs, and corrupt results in NIFs, port handlers, IRQ/event
  callbacks, storage, and network drivers.
- Compare process supervision, VM watchdog reset, dual-image recovery, and
  remote-node monitoring. Read the full Erlang '25 fault-tolerance paper before
  adopting its design.

### Trust and lifecycle

- Write explicit single-tenant and protected-component threat models.
- Prototype checked capability handles and quotas before attempting a broad
  user/kernel API. If protected components are required, test one MPU/PMP-backed
  native boundary and measure its context-switch and memory cost.
- Specify power-loss-safe image selection, signed updates, rollback state,
  encrypted credential storage, and retained crash records.

## Findings

- The current [synthesis](../20-notes/atomvm-as-an-operating-system-foundation.md)
  supports AtomVM as an execution nucleus, not a complete kernel.
- The pinned [source audit](../30-sources/atomvm-project-2026-source-tree.md)
  finds direct STM32 and RP2 VM entry points but continued dependence on vendor
  SDK/HAL, startup, libc, allocator, and native drivers.
- The [documentation](../30-sources/atomvm-project-2026-main-documentation.md)
  supplies a clear scheduler/event seam and per-process memory model, while
  documenting limited OTP, partial distribution, no distribution TLS, and no
  OTA workflow.
- Published [ESP32 measurements](../30-sources/ferenczi-ruda-toth-2025-measuring-erlang-scalability.md)
  demonstrate hundreds of processes but also global failure from mailbox and
  compute overload. The older [gateway
  comparison](../30-sources/branch-weinstock-2024-functional-programming-iot.md)
  shows that driver-heavy end-to-end behavior needs current reproduction.
- No target experiment has yet met the operational standard. The local build
  attempt failed on host prerequisites before compiling AtomVM; see the
  [journal](../50-journal/2026-08-28-atomvm-deep-dive.md).

## Outcome

Open. The next decisive artifact is a pinned, reproducible reset-to-BEAM trace
and dependency census on an MCU or faithful simulator, followed by mailbox and
native-fault pressure tests. Until then, the foundation claim is a supported
architectural hypothesis rather than a demonstrated OS design.
