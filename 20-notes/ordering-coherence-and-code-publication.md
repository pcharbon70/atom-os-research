---
title: "Ordering, coherence, and code publication"
kind: note
created: "2026-09-02"
maturity: developing
tags:
  - architecture-support
  - cache-maintenance
  - concurrency
  - instruction-fetch
  - just-in-time-compilation
  - memory-ordering
aliases:
  - "Kernel ordering component"
  - "Executable-code publication protocol"
---

# Ordering, coherence, and code publication

The kernel needs one small vocabulary for ordinary shared-memory
synchronization and several separate protocols for translation, MMIO, DMA,
cache maintenance, and instruction fetch. It should not expose an omnipotent
`barrier()` and let callers guess what it orders.

The recommended implementation is a data-race-free kernel memory model based
on the implementation language's acquire/release atomics and locks; typed
device and DMA accessors outside that model; backend-private architecture
fences; and a first-class immutable-code publication transaction. New native
code is built in a writable, non-executable staging mapping, sealed, made
fetch-visible on every eligible CPU, mapped executable without a writable
alias, and published by an atomic version/entry-point change. Old versions are
retired only after execution quiescence. In-place incompatible patching is not
part of the baseline.

This is a proposed design. Architecture manuals and formal work establish the
hazards and some required sequences; they do not verify this project's API or
implementation.

## Question, scope, and operational standard

The question is:

> What common contract lets portable kernel protocols, drivers, and a
> BEAM-compatible runtime establish the ordering and instruction-fetch effects
> they actually need without leaking ISA mnemonics or relying on accidental
> cache behavior?

This component owns:

- the kernel's allowed atomic widths and memory orders;
- the mapping from that language-level model to each architecture backend;
- semantic compiler and CPU fence primitives used inside named protocols;
- typed MMIO ordering and posted-write completion operations;
- cache-maintenance plans used by translation, DMA, and code publication;
- writable-to-executable publication and executable-version retirement; and
- test models and generated-code audits for those contracts.

The translation component owns TLB and page-table-walker completion. The DMA
component owns buffer and device ownership. Drivers own device-register
protocols. A BEAM runtime owns module validation, native lowering, hot-code
policy, stack maps, and safe-point semantics. This component composes with
those owners but does not absorb their policy. It is the sole public
orchestrator that can turn a sealed `ExecutableImage` into `PublishedCode`.
Translation exposes only prepared, crate-private executable-mapping effects to
an unforgeable `Authorized<CodePublication>` caller; it never publishes code or
grants execute authority directly.

The first implementation is adequate when:

1. Every shared kernel protocol is data-race-free under one pinned language
   memory model or explicitly uses a separately modeled low-level primitive.
2. The same source-level atomic contract passes executable litmus tests on at
   least two materially different ISA backends.
3. MMIO, DMA, page-table, and code-fetch ordering are distinct in types and
   documentation; an ordinary atomic fence cannot be substituted silently.
4. Code cannot become executable before all bytes and metadata are sealed and
   every CPU eligible to execute that version has completed its required fetch
   synchronization.
5. No baseline transition leaves a frame simultaneously writable and
   executable through any CPU alias.
6. CPU migration cannot move a runtime thread to a CPU that missed publication.
7. A failed remote synchronization keeps the new version unpublished and its
   frames pinned or confined; it yields an explicit terminal `Incomplete` or
   quarantine record, never partial executable success or a late
   `CodePublishError`.
8. Retirement cannot reclaim or rewrite code while any CPU may execute or
   return into it.

## Evidence and its boundaries

| Evidence | Supported conclusion | Explicit boundary |
| --- | --- | --- |
| [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md) | x86 ordinary memory is strong but not sequentially consistent; formal models are preferable to folklore | Excludes self-modifying code, exceptions, page tables, and devices |
| [Multicopy-atomic Armv8 model](../30-sources/pulte-et-al-2018-simplifying-arm-concurrency.md) | Arm ordinary-memory acquire, release, dependencies, atomics, and barriers have distinct executable semantics | Does not establish translation, instruction fetch, MMIO, or DMA behavior |
| [Linux kernel concurrency model](../30-sources/alglave-et-al-2018-linux-kernel-concurrency.md) | A portable kernel can maintain an executable software memory model and litmus suite | The published model explicitly excludes interrupts, self-modifying code, I/O, and other mechanisms |
| [Arm instruction-fetch semantics](../30-sources/simner-et-al-2020-arm-instruction-fetch.md) | Data writes, cache maintenance, barriers, pipeline state, and cross-core fetch form a separate system protocol | Covers Arm, not this kernel's authority or lifecycle |
| [RISC-V unprivileged ISA](../30-sources/risc-v-international-2026-unprivileged-architecture.md) | RVWMO, I/O fence classes, and local `FENCE.I` are distinct; remote code publication needs more than the writer's local fence | The execution environment must supply remote action and cache facilities |
| [RISC-V SBI](../30-sources/risc-v-international-2025-supervisor-binary-interface.md) | Remote `FENCE.I` can be requested through a versioned, fallible firmware boundary | A successful request is not automatically this project's migration, lifetime, or fault proof |
| [Arm engineering guidance for threaded self-modifying code](../30-sources/bramley-2025-arm-self-modifying-code-threads.md) | The writing core's local instruction synchronization is not broadcast; full cooperation and best-effort compatible patching are different contracts | Engineering explanation, not a formal proof or benchmark |
| [Linux low-level API documentation](../30-sources/linux-kernel-community-2026-low-level-core-apis.md) | Compiler, CPU, I/O, DMA, and cache/TLB operations need separate semantic interfaces | Linux's compatibility surface is not a minimal design requirement |
| [The Road to the JIT](../30-sources/gustavsson-2020-road-to-the-jit.md) | BEAM native execution is constrained by hot loading, scheduling, tracing, and whole-system behavior, not instruction throughput alone | Historical engineering account; it does not specify an OS publication primitive |

