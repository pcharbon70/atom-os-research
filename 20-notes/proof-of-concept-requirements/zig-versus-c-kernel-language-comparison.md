---
title: "Zig versus C for the Atom kernel: comparison and recommendation"
kind: note
created: "2026-09-08"
maturity: developing
tags: [zig, c-language, kernel-language, language-comparison, proof-of-concept]
aliases: ["Zig versus C kernel comparison"]
---

# Zig versus C for the Atom kernel: comparison and recommendation

## Recommendation

**Retain Zig for the new kernel's ordinary implementation, with a small audited
assembly boundary and selectively admitted C components. Make that choice
conditional on executable toolchain and kernel-boundary qualification.**

This is a moderate-confidence engineering recommendation for our research PoC,
not a finding that Zig is generally safer, faster or easier than C. C is the
more conservative choice when independent compiler substitution, an established
C verification workflow, extensive C reuse or demonstrated team constraints
dominate. Those priorities could reasonably change the recommendation.

The case for Zig here is that a small, newly written kernel can benefit from
explicit error/cleanup idioms and checked interfaces while keeping difficult
machine transitions isolated. The case against it is substantial: additional
language/toolchain integration risk without C's established assurance record.
A bounded M0 qualification effort is the way to test that tradeoff.

The prior user selection is **not evidence of technical superiority**. It
remains the operative decision because this request asks for analysis, not a
language switch. No implementation, plan acceptance or new compiler pin is
authorized by this report.

Audience: the Atom OS research and implementation team. Evidence checked
2026-09-08. Read the individual [Zig](zig-kernel-language-feasibility-and-c-interoperability.md)
and [C](c-kernel-language-feasibility-and-low-level-compatibility.md) studies
for facility inventories; this report evaluates their tradeoffs rather than
repeating those inventories.

## Decision frame

Both languages must satisfy the same [T7500 / Intel x86-64 contract](dell-precision-t7500-target-and-minimal-qemu-profile.md):
minimal QEMU first, using the planned Nehalem-v1, one-CPU, 128-MiB serial
fixture; separately inventoried physical hardware later. Neither compiler CPU
selection nor a hosted target support tier proves that the Dell boots.

The first result is a native user-mode CLI on our own kernel. Later M0–M4
obligations still include protected services, bounded authority/resources,
compiled BEAM and automatic process-local tracing GC outside ring 0.
Neither language implements those architectural properties automatically.
AtomVM and graphical UI remain excluded.

Assumptions behind the recommendation:

- Most privileged policy code will be new, rather than an already selected,
  large C subsystem port.
- The team can sustain one pinned Zig profile and a narrow C/assembly boundary.
  Actual experience, staffing, deadline and maintenance budget are not known.
- Strong assurance is a design objective, but no specific C-only proof or
  certification workflow has been made an immediate requirement.
- Qualification is permitted to reject the candidate; writing a survey is not
  a substitute for that test.

If these assumptions are false, reconsider the choice using the sensitivity
analysis below. There is no defensible numerical score or universal winner:
priority weights and project measurements have not been supplied.

## Comparative summary

These judgments synthesize the cited sections below; “advantage” means a
relevant engineering affordance or evidence advantage, not a measured outcome.

| Criterion | Zig | C | Judgment for this PoC |
| --- | --- | --- | --- |
| Required machine control | Suitable mechanisms plus assembly | Suitable extensions plus assembly | No demonstrated capability winner |
| Everyday errors and cleanup | Integrated error/optional and cleanup constructs | Explicit conventions and helper APIs | Zig advantage in expression, not proof |
| Memory safety | Selected checks; unsafe lifetimes and unchecked behavior remain | Manual discipline plus optional analysis/instrumentation | Neither supplies full memory safety |
| Compiler alternatives | Multiple backends within the Zig implementation | Independently implemented GCC and Clang paths | C advantage in qualification options |
| Language/build stability | Concrete migration and regression risks | Explicit standard/dialect with implementation extensions | C is the conservative default |
| Existing C components | ABI wrappers/bindings add work | Direct source integration | C advantage grows with actual reuse |
| Freestanding libraries | Every selected utility/backend needs admission | Every selected library/service needs admission | Neither imports an OS for free |
| Source analysis and formal precedent | Current qualified path not established here | Documented analyzers and verified C kernel precedents | C evidence advantage |
| Execution speed, size and latency | No matched kernel measurements | No matched kernel measurements | Undetermined |
| Actor isolation and BEAM/GC | Kernel/runtime architecture must supply them | Kernel/runtime architecture must supply them | Language choice is not the mechanism |

