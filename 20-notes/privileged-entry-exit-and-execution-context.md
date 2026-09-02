---
title: "Privileged entry, exit, and execution context"
kind: note
created: "2026-09-02"
maturity: developing
tags:
  - architecture-support
  - context-switching
  - exceptions
  - operating-systems
  - privilege
  - security
  - system-calls
aliases:
  - "Privileged entry and return"
  - "Execution-context boundary"
---

# Privileged entry, exit, and execution context

The recommended implementation is a **typed, per-CPU entry state machine with
one validated semantic return gate**. Small ISA-specific stubs establish a safe
stack and capture a backend-private raw frame; common low-level code records
origin and nesting, applies the pinned security profile, normalizes the event
into a frame type that cannot be misreturned, performs only bounded dispatch,
and returns to less privilege only through a validator.

Execution context includes every enabled architectural state component that
can carry authority, alter execution, or disclose data. Integer registers are
only the beginning. Extended-state ownership is explicit and cross-domain
switches use eager save/restore or initialization/scrubbing as the baseline.
The kernel does not use FP, SIMD, vector, or matrix state in hard-entry code.

This is component 2 of the [kernel hardware and architecture support
layer](kernel-hardware-and-architecture-support-layer.md). It implements the
mechanism of entry, frame ownership, dispatch boundaries, context transfer, and
return. System-call policy, scheduling, actor reductions, and restart policy
remain above it.

## Question, scope, and operational standard

The implementation question is:

> How should architecture-defined partial entry states become a kernel-defined
> execution state, and how can the kernel prove that every return restores only
> an authorized, non-leaking, representable less-privileged context?

The component is acceptable only when tests and review establish that:

- every syscall, user exception, external interrupt, kernel exception,
  NMI-like event, and fatal recursive fault enters through a named vector class
  with a bounded stack and nesting rule;
- assembly reaches common code only after saving every value it will clobber,
  establishing CPU-local addressing, and recording enough raw state to classify
  origin without mutable global inference;
- no raw architecture frame can be passed directly to a user-return
  instruction;
- all fast and slow paths converge on the same `UserReturnEnvelope` validation,
  even if their final instructions differ;
- return validates privilege, address form and range, stack alignment, allowed
  status/control bits, interrupt state, address-space and domain generation,
  enabled feature shape, debug/performance state, and pending lifecycle work;
- no register or enabled state component belonging to one protection domain is
  observable in another; leakage tests include FP/SIMD/vector, debug, PMU,
  thread-local, protection-key, authentication, and other discovered state;
- entry before normal dispatch and final return are allocation-free,
  non-blocking, non-unwinding, and restricted to primitives approved for that
  context;
- maximum hard-path nesting and stack use are measured and enforced, with a
  dedicated terminal path when the bound is exceeded; and
- syscall, interrupt, context-switch, and mitigation costs are reported by
  entry class and `ContextShape`, including p50, p99, worst observed, cold-cache,
  cross-CPU migration, and virtualized results.

## Evidence and synthesis

### Normative architecture evidence

