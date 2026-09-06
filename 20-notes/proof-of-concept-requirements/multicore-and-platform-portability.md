---
title: "Multicore and platform portability"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - capability-roadmap
  - proof-of-concept
  - requirements
aliases: []
---

# Multicore and platform portability

Requirement R17, SMP and second-ISA work after M4. The [T7500 profile](dell-precision-t7500-target-and-minimal-qemu-profile.md) allows an earlier single-CPU physical CLI check after virtual bring-up. Validate concurrency, physical platform behavior and second-ISA portability as separate claims.

## Evidence and architectural differences

As comparative evidence, the [RISC-V supervisor specification](../../30-sources/risc-v-international-2026-privileged-architecture.md) makes SFENCE.VMA local to the executing hart. Reclaiming a mapping used elsewhere requires a remote coordination and acknowledgement protocol, not only a local fence.

[Arm's threaded self-modifying-code discussion](../../30-sources/bramley-2025-arm-self-modifying-code-threads.md) explains why instruction synchronization on the publishing core is not automatically broadcast to executing cores. Code publication must follow the target's actual cache and synchronization rules.

[RCU's quiescence principle](../../30-sources/mckenney-slingwine-1998-read-copy-update.md) is relevant to concurrent reference retirement, but does not replace translation, execution or device completion evidence.

## Proposed staged expansion

After the single-CPU M0–M4 proof, add a second Intel x86-64 vCPU on one virtual socket (two cores, one thread per core). Keep a serialized kernel design initially if it simplifies correctness, but do not claim that one global lock eliminates cross-core stop, interrupt, translation or user-execution races.

Define boot and shutdown participation for each CPU, interrupt ownership, per-CPU stacks/state, scheduler accounting and cross-core notification. Record all shared structures and the lock/atomic/memory-order rules protecting them.

Next exercise two virtual sockets when needed, and explicit NUMA nodes/memory placement as a separate test. Do not equate sockets with NUMA or guest topology with host affinity. Qualify the lab CPU, board, firmware and device inventory before matching its full topology. Physical single-CPU bring-up need not wait for any of these tests. A later materially different ISA, such as RISC-V or AArch64, remains an unselected portability experiment.

A second emulator configuration is useful evidence of architectural adaptation; it does not validate physical power behavior, DMA interconnect ordering, cache effects or timing bounds.

## Stop, shootdown and publication obligations

Domain closing must prevent every CPU from returning to old user state. Track which CPUs can hold an address space, which have acknowledged a stop/invalidation request, and what prevents a late entrant from using an already retired generation.

Do not free page tables or physical pages until the relevant translation and execution obligations are satisfied. Define software address-space generation reuse and wrap rules and test them with a small identifier space. PCID is optional, not an assumed baseline; if enabled later, include its hardware reuse and invalidation obligations.

If code remains immutable after initial installation, exploit that restriction but still synchronize initial publication before execution. If later patching or module replacement is enabled, specify instruction-cache maintenance and executing-core synchronization independently of data visibility.

Preserve all enabled context state at migration and traps, including floating-point/vector state if admitted. Revisit ABI alignment, atomics, memory ordering, page sizes and exception return on the second ISA; a generic register array is not sufficient evidence.

## Acceptance and next exploration

Run two CPUs with forced preemption during capability revocation, page unmapping, domain stop, timer cancellation and identifier reuse. Delay acknowledgements and simulate an unresponsive CPU. The safe response may be to stop reclamation or reset, not to declare a timed-out shootdown successful.

Use architecture-appropriate memory-model litmus tests alongside executable lifecycle models and guest stress tests. Retain exact compiler, atomic implementation and hardware/emulator configuration.

Repeat the relevant CLI, protection, IPC, GC and recovery corpus on the qualified physical T7500, and later on any selected second ISA. Report which assumptions changed and which tests no longer exercise the same path.

The next artifact after M4 is the two-CPU stop/shootdown protocol. No SMP correctness, second-ISA port or physical-hardware validation was performed here.

## Connections

[Entry and user return](privilege-entry-memory-and-user-return.md), [time](time-preemption-and-cpu-budgets.md), [lifecycle](domain-lifecycle-and-safe-reclamation.md) and [DMA](dma-driver-isolation-and-recovery.md) all acquire additional completion obligations.