The claim ledger must remain explicit: a proof about ordinary-memory
happens-before does not justify a device-doorbell order, page-table reuse, or
instruction-fetch completion. “Coherent machine” is not a substitute for
naming the participating agents and completion point.

## Semantic taxonomy

The common vocabulary should distinguish six relations.

| Relation | Participants | Typical question | Owning API |
| --- | --- | --- | --- |
| Compiler ordering | Source operations and compiler transformations | May the compiler move or eliminate this access? | Language atomics and private compiler barriers |
| CPU ordinary-memory ordering | CPUs observing coherent normal memory | Does a consumer see initialized state after a publication flag? | Atomics, locks, and CPU fences |
| Device-I/O ordering | CPU and device-register/interconnect accesses | Did descriptor writes precede the doorbell, and did a posted write arrive? | Typed MMIO accessors and explicit flush/readback |
| DMA visibility | CPU caches, interconnect, IOMMU, and device | Does the current owner see the buffer contents? | DMA publish/consume composed with ownership transfer |
| Translation ordering | CPU stores, page-table walkers, and TLBs | Can any CPU still use the old mapping? | [Translation transaction](address-translation-and-protection-transitions.md) |
| Instruction publication | Data stores, caches, pipelines, and executing CPUs | May every eligible CPU fetch the complete new code version? | `CodePublication` lifecycle |

One backend instruction may satisfy several relations on one machine. The
types remain separate because another architecture, cacheability mode, or
interconnect may require different operations.

## Recommended ordinary-memory model

### Data-race-free baseline

Ordinary shared kernel data must be protected by a lock or accessed through an
atomic type. Racy non-atomic reads, even when aligned or declared volatile,
are forbidden. Volatile semantics are reserved for MMIO or narrowly audited
compiler interactions; volatility neither creates inter-CPU happens-before
nor makes a multi-step protocol atomic.

Supported atomic operations should initially be limited to naturally aligned
word and pointer widths that are lock-free on every baseline backend. The
portable facade exposes:

- relaxed operations for atomicity and per-location modification order only;
- acquire loads and successful read-modify-write operations;
- release stores and successful read-modify-write operations;
- acquire-release read-modify-write operations;
- sequentially consistent operations only where a global order is actually
  part of the protocol; and
- explicit compare/exchange failure ordering.

Unsupported widths fail at build time or use an explicit lock object whose
interrupt, nesting, and blocking properties are part of the call site. A
compiler-emitted hidden lock is unacceptable in hard-interrupt or NMI-like
code.

### Protocol-shaped wrappers

Most callers should use an object operation such as `binding_publish`,
`queue_push`, or `mapping_close`, not insert a free-standing fence. Within
those implementations, release publishes fully initialized immutable state;
acquire obtains a stable reference. Refcounts, generations, and sequence
counters state their overflow and ABA rules.

The unsafe architecture capsule may contain compiler and CPU fence primitives,
but use outside the ordering component and audited leaf protocols is rejected
by convention or visibility rules. This makes missing semantics reviewable.

### Interrupt interaction

Disabling local interrupts is not a memory order and affects no remote CPU.
Likewise, an acquire/release pair does not prevent an interrupt handler from
re-entering a non-reentrant CPU-local structure. Each structure separately
declares:

- ordinary-thread synchronization;
- local interrupt masking or interrupt-safe atomic requirements;
- NMI-like accessibility;
- migration or preemption exclusion; and
- maximum lock or retry bound.

## Typed device and DMA ordering

### MMIO

An `MmioRegion<Profile>` carries permitted offsets, access widths,
endianness, memory type, side-effect rules, and ordering capabilities. Useful
operations include:

