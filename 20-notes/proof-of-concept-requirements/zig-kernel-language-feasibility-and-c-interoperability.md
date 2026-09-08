---
title: "Zig kernel language feasibility and C interoperability"
kind: note
created: "2026-09-08"
maturity: developing
tags: [zig, kernel-language, interoperability, proof-of-concept, x86-64]
aliases: ["Zig kernel feasibility assessment"]
---

# Zig kernel language feasibility and C interoperability

## Decision and assessment

**Use Zig as the kernel implementation language, as selected by the user on
2026-09-08. It is feasible enough to begin the bounded M0 qualification work.**
Small C components and assembly are credible escape hatches where they reduce
risk or supply missing mechanisms. This conclusion is **not** a certification
of Zig, approval of a particular library, or evidence that our OS already boots.

The strongest evidence is the combination of versioned language/compiler
documentation, primary low-level implementations, two relevant peer-reviewed
papers, and our own limited compile/link and hosted interoperability probes.
The assessment found no language-level blocker to the planned kernel. The main
risks are compiler/version churn, unsafe lifetime and concurrency behavior,
nonordinary CPU entry/exit, and accidental hosted-library dependencies.

The language choice is accepted. **Zig 0.16.0 is the researched and locally
tested candidate, not yet the accepted M0 toolchain pin.** Compiler distribution,
backend, linker, translator, image layout, enabled processor state, repository
and acceptance ownership still need decisions and qualification.

This study extends [R02: freestanding build and static images](freestanding-build-and-static-images.md).
It does not replace the [M0–M4 plan](../../60-planning/01-proof-of-concept/README.md).

## Scope and standard of evidence

The target remains the [Dell Precision T7500 / Intel x86-64](dell-precision-t7500-target-and-minimal-qemu-profile.md).
Initial guest tests must use the planned versioned q35/SeaBIOS/TCG,
`Nehalem-v1`, one CPU, 128 MiB and serial fixture. A compiler CPU name is not
a bit-for-bit match to a QEMU CPU model; reconcile their feature sets.
M0 must qualify that fixture before acceptance. The installed Xeon SKUs and
physical firmware/device inventory remain unknown.

“Feasible” means we can express the required low-level operations, produce
freestanding native artifacts, define testable foreign-function boundaries,
and identify how remaining dependencies will be supplied. It does not mean
memory safety, real-time bounds, complete C compatibility or hardware support
are already demonstrated.

Evidence is separated as follows:

- **Documented:** versioned language/build/ABI contracts.
- **Reported:** papers and author-maintained implementations, with their original
  compiler, platform and evaluation limits.
- **Observed locally:** the exact small fixtures and transcript in the
  [research assets](../../assets/zig-kernel-feasibility/README.md).
- **Proposed:** the Atom policies and qualification tests below.

The [session journal](../../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md)
contains search scope, source provenance, commands, failed/limited observations
and remaining gaps. This is a targeted engineering deep dive, not an exhaustive
systematic literature review.

## What Zig brings, and what it does not

The [0.16 language reference](../../30-sources/zig-project-2026-language-reference-0-16.md)
provides explicit allocation, compile-time computation, optional values, error
unions, layout controls and assembly. Debug/ReleaseSafe enable safety checks
that ReleaseFast/ReleaseSmall normally disable. Those checks do not establish
general lifetime or race safety. Zig does not provide automatic tracing GC
or Rust-style ownership enforcement. Volatile accesses address side-effectful
memory access, not synchronization.

**Our design inference:** these facilities fit explicit kernel resource
ownership well, but kernel invariants must still be designed and tested.
Use error returns for expected exhaustion or malformed requests. Reserve panic
for violated internal invariants, with a bounded failure path that does not
allocate, wait for a held lock or depend on a functioning user service.
The probe's trap-only panic is a compile fixture, not the future diagnostic
or recovery policy.

Compile-time generated descriptor tables and typed wrappers may reduce
duplication. They do not prove that descriptor bits, stack transitions,
capability checks or reclamation are correct. Inspect generated output when
the abstraction hides a privileged operation.

