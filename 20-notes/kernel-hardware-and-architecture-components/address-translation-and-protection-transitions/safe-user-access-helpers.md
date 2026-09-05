---
title: "Safe user-access helpers"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - architecture-support
  - capabilities
  - memory-safety
  - security
  - virtual-memory
aliases:
  - "Safe copyin and copyout"
  - "Privileged user-memory access helpers"
---

# Safe user-access helpers

Privileged code should access user memory only through capability-bounded,
fault-recoverable helpers tied to a live address-space access guard. The
baseline should not accept a raw user pointer as authority, should not rely on
an ambient supervisor direct-map alias, and should copy control data once into
kernel-owned memory before interpreting it. Architecture controls such as
SMAP, PAN, or SUM remain normally restrictive and open only inside a lexical,
interrupt-safe access window.

These helpers provide memory-safety and access-mechanism guarantees; they do
not authenticate a caller, authorize an operation, freeze concurrent user
writes, or turn a pin into a coherent snapshot. Those semantics must be
explicit at the API boundary.

This is proposed Atom architecture. Its fault-table ABI, access-window
mechanism, and cross-ISA implementations remain unverified.

## Question, scope, and operational standard

The question is:

> How can privileged kernel paths read or write a domain's memory without raw-
> pointer authority, unrecoverable faults, double-fetch decisions, stale
> address-space use, or a broad alias that defeats hardware isolation?

The helper layer owns:

- checked user-range arithmetic and canonical-address validation;
- capability, address-space-incarnation, and mapping-incarnation revalidation;
- bounded copy, clear, scalar fetch/store, string, and vector operations;
- controlled SMAP/PAN/SUM or equivalent access windows;
- precisely registered fault recovery and cleanup;
- temporary privileged aliases when unavoidable;
- partial-copy, zeroing, cancellation, and concurrency result semantics; and
- interfaces to translation mutation and deferred-shootdown gates.

It does not parse arbitrary application structures, decide business authority,
pin pages indefinitely, or promise transactionality across mutable user
memory. A baseline passes only if:

1. Every access starts from a live, rights-bearing object and an explicit
   address-space incarnation; a numeric virtual address alone has no authority.
2. `base + length`, page rounding, vector summation, and nested-length
   arithmetic are checked without overflow before any dereference.
3. The range lies entirely in the declared user regime, outside kernel/trap/
   metadata exclusions, and within the helper's purpose and byte budget.
4. Faults at every load/store boundary return a typed result, restore all CPU
   and temporary-mapping state, and cannot redirect recovery arbitrarily.
5. Architecture user-access permission is restrictive outside the smallest
   lexical window, including interrupts, preemption, migration, and nesting.
6. Security decisions never compare one user fetch and then act on a second
   fetch of the same mutable control data.
7. Partial results and destination initialization are explicit; no caller can
   mistake uncopied or stale kernel bytes for valid input.
8. A concurrent restrictive transition either waits for the access guard or
   makes the helper fail/retry before old memory can be used.
9. Hard-interrupt/NMI-like paths cannot perform arbitrary pageable user access.

## Evidence and limits