```text
mmio_read_relaxed(region, register)
mmio_write_relaxed(region, register, value)
mmio_read_ordered(region, register, before_after)
mmio_write_release(region, register, value)
mmio_posted_write_complete(region, completion_register)
```

These names describe minimum effects. A backend or device profile may
strengthen them. A readback is used only when the device or interconnect
contract identifies it as the posted-write completion mechanism; random
readbacks can have device side effects and are not a universal fence.

Register access validation and device policy remain in the protected-I/O
component. This ordering component supplies the safe access mechanism after
authority has been checked.

### DMA

DMA operations attach visibility to ownership:

```text
dma_publish_to_device(buffer_lease, written_range, direction)
dma_consume_from_device(buffer_lease, completed_range, direction)
```

The DMA profile decides whether those operations are no-ops on coherent
buffers, cache clean/invalidate sequences on non-coherent buffers, or errors
for unsupported aliases. The operations do not transfer ownership by
themselves; the queue protocol does that atomically with descriptor or
completion state.

A CPU fence alone does not invalidate an IOMMU translation or prove that a
device stopped writing. Conversely, an IOTLB completion does not make dirty
CPU cache lines visible to the device.

## Executable-image model

### Objects and authority

`ExecutableImage` is a kernel-visible aggregate for opaque bytes. The kernel does
not parse BEAM instructions, stack maps, native relocations, or module names.
It records:

- image identity and generation;
- backing frame set and exact initialized byte range;
- writer domain and `CodeWriteLease` generation;
- current CPU mappings and rights;
- content digest if required by a higher security profile;
- publication target CPU set and completed CPU set;
- executable-version identity;
- retirement epoch; and
- state and failure evidence.

Ownership is split deliberately. The minimal privileged kernel owns the
capability-bearing, resource-accounted `ExecutableImage` wrapper, its frame
and mapping references, and destruction ledger. The ordinary `Frame` and
`Mapping` objects remain authoritative for storage and translation; the image
does not duplicate them or create another storage owner. This component owns
the private `CodePublicationState` referenced exclusively by that aggregate:
write and publication generations, cache/fetch progress, target-set evidence,
and terminal completion. Neither the backend state nor its raw handles are
minted directly to a caller.

The aggregate has one payer `ResourceAccount` and one owning `LifetimeGroup`.
Its public rights are attenuated state views rather than independent objects:

| View or facet | Permitted authority | Closing/lifetime rule |
| --- | --- | --- |
| `CodeWriteLease` | Write only the admitted initialized range; never execute | Seal consumes the final writer generation and waits for admitted stores |
| `SealedCode` | Submit the immutable image with a `PublicationSet` for publication | Holds every frame/mapping reference while an accepted publication operation can complete |
| `PublishedCode` | Install or execute the exact published version; inspect its generation | Grants no write; retirement first removes reachability and waits for execution quiescence |
| image retirement/reclaim facet | Start retirement and inspect or reclaim terminal state | Reclaim waits for writer closure, publication/retirement operation drainage, execution quiescence, mapping/TLB completion, and diagnostic or unwind references |

A failed publication therefore leaves the aggregate pinned or explicitly
quarantined; dropping a public view cannot release a frame behind an admitted
operation. Moving the aggregate's charge uses the minimal kernel's normal
two-account transfer and moves no underlying authority implicitly.

The loader or JIT holds write authority during construction. Execute authority
is a separate facet granted only after the write lease is closed and cache,
translation, and remote-fetch protocols complete. No handle grants both in the
baseline.

### Publication state machine

```text
Allocated
   -> WritableOwned(write_generation)
   -> Sealing(no_new_writers)
   -> Sealed
      +-- admission rejection --> Rejected(CodePublishError, SealedCode)
      +-- fully reserved ------> PublicationAccepted(
                                  CodePublicationOperation,
                                  frozen_publication_set,
                                  owned_resources)
          -> DataVisible(cache_scope)
          -> WritableTranslationClosed(tlb_epoch)
          -> ExecutableMappedButUnreachable(mapping_generation)
          -> InstructionStateInvalidated(cache_scope)
          -> RemoteFetchPending(frozen_publication_set, version)
          -> RemoteFetchSynchronized(completed_cpu_set, version)
          -> PublishedCode(version, publication_epoch)
             +-- retirement rejection --> PublishedCode
             +-- fully reserved -------> RetirementAccepted(
                                          CodeRetirementOperation,
                                          frozen_executor_set,
                                          owned_resources)
                    -> Retiring(retirement_epoch)
                    -> ExecutionQuiescent
                    -> ReclaimableExecutableImage

PublicationAccepted/Pending + selectable cancellation
   -> Cancelling -> Cancelled only after translation/fetch effects drain
Any accepted publication + unproved completion
   -> Incomplete(acked, missing, Quarantine<ExecutableImage>)
Any accepted publication + unsafe backend failure
   -> Quarantined(reason, Quarantine<ExecutableImage>)
PublishedCode -> never WritableOwned for the same version
```

