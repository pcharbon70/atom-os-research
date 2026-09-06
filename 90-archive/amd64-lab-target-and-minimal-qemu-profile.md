---
title: "Superseded AMD lab target and minimal QEMU profile"
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
  - "Superseded AMD processor assumption"
---

# Superseded AMD lab target and minimal QEMU profile

## Superseded by explicit user correction

Archived on 2026-09-06. The user confirmed the **Dell Precision T7500 and its
Intel Xeon x86-64 architecture**; the AMD-processor assumption was wrong.
The [T7500 target specification](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
replaces this document. The former Opteron fixture and AMD-manual dependency
below are inactive. The term AMD64 remains valid in shared ISA/ABI names;
it does not identify this machine's processor vendor.

The original body is retained as decision history, not current instructions.
Its linked JSON is a live configuration record and now follows the Intel
profile; the embedded launch example below preserves the superseded intent.

## Decision and scope

The active research and first implementation target is **AMD64/x86-64**, based
on the user's available lab architecture. This replaces the provisional
RV64/QEMU virt/Sv39/OpenSBI path in the readiness assessment and requirement
studies. RISC-V and Arm research remains useful comparative evidence, not a
prerequisite or active first-port commitment.

The first delivery remains a minimal bootable OS with a native ring-3 CLI and
an Atom-owned ring-0 kernel. The completed M0–M4 proof still requires the
project's compiled-BEAM compatibility profile and automatic process-local
tracing GC outside the kernel. AtomVM, graphics, desktop work, networking and
writable storage do not enter the minimum boot test.

The preceding hardware discussion selected a Dell Precision T7500. That
platform uses Intel Xeons, which implement the x86-64 architecture; it is not
an AMD-processor motherboard. The user's subsequent AMD x86-64 direction
settles the ISA, but does not identify an AMD CPU or board. Preserve the
[Dell platform reference](../20-notes/proof-of-concept-requirements/dell-precision-t7500-platform-reference.md) pending
clarification rather than silently relabeling its processors as AMD or
inventing an AMD replacement.

**Confirmed:** architecture and CLI-first scope. **User-reported but not
inventoried:** two multicore processor packages in the earlier machine
discussion. **Unresolved:** whether that is the current lab target, exact
CPU vendor/model/stepping, motherboard, firmware mode, RAM, NUMA, serial path
and device IDs. None is inferred from this checkout's development host.

## Minimal execution profile

These are adopted test constraints and implementation proposals, not results
from a booted guest.

| Area | Initial constraint | Evidence still required |
| --- | --- | --- |
| ISA and privilege | 64-bit AMD64; kernel CPL 0, native services CPL 3 | Actual entry state, CPUID feature record and ring-transition trace |
| Memory | Four-level paging and 4 KiB base pages as the initial design; 128 MiB guest RAM | Entry/allocator layout, reserved ranges, NX availability and enforced permissions |
| CPU use | One executing logical CPU; one virtual socket/core/thread | Timer/context tests before enabling concurrency |
| Firmware | Explicit SeaBIOS for the minimal QEMU fixture | Pin firmware and bootloader; separately discover the physical firmware path |
| Native images | Static, little-endian ELF64/AMD64 subset proposed | Toolchain, linker, calling convention, helper census and loader tests |
| I/O | Explicit emulated serial, headless display, no NIC or writable data disk | Bounded serial input/output and unattended test harness |
| Runtime | Independent user-space interpreter and process-local tracing GC | Compiled fixtures, feature closure and guest conformance tests |

Do not turn optional modern facilities into baseline requirements: AVX/AVX2,
five-level paging, PCID, x2APIC, TSC-deadline, SVM, SEV or an IOMMU all need
separate discovery and justification. Availability in a manual or a QEMU
model is not proof of availability or enablement on the lab CPU.

The [AMD64 psABI study](../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md)
separates the baseline from later microarchitecture levels. A full ordinary
AMD64 procedure environment includes floating-point/SIMD expectations. An
integer-only bring-up must therefore be an explicitly restricted native
profile, with generated-code checks and rejected unsupported use; it must not
claim full psABI execution support merely because pointers are 64-bit.
Implement initialized, isolated context ownership before admitting additional
register state.

## QEMU configuration intent

The [JSON record](../assets/qemu-minimal-x86-64.json) records project intent.
It is **not QEMU's `-readconfig` format**, an implemented launcher, or a
qualified run manifest.

Use `qemu-system-x86_64`, a pinned versioned `pc-q35-...` machine and TCG.
Start with `Opteron_G1-v1` as a conservative AMD-family instruction fixture,
not a claim that the lab contains an Opteron. The named model is listed in
[QEMU's CPU/configuration documentation](../30-sources/qemu-project-2026-x86-pc-test-configuration.md).
Its availability and required features must be checked in the chosen binary
before accepting a run. Do not silently substitute `max`, `host` or a
different CPU when a feature is missing.

Q35 is a synthetic PC fixture, not an AMD motherboard or a T7500 replica.
Its chipset and boot-media controller do not validate the physical storage,
network or interrupt wiring. TCG keeps initial execution independent of
host-vendor hardware acceleration. KVM/host passthrough can be a separately
recorded later acceleration profile, not the reproducible baseline.

An eventual launch template, **not executed here**, is:

```bash
qemu-system-x86_64 \
  -machine "${ATOM_QEMU_MACHINE:?set the pinned versioned pc-q35 machine}" \
  -accel tcg \
  -cpu Opteron_G1-v1 \
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

| Priority | Requirement | AMD64-specific work to finish | Acceptance artifact |
| --- | --- | --- | --- |
| First | R01 boot | Pin firmware/bootloader handoff; normalize memory reservations and ACPI roots; validate CPU features and long-mode entry ownership | Reset-to-ring-0 trace, immutable boot snapshot, malformed-handoff tests |
| First | R02 build | Pin ELF64/AMD64 and assembly/compiler conventions; stack alignment, red-zone policy, code model and FP/SIMD restrictions | Link map, dependency census, two matching clean builds |
| First | R03 protection | Define GDT/IDT/TSS and stack ownership, page permissions, exception frames and validated ring-3 return | User-mode CLI plus negative access/return and register-leak tests |
| First | R04–R05 console/time | Select serial resources, interrupt routing, monotonic clock and calibrated timer path | Interactive help/version/uptime, idle timer progress and non-yielding child preemption |
| Next | R07/R12/R13 lifecycle and recovery | Integrate local translation invalidation with close/reuse, test interrupt races and independent budgets | Repeated restart/resource traces and model checks |
| After single-CPU proof | R17 SMP/NUMA | AP startup, per-CPU state, IPIs, stop acknowledgement, TLB shootdown and topology | Two-CPU races first; sockets/SMT/NUMA only as needed |
| When DMA enters scope | R16 devices | Actual chipset/device manuals and vendor-specific remapping/reset semantics | Device-specific quiescence and buffer-reuse evidence |

[AMD's system-programming manual record](../30-sources/amd-2026-amd64-system-programming-manual.md)
is the primary reading target for AMD-specific implementation detail. Its
current catalog metadata was located, but the full text could not be retrieved
in this session. Before coding entry, paging, APIC or MSR paths, obtain the
manual and applicable processor-family programming reference and errata.
Do not treat this retargeting pass as that completed audit.

The existing [Intel system-programming study](../30-sources/intel-2026-system-programming-documentation.md)
provides common x86-64 context and remains relevant if the T7500 is retained.
It does not establish AMD-specific MSR, exception, timer or IOMMU behavior.
The [ACPI study](../30-sources/uefi-forum-2025-acpi-6-6.md) supplies the
platform-description context; actual tables and firmware revisions still
require inspection. The kernel remains responsible for validating and using
those descriptions.

BEAM loading, actor semantics, process-local GC, bounded IPC, authority,
accounting and supervision keep their requirements. Retarget their native
adapter and context implementation, not their language semantics. Deferred
durability, networking, authentication and updates remain separate gates.

## Lab qualification and staged tests

First obtain the actual CPU and motherboard identity. On that machine, use
read-only inventory such as `lscpu`, `lscpu -e` and `lspci -nn` if a
Linux environment is available. Record firmware version and boot mode,
memory distribution, CPU feature output, ACPI table identities, and available
serial/debug transport. Redact service tags and other unique identifiers from
public notes. Firmware menus may be inspected; no firmware update, settings
change or disk write is authorized by this research decision.

Run the first QEMU CLI test with one CPU and 128 MiB, increasing memory only
if measured image/allocator requirements justify a recorded change. A
single-CPU physical CLI boot should follow virtual bring-up once the machine
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
boot, timing, containment or conformance result is claimed. Architecture
selection narrows M0; exact binary identities, ABI and executable evidence
remain open.

- [Requirements inventory](../20-notes/proof-of-concept-requirements/README.md) maps all nineteen requirement groups.
- [Boot contract](../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) and [user return](../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md) own first-entry responsibilities.
- [Multicore study](../20-notes/proof-of-concept-requirements/multicore-and-platform-portability.md) owns later concurrency gates.
- [Retargeting journal](../50-journal/2026-09-06-amd64-retargeting-deep-dive.md) records decision order, sources and checks.