| Evidence | Supported conclusion | Limit |
| --- | --- | --- |
| [Linux VM implementation contracts](../../../30-sources/linux-kernel-community-2026-virtual-memory-implementation-contracts.md) | Mature user-copy APIs distinguish access checks, faultable copy, uncopied-byte results, destination zeroing, and pin semantics | Linux's large API surface and architecture details are precedent, not Atom's contract |
| [SafeFetch](../../../30-sources/duta-et-al-2024-safefetch.md) | Compiler instrumentation plus a byte-granular per-system-call cache can replay the first value for later overlapping fetches | Whole-kernel mediation and caching are not as small as copy-once API discipline |
| [Midas](../../../30-sources/bhattacharyya-et-al-2022-midas.md) | Page-table-mediated guarantees can stop double-fetch attacks with modest reported overhead | The mechanism modifies Linux and relies on evaluated hardware/workloads |
| [ret2dir](../../../30-sources/kemerlis-et-al-2014-ret2dir.md) | A privileged direct physical map can provide an alias around user/supervisor isolation and be exploitable | Attack demonstrations cover particular Linux kernels and mitigations have evolved |
| [Ephemeral mapping management](../../../30-sources/elmeleegy-et-al-2005-ephemeral-mapping-management.md) | Temporary kernel mappings need explicit lifetime, ownership, and bounded resource management | Historical x86 implementation does not establish modern security or concurrency |
| [Secure memory management](../../../30-sources/achermann-et-al-2020-secure-memory-management.md) | Typed mappings and explicit authority can make cross-layer memory operations auditable and least-privileged | The framework is not an implementation of Atom's copy API |
| [Nested Kernel](../../../30-sources/dautenhahn-et-al-2015-nested-kernel.md) | Protecting page-table and isolation machinery from the rest of a privileged kernel can preserve complete mediation under compromise | Threat model and x86 prototype differ from Atom |
| [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md), [Arm A-profile documentation](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md), and [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) | SMAP-like, PAN-like, and SUM-like controls can make supervisor access to user mappings normally unavailable | Exact control, fault, speculation, and interrupt behavior is architecture/profile specific |

The evidence supports explicit access mediation, copy-once parsing, guarded
hardware windows, and avoidance of ambient aliases. The handle types and
snapshot contract below are Atom synthesis.

## Authority-bearing access guard

```text
UserAccessGuard {
    guard_id,
    caller_domain_and_incarnation,
    target_address_space: AddressSpaceIncarnation,
    rights: ReadUser | WriteUser | ClearUser,
    allowed_range,
    purpose,
    maximum_bytes,
    mutation_sequence,
    borrow_epoch,
    borrow_id,
    lifetime,
    revocation_epoch
}

AliasSlotIncarnation = (window_slot_id, slot_generation)
AliasOperationIncarnation = (alias_operation_id, operation_generation)

UserAccessBorrowRecord {
    borrow_id,
    target_address_space: AddressSpaceIncarnation,
    cpu: (CpuIdentity, CpuIncarnation),
    borrow_epoch,
    observed_mutation_sequence,
    normalized_range,
    direction,
    mapping_obligation:
        ResolvedForWholeBorrow(Set<MappingIncarnation>) |
        UnresolvedRange(normalized_range, observed_mutation_sequence),
    installed_translation_mode:
        ExistingTargetRoot(
            activation_guard: ActivationGuardIncarnation,
            binding: TargetTranslationBinding) |
        TemporaryTargetRoot(install_guard: ContextInstallGuard) |
        TemporaryAlias(alias_slot: AliasSlotIncarnation,
                       alias_operation: AliasOperationIncarnation,
                       alias_reservation_id,
                       private_kernel_context_fingerprint,
                       profile_id),
    guard_revocation_epoch,
    state: Publishing | Live | Draining | Released
}

ContextInstallGuard {
    guard_id,
    guard_generation,
    install_owner:
        UserActivation(activation_guard: ActivationGuardIncarnation) |
        UserAccessBorrow(borrow_id),
    target_address_space: AddressSpaceIncarnation,
    cpu: (CpuIdentity, CpuIncarnation),
    binding: TargetTranslationBinding,
    neutral_safe_context_fingerprint,
    allocator_slot_generation,
    install_generation,
    lease_retirement_epoch_at_issue,
    execution_admission_binding:
        UserActivationEpoch(execution_admission_epoch) |
        DataOnlyBorrow(privileged_instruction_fetch_denied_profile_digest),
    state: Installing | LoadingRoot | Installed | RestoringSafeContext | Released
}

SafeContextRestored {
    install_guard_id,
    install_guard_generation,
    install_generation,
    install_owner:
        UserActivation(activation_guard: ActivationGuardIncarnation) |
        UserAccessBorrow(borrow_id),
    target_address_space: AddressSpaceIncarnation,
    cpu: (CpuIdentity, CpuIncarnation),
    binding: TargetTranslationBinding,
    neutral_safe_context_fingerprint,
    allocator_slot_generation,
    local_ordering_and_maintenance_completion_digest,
    may_hold_disposition:
        RetainedForLaterInvalidation |
        RemovedByExactBindingInvalidation(completion_digest)
}

InstallWithdrawnSafe {
    install_guard_id,
    install_guard_generation,
    install_generation,
    install_owner:
        UserActivation(activation_guard: ActivationGuardIncarnation) |
        UserAccessBorrow(borrow_id),
    target_address_space: AddressSpaceIncarnation,
    cpu: (CpuIdentity, CpuIncarnation),
    binding: TargetTranslationBinding,
    allocator_slot_generation,
    proof_no_root_load_and_slot_no_binding,
    withdrawal_ordering_digest
}
```

