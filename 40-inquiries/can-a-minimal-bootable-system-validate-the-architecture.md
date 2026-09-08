---
title: "Can a minimal bootable system validate the architecture?"
kind: inquiry
created: "2026-09-05"
status: open
tags:
  - beam
  - fault-containment
  - operating-systems
  - proof-of-concept
aliases:
  - "First Atom OS prototype gates"
---

# Can a minimal bootable system validate the architecture?

## Why this matters

The archive has enough architectural research to start a bounded proof of
concept, but its layer inquiries describe a much larger eventual system.
This workbench defines an integration milestone without treating all future
features as prerequisites or prematurely resolving the wider inquiries.
The confirmed first delivery boots into a minimal CLI. AtomVM is rejected;
graphical UI and desktop work are excluded from the proof of concept.

The [T7500 target decision](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
fixes the initial physical machine and Intel x86-64 architecture. The user's
AMD-processor assumption has been corrected. Exact installed Xeon models,
board revision, memory, firmware and device inventory remain open.

## Operational question

Can one pinned virtual target boot an Atom-owned privileged kernel into a
native user-mode CLI, then use that CLI to operate protected services and a
project runtime executing declared compiled BEAM, with automatic process-local
tracing collection, supervised actor failure, enforced domain resources,
isolated native work, and independent domain recovery?

The required artifact is a repeatable build and test bundle meeting M0–M4 in
the [readiness assessment](../20-notes/proof-of-concept-research-readiness.md).
It must include exact compatibility coverage and exclusions, authority/resource
configuration, host and firmware dependencies, negative tests, raw measurements,
fault traces, and observed resource reclamation across repeated restarts.

## Working hypotheses

- One CPU, static images, a minimal console/time ABI, and a native user-mode
  CLI are enough for the first bootable delivery.
- Finite kernel objects, server-funded leaf services, and separate CLI,
  recovery, runtime, and native-service domains can test the integrated OS.
- The project's small compatible interpreter can consume a narrow native
  adapter without importing a general guest host-OS contract.
- Kernel budgets can preserve outer recovery under child overload, while
  managed scheduling and collection can meet a declared workload envelope.
- Generations, closed admission, and quiescence-gated cleanup can prevent old
  operations from affecting a replacement even without SMP or DMA.

Each is a proposal. They are falsified by required hidden substrate services,
unmanageable compatibility gaps, authority escape, starvation of recovery,
unbounded retained resources, stale-generation effects, or failure to meet the
predeclared workload envelope.

## Paths to explore

1. Freeze the target/build/firmware record, static image format, console/time
   interface, and automated serial test harness.
2. Boot to a native user-mode CLI with `help`, `version`, and `uptime`, bounded
   input, error handling, and continued timer progress while idle.
3. Add the protected service nucleus, real CLI inspection/control commands,
   resource limits, lifecycle models, and independent recovery.
4. Establish pinned OTP fixtures and the project interpreter's declared
   compatibility profile; launch real BEAM modules from the CLI in the guest.
5. Stress GC, mailbox and global runtime memory, kernel quotas, CPU budgets,
   CLI/actor/native/runtime failure, stale replies, and repeated reclamation.

The [prototype map](../10-maps/proof-of-concept.md) connects each step to the
existing component research.

## Findings

The [2026-09-05 assessment](../50-journal/2026-09-05-proof-of-concept-readiness-deep-dive.md)
found substantial design coverage but no checked-in executable kernel or
runtime model, successful target boot, or conformance campaign. The user's
subsequent direction excludes AtomVM and makes the CLI boot the first delivery.
Thus implementation can start, but none of the integration gates is yet
satisfied.

The user subsequently selected Zig as the kernel language. The
[Zig qualification inquiry](can-zig-meet-the-kernel-qualification-contract.md)
tracks the remaining compiler/ABI/entry evidence; its narrow research probes
do not constitute a guest boot or close the gates below.

Current gate state:

The [requirement deep dives](../20-notes/proof-of-concept-requirements/README.md)
and their [2026-09-06 session](../50-journal/2026-09-06-proof-of-concept-requirements-deep-dive.md)
now connect every assessment requirement to evidence, alternatives, failure
boundaries and next tests. They confirm that the decisive remaining work is
executable: the boot record, operation/lifecycle contract, generated BEAM
closure, and integrated resource/recovery campaign. Finite OTP calls require
careful alias/monitor coverage; kernel preemption and same-runtime GC latency
remain separate obligations. No model or guest experiment was run in that
session. The corrected T7500 / Intel x86-64 selection narrows M0 but provides no executable
boot evidence. A qualified physical single-CPU CLI check can follow virtual
M1 before SMP or second-ISA work. All gates below therefore remain open.

The [M0–M4 definitions](../60-planning/01-proof-of-concept/README.md), authored
on 2026-09-08, assign detailed artifact and acceptance obligations to each
milestone and map the coverage gaps to their owners or explicit deferrals.
No phase/task decomposition, implementation, model execution, or guest test
was delivered by that writing pass. The gate state is unchanged.

The subsequent M0–M4 planning pass added 18 draft phases, explicit decision and
task dependencies, artifact/case mappings, and phase-ending integration tests.
M1 virtual CLI acceptance and physical T7500 qualification are separate gates.
No implementation or test execution accompanied that decomposition; all gates
below remain open, and unresolved inputs still block dependent work.

| Gate | State |
| --- | --- |
| M0: pinned boot inputs | Open; T7500 / Intel x86-64 selected, but exact installed-unit inventory, virtual binary pins, toolchain, firmware/bootloader, static image and console/time ABI need concrete artifacts |
| M1: first boot into a native user-mode CLI | Open; no interactive Atom OS boot is recorded |
| M2: protected service nucleus and CLI control | Open |
| M3: CLI-launched compiled BEAM and tracing GC | Open |
| M4: integrated recovery/resource/fault campaign | Open |

## Outcome

Open. Resolve only after the recorded integrated campaign passes or after an
explicitly justified change to these criteria. A successful result supports
the named single-node profile, not production security, durable state,
distribution, DMA isolation, multicore correctness, a desktop, or portability.
