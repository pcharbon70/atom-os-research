---
title: "Hardware and architecture support for the Zig kernel"
kind: note
created: "2026-08-29"
maturity: developing
tags:
  - aarch64
  - capabilities
  - dma
  - hardware-architecture
  - interrupts
  - iommu
  - kernel-development
  - memory-protection
  - multicore
  - operating-systems
  - risc-v
  - zig
aliases:
  - "Hardware support layer"
  - "Kernel architecture layer"
---

# Hardware and architecture support for the Zig kernel

The hardware and architecture support layer should be a set of small,
composable mechanism components, not one universal HAL. Its job is to turn
firmware descriptions, privileged CPU state, interrupt controllers, timers,
translation hardware, caches, DMA engines, and reset/error mechanisms into a
validated resource and event model that the minimal kernel can safely expose.

The current recommended target sequence is:

1. **Bootstrap on RV64 QEMU `virt`** in supervisor mode above pinned OpenSBI,
   using Devicetree, Sv39, the SBI timer and hart services, PLIC, a UART, and
   simple virtio. This profile minimizes the first proof-of-life surface.
2. **Enable an RV64 protection profile** on the same virtual platform with AIA
   (APLIC plus IMSIC), message-signaled interrupts, and the RISC-V IOMMU. This
   forces the design to implement device assignment and revocation rather than
   treating DMA as trusted.
3. **Port the same contracts to AArch64 QEMU `virt`**, using GICv3, the generic
   timer, PSCI, and SMMUv3. The point is to expose hidden assumptions about
   privilege, cache maintenance, weak ordering, firmware, and interrupt
   topology.
4. **Select physical hardware only after those contracts pass.** The board must
   have public documentation, a reproducible boot chain, usable debug and
   recovery, stable timers, an IOMMU or an explicitly weaker DMA threat model,
   and no essential opaque firmware dependency that the project cannot test.

This is an architectural recommendation, not evidence that a kernel already
boots. The first physical board, exact RV64 extension profile, page layout,
and firmware artifacts remain open in the [reference hardware-contract
inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md).
Zig is already the fixed implementation language under the [language
decision](zig-as-the-kernel-implementation-language.md); language comparison is
out of scope here.

## Question, scope, and evidence standard

The research question is:

> What must the lowest software layer own so that higher kernel, actor-runtime,
> and OTP-like service layers can use hardware through stable, capability-
> checked, bounded, recoverable contracts without inheriting raw firmware or
> ISA details?

The operational standard is stronger than “boots in an emulator.” A proposed
component is credible only when its state transitions, privilege boundary,
ordering requirements, resource bounds, failure behavior, firmware and host
dependencies, and target assumptions are explicit. A target profile is
credible only when the same tests pass under emulation and on at least one
documented physical implementation.

This note distinguishes four kinds of statement:

- **Architectural fact:** required or permitted by a cited specification.
- **Reported result:** measured, demonstrated, or verified by a cited paper.
- **Synthesis:** an interpretation across sources.
- **Proposal:** the contract this project should test; it remains unverified.

No local boot, interrupt-latency, TLB-shootdown, DMA-fault, suspend, or hardware
experiment was performed during this research pass. All proposed interfaces and
target choices must therefore remain developing.

## Boundary of the layer

### What this layer owns

The hardware and architecture support layer owns mechanisms whose correct use
requires privilege, exact architecture knowledge, or operation before ordinary
services exist:

- reset entry, boot handoff, firmware exit, and early recovery;
- trap entry/exit, privilege transition, register context, atomics, barriers,
  cache/TLB operations, and CPU feature discovery;
- validated platform description and normalized topology/resource identities;
- CPU address translation, physical protection, memory attributes, and
  translation invalidation;
- interrupt-controller programming, source masking and completion, MSI routing,
  IPIs, and conversion of hardware interrupts into bounded kernel events;
- monotonically advancing counters, per-CPU event timers, calibration, and
  suspend/resume continuity;
- secondary-CPU bring-up, per-CPU state, topology, online/offline protocols,
  and architecture memory-ordering primitives;
- data/instruction cache maintenance and safe publication of native code;
- FPU, SIMD, vector, debug, and other extended architectural context;
- DMA addressability, cache synchronization, IOMMU domains, fault queues,
  device assignment, and revocation mechanisms;
- privileged MMIO/PIO delegation, reset domains, clocks needed for device
  access, and the minimum bus enumeration needed to construct resources;
- CPU/device idle and reset mechanisms, watchdog programming, and the atomic
  machine-side steps of suspend and resume;
- boot measurements, entropy-source admission, debug lockdown, RAS event
  capture, reset reasons, and a minimal crash/recovery sink.

### What it must not absorb

The layer should not decide application or service policy merely because the
policy ultimately affects hardware:

- actor scheduling, supervision trees, restart intensity, and application
  dependencies belong above the minimal kernel;
- filesystem, network, storage, display, and device-class semantics belong in
  isolated driver or service domains;
- wall-clock synchronization, timezone, timer coalescing policy, thermal
  strategy, and performance governors are services;
- firmware update selection, system release orchestration, state migration,
  and rollback policy are OTP-like lifecycle services, although they consume
  lower verified-boot and durable-generation primitives;
- arbitrary ACPI policy or vendor firmware behavior must not silently become
  the kernel's mechanism API;
- BEAM instructions, actor mailboxes, managed heaps, and garbage collection do
  not belong in this layer.

The separation is mechanism versus authority and policy, not “hardware versus
software.” An IOMMU driver is low-level software, but deciding which network
service receives a virtual NIC is policy. A timer comparator is hardware, but
choosing a service's retry deadline is policy.

## Trust, privilege, and failure boundaries

The proposed boundary is:

| Element | Normal privilege | Trusted for | Not trusted for |
| --- | --- | --- | --- |
| Boot ROM and platform firmware | Above or prior to kernel | Initial hardware state and declared handoff contract | Correct policy, complete recovery, or bug-free runtime behavior |
| Boot adapter | Firmware application or highest kernel entry | Authenticate/load the image, snapshot inputs, construct `BootInfo`, leave firmware services | General allocation, drivers, or permanent platform APIs |
| ISA and controller mechanisms | Privileged kernel | Enforcing CPU, IRQ, timer, and translation state | Application policy or parsing complex untrusted protocols |
| Hardware resource manager | Privileged kernel | Typed ownership, capabilities, generations, and atomic cross-component transitions | Device-class logic or high-volume data paths |
| Device driver | Isolated native domain by default | One declared device protocol and buffers | Kernel memory, unrelated MMIO, arbitrary DMA, global IRQ routing |
| Managed actor runtime | Isolated runtime domain | Actor execution, heaps, mailboxes, safe points, runtime scheduling | Raw page tables, interrupt controllers, IOMMU, or unrestricted native state |
| OTP-like services | Ordinary domains | Supervision, naming, update, power, and driver policy | Bypassing kernel ownership or resource limits |

Firmware and hardware remain part of the system's trusted computing base in
the physical sense even when the kernel distrusts their data. Validation can
prevent a malformed table from corrupting memory; it cannot make a malicious
memory controller honor isolation. Every assurance claim must name that lower
assumption.

## Design principles

### Normalize once, then forget the source format

UEFI, ACPI, Devicetree, SBI, PSCI, and compiled board descriptions are inputs,
not long-lived kernel object models. Each adapter should parse into the same
typed graph, retain the raw bytes for diagnosis, and prevent later subsystems
from depending on offsets, phandles, AML names, or firmware pointers.

### Make authority a first-class typed value

A numeric IRQ, physical address, CPU index, IOVA, or MMIO pointer is not
authority. Higher layers receive unforgeable handles carrying object type,
rights, lifetime, owner, and generation. Conversion to a raw register value
occurs only inside the responsible component.

### Model transitions, not just configurations

Most dangerous bugs occur between valid steady states: a page is reused before
remote TLB invalidation completes; a DMA buffer is freed while a device still
owns a descriptor; an IRQ is rerouted while level state remains asserted; a
CPU sleeps while it owns timer work; a new code page becomes executable before
all instruction caches observe it. APIs must represent prepare, publish,
quiesce, acknowledge, revoke, and failure states.

### Prefer deny-by-default reset states

Secondary CPUs remain parked, device DMA remains blocked, interrupts remain
masked, writable pages remain non-executable, debug access remains disabled in
production profiles, and mutable images remain unselected until validation and
ownership complete.

### Keep trap context finite and allocation-free

A hard trap path should capture architectural state, acknowledge or mask the
minimum hardware source, timestamp if safe, enqueue a bounded event, and leave.
It must not allocate, parse firmware, block on a service, run arbitrary driver
logic, acquire an unbounded lock, or execute managed actor code.

### Design against the weakest selected memory model

Successful x86 tests do not establish correct Arm or RISC-V behavior. Queue,
page-table, IRQ, DMA, and cross-core protocols state their acquire, release,
completion, I/O-ordering, and instruction-synchronization obligations at the
architecture-neutral boundary. Each port proves or tests the mapping.

### Preserve evidence across the failing boundary

A driver cannot be solely responsible for its own crash report, and a kernel
cannot store its only fatal record through a complex service it just killed.
Reset reason, raw trap frame, CPU identity, monotonic timestamp, component
generation, bounded recent events, and image identity need a sink outside the
failed domain.

### Make the simple implementation a valid subset

The single-core, polled, no-IOMMU bootstrap path must implement the same
ownership and completion contracts as the SMP, MSI, IOMMU path, with explicitly
weaker protection. It should not establish incompatible APIs that later need
to be bypassed.

## Component and dependency model

The internal structure should look like this:

```text
reset / firmware / boot image
              |
         boot adapter
              v
        validated BootInfo
              |
     description front ends
       (DT / ACPI / static)
              v
  immutable topology + resource graph
       /      |       |       \
      v       v       v        v
  CPU/ISA  memory   IRQ/time  device/bus
      |       |       |        |
      +--- cache/TLB -+        |
      |       |                |
      |    DMA/IOMMU <----------+
      |       |
      +--- power/reset/watchdog
              |
       security / RAS / crash
              v
  typed capabilities, events, and leases
              |
        minimal kernel services
              |
 managed runtimes, drivers, OTP-like policy
```