The capability layer creates the guard after validating and unsealing the
caller's kernel-side object reference and separately authorizing the direction, target, range,
purpose, and budget. Guard acquisition is not complete until the helper has
joined the address space's live-borrow ledger: it reads `state == Live`, an
even mutation sequence, and the borrow epoch, publishes a generation-bound
borrow with release
ordering, executes the profile/compiler's full Store→Load fence, rereads the
mutation sequence, borrow epoch, **and lifecycle state** with acquire ordering,
and withdraws/retries
if either generation changed or the sequence is odd. For a profile in which
this helper's root could permit privileged instruction fetch, acquisition also
requires an owner-free execution-admission gate at the observed epoch before
and after publication; a code-publication suspension advances/closes that
epoch and drains the frozen borrow set. `Closing`, `Quarantined`,
or `Dead` withdraws the record and returns the corresponding terminal admission
failure; it never retries into a non-live object. Only then may it revalidate
the guard and open the access window. It
holds that linear borrow across the last possible access and removes the ledger
record with release ordering only after the window is closed; drain observation
uses acquire semantics.

`TargetRoot` access must also join the context allocator's installation and
retirement protocol. The common current-domain path borrows an already
installed same-CPU `ActivationGuard` and records its exact
`TargetTranslationBinding`; it cannot substitute a tag from another CPU scope.
The borrow participates in that guard's linear drain. A publication suspension
cannot become `Held` until every frozen guard is consumed or terminally
unusable and every outstanding borrow has released; closed activation prevents
a post-snapshot replacement guard.
A cross-domain root switch instead consumes an allocator-issued
`ContextInstallGuard<UserAccessBorrow>` whose `DataOnlyBorrow` binding proves
the pinned profile prevents privileged instruction fetch through the target
mapping independently of this data-access window. A profile without that
property must include and drain these borrows in any code-publication execution
suspension. Before loading the target root, the CPU publishes
`Installing(binding, install_generation)` with release ordering,
executes the allocator's full Store→Load fence, and acquire-rechecks namespace
generation, rollover state, the current accepted address-space mutation
sequence, `ContextTagLease.state == Active`, the unchanged lease retirement
epoch, root fingerprint, profile, and pending flush/catch-up state. The helper
rechecks the sequence and pending state once more before opening its hardware
access window.
It retries from a safe context if any changed. Only a valid guard permits a
release transition to `LoadingRoot`; that state is published before the first
root/tag-changing instruction and is followed by `Installed`. Any trap or
ambiguous machine result in `LoadingRoot` must restore the neutral context and
produce `SafeContextRestored`; it can never use the no-root-load abort. A
concurrent rollover must observe and reserve that
installing/loading/installed/restoring-safe-context CPU or the installer must observe the
rollover and withdraw. An ordinary `Active` → `Retiring` transition follows the
same rule: it atomically denies new installs and advances the retirement epoch
before its fenced scan, so a pre-issued guard cannot publish `Installing`
without either being captured or observing retirement and withdrawing.