## Language-level benefits and limitations

### Why Zig is attractive for newly written policy code

The [language overview](../../30-sources/zig-project-2026-language-overview.md)
demonstrates error/optional values, allocator passing, scope-exit cleanup and
compile-time construction. Their value is integration: programmers can express
some recurring contracts directly rather than rebuilding every convention.

Our design inference is that this is useful for allocation rollback, bounded
input decoding and explicit object-state transitions. For example, a domain
creation operation should either publish a fully funded object or release all
staged reservations. Zig can make the local cleanup structure visible; C can
implement the same transaction with status returns and disciplined cleanup
labels. Neither automatically defines the publication point or accounts for
asynchronous users.

Similarly, a typed internal handle can make accidental mix-ups harder to write,
but cannot prove authority. Generation checks, revocation, ownership transfer
and stale-callback rejection remain runtime kernel obligations.

Use compile-time abstraction only where its generated result remains easy to
inspect. A generated dispatch table is not evidence that its permissions,
machine encodings or handler state are correct. Avoid replacing a small,
reviewable mechanism with a difficult metaprogram merely because it is possible.

**Zig's advantage is better-integrated expression of chosen discipline, not
exclusive access to that discipline.** C can also use caller-owned buffers,
injected allocators, explicit results, static assertions and generated tables.
A freestanding C kernel need not use a global malloc-backed heap.

### Safety checks are useful, but not a protection boundary

The [Zig 0.16 reference](../../30-sources/zig-project-2026-language-reference-0-16.md)
documents Debug/ReleaseSafe checks, unchecked illegal behavior and scope-level
overrides. A checked slice index does not validate the lifetime of its backing
allocation. Neither use-after-free freedom nor race freedom follows from
ReleaseSafe. Ordinary Zig unsigned overflow is not C-style automatic wrapping.

C has [undefined-behavior and pointer-model obligations](../../30-sources/wg14-2011-c11-committee-draft.md).
The [optimization study](../../30-sources/wang-et-al-2013-optimization-safe-systems.md)
and [provenance research](../../30-sources/memarian-et-al-2019-c-pointer-provenance.md)
explain why machine-address intuition is insufficient. Zig's remaining
unchecked operations also require an explicit semantic contract; describing
C's risks does not eliminate them from Zig.

For our kernel, the decisive distinction is between:

- rejecting a malformed request before modifying state;
- detecting an internal invariant violation; and
- containing failure in a separate protected domain.

Only the last is fault isolation. A ring-0 panic can stop the whole machine.
It may prevent further execution of a bad path, but is not successful recovery.

The inspected [Zig runtime source](../../30-sources/zig-project-2026-freestanding-source-profile.md)
traps in defaultPanic on freestanding targets. Serial diagnostics and recovery
are not supplied. Recommend explicit recoverable errors for invalid input and
exhaustion, and a bounded, nonallocating panic path for internal failure.
Scope-exit cleanup is not a transaction-recovery mechanism after a trap or
abandonment of an execution context without normal scope exit. Correctly
saved and resumed preemption does not itself invalidate that cleanup.

Imported C shares ring-0 privilege if linked there. Zig checking does not
retroactively protect accesses inside that C code. A narrow foreign boundary
reduces review scope, not the privilege of the code behind it.

## Toolchain, ecosystem and assurance

### C's strongest advantage: independent qualification paths