The logical close in `Sealing` prevents further writers while the backend
performs data-cache visibility through the still-valid staging mapping. The
translation component then removes writable access to quiescent completion
before an RX mapping is created but kept unreachable. Instruction-cache
invalidation is performed over the executable aliases after they exist, then
the participating CPUs perform their fetch/pipeline synchronization. An exact
backend may combine or omit hidden steps only when its pinned alias and
coherence profile proves the same order and postcondition; no task can enter
the RX mapping early and no writable CPU alias may survive.

Before `PublicationAccepted`, component 4 validates every authority,
generation, range, alias, profile, and budget; freezes a `PublicationSet` of CPU
identities and incarnations; prepares and reserves component 3's complete
`ExecutableImageTranslationPlan`; and preallocates cache, remote-request,
completion, and teardown records. Rejection occurs before any
mapping or cache effect and returns `SealedCode` with ownership unchanged.
After acceptance, the operation exclusively owns that typestate view, the
translation plan, frame and address-space pins, lifecycle participation guards,
and all completion capacity until a terminal result transfers or quarantines
them. No later internal rejection is surfaced as `CodePublishError` or
`MappingError`.

### Publication interface

```text
code_create(frame_authorities, byte_length)
  -> Rejected(CodeCreateError, frame_authorities)
   | ExecutableImage<Allocated> + CodeWriteLease

code_seal(write_lease, initialized_range, metadata_digest)
  -> Rejected(CodeSealError, CodeWriteLease)
   | SealedCode

code_publish(sealed_code, executable_address_space,
             virtual_range, publication_set)
  -> Rejected(CodePublishError, SealedCode)
   | Accepted(CodePublicationOperation)

code_publication_poll(operation)
  -> Pending(stage, acknowledged_cpu_set)
   | Succeeded(PublishedCode)
   | Cancelled(SealedCode, PublicationDrainEpoch)
   | Incomplete(acknowledged_cpu_set, missing_cpu_set,
                Quarantine<ExecutableImage>)
   | Quarantined(reason, Quarantine<ExecutableImage>)
   | Fatal(ArchitectureFaultRecord)

code_publication_cancel(operation)
  -> CancellationRequested
   | CancellationNotSelectable(stage)
   | AlreadyTerminal(CodePublicationTerminal)

code_retire(published_code, execution_quiescence_source)
  -> Rejected(CodeRetireError, PublishedCode)
   | Accepted(CodeRetirementOperation)

code_retirement_poll(operation)
  -> Pending(stage, observed_executor_set)
   | Succeeded(ReclaimableExecutableImage)
   | Cancelled(PublishedCode, RetirementDrainEpoch)
   | Incomplete(observed_executor_set, missing_executor_set,
                Quarantine<ExecutableImage>)
   | Quarantined(reason, Quarantine<ExecutableImage>)
   | Fatal(ArchitectureFaultRecord)

code_retirement_cancel(operation)
  -> CancellationRequested
   | CancellationNotSelectable(stage)
   | AlreadyTerminal(CodeRetirementTerminal)
```

The architecture API ends at `PublishedCode`. The runtime owns its module or
entry table and may atomically install the returned version at a runtime safe
point using the ordinary-memory publication contract. Keeping
`runtime_slot` out of this component prevents a BEAM-specific dispatch policy
from becoming an architecture primitive.

`CodeCreateError`, `CodeSealError`, `CodePublishError`, and `CodeRetireError`
are rejection reasons only. `code_seal` performs all fallible validation before
its one-way logical writer close. An accepted operation never returns one of
those errors. Cancellation requests select a path but do not themselves return
resources: the matching poll reports `Cancelled` only after every started
translation, cache, remote-fetch, or retirement effect has drained to the named
epoch. If drainage cannot be proved, the exactly-once terminal result is
`Incomplete` or `Quarantined`, and its quarantine owns all unreusable state.
After `PublishedCode`, publication cancellation is too late and the caller must
use retirement; after retirement's unreachable commit point, retirement
cancellation is likewise nonselectable and drainage continues.

Retirement admission performs the same ownership discipline independently. It
freezes the executor identities/epochs named by the runtime's opaque
`execution_quiescence_source`, reserves translation and diagnostic-reference
drainage capacity, and moves `PublishedCode` plus every RX mapping and frame pin
into `CodeRetirementOperation`. Rejection returns the unchanged view before
reachability changes. A selectable cancellation can return `PublishedCode`
only before the runtime-supplied no-new-dispatch proof commits; afterward the
operation must reach reclaimable, incomplete, or quarantined terminal state.