The baseline conservatively freezes every nonterminal old-epoch borrow
(`Publishing`, `Live`, or `Draining`) whose `normalized_range` overlaps the
restrictive operation. Promotion from `Publishing` to `Live` performs one more
compare-and-transition against the unchanged even sequence and borrow epoch;
it cannot change the record's range, CPU incarnation, or mapping bindings. As
part of publication, `mapping_obligation` is immutable: it is an exact set only
if the complete borrow range was pre-resolved, otherwise it is the normalized
range plus observed sequence. Chunk-resolution details may be appended to a
diagnostic trace, but cannot narrow or mutate the security obligation after
publication. A mutator therefore seals either the exact set or the conservative
range; it never uses an unproved generation “floor” to omit a possible old
observer.

The guard is not a transferable integer and does not contain a page-table
root. It prevents address-space-ID reuse and confused-deputy access to another
domain's pointer. An attenuated guard can narrow rights, range, purpose, bytes,
or lifetime, never broaden them.

For a syscall, the target will commonly be the current domain's address space,
but that is an explicit equality check rather than an ambient assumption.
Cross-domain copy requires a separate delegated capability and is preferably
implemented through message or buffer transfer instead.

## Range validation

Before enabling access, compute a normalized half-open range `[start, end)`:

1. Reject `length > guard.maximum_bytes` and per-operation policy limits.
2. Use checked addition for `start + length`; reject wrap.
3. For a nonempty range, validate canonicality and implemented virtual-address
   width for `start` and the last included byte `end - 1`, then validate
   containment. `end` is an exclusive boundary and may itself be the first
   excluded address.
4. Check the whole range is user accessible under the frozen translation
   profile and within `guard.allowed_range`.
5. Reject intersection with guard/trampoline, kernel, device, page-table,
   metadata, or deliberately inaccessible regions.
6. Validate direction-specific effective mapping rights and memory type as
   pages are faulted or resolved.
7. Pass a speculation-safe, normalized length/index to the copy primitive.

Zero length has a documented no-access result and never dereferences `start`.
Strings and iovectors have independent maxima on element count, aggregate
bytes, nesting depth, and termination search. Page-count and alignment
calculations use checked arithmetic too.

An early range check is necessary but not sufficient: mappings can change and
pages can fault. The live access guard and transaction protocol establish how
that race resolves.

## Copy-once control-data rule

If privileged code will branch, allocate, authorize, index, or choose a target
from user-provided control data, it must:

1. validate an upper bound;
2. copy the entire controlling representation once into initialized kernel-
   owned memory;
3. validate its internal offsets, lengths, discriminants, and version there;
4. use only that snapshot for decisions; and
5. copy bulk payload separately under semantics that tolerate concurrent
   mutation or use a stronger leased-buffer protocol.

It must not validate `user_header.length`, reread the header, and then copy
using the second value. It must not follow nested user pointers after only
copying the outer pointer array unless each pointer/range is independently
validated and the API intentionally permits a non-atomic live view.

Copy-once is a kernel software snapshot of the copied bytes. It is not an
atomic snapshot with respect to several cache lines while the user writes
during the copy. Protocols needing atomic multiword state use versioned shared
memory, immutable sealed buffers, message transfer, or explicit application
synchronization rather than silently strengthening `copy_from_user`.

## Core API and result types

```text
copy_from_user(guard: ReadUser, destination: InitializedKernelBuffer,
               source: UserRange)
  -> CopyInResult

copy_to_user(guard: WriteUser, destination: UserRange,
             source: KernelBuffer)
  -> CopyOutResult

CopyInResult = Complete(bytes)
             | Partial(bytes_copied, fault, destination_tail_zeroed)
             | Rejected(reason)
             | Interrupted(bytes_copied)

CopyOutResult = Complete(bytes)
              | Partial(bytes_copied, fault)
              | Rejected(reason)
              | Interrupted(bytes_copied)
```