Manual kernel memory management does **not** weaken the project's BEAM
requirement. The automatic process-local tracing collector remains part of
the later unprivileged managed runtime. Kernel-language selection does not
choose the runtime implementation or turn BEAM instructions into a kernel ABI.

## Low-level feasibility by kernel responsibility

The [tagged compiler/runtime profile](../../30-sources/zig-project-2026-freestanding-source-profile.md)
and our compile-only probes establish available mechanisms. The last column
is proposed Atom work, not upstream functionality.

| Responsibility | Evidence and feasibility | What Atom must still own and test |
| --- | --- | --- |
| Freestanding code and ELF | Zig and C objects linked locally without a hosted runtime or unresolved symbols | Real boot entry, linker script, reservations, BSS, relocation rules, permissions and full helper census |
| Port I/O and machine instructions | Local Zig assembly emitted `out`, `cli` and `hlt`; external assembly can be linked | Exact operands/clobbers, compiler ordering, privilege preconditions, bounded UART policy and hardware qualification |
| MMIO and hardware tables | Volatile read compiled to a load; explicit layouts support structured descriptions | Access width/alignment, mapping/cache attributes, reserved bits and device-specific ordering |
| Interrupts and exceptions | Primary Ymir implementation shows Zig/assembly dispatch; compiler exposes naked and interrupt conventions | Error-code normalization, all interrupted state, stack alignment, nesting, known-good fault stacks and validated return |
| Paging and isolation | Integer/pointer operations and assembly can express the mechanisms | Frame ownership, checked mappings, invalidation, W^X and user-buffer validation |
| Time, scheduling and preemption | No special language runtime is required for native control structures | Timer calibration, interrupt latency, context ownership, non-yielding-domain budgets and progress |
| Atomics and synchronization | Local u64 atomic increment emitted `lock xadd` | Ordering proof, lock discipline, IRQ reentrancy, memory-reuse protocol and later SMP tests |
| Bootstrap allocation | Installed fixed-buffer allocator accepts caller-owned storage | Accounted page/slab allocation, exhaustion behavior, bounded metadata and reclamation |
| Native service interface | Mixed-language scalar, aggregate and callback probe passed on the host | Versioned syscall/IPC ABI, capability validation, buffer ownership, cancellation and safe domain teardown |
| Diagnostics and testing | Local builds preserved symbols/disassembly; compiler supports custom panic | Serial diagnostics independent of heap/services, stack bounds, fault injection and exact-run evidence |

### Keep the architecture boundary small

Our recommendation is a narrow x86-64 boundary for entry, register access,
interrupt return and context switching, implemented in audited Zig assembly
or separate assembly files. Ordinary kernel policy stays in Zig.

Do **not** use `callconv(.kernel)` for an x86 OS: the inspected compiler defines
that name for GPU compute. Use the selected native procedure convention for
ordinary calls and separately specified assembly/trap interfaces.
A naked function supplies no ordinary prologue/epilogue. Merely naming an
interrupt convention cannot establish safe user-to-kernel transitions.

The [SysV AMD64 ABI](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md)
is a procedure contract, not our syscall ABI or an interrupted-context format.
Exclude the kernel red zone. Decide FP/SIMD ownership explicitly; compiling
integer source for Nehalem does not guarantee that every generated helper is
integer-only. A restricted initial profile must be named as such, not described
as full psABI support.

Use [Intel architecture documentation](../../30-sources/intel-2026-system-programming-documentation.md)
and the actual Xeon family/errata when implementing privileged transitions.
This study did not complete a processor-specific sequence audit. Do not import
modern CPU features or a UEFI tutorial's boot assumptions into the SeaBIOS fixture.

One executing CPU does not eliminate concurrency: IRQ entry can interrupt a
lock holder. Likewise, `-fsingle-threaded` is an optimization assumption, not
a substitute for an interrupt/preemption policy. Leave such assumptions
explicit and test them before relying on them.

## C compatibility: four separate questions

**Yes, Zig can call C and C can call Zig. No, that does not make every C
library directly usable inside this kernel.** Keep these distinctions visible:

| Compatibility question | Assessment | Boundary policy |
| --- | --- | --- |
| Function-call ABI | Supported by documented extern/export conventions and the local mixed GCC/Zig callback test | Use explicit C-compatible exports and callback signatures; never expose an internal Zig ABI as stable |
| Memory layout | Extern aggregates provide the target C layout; local size/alignment/offset assertions passed | Verify every public record in both languages; prefer fixed-width integers and opaque handles |
| Header/source translation | Available, but incomplete and changing in 0.16 | Pin translator, target, defines and include closure; inspect generated declarations |
| Library execution environment | Depends on the individual component | Audit allocation, locks, TLS, I/O, clocks, entropy, startup, helpers and failure paths |

### A deliberately small foreign interface

Proposed first boundary: fixed-signature functions; fixed-width integers;
pointer-plus-length buffers with documented validity/lifetime; explicit status
codes; simple extern records or opaque handles. Use C-compatible callback types
and define who may retain or invoke each callback.

Do not pass Zig slices, error unions, unspecified-layout records, allocator
objects or managed terms directly over a public C ABI. Translate them into
an explicitly versioned representation. Do not propagate language-specific
unwinding or `longjmp` across ownership/lock boundaries; fixed return-based
failure is the initial policy.

C bitfield layout is not guaranteed by replacing it with a Zig packed struct.
Compile the C record/accessor implementation and expose an opaque handle when
layout cannot be audited reliably. The [release-linked translator source](../../30-sources/zig-project-2026-c-translator-limits.md)
demotes bitfield-containing records and rejects several complex statement
forms. A translation failure is not necessarily a linking failure.

Variadic interfaces, unusual aggregate classification, long double, vectors,
TLS, C++ ABI and exception integration are **not qualified by our probe**.
Use fixed C wrapper functions before admitting these features. C++ reuse, if
ever needed, should first expose a narrow C surface and separately account
for constructors, allocation and exception/runtime dependencies.

### Version-sensitive integration traps

The [0.16 release record](../../30-sources/zig-project-2026-release-0-16.md)
deprecates but retains `@cImport`, replaces libclang translation with Aro, and
points toward build-system translation. Prefer `b.addTranslateC` or a pinned
official translator package for new build integration; do not treat an older
tutorial as current syntax or silently follow master documentation.

Our local `zig translate-c` run emitted the expected record and function
declarations, but also deferred `@compileError` declarations for untranslatable
macros. Translation command success is therefore not proof that every exposed
declaration can be used. This session did not compile a consumer of every
generated declaration.

The installed compiler rejected bare `-femit-h` as currently broken. Maintain
an audited C header and layout/call fixtures instead of depending on automatic
header generation. This is a measured limitation, not a reason to abandon C
interop. The versioned reference still contains examples that imply this
workflow works; the actual compiler result controls our candidate assessment.

## What can be reused from C?

