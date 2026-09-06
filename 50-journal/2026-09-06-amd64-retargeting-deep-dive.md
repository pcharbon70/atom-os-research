---
title: "AMD64 target retargeting and minimum QEMU research"
kind: journal
created: "2026-09-06"
tags:
  - boot
  - hardware-profile
  - proof-of-concept
  - research-session
  - x86-64
aliases: []
---

# AMD64 target retargeting and minimum QEMU research

## Subsequent correction

After this session, the user confirmed the Dell Precision T7500 and stated
that the AMD assumption was wrong. The [target-correction journal](2026-09-06-t7500-target-correction.md)
and [current T7500 specification](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
supersede the target choice below. This session's original findings, failed
retrievals and source-introduction manifest remain historical evidence. Its
linked JSON record has since been updated; the archived profile retains the
former launch template.

## Question and scope

How should the active CLI-first proof of concept use the available AMD64 lab
architecture, starting with the smallest useful virtual tests?

This is a focused target-decision and configuration research session, not a
new systematic OS survey or implementation experiment. It follows the
[requirements deep dive](2026-09-06-proof-of-concept-requirements-deep-dive.md);
that earlier session's RV64 hypothesis remains historical evidence rather
than being rewritten as an AMD64 result.

## Decision sequence and evidence boundary

1. The user asked to record the Dell Precision T7500 as the initial physical
   machine and start QEMU with minimum resources.
2. Manufacturer evidence was recorded and an uncommitted target draft prepared.
3. During the work, the user directed research toward AMD x86-64, identifying
   that as the available lab architecture.
4. The active decision became AMD64/x86-64. The Dell facts were consolidated
   into a platform reference; no manufacturer facts or prior research were
   discarded. The T7500 uses Intel Xeons, so whether the newer direction
   means its compatible ISA or another AMD machine remains an explicit
   clarification rather than an invented hardware fact.

The resulting [AMD64 specification](../90-archive/amd64-lab-target-and-minimal-qemu-profile.md)
and [configuration intent](../assets/qemu-minimal-x86-64.json) adopt one vCPU,
128 MiB, TCG, a versioned q35-family fixture to pin later, an Opteron_G1-v1
instruction fixture, explicit SeaBIOS and serial I/O. This neither identifies
the lab CPU nor emulates its complete motherboard. Firmware, bootloader,
executable and image hashes remain unset.

The [Dell reference](../20-notes/proof-of-concept-requirements/dell-precision-t7500-platform-reference.md)
retains the originally researched CPU generations, optional second-CPU riser,
memory, serial and device options, and catalog-versus-installed distinctions.
The previous Nehalem-oriented draft is not an active QEMU baseline.

## Research method and retrieval limits

Read Dell's two-page later specification sheet, relevant CPU/memory/device
tables in the original 37-page technical guide, the service manual's
configuration/setup/specification sections, and the A18 driver release
record. Distinguish 5500-era from 5600-era options; preserve the conflicting
Broadcom model references and require actual PCI inventory. No BIOS update
or firmware-mode capability was inferred from generic installation text.

Read QEMU's invocation, CPU-model and PC documentation for machine versions,
CPU naming, explicit topology, serial/default devices, boot selection and
shutdown behavior. The moving documentation is not an executable version pin.
The QEMU PC page identifies SeaBIOS; direct SeaBIOS site retrieval failed.

Read the AMD64 psABI project's low-level source sections for baseline feature
levels, LP64, register conventions and stack/red-zone obligations. Record a
restricted integer-only bring-up separately from full ordinary ABI support.

Located AMD's indexed official Volume 2 catalog, publication 24593 revision
3.44, release date 2026-03-06. The catalog and content endpoint returned 404 on
direct access, confirmed with an independent HTTP request. The older TechDocs
path redirected to the documentation hub. Only bibliographic metadata was
available; no detailed AMD manual section was represented as read. Obtaining
readable official text plus the actual CPU's family documentation and errata
is a priority before architecture-sensitive implementation.

Reused the existing Intel system-programming and ACPI source records for
common x86 and platform-description context. This session did not re-audit
their complete manuals, and Intel-specific mechanisms are not attributed to
AMD. An attempted direct ACPI section retrieval also failed.

## Resulting research changes

The active readiness assessment, requirement inventory, PoC map and inquiry,
home navigation, repository direction, and hardware-layer entry points now
lead with AMD64. Hardware-facing requirement studies replace active
SBI/Sv39/hart/U-mode/S-mode assumptions with a ring-0/ring-3 AMD64 contract,
explicit firmware/bootloader discovery, native ABI, paging, timer and
single-CPU lifecycle obligations.

Existing papers and RISC-V/Arm examples remain useful comparisons. The
architecture-wide inquiries retain broader portability criteria; these are
not new blockers for the first AMD64 CLI. BEAM compatibility, automatic
process-local tracing GC, bounded IPC and independent recovery are unchanged.
AtomVM and desktop scope remain excluded.

Physical single-CPU bring-up may follow the virtual CLI once the machine and
boot medium are qualified. SMP, multiple virtual sockets and NUMA are distinct
later tests; full topology must come from inventory, not guessed core counts.

## Local checks and reproducibility

The archive has no bootable kernel image, and
`command -v qemu-system-x86_64` returned exit status 1: no executable was
available on PATH. No QEMU package was installed and no VM was launched.
This is an environment observation, not proof that QEMU is absent from every
location on the host.

Handoff checks:

- JSON syntax and agreement with the documented CPU, RAM, topology, serial
  and exclusion settings passed; this is not QEMU execution qualification.
- `python3 validate_archive.py` passed: 503 completed documents, 19
  directories, 4,787 local links and 320 source notes; 19 deep-dive manifests
  classify 308 introduced and 343 reused source uses, with 12 source notes
  introduced outside a deep-dive manifest.
- `git diff --check` passed. New-file whitespace checks were also run
  separately because ordinary Git diff does not include untracked files.
- The 27 existing files changed in this session were compared with the
  initial dirty-tree snapshot; no unexpected content drift was found.
- Active PoC guidance was searched for superseded RISC-V instructions.
  Remaining references describe history or comparisons, not a first port.

No firmware flash, BIOS configuration change, physical disk write, hardware
inventory, kernel build, boot trace or conformance test occurred. The virtual
host/emulator/firmware/bootloader remain trusted, and the intended kernel/user
boundary is CPL 0/CPL 3. No isolation from the host or SMM, physical timing,
DMA containment or multicore correctness is established.

## Source manifest

### Newly introduced sources

- [Dell T7500 specification sheet](../30-sources/dell-2026-precision-t7500-specification-sheet.md) — later CPU/memory/device platform capabilities, not the installed inventory.
- [Dell T5500/T7500 technical guide](../30-sources/dell-2026-precision-t5500-t7500-technical-guide.md) — original-generation configurations and contradictory NIC identifiers.
- [Dell T7500 service manual](../30-sources/dell-2026-precision-t7500-service-manual.md) — optional riser, physical resources and setup inspection context.
- [Dell T7500 BIOS A18](../30-sources/dell-2018-precision-t7500-bios-a18.md) — release identity, distinguished from installed firmware and update authority.
- [QEMU x86 PC configuration](../30-sources/qemu-project-2026-x86-pc-test-configuration.md) — explicit virtual fixture controls and CPU-model/topology limitations.
- [AMD64 system-programming manual discovery](../30-sources/amd-2026-amd64-system-programming-manual.md) — catalog metadata and failed full-text retrieval; not detailed architecture evidence.
- [AMD64 procedure ABI](../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md) — baseline versus later feature levels, native context and stack obligations.

### Reused sources

- [Intel system-programming study](../30-sources/intel-2026-system-programming-documentation.md) — existing common x86-64 context, not AMD-specific implementation authority.
- [ACPI 6.6 study](../30-sources/uefi-forum-2025-acpi-6-6.md) — existing platform-description and discovery context.

## Follow-ups

Identify the actual CPU/board and firmware; retrieve and read the AMD manual
and processor-family errata; then pin the bootloader/native ABI and execute
the first entry, serial and timer tests. M0–M4 remain open.

Changes are local and uncommitted. Previous unrelated archive changes are
preserved; no commit, push or publication was requested.