Atom's safe `copy_from_user` baseline should zero the uncopied destination tail
on any partial result, including failures from later vector elements. An
internal raw primitive may report “bytes not copied,” as Linux does, but it is
not a general kernel API and can write only into a buffer whose initialization
state is tracked.

Scalar fetch/store return `Result<T, UserAccessFault>` and never leave a
partially initialized `T`. String copying returns length/termination status and
does not scan beyond the caller's explicit bound. Vector copy reports the
element and byte offset of a fault.

Copy-in callers must select one of:

- `RequireComplete`: the caller takes no semantic action and consumes none of
  the kernel destination unless all requested bytes arrived;
- `AcceptPartial`: a streaming/data API explicitly consumes the prefix; or
- `Retryable`: the caller can restart using an application-level generation.

This prevents a generic byte count from acquiring inconsistent meanings.
Copy-out is different: a fault after several stores leaves a user-visible
prefix and the generic helper cannot roll it back. Every copy-out policy must
therefore expose prefix progress, unless a separate prevalidated transactional
buffer or ownership-transfer protocol performs an atomic publication step.

## Fault-recovery contract

Only load/store instructions emitted in an audited helper region may use the
user-access recovery table. Each entry maps an exact faulting instruction or
bounded interval to a fixed cleanup continuation. The trap handler validates:

- current CPU and kernel stack state;
- active helper and nesting token;
- fault address and architecture syndrome;
- permitted exception class;
- matching recovery-table entry; and
- outstanding access-window/temporary-map cleanup state.

It then records progress, disables user access, releases temporary mappings or
pins as specified, restores preemption/migration/interrupt state, and returns a
typed fault. A malformed kernel pointer, page-table corruption, execute fault,
or fault outside the table remains a kernel fault; the mechanism is not a
generic exception-swallowing region.

Page faults that policy may resolve are handed to an unprivileged pager only
after leaving any state the pager would need. Restart checks the guard,
address-space incarnation, mutation sequence, and remaining range again.

## Hardware access window

On supported profiles:

- x86 keeps SMAP enforced and uses the smallest reviewed AC-open interval;
- Arm keeps PAN enforced and uses the appropriate privileged-access mechanism
  only around the transfer; and
- RISC-V keeps SUM clear and sets it only for a reviewed S-mode data access.

The window is represented by a linear `CpuUserAccessWindow` token. Entry pins
the CPU or otherwise prevents migration, records nesting, constrains preemption
as required, and establishes the architecture barrier/speculation contract.
Exit closes the permission before restoring ordinary scheduling or interrupts.

If normal interrupts remain enabled, their prologue must force the restrictive
state and restore only through validated nesting state. If the architecture
cannot make that safe, interrupts are masked for a strictly bounded copy chunk,
not an unbounded user length. NMI-like paths always observe the restrictive
state and cannot borrow the interrupted helper's authority.

## Translation mutation and deferred shootdown

Entering a helper publishes a privileged-access borrow against the address-
space mutation sequence using the two-sided handshake above. Acceptance of a
restrictive mapping transaction atomically changes the sequence to odd **and
advances the borrow epoch**, thereby closing new borrow acquisition; after its
full Store→Load fence it acquire-scans the preceding borrow epoch and freezes
every overlapping nonterminal `Publishing`, `Live`, or `Draining` borrow. Each
drain token is bound to the address-space incarnation, old borrow epoch, borrow
ID, CPU incarnation, and frozen exact-set-or-range `mapping_obligation`.
Borrow IDs and epochs are not reused until wrap establishes a
broad absence proof. The transaction
must then either:

- wait for pre-existing borrows to exit before claiming
  `CpuAccessQuiescent`; or
- close future chunks, let the current bounded chunk finish under its pinned
  old mapping, and retain the frame until the borrow is discharged.

