---
title: "x86-64 compatibility envelope and test fixtures"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - boot
  - cpu-architecture
  - hardware-profile
  - proof-of-concept
  - qemu
  - x86-64
aliases:
  - "Active architecture target"
  - "Generic x86-64 PC target"
---

# x86-64 compatibility envelope and test fixtures

## Decision and scope

Kay OS initially targets a documented **generic Intel-compatible x86-64 PC
envelope**, not a particular motherboard or workstation. A machine is a
physical qualification fixture only after its observed configuration and Kay
OS result are recorded. The Dell Precision T7500 in the laboratory is the
first available candidate, designated **physical fixture P1**, but it neither
defines the architecture nor blocks virtual implementation.

This scope preserves the user's correction from an AMD processor assumption to
the available Intel/x86-64 laboratory hardware while superseding the later,
overly narrow interpretation that the T7500 itself was the OS target. The
[archived AMD detour](../../90-archive/amd64-lab-target-and-minimal-qemu-profile.md)
and earlier provisional RV64/QEMU virt/Sv39/OpenSBI path remain historical.

The [T7500 platform reference](dell-precision-t7500-platform-reference.md)
records family capabilities useful when P1 is eventually qualified. Published
family options are not installed-unit facts and are not kernel configuration.
Other x86-64 machines may become P2, P3, and later fixtures without changing
the architecture contract.

On 2026-09-17 the user fixed the initial QEMU baseline at 64 MiB, superseding
the earlier 128 MiB proposal. That number constrains the smallest development
fixture; it is not a maximum supported physical memory size or a statement
about the T7500.

The first delivery remains a minimal bootable OS with a native ring-3 CLI and
an Kay-owned ring-0 kernel. The completed M0–M4 proof still requires the
project's compiled-BEAM profile and automatic process-local tracing GC outside
the kernel. AtomVM, graphics, desktop work, networking and writable storage
do not enter the minimum boot test.

“AMD64” in an ELF machine identifier or the System V AMD64 ABI is a shared
architecture/ABI name, not a requirement for an AMD processor. Those valid
technical references remain. The first backend and test fixtures use
Intel-compatible behavior; AMD-specific MSRs, SVM/SEV, AMD IOMMU and AMD
processor-family work are outside the initial envelope unless a future fixture
and capability require them.

## Initial compatibility envelope

Kay OS must discover machine properties during boot instead of compiling a
fixture inventory into the kernel. The initial envelope is deliberately
bounded and grows only through explicit capability and test evidence:

- x86-64 long mode and the declared compiler instruction subset;
- Limine's selected x86-64 handoff and validated memory-map information;
- CPUID-based feature detection rather than model-name inference;
- ACPI root/table validation and APIC discovery needed by the implemented
  single-CPU interrupt and timer path;
- a supported early serial-console path for the CLI-first proof of concept;
- runtime discovery of memory, CPU topology and relevant platform resources;
- rejection of missing mandatory facilities with bounded diagnostics; and
- safe ignoring or reporting of unsupported devices that are not required for
  boot, memory protection, interrupts, time or the selected console.

The initial proof does not claim every x86-64 PC, every firmware path, arbitrary
USB input, graphics, storage, networking, SMP, NUMA or hotplug. Each newly
claimed facility expands the envelope only after its discovery, fallback and
failure behavior are tested.

## Minimal execution profile

These are adopted test constraints and implementation proposals, not results
from a booted guest.

| Area | Initial constraint | Evidence still required |
| --- | --- | --- |
| ISA and privilege | Intel-compatible x86-64 subset; kernel CPL 0, native services CPL 3 | Actual entry state, CPUID discovery report and ring-transition trace |
| Memory | Four-level paging and 4 KiB base pages as the initial design; 64 MiB guest RAM | Entry/allocator layout, reserved ranges, NX availability and enforced permissions |
| CPU use | One executing logical CPU; one virtual socket/core/thread | Timer/context tests before enabling concurrency |
| Firmware | Explicit SeaBIOS for the minimal QEMU baseline | Pin firmware and bootloader; qualify each additional BIOS/UEFI path separately |
| Native images | Static, little-endian ELF64/AMD64 subset proposed | Toolchain, linker, calling convention, helper census and loader tests |
| I/O | Explicit emulated serial, headless display, no NIC or writable data disk | Bounded serial input/output and unattended test harness |
| Runtime | Independent user-space interpreter and process-local tracing GC | Compiled fixtures, feature closure and guest conformance tests |