### Why immutable versions are the baseline

Generating a new immutable body and atomically switching an entry-point or
version table avoids concurrent modification of instructions already in
flight. It supports BEAM hot loading naturally: runtime policy determines
which process may call which module generation, while architecture machinery
only guarantees native bytes are fetchable.

In-place patching has at least three different meanings:

1. **Incompatible atomic update.** No CPU may execute a mixed old/new stream.
   This requires a stronger stop or patch protocol and is excluded initially.
2. **Compatible best-effort optimization.** Either old or new behavior is
   correct. Arm's engineering guidance shows why this can use weaker
   synchronization, but the contract must say so explicitly.
3. **Security revocation.** Old instructions must become unusable. This is a
   protection and execution-quiescence transition and can never use the
   best-effort path.

Keeping these as distinct APIs prevents an optimization technique from being
mistaken for revocation.

## Cross-CPU publication protocol

The scheduler and CPU-lifecycle components define an eligible CPU set for a
runtime domain. Component 4 is the only public caller that turns it into a
publication transition:

1. `code_seal` has already closed the writer lease so no later byte store can
   begin.
2. Admission allocates a new version; freezes a `PublicationSet` containing the
   complete CPU identities, incarnations, and membership generation; prepares
   component 3's private translation plan; and reserves every operation record
   and resource pin. A rejection here has made no architectural mutation.
3. Acceptance moves `SealedCode` and all reservations into the
   `CodePublicationOperation`. A CPU trying to join the domain's eligible set
   must perform publication catch-up before admission; the frozen set itself is
   never edited.
4. The backend completes data-cache visibility for the exact range through the
   authorized staging aliases.
5. Component 4 starts the already-prepared private translation phase that
   removes every writable CPU alias and observes `TranslationQuiescent` for its
   frozen target set.
6. Component 4 starts the already-prepared private translation phase that
   installs an RX mapping which remains unreachable by runtime dispatch.
7. The backend performs required instruction-cache invalidation over the
   executable aliases and the publisher performs its local fetch/pipeline
   synchronization.
8. Every other target CPU performs its required local fetch/pipeline
   synchronization and acknowledges `(executable_image, version)` afterward.
   The scheduler may run the target domain only on a CPU whose observed
   publication generation is current.
9. After every required target acknowledges, component 4 atomically records
   `PublishedCode`; only then may the runtime install that authority view in its
   own entry table.

This deliberately parallels translation shootdown. The two can share
preallocated cross-CPU request transport and CPU-set generation machinery, but
their completion records and local instructions remain distinct.

If one CPU fails to acknowledge, that publication generation completes as
`Incomplete`; its frozen target set is never shrunk in place and its quarantine
owns the image, mappings, pins, and completion evidence. Recovery may finish a
separate CPU-offline or domain-eligibility transition and use that proof to
drain the quarantine. Only after all started translation and fetch effects are
accounted for may recovery mint a fresh `SealedCode` view and submit a new
generation with a newly frozen set. No acknowledgement or completion from the
failed generation is inherited. If drainage cannot be proved, the image stays
quarantined and pinned. At no point may the new version run on the missing CPU.

## Cross-ISA backend plans

| Semantic step | x86-64 | AArch64 | RISC-V |
| --- | --- | --- | --- |
| Ordinary kernel atomics | Map pinned language orders to TSO-aware compiler and ISA operations; do not infer SC | Map to acquire/release atomics and barriers required by the pinned Arm model | Map to RVWMO atomics/fences for the selected extensions |
| Device ordering | Typed MMIO and posted-write rules from the platform/device profile | Normal versus Device memory and required barrier scope | `FENCE` predecessor/successor I/O classes plus execution-environment rules |
| Local code publication | Follow Intel's defined self-/cross-modifying-code and serialization rules even where caches are coherent | Data clean to required point, completion barrier, instruction invalidate, completion barrier, local instruction synchronization as specified | Make data stores visible, then execute local `FENCE.I` |
| Remote code publication | Execute the required serializing/fetch action on every eligible logical CPU | Remote CPUs execute the required local instruction synchronization; the writer's `ISB` is not broadcast | Data fence at publisher and `FENCE.I` on every eligible hart, directly or through SBI RFENCE |
| Range precision | Feature/profile dependent | Cache-line and maintenance-scope dependent | Baseline `FENCE.I` may be broader than the supplied range |

Exact instruction sequences belong in versioned backend documentation and
generated-code tests. The table is a semantic map, not assembly to copy.

## Cache-maintenance planner

A shared internal planner accepts an authorized semantic request and produces
a backend-specific sequence. Its input includes:

- address and overflow-checked length;
- physical alias set where relevant;
- cacheability and shareability profile;
- participating agent set: local CPU, CPU set, device, or point of coherency;
- direction: clean, invalidate, clean-and-invalidate, or instruction
  invalidation;
