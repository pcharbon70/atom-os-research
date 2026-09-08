---
title: "C kernel language feasibility and low-level compatibility"
kind: note
created: "2026-09-08"
maturity: developing
tags: [c-language, kernel-language, freestanding, x86-64, proof-of-concept]
aliases: ["C kernel feasibility assessment"]
---

# C kernel language feasibility and low-level compatibility

## Conclusion and decision boundary

C is technically feasible for the Dell Precision T7500 kernel. No fundamental
language/toolchain facility gap was identified for our minimum Intel x86-64
boot, protection, interrupt, scheduling, memory and CLI substrate. The practical
implementation is **C plus a documented compiler-extension profile, audited
assembly, startup/linker support and a small explicit runtime-support layer**,
not portable ISO C alone.

This assessment does **not** replace the user's selected Zig language.
It evaluates C as an alternative primary language and as the existing C
interoperability/fallback path. The [Zig assessment](zig-kernel-language-feasibility-and-c-interoperability.md)
and recorded language decision remain in force. Changing the primary language
requires an explicit decision; this research does not authorize implementation
or reopen every milestone.

Evidence is sufficient to begin bounded qualification, not to declare a
bootable, safe or performance-qualified C kernel. We locally verified a narrow
GCC/Clang C ABI path and freestanding code generation/linking, and deliberately
demonstrated a missing compiler helper. We did not boot QEMU or the physical
machine, execute privileged instructions, qualify arbitrary libraries, or
complete M0.

## Question, scope and evidence standard

“C-level compatibility” has four distinct meanings:

| Contract | What it establishes | What it does not establish |
| --- | --- | --- |
| Language/source compatibility | A selected dialect accepts the component and its extensions | Compatible binary layout or correct source semantics |
| Procedure ABI compatibility | Agreed symbols, types, argument/result passing, stack and register use | Hardware interrupt entry or a syscall protocol |
| Freestanding dependency compatibility | Every emitted call and required service has an admitted implementation | A safe allocator, driver or recovery policy |
| Execution compatibility | Code meets the actual privilege, CPU, concurrency and resource contract | Evidence for untested targets or configurations |

The operational test is whether a pinned implementation can produce
dependency-closed images and preserve the existing PoC contracts under ordinary
and adversarial execution. We distinguish official specifications, reported
research, practitioner accounts, local observations and our proposed controls.
The [journal](../../50-journal/2026-09-08-c-kernel-feasibility-deep-dive.md)
contains the claim ledger, search scope, exact new/reused source manifest and
reproduction limits.

The [T7500 target profile](dell-precision-t7500-target-and-minimal-qemu-profile.md)
remains authoritative: Intel Xeon/Intel 64, initially the minimal Nehalem-v1
QEMU fixture with one CPU, 128 MiB and serial I/O. Compiler `nehalem` selection
and QEMU's named CPU model are different interfaces that must be reconciled.
The installed Xeon SKUs, firmware and devices are unverified. q35 is a test
platform, not a faithful T7500 motherboard replica. No AMD-specific feature,
AtomVM path or graphical UI enters this assessment.

## What C provides—and what the kernel must provide

### A useful freestanding language, not a built-in operating system

The [C11 public draft](../../30-sources/wg14-2011-c11-committee-draft.md)
permits an environment without an OS, with implementation-defined startup.
It does not promise a hosted libc, threads, files or a conventional `main`.
The minimum C11 freestanding headers do not include `stdatomic.h`; support
must be checked rather than inferred.