[Linux's documented GNU C11/GCC/Clang profile](../../30-sources/linux-community-2026-kernel-c-dialect.md)
is concrete evidence for established C kernel practice. An intentionally
constrained C subset can retain GCC and Clang builds as independent
implementation paths. This helps investigate disagreements and avoid some
single-compiler dependencies.

Zig has multiple backends; it is incorrect to say that it inherently requires
LLVM. However, using different backends still retains Zig frontend processing.
Our archive has not qualified an independently implemented Zig frontend.
Likewise, Zig using LLVM and C using Clang do not form a wholly independent
compiler experiment. Two compilers agreeing is useful evidence, not a proof.

C is not “portable assembly.” [GCC's x86 profile](../../30-sources/gnu-project-2026-x86-kernel-c-profile.md)
and [Clang interrupt attributes](../../30-sources/llvm-project-2025-clang-x86-interrupt-contract.md)
impose real restrictions. Switching compiler may require adapting extensions,
not just changing an executable name.

### Zig's maintenance risk is concrete, not merely its age

The [0.16 release record](../../30-sources/zig-project-2026-release-0-16.md)
records interface migrations, acknowledged regressions, disabled-by-default
incremental compilation with known miscompilations, and an LLVM vectorization
workaround. Its freestanding x86 targets are outside the ordinary tier table.

Our inference is that a Zig owner must be prepared to investigate toolchain
issues. Pinning limits compulsory migration, and a small freestanding subset
avoids much hosted-library churn, but does not remove defects. C also needs
compiler-upgrade qualification; a stable dialect does not freeze optimizer,
linker or platform behavior.

Start with the previously exercised LLVM candidate because we have evidence
for that exact route, not because the backend is proven safer. Keep
experimental incremental compilation out of accepted-image generation until
separately qualified. Do not follow master documentation when using a pinned
release.

### C has a stronger established analysis and proof route

[Clang 21's diagnostic contracts](../../30-sources/llvm-project-2025-clang-analysis-and-sanitizer-contracts.md)
provide concrete source analysis and ASan/UBSan options. Hosted instrumentation
can expose some errors that ordinary execution misses. It does not prove all
paths, model our allocator automatically, or validate interrupt/device behavior.
The documented ASan runtime is not an off-the-shelf production kernel component.

Selected UBSan checks can use trap mode without the reporting runtime. Thus
it would be unfair to compare checked Zig only against deliberately
uninstrumented C, or to claim that C cannot have runtime checks. Qualification
must account for which checks actually run and their failure behavior.

[seL4's C verification](../../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
and [translation validation](../../30-sources/sewell-et-al-2013-translation-validation.md)
give C a stronger established assurance precedent in this corpus. Their
architecture, semantics, assembly, hardware and configuration assumptions do
not transfer to Atom. A C implementation would still need its own proof
strategy and supported subset.

This study did not establish an equivalent end-to-end proof route for our Zig
candidate; that is an evidence gap, not proof that one is impossible. If
machine-checked implementation refinement becomes the near-term governing
requirement, reevaluate C before accumulating a large Zig implementation.

For debugging, require actual source stepping, variable/type inspection and
fault-frame diagnosis on our guest images in either language. Neither prior
study demonstrated those workflows. We do not rank debug quality from the
presence of symbols in an ELF.

## Hardware access and C interoperability

Both candidates can express the required instructions, data layouts and native
control flow. Both must satisfy [Intel's hardware contract](../../30-sources/intel-2026-system-programming-documentation.md),
including entry frames, processor state, mapping, interrupt semantics and
validated return. Inline assembly, volatile, atomics and CPU fences have
different roles in either implementation.

The [SysV AMD64 procedure ABI](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md)
does not define our syscall or interrupt ABI. Preserve the red-zone, stack,
extended-register and helper policies across every reachable object.
A mostly Zig kernel does not require that every entry stub be Zig; a mostly
C kernel does not avoid assembly obligations.

Zig can call original compiled C; translating the C implementation is optional.
But maintaining declarations/layouts and callbacks adds work compared with
an all-C component interface. The [translator limitations](../../30-sources/zig-project-2026-c-translator-limits.md)
and earlier failed bare header-emission probe are actual integration costs,
not a general inability to interoperate.

Use fixed signatures, explicit status/length fields and opaque handles. Keep
language-specific error unions, slices and allocator objects inside the Zig
boundary. Audit callback lifetime, permitted execution context and ownership
separately from argument passing.

Both [GCC](../../30-sources/gnu-project-2026-gcc-freestanding-environment.md)
and [Clang](../../30-sources/llvm-project-2025-clang-21-freestanding.md)
can require compiler-support helpers. “No libc” does not mean “no runtime
support.” Our C division probe imported __udivti3; the Zig tiny-link result
does not establish that future Zig arithmetic or memory code is helper-free.

Changing languages also does not remove a library's OS dependencies.
[musl's Linux contract](../../30-sources/musl-project-2026-linux-dependency.md)
is a concrete counterexample. [OSKit's reuse work](../../30-sources/ford-et-al-1997-flux-oskit.md)
explains the environment-adapter problem. A driver missing from the project
is not evidence against Zig; an actually required, difficult C interface may
be evidence for C if wrapper cost becomes material. No decisive imported
subsystem of that kind has been selected.

## What the papers and experiments can actually compare

| Evidence | What it contributes | Invalid inference |
| --- | --- | --- |
| [Csmith, PLDI 2011](../../30-sources/yang-et-al-2011-csmith.md) | Historical differential C compiler testing with generated inputs designed to avoid semantic ambiguity | Today's C compiler failure rate |
| [No-fuss fuzzing, CC 2022](../../30-sources/groce-et-al-2022-no-fuss-compiler-fuzzing.md) | Historical Zig compiler-crash discovery | Direct comparison with Csmith's counts or generated-code correctness |
| [Optimization-safe systems, SOSP 2013](../../30-sources/wang-et-al-2013-optimization-safe-systems.md) | Real systems-code failures involving undefined behavior | All C code is unreliable, or Zig avoids all analogous risks |
| [Pointer provenance, POPL 2019](../../30-sources/memarian-et-al-2019-c-pointer-provenance.md) | Executable semantic proposals and low-level pointer tensions | Today's complete binding ISO/implementation contract |
| [Zig/OpenMP, SC-W 2024](../../30-sources/kacs-et-al-2024-zig-openmp.md) | Modified historical compiler and hosted interoperability/performance work | Stock Zig, freestanding or T7500 performance |
| [Off by Two](../../30-sources/desaulniers-2020-off-by-two.md) | First-person account of a fixed C/assembly compiler regression | A claim that the current Clang has that defect |
| [Ymir](../../30-sources/smallkirby-2024-writing-hypervisor-in-zig.md) | Practitioner evidence for Zig/assembly Intel mechanisms | Our boot, isolation or recovery qualification |

These works establish mechanisms and risks, not a controlled comparison of
two otherwise equivalent Atom kernels. They differ in compiler version,
generator, error oracle, hardware, workload and effort. We do not infer a
language ranking from publication counts or raw bug counts.

### Our local evidence is asymmetric

The [Zig session](../../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md)
and [C session](../../50-journal/2026-09-08-c-kernel-feasibility-deep-dive.md)
both recorded narrow hosted ABI success and freestanding linking. They are
feasibility probes, **not head-to-head benchmarks**:

- Zig used ReleaseSafe for an interoperability object and ReleaseSmall for
  architecture emission; C used O2 with separate register/unwind controls.
- C tested an empty interrupt attribute; Zig's architecture fixture tested a
  naked halt entry. Those are not the same transition.
- The linked contents, metadata and entry points differ. Comparing file size,
  instruction count or hashes would not establish efficiency.
- Clang came through the same Zig distribution, and the Zig objects used LLVM.
  This does not provide three independent compiler implementations.
- Neither session booted a guest, exercised real MMIO/interrupts, measured
  latency or qualified a kernel allocator.

No new implementation or comparative benchmark was run in this session.
We inspected the existing scripts/results and current primary documentation.

The [Zig overview](../../30-sources/zig-project-2026-language-overview.md)
makes a broad speed claim that this analysis does not adopt. Faster compilation,
faster execution, smaller text, lower peak memory and better worst-case latency
are separate measurements. Neither using LLVM nor omitting tracing GC decides
them. Tracing GC remains required in the unprivileged BEAM runtime regardless.

If performance becomes decision-changing, compare the same contract, algorithm,
data, CPU features, safety policy and measurement conditions. Report safety-
equivalent and intended-shipping profiles separately where they differ. Start
with an actual bottleneck, not an unrelated microbenchmark suite.

## Pros and cons in practical terms

**Choose Zig for its potential to improve the new code's expression.** Expected
benefits are clearer local failure/cleanup structure and useful checked
interfaces. Costs include language-specific qualification, version-sensitive
integration and a weaker established proof path. Those benefits matter only
if the team uses the features consistently and does not trade them away through
unchecked casts or blanket safety disabling.

**Choose C for its established implementation and assurance options.** Benefits
include independent compiler paths, direct C integration and documented
analysis/verification precedents. Costs include more manually maintained
error/ownership conventions and persistent semantic and memory hazards.
Those hazards require active controls, not confidence based on familiarity.

**Do not build two complete kernels to avoid choosing.** Use one primary
implementation and small independent fixtures at uncertain boundaries. A
mixed-language kernel is useful only when each boundary saves more risk/work
than it adds; every imported privileged component remains part of the trusted
code and maintenance surface.

## Recommendation sensitivity

| Actual project priority or observation | Preferred response |
| --- | --- |
| Small greenfield research kernel, sustainable Zig ownership, no mandatory C proof workflow | Retain Zig with bounded C/assembly |
| Lowest additional language/tooling uncertainty is the governing requirement | Prefer constrained C; still qualify its extensions and boot path |
| Required implementation-refinement tooling supports a qualified C subset but not our Zig route | Prefer C for the covered kernel, after checking the actual proof boundary |
| Substantial admitted C code makes wrappers a demonstrated ongoing burden | Reevaluate primary C, or isolate the subsystem outside the kernel |
| Team cannot maintain/debug the Zig profile within actual delivery constraints | Prefer the demonstrably supportable C path, not a hypothetical staffing assumption |
| Zig has a required, reproducible wrong-code/ABI failure without a bounded workaround | Stop acceptance; evaluate a C/assembly replacement, then primary C if necessary |
| One awkward header, missing device driver or unsupported convenience API | Try a narrow wrapper/implementation first; not sufficient reason to switch |
| Representative equivalent measurements show a material unresolved cost | Optimize the affected component or revisit language choice with the measurements |

The strongest objection to retaining Zig is that boot bring-up is already
difficult, so adding toolchain uncertainty may not be worth language
convenience. That objection wins if minimizing that uncertainty is the user's
dominant constraint. Under the stated research assumptions, a small kernel and
a rejectable qualification gate make Zig's potential benefit worth evaluating.
The recommendation would be the same for a fresh choice under those assumptions;
it is not based on unmeasured migration costs or sunk implementation effort.

## Immediate acceptance questions

The existing [M0–M4 program](../../60-planning/01-proof-of-concept/README.md)
should answer these; this list is not a replacement phased plan:

1. Can the chosen toolchain produce repeatable, dependency-audited images with
   the exact CPU/register, ABI, helper and linker policy?
2. Can we diagnose both expected errors and internal faults without relying
   on a healthy heap or user service, including before full trap setup?
3. Do real entry/exit, stack and register tests pass, followed by the native
   user-mode CLI in the exact minimum guest?
4. Do allocation rollback, stale handles, callback teardown, interrupt
   reentrancy and resource-exhaustion tests preserve kernel invariants?
5. Is there a named maintainer and an acceptable debugging/upgrade workflow?
   What concrete requirement, failed test or measured cost would reverse
   the choice?

For Zig, propose ReleaseSafe qualification of ordinary policy code, explicit
backend selection and a custom panic path. Treat raw entry/assembly separately;
the prior ReleaseSmall architecture probe does not validate a checked kernel.
For any C components, use an explicit dialect, both compiler paths where
practical, and suitable hosted analysis; do not claim those tools were run.

Continue to preserve M3's compiled-BEAM and tracing-GC requirements and M4's
integrated failure/resource campaign. Neither language recommendation closes
those obligations. Further broad comparison is unlikely to decide more than
the next concrete qualification result.

## Connections and provenance

- [Kernel-language selection map](../../10-maps/kernel-language-selection.md) — comparative reading route.
- [Decision-change inquiry](../../40-inquiries/what-evidence-would-change-the-kernel-language-choice.md) — falsifiable triggers without silently changing the selected language.
- [Comparison journal](../../50-journal/2026-09-08-zig-versus-c-kernel-language-deep-dive.md) — source manifest, claim/gap ledger, access notes and verification.
- [Freestanding build contract](freestanding-build-and-static-images.md) — active R02 obligations.