- required completion point; and
- context restrictions such as hard-interrupt safety.

It rounds ranges with overflow-safe arithmetic, reads discovered line sizes,
and rejects unsupported alias configurations. Callers cannot provide a line
size or raw cache level as ambient authority.

Cache maintenance is fallible at the semantic level even if individual
instructions do not report errors. An unsupported range, absent remote
mechanism, invalid feature profile, or known platform erratum is a pre-mutation
admission rejection. An offline-CPU race or unexpected backend failure after
acceptance is instead an `Incomplete`, quarantine, or fatal terminal result; it
cannot surface as a late `CodePublishError`.

## Interaction with the capability microkernel

The [minimal privileged kernel](minimal-privileged-kernel-layer.md) supplies
frame authority, mapping generations, runtime-domain lifecycle, scheduling
contexts, and teardown ledgers. This component adds:

- release/acquire publication for immutable kernel objects;
- typed MMIO and DMA visibility used by protected-I/O bindings;
- the private `CodePublicationState`, write-lease transition, publication
  operation, and retirement operation behind the kernel-owned
  `ExecutableImage`;
- remote fetch generations incorporated into domain stop and CPU migration;
  and
- bounded architecture work charged to the initiating domain or a declared
  supervisor reserve.

Kernel capability selectors and user-level PIDs are never embedded directly
in native code as transferable authority. A generated stub may contain a
domain-local slot index whose use still crosses the capability validation
path.

## Interaction with BEAM compatibility

The kernel sees opaque native-code bytes, not BEAM as its ABI. A compatible
runtime remains responsible for:

- validating the selected BEAM/OTP compatibility profile;
- loading compiled BEAM modules;
- producing interpreted or BeamAsm-like executable form;
- maintaining stack maps, safe points, exception metadata, tracing, and hot
  code-version rules; and
- automatic process-local tracing garbage collection.

The runtime should batch generated code into immutable `ExecutableImage`
instances, seal them once, and install `PublishedCode` through an atomic runtime
table. Garbage
collecting actor heaps is unrelated to code retirement. Code retirement uses
runtime execution quiescence—safe points, scheduler epochs, or explicit frame
tracking—not reachability in one BEAM process heap.

An in-process native extension or JIT shares the runtime domain's memory and
failure boundary. W^X prevents one direct avenue of modification but does not
make generated code semantically safe. A malformed JIT, relocation, or native
call remains capable of crashing the runtime domain, after which the outer
supervisor tears it down and starts a new incarnation.

## Failure and security analysis

### Partial publication

Until the entire declared target set acknowledges, the runtime cannot install
the version. The image remains sealed and non-writable. Timeout is an
observation deadline, not cancellation: the operation publishes an exactly-once
`Incomplete` terminal record containing acknowledged CPUs, missing CPUs, and
the quarantine that owns every still-live resource. Recovery can reduce the
scheduler eligibility set only through a CPU/domain lifecycle transition that
prevents later migration to a missing CPU, then drain that quarantine through a
separate recovery operation.

### Cancellation and late completion

`code_publication_cancel` and `code_retirement_cancel` request cancellation;
they do not manufacture a terminal state. Before returning `Cancelled`, the
operation must prove that remote requests cannot publish authority, any
unreachable RX mapping has been removed to translation quiescence, cache/fetch
work is accounted for, and every frame or address-space pin has a named owner.
If any proof is missing, the terminal record is `Incomplete` or `Quarantined`.
Late acknowledgements are generation-checked and may help a recovery ledger,
but cannot change the original sticky terminal result or release its quarantine
implicitly.

### Writer death

If the writer dies in `WritableOwned`, the write lease closes, the staging
mapping is removed, and incomplete bytes are never executable. If it dies
after sealing, a supervisor with explicit adoption authority may continue
publication or destroy the image. Image generations prevent a stale writer
from resuming.

### W^X and alias attacks

W^X is checked across every CPU mapping of the frame, not only one virtual
address. DMA authority to the same frame is also denied while it is executable
unless a special trusted profile proves why device writes cannot alter code.
Changing cacheability or memory type during publication is prohibited.

### Metadata mismatch

The runtime binds its stack maps, relocation results, and module metadata to
the same `ExecutableImage` generation and optional digest before sealing. The kernel
need not interpret the metadata, but it prevents substituting bytes after the
runtime validated their companion data.

### Speculation and stale targets

Publication establishes architectural fetch visibility. It does not prove
that all microarchitectural instruction, branch-predictor, or decode state is
free of cross-domain timing channels unless the selected security profile adds
the required flush or partition steps. Indirect-branch mitigation and control-
flow integrity are separate feature-profile concerns.

### Retirement races