[ISO's catalogue](https://www.iso.org/standard/82075.html) identifies C23 as
ISO/IEC 9899:2024, published October 2024. The
[public-draft/status record](../../30-sources/iso-wg14-2024-c23-status-and-draft.md)
separates that fact from N3096's earlier expanded freestanding provisions.
We did not read the paid final standard. Neither C23 branding nor a compiler's
latest default is an accepted project profile.

C offers explicit data representation, pointers, function pointers, separate
compilation and compile-time layout assertions. Our proposed coding subset
uses fixed-width interface fields, explicit ownership and bounded operations;
it does not rely on automatic bounds/lifetime checking or tracing collection.
Macros and conditional compilation should remain behind small architecture
or compiler adapters. Avoid evaluating side-effecting arguments repeatedly
and use typed functions where possible.

A reasonable **candidate**, if C is selected, is GNU C11 with a small enumerated
extension allowlist. C17 is another possible baseline, but changing modes must
be tested. The local probes explicitly used `-std=gnu11`; this is not a claim
that every C11 construct was qualified. [Linux's own profile](../../30-sources/linux-community-2026-kernel-c-dialect.md)
is evidence that an engineered GNU C11/GCC/Clang kernel is practical, not a
license to copy Linux's flags, APIs or memory model.

### Required low-level facilities

| Required mechanism | C/toolchain route | Atom's unresolved responsibility |
| --- | --- | --- |
| Boot and C startup | Assembly entry, linker-defined regions, freestanding C entry function | Bootloader handoff, stack/alignment, initialized data/BSS, mapping and processor state |
| Port I/O and CPU control | GNU-style inline assembly or external assembly | Correct operands/clobbers, privilege, register/MSR semantics and feature checks |
| MMIO and descriptor fields | Explicit-width accessors, volatile where appropriate, masks/shifts | Mapping/cache type, access width, ordering and device-specific protocol |
| Exceptions and interrupts | Assembly stubs or qualified compiler interrupt attributes | Exact frame/error-code ABI, IDT/TSS/IST, nesting, acknowledgement and safe return |
| Context switching and syscalls | Assembly boundary plus C policy | Full state ownership, user/kernel stack changes, argument validation and return constraints |
| Page tables and allocation | C data structures with explicit address/size types | Provenance assumptions, checked arithmetic, page ownership, permissions and reclamation |
| Atomics and synchronization | Qualified C atomics or compiler builtins | Exact widths/alignment, lock-free helper closure, IRQ rules and progress bounds |
| Console, timers and CLI services | Small C/assembly hardware backend; bounded service interfaces | Actual UART/timer behavior, user-mode CLI separation and fault isolation |
| BEAM execution and tracing GC | Implementable in C, but not supplied by C | Declared compiled-BEAM profile and automatic process-local tracing GC outside ring 0 |

The [Intel architecture source](../../30-sources/intel-2026-system-programming-documentation.md)
governs hardware transitions. Language features cannot substitute for those
contracts. In particular, saving ordinary C callee-saved registers is not a
complete interrupted-context save.

[GCC's versioned x86/assembly contracts](../../30-sources/gnu-project-2026-x86-kernel-c-profile.md)
and [Clang's interrupt contract](../../30-sources/llvm-project-2025-clang-x86-interrupt-contract.md)
support the necessary mechanisms with constraints. Same-stack interruptible
kernel code must exclude the red zone; general-register-only compilation
must cover relevant callees/helpers while FP/SIMD ownership is unavailable.
An error-code exception needs the corresponding signature. An empty function
that emits `iretq` does not establish a valid installed handler.

Keep stack-changing entry/context-switch assembly separate from ordinary
extended asm. Describe every operand, register/flags change and memory effect.
A `"memory"` clobber constrains the compiler, not CPU speculation. Do not use
a naked C function as permission to mix arbitrary C with an unmanaged stack.

The code model must match the actual linker layout. GCC's
`-mcmodel=kernel` describes negative-2-GiB placement; it is not a generic
“kernel mode” switch. Our low-address research link did not use it.

### Volatile, atomics and ordering are different contracts

Use volatile-qualified access only as one part of a hardware-access contract.
It does not make shared state atomic or order unrelated ordinary accesses.
Do not assume volatile bitfields issue the exact device transaction intended.
Use masks and explicit access widths, with register-specific ordering.

Atomic operations can lower to helper calls when the target/type cannot
support an inline sequence. Qualify size, alignment and generated code; reject
undeclared `libatomic` dependencies in critical paths. A compile-time lock-free
check is useful, but lock-free does not imply wait-free or a bounded retry
count. IRQ reentrancy matters even before SMP.

These are proposed Atom rules derived from the GCC contracts above, not an
adoption of a hosted threading runtime. The kernel must define the interaction
between ordinary code, interrupt handlers, CPU memory ordering and later SMP.

## C ABI and library compatibility assessment

### Direct C calls are practical, but there is no universal C binary ABI

The [AMD64 procedure ABI](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md)
is the relevant shared ISA/ABI name for this Intel target. Select an explicit
LP64/SysV integer-only bring-up subset. Freeze structure size/alignment/offsets,
enum and scalar representation, linkage, calling convention and compiler
options. C interfaces should use opaque handles, explicit lengths and status
returns; prohibit casual casts between incompatible function-pointer types.

Avoid unqualified packed records, bitfields, varargs, floating/vector arguments
and cross-compiler LTO in the first boundary. They are not universally
impossible, but they expand the contract beyond our tested subset. Serialization
must define byte layout independently of native padding. Do not expose raw
kernel pointers as user authority.

The procedure ABI, boot handoff, CPU interrupt frame and Atom syscall ABI
are separate. A Linux-target compiler does not supply Atom's syscall interface.
Likewise, a callback that returns correctly on Linux says nothing about its
allowed blocking, allocation, cancellation, lifetime or interrupt context
inside the kernel. Those obligations remain with the component wrapper.

### Library admission is per component, not per language label

| Component category | Assessment | Required admission evidence |
| --- | --- | --- |
| Small pure-C algorithms | Strong reuse candidate | Target build, bounds/ownership review, dependency census and negative tests |
| Compiler support and memory primitives | Necessary when emitted or required by the compiler contract | Reviewed implementations, no recursive helper lowering, exact semantics and codegen audit |
| Newlib portions | Porting candidate, not free host services | Real bounded system hooks and reentrancy/allocator policy |
| musl as a whole | Not a drop-in libc for Atom | Its Linux syscall dependency would require a separate compatibility effort |
| Explicit freestanding LZ4 subset | Evidence that bounded C-library profiles exist | Version/macros, memory hooks, input limits and fuzzing; not selected here |
| Linux/BSD drivers or subsystems | Potential source reuse, not direct ABI reuse | Donor environment, locking, allocation, DMA, address and reset adapters |

[GCC freestanding support](../../30-sources/gnu-project-2026-gcc-freestanding-environment.md)
requires memory primitives and leaves startup/linking to the environment.
Its helper contract includes exact self-copy behavior for `memcpy`, so a
strict-ISO library slogan is not enough. [Clang's freestanding documentation](../../30-sources/llvm-project-2025-clang-21-freestanding.md)
also permits emitted memory calls and does not provide a complete freestanding
library. `-nostdlib` removes default support libraries, not generated demand.
Our `__udivti3` rejection makes this dependency visible.

The [Newlib hooks](../../30-sources/newlib-project-2026-libc-system-hooks.md),
[musl environment](../../30-sources/musl-project-2026-linux-dependency.md)
and [LZ4 freestanding profile](../../30-sources/collet-2024-lz4-freestanding-profile.md)
support different conclusions; none was built or ported during this session.
Stubbing every hook with success is not compatibility. Decide whether a
required allocator, clock, entropy source, thread, file or console operation
is truly supported, explicitly unsupported, or outside the admitted subset.

[OSKit's historical reuse work](../../30-sources/ford-et-al-1997-flux-oskit.md)
shows why interfaces need execution-environment adapters, not just matching
function declarations. Atom should prefer narrow unprivileged services for
larger imported code. Review component licensing and provenance before reuse;
no third-party implementation is vendored by this study.

## Safety, optimization and scientific evidence

C feasibility is not a memory-safety result. Our proposed kernel profile must
make allocation ownership, lifetimes, bounds, initialization, aliasing and
resource exhaustion explicit. Validate arithmetic before using its result to
form pointers or reserve memory. Do not treat signed overflow, excessive
shifts, stale pointers or incompatible typed accesses as ordinary hardware
behavior. Limit recursion and variable-size stack use; make error cleanup and
resource release reviewable.

The selected scientific evidence covers complementary risks:

- [Yang et al., PLDI 2011](../../30-sources/yang-et-al-2011-csmith.md) found over
  325 historical compiler defects using differential testing. It motivates
  pinned tools and minimized regressions, not a present-day compiler ranking.
- [Wang et al., SOSP 2013](../../30-sources/wang-et-al-2013-optimization-safe-systems.md)
  demonstrates how undefined behavior can undermine defensive checks.
  Its 160 confirmed/fixed bugs were not all exploited vulnerabilities.
- [Memarian et al., POPL 2019](../../30-sources/memarian-et-al-2019-c-pointer-provenance.md)
  makes numeric-address versus object/provenance assumptions explicit.
  The proposed semantics are research, not current universal compiler law.

[Lattner's original LLVM article](../../30-sources/lattner-2011-c-undefined-behavior.md)
explains the optimization mechanisms. [Desaulniers's engineering account](../../30-sources/desaulniers-2020-off-by-two.md)
provides a concrete, historical C/assembly compiler regression. Both are
author-written technical evidence, not independent certification.

[Sewell et al.'s translation validation](../../30-sources/sewell-et-al-2013-translation-validation.md)
and [Klein et al.'s verified microkernel](../../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
demonstrate that disciplined C systems can receive substantial assurance.
Their model, assembly, hardware and configuration boundaries do not transfer
to Atom. Disassembly inspection is not formal translation validation.

Proposed controls are hosted tests and analysis for portable components,
compiler/optimization differential checks, explicit checked arithmetic,
adversarial ABI/parser tests and separate guest/hardware validation. Sanitizer
instrumentation is a candidate hosted aid, not assumed kernel support; it was
not run here. Compiler flags addressing overflow or aliasing do not cure every
undefined behavior, and a sanitizer pass would not establish whole-kernel
correctness. Keep the privileged trusted code small in either language.

## Local evidence and its limits

[Retained fixtures and results](../../assets/c-kernel-feasibility/README.md)
use GCC 13.3.0, Clang 21.1.0 through installed Zig 0.16.0, and GNU ld 2.42.
The source is C; using `zig cc` is a Clang distribution route, not a test of
Zig language semantics. GCC is the installed Linux-target compiler with
explicit freestanding flags, not a qualified bare-metal cross-toolchain.

| Case | Observed result | Claim boundary |
| --- | --- | --- |
| C-R01: cross-compiler calls | GCC client/Clang object and Clang client/GCC object both passed record argument/result, layout assertions and callback checks | Hosted Linux execution; one small integer ABI |
| C-R02: freestanding link | Both compilers' selected objects linked as static ELF64 with no interpreter, dynamic section or unresolved symbols | Tiny dependency-closed fixture, not a bootable image |
| C-R03: architecture emission | Both emitted port output, explicit-width load, lock-prefixed atomic increment and interrupt return | Compile/disassembly only; no privileged execution |
| C-R04: omitted helper | Both wide-division objects imported `__udivti3`; linking without it failed as expected | Demonstrated dependency, not a supplied/qualified helper |
| C-R05: ambient defaults | First GCC output contained `endbr64`; explicit `-fcf-protection=none` removed it in the retained final run | Host defaults need audit; no assertion that the first bytes would fault |

The `research_entry` is only an assembly halt loop. It does not call a C
startup function, initialize memory or implement a boot protocol. No result
establishes IDT correctness, physical MMIO, page protection, context switching,
timing, SMP, reproducible builds or T7500 boot. Two runs used a changed flag;
they are not a same-input reproducibility test. Hashes identify observations,
not an accepted build closure.

## Relationship to the Zig decision

| Consideration | C assessment | Implication for our selected Zig path |
| --- | --- | --- |
| Existing C components | Direct compilation avoids a C-to-other-language source translator | Narrow C wrappers/objects remain available |
| Low-level escape hatches | Compiler extensions and assembly are sufficient in principle | Neither language removes hardware/ABI qualification |
| Memory discipline | Manual bounds, lifetime and ownership discipline is central | Zig checks do not protect arbitrary imported C |
| Engineering evidence | Extensive kernel practice and systems research, with documented failures | Evidence supports a fallback, not automatic superiority |
| Build qualification | Exact dialect/compiler/helper closure required | Both routes need pinned and tested inputs |

The [versioned Zig language record](../../30-sources/zig-project-2026-language-reference-0-16.md)
and earlier local assessment support this comparison. We have no controlled
C-versus-Zig kernel performance, defect-rate or development-time experiment.
There is no evidence here requiring a language change. If Zig qualification
encounters a reproducible blocker, first assess a bounded C/assembly component;
consider changing the primary language only with a recorded tradeoff decision.

## What to qualify next

These are research-derived acceptance inputs to the existing
[M0–M4 plans](../../60-planning/01-proof-of-concept/README.md), not a replacement
phased plan or newly completed work.

1. **M0: freeze the compilation and boundary contract.** Keep Zig selected
   unless the user changes it. For any C component, record compiler binary and
   support-library identities, dialect/extensions, target features, link model,
   optimization, red-zone/FP policy, stack protection and allowed imports.
   Expand layout/callback tests; test helper closure, bad imports and memory
   primitives; compare clean builds in different paths.
2. **M1: demonstrate assembled privileged execution.** Verify initialized
   data/BSS and stack alignment, then real exception/IRQ frames, register
   preservation, safe user return, timer progress and the native user-mode CLI.
   Include wrong/error-code frames, invalid user input and fault diagnostics.
   The physical T7500 requires a separately recorded inventory and boot check.
3. **M2: test authority and lifetime.** Exercise bounds, stale handles, allocator
   exhaustion, cancellation, IRQ reentrancy and teardown/reuse. C does not
   supply capability enforcement or protect ring 0 from a bad pointer.
4. **M3: preserve the managed execution requirement.** A native C kernel or
   CLI is not compiled-BEAM compatibility. Implement and test the declared
   runtime profile and process-local tracing collector outside the kernel;
   account for native-service allocation and blocking.
5. **M4: measure the composition.** Run the declared recovery, fault and
   resource campaign against identified binaries and capacities. Compiler
   upgrade, changed ABI or helper implementation reopens affected evidence.

Next research should be driven by a failing qualification case or an actual
candidate library's dependency audit. Another broad language survey is not
needed before beginning that bounded work. The open
[C qualification inquiry](../../40-inquiries/can-c-meet-the-kernel-qualification-contract.md)
tracks this distinction between feasibility and demonstrated correctness.

## Connections and evidence route

- [Zig versus C comparison](zig-versus-c-kernel-language-comparison.md) — direct tradeoffs, recommendation and decision sensitivity.
- [C kernel-development map](../../10-maps/c-kernel-development.md) — selective reading route.
- [Freestanding build and static images](freestanding-build-and-static-images.md) — active R02 contract.
- [Privilege entry and user return](privilege-entry-memory-and-user-return.md) — hardware isolation obligations.
- [Source manifest and claim ledger](../../50-journal/2026-09-08-c-kernel-feasibility-deep-dive.md) — exhaustive provenance, method and observed evidence.