The baseline should choose the first, simpler contract. Every borrow-owning CPU
that may retain its exact target-root translation binding or a temporary alias
is unioned into the invalidation target set. Its target request carries a
nonempty bounded observer-binding set: `TargetRoot(binding)` records the scope
key, context-tag incarnation, root fingerprint, retirement epoch, and profile,
while `TemporaryAlias` records the CPU-private alias slot, operation,
reservation, kernel-context fingerprint, and profile without inventing an ASID
lease. A CPU retaining both modes carries both members. A temporary-alias borrow
cannot release its record
until it has removed that alias, completed the required local invalidation, and
published `BorrowTranslationReleased`; the aggregate CPU-translation proof
includes that evidence. It emits
`CpuAccessQuiescent` only after every frozen old borrow has drained or its CPU
incarnation is terminally excluded. The CPU separately checks pending
shootdown/context generations before opening its window and again before
returning to user mode. `RestrictionQuiescent` is the conjunction of this
access-borrow proof and `CpuTranslationQuiescent`; neither notification nor an
early `CpuUserReturnClosed` acknowledgement can claim old access is closed
while an active helper may still dereference the mapping.

A `TemporaryTargetRoot` borrow has the symmetric release rule. After the final
access and after closing the hardware access window, it first release-publishes
the allocator slot as `RestoringSafeContext`, then installs the recorded neutral
safe context and performs every profile-required local maintenance step. It
clears current residency to `NoBinding` and consumes `ContextInstallGuard` into
the exact `SafeContextRestored` proof above. The mapping-borrow record remains
nonterminal until that proof exists; only then can it publish `Released`. The
proof is accepted here only when `install_owner == UserAccessBorrow` names this
exact borrow ID. A failure before root load instead consumes the still-
`Installing` guard into `InstallWithdrawnSafe`; that proof likewise must name
this borrow and its proof must establish no root load and `NoBinding`. The
borrow remains nonterminal until either exact departure proof is validated.
Failure to prove restoration transfers both guards, the exact binding, and the
CPU-local slot to quarantine. Borrowing an existing `ActivationGuard` never
releases or retargets that guard; it merely validates the still-current binding
before and after the bounded access. This baseline does not restore an arbitrary
prior user context; re-entry to one requires its own still-current
`ActivationGuard` and the ordinary final sequence and pending-state checks.

The restoration entry point also accepts an interrupted
`RestoringSafeContext` guard and resumes idempotently with the same install
generation and neutral-context fingerprint; it does not require a new guard.

Access borrowing must not hold a mutation lock across a pageable fault that
requires the mapping transaction to progress. The model needs an explicit
fault/retry edge and lock order.

## Temporary privileged mappings

The preferred path uses the target address space under a guarded hardware
window, without a supervisor direct-map alias for user frames. When a backend
requires a temporary alias, it uses a bounded object:

```text
UserAccessMapping {
    alias_slot: AliasSlotIncarnation,
    cpu_and_incarnation,
    private_kernel_context_fingerprint,
    profile_id,
    frame_and_mapping_incarnations,
    direction,
    rights,
    non_executable: true,
    memory_type,
    alias_operation: AliasOperationIncarnation,
    alias_reservation_id,
    alias_state: PendingAdd | Live | RetiringOldAccess,
    lifetime
}

BorrowTranslationReleased {
    borrow_id,
    target_address_space: AddressSpaceIncarnation,
    cpu: (CpuIdentity, CpuIncarnation),
    alias_slot: AliasSlotIncarnation,
    alias_operation: AliasOperationIncarnation,
    alias_reservation_id,
    private_kernel_context_fingerprint,
    profile_id,
    local_removal_and_invalidation_completion_digest
}
```

The secure baseline requires the mapping to be CPU-local and visible only in a
CPU-private kernel translation context, and it is never executable. A backend
that exposes the alias through a shared kernel root is not this baseline: it
must declare a separate profile with an explicit sharing-domain/root binding,
a frozen may-hold CPU-incarnation set, remote completion for every such target,
and matching observer bindings in plan, request, and evidence digests. Without
those proofs the helper is unsupported, not merely weaker by convention.
Before installation, the helper acquires a generation-bound reservation for the
complete canonical physical extent/backing lineage in the same globally
ordered alias ledger used by CPU mappings, code publication, IOMMU/DMA,
device, and diagnostic aliases; a pending executable or incompatible memory-
type entry conflicts. It revalidates frame authority and the complete ledger
under that reservation, releases it on pre-effect rejection, and records the
alias first as operation-owned `PendingAdd`, then `Live`, before use.