The [Intel system-programming
documentation](../30-sources/intel-2026-system-programming-documentation.md)
defines IDT-based events, privilege-stack transitions, syscall/return
mechanisms, IRET frames, control state, and CPUID/XSAVE-discovered extended
state. The [Arm A-profile
documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
defines exception levels, vector classes, saved program state, exception link
and syndrome registers, `ERET`, and feature-dependent FP/SIMD/SVE/SME state.
The [RISC-V privileged
architecture](../30-sources/risc-v-international-2026-privileged-architecture.md)
defines delegated traps, `stvec`, supervisor cause/value/PC/status state,
`SRET`, and optional extension status including floating-point and vector
state.

These sources support a common transition model but not a common binary frame.
Each architecture saves a different subset before software runs, admits
different vector classes, and exposes different return hazards.

### Engineering evidence

The [Linux entry/exit
documentation](../30-sources/linux-kernel-community-2026-low-level-core-apis.md)
treats entry as ordered state transitions and marks windows in which
instrumentation is unsafe; NMI-like handling has distinct nesting behavior.
This is useful precedent for a visible protocol and tool-enforced
non-instrumentable sections. Linux's exact RCU, tracing, audit, compatibility,
and task-work ordering is not this kernel's required design.

The [L4 retrospective](../30-sources/elphinstone-heiser-2013-l4-lessons.md)
supports small architecture-specific entry paths and optimization based on
measurement. The [seL4 verification
work](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
shows how a small explicit kernel state aids reasoning while also making clear
that assembly, hardware, caches, and timing require separate assumptions.

### Security evidence

[LazyFP](../30-sources/stecklina-prescher-2018-lazyfp.md) demonstrated that
fault-based lazy floating-point restore left prior-domain FP/SIMD values
transiently observable on affected processors. It directly supports rejecting
that class of lazy cross-domain ownership for the safe baseline; it does not
prove all lazy schemes or all ISAs insecure.

[Meltdown](../30-sources/lipp-et-al-2018-meltdown.md) demonstrated that, on
affected machines, supervisor-only mappings could be read through transient
execution and that removing most kernel mappings from the user page table
impeded the attack. [Spectre](../30-sources/kocher-et-al-2019-spectre.md)
demonstrated a broader class in which mistrained speculative execution leaves
observable microarchitectural effects across software isolation boundaries.
The justified conclusion is not one universal barrier: entry and return need a
versioned CPU security profile with explicit coverage and cost.

### Synthesis

No source proves this proposed state machine. It combines:

1. architecture-defined raw entry and return semantics;
2. mature-kernel evidence that bookkeeping order and non-instrumentable windows
   are correctness properties;
3. microkernel evidence for a small, explicit state and assembly boundary; and
4. attacks showing that residual extended and speculative state can cross
   architecturally correct domain transitions.

The frame types, ownership states, return token, and staged policy below are
project proposals awaiting model, emulator, and hardware evidence.

## Trust boundary and ownership

```text
less-privileged execution
       |
       | architecture event / syscall / interrupt
       v
ISA vector stub                   raw, bounded, non-instrumented
       |
entry-state transition           CPU-local state becomes coherent
       |
typed frame normalization        architecture facts retained
       |
bounded dispatch / typed event   policy invoked only in safe context
       |
return preparation + validation  one semantic gate
       |
ISA restore and return
       v
less-privileged execution
```

The protected kernel owns entry stacks, raw and normalized frames, saved
contexts, CPU-local entry state, and the return validator. A user domain owns
the values in its saved context but cannot write the kernel metadata that says
which values are valid or where they may return.

The scheduler owns the decision to switch threads or CPUs. It asks this
component to transfer context using a generation-checked execution-context
handle. The component does not choose priorities, budgets, reductions, or
placement.

Component 1 owns the compiled vector/return leaf symbols and their unsafe
instruction and clobber contracts. This component owns vector-table
configuration, chooses and invokes the appropriate leaf, supplies its
prevalidated stack and CPU-local operands, and owns every semantic state
transition after entry. Component 1 therefore cannot choose dispatch or
recovery policy merely because its code executes first.

## Per-CPU entry state

Every online CPU has preallocated, guard-protected state prepared before it can
receive work or external interrupts:

```text
EntryCpuState {
    cpu_id,
    lifecycle_generation,
    current_domain,
    current_thread,
    active_translation_guard: Option<ActivationGuard>,
    thread_kernel_stack,
    hard_interrupt_stack,
    nmi_like_stack,
    terminal_stack,
    entry_depth,
    nmi_depth,
    preemption_state,
    local_interrupt_state,
    active_raw_frame,
    extended_state_owner,
    mitigation_profile,
    fault_capture_state_ref,
}
```

Stacks have unmapped or otherwise protected guard regions where the
architecture profile permits. Hard-interrupt and NMI-like stacks are CPU-local
and contain no actor-owned data. A terminal stack is small, single-use, and
supports only bounded evidence capture followed by halt/reset.

`fault_capture_state_ref` names preallocated slots owned by the architecture-
fault component; entry code owns only the stacks, nesting state, and transfer
into that component's bounded capture routine.

`entry_depth` and `nmi_depth` are updated in the earliest sequence that is safe
against their own event classes. They are diagnostic and protective state, not
permission to allow arbitrary nesting.

### Entry-context tokens

After the required stack, CPU-local base, raw frame, and nesting state are
established, component 2 mints one lexical, non-storable context token:

- `HardEntryContext` permits only the bounded operations approved for ordinary
  hard entry;
- `NmiContext` is a stricter, non-widening subtype for an event that cannot rely
  on ordinary interrupt masking or lock exclusion; and
- `FatalCaptureContext` is the smallest subtype, permitting only direct raw
  capture under a `FatalPreclassificationProof`, recursive evidence sealing,
  and the terminal leaf needed when further common code is unsafe.

“Subtype” describes a subset of effects, not an implicit cast. Safe code cannot
widen `NmiContext` or `FatalCaptureContext` into `HardEntryContext`; operations
name the exact context classes they accept. `CrashContext` is different: it is
minted only after component 9 has sealed terminal evidence and authorizes only
prevalidated crash-sink, halt, or reset operations. It is never the token for
ordinary fault capture.

## Entry classes and state machine

The semantic entry classes are:

- `UserCall`: an intentional service invocation;
- `UserFault`: a synchronous fault attributable to less-privileged state;
- `ExternalInterrupt`: a routable ordinary interrupt;
- `KernelFault`: a synchronous kernel exception, possibly inside a declared
  guarded user-access or discovery region;
- `NmiLike`: an event not excluded by ordinary local interrupt masking;
- `MachineFault`: an architecture/RAS condition with architecture-dependent
  precision and recoverability; and
- `RecursiveFatal`: entry while the required entry/fault state is already
  unusable.

The full transition is:

```text
HardwareEntry
  -> SafeStackEstablished
  -> RawStateCaptured
  -> KernelAddressingEstablished
  -> BookkeepingEstablished
  -> FrameNormalized
  -> Dispatched
  -> ReturnPrepared
  -> ReturnValidated
  -> ArchitecturalStateRestored
  -> LessPrivileged

Any pre-dispatch state -> FatalCapture -> TerminalAction
Dispatched -> BlockedOrSwitched -> later ReturnPrepared
UserFault -> FaultEventPosted -> BlockedOrSwitched
```

Each arrow has an allowed-instrumentation, interrupt, allocation, lock, and
fault policy. The contract is generated into documentation and debug trace
points; trace points themselves occur only where instrumentation is permitted.

### Phase 1: vector stub

The first instructions:

1. preserve every register/field they must reuse;
2. select or verify the required stack without trusting a user-controlled
   pointer;
3. establish a CPU-local base through the architecture's safe mechanism;
4. capture raw cause, PC, status, fault value, and hardware-supplied frame
   before a nested event can overwrite them;
5. apply only the earliest mitigation sequence required by the pinned profile;
   and
6. call one low-level routine under the pinned kernel ABI.

The stub does not decode a system call, access a user pointer, take a general
lock, allocate, invoke a driver, schedule an actor, or enable ordinary
interrupts.

### Phase 2: entry bookkeeping

Low-level code derives origin from captured status, not from `current_thread`
or a stack-address heuristic alone. It records the entry class, switches to the
kernel's accounting/addressing view when required, updates preemption and
nesting state, and enters the first instrumentable region in a documented
order.

The order is architecture- and kernel-specific but fixed per port. Tools should
reject calls or instrumentation in the protected prefix/suffix, similar in
spirit to Linux's `noinstr` validation without importing Linux's entire entry
model.

### Phase 3: frame normalization

`RawArchFrame` is backend-private and versioned for crash decoding. It becomes
one of these disjoint types:

```text
EntryFrame =
    UserCallFrame(UserReturnEnvelope, CallArguments)
  | UserFaultFrame(UserReturnEnvelope, NormalizedFault)
  | InterruptFrame(InterruptedOrigin, InterruptEvidence)
  | KernelFaultFrame(KernelResumeClass, FaultEvidence)
  | ArchitectureFaultFrame(MachineFaultDelivery, FaultEvidenceView)
  | NmiFrame(InterruptedOrigin, MinimalEvidence)
  | FatalFrame(MinimalRawEvidence)
```

Only the first two contain a `UserReturnEnvelope`. A fatal, architecture-fault,
or kernel-fault frame therefore cannot reach the user-return function by
casting or a shared union tag error. Every semantic `MachineFault` becomes an
`ArchitectureFaultFrame` before component 9 is called. An NMI-delivered machine
error still uses that frame under `NmiContext`; `NmiFrame` is reserved for a
non-machine-fault diagnostic NMI-like event. `FatalFrame` is reserved for a
preclassified or recursive terminal path, not used merely because severity is
not yet known. Raw architecture cause/status fields remain attached for
diagnosis; normalization does not discard evidence it cannot interpret.

`CallArguments` are scalar register values and bounded copied metadata only.
They are not trusted pointers. Capability lookup and safe user-memory access
occur in higher kernel services after entry state is established.

### Phase 4: bounded dispatch and deferral

The hard path classifies and captures. A small syscall may proceed into normal
kernel code once the context is fully established. External interrupts post a
typed event through component 5 after only the controller transition required
by that flow. User faults post a structured fault event and block the context.
An `ArchitectureFaultFrame` is passed to component 9 with
`HardEntryContext`, `NmiContext`, or `FatalCaptureContext` as justified by its
entry state. NMI-like and machine-fault paths do only operations approved for
that exact context.

No ordinary BEAM process, garbage collector, driver process, or supervisor runs
on an entry stack. Those entities receive events after the kernel has restored
normal scheduling and accounting context.

## Return envelope and validation

The user-return object is not raw saved memory:

```text
UserReturnEnvelope {
    domain_id,
    domain_generation,
    thread_id,
    context_generation,
    address_space_id,
    address_space_generation,
    context_shape_id,
    user_pc,
    user_sp,
    allowed_integer_state,
    sanitized_status,
    thread_local_state,
    signal_or_upcall_state,
    mitigation_generation,
}
```

Before final return, the validator proves:

- the domain, thread, address space, context shape, CPU lifecycle, and
  mitigation generations are current;
- `user_pc` and `user_sp` are correctly formed, aligned, in the permitted user
  range, and mapped under the expected address-space generation;
- privilege fields request only the configured less-privileged mode;
- reserved, virtualization, single-step, interrupt-mask, alignment, arithmetic,
  endianness, access-override, and other sensitive status fields match an
  explicit allowlist;
- enabled integer and extended-state features match `context_shape_id` and
  their backing state is initialized for this context;
- debug, trace, performance, protection-key, tagging, authentication, and
  thread-local controls have been restored, disabled, or scrubbed according to
  delegated authority;
- pending stop, revoke, fault, signal/upcall, budget, CPU-offline, and
  address-space invalidation work has been handled; and
- registers not defined as user results contain user-owned restored values or
  public constants, never kernel temporaries.

Validation yields a short-lived, CPU-bound `ValidatedReturnToken`. Only the
final assembly leaf accepts this token. An interrupt or generation change
between validation and final return invalidates or restarts the return path.
Where static linear types are unavailable, the token is opaque and guarded by
CPU-local generation checks.

Fast return is a representability optimization. On x86-64, a SYSRET-class path
is used only when its address, status, compatibility, tracing, and mitigation
constraints hold; otherwise an IRET-class slow path consumes the same semantic
envelope. AArch64 `ERET` and RISC-V `SRET` still require validation even though
their fast/slow split differs.

## Execution-context shape and ownership

### Discover the shape, do not hard-code a register block

`ContextShape` is derived from the immutable `KernelRequiredProfile`, explicit
context feature requirements, and component 7's current per-CPU eligibility
generation—not from the boot CPU's optional features:

```text
ContextShape {
    feature_requirements,
    eligible_cpu_class,
    eligibility_generation,
    integer_layout,
    control_layout,
    fp_simd_layout,
    vector_or_matrix_layout,
    debug_layout,
    performance_layout,
    protection_layout,
    thread_local_layout,
    save_bytes,
    save_alignment,
    supported_return_features,
}
```

On x86-64, CPUID/XSAVE-family discovery determines enabled components and
layout. On AArch64, FP/SIMD and optional SVE/SME, debug, pointer-authentication,
and tagging features alter context obligations. On RISC-V, optional F/D/V and
other extensions plus architectural status determine what can be live. A port
must also inventory implementation-specific control and mitigation state.

Unknown enabled state is a boot failure. A feature can be deliberately disabled
to keep the first context shape small; it cannot remain live and unmanaged.
Saved-context memory is explicit kernel object memory charged to the owning
domain's resource budget.

Before restoring a context, this component checks that the current
`CpuFeatureEvidence<CpuIncarnation>` still satisfies the shape and that its
eligibility generation is current. A lifecycle change invalidates prepared
returns for shapes whose placement set changed; the scheduler supplies policy,
while this component enforces representability and state isolation.

### Coupled ownership state machines

One state machine cannot represent both the single live hardware unit on a CPU
and the independently saved state of many contexts. For every independently
managed extended-state class, keep two coupled machines.

The per-CPU hardware-unit machine is:

```text
CpuExtendedUnitState =
    Disabled
  | Clean(shape_generation)
  | Resident(context_id, context_generation,
             residency_generation, dirty_state)
  | ScrubRequired(previous_context_generation)
  | Failed(reason)
```

Each execution context has its own backing-state machine:

```text
ContextExtendedState =
    Disabled
  | Uninitialized(shape_generation)
  | Saved(context_generation, buffer, contents_generation)
  | ResidentOn(cpu_id, cpu_lifecycle_generation, residency_generation)
  | Discarded(context_generation)
  | Failed(reason)
```

Many contexts may simultaneously be `Saved`; at most one context per CPU and
state class may be `ResidentOn` that CPU. A `Resident` CPU state and
`ResidentOn` context state exist only as a matching pair with identical CPU,
context, lifecycle, and residency generations. While that pair exists, the
backing buffer is not authoritative. A context is eligible for migration only
from `Saved`, `Uninitialized`, or `Disabled`; a terminated context reaches
`Discarded` only after no CPU names it as resident.

A legal eager cross-domain switch commits the paired transitions under the
CPU-local switch guard:

```text
(CPU Resident(old, r), old ResidentOn(cpu, r))
  -> save:    (CPU Clean-or-ScrubRequired, old Saved(new_contents_generation))
     or drop: (CPU Clean-or-ScrubRequired, old Discarded) [only if terminated]
  -> scrub when required: CPU Clean
  -> restore or initialize new context
  -> (CPU Resident(new, r+1), new ResidentOn(cpu, r+1))
```

A fault before the paired save/drop commit leaves the old pair authoritative.
A fault after it but before the new pair commits leaves the CPU clean or
scrub-required and the new context saved/uninitialized. Any failure for which
neither post-state can be proved enters `Failed` and prevents cross-domain
return; it is never repaired by guessing which copy is newer.

At an ordinary syscall or interrupt that will return to the same context, the
matching `Resident`/`ResidentOn` pair may remain live **only if kernel entry code
cannot use the unit, migration is prohibited, and no other context runs**. This
avoids an unnecessary full vector save on every syscall while retaining
explicit ownership. Before another protection domain runs or the context
migrates, the old state is eagerly saved or explicitly discarded and the new
state eagerly restored or initialized after any required scrub.

The initial profile rejects fault-triggered lazy cross-domain restore. A later
optimization needs a separate threat analysis, proof that no stale state is
transiently observable on the target, bounded fault behavior, and measurements
showing material benefit. LazyFP is evidence against treating the old scheme as
the safe default.

### Kernel use of extended state

Hard entry, hard interrupt, NMI-like, fatal capture, and code reachable from
them are compiled without implicit FP/vector use and scanned for forbidden
opcodes. Ordinary kernel code also avoids extended state initially. A future
scoped kernel-vector API would need to save/borrow ownership, disable
preemption/migration as required, handle nested events, and restore it on every
exit—including faults. That complexity is not justified before measurement.

## Cross-ISA realization

| Concern | x86-64 | AArch64 A-profile | RISC-V supervisor profile | Common contract |
| --- | --- | --- | --- | --- |
| Vector selection | IDT gates plus SYSCALL-class entry; TSS/IST can select stacks for named events | Vector table distinguishes current/lower EL, SP choice, and synchronous/IRQ/FIQ/SError classes | `stvec` direct or vectored base; delegation determines supervisor-visible traps | Named `EntryClass` and pinned raw vector revision |
| Hardware-saved state | Event-dependent stack frame; software saves remaining registers; SYSCALL saves a different subset | PC/status in ELR/SPSR plus syndrome/fault registers; software saves GPRs | PC/cause/value/status CSRs; software saves GPRs, often using `sscratch` in the stack protocol | Backend-private complete `RawArchFrame` |
| CPU-local/stack establishment | Privilege stack mechanisms, per-CPU base handling, and IST for selected events; nested SWAPGS-like state needs exact rules | Appropriate SP_ELx/vector class and CPU-local register or mapping | Scratch CSR/per-CPU convention and supervisor stack | Safe stack before common calls; origin captured explicitly |
| Return | SYSRET-class fast path or IRET-class general path with different hazards | Restore saved state then `ERET`; illegal return conditions must be handled | Restore supervisor state then `SRET`; privilege and status bits require sanitization | One validated envelope; backend chooses representable leaf |
| Extended state | XSAVE-discovered components, debug, PKRU-like and other optional state | FP/SIMD, SVE/SME, debug, PMU, PAC/MTE-related controls as enabled | F/D/V and optional state tracked by status/extensions | Feature-shaped explicit ownership |
| Speculation profile | May require page-table isolation and branch/predictor/return-stack mitigations by model | May require architecture/vendor-prescribed barriers or predictor controls by profile | Depends on implementation and disclosed mitigations, not base ISA name alone | Versioned actions with stated attack coverage |

The common code must not infer an architecture from a frame shape. The port
constructs the frame type and supplies its exact `RawFrameRevision` for crash
tools.

## Nested events, faults, and stack failure

### Ordinary hard interrupts

The safe initial policy keeps ordinary hard interrupts masked until
`BookkeepingEstablished`. It may then allow bounded nesting only for explicitly
higher-priority classes and only on the CPU-local interrupt stack. A non-nested
baseline is easier to validate and should be retained unless latency
measurements justify complexity.

### NMI-like events

NMI-like entry never assumes ordinary interrupt masking or normal lock state.
Component 2 supplies its dedicated stack, separate depth bound, and narrow
primitive allowlist, mints a non-widening `NmiContext`, then passes a bounded
raw-frame view to component 9's staging store. A recursive event while capture
is active enters the smaller terminal stack/path, presents the pinned
`FatalPreclassificationProof` and `FatalCaptureContext`, and selects component
9's recursive terminal slot; it does not overwrite the first frame. A
`CrashContext` exists only after that terminal evidence is sealed.

Architecture names differ: x86 NMI/machine-check, Arm FIQ/SError-like classes,
and RISC-V machine-level events or delegated supervisor events do not have
identical masking and precision. `NmiLike` means the kernel context restriction,
not identical hardware behavior.

### Kernel faults and guarded recovery

A kernel fault is recoverable only when the faulting PC lies in a generated,
typed recovery region whose contract states allowed cause, partial effects, and
resume target—for example, a bounded user copy or boot feature probe. Everything
else becomes a structured kernel fault or fatal event. A global exception table
must not convert arbitrary faults into short reads after privileged state may
have changed.

### Stack exhaustion

Guard faults during ordinary entry switch to fatal capture if the architecture
can do so reliably and the pinned rule can produce
`FatalPreclassificationProof`; that path receives `FatalCaptureContext`, not a
widened hard-entry token. Stack high-water marks are measured under synthetic
maximum nesting. The component never attempts heap allocation to recover an
entry stack. Per-context kernel stack sizing and CPU-local emergency-stack
sizing are part of the pinned port profile.

## Speculation and transition security

The mitigation profile is created during boot from architectural discovery,
microcode/firmware status, errata, and project policy:

```text
EntryMitigationProfile {
    user_to_kernel_actions,
    kernel_to_user_actions,
    cross_domain_actions,
    cross_cpu_actions,
    simultaneous_threading_constraints,
    kernel_mapping_profile,
    evidence_revision,
}
```

Actions can include an entry trampoline and address-space switch, instruction
serialization, branch-predictor or return-stack controls, buffer clearing,
state scrubbing, or scheduling constraints. Each action names the threat class
and processor coverage it claims. “Mitigated” without a profile revision is not
a valid state.

Address-space construction and TLB completion belong to component 3. This
component sequences the already prepared entry/user roots at the privilege
boundary and will not touch secrets until the profile's kernel-addressing
postcondition holds. On hardware not requiring page-table isolation, the
profile can use a shared kernel mapping; the difference remains visible in
benchmarks and assurance claims.

The baseline does not claim elimination of all microarchitectural channels.
Cache, predictor, SMT, and timing isolation require a broader time-protection
and scheduling design. This component is responsible for the transition
actions assigned to it and for stating what remains outside.

## Capability, fault, and scheduling integration

An intentional user call carries a small invocation selector and scalar
arguments into kernel code. The dispatcher resolves a capability in the
calling domain and validates rights before invoking an object. A raw syscall
number or register value is not authority.

User exceptions become structured fault messages containing normalized cause,
user-visible register data allowed by policy, domain/context generations, and
raw architecture evidence needed by a trusted handler. The kernel suspends or
blocks the context until policy replies; it does not implement OTP restart
strategy in the trap handler.

A preemption or blocking decision occurs only after entry accounting is
established. Before a context migrates, extended-state ownership is saved and
its return token is invalidated. Scheduling contexts, CPU budgets, actor
reductions, and load balancing are consumers of this mechanism, not part of
the frame.

## Safety and failure cases

### Incomplete frame capture

If a stub overwrites an argument, status, fault address, or scratch register
before saving it, later normalization cannot repair the evidence. Generated
offsets, instruction-level tests, and register canaries must cover each vector
class separately; “the interrupt path works” does not validate the syscall
path.

### Origin confusion

Nested entry can occur while CPU-local state says “kernel” but the hardware
frame describes a transition from user, or during a partial user return. The
raw frame and transition phase are the source of truth. State machine phases
are explicit so partial-return entry takes a named recovery path.

### Forged return state

Signal/upcall or fault-handler replies may legitimately propose user register
changes, but they never supply a complete raw status word. The kernel builds a
new envelope from allowlisted fields and current generations. Invalid PC/SP,
privilege, feature, debug, or status values produce a user fault or handler
error, not a kernel return fault.

### Context leakage

Leakage can come from integer scratch registers, extended state, debug and PMU
configuration, thread-local bases, protection controls, predictor state, or
uninitialized save-buffer padding. Context buffers are initialized, owned,
bounded, and not copied wholesale to user fault messages. Cross-domain tests
fill every state component with distinct patterns and search the next domain's
architectural and permitted diagnostic view.

### Stale generations

A context can be destroyed and its numeric ID reused while a fault reply,
interrupt, CPU request, or return preparation remains in flight. Domain,
context, address-space, CPU, and mitigation generations travel with frames and
tokens. Any mismatch cancels the return and re-enters lifecycle policy.

### Instrumentation recursion

Sanitizers, tracers, coverage, stack protectors, and profiling can allocate,
touch unavailable CPU-local data, use vector instructions, or recurse. The
protected entry/return sections are placed in named link sections and scanned.
Instrumented code begins only after the transition says it is safe.

## Verification and benchmark plan

### Executable state-machine model

Model every phase, event class, origin, nesting level, interrupt-mask state,
context owner, generation, and return outcome. Check at minimum:

- `LessPrivileged` is reachable only from `ReturnValidated`;
- only a user frame can produce a `ValidatedReturnToken`;
- a `Resident` CPU-unit state exists iff exactly one context has the matching
  `ResidentOn` state, and a new pair cannot commit before the old pair is saved
  or discarded and any required scrub completes;
- an event at every transition either reaches a valid nested state or bounded
  fatal state; and
- a generation change invalidates all prepared returns for the old generation.

### Frame and return property tests

- Generate raw frames across every representable cause and status bit pattern.
- Assert that every semantic `MachineFault` produces
  `ArchitectureFaultFrame`, including NMI-delivered cases, and that only a
  pinned `FatalPreclassificationProof` or recursive entry can select
  `FatalFrame` before classification.
- Round-trip all permitted user register values and prove that rejected bits
  cannot reappear through another path.
- Mutate PC, SP, privilege, interrupt, debug, feature, address-space, and
  generation fields independently and assert rejection before final assembly.
- Compare fast and slow returns for identical allowed semantic state.
- Verify that every invalid final-return condition is converted before the
  return instruction, or reaches a bounded architecture-defined recovery
  vector without exposing kernel state.

### Adversarial nesting and fault injection

Inject an ordinary interrupt, NMI-like event, page fault, debug trap, and
machine fault at every instrumented transition boundary. Test maximum nesting,
guard-page hits, fatal-stack recursion, stale CPU-local base, invalid current
context, forbidden context-token widening, and CPU-offline during prepared
return. Virtual tests are followed by targeted physical tests because emulators
may simplify event timing.

### Context-leakage tests

For each enabled `ContextShape`, domain A fills every writable component with a
recognizable random pattern; domain B then executes after each switch type and
attempts to observe its permitted architectural state, fault records, debug
view, and timing probes. Repeat with termination, migration, interrupt during
save, forced faults, feature disable, and CPU hot-unplug. A passing test is
evidence for covered components, not proof against all transient channels.

### Performance matrix

Measure serialized cycles or a calibrated raw counter for:

- null user call and validated return;
- user fault delivery;
- external interrupt from user and kernel origins;
- same-context enter/return without an extended-state switch;
- same-CPU cross-domain switch for every enabled context shape;
- cross-CPU migration;
- NMI-like minimal capture;
- fast versus general return; and
- each mitigation profile independently and combined.

Report p50, p99, worst observed, distribution, CPU/firmware/microcode,
virtualization, clock source, cache-warm/cold condition, enabled features,
compiler/build manifest, and sample count. Also report entry-stack high-water
marks and context-buffer bytes charged per thread/domain.

Correctness gates optimization: zero direct return bypasses, zero observed
cross-domain architectural leaks in the test matrix, and bounded maximum stack
and nesting come before a cycle target. Performance targets are then set from
reference workloads, including a BEAM-compatible runtime with high message and
timer rates.

## Staged implementation

### Stage 0: model, frame schema, and generated ABI

Define phases, origins, frame variants, return envelope, sensitive status
allowlists, stack classes, context shapes, entry-context types, and the coupled
CPU-unit/context-backing ownership transitions. Generate assembly offsets and
model nested events before executing user code.

### Stage 1: one CPU, integer-only user context

On one virtual target, disable optional FP/vector/debug/performance state.
Implement user call, user fault, one timer interrupt, kernel fault, a guarded
user-copy recovery region, general validated return, and guard-protected
stacks. Run arbitrary user register/property tests.

### Stage 2: fault routing and bounded interrupt deferral

Connect typed user faults and interrupt events to the minimal kernel. Add
preallocated hard-path queues and connect NMI-like entry and recursion
detection to component 9's raw staging, post-classification terminal promotion,
and direct recursive terminal evidence. Keep ordinary interrupt nesting
disabled initially.

### Stage 3: discovered extended state

Enable FP/SIMD first, then one variable-sized vector facility if the target has
it. Preallocate and account buffers, implement ownership generations and eager
cross-domain save/restore or scrub, and run leakage tests before exposing the
feature to the runtime.

### Stage 4: SMP, migration, and mitigation profiles

Integrate CPU lifecycle, address-space generations, remote stop, and
cross-CPU context migration. Implement and measure the selected processor
mitigations, including any entry trampoline/page-table switch.

### Stage 5: second ISA

Port the semantic state machine to an ISA with a materially different raw
frame and return model. Keep the normalized variants and postconditions; split
any contract that had accidentally encoded the first ISA.

### Stage 6: measured fast paths

Add a fast syscall return, lazy save of same-context state, limited interrupt
nesting, or scoped kernel vector use only when its preconditions are machine-
checked/tested, its slow fallback remains correct, and workload measurements
show material benefit.

## Alternatives and tradeoffs

### One universal trap-frame structure

A single maximum-sized frame simplifies some dispatch code but conflates
hardware-saved and software-saved fields, wastes entry-stack space, encourages
returning non-user events, and breaks as variable-sized state grows. Use a
small tagged semantic variant and keep raw layouts private.

### Save all extended state on every entry

This is simple and safe with respect to ownership, but can make every syscall
pay for large vector/matrix state even though the kernel never touches it. The
recommended baseline keeps state owned by the interrupted context across a
same-context entry and eagerly transfers it only before another domain runs or
migration occurs. This is not fault-triggered lazy cross-domain restore.

### Lazy fault-triggered restore

It can avoid work for contexts that never use a feature, but adds faults,
ownership races, migration complexity, and transient-state risk demonstrated
by LazyFP on affected x86 systems. It is a later target-specific optimization,
not the safe default.

### Permit FP/vector use in ordinary kernel code

Compiler auto-vectorization can improve bulk operations but forces every
possible preemption and nested-entry path to understand borrowed state. Start
with a no-vector kernel ABI and add a scoped API only for measured workloads.

### Always use the general return instruction

This offers one final assembly path and usually the simplest assurance story,
at possible syscall cost. It is the correct initial implementation. Add a fast
return only as a refinement of the same validator.

### Exception-less or shared-queue system calls

User/kernel shared queues can amortize entry cost for batches but require
mapping, ownership, wakeup, revocation, and backpressure protocols and cannot
replace faults or interrupts. They may be an IPC optimization above the
baseline call path, not the only control-transfer mechanism.

### Map the kernel into every user address space

This reduces page-table transition cost on processors where permission checks
provide the assumed security. Meltdown invalidated that assumption on affected
machines. Mapping policy must be selected by the mitigation profile, with a
minimal trampoline/separate root available where required.

### Allow unrestricted nested interrupts

Nesting can reduce high-priority latency but multiplies stack, locking,
re-entrancy, and accounting states. Begin with masked ordinary hard paths and a
separate NMI-like path; introduce priority nesting only against a measured
latency requirement.

## Relationship to the OTP/BEAM architecture

Compiled BEAM compatibility does not make a BEAM instruction or process a
kernel entry frame. The managed runtime schedules lightweight language
processes in user protection domains and implements automatic process-local
tracing garbage collection outside the kernel. A kernel execution-context
switch is therefore much coarser and more security-sensitive than an Erlang
process switch.

The runtime consumes:

- a capability-mediated invocation path;
- preemptible CPU budget and deadline events;
- safe user-memory and mapping services;
- typed faults and asynchronous notifications; and
- protection-domain stop and restart.

It does not consume architecture frames, CPU feature registers, raw interrupt
state, or extended-state ownership. OTP-like supervision begins after a fault
has been normalized and the failing user context contained. Entry recursion,
corrupt return state, or unsaved cross-domain CPU state is a kernel integrity
failure, not an actor crash that a supervisor can safely restart.

## Unresolved questions

- Which ISA and virtual/physical platform should define the first raw-frame and
  mitigation profile?
- What exact state belongs in the first `ContextShape`, especially debug, PMU,
  pointer-authentication, tagging, protection-key, and future accelerator
  controls?
- Can the implementation language express linear interrupt/return/ownership
  tokens strongly enough, or are generated dynamic checks necessary?
- Which user-return fields may a fault handler or upcall modify, and how is that
  authority represented?
- What maximum entry and NMI-like nesting depths satisfy real latency
  requirements without making stack proof impractical?
- Which transient-execution mitigations remain necessary on each selected CPU
  and firmware/microcode revision, and how will their evidence expire?
- Does a separate kernel address-space root remain worthwhile on unaffected
  hardware for defense in depth, or does its measurable cost outweigh the
  declared threat model?
- What context-switch budget can a BEAM-compatible runtime tolerate before it
  changes its scheduler/domain partitioning strategy?
- How can binary verification cover the first and last assembly instructions,
  including nested exceptions and final return faults?

## Connections

- [Kernel hardware and architecture support
  layer](kernel-hardware-and-architecture-support-layer.md) defines the wider
  architecture boundary and consumers of entry state.
- [Unsafe architecture-primitives
  capsule](unsafe-architecture-primitives-capsule.md) contains the small vector,
  register, interrupt, mitigation, and return leaves used here.
- [Normalized boot handoff and feature
  discovery](normalized-boot-handoff-and-feature-discovery.md) seals the CPU
  feature, privilege dependency, and mitigation profile that determines
  `ContextShape`.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) supplies
  capabilities, protection domains, execution-stop, bounded IPC, scheduling
  contexts, faults, and lifecycle generations around this mechanism.
- [BEAM, ERTS, and OTP principles for a new operating
  system](beam-erts-and-otp-principles-for-a-new-operating-system.md) explains
  why language-process scheduling and garbage collection remain outside this
  privileged execution-context boundary.
- [Kernel hardware-contract
  inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  tracks the unverified port and performance questions.

## Sources

- [Intel 64 and IA-32 system programming
  documentation](../30-sources/intel-2026-system-programming-documentation.md)
- [Arm A-profile system architecture
  documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [The RISC-V privileged
  architecture](../30-sources/risc-v-international-2026-privileged-architecture.md)
- [Linux kernel low-level core API
  documentation](../30-sources/linux-kernel-community-2026-low-level-core-apis.md)
- [From L3 to seL4: What have we learnt in 20 years of L4
  microkernels?](../30-sources/elphinstone-heiser-2013-l4-lessons.md)
- [Comprehensive formal verification of an OS
  microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
- [LazyFP: Leaking FPU register state using microarchitectural side-
  channels](../30-sources/stecklina-prescher-2018-lazyfp.md)
- [Meltdown: Reading kernel memory from user
  space](../30-sources/lipp-et-al-2018-meltdown.md)
- [Spectre attacks: Exploiting speculative
  execution](../30-sources/kocher-et-al-2019-spectre.md)