A code version can be unreachable from new dispatch and still present in a
thread's stack, return address, continuation, signal frame, or CPU pipeline.
Retirement therefore requires runtime execution quiescence plus any
architecture synchronization needed before frame reuse. A timeout retains the
old RX mapping or quarantines the domain; it never remaps those bytes writable.

### Ordering bugs as authority bugs

Publishing a capability-table pointer before its rights, generation, or
lifetime fields are initialized can expose authority even if the pointer value
is correct. Security review therefore treats release/acquire edges and
immutable initialization as part of the capability invariant, not merely
performance details.

## Verification strategy

### Kernel memory model

Create a versioned Atom OS kernel memory-model document and executable litmus
suite for:

- message passing with release/acquire;
- lock and unlock;
- reference acquisition versus object close;
- generation publication;
- CPU-local queue producer/consumer;
- interrupt-to-thread sticky notification;
- domain stop and scheduler eligibility; and
- code-version entry publication and retirement.

Run each test through the source-language/compiler model where available, the
chosen ISA model, and hardware stress tests. Pin model and compiler versions.
Review every use of relaxed order and every free-standing fence.

### Code-publication model

Model-check the code state machine with writer death, duplicate and delayed
CPU acknowledgements, migration, CPU offline, publication abort, entry-table
replacement, and retirement. Required invariants include:

- no execution edge reaches a pre-published version;
- no write lease exists for an executable version;
- no CPU executes version `v` without observing publication `v`;
- old versions remain mapped until execution quiescence; and
- a stale operation cannot publish or reclaim a later image generation.

### Backend conformance

- Inspect emitted atomics and barriers for all supported compiler/optimization
  combinations.
- Use Arm instruction-fetch tests and model oracles where applicable.
- Test RISC-V local and remote `FENCE.I` with migration deliberately forced
  between generation and execution.
- Exercise Intel-defined cross-modifying-code sequences rather than assuming
  coherent caches make testing unnecessary.
- Test cache-line boundaries, empty and overflowed ranges, aliases, huge
  objects, offline CPUs, and feature/erratum fallbacks.
- Run on real hardware after emulation; cache and pipeline behavior are exactly
  where emulators may be too strong or too simple.

### MMIO and DMA tests

Use a model device and, later, real devices to delay posted writes, reorder
descriptor observation, and vary coherency. Confirm that queue ownership
transfer plus the typed ordering operation—not an accidental full fence—sets
the visibility point. Fault injection must include reset and DMA completion
racing with code/frame reuse.

### Performance measurements

Measure:

- atomic and lock latency uncontended and contended across sockets;
- CPU-local queue throughput and tail latency;
- each MMIO accessor class and posted-write completion;
- cache-maintenance cost by size, alignment, and sharing scope;
- code sealing and publication for small stubs through large BEAM modules;
- target CPU counts, cross-socket publication, and one failed target;
- entry-table swap and retirement delay; and
- a representative BEAM workload performing load-time native lowering, hot
  code replacement, messaging, and process-local tracing GC.

The performance report must separate generation cost, translation changes,
cache maintenance, remote synchronization, and runtime quiescence. Otherwise a
slow loader can be misdiagnosed as an ISA fence problem.

## Staged implementation

### Stage 1: ordinary-memory contract

- Choose and pin the implementation language and compiler memory model.
- Support one word-sized atomic family, one IRQ-safe spin primitive, and one
  blocking kernel lock with explicit context rules.
- Publish litmus tests and generated-code checks on the first ISA.

### Stage 2: typed MMIO and cache primitives

- Implement access-width, endianness, memory-type, and posted-write profiles.
- Add overflow-safe local data and instruction cache-maintenance planning.
- Keep DMA ownership and device protocols outside this component.

### Stage 3: single-CPU immutable code

- Add `ExecutableImage`, write lease, W^X transition, local publication,
  executable mapping, atomic entry install, and quiescent retirement.
- Integrate a minimal native test loader before a BEAM JIT.

### Stage 4: multicore publication and second ISA

- Add eligible-CPU generations, preallocated remote requests, migration
  catch-up, split-phase operations, and CPU-offline composition.
- Port the same semantic interface to a weaker or materially different memory
  and instruction-fetch model.

### Stage 5: managed-runtime integration and optimization

- Publish immutable native `ExecutableImage` instances for compiled BEAM
  modules and test hot replacement and retirement at runtime safe points.
- Measure batching and only then consider compatible in-place patches,
  narrower cache operations, or platform-specific accelerations.

## Alternatives and tradeoffs

### One universal full fence

A maximally strong fence can hide early mistakes but cannot necessarily order
device signaling, remote instruction pipelines, TLBs, or DMA. It also imposes
unrelated costs. Strong fallbacks are useful inside backend plans; the public
API remains semantic and narrow.

