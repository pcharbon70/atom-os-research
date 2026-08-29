---
title: "Zig is the kernel implementation language"
kind: note
created: "2026-08-29"
maturity: stable
tags:
  - c-interop
  - kernel-development
  - operating-systems
  - programming-languages
  - simd
  - systems-architecture
  - zig
aliases:
  - "Kernel implementation language"
  - "Zig kernel language decision"
---

# Zig is the kernel implementation language

## Decision

Effective 2026-08-29, **Zig is the base implementation language for the new
kernel and its native operating-system substrate**. This is a settled project
decision. It is not a tentative preference, a request for another comparative
language study, or a claim that Zig is universally superior for kernels.

Future architecture research and implementation should work within this
constraint. Rust, C, C++, and kernels written in those languages remain useful
comparison evidence, but they are not parallel candidates for the project's
default implementation. This decision is superseded only by another explicit
project-level decision; experimental difficulty must be recorded and addressed
rather than silently changing the base language.

The note is marked stable because the decision itself is final for current
project work. The toolchain policy, target support, safety profile, and kernel
architecture remain subjects for development and experiment.

## Scope

| Area | Language policy |
| --- | --- |
| Privileged kernel | New scheduling, memory, capability, IPC, time, interrupt, boot, recovery, and protection-domain code is Zig. |
| Architecture support | Use Zig wherever it can express the required semantics; keep assembly to the smallest reviewed entry, context, or instruction sequences that require it. |
| Native drivers and runtime support | New project-owned code is Zig and should normally live in the least privileged domain that can do its job. |
| Existing C components | Import headers, compile sources, or link objects through an explicit Zig/C boundary. Inventory host assumptions and treat the C side as unsafe native code. |
| Existing C++ components | Avoid making C++ ABI details part of the system contract. Put unavoidable upstream or vendor code behind a C ABI or another narrow adapter. |
| Managed actors and services | Their source language, instruction format, and compatibility model remain separate decisions. Zig is the substrate language, not a mandate for application code. |
| Research tooling | Host-side scripts, validators, generators, and analysis tools may use an appropriate host language. |

An upstream ERTS or AtomVM experiment does not contradict this rule. Their
existing C implementation can run as an imported compatibility component or
protected runtime domain, while the new kernel, substrate, adapters, and
project-owned native mechanisms remain Zig.

## Why Zig fits this architecture

The official [Zig language documentation](../30-sources/zig-project-2026-language-documentation.md)
supports four properties that align with the work ahead:

1. **C is an integration boundary rather than a separate toolchain.** Zig can
   import C headers, use C-compatible primitive types, compile C sources, and
   export C ABI symbols. That makes incremental use of hardware headers,
   firmware interfaces, vendor code, and selected ERTS or AtomVM components
   practical without choosing C for new kernel code.
2. **Resource effects are visible.** Zig documents no hidden allocation or
   control flow, makes allocation an explicit allocator dependency, and treats
   allocation failure as an ordinary condition to handle. Those properties fit
   a kernel that must make ownership, budgets, and failure paths inspectable.
3. **Freestanding and cross-target work are first-class use cases.** The
   standard library can be used selectively on freestanding targets, and the
   compiler and build system are designed to target machines other than the
   host. Exact support still has to be verified for the selected board and CPU.
4. **Low-level facilities remain directly expressible.** Compile-time
   evaluation, explicit layouts, inline assembly, and `@Vector` provide tools
   for register descriptions, generated tables, architectural seams, and
   portable SIMD-aware routines while retaining an escape hatch for exact
   instructions.

Zig also fits the intended layer boundary. A small native kernel can remain
explicit and auditable, while the much cheaper actor abstraction, garbage
collection, supervision, and application code live above it. Selecting Zig
does not collapse kernel threads, protected domains, and managed actors into
one execution model.

## Accepted costs and non-guarantees

Choosing Zig accepts responsibilities that the language does not discharge for
us:

- memory reclamation and lifetime correctness remain manual design concerns;
- imported C retains its memory hazards and any hidden libc, allocator,
  threading, syscall, firmware, or operating-system assumptions;
- runtime safety checks depend on build mode and can be disabled, so production
  safety policy must be explicit rather than inferred from the language name;
- concurrency races, deadlocks, priority inversion, capability mistakes,
  unbounded queues, and incorrect recovery policy remain architectural bugs;
- portable vector expressions do not guarantee one instruction sequence or
  portable performance, and SIMD state still has to be enabled, isolated, and
  preserved by the kernel; and
- compiler, linker, target, and ABI behavior must be pinned and tested for each
  supported platform.

The ability to import C must not become permission to import an accidental host
operating system. Every reused component still needs a dependency census,
privilege placement, failure model, resource accounting policy, and replacement
or containment plan.

## Consequences for implementation

The first implementation baseline should:

1. pin an exact Zig release, distribution checksum, target triple, CPU feature
   baseline, linker configuration, and reproducible build invocation;
2. boot a minimal Zig kernel on the selected emulator or board with the reset,
   entry, linker, stack, panic, and console contracts documented;
3. define kernel allocators and out-of-memory behavior without an implicit
   libc heap;
4. establish reviewed rules for unsafe pointer operations, volatile MMIO,
   packed and external layouts, inline assembly, and C ABI crossings;
5. prove one real C-header and C-object integration path while enumerating the
   component's target flags and host dependencies;
6. define scalar, floating-point, and SIMD context policy before allowing such
   instructions in pre-emptible or interruptible code; and
7. test every architectural mechanism in safety-enabled builds, then justify
   any locally disabled check with measurement and a recorded invariant.

These tasks validate how Zig will be used. They do not decide whether Zig will
be used.

## Connections

- The [home map](../10-maps/home.md) treats this note as a settled project
  constraint.
- The [BEAM, ERTS, and OTP synthesis](beam-erts-and-otp-principles-for-a-new-operating-system.md)
  places the Zig kernel beneath the managed actor and OTP-like service layers.
- The [kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
  continues to test which mechanisms belong in each layer, using Zig for new
  native implementation work.
- The [AtomVM assessment](atomvm-as-an-operating-system-foundation.md) treats
  AtomVM's C core as an optional imported runtime rather than a reason to write
  a new C kernel.

## Sources

- [Zig 0.16.0 language documentation](../30-sources/zig-project-2026-language-documentation.md)