The graph is deliberately not a strict stack. Memory management is needed to
allocate interrupt tables and IOMMU queues; interrupts are needed for IOMMU
faults; CPU hotplug affects timers, IRQ affinity, TLB invalidation, and vector
state; power transitions require all of them to quiesce. The correct unit of
composition is therefore a transaction across small components, not a call
down a single HAL hierarchy.

| Component | Subcomponents | Primary outputs | Hard dependencies |
| --- | --- | --- | --- |
| Boot envelope | image verifier, firmware adapter, early allocator, recovery console | immutable `BootInfo`, image and measurement identity | reset ABI, linker layout, firmware contract |
| ISA core | trap stubs, context codec, atomics/barriers, cache/TLB ops, feature and erratum admission | exact privileged primitives and safe CPU profiles | CPU architecture, implementation revision, firmware/microcode identity |
| Description | DT/ACPI/static parsers, validator, normalizer | topology/resource graph | boot memory map, binding/table rules |
| Protection | frame metadata, page/region tables, ASID generations, shootdown | address spaces and mapping leases | ISA translation, CPU set, memory attributes |
| Interrupt | controller backends, source registry, router, event bridge | IRQ capabilities and bounded events | topology, CPU IDs, memory, MSI/IOMMU when used |
| Time | clocksource, event timer, calibration, deadline queues | monotonic timestamps and wake events | CPU counters, IRQs, power transitions |
| CPU topology | bring-up, per-CPU storage, IPI, online/offline, NUMA | online CPU set and topology generations | firmware, protection, IRQ, time |
| Cache/publication | data/instruction maintenance, executable-page state | code-publication and DMA-sync tokens | ISA, CPU set, protection |
| Extended state | FPU/SIMD/vector/debug state codecs | domain context ownership | ISA features, scheduler boundary |
| DMA/IOMMU | domains, IOVA allocator, buffer leases, sync, fault handler | DMA-safe buffer and device leases | protection, cache, IRQ, topology |
| Device boundary | bus enumeration, register access, hot-plug, MMIO/PIO grants, reset/clock bindings | isolated device-resource bundles | description, IRQ, DMA, power |
| Power and reset | idle, CPU/device/system states, watchdog, reset reason | bounded transition results | every component that can remain active |
| Security/RAS | boot evidence, entropy admission, debug policy, fatal records | attestation inputs and durable crash evidence | firmware roots, timers, reset, minimal storage |

## 1. Reset, boot, and firmware envelope

### Responsibilities

The boot envelope has one job: establish a state the kernel can own and
describe it without ambiguity. It should:

1. validate the executing image and its immutable layout;
2. identify the architecture, entry privilege, boot CPU, endianness, and
   enabled features needed before probing is safe;
3. snapshot the usable, reserved, firmware-runtime, device, persistent, and
   image memory ranges;
4. locate and copy or pin hardware-description roots;
5. record command line, initial payloads, entropy seed with provenance, boot
   measurements, image generation, and reset reason;
6. establish a bounded early console and fatal-reset path;
7. stop or account for firmware-owned asynchronous activity and DMA;
8. leave boot services exactly once; and
9. enter the same internal kernel ABI regardless of UEFI, SBI, a board ROM, or
   a test harness.

A conceptual `BootInfo` needs version and total length, not just fields, so an
older kernel can reject an incompatible loader. Every referenced byte range
needs physical address, length, type, permissions, lifetime, and ownership.
Pointers valid only in firmware virtual mappings must not survive the handoff.

### Boot architecture choices

| Choice | Advantages | Costs and risks | Position |
| --- | --- | --- | --- |
| Kernel owns reset and highest privilege from the first instruction | Maximum control; minimal permanent firmware; good for small boards and later assurance | Board-specific DRAM, clocks, security, and core bring-up; larger initial scope; easy to conflate firmware and kernel | Not first target; useful for a later MCU or audited appliance profile |
| Thin UEFI loader | Cross-ISA image loading, memory map, files and console before exit; works with standardized hardware | PE/COFF and firmware ABI; `ExitBootServices` race; optional runtime-services trust; firmware variance | Supported boot adapter, especially AArch64/x86 and future RISC-V servers |
| OpenSBI plus Devicetree, kernel in RISC-V S-mode | Keeps M-mode board mechanisms out of first kernel; open specifications; simple QEMU path | Firmware remains trusted; SBI extension variation; real RISC-V board fragmentation | Preferred first RV64 path |
| Arm EL1 above trusted firmware/PSCI | Standard CPU power interface and common AArch64 deployment model | EL3/secure firmware remains beneath the kernel; board may require UEFI/ACPI or vendor DT | Preferred AArch64 validation path |
| Compiled static board table | Small code and deterministic data for one board | No portability or runtime verification; board revision becomes kernel build; hides missing discovery model | Only as an explicit test/MCU adapter, never the common API |

The loader should copy only the firmware data it needs, use firmware services
only before handoff, and disable UEFI runtime services by default. A later
profile may retain a narrow reset or variable service, but every call then
needs a dedicated mapping, serialization, timeout, error policy, and inclusion
in the TCB inventory.

### Verified, measured, and recoverable boot

These terms must remain separate:

- **Verified boot** refuses an image that does not satisfy signature and
  version policy.
- **Measured boot** records what was selected into a tamper-resistant or
  externally verifiable chain; it need not refuse it.
- **Recoverable boot** can select a known-good image or immutable recovery path
  after corruption, interrupted update, repeated boot failure, or policy error.

Following [NIST firmware-resilience guidance](../30-sources/regenscheid-2018-platform-firmware-resiliency.md),
protection, detection, and recovery are three mechanisms. An OTP supervisor
cannot repair firmware that prevents the first actor from starting. The boot
envelope should therefore expose image generation, attempt counter, success
commit, rollback floor, measurement log location, and recovery reason to a
later lifecycle service without delegating the enforcement primitive to it.

## 2. ISA, privilege, traps, and architectural context

### The narrow ISA mechanism layer

The ISA layer should contain only operations whose semantics cannot be stated
portably:

- enable, disable, and query interrupt state;
- enter and leave user/protected domains;
- read and write trap cause, fault address, status, and return state;
- perform system calls and architecture-defined fast paths;
- issue atomic operations and acquire/release/full/I/O barriers;
- create and activate a translation root;
- invalidate local address or instruction translations;
- clean and invalidate data or instruction cache ranges;
- send or receive the architecture's low-level IPI mechanism;
- read stable counters and CPU/extension identifiers;
- enter an idle state; and
- save, restore, initialize, and scrub architectural context.

Everything should have a Zig wrapper with typed operands and documented
preconditions. Assembly is limited to reset, trap entry/exit, context restore,
and instructions Zig cannot express correctly. The wrapper tests must inspect
generated code and exercise ABI preservation; `volatile` alone is not a memory
barrier, and a compiler barrier alone is not a device-ordering operation.

### Privilege placement choices

| Placement | Benefit | Cost | Recommendation |
| --- | --- | --- | --- |
| Kernel at highest privilege (RISC-V M, Arm EL3) | Direct ownership of every mechanism | Pulls firmware, secure monitor, vendor initialization, and a much larger threat surface into the kernel | Avoid in first application-class profile |
| Kernel in OS supervisor privilege (RISC-V S, Arm EL1, x86 ring 0) | Conventional page/user protection; firmware handles only declared lower services | Trusts firmware/monitor contract; some work needs calls across privilege | Default |
| Kernel as hypervisor (RISC-V HS, Arm EL2, VMX root) | Stage-2 isolation, guest support, potentially stronger driver/runtime domains | Larger context, interrupt virtualization, nested translation, and proof surface | Later profile only when a concrete isolation or compatibility experiment needs it |
| Managed runtime at kernel privilege | Lowest call overhead between actors and hardware | One runtime/native fault becomes machine-wide; GC and loaders join privileged TCB | Reject as default |

### Trap decomposition

Trap entry should create a small architecture-neutral envelope while retaining
the complete raw frame for diagnosis:

1. switch to a known per-CPU emergency stack without touching untrusted memory;
2. save the minimum clobbered integer and status state;
3. classify synchronous fault, syscall, maskable IRQ, IPI, debug, or fatal
   asynchronous error;
4. capture fault address, instruction address, origin privilege, CPU,
   architecture cause, and nesting depth;
5. dispatch to a finite handler; and
6. restore only state authorized for the destination domain.

The portable classification must never erase architecture detail. A generic
`PageFault` can carry read/write/execute, present/protection, user/kernel, stage,
and access size, while the raw syndrome remains attached for crash analysis.

Nested maskable interrupts should be disabled initially. They may later be
enabled only with per-priority stacks, bounded nesting, lock rules, and proof
that completion cannot be reordered. Fatal/NMI-style paths use reserved stacks
and memory and never call ordinary allocation, logging, or driver code.

### Context is a family, not one struct

Keep separate representations for:

- integer scheduling context;
- trap/error frame;
- FPU/SIMD/vector state;
- debug and performance-monitor state;
- virtualization state; and
- architecture-private firmware state that the kernel does not own.

This permits the common scheduler path to remain small and makes optional
state ownership explicit. Every extension enabled for untrusted domains needs
initialization, save, restore, sanitization, crash-capture, migration, and
feature-compatibility rules.

### Feature admission, errata, and microcode

“The CPU supports an instruction” and “the kernel may safely enable the
facility” are different statements. Feature admission should combine:

- architectural discovery registers or Devicetree/ACPI declarations;
- implementation, revision, and firmware or microcode identity;
- whether every CPU in the intended migration set implements the feature;
- required context, exception, cache, ordering, and power-state handling;
- known errata and enabled workarounds;
- toolchain-generated-code assumptions; and
- the signed hardware profile the image was tested against.

The result is an immutable `CpuFeatureProfile` per CPU plus a computed common
profile per scheduling domain. A feature remains disabled until its probe is
safe, its dependent state is allocated, its trap and restore paths exist, and
negative tests show that a domain lacking the grant receives a contained
fault. Higher layers request a semantic facility—such as scalar floating
point, fixed SIMD, scalable vectors, or a stable user counter—not a raw feature
bit.

Errata should be data-driven entries keyed by architecture, implementer,
part/revision, firmware revision, and affected configuration. An entry records
the workaround, phase at which it must run, incompatible features, whether it
must execute on every CPU, and whether failure requires disabling a CPU or the
whole profile. Workarounds remain architecture code; policy can reject a
machine whose safe configuration no longer meets the profile.

Firmware or microcode update is similarly a lifecycle, not an opaque boot
side effect:

1. record the initial revision before enabling optional features;
2. authenticate and apply an update through the platform-defined mechanism;
3. serialize CPUs and re-probe affected features;
4. reapply or retire erratum workarounds;
5. record the resulting revision in boot and crash evidence; and
6. refuse hot addition of a CPU whose safe profile is incompatible with live
   domains.

The first RV64 QEMU profile will not validate silicon errata or a physical
microcode path. Its fake backend should still test feature-profile changes and
rejection, so physical support does not later bypass the domain compatibility
contract. QEMU CPU models and `-cpu max` are test inputs, not proof that a
given board implements the same safe feature set.

## 3. Hardware description, discovery, and the resource graph

### Parsing pipeline

Discovery should be four components:

1. **Acquisition:** copy or retain an immutable raw ACPI/DT/static blob with
   source, address, length, checksum, and boot generation.
2. **Structural validation:** bounds-check every header, array, string, offset,
   cell count, checksum, revision, and reference before semantic use.
3. **Semantic normalization:** resolve address ranges, interrupt parents,
   proximity domains, IOMMU paths, clocks, reset lines, and dependencies into
   typed records.
4. **Admission:** reject overlaps, ambiguous ownership, unsupported interrupt
   chains, unprotected DMA paths, cyclic dependencies, and resources outside
   the boot memory map before publishing them.

Parsing firmware data in Zig reduces some memory hazards but does not validate
meaning. Integer overflow, aliasing ranges, duplicate identifiers, invalid
endianness, resource cycles, and inconsistent tables are semantic problems.

### Normalized graph

The graph should include at least these node kinds:

- CPU/hart and execution context;
- NUMA/proximity and cache-coherence domain;
- memory extent and persistent-memory extent;
- address space and translation unit;
- interrupt source, controller, and destination domain;
- counter, event timer, RTC, and watchdog;
- bus, bridge, and device function;
- MMIO/PIO window;
- DMA requester and IOMMU group;
- clock, reset, power, and thermal domain;
- entropy, TPM/root-of-trust, debug, and RAS source; and
- firmware service dependency.

Edges express `contains`, `translates-through`, `interrupts-through`,
`coherent-with`, `near`, `powered-by`, `clocked-by`, `reset-by`, and
`owned-by`. Each node has a stable internal ID plus a generation. Firmware
names remain diagnostic aliases, not capability identifiers.

### Discovery alternatives

| Input | Strengths | Weaknesses | Use |
| --- | --- | --- | --- |
| Devicetree | Compact, declarative, common on SoCs, easy to pass at boot, no AML interpreter | Binding-specific semantics, firmware errors, weak hot-plug story, address/interrupt graph still subtle | First RV64 profile and many Arm boards |
| ACPI | Standard server/PC topology, power, NUMA, I/O, timer, and RAS descriptions; supports dynamic methods | Large table surface plus AML execution, firmware quirks, parser/interpreter TCB | Later server profile; table subset before full AML |
| Bus self-enumeration (PCIe, USB) | Discovers functions dynamically and supports hot-plug | Does not discover CPUs, RAM, root controllers, power/reset topology, or trustworthy isolation by itself | Child of a described host bridge |
| Static board description | Tiny and deterministic for fixed silicon | Build-time coupling, no revision discovery, easy to hide undocumented assumptions | Constrained profile or test fixture only |
| Active probing | Useful for selected legacy or optional devices | Can hang, corrupt state, trigger DMA, or conflict with firmware | Only under a controller-specific safe protocol |

The common graph must express uncertainty: `present`, `disabled`, `reserved`,
`unverified`, `hot-removed`, and `failed` differ. Drivers bind only to admitted
resources, not every node firmware mentions.

## 4. Memory, protection, and address translation

### Responsibility split

The hardware support component implements translation and protection
mechanisms. The minimal kernel decides domain ownership and physical-memory
allocation. A useful split is:

- **physical inventory:** normalized usable/reserved/device/persistent ranges,
  NUMA node, cacheability, DMA reach, encryption domain, and page color if
  relevant;
- **frame ledger:** owner, rights, pin count, DMA leases, executable state,
  zeroing state, and generation;
- **translation engine:** page/region table formats, attributes, ASIDs/PCIDs,
  activation, and faults;
- **shootdown engine:** target CPU set, generation, invalidate command,
  acknowledgement, timeout, and deferred reuse;
- **mapping policy:** kernel/user split, guard pages, W^X, shared memory,
  copy-on-write, large pages, and quotas; and
- **constrained protection backend:** MPU/PMP region packing and admission for
  targets without virtual memory.

### MMU, MPU/PMP, and capability hardware

| Mechanism | Advantages | Costs and limits | Architectural treatment |
| --- | --- | --- | --- |
| Multi-level MMU page tables | Sparse virtual spaces, guard pages, W^X, per-domain mappings, sharing, COW, ASIDs, stage-2 options | Page-table memory, TLB misses, shootdowns, aliasing and concurrent-update complexity | Primary application-class profile |
| MPU or RISC-V PMP | Small, deterministic, no page-walk machinery, good for fixed embedded regions | Finite regions, alignment/granularity constraints, no virtual addressing, expensive repacking, often weak sharing | Separate constrained profile with explicit maxima |
| Stage-2 translation | Stronger guest/domain isolation and independent physical remap | Hypervisor privilege, nested faults/TLBs, more context and interrupt virtualization | Optional later mechanism, not baseline |
| CHERI capabilities | Fine-grained bounds, permissions, provenance, sealing, compartmentalization within address spaces | New hardware/toolchain/ABI, larger pointers/state, revocation and temporal safety still need policy | Future hardening profile; software capabilities must not depend on it |
| Software fault isolation | Can compartmentalize without hardware domains and tune granularity | Compiler/verifier TCB, instrumentation overhead, DMA and privileged instructions still external | Possible runtime optimization, not hardware root of trust |

The portable model should express authority and isolation strength, not pretend
an MPU is a slow MMU. A constrained target can implement `RegionDomain` with a
declared maximum region count; it should reject an impossible mapping rather
than silently merge permissions.

### Baseline virtual-memory choices

For the first 64-bit profiles:

- use the architecture's 4 KiB base page initially;
- use Sv39 on RV64 and a 4 KiB granule on AArch64;
- require non-executable data and non-writable executable pages;
- place unmapped guard pages around kernel, per-CPU, interrupt, and domain
  stacks;
- map MMIO only with device-appropriate attributes and never through an
  ordinary cached alias;
- keep large pages as a later optimization after split/merge and shootdown are
  tested;
- allocate ASID/PCID-like identifiers with generations so reuse cannot alias a
  stale translation; and
- defer physical-frame reuse until every CPU and IOMMU that could retain a
  translation acknowledges invalidation.

Whether to maintain a permanent physical direct map is open. It simplifies
frame initialization, crash inspection, and some DMA paths, but expands the
kernel's reachable address space and creates alias/attribute hazards. The
experiment should compare a constrained direct map of admitted RAM against
temporary mapping windows; no mapping may cover MMIO or firmware-reserved
memory just because it is numerically within a broad range.

### Mapping transaction

A cross-core mapping replacement should be one explicit state machine:

```text
Reserved -> Constructed -> Published -> Active
    |            |             |          |
    +---------> Aborted         |          v
                           Invalidating -> Quiescent -> Reusable
                                      \-> Failed/Quarantined
```

The implementation must specify:

1. who owns the page-table memory;
2. how descriptor writes become visible to hardware walkers;
3. whether break-before-make is required;
4. which local barrier precedes invalidation;
5. which CPUs can have cached the old translation;
6. how remote invalidation is requested and acknowledged;
7. how concurrent faults observe the transition;
8. when instruction fetch and data access are synchronized;
9. which IOMMU or device caches also require invalidation; and
10. when the old frame may be zeroed and reallocated.

The [relaxed virtual-memory research](../30-sources/simner-et-al-2022-relaxed-virtual-memory.md)
shows why this cannot be reduced to `pte = value; flush_tlb()` intuition.

### Managed-runtime interaction

Actor heaps and garbage collection use ordinary runtime mappings; they do not
receive page-table authority. The kernel can expose page commitments, guard
faults, shared immutable regions, and revocable bulk-transfer mappings. The
runtime then enforces actor-local heap semantics inside its protected domain.

Generated native code or loaded native stubs use a separate publication API:
write through non-executable mappings, validate, make immutable, synchronize
caches and instruction fetch, then publish an executable entry capability. No
mapping is simultaneously writable and executable.

## 5. Interrupt and exception delivery

### Internal subcomponents

The interrupt component should separate:

- **source configuration:** edge/level, polarity, priority, mask, wake ability;
- **controller backend:** PLIC, APLIC/IMSIC, GIC, APIC, or NVIC register
  semantics;
- **route:** destination CPU/domain, vector/identity, affinity generation;
- **hard handler:** claim/acknowledge, mask, timestamp, bounded event enqueue;
- **device completion adapter:** device-specific status read/clear ordering;
- **endpoint bridge:** converts a claimed interrupt into an authorized kernel
  notification; and
- **accounting:** rate, service time, drops/coalescing, storms, spurious count,
  and last owner generation.

An `IrqSource` capability permits binding and masking a source; an
`IrqDelivery` capability permits receiving its event. Neither should imply
MMIO, DMA, CPU-affinity, or reset authority.

### Handler architecture choices

| Model | Advantages | Risks | Position |
| --- | --- | --- | --- |
| Entire driver runs in hard interrupt context | Minimal dispatch latency | Unbounded privileged execution, allocation/lock hazards, poor recovery, priority inversion | Reject except tiny architecture-owned handlers |
| Split top half and kernel thread | Familiar, easy to defer work, can prioritize threads | Kernel driver code remains trusted; thread and queue overhead | Useful for boot-critical mechanisms and fallback |
| Interrupt delivered to isolated driver endpoint | Driver faults contained; actor-like event model; capability ownership visible | Extra domain scheduling; level-triggered masking and backpressure must be exact | Default for ordinary devices |
| Polling | Predictable batching and no interrupt storm at high load | Wastes CPU/power at low load; needs scheduling and completion policy | Driver-selectable data-plane mode, not universal |

The default sequence is:

1. controller claims or identifies the source;
2. hard path masks a level source or otherwise prevents unbounded re-entry;
3. hard path records a sequence number and attempts one bounded enqueue;
4. an isolated driver domain reads device status, drains work, and clears the
   device condition with required I/O ordering;
