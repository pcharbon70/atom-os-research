---
title: "Time, preemption, and CPU budgets"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Time, preemption, and CPU budgets

Requirement R05, M1–M4. Define who receives processor time, who pays for kernel work, and how deadlines remain observable when a child refuses to cooperate. Kernel-domain isolation and responsiveness among actors within one runtime are different obligations.

## Evidence and alternatives

[Scheduling-context research](../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) separates authority to consume CPU from execution identity. The [seL4 manual](../../30-sources/sel4-foundation-2026-reference-manual.md) makes donation and replenishment concrete. These are precedents, not ready-made Atom semantics: a donated context need not return if the server never replies.

[Blackham and colleagues](../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) found nonpreemptible paths requiring redesign even in a small protected kernel. Their target-specific timing analysis cannot supply a bound for this implementation.

The [T7500 / Intel x86-64 target](dell-precision-t7500-target-and-minimal-qemu-profile.md) replaces the SBI TIME dependency with a qualified x86 clock and interrupt-timer path. Investigate a local-APIC timer and an available calibration reference; TSC invariance, cross-CPU synchronization, frequency discovery and TSC-deadline support must not be assumed. Clock reading and deadline delivery are separate contracts. Exact sources and interrupt routing remain M0–M1 decisions; neither architecture documentation nor QEMU timing supplies Atom's scheduling policy or physical latency bounds.

## Proposed time and scheduling contract

Record the timebase frequency, counter width, conversion and rounding rules, interrupt mechanism, minimum programmable separation, and behavior for an already expired deadline. Use monotonic elapsed time, not wall-clock time, for uptime, budgets and timeouts. Firmware time services remain a privileged dependency.

For the first single-CPU profile, use independently funded domains with configured priority, period and budget; defer nested donation. Specify whether replenishment uses fixed windows, a sporadic mechanism or another algorithm before implementation. A simple fixed-period reset permits a burst across a period boundary. Therefore a budget Q per aligned period T does not establish a Q limit for every sliding interval of length T.

Account execution at switches, traps and budget interrupts. Assign syscall execution and interrupt work explicitly; record maximum permitted accounting overshoot. Bound interrupt draining and cleanup batches. A timer interrupt alone cannot preempt code that has indefinitely disabled interrupts.

Reserve recovery's CPU separately. Analyze the entire priority order and blocking paths: a utilization sum below one is neither a response-time proof nor protection against an unbounded high-priority handler. Server-funded calls require adequate server capacity and finite client admission, not merely a different accounting label.

Within the runtime, reductions provide cooperative scheduling opportunities. Every interpreter dispatch path, BIF, collector and adapter loop needs a stated yield policy. Kernel preemption of the runtime protects another domain; it does not schedule a second actor while a first actor's non-resumable collector owns that runtime thread.

## Failure and trust boundaries

The host can pause or deschedule QEMU. Separate guest-counter measurements from host wall-clock watchdogs, and record the emulator acceleration and clock configuration. A stalled emulator is not evidence of guest starvation; a healthy host deadline is not evidence that the guest timer advanced correctly.

Test timer wrap/conversion boundaries, delayed and coalesced interrupts, a continuously runnable child, receive and transmit floods, and repeated syscalls with expensive but valid inputs. Closing a depleted domain must not require it to run voluntarily.

## Acceptance and next exploration

Freeze numerical periods, budgets, priorities, overrun allowance and response targets before measuring. Run a non-yielding native child while observing CLI responses, an independent recovery heartbeat and timer delivery. Measure consumed CPU per domain and budget violations, including kernel/interrupt attribution.

Repeat with a runtime allocation storm and record same-runtime actor delay separately from independent-domain progress. Sweep live heap size and admitted load. Retain p99, maximum observed, sample counts and raw traces; do not label those observations physical worst-case guarantees.

The next decisive artifacts are a small scheduler/accounting state machine, a timer bring-up trace and an adversarial budget test. Policy selection is still open; no timing experiment has passed.

## Connections

[IPC funding](capabilities-syscalls-and-bounded-ipc.md), [tracing GC](private-heaps-and-tracing-garbage-collection.md) and [measurement](models-fault-injection-and-measurement.md) define the main cross-layer checks.