Do not require later-generation features such as AVX/AVX2 or five-level paging
for the initial envelope. PCID, x2APIC, timer modes, extended-state facilities
and IOMMU support must be discovered and independently qualified before use.
Intel virtualization support is not a first-boot dependency. A modern Intel
manual is not evidence that any particular fixture implements every feature it
describes.

The [AMD64 psABI study](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md)
separates the baseline from later microarchitecture levels. A full ordinary
AMD64 procedure environment includes floating-point/SIMD expectations. An
integer-only bring-up must therefore be an explicitly restricted native
profile, with generated-code checks and rejected unsupported use; it must not
claim full psABI execution support merely because pointers are 64-bit.
Implement initialized, isolated context ownership before admitting additional
register state.

## QEMU configuration intent

The [JSON record](../../assets/qemu-minimal-x86-64.json) records the selected
virtual inputs and their checked identities. It is **not QEMU's `-readconfig`
format**, an implemented launcher, a guest boot result, or a qualified run
manifest.

The selected baseline uses distribution QEMU 8.2.2 package
`1:8.2.2+ds-0ubuntu1.18`, the versioned `pc-q35-8.2` machine and TCG.
Start with `Nehalem-v1` as an older-generation Intel instruction fixture,
not as an exact emulation of any physical CPU. This replaces the Opteron
model. The named model is listed in
[QEMU's CPU/configuration documentation](../../30-sources/qemu-project-2026-x86-pc-test-configuration.md).
Its name and the machine version are available in the selected binary; each
run must recheck the pinned executable and firmware identities. Do not silently
substitute `max`, `host` or a different CPU when a feature is missing.

Q35 is a synthetic PC fixture, not a physical motherboard replica.
Its chipset and boot-media controller do not validate the physical storage,
network or interrupt wiring. TCG keeps initial execution independent of
host-vendor hardware acceleration. KVM/host passthrough can be a separately
recorded later acceleration profile, not the reproducible baseline.

Additional pinned CPU, machine, memory, topology and firmware profiles form a
capability-driven compatibility matrix. Add a profile only when it tests an
implemented discovery or fallback path. Do not silently expand the baseline or
use host CPU passthrough as portable evidence. Keep compiler instruction
selection within the agreed subset and record every profile independently.

An eventual launch template, **not executed here**, is:

```bash
qemu-system-x86_64 \
  -machine "${KAY_QEMU_MACHINE:?set the pinned versioned pc-q35 machine}" \
  -accel tcg \
  -cpu Nehalem-v1 \
  -smp 1,sockets=1,cores=1,threads=1 \
  -m 64M \
  -nodefaults \
  -display none \
  -monitor none \
  -serial stdio \
  -nic none \
  -bios "${KAY_SEABIOS:?set the pinned SeaBIOS path}" \
  -drive "file=${KAY_BOOT_ISO:?set the bootable ISO path},format=raw,if=ide,index=0,media=cdrom,readonly=on" \
  -boot order=d \
  -no-reboot \
  -no-shutdown
```

The bootloader, its entry protocol and the BIOS-bootable ISO do not yet exist
as pinned artifacts in this archive. Use paths without commas in this template,
or implement correct QEMU option escaping in a future launcher. Check
`--version`, `-machine help` and `-cpu help` against the chosen binary;
record hashes for the executable, firmware, bootloader, kernel and CLI images.
The shell variables deliberately fail if required inputs are unset, but do
not validate their contents.

No NIC, writable guest data storage, passthrough or host-shared directory is
configured. The read-only ISO supplies initial images; this does not mean the
guest has no virtual boot controller. `-nodefaults` removes optional default
devices, not the machine's entire chipset. `-no-reboot` prevents an automatic
reboot loop; `-no-shutdown` can leave the emulator stopped. A future host
harness must impose a finite watchdog, assert serial outcomes, capture errors
and clean up the process. QEMU's exit status alone cannot establish M1.

## Compatibility work and next artifacts

| Priority | Requirement | Generic x86-64 work to finish | Acceptance artifact |
| --- | --- | --- | --- |
| First | R01 boot | Pin firmware/bootloader handoff; normalize memory reservations and ACPI roots; validate CPU features and long-mode entry ownership | Reset-to-ring-0 trace, immutable boot snapshot, malformed-handoff tests |
| First | R02 build | Pin ELF64/AMD64 and assembly/compiler conventions; stack alignment, red-zone policy, code model and FP/SIMD restrictions | Link map, dependency census, two matching clean builds |
| First | R03 protection | Define GDT/IDT/TSS and stack ownership, page permissions, exception frames and validated ring-3 return | User-mode CLI plus negative access/return and register-leak tests |
| First | R04–R05 console/time | Select serial resources, interrupt routing, monotonic clock and calibrated timer path | Interactive help/version/uptime, idle timer progress and non-yielding child preemption |
| Next | R07/R12/R13 lifecycle and recovery | Integrate local translation invalidation with close/reuse, test interrupt races and independent budgets | Repeated restart/resource traces and model checks |
| After single-CPU proof | R17 SMP/NUMA | AP startup, per-CPU state, IPIs, stop acknowledgement, TLB shootdown and topology | Two-CPU races first; sockets/SMT/NUMA only as needed |
| When DMA enters scope | R16 devices | Actual chipset/device manuals and vendor-specific remapping/reset semantics | Device-specific quiescence and buffer-reuse evidence |

The [Intel system-programming study](../../30-sources/intel-2026-system-programming-documentation.md)
is the primary architecture reference for the first backend. Before coding
entry, paging, APIC, timers or MSRs, qualify the exact sequences against the
relevant Intel SDM sections and discover required facilities at runtime. A
physical fixture may also require its processor-family specification update
and errata; those fixture-specific inputs do not redefine the generic backend.

The [ACPI study](../../30-sources/uefi-forum-2025-acpi-6-6.md) supplies platform
discovery context; actual tables and firmware revisions still require
inspection. The kernel remains responsible for validating those descriptions.
For later DMA isolation, investigate the chipset/IOMMU capabilities, firmware
DMAR description, requester paths and device reset rules of each claimed
fixture; do not assume modern VT-d features or working isolation from a CPU or
product-family name.

BEAM loading, actor semantics, process-local GC, bounded IPC, authority,
accounting and supervision keep their requirements. Retarget their native
adapter and context implementation, not their language semantics. Deferred
durability, networking, authentication and updates remain separate gates.

## Qualification ladder and staged tests

Run the first QEMU CLI test with one CPU and 64 MiB. This is the reproducible
baseline, not the whole compatibility claim. As Kay OS implements relevant
discovery or fallback behavior, add independently named and pinned matrix rows
that vary one or more of CPU feature profile, machine/chipset, memory size,
firmware path, topology and device layout. Every row records whether it is
expected to pass, fail as unsupported, or exercise a degraded path. A matrix
row cannot be added after observing its result merely to turn a failure into a
pass.

After virtual acceptance, qualify physical fixtures one at a time. Before a
physical boot, collect a read-only external observation record with CPU,
firmware, memory and relevant device facts, redacting unique identifiers. Kay
OS must independently emit its own discovered-hardware report during boot.
Compare the two records and investigate discrepancies; the external inventory
is a test oracle and safety aid, not kernel input.

The T7500 may serve as P1 when access, boot media and debug recovery are ready.
Future fixtures should be selected for diversity in CPU generation, chipset,
firmware mode, topology and devices. A single-CPU physical CLI boot need not
wait for SMP or a second ISA. Additional physical CPUs must remain unstarted or
safely parked under the chosen bootloader/kernel contract, not physically
removed. Nothing here authorizes a firmware update, settings change or disk
write.

Keep M2–M4 single-CPU. Then add two virtual CPUs on one socket, followed by a
separate two-socket test if it exercises a required path. Add explicit NUMA
memory/node relationships only for a NUMA test: sockets do not automatically
define NUMA, and virtual topology does not pin host threads to physical CPUs.
Match a fixture's full topology only after its observation record and the
small-SMP tests. Second-ISA portability remains later work without a selected
second architecture.

## Evidence status and connections

QEMU 8.2.2, `pc-q35-8.2`, `Nehalem-v1`, and SeaBIOS 1.16.3 availability and
hashes were checked on 2026-09-17. The executable verifier lives in the
[Kay OS implementation repository](https://github.com/pcharbon70/kay-os).
No guest launch or physical qualification was performed, and no boot, timing,
containment or conformance result is claimed. The generic envelope and minimal
baseline narrow M0; runtime discovery, a compatibility matrix and later
physical evidence remain open.

- [Requirements inventory](README.md) maps all nineteen requirement groups.
- [Boot contract](target-firmware-and-boot-handoff.md) and [user return](privilege-entry-memory-and-user-return.md) own first-entry responsibilities.
- [Multicore study](multicore-and-platform-portability.md) owns later concurrency gates.
- [Target-correction journal](../../50-journal/2026-09-06-t7500-target-correction.md) records the correction and checks.