| Component class | Example evidence | Proposed treatment |
| --- | --- | --- |
| Pure algorithms with caller-owned buffers | [LZ4's explicit freestanding subset](../../30-sources/collet-2024-lz4-freestanding-profile.md) | Smallest plausible fallback; inspect bounds, helpers, licenses and selected API. LZ4 itself is not selected. |
| Portable libraries with OS hooks | [Newlib's documented system dependencies](../../30-sources/newlib-project-2026-libc-system-hooks.md) | Port only needed hooks with bounded contracts; reject unsupported behavior instead of inventing success. |
| Linux-targeted libc/application code | [musl's Linux syscall dependency](../../30-sources/musl-project-2026-linux-dependency.md) | Not directly usable; static linking does not remove Linux semantics. A Linux compatibility layer is outside this PoC. |
| Platform drivers or full runtime subsystems | Their original OS/platform must supply the surrounding contracts | C syntax is insufficient. Inventory scheduling, IRQ, DMA, locking, mapping, allocation and teardown before estimating a port. |

A missing instruction wrapper usually calls for a small assembly primitive,
not a large C library. A missing driver usually calls for device-specific
implementation and tests, not a different language.

For each prospective C fallback, record its exact revision/license, exposed
header, target/defines, transitive symbols, memory ownership, permitted calling
context, failure/cancellation policy and tests. Prefer placing substantial
services outside ring 0 when compatible with the architecture. Foreign code
inside the kernel shares its privilege and failure domain.

[Clang's freestanding contract](../../30-sources/llvm-project-2025-clang-21-freestanding.md)
still permits generated memory-helper calls. Compiler-support libraries are
separate from libc. Supply audited required helpers or fail the link; disabling
implicit compiler-rt is not a universal solution. The successful tiny fixture
does not prove a larger allocator, parser or runtime is helper-free.

## Standard-library and build policy

Treat `std` as a collection to qualify, not an OS abstraction that is already
ported. Pure algorithms and caller-buffer utilities are candidates. Default
heap, threading, files, sockets, entropy and clock backends must not silently
supply host assumptions. The 0.16 I/O interface creates a possible adapter
boundary; it does not supply Atom's implementation.

For M0, propose:

1. A checksum-pinned Zig distribution and standard library, explicitly selected
   codegen backend and linker. Start qualification with 0.16.0 and LLVM
   (`-fllvm`), because that is what our probes exercised. This is a candidate
   policy, not proof that LLVM is bug-free or the alternative backend unsuitable.
2. A freestanding Intel x86-64 target, explicit CPU-feature list, red-zone
   exclusion, image/code model, stack support, unwind/debug and FP/SIMD policies
   applied consistently to every Zig, C, assembly and helper object.
3. A small custom panic path; explicit allocator injection; no kernel dependence
   on hosted I/O or libc. Decide which stack checks/protection can operate
   correctly before enabling or disabling them.
4. A link map, relocation/segment/symbol census and disassembly review that
   reject undeclared dependencies. Preserve symbols tied to the executed image.
5. Controlled clean builds with paths, timestamps, environment, dependencies
   and generated translator tools pinned. Re-run ABI/codegen regressions for
   upgrades, then re-run the affected M0–M4 gates.

The research fixture intentionally uses a simple low-address link, not the
eventual kernel code model or boot linker script. Its ELF includes unwind
metadata. It is evidence for object/link interoperability, not the accepted
image policy.

## Scientific and practitioner evidence

Two peer-reviewed works materially inform the conclusion:

- [Groce et al., CC 2022](../../30-sources/groce-et-al-2022-no-fuss-compiler-fuzzing.md)
  found historical Zig compiler crashes through fuzzing. This supports a
  compiler-regression discipline; it does not quantify 0.16.0 safety or
  demonstrate kernel miscompilations.
- [Kacs et al., SC-W 2024](../../30-sources/kacs-et-al-2024-zig-openmp.md)
  integrated a modified Zig 0.10.1 compiler with a C runtime and C/Fortran
  benchmark components. It demonstrates foreign-runtime engineering, not
  stock-current OpenMP, freestanding portability or Nehalem performance.

The closest architecture example is
[smallkirby's Ymir tutorial](../../30-sources/smallkirby-2024-writing-hypervisor-in-zig.md):
Intel 64 mechanisms in Zig/assembly, with explicit platform and feature
limits. [Ashet OS](../../30-sources/ashet-technologies-2026-operating-system.md)
adds practical OS evidence, but its 32-bit cooperative design is not our
protected/preemptive kernel.
[Uber's engineering article](../../30-sources/lubys-et-al-2023-uber-zig-toolchain.md)
supports industrial use of Zig's C/C++ toolchain, explicitly not production
Zig application adoption at the article's date.

These are complementary evidence classes, not interchangeable endorsements.
No peer-reviewed end-to-end qualification of a current Zig protected x86-64
kernel was established by this search. No performance ranking or real-time
guarantee is inferred from hosted benchmarks.

## Local results and their limits

See the [exact transcript and fixtures](../../assets/zig-kernel-feasibility/README.md).

| Probe | Observed result | Not established |
| --- | --- | --- |
| Hosted C → Zig → C → Zig callback | Expected values; 16-byte extern record, 8-byte alignment and offset checks passed using GCC 13.3.0 with Zig 0.16.0 | All ABI types, malformed inputs, cross-privilege invocation or kernel execution |
| Freestanding mixed-language ELF | Static ELF64/x86-64, no dynamic section or interpreter segment, no unresolved symbols | Bootable image, complete helper closure for future code, loader acceptance or hardware support |
| Architecture code generation | Port output, volatile load, atomic increment and naked halt loop inspected | Real MMIO behavior, ordering proof, interrupt entry/return or context-switch safety |
| C header translation | Intended declarations emitted; unsupported macros also visible | Complete translation compatibility or generated-binding consumer conformance |
| Header emission | Bare `-femit-h` rejected | Every possible emission API/backend combination |
| Repeated research runs | Both small mixed-language executions passed; binary hashes differed | Reproducible M0 builds; build-path/debug-input variation was not normalized or fully diagnosed |

The actual installed `zig cc --version` reports Clang **21.1.0**, resolving
what was used locally despite inconsistent release prose. No compiler was
installed and no project-wide version setting was changed.

No QEMU guest, physical board, imported OS project or privileged host instruction
was executed. No allocator/GC fault campaign, compiler differential campaign,
ring transition or latency measurement was performed. All implementation
checkboxes and M0–M4 acceptance gates remain open.

## What to explore next, in order

Broad language comparison is no longer the decision to make. The next decisive
work is qualification of the chosen language on our actual contracts:

| Priority | Decisive artifact | Existing plan owner and required result |
| --- | --- | --- |
| First | Accepted Zig/compiler/backend/linker/translator and source-location manifest | [M0 Phase 1](../../60-planning/01-proof-of-concept/m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md), `m0-p01-decisions`: pin inputs and roles; record every departure from this research candidate |
| First | Expanded ABI and helper regression corpus | Same phase, `m0-p01-build`: compile all intended boundary types, callbacks, allocation/helper cases; compare layout and both call directions; reject undeclared imports/instructions; achieve controlled clean-build reproduction |
| Before real boot acceptance | Boot/image/native procedure and syscall contracts | [M0 Phase 2](../../60-planning/01-proof-of-concept/m0-boot-inputs/phase-02-boot-image-and-interface-contracts.md): separate loader, ordinary calls, interrupt entry and user return; fix stack/FP/panic policies |
| Before claiming M1 | Reset-to-CLI trace plus register/stack/protection negative tests | [M1](../../60-planning/01-proof-of-concept/m1-boot-to-cli/README.md): exact QEMU fixture first; physical T7500 qualification remains separate |
| Before claiming containment | IRQ/preemption, lifetime, quota, reclamation and callback teardown tests | [M2](../../60-planning/01-proof-of-concept/m2-protected-service-nucleus/README.md): demonstrate the kernel invariants that Zig cannot guarantee |
| Before claiming completed PoC | Compiled-BEAM compatibility, local tracing GC and integrated failure campaign | [M3](../../60-planning/01-proof-of-concept/m3-project-beam-runtime/README.md) and [M4](../../60-planning/01-proof-of-concept/m4-integrated-recovery-and-resource-campaign/README.md): language choice does not close managed-runtime obligations |

Stop or revise the candidate compiler profile if critical entry/ABI code is
miscompiled without a bounded workaround, if generated dependencies cannot be
supplied within the design, or if required instruction/state restrictions
cannot be demonstrated. Prefer a narrowly audited C/assembly fallback where
it preserves the architecture; do not hide a compiler or design failure by
disabling all checks or expanding the guest into a hosted OS.

## Connections and source trail

- [Zig versus C comparison](zig-versus-c-kernel-language-comparison.md) — subsequent user-requested comparison, conditional recommendation and circumstances favoring C; the operative selection remains unchanged.
- [C kernel feasibility and low-level compatibility](c-kernel-language-feasibility-and-low-level-compatibility.md) — complementary alternative/C-component assessment; does not replace the selected Zig decision.

The [Zig topic map](../../10-maps/zig-kernel-development.md) provides short
reading routes. The [qualification inquiry](../../40-inquiries/can-zig-meet-the-kernel-qualification-contract.md)
stays open until executable evidence resolves the remaining questions.

Inline source-note links preserve claim provenance. The
[journal source manifest](../../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md#source-manifest)
is the exhaustive record of this session's thirteen new and two reused sources;
each source note records bibliographic details, primary URLs, method and limits.