Teardown moves the entry to `RetiringOldAccess`; that remains a W^X and memory-
type hazard until the CPU-local alias is removed, required local invalidation
has completed, and a `BorrowTranslationReleased` with every exact nominal
identity above permits release of the borrow. A slot or operation generation
without its object ID cannot discharge another alias.
Only then may the ledger entry and reservation be removed. Uncertain teardown
transfers the slot, frame pin, borrow, and alias reservation to a named
quarantine. Slots are preallocated and bounded; exhaustion returns a typed
failure or waits outside critical state.

The ret2dir result motivates a strong baseline: ordinary kernel code has no
ambient writable/executable direct alias for user-controlled frames. If a
platform cannot eliminate such an alias during bring-up, that limitation is a
named weaker security profile, not hidden behind SMAP/PAN/SUM.

## Pins, snapshots, and large payloads

A pin proves that the backing frame and mapping relation will not be reclaimed
during the lease. It does not prove that user code or a device cannot change
the bytes. APIs must name this distinction:

- `PinnedMutable`: stable backing, live contents;
- `CopiedSnapshot`: kernel-owned bytes as observed during a bounded copy;
- `SealedImmutableBuffer`: contents frozen by a separate protocol; and
- `ExclusiveTransfer`: ownership moved so the sender can no longer mutate.

Small control records use `CopiedSnapshot`. Large data should use chunked
copies with explicit partial semantics or capability-backed leased/transfer
buffers, not one long interrupt-constrained window. Long-lived pins are quota-
charged and cannot prevent teardown without a visible lease owner.

## Concurrency and execution-context restrictions

- General user copies run only in a faultable thread context.
- Hard interrupt and NMI-like contexts may copy only previously pinned,
  nonfaulting, explicitly authorized fixed-size data through a separate API—or
  preferably enqueue work to a thread.
- Preemption and migration rules are encoded in the access-window token; no
  helper assumes CPU locality informally.
- Cancellation is checked between bounded chunks. Cleanup completes before an
  interrupted result is returned.
- Nested helpers are rejected by default. A proven nesting profile records and
  restores direction, window state, and outer progress exactly.
- Concurrent unmap/revocation closes new guards and waits for existing borrows
  or retains their resources; it never invalidates a live raw pointer behind
  an untracked helper.

## Speculation and transient execution

Range validation and SMAP/PAN/SUM do not by themselves prove that transient
execution cannot use an attacker-controlled index. The backend records the
profile's required speculation barrier or data-dependency pattern between
range normalization and the first access. Kernel destinations and later array
indices are bounds-checked using the copied snapshot.

Sensitive copyout buffers are fully initialized before the window opens. Fault
paths do not reveal uninitialized tails, kernel addresses, unrelated residual
bytes, or high-resolution architectural diagnostics to an unprivileged caller.
Microarchitectural side-channel resistance beyond these baseline rules needs a
separate threat model and measurement campaign.

## Verification and testing

- Property-test every range calculation near zero, canonical boundaries,
  excluded regions, maximum user address, and integer wrap.
- Fault-inject every load/store byte and page boundary; assert destination-tail
  zeroing, window closure, pin release, and exact progress.
- Mutate length, discriminant, iovec array, nested pointers, and payload during
  copy; control flow must use only the kernel snapshot.
- Race copy with unmap, permission reduction, frame replacement, address-space
  close, capability revocation, CPU migration, and deferred shootdown.
- Interrupt and nest at every access-window instruction; NMI/debug paths must
  never inherit user access.
- Search generated privileged code for unauthorized user-memory loads/stores
  and unregistered recovery entries.