5. the driver acknowledges the generation-tagged event; and
6. the privileged component completes/unmasks only if the device and route are
   still owned by that generation.

If an event queue is full, the kernel must not allocate or overwrite evidence.
For level interrupts it can keep the source masked and mark `pending`; for edge
or MSI sources it needs a counter, coalescing rule, or explicit loss flag.
Overflow behavior is part of the device contract.

### Trigger semantics

- **Level-triggered:** the device condition persists. Masking, device clear,
  controller completion, and unmask ordering matter; doing them in the wrong
  order causes storms or lost service.
- **Edge-triggered:** an edge may be lost if software has no latched count. The
  event API must say whether multiple edges coalesce.
- **MSI/MSI-X:** a device performs a memory write that identifies an interrupt.
  Routing and isolation therefore interact with IOMMU and interrupt remapping.
- **IPI:** is an internal cross-CPU request, not a generic device IRQ. TLB
  shootdown, reschedule, stop, crash-freeze, and code-publication reasons should
  have separate bounded mailboxes or bits so one cannot starve another.
- **NMI/SError/machine check:** is not an ordinary source and may arrive with
  locks held or memory unreliable. It uses reserved state and a fail-stop or
  explicitly recoverable classification.

### Relationship to actors

An interrupt can become a message, but an actor must never run on the hardware
trap stack. The kernel event says “source generation N requires service,” not
“execute arbitrary callback.” Actor mailboxes can receive a runtime-level
translation after the driver domain has applied device protocol and resource
accounting.

This preserves OTP-like failure signaling while keeping electrical interrupt
semantics below the managed runtime. Driver exit itself is a separate reliable
event delivered to a supervisor after the kernel has contained hardware access.

## 6. Time, counters, and timers

### Four different notions

The design must not compress these into one clock:

1. **Clocksource/counter:** a continuously advancing value and frequency used
   to measure intervals.
2. **Clock event:** a comparator or decrementer that causes an interrupt at or
   after a programmed deadline.
3. **Monotonic kernel time:** a converted, non-decreasing timeline that remains
   meaningful across CPUs and documented suspend states.
4. **Civil time:** UTC, synchronization, leap behavior, timezone, and policy,
   implemented by a service from RTC/network/persistent inputs.

The kernel API should expose monotonic deadlines and durations. Civil time must
not control resource leases, scheduler budgets, or retry expiry.

### Periodic tick versus deadline timer

| Choice | Advantages | Costs | Position |
| --- | --- | --- | --- |
| Fixed periodic tick | Simple accounting and timer wheel; easy early bring-up | Idle wakeups, quantized deadlines, frequency-dependent overhead, poor large-core scaling | Bootstrap only |
| Tickless per-CPU deadline | Sleeps until real work; precise actor timers; scales with idle CPUs | Needs robust comparator reprogramming, race handling, migration, and minimum-delta rules | Target design |
| Dedicated timer service CPU | Central ordering and simple global queue | Bottleneck and cross-core wake latency; single failure/overload point | Optional for constrained profile, not default SMP design |

Use per-CPU earliest-deadline queues for local scheduler and actor-runtime wake
events. A global or sharded service handles long-lived civil and application
timers above the kernel. When work migrates, ownership of the programmed
deadline transfers with an IPI/ack protocol; both CPUs may conservatively fire,
but generation checks must make delivery idempotent.

### Required timer behavior

The implementation records:

- counter width, frequency, stability, and conversion error;
- whether values are synchronized across CPUs;
- minimum and maximum programmable delta;
- whether the event is level-sensitive and what clears it;
- behavior under CPU idle, DVFS, suspend, hotplug, and virtualization;
- deadline-overrun and late-interrupt counts;
- wrap handling and maximum safe interval; and
- calibration source and confidence.

Clocksource reads must be ordered enough for their stated use. A timestamp does
not automatically order MMIO completion or memory ownership; the relevant
barrier remains separate.

### Actor-runtime interaction

The kernel should not maintain one hardware timer per actor. A runtime owns a
bounded timer structure and asks for its next domain deadline. The kernel
charges timer insertion and wake events to the domain, wakes the runtime once,
and lets it dispatch expired actor timers. High-assurance system timers—budget
expiry, driver watchdog, shootdown timeout—remain kernel events so a stalled
runtime cannot suppress them.

## 7. CPU bring-up, topology, multicore state, and memory ordering

### CPU lifecycle

Each CPU moves through explicit states:

```text
Absent -> Present -> Parked -> Starting -> Online -> Quiescing -> Offline
                                  \                    \
                                   -> Failed            -> Failed
```

Bring-up must establish a per-CPU stack, trap vector, translation root, local
interrupt interface, timer, per-CPU allocator/cache, scheduler state, and
online generation before the CPU receives work. A CPU is not `Online` merely
because firmware returned success from a start call.

Offline is a transaction:

1. stop new scheduling and device-affinity assignments;
2. migrate or terminate domain work according to policy;
3. drain timer deadlines and local queues;
4. reroute or mask interrupts and wait for in-flight handlers;
5. complete TLB/code-publication generations involving the CPU;
6. save or reject pinned extended state;
7. flush or coordinate caches if the architecture requires it;
8. report quiescence; and
9. invoke the firmware or architecture power mechanism.

Timeout produces `Failed` or `Stuck`, never a false `Offline` state.

### Shared kernel, multikernel, and hybrid

| Structure | Strengths | Weaknesses | Position |
| --- | --- | --- | --- |
| One shared kernel image and structures | Simple global invariants; familiar fast shared-memory paths | Lock contention, cache-line movement, topology assumptions, hard fault containment | Use only for truly global mechanisms |
| Full multikernel with replicated state | Explicit messages, natural heterogeneity, local ownership | Distributed agreement and revocation, duplicate policy, more complex failure/rejoin | Research comparison, not immediate commitment |
| Hybrid per-CPU ownership with message-based mutation | Local fast paths and explicit cross-core effects while retaining a small global capability root | Requires disciplined ownership and carefully chosen shared read-mostly data | Recommended baseline |

The hybrid model uses immutable topology snapshots, per-CPU run/timer/IRQ
queues, owner-CPU mutation for most objects, and explicit messages for remote
operations. Capability derivation, physical-frame ownership, and image
generation retain globally enforced invariants but can use sharded ledgers and
batched cross-core protocols.

### Memory-order contract

The [x86-TSO model](../30-sources/sewell-et-al-2010-x86-tso.md), [Armv8
operational model](../30-sources/flur-et-al-2016-armv8-concurrency.md), and
[RISC-V RVWMO specification](../30-sources/risc-v-international-2026-privileged-architecture.md)
show that “atomic” is not one portable ordering.

Every shared protocol identifies:

- which field publishes object initialization;
- which store is release and which load is acquire;
- which operations require a single total modification order;
- when a full barrier is needed before an IPI, MMIO doorbell, or invalidation;
- whether device memory participates in ordinary coherence;
- who owns the cache line and whether false sharing is permitted; and
- how teardown proves that no observer can retain the old generation.

Zig atomics must be checked against generated instructions for the pinned
toolchain and target features. Architecture wrappers are still needed for
page-table walks, cache maintenance, I/O, and instruction fetch because the
language memory model alone does not define them.

### Topology and heterogeneity

Scheduler policy above this layer consumes, but does not invent:

- package/cluster/core/thread relationships;
- cache and coherence domains;
- NUMA proximity and memory distance;
- heterogeneous performance/energy class;
- supported ISA and vector extensions per CPU; and
- device and memory locality.

The common executable profile must be the intersection of CPUs on which a
domain may migrate. Feature-specific code can pin a domain or use dispatch
stubs; it cannot silently migrate SVE/RVV/crypto state to an incompatible CPU.

## 8. Cache, coherency, and native-code publication

### Three coherence questions

For every memory range ask separately:

1. Are CPU data caches coherent with one another?
2. Are CPU instruction fetches coherent with recent data writes?
3. Are device DMA accesses coherent with CPU caches?

A platform may answer yes, no, or only within a shareability domain for each.
The memory-type registry should prevent two live aliases with incompatible
cacheability. MMIO is never treated as ordinary cached memory merely because a
load/store instruction can address it.

### Publication protocol for generated or loaded code

BEAM-style load-time native generation and hot code publication make this a
first-class system service. The safe conceptual sequence is:

1. allocate writable, non-executable pages owned by a loader domain;
2. emit code and relocation data;
3. validate bounds, entry points, imports, architecture feature set, and image
   identity;
4. finish all data writes;
5. clean data cache to the architecture's point of instruction coherence when
   required;
6. change the mapping to read/execute and invalidate stale writable aliases;
7. invalidate instruction cache or execute `FENCE.I` on every CPU that may run
   the code;
8. issue the required completion and instruction-synchronization barriers;
9. atomically publish a versioned entry capability; and
10. retain old code until all executing and return-address references have
    reached a quiescent generation.

On RISC-V, local `FENCE.I` does not synchronize another hart. On AArch64, the
data clean, instruction invalidate, completion barriers, and final execution
context synchronization have distinct purposes. The runtime must request one
kernel `publishExecutable` operation instead of implementing these sequences
inside each loader.

### Data synchronization for DMA

CPU-to-device and device-to-CPU transfers use direction-aware operations:

- `prepareForDeviceRead`: finish CPU writes and clean as needed;
- `prepareForDeviceWrite`: prevent dirty CPU data from later overwriting the
  device's result and invalidate as needed;
- `completeDeviceRead/Write`: wait for DMA completion and make results visible;
- `transferOwnership`: combine synchronization with queue state; and
- `revoke`: drain, invalidate translation, quarantine on timeout.

On coherent platforms these may compile to ordering only, but the semantic
operation remains so non-coherent backends and bounce buffers do not leak into
drivers.

## 9. FPU, SIMD, vector, and extended state

### Why it belongs here

SIMD is not only an instruction-set optimization. Once code can execute vector
instructions, the kernel owns:

- enable/disable state per privilege level;
- register save, restore, initialization, and scrubbing;
- control/status registers and exception mode;
- vector-length and feature compatibility;
- signal/trap/crash-frame representation;
- debug and core-dump exposure; and
- rules for use in interrupt, kernel, driver, runtime, and cryptographic code.

