---
title: "Arm Power State Coordination Interface, version 1.3"
kind: source
created: "2026-09-02"
authors:
  - "Arm Limited"
published: "2024-10"
citation_key: "arm-2024-psci-1-3"
container: "Arm system-software specification"
edition: "DEN0022F.b"
isbn: null
doi: null
url: "https://documentation-service.arm.com/static/6703a8b8d7e4b739d817e10d"
accessed: "2026-09-02"
tags:
  - arm64
  - cpu-lifecycle
  - firmware
  - power-management
aliases:
  - "PSCI 1.3"
---

# Arm Power State Coordination Interface, version 1.3

## Reference

Arm Limited. *Arm Power State Coordination Interface*, version 1.3, issue
F.b, document DEN0022F.b, October 2024.
[Official specification](https://documentation-service.arm.com/static/6703a8b8d7e4b739d817e10d).

## Research question or contribution

What portable interface may supervisory software use to request Arm CPU
start, stop, suspend, affinity-state query, and system power transitions from
higher-privilege platform firmware?

## Method

This is a normative firmware-interface specification. The analysis focuses on
CPU lifecycle, asynchronous completion, caller obligations, race states, and
the boundary between OS quiescence and platform power/coherency work.

## Findings

- `CPU_ON` is asynchronous. A successful return means the start request was
  accepted, not that the target is ready for scheduling or interrupt delivery.
  `ALREADY_ON` and `ON_PENDING` expose important race states.
- The target enters at a supplied address with a constrained initial execution
  environment. The OS still needs its own secondary-entry handshake before it
  can publish the CPU as online.
- `CPU_OFF` is a self-operation that does not return on success. Before calling
  it, the OS must migrate threads and interrupts away; asynchronous wakeups of
  an off CPU are erroneous.
- Firmware owns the specified cache and coherency work for power-down and
  power-up. The OS is not thereby relieved of draining its own timers,
  mailboxes, address-space references, or extended execution state.
- `AFFINITY_INFO` distinguishes `ON`, `OFF`, and `ON_PENDING`, but its answer can
  race with simultaneous lifecycle calls. The interface also admits disabled
  and error states.
- The specification explicitly discusses `CPU_ON`/`CPU_OFF` races and requires
  coherent state tracking on both sides of the firmware boundary.

## Relevance

An AArch64 backend should treat PSCI as a fallible, asynchronous mechanism
behind the kernel's richer logical-CPU transaction. Kernel `Online` follows a
generation-checked secondary handshake; kernel `Offline` follows quiescence
plus firmware-confirmed off state. A firmware timeout or ambiguous state must
quarantine the CPU and keep reachable CPU-local memory pinned.

## Limits

PSCI standardizes an interface, not a particular firmware implementation or
its timeliness. Platform firmware remains in the trusted computing base, and
implementation-defined hardware behavior remains. PSCI does not define
scheduler admission, IPI mailboxes, TLB-shootdown completion, runtime topology
policy, or safe reclamation of kernel per-CPU objects.

## Derived work

- [Logical-CPU coordination and lifecycle](../20-notes/kernel-hardware-and-architecture-components/logical-cpu-coordination-and-lifecycle.md)
