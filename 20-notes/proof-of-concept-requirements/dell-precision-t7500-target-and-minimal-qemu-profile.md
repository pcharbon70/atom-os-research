---
title: "Dell Precision T7500 target and minimal QEMU profile"
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
---

# Dell Precision T7500 target and minimal QEMU profile

## Decision and scope

The initial physical target is specifically the **Dell Precision T7500**,
using **Intel Xeon processors and Intel 64/x86-64**. The user explicitly
corrected the intervening AMD-processor assumption. This decision supersedes
both that [archived detour](../../90-archive/amd64-lab-target-and-minimal-qemu-profile.md)
and the earlier provisional RV64/QEMU virt/Sv39/OpenSBI path.

The [platform reference](dell-precision-t7500-platform-reference.md) records
Dell's Xeon 5500-era and later 5600-era options, Intel 5520 chipset, memory,
serial and device capabilities. The exact installed Xeon models are unknown;
do not infer cores, enabled Hyper-Threading or feature bits from the T7500
name alone. Two multicore processor packages are user-reported, not yet
verified by a physical inventory.

**Confirmed:** T7500 model, Intel processor platform, x86-64 architecture and
CLI-first scope. **Still unverified:** CPU SKUs/steppings and enabled topology,
motherboard revision, BIOS version/mode, installed RAM/NUMA, serial settings
and device IDs. The target is no longer ambiguous; only its installed
configuration remains to be recorded.

The first delivery remains a minimal bootable OS with a native ring-3 CLI and
an Atom-owned ring-0 kernel. The completed M0–M4 proof still requires the
project's compiled-BEAM profile and automatic process-local tracing GC outside
the kernel. AtomVM, graphics, desktop work, networking and writable storage
do not enter the minimum boot test.

“AMD64” in an ELF machine identifier or the System V AMD64 ABI is a shared
architecture/ABI name, not a requirement for an AMD processor. Those valid
technical references remain; AMD-specific MSRs, SVM/SEV, AMD IOMMU and AMD
processor-family research do not gate this Intel target.

## Minimal execution profile

These are adopted test constraints and implementation proposals, not results
from a booted guest.

| Area | Initial constraint | Evidence still required |
| --- | --- | --- |
| ISA and privilege | Intel 64/x86-64; kernel CPL 0, native services CPL 3 | Actual entry state, CPUID feature record and ring-transition trace |
| Memory | Four-level paging and 4 KiB base pages as the initial design; 128 MiB guest RAM | Entry/allocator layout, reserved ranges, NX availability and enforced permissions |
| CPU use | One executing logical CPU; one virtual socket/core/thread | Timer/context tests before enabling concurrency |
| Firmware | Explicit SeaBIOS for the minimal QEMU fixture | Pin firmware and bootloader; separately discover the physical firmware path |
| Native images | Static, little-endian ELF64/AMD64 subset proposed | Toolchain, linker, calling convention, helper census and loader tests |
| I/O | Explicit emulated serial, headless display, no NIC or writable data disk | Bounded serial input/output and unattended test harness |
| Runtime | Independent user-space interpreter and process-local tracing GC | Compiled fixtures, feature closure and guest conformance tests |

Do not require later-generation features such as AVX/AVX2 or five-level
paging on this older platform. PCID, x2APIC, timer modes, extended-state
facilities and VT-d must be qualified against the installed CPUs, chipset
and firmware before use. Intel virtualization support is not a first-boot
dependency. A modern Intel manual is not evidence that the T7500 implements
every feature it describes.

The [AMD64 psABI study](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md)
separates the baseline from later microarchitecture levels. A full ordinary
AMD64 procedure environment includes floating-point/SIMD expectations. An
integer-only bring-up must therefore be an explicitly restricted native
profile, with generated-code checks and rejected unsupported use; it must not
claim full psABI execution support merely because pointers are 64-bit.
Implement initialized, isolated context ownership before admitting additional
register state.

## QEMU configuration intent

The [JSON record](../../assets/qemu-minimal-x86-64.json) records project intent.
It is **not QEMU's `-readconfig` format**, an implemented launcher, or a
qualified run manifest.

