---
title: "Privilege entry, memory protection, and user return"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - boot
  - proof-of-concept
  - requirements
aliases: []
---

# Privilege entry, memory protection, and user return

Requirement R03, M1–M2. The first CLI delivery must execute in a real user protection domain. Atom's kernel must own page allocation, mappings, trap entry and validated return, even when only one user program exists.

## Evidence and architectural choice

The [active T7500 / Intel x86-64 profile](dell-precision-t7500-target-and-minimal-qemu-profile.md) selects ring 0 for the kernel and ring 3 for services. The [Intel system-programming study](../../30-sources/intel-2026-system-programming-documentation.md) is the primary architecture reference. Qualify entry/context sequences and the installed Xeon's family-specific errata before coding; a modern manual does not make every feature available on an older CPU. Interrupt gates, syscall instructions and return instructions have different frame and stack semantics. Do not transplant the earlier xv6/RISC-V trap sequence: define GDT/IDT/TSS ownership, kernel/exception stacks and the selected entry mechanism explicitly.

The [AMD64 procedure ABI](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md) is useful for calls from assembly to compiled code. Its callee-save convention is not enough for interruption at an arbitrary instruction; interrupted code may own every live register.

For the first Atom profile, choose one documented mapping arrangement: a minimal supervisor-only entry mapping present in user address spaces, followed by a switch to the kernel table, is an understandable baseline. A shared kernel mapping can simplify entry but increases the privileged alias surface and later mitigation obligations. Neither arrangement establishes resistance to speculative attacks; the current PoC threat profile does not claim that protection.

## Proposed memory and context contract

Seed a fixed page allocator from the validated boot snapshot. Track each page as reserved, free, staged, mapped, closing or quarantined, with one accountable owner. The first CLI has immutable executable code, separate writable nonexecuting data and stack, and a bounded memory grant. Stack guards must remain unmapped. Firmware, kernel data, page tables and MMIO must never acquire user access through a convenient identity map.

Store saved contexts and trap frames in kernel-owned memory. The user can influence register values but cannot choose the record's owner, address-space identity or privilege metadata. Before calling ordinary kernel code, entry assembly establishes an aligned stack, preserves interrupted state, records the trap cause and origin, and follows a bounded nesting policy.

One return gate validates canonical user PC/stack addresses, selectors and allowed RFLAGS, the intended page-table/address-space generation, pending domain closure and feature-state policy. Select and audit an IRETQ-based path or another explicit mechanism; do not assume SYSRET and interrupt return have identical fault behavior. A domain closed while servicing its syscall must not return to user execution. Final return must select user privilege and the intended interrupt state, and must not trust a user-supplied raw status word.

Use an explicit policy for FP/vector state: prevent its use in the initial restricted profile, or implement full initialization and context ownership. Merely compiling the kernel without floating point does not constrain a native user image. Validate admitted binaries and trap unsupported use.

## User-memory access

Specify length limits and overflow-safe range checks on every console and information call. Stage each small input in kernel-owned bounded storage before acting on it. This avoids repeated reads of a mutable user descriptor. Check every covered page for the required direction of access; a valid first byte does not validate a range spanning an unmapped page.

The single-core profile simplifies concurrent mutation but does not remove interruption, mappings changed through system calls, or later sharing. Either pin the accepted range until the copy completes or use a fault-aware copy primitive with a defined partial-copy result. No kernel decision should be made from half of a descriptor.

Mapping removal requires closing access and completing local translation invalidation before page reuse. Delayed timer, endpoint or saved-frame references are separate obligations handled by [domain reclamation](domain-lifecycle-and-safe-reclamation.md). Changing a page-table entry is not itself evidence that all old authority has disappeared.

## Acceptance and next experiments

Construct user programs that attempt privileged instructions, kernel reads/writes, execution from data, writes to text, stack overflow, invalid syscalls and cross-page user buffers. Compare kernel and neighboring-domain canaries before and after each operation. A denied request must not corrupt state even when fault logging is full.

Exercise timer interruption during syscalls and on the final return path. Fill registers with domain-specific patterns, switch domains, and check for leakage of every enabled state component. Fault before and after context installation to test staged rollback.

Retain a debugger trace showing the CLI PC at CPL 3 and the syscall handler at CPL 0. A prompt alone does not establish this boundary. The first accepted artifact is a minimal entry/return implementation and negative protection corpus; wider portability and hardware-channel claims remain open.

## Connections

[Static image admission](freestanding-build-and-static-images.md) decides what can run. [Capability ABI](capabilities-syscalls-and-bounded-ipc.md) decides what running code can request. The existing [entry/context study](../kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context.md) supplies the broader multi-ISA contract.