The state can grow from scalar floating point through fixed-width SIMD to
scalable vectors, matrix extensions, and accelerator contexts. It must be
inventoried from probed features rather than sized by one compile-time x86 or
NEON assumption.

### Switching choices

| Policy | Advantages | Risks | Position |
| --- | --- | --- | --- |
| Disable extended state | Small context and deterministic kernel; catches accidental use | Forfeits compiler/runtime acceleration and cryptography; libraries may assume it | Early trap-path profile only |
| Eager save/restore at every protected-domain switch | Simple ownership and strong confidentiality; predictable worst case | Pays for full state even when unused; scalable vectors can be large | Safe default once enabled |
| Lazy first-use switching | Avoids cost for domains that never use state | More state machine and fault paths; historical LazyFP leak; compiler use is hard to predict | Reject as default; reconsider only with architecture-specific proof and measurements |
| Pin vector work to dedicated domains/CPUs | Amortizes state, supports accelerators and large vectors | Reduces scheduler flexibility and can create hotspots | Optional optimization above eager-safe semantics |

The [LazyFP result](../30-sources/stecklina-prescher-2018-lazyfp.md) is direct
evidence that register ownership is a security boundary. The first
implementation should eagerly restore initialized state for every domain that
uses it and zero or replace secrets before reassignment.

### Managed actors versus kernel domains

The kernel switches extended state per hardware-protected domain or native
thread, not per lightweight actor. A managed runtime may execute many actors on
one scheduler thread and therefore one architectural state owner. Its actor
scheduler must reach a safe point with no live vector temporary assumed across
an actor yield; this is normally a compiler/runtime invariant, not a kernel
save operation.

Native calls that block or migrate need an explicit runtime thread context.
Cryptographic services should prefer isolated domains so key-bearing vector
state, caches, and crash records have a narrower authority boundary.

### Kernel restrictions

- No floating-point or SIMD in reset, trap, hard IRQ, shootdown, or fatal paths.
- Ordinary kernel code remains compiled with features that cannot introduce
  implicit vector instructions unless the function is inside an annotated
  vector-safe component.
- Each optimized implementation has a scalar reference path and runtime
  feature dispatch.
- Vector types are not packet, MMIO, persistent, DMA-descriptor, or ABI layouts;
  serialization uses explicitly sized byte representations.
- Deterministic/replay or numerically sensitive services must state rounding,
  exception, denormal, and feature requirements.

## 10. DMA, IOMMU, and data movement

### Threat and failure model

A bus-mastering device or compromised driver can:

- read secrets or executable code;
- overwrite page tables, capabilities, queues, or another domain;
- keep accessing a buffer after software frees it;
- exploit broad intentionally shared mappings;
- write forged MSI data;
- continue a transaction across reset or ownership transfer;
- exhaust fault queues or I/O translation caches; and
- corrupt results while staying within an authorized buffer.