Use `qemu-system-x86_64`, a pinned versioned `pc-q35-...` machine and TCG.
Start with `Nehalem-v1` as an older-generation Intel instruction fixture,
not an exact emulation of the installed Xeon SKU. This replaces the Opteron
model. The named model is listed in
[QEMU's CPU/configuration documentation](../../30-sources/qemu-project-2026-x86-pc-test-configuration.md).
Its availability and required features must be checked in the chosen binary
before accepting a run. Do not silently substitute `max`, `host` or a
different CPU when a feature is missing.

Q35 is a synthetic PC fixture, not a T7500/Intel 5520 motherboard replica.
Its chipset and boot-media controller do not validate the physical storage,
network or interrupt wiring. TCG keeps initial execution independent of
host-vendor hardware acceleration. KVM/host passthrough can be a separately
recorded later acceleration profile, not the reproducible baseline.

If inventory later identifies Xeon 5600 processors, a separately pinned
Westmere feature profile may be added for tests that require it. Do not
silently expand the baseline. First compare exposed CPUID features with the
actual CPU and keep compiler instruction selection within the agreed subset.

An eventual launch template, **not executed here**, is:

```bash
qemu-system-x86_64 \
  -machine "${ATOM_QEMU_MACHINE:?set the pinned versioned pc-q35 machine}" \
  -accel tcg \
  -cpu Nehalem-v1 \
  -smp 1,sockets=1,cores=1,threads=1 \
  -m 128M \
  -nodefaults \
  -display none \
  -monitor none \
  -serial stdio \
  -nic none \
  -bios "${ATOM_SEABIOS:?set the pinned SeaBIOS path}" \
  -drive "file=${ATOM_BOOT_ISO:?set the bootable ISO path},format=raw,if=ide,index=0,media=cdrom,readonly=on" \
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

## Research retargeting and next artifacts

| Priority | Requirement | T7500 / Intel x86-64 work to finish | Acceptance artifact |
| --- | --- | --- | --- |
| First | R01 boot | Pin firmware/bootloader handoff; normalize memory reservations and ACPI roots; validate CPU features and long-mode entry ownership | Reset-to-ring-0 trace, immutable boot snapshot, malformed-handoff tests |
| First | R02 build | Pin ELF64/AMD64 and assembly/compiler conventions; stack alignment, red-zone policy, code model and FP/SIMD restrictions | Link map, dependency census, two matching clean builds |
| First | R03 protection | Define GDT/IDT/TSS and stack ownership, page permissions, exception frames and validated ring-3 return | User-mode CLI plus negative access/return and register-leak tests |
| First | R04–R05 console/time | Select serial resources, interrupt routing, monotonic clock and calibrated timer path | Interactive help/version/uptime, idle timer progress and non-yielding child preemption |
| Next | R07/R12/R13 lifecycle and recovery | Integrate local translation invalidation with close/reuse, test interrupt races and independent budgets | Repeated restart/resource traces and model checks |
| After single-CPU proof | R17 SMP/NUMA | AP startup, per-CPU state, IPIs, stop acknowledgement, TLB shootdown and topology | Two-CPU races first; sockets/SMT/NUMA only as needed |
| When DMA enters scope | R16 devices | Actual chipset/device manuals and vendor-specific remapping/reset semantics | Device-specific quiescence and buffer-reuse evidence |

The [Intel system-programming study](../../30-sources/intel-2026-system-programming-documentation.md)
is now the primary architecture reference. Before coding entry, paging, APIC,
timers or MSRs, qualify the exact sequences against the relevant Intel SDM
sections and the installed Xeon family's specification updates/errata. This
correction is not a completed processor-specific audit. The earlier failed
AMD-manual retrieval is historical and no longer a blocker.

The [ACPI study](../../30-sources/uefi-forum-2025-acpi-6-6.md) supplies platform
discovery context; actual tables and firmware revisions still require
inspection. The kernel remains responsible for validating those descriptions.
For later DMA isolation, investigate the actual Intel 5520/VT-d capabilities,
firmware DMAR description, requester paths and device reset rules; do not
assume modern VT-d features or working isolation from the CPU family name.

BEAM loading, actor semantics, process-local GC, bounded IPC, authority,
accounting and supervision keep their requirements. Retarget their native
adapter and context implementation, not their language semantics. Deferred
durability, networking, authentication and updates remain separate gates.

## Lab qualification and staged tests

Inventory the selected T7500's CPU SKUs and motherboard revision. On that machine, use
read-only inventory such as `lscpu`, `lscpu -e` and `lspci -nn` if a
Linux environment is available. Record firmware version and boot mode,
memory distribution, CPU feature output, ACPI table identities, and available
serial/debug transport. Redact service tags and other unique identifiers from
public notes. Firmware menus may be inspected; no firmware update, settings
change or disk write is authorized by this research decision.

Run the first QEMU CLI test with one CPU and 128 MiB, increasing memory only
if measured image/allocator requirements justify a recorded change. A
single-CPU physical CLI boot on the T7500 should follow virtual bring-up once the machine
and boot media are qualified; it need not wait for SMP or a second ISA.
Additional physical CPUs must remain unstarted or safely parked under the
chosen bootloader/kernel contract, not physically removed.

Keep M2–M4 single-CPU. Then add two virtual CPUs on one socket, followed by a
separate two-socket test if it exercises a required path. Add explicit NUMA
memory/node relationships only for a NUMA test: sockets do not automatically
define NUMA, and virtual topology does not pin host threads to physical CPUs.
Match full lab topology only after inventory and the small-SMP tests.
Second-ISA portability remains later work without a selected second target.

## Evidence status and connections

No QEMU installation or guest launch was performed. No physical inventory,
boot, timing, containment or conformance result is claimed. Board and architecture
selection narrow M0; exact binary identities, ABI and executable evidence
remain open.

- [Requirements inventory](README.md) maps all nineteen requirement groups.
- [Boot contract](target-firmware-and-boot-handoff.md) and [user return](privilege-entry-memory-and-user-return.md) own first-entry responsibilities.
- [Multicore study](multicore-and-platform-portability.md) owns later concurrency gates.
- [Target-correction journal](../../50-journal/2026-09-06-t7500-target-correction.md) records the correction and checks.