### Architecture mnemonics in portable code

Mnemonic wrappers appear transparent but spread architecture scope and errata
knowledge throughout the kernel. They also invite x86-tested code to omit
portable ordering. The recommended backend contains them behind effect-shaped
operations.

### Persistent dual RW/RX mappings

Dual aliases avoid repeated remapping and can make JITs fast. They weaken W^X,
complicate cache aliases, and let a compromised runtime modify executable
frames. The baseline removes all writable aliases before execution. A future
trusted JIT profile may use isolated writer and executor domains with an
explicit transfer protocol, not a hidden alias.

### Stop-the-world publication

Stopping every runtime thread and synchronizing every CPU is simple and can be
appropriate initially. Its pause grows with CPU count and conflicts with the
responsiveness goal. Immutable versions plus eligibility generations let work
continue on the old version until the new one is fully published.

### Runtime-only synchronization

Allowing each runtime to execute cache instructions can reduce system calls but
cannot safely coordinate privileged mappings, migration, CPU offline, or
feature variation. The runtime can batch and choose publication points; the
kernel executes the architecture transition.

### In-place compatible patching

Best-effort patching can avoid remote stops when both instruction streams are
valid, as the Arm engineering article explains. It is a useful later
optimization for counters or hints. It must be a separate API that cannot
grant execute permission, revoke old behavior, or release the patched frame.

### Sequential consistency everywhere

SC atomics simplify some reasoning but do not solve MMIO, DMA, TLB, or code
fetch and may impose unnecessary global order. Acquire/release plus modeled
protocols is the baseline; use SC where the algorithm truly needs one total
order.

## Unresolved questions

- Which implementation language and compiler versions define the first kernel
  memory model, and what unsupported atomic widths must be rejected?
- Can one executable model cover ordinary thread and interrupt communication
  without adopting Linux-specific primitives?
- What is the smallest portable MMIO accessor set that still represents
  posted writes and architecture/device scopes honestly?
- What compact encoding keeps the aggregate's references to existing frames,
  mappings, and private `CodePublicationState` independently auditable without
  inflating its hot-path footprint?
- Which runtime safe-point evidence is sufficient to retire BeamAsm code that
  may appear in stacks, continuations, exception state, or native helpers?
- Which policy should choose between offlining a missing CPU, excluding the
  runtime domain through a completed eligibility transition, and aborting a
  failed publication before resubmission?
- Which Arm cache-maintenance scope and RISC-V execution-environment profiles
  are available on the first hardware targets?
- What code batching size minimizes publication overhead without creating
  unacceptable module-load or hot-upgrade latency?
- Which speculative-execution mitigations belong in the mandatory publication
  profile, and which remain target-specific security options?

## Connections

- [Kernel hardware and architecture support
  layer](kernel-hardware-and-architecture-support-layer.md) defines this as
  component 4 and separates it from translation, DMA, and interrupt flow.
- [Address translation and protection
  transitions](address-translation-and-protection-transitions.md) supplies only
  the private prepared W^X mapping effects and TLB completion that this sole
  public publication orchestrator composes.
- [Interrupt event fabric](interrupt-event-fabric.md) consumes IRQ-safe
  atomics and release/acquire publication but has its own controller flow and
  acknowledgement semantics.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md)
  supplies capability authority, domain lifecycle, scheduling eligibility,
  teardown, and code-frame accounting.
- [BEAM, ERTS, and OTP principles for a new operating
  system](beam-erts-and-otp-principles-for-a-new-operating-system.md) keeps
  compiled-BEAM policy, hot-code semantics, and tracing GC in the managed
  runtime.
- [Kernel hardware-contract
  inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  remains the workbench for testing the contract on two ISAs.

## Sources

- [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md)
- [Simplifying Arm concurrency](../30-sources/pulte-et-al-2018-simplifying-arm-concurrency.md)
- [Concurrency in the Linux kernel](../30-sources/alglave-et-al-2018-linux-kernel-concurrency.md)
- [Arm instruction-fetch semantics](../30-sources/simner-et-al-2020-arm-instruction-fetch.md)
- [Arm A-profile system architecture documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [Intel system programming documentation](../30-sources/intel-2026-system-programming-documentation.md)
- [RISC-V unprivileged architecture](../30-sources/risc-v-international-2026-unprivileged-architecture.md)
- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md)
- [RISC-V supervisor binary interface](../30-sources/risc-v-international-2025-supervisor-binary-interface.md)
- [Arm self-modifying code with threads](../30-sources/bramley-2025-arm-self-modifying-code-threads.md)
- [Linux kernel low-level core APIs](../30-sources/linux-kernel-community-2026-low-level-core-apis.md)
- [The Road to the JIT](../30-sources/gustavsson-2020-road-to-the-jit.md)