The [Thunderclap experiments](../30-sources/markettos-et-al-2019-thunderclap.md)
show that merely turning on an IOMMU is insufficient. The [least-privilege
address-space model](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
shows that CPU, device, and translation authority form a network rather than
one physical address space.

### Internal components

- **DMA reachability model:** requester IDs, address width, coherency, segment
  limits, alignment, boundaries, and device/IOMMU group.
- **Buffer manager:** physically backed regions, pinning, zeroing, direction,
  cache state, owner, and generation.
- **IOVA allocator:** per-domain virtual address ranges with guard gaps and
  overflow-safe lengths.
- **IOMMU backend:** device contexts, page tables, command/event/fault queues,
  invalidation, and interrupt remapping.
- **Bounce backend:** trusted low-address/coherent pool and copy protocol for
  devices the IOMMU cannot isolate or reach.
- **Queue protocol:** descriptor ownership, release/acquire and doorbell
  ordering, completion, cancellation, and bounds.
- **Fault service:** attributes a fault to device/domain/generation, masks or
  quarantines the source, and produces bounded evidence.
- **Revocation coordinator:** stops submissions, drains in-flight work,
  invalidates mappings, resets hardware, and releases memory only after proof.

### IOMMU strategy choices

| Strategy | Advantages | Security and performance costs | Position |
| --- | --- | --- | --- |
| No IOMMU, raw physical DMA | Minimal code and translation overhead | Driver/device can access all reachable memory; physical addresses leak; unsafe reuse | Only trusted bootstrap device with explicit degraded profile |
| No IOMMU, validated descriptors and protected rings | Can isolate some software mistakes on constrained hardware | Cannot contain a malicious device; validator/descriptor memory is trusted; protocol-specific | Constrained fallback |
| Shared broad IOMMU domain | Stops access outside a large pool; simple setup | Weak inter-driver isolation; broad shared-memory attacks; hard revocation | Temporary bring-up only |
| Per-driver or per-device IOMMU domain | Least-privilege mappings and clean fault attribution | More page tables, invalidations, context limits, group granularity | Default protection profile |
| Direct user/runtime queue with IOMMU | Fast data plane and customizable service | Complex queue, quota, reset, interrupt, and lifecycle contract | Later optimization after mediated path passes |
| Bounce buffers | Handles address limits and can copy across trust boundary | Copies, fixed pool pressure, secret residue, extra latency | Required safe fallback, not invisible infinite resource |

### Buffer and queue state

Following [CleanQ's ownership insight](../30-sources/haecki-et-al-2019-cleanq.md),
a descriptor does not make memory simultaneously owned by CPU and device.

```text
CPU-owned
   -> prepared-for-device
   -> submitted
   -> device-owned/in-flight
   -> completed
   -> synchronized-for-CPU
   -> CPU-owned

Any state -> revoking -> quiescent -> scrubbed/reusable
                     \-> timeout/quarantined
```

Each transition carries a generation and direction. A timeout does not return
the buffer to the allocator. It moves the buffer and device into quarantine
until reset and invalidation establish that access is impossible.

### Device assignment transaction

Assigning a device to a driver domain should atomically bind:

1. one admitted device function and reset domain;
2. only the required MMIO/PIO subranges;
3. a dedicated IOMMU domain or declared degraded DMA mode;
4. bounded DMA and pinned-memory quotas;
5. interrupt sources and destinations;
6. command/completion queues with ownership semantics;
7. clock/power votes needed to operate;
8. a watchdog and fault endpoint; and
9. a generation-tagged revoke capability retained by the device manager.

If any preparation step fails, none of the grants become usable. Publication
occurs last. Revoke runs in reverse but must first stop new work and drain or
reset old work.

## 11. Device access, buses, and driver domains

### Hardware resource bundle

A driver should never receive “the device” as an unstructured pointer. It
receives a bundle of separately revocable capabilities:

- configuration-space access restricted by register/operation;
- MMIO or PIO windows with memory type and width rules;
- interrupt source and event endpoint;
- DMA domain and buffer allocator quota;
- reset, clock, and power operations allowed for that function;
- device identity, topology location, IOMMU group, and generation;
- optional firmware mailbox under a message-size and timeout contract; and
- diagnostic access that excludes secrets and unrelated functions.

The bus manager owns enumeration and safe configuration writes. Device-class
drivers own device protocol. An isolated PCI driver cannot rewrite bridge
windows or bus mastering for another function.

### Register access and bus lifecycle

Raw `*volatile` pointers are not a sufficient register API. Each admitted
register block needs:

- exact offset, access width, alignment, byte order, and memory type;
- read, write, read-modify-write, write-one-to-clear, or read-to-clear
  semantics;
- reserved-bit masks and values that must be preserved;
- whether reads or writes have side effects;
- required device, memory, or completion barriers;
- whether writes are posted and which safe read or status bit proves
  completion;
- concurrency ownership and interrupt-context rules; and
- behavior when the bus reports an access fault or the device disappears.

Architecture code supplies ordered MMIO/PIO primitives; a controller or driver
wraps them in register-specific operations. A generic service cannot form an
arbitrary physical pointer, and a driver cannot substitute ordinary atomics or
cached memory access for device ordering. Diagnostic register dumps must omit
destructive reads and secret-bearing registers.

Enumeration itself should be decomposed into:

1. **root admission:** obtain an authorized host bridge, bus ranges, MMIO/PIO
   apertures, requester-ID mapping, interrupt path, and power/reset dependency
   from the normalized graph;
2. **safe discovery:** walk functions with bounded timeouts and fault recovery,
   without enabling decoding or bus mastering merely to identify them;
3. **resource sizing:** determine requirements without accepting overflow,
   overlap, aliased windows, or firmware allocations outside admitted roots;
4. **placement:** assign bridge and function windows transactionally under the
   kernel resource ledger;
5. **isolation grouping:** resolve requester IDs, aliases, shared reset and
   power domains, ACS/firewall limitations, and IOMMU granularity before
   claiming two functions are independently assignable;
6. **activation:** install IOMMU-deny state and interrupt ownership before
   enabling decode, MSI, or bus mastering; and
7. **publication:** expose a new topology generation only after every resource
   is valid.

Hot-plug and surprise removal run the same lifecycle in reverse. Removal first
marks the generation unavailable, stops new submissions, masks events, revokes
DMA and MMIO, resets or quarantines dependent functions, and then removes the
resource graph nodes. A bus error from a disappeared device must become a
contained driver failure where the architecture permits recovery; it must not
turn into an endless retry or reuse of the old MMIO capability.

USB-like discovery adds an untrusted descriptor parser and device protocol but
does not change the authority model: the host-controller driver owns only its
controller and DMA domain, while enumerated device identities and bandwidth
allocations are service-level resources. PCIe-like discovery adds bridge
windows, requester aliases, MSI, and function reset. Neither bus should define
the architecture-neutral device API.

### Driver placement choices

| Placement | Benefits | Costs | Default use |
| --- | --- | --- | --- |
| Privileged in-kernel driver | Lowest setup complexity and latency; works before domains exist | Fault/memory corruption is system-wide; expands TCB; hard restart | Interrupt controller, timer, IOMMU, boot console, and smallest boot storage only |
| Isolated Zig native driver | Hardware memory isolation, restart, explicit resources, direct register performance | IPC/domain switch overhead; DMA/IRQ protocol and recovery orchestration | Ordinary device drivers |
| Imported C driver in isolated domain | Reuses vendor/upstream code behind C ABI | Preserves C memory and concurrency hazards; ABI/build assumptions; larger audit | Compatibility exception with wrapper, quotas, and reset |
| Managed actor driver | Natural supervision and messaging; productive protocol code | GC/scheduler latency, no safe raw MMIO semantics, native shim still needed | High-level device service above a small native driver |

The [Nooks experiments](../30-sources/swift-et-al-2003-nooks.md) demonstrate
that isolation and a resource ledger materially improve recovery even in a
compatibility design. This project can make the boundary stronger by starting
ordinary drivers unprivileged and constraining DMA as well as CPU memory
access.

### Failure and restart sequence

When a driver exits, stalls, violates MMIO policy, overruns its IRQ budget, or
causes an IOMMU fault:

1. increment the device-owner generation;
2. mask its interrupt sources and reject old acknowledgements;
3. block new DMA submissions and detach doorbells;
4. wait a bounded interval for completions;
5. invalidate DMA mappings and interrupt remaps;
6. perform function, bus, or power reset if the topology permits it;
7. quarantine on uncertain reset or shared reset-domain impact;
8. scrub and reclaim buffers whose non-access is proven;
9. revoke MMIO, DMA, IRQ, and power capabilities; and
10. send structured failure evidence to the supervisor that decides whether
    and when to instantiate a replacement.

The kernel provides containment and cleanup. OTP-like policy decides
`one-for-one`, dependent-service restart, escalation, or permanent shutdown.

## 12. Power, reset, watchdog, and thermal mechanisms

### Mechanism and policy split

The privileged layer exposes:

- CPU wait-for-interrupt/event and architectural idle states;
- CPU start, stop, suspend, and resume mechanisms;
- device power/reset/clock dependencies and safe register transactions;
- system suspend and reset calls;
- watchdog program, pet, disable, and reason capture;
- thermal and power-limit observations supplied by hardware; and
- transition completion or failure evidence.

An ordinary power service decides governors, wake policy, timer coalescing,
device autosuspend, thermal response, performance versus energy, and user
policy. A service can request a state; the kernel verifies authority and runs
the cross-component transaction.

### CPU idle versus CPU offline

Idle preserves CPU membership and local state while waiting for an event.
Offline removes the CPU from scheduler, timer, interrupt, shootdown, and code-
publication target sets. Treating them as the same creates missed IPIs and
stale translations.

The idle loop must check work after publishing its intent to sleep and before
executing the architecture instruction, closing the “work arrived just before
sleep” race. Wake sources are capability-authorized and rate-limited.

### Device power transition

Powering down a device requires:

1. deny new clients and submissions;
2. drain or cancel operations;
3. mask interrupts;
4. quiesce DMA and invalidate mappings when state will be lost;
5. save only documented restorable registers;
6. enter the device state and then gate clocks/power in dependency order; and
7. publish completion.

Resume reverses dependency order, resets if state is uncertain, rebuilds DMA
and IRQ routes, and publishes a new generation. The old driver cannot continue
using pre-suspend tokens.

### System suspend

System suspend is a distributed transaction across supervised services and
hardware components:

- freeze or checkpoint services;
- choose wake-capable endpoints;
- quiesce storage and update state;
- stop DMA and non-wake interrupts;
- migrate timers to a surviving counter/wake timer;
- offline secondary CPUs;
- persist image/generation and crash-safe intent;
- call the platform mechanism; and
- on resume, validate reset versus resume, reconstruct topology, and restart
  components in dependency order.

A partial failure aborts toward the last known running state. It must not enter
firmware with a device still writing into memory the resume path will reuse.

### Watchdog

The watchdog must be independent enough to reset a wedged scheduler. Petting is
conditional on progress proofs from critical components, not a periodic kernel
timer that fires even when the system is unhealthy. Record last successful
progress generations and watchdog stage in retained memory before reset.

Use a staged design where possible: early warning captures bounded state on a
reserved CPU/path; hard timeout resets regardless of capture success.

## 13. Security roots, entropy, debug, and RAS

### Security services below actors

The hardware layer should inventory and expose, without overclaiming:

- immutable or firmware root of trust;
- verified-boot result and measurement log;
- rollback-protected counters or their absence;
- device-unique key service with non-exportable-key semantics if present;
- entropy sources, health status, boot seed provenance, and reseed events;
- memory-encryption or tagging domains;
- debug authentication and production lock state;
- hardware unique IDs that are not automatically identities; and
- speculative-execution and architecture security mitigations enabled.

Raw hardware RNG output is not directly an actor API. A cryptographic service
combines admitted sources, health tests, persistent state where appropriate,
and a DRBG. The boot seed must be labeled `untrusted`, `provisional`, or
`conditioned` so early capabilities and network identities do not claim more
entropy than exists.

### Debug and observability boundary

Bring-up requires serial, semihosting, JTAG, breakpoints, trace, performance
counters, and memory inspection. Production may need to restrict or
authenticate all of them because debug modules can bypass CPU execution and
access physical memory.

Debug configuration is a security state recorded in boot evidence. Diagnostic
builds, production builds, and recovery builds should be distinct signed
profiles. A “disabled” software console does not prove a hardware debug port is
locked.

### RAS classification

Hardware errors should be normalized without erasing raw records:

- corrected and continuing;
- deferred or restartable with a poisoned resource;
- uncorrected but contained to a CPU, page, device, or domain;
- uncontained or execution-state-corrupting; and
- unknown.

The response depends on scope: retire a page, offline a CPU, reset a device,
terminate a domain, or reset the machine. Continuing after an uncontained
machine check because a supervisor prefers restart is not fault tolerance.

### Minimal crash record

The fatal path writes a fixed-size, checksummed, append/generation record using
preallocated memory and the smallest available sink. It should include:

- magic, schema, length, and checksum;
- boot/image and hardware-profile identity;
- reset reason and prior boot attempt;
- CPU, privilege, monotonic counter, raw cause, and full trap frame pointer or
  bounded copy;
- online CPU mask and whether other CPUs acknowledged freeze;
- active domain, driver, IRQ, mapping, and DMA generations;
- recent bounded event headers, not arbitrary logs;
- memory/RAS/IOMMU error records available without allocation; and
- why capture stopped or which fields are incomplete.

Crash storage is not a general filesystem. A later diagnostic service extracts
and authenticates the record after reboot.

## Cross-component transactions

These interactions are the real architecture. Each needs a testable state
machine and timeout behavior.

| Transaction | Components that must agree | Commit point | Safe failure state |
| --- | --- | --- | --- |
| Boot handoff | firmware, loader, memory map, description, image verifier | validated immutable `BootInfo` and firmware exit | recovery console/reset with boot-attempt evidence |
| Map or unmap | frame ledger, page tables, CPU set, TLB generations, executable/cache state | all required observers acknowledge new generation | old mapping retained or frame quarantined |
| Deliver IRQ | device, controller, route, owner generation, endpoint, scheduler | bounded event accepted or explicit pending/loss state | source masked and attributed |
| Publish code | loader mapping, validation, D/I caches, TLB, CPU set, service registry | versioned executable capability atomically selected | unpublished pages or old version remains current |
| Assign device | bus, MMIO, reset, IOMMU, buffers, IRQ, power, driver domain | resource bundle published to new generation | DMA denied, IRQ masked, no driver authority |
| Revoke device | driver, queues, DMA, IOMMU, IRQ, reset, buffer ledger | no possible access by old generation | device and buffers quarantined |
| Offline CPU | scheduler, timers, IRQ routes, TLB/code generations, extended state, firmware | CPU removed from every target set and parked | CPU stays online or is marked stuck; never silently absent |
| Suspend system | services, storage/update, devices, DMA, IRQ, timers, CPUs, firmware | final platform suspend call after durable intent | abort back to running or reset into recovery |
| Fatal failure | CPU freeze, IRQ/DMA containment, RAS, crash sink, watchdog | bounded record committed | watchdog reset with partial-record marker |

### Locking and callback rule

No cross-component transaction calls an untrusted driver or managed service
while holding architecture-global locks. Preparation gathers immutable plans
and capabilities; components apply bounded local changes; publication uses a
generation; notifications occur after locks are released. Rollback either
returns to the prior generation or marks resources quarantined.

### Idempotence and generations

Hardware events can be duplicated, delayed, or arrive after reset. Every
completion and acknowledgement carries an object generation where the hardware
allows software association. If hardware supplies only a numeric source, the
privileged bridge attaches the current route generation and rejects late
userspace responses.

## Architecture-neutral interfaces

### Type vocabulary

The API should distinguish at least:

- `CpuId`, `CpuGeneration`, `CpuSet`;
- `PhysAddr`, `VirtAddr`, `Iova`, and checked `ByteRange`;
- `FrameId`, `FrameLease`, `MappingId`, `AddressSpaceId`;
- `IrqSourceId`, `IrqRouteId`, `IrqEventSequence`;
- `CounterTicks`, `MonotonicInstant`, `Duration`, `Deadline`;
- `DeviceId`, `DeviceGeneration`, `DmaDomainId`, `DmaLease`;
- `MemoryType`, `CacheDomainId`, `CoherencyKind`;
- `PowerDomainId`, `ResetDomainId`, `TransitionId`; and
- `BootGeneration`, `ImageGeneration`, `CapabilityId`.

None are implicitly interchangeable integers. Construction checks range and
provenance; arithmetic uses checked operations; serialization has a versioned
byte format separate from in-memory Zig layout.

### Interface rules

- Functions name whether they may allocate, block, sleep, send IPIs, or wait
  for hardware.
- Trap-safe functions are a small audited subset.
- Every asynchronous request returns a token that reaches `complete`,
  `cancelled`, `timed_out`, or `quarantined`; dropping a token does not cancel
  hardware implicitly.
- Timeouts use monotonic deadlines and report whether the operation may still
  complete later.
- APIs return unsupported-feature and degraded-protection results explicitly.
- Batch forms exist for page maps, invalidations, DMA mappings, and IRQ routes
  so correctness does not force one expensive global operation per element.
- Query returns a snapshot generation; consumers must tolerate topology change
  or hold a lease that prevents it.
- Raw controller registers, PTE bits, firmware table nodes, and physical
  pointers never cross into managed runtime or ordinary driver APIs.

### Suggested Zig package boundaries

```text
kernel/
  arch/
    riscv64/        trap, CSR, RVWMO, Sv39, cache/TLB, context
    aarch64/        exception, system registers, translation, cache, context
    x86_64/         later compatibility port
  boot/
    uefi/           UEFI loader adapter
    sbi/            RISC-V supervisor handoff
    test/           deterministic synthetic handoff
  description/
    dt/             parser and binding normalization
    acpi/           table subset, later AML boundary
    static/         constrained test/board descriptions
  hw/
    topology/       immutable graph and generations
    protection/     frame and translation transactions
    interrupt/      source, controller, route, endpoint bridge
    time/           counters, event timers, deadlines
    cpu/            bring-up, IPI, online/offline
    cache/          memory attributes, DMA sync, code publication
    extended_state/ FPU/SIMD/vector/debug state
    dma/            domains, leases, IOMMU, bounce backend
    device/         MMIO, bus, reset, driver-resource bundles
    power/          idle, suspend, reset, watchdog
    ras/            faults, crash records, boot evidence
  platform/
    qemu_riscv_virt/
    qemu_aarch64_virt/
```

Architecture directories implement mechanisms. Platform directories bind
real controller instances and quirks. Shared `hw` components own policy-free
state machines. A platform file may not reimplement page allocation, IRQ event
semantics, or device revocation.

## Candidate architecture comparison

| Criterion | RV64 application profile | AArch64 application profile | x86-64 PC/server | Armv8-M or RV32 PMP profile |
| --- | --- | --- | --- | --- |
| Privilege | Open M/S/U separation; S-mode kernel above SBI | Mature EL0/EL1 plus optional EL2/EL3 separation | Mature rings plus VMX | Privileged/unprivileged modes; often no virtual memory |
| VM/protection | Sv39 is compact; PMP below S-mode; open spec | Rich stage-1/2 translation and attributes | Mature paging, PCID, large pages, protection keys on some CPUs | Finite MPU/PMP regions; physical addressing and static limits |
| Memory model | RVWMO weak ordering; explicit fences | Weak ordering and explicit barriers/shareability | TSO is stronger and can hide portability bugs | Architecture-dependent; often simpler cores but devices still need ordering |
| Interrupts | PLIC simple but limited; AIA modern MSI/virtualization | GICv3/v4 and ITS are mature but complex | Local/I/O APIC plus MSI/MSI-X and legacy | NVIC/CLIC-like low-latency options vary; not one common model |
| Time | SBI timer initially; Sstc/architectural counters by profile | Generic counter/timer and PSCI integration | TSC, deadline timer, HPET/APIC variants | SysTick/mtime/vendor timers; suspend behavior varies |
| DMA isolation | Ratified IOMMU, QEMU reference support; physical adoption still growing | Mature SMMUv3 ecosystem | VT-d/AMD IOMMU and interrupt remapping mature | Usually no IOMMU; bus firewalls or validated/bounce paths needed |
| Discovery/firmware | DT common; SBI; UEFI/ACPI server profile emerging | DT on SoCs; UEFI/ACPI and PSCI on standardized systems | UEFI/ACPI/PCI mature but large and quirky | Static/DT/vendor metadata, board-specific clocks and pins |
| Emulation | QEMU `virt` can switch PLIC/AIA, DT/ACPI, IOMMU | QEMU `virt` supports GIC, SMMU, PSCI, PCI/virtio | QEMU PC models broad but include legacy surface | QEMU boards vary and often omit exact silicon behavior |
| Ecosystem | Open specifications, easy ISA inspection, growing boards; platform fragmentation | Mature silicon, documentation and OS experience; licensing and SoC diversity | Best commodity availability and tools; largest initial legacy/security surface | Low cost, deterministic, excellent constrained test; weaker isolation guarantees |
| Main attraction | Clean research target with open, decomposed contracts | Strong portability and production-system validation | Commodity compatibility and mature server features | Forces explicit resource bounds and no-MMU design |
| Main risk | Treating open ISA as a standardized board; uneven AIA/IOMMU adoption | Underestimating cache, firmware, and GIC/SMMU complexity | PC complexity dominates architecture work and TSO masks errors | Claiming equivalence to MMU/IOMMU isolation when hardware cannot supply it |

### Why RV64 first

RV64 is not selected because it is universally simpler. It is selected because
the ISA, privileged architecture, SBI, AIA, and IOMMU contracts are openly
available; QEMU can expose them incrementally; and an S-mode kernel can avoid
owning M-mode board bring-up initially. The modularity makes missing assumptions
visible.

The risk is platform fragmentation. The first profile must list exact mandatory
extensions, firmware calls, interrupt controller, timer, discovery input,
device set, and IOMMU mode. “Runs on RISC-V” is not a compatibility statement.

### Why AArch64 second

AArch64 supplies a mature contrasting system: exception levels, GICv3,
generic timers, PSCI, SMMUv3, explicit cache maintenance, and a broad SoC/server
ecosystem. Porting early prevents RISC-V controller and firmware shapes from
becoming the common API.

The AArch64 port is complete only when SMP, remote TLB invalidation, native-code
publication, IRQ affinity, timer migration, SMMU faults, and driver restart
pass—not when serial output appears.

### Why not x86-64 first

x86-64 has excellent tools and hardware, but its first boot path rapidly pulls
in UEFI, ACPI/AML, APIC variants, PCI, model-specific registers, XSAVE feature
state, chipset behavior, and mitigation policy. Its relatively strong TSO model
also makes it a poor sole test of portable concurrency. It should become a
later commodity-compatibility target once the architecture-neutral contracts
exist.

### Why keep a constrained profile

An MPU/PMP system is valuable because it tests whether capabilities, endpoint
bounds, static allocation, driver recovery, and supervision still make sense
without paging, large RAM, an IOMMU, or many cores. It needs its own declared
guarantee class. A device with unrestricted DMA cannot host mutually hostile
drivers simply because CPU MPU regions are correct.

## Recommended target profiles

### Profile R0: RV64 single-core bootstrap

- QEMU `virt`, with the exact QEMU release/build, machine options, CPU model,
  and generated Devicetree hash recorded;
- RV64 integer/atomic/compressed plus the floating-point choice pinned rather
  than relying on `-cpu max` drift;
- S-mode kernel above pinned OpenSBI 3.0-compatible firmware;
- Devicetree v0.4-compatible input copied and validated at boot;
- Sv39, 4 KiB pages, W^X, guard pages, no large-page optimization;
- SBI timer, reset, debug console, and hart services where applicable;
- one CPU, PLIC, UART, and polled then interrupt-driven virtio-mmio block or
  network device;
- no untrusted DMA: device path is explicitly trusted or uses a bounded bounce
  pool; and
- deterministic reset-to-first-domain trace and crash record.

R0 exists to validate decomposition. It is not the security target.

### Profile R1: RV64 SMP and protection

- multiple harts, per-CPU state, IPIs, remote fences, shootdown generations,
  and tickless deadlines;
- AIA with APLIC and IMSIC, including MSI routing and affinity changes;
- RISC-V IOMMU enabled in deny-by-default mode with command/fault queues;
- per-driver domains, bounded DMA leases, interrupt-to-endpoint delivery,
  restart and revoke tests;
- safe cross-hart `FENCE.I` code publication;
- weak-memory litmus and queue stress under TCG and, when available, KVM or
  physical hardware; and
- injected malformed DT, stuck IRQ, IOMMU fault, late completion, and CPU
  offline timeout.

R1 is the first meaningful isolation profile.

### Profile A1: AArch64 portability validation

- a versioned Arm `virt-N.N` machine type on a pinned QEMU release and a
  specified AArch64 CPU model;
- EL1 non-secure kernel, PSCI firmware interface, DT first and UEFI as a second
  boot adapter;
- 4 KiB translation granule, ASID generations, W^X, SMP TLB shootdown;
- GICv3 plus ITS/MSI, generic timer, SMMUv3;
- the same driver-domain, DMA-lease, interrupt-event, code-publication,
  CPU-offline, and crash tests as R1; and
- architecture-specific cache and barrier tracing enabled in diagnostic builds.

### Physical profile selection gate

Do not choose by CPU benchmark or popularity alone. Require:

- public CPU, interrupt, timer, IOMMU, reset, clock, and board documentation;
- a maintained firmware source or a narrow stable interface with pin-able
  binaries;
- hardware debug plus a recoverable flash/update method;
- at least two independent boot media or immutable recovery path;
- stable monotonic counter across documented idle states;
- an IOMMU with known requester topology, or an explicit single-trusted-driver
  DMA profile;
- accessible reset for devices used in driver-restart experiments;
- serial or memory crash evidence that survives ordinary service failure;
- upstream QEMU/FVP or another model useful for differential tests; and
- availability to every contributor who must reproduce bring-up.

## Implementation and experiment sequence

### Phase 0: contracts before controllers

1. Define checked address/range, ID/generation, capability, deadline, mapping,
   IRQ event, DMA lease, and transition-result types.
2. Write state-machine tests for feature admission, mapping, IRQ bind/ack,
   device assignment and removal, buffer ownership, CPU lifecycle, and code
   publication using fake backends.
3. Fuzz Devicetree and `BootInfo` parsers on the host; reject all overlapping
   or out-of-bounds resources deterministically.
4. Pin Zig, linker, QEMU, firmware, machine, CPU, and build modes.
5. Inspect all assembly and freestanding ABI boundaries in generated code.

### Phase 1: single-core proof of ownership

1. Enter from the test and SBI boot adapters into identical `BootInfo`.
2. Bring up early console, frame ledger, Sv39, guarded kernel stack, trap table,
   monotonic counter, and one event timer.
3. Enter an unprivileged Zig test domain and contain illegal instruction,
   execute, read/write, and syscall faults.
4. Route one timer and one UART interrupt through the bounded endpoint bridge.
5. Record a fatal trap into the minimal crash sink and validate it after reset.

Success is a complete state trace and negative tests, not just output.

### Phase 2: SMP, ordering, and publication

1. Start and stop secondary harts with online generations.
2. Implement per-CPU queues and explicit IPI reasons.
3. Stress ASID reuse and TLB shootdown while domains map/unmap and fault.
4. Run architecture litmus tests and queue ownership tests under randomized
   delays.
5. Generate a small native function, publish it under W^X, execute on every
   hart, replace it, quiesce, and reclaim the old version.
6. Enable and eagerly switch FPU/SIMD state between hostile test domains;
   verify initialization and no cross-domain residue.

### Phase 3: isolated device lifecycle

1. Bind a virtio device to an unprivileged Zig driver through MMIO and IRQ
   capabilities without DMA first.
2. Add bounded bounce buffers and explicit ownership transitions.
3. Enable the RISC-V IOMMU, start DMA-denied, and grant only submitted buffers.
4. Inject invalid IOVA, stale generation, queue overflow, interrupt storm,
   surprise removal, MMIO fault, driver crash, stuck DMA, and reset failure.
5. Verify that uncertain buffers quarantine, unrelated domains continue, and a
   supervisor receives structured failure evidence.
6. Compare mediated I/O with direct queue access only after identical safety
   tests pass.

### Phase 4: power, firmware, and recovery

1. Test idle-entry race, timer wake, CPU offline timeout, IRQ rerouting, and
   domain migration.
2. Suspend and resume in QEMU while queues, timers, and code versions are
   active; distinguish true resume from reset.
3. Stage signed A/B images, cut power at every update write/commit point, and
   prove selection of old or new complete generation.
4. Stop critical progress and confirm watchdog early warning and hard reset.
5. Corrupt firmware description inputs and boot measurements and confirm
   recovery behavior.

### Phase 5: AArch64 and physical hardware

Port contracts rather than copy the RV64 implementation. Run the full suite
with GICv3, generic timer, SMMUv3, AArch64 page-table sequences, and cache
publication. Then repeat on physical hardware with logic-analyzer or external
timestamp evidence for interrupt/reset paths, DMA fault injection, and power
loss.

## Verification matrix

| Property | Host/model test | QEMU test | Physical test |
| --- | --- | --- | --- |
| Parser safety and normalization | fuzz, property, malformed corpus | boot malformed tables/blobs | altered firmware DT/ACPI where safe |
| Feature and erratum admission | profile/intersection and rejection properties | varied CPU models and denied instructions | implementation revision, firmware/microcode, and workaround checks |
| Privilege isolation | model state transitions | illegal accesses and trap corpus | same plus debug-port checks |
| Mapping/TLB correctness | transaction model and generation tests | concurrent map/fault/shootdown stress | architecture litmus and long stress |
| IRQ semantics | fake edge/level/MSI backend | storm, coalesce, late ack, affinity | electrical/device status and latency |
| Timer monotonicity | conversion/wrap properties | migration, load, virtual suspend | DVFS, idle, suspend, drift measurement |
| Code publication | cache-backend trace model | cross-CPU replace/execute stress | incoherent-cache-sensitive hardware where available |
| Extended state | randomized context codec | hostile domain SIMD patterns | cross-core and feature-heterogeneous test |
| DMA isolation | lease/queue model | IOMMU faults, stale IOVA, reset timeout | malicious/fault-injected device or FPGA where possible |
| Driver recovery | deterministic resource ledger | crash, removal, and bus fault at every lifecycle state | device reset and hot-plug/power-cycle |
| Boot/update recovery | image state-machine property tests | interrupted virtual-media writes | power cut at every commit phase |
| Fatal evidence | serialization/checksum tests | injected trap and frozen CPU | watchdog, machine error where safely injectable |

Every test records architecture, CPU features, firmware, QEMU or board
revision, toolchain, build mode, CPU count, memory size, controller selection,
IOMMU mode, and exact commands. A result without those conditions is an
observation, not a portability claim.

## Decisions and non-decisions

### Decisions this synthesis recommends now

- Zig implements the kernel and new native hardware components.
- The common layer is componentized around explicit state machines; no
  monolithic HAL.
- The normal application-class kernel runs at OS supervisor privilege, not
  firmware/secure-monitor privilege.
- RV64 QEMU `virt` is the first bootstrap architecture; AArch64 `virt` is the
  required second architecture.
- PLIC may bootstrap interrupts, but the interface must pass an AIA/MSI profile.
- Devicetree is the first discovery input; ACPI is a separate normalized front
  end, not a future replacement API.
- MMU profiles use W^X, guard pages, generation-tagged ASIDs, centralized
  mapping transactions, and deferred reuse after shootdown.
- Hard interrupt paths are bounded and allocation-free; ordinary drivers are
  isolated domains receiving event endpoints.
- IOMMU-enabled profiles start DMA-denied and use per-driver/device domains
  when requester topology permits.
- FPU/SIMD state switching is eager by default at protected-domain boundaries;
  trap and hard IRQ code does not use it.
- Native-code publication is a kernel architecture service because hot loading
  crosses W^X, cache, TLB, CPU, and version-lifetime boundaries.
- Power, reset, and driver recovery are cross-component transactions with
  quarantine on uncertainty.

### Still open

- exact mandatory RV64 extensions and CPU model;
- physical CPU erratum data, firmware/microcode update, and feature-admission
  policy for each selected board;
- exact pinned QEMU, OpenSBI, and firmware artifacts;
- whether R0 uses SBI timer only or requires Sstc immediately;
- permanent direct map versus temporary kernel mapping windows;
- specific endpoint overflow/coalescing semantics per IRQ class;
- capability representation and revocation data structure;
- per-CPU ownership versus replication for each global ledger;
- minimum IOMMU and interrupt-remapping requirements for a production profile;
- retained crash-storage medium and atomic record format;
- full ACPI interpreter strategy and whether it runs outside the kernel;
- CHERI, MTE/tagging, stage-2, and confidential-computing profiles;
- first physical RV64 and AArch64 boards; and
- quantified interrupt, syscall, shootdown, DMA-map, context-switch, and
  restart budgets.

## Attractive mistakes to avoid

- Calling a set of architecture-specific function pointers a portable design
  while raw PTE, IRQ, and firmware semantics leak into callers.
- Treating QEMU `virt` as representative physical hardware.
- Treating “RISC-V,” “Arm,” or “x86-64” as one complete platform profile.
- Parsing ACPI or Devicetree directly inside every driver.
- Using the existence of an IOMMU as evidence that DMA is isolated.
- Freeing a frame immediately after editing a page table or IOMMU mapping.
- Running managed actors or arbitrary driver callbacks on a trap stack.
- Leaving a level IRQ enabled when its endpoint is full.
- Using one wall clock for deadlines, accounting, and civil time.
- Assuming CPU cache coherence includes instruction fetch or device DMA.
- Lazy-switching FPU/SIMD state before threat analysis and measurement.
- Making every lightweight actor a hardware context, or conversely making a
  whole machine one runtime protection domain.
- Letting a crashed driver decide whether its device is quiescent.
- Claiming an MPU/PMP target provides the same guarantees as MMU plus IOMMU.
- Retaining UEFI runtime services merely because they are available.
- Choosing a physical board before reset, debug, documentation, and recovery
  are reproducible.

## Consequences for the wider operating-system layers

This hardware layer changes the proposed system decomposition in specific
ways:

- The **minimal privileged kernel** consumes typed architecture components and
  owns cross-domain capability, frame, endpoint, budget, and transition
  ledgers. It does not contain device-class policy.
- The **managed actor runtime** receives monotonic deadlines, bounded event
  channels, memory leases, domain faults, and versioned executable publication.
  It does not see raw interrupts, page tables, or DMA addresses.
- **Driver services** are native Zig domains by default. They can be supervised
  like OTP workers only because the kernel first masks, revokes, resets, and
  accounts for their hardware.
- **OTP-like services** decide restart, dependency, power, update, naming, and
  distribution policy from structured events. They cannot override quarantine
  or claim a failed hardware transition succeeded.
- **Applications** use service capabilities. Local and remote services can
  share actor semantics without pretending hardware latency, loss, and failure
  are identical.

The deepest BEAM/OTP influence is therefore not “make the interrupt controller
an actor.” It is to turn uncontrolled asynchronous hardware behavior into
isolated identities, explicit messages, observable failure, bounded ownership,
and restartable services—while keeping the tiny mechanisms that enforce those
properties below the runtime that benefits from them.

## Connections

- [BEAM, ERTS, and OTP principles for a new operating
  system](beam-erts-and-otp-principles-for-a-new-operating-system.md) supplies
  the wider kernel/runtime/service decomposition this note refines.
- [Zig is the kernel implementation
  language](zig-as-the-kernel-implementation-language.md) fixes the language
  and unsafe-boundary policy used by every proposed component.
- [Which hardware contract should the kernel
  adopt?](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
  tracks the unverified target, profile, and performance choices.
- [Hardware and architecture support](../10-maps/hardware-and-architecture-support.md)
  is the curated path through specifications, papers, this synthesis, and the
  research journal.

## Sources

### Firmware and platform description

- [UEFI Specification 2.11](../30-sources/uefi-forum-2024-uefi-2-11.md)
- [ACPI Specification 6.6](../30-sources/uefi-forum-2025-acpi-6-6.md)
- [Devicetree Specification 0.4](../30-sources/devicetree-org-2023-devicetree-0-4.md)
- [Platform Firmware Resiliency Guidelines](../30-sources/regenscheid-2018-platform-firmware-resiliency.md)

### Architecture and reference-platform specifications

- [RISC-V privileged and unprivileged architecture specifications](../30-sources/risc-v-international-2026-privileged-architecture.md)
- [RISC-V SBI 3.0](../30-sources/risc-v-international-2025-sbi-3-0.md)
- [RISC-V AIA 1.0](../30-sources/risc-v-international-2023-advanced-interrupt-architecture.md)
- [RISC-V IOMMU 1.0.1](../30-sources/risc-v-international-2026-iommu-1-0-1.md)
- [Arm A-profile system architecture documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [Intel 64 system programming and VT-d documentation](../30-sources/intel-2026-system-programming-documentation.md)
- [QEMU Arm and RISC-V `virt` platform documentation](../30-sources/qemu-project-2026-virt-platform-documentation.md)

### OS structure, isolation, and I/O research

- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md)
- [Comprehensive formal verification of an OS microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
- [A least-privilege memory protection model for modern hardware](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
- [Arrakis](../30-sources/peter-et-al-2014-arrakis.md)
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md)
- [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md)
- [Tock](../30-sources/levy-et-al-2017-tock.md)
- [Nooks](../30-sources/swift-et-al-2003-nooks.md)
- [CHERI ISAv9](../30-sources/watson-et-al-2023-cheri-v9.md)

### Concurrency, virtual memory, and extended state

- [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md)
- [Operational ARMv8 concurrency model](../30-sources/flur-et-al-2016-armv8-concurrency.md)
- [Relaxed virtual memory in Armv8-A](../30-sources/simner-et-al-2022-relaxed-virtual-memory.md)
- [LazyFP](../30-sources/stecklina-prescher-2018-lazyfp.md)