- Map attacker-controlled frames at direct-map-correlated addresses in the
  adversarial backend and verify no ambient alias is usable.
- Model the borrow/mutation protocol and prove old frame reuse implies no live
  helper can access it.
- Measure bytes/cycle, fault latency, bounded interrupt-off time, window-open
  duration, temporary-map churn, and tail latency by copy size.

A SafeFetch-like first-fetch cache can serve as a compatibility profile for
code that cannot yet obey copy-once discipline; separate instrumentation can
report those repeated-fetch sites. Midas-like page-table enforcement is a
possible stronger deployment profile, not a substitute for a small default API
until its portability and interaction with Atom's mapper are demonstrated.

## Staged implementation

1. Provide complete-only scalar and bounded-buffer copies in faultable thread
   context, one access window per bounded chunk, and no ambient user-frame
   direct alias.
2. Add strings/iovectors, exact recovery-table generation, static call-site
   checking, mutation-borrow modeling, and exhaustive fault injection.
3. Add capability-backed large-buffer lease/transfer APIs and bounded temporary
   mappings only for architectures that require them.
4. Evaluate duplicate-fetch detection and page-table-enforced snapshot modes
   with explicit performance and threat-model results.

## Alternatives and tradeoffs

- **Direct user-pointer dereference** is compact but makes a numeric address
  ambient authority and scatters recovery/access-window obligations.
- **Permanent direct physical map** simplifies many kernel operations but
  creates aliases that can undermine hardware user/supervisor protections.
- **Pin and parse in place** avoids copying but stabilizes only backing, not
  contents, so it is unsuitable for mutable control data.
- **Always copy entire payloads** gives clear ownership at high bandwidth and
  latency cost; leases or ownership transfer fit large data better.
- **Hardware/page-table double-fetch prevention** can strengthen legacy code,
  but a small copy-once API reduces the proof surface first.

## Unresolved questions

- Can all supported ISAs eliminate routine privileged aliases for user frames,
  including firmware and crash/debug paths?
- What exact interrupt/preemption discipline minimizes open-window time without
  imposing unacceptable latency on large copies?
- How should BEAM binary and message transfer use sealed or exclusive buffers
  to avoid redundant copies while preserving process isolation?
- Which page faults may safely be resolved and retried without creating a
  lock-order cycle with mapping transactions?
- What transient-execution mitigations belong in each machine profile and how
  will their sufficiency be measured?
- Should compatibility builds deploy SafeFetch-like first-fetch caching, and
  can static analysis report duplicate fetches and reject raw user-pointer
  dereferences completely?

## Connections

- [Address translation and protection transitions](../address-translation-and-protection-transitions.md)
- [Address-space object](address-space-object.md)
- [Mapping validator](mapping-validator.md)
- [Mapping transaction](mapping-transaction.md)
- [Shootdown coordinator](shootdown-coordinator.md)
- [Reclamation gate](reclamation-gate.md)
- [Capability spaces and authority](../../minimal-privileged-kernel-components/capability-spaces-and-authority.md)
- [Interrupt event fabric](../interrupt-event-fabric.md)
- [Privileged entry, exit, and execution context](../privileged-entry-exit-and-execution-context.md)

## Sources

- [Linux VM implementation contracts](../../../30-sources/linux-kernel-community-2026-virtual-memory-implementation-contracts.md)
- [SafeFetch](../../../30-sources/duta-et-al-2024-safefetch.md)
- [Midas](../../../30-sources/bhattacharyya-et-al-2022-midas.md)
- [ret2dir](../../../30-sources/kemerlis-et-al-2014-ret2dir.md)
- [Ephemeral mapping management](../../../30-sources/elmeleegy-et-al-2005-ephemeral-mapping-management.md)
- [Secure memory management](../../../30-sources/achermann-et-al-2020-secure-memory-management.md)
- [Nested Kernel](../../../30-sources/dautenhahn-et-al-2015-nested-kernel.md)
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md)
- [Arm A-profile documentation](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md)
