---
title: "Target, firmware, and boot handoff"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - boot
  - proof-of-concept
  - requirements
aliases: []
---

# Target, firmware, and boot handoff

Requirement R01, M0–M1. Establish a reproducible path from reset to an
Atom-owned Intel x86-64 ring-0 kernel and then a ring-3 CLI. The
[active lab/QEMU profile](dell-precision-t7500-target-and-minimal-qemu-profile.md)
selects the Dell Precision T7500 and supersedes the earlier RV64/OpenSBI
proposal and AMD-processor assumption. Begin with one virtual CPU, 128 MiB
and serial I/O; installed-unit inventory and binary pins remain unconfirmed.

## Evidence and alternatives

[QEMU's PC configuration study](../../30-sources/qemu-project-2026-x86-pc-test-configuration.md)
supports an explicit machine, CPU, firmware and device fixture. It does not
establish fidelity to the selected T7500's complete chipset or firmware.

The [Intel system-programming study](../../30-sources/intel-2026-system-programming-documentation.md)
is the primary architecture reference for the selected Xeon platform.
It identifies long-mode, descriptor, interrupt, translation and context
concerns. Qualify exact SDM sequences and CPU-family errata before coding;
modern documented features are not automatically available on this T7500.
The former AMD-manual audit is no longer a first-target dependency.

The [ACPI study](../../30-sources/uefi-forum-2025-acpi-6-6.md) supplies the
platform-description context. Firmware memory maps, ACPI and CPUID serve
different purposes; no one replaces the others. A table is a claim to validate,
not proof that hardware routing agrees.

The earlier [QEMU RISC-V](../../30-sources/qemu-project-2026-risc-v-virt-platform.md),
[OpenSBI](../../30-sources/opensbi-project-2026-firmware-handoff.md) and
[Devicetree](../../30-sources/devicetree-org-2023-devicetree-specification-0-4.md)
work remains comparative research. SBI, hart IDs, Sv39 and a mandatory DTB are
not the T7500 first-boot contract.

## Proposed boot contract

Freeze the QEMU binary, versioned machine, CPU/features, accelerator, topology,
RAM, serial backend, firmware hash, bootloader/version/protocol and image
hashes. SeaBIOS is the initial virtual fixture; do not infer physical BIOS or
UEFI support from the ISA. Select a BIOS-compatible loader for that fixture,
or explicitly revise the firmware fixture after qualifying the actual board.
A bootloader may establish long mode; record that ownership rather than
assuming reset enters a 64-bit C function.

The first assembly entry establishes a known aligned stack and documented
register convention before compiled code. Confirm CPU support and entry mode.
Copy or pin every retained handoff byte before allocation. Normalize usable
RAM, reserved and firmware ranges, kernel/service images, ACPI roots,
CPU/features, serial resources and interrupt/timer descriptions into an
immutable bounded snapshot. Unknown or conflicting ranges stay unavailable.

Validate handoff sizes, version, alignment, pointer ranges, interval arithmetic
and overlap. Validate applicable ACPI lengths and checksums before following
tables; impose maximum size and table count and reject cycles or conflicting
mandatory records. Use a limited table set, including the interrupt-controller
description when needed; SRAT/SLIT NUMA work can follow later. Do not add a
general AML interpreter merely to display the first prompt. Actual device
resources must come from the qualified fixture/platform contract, not guessed
addresses copied from a RISC-V tutorial.

Initialize or deliberately replace descriptor tables, exception entry,
page tables and CPU-local state before relying on them. The initial design
uses four-level paging with 4 KiB pages, ring 0 and ring 3, and one executing
CPU. Reserve bootloader/firmware memory until the selected handoff explicitly
permits reclamation. Do not require optional PCID, x2APIC or advanced timer
features without detection.

## Trust and failure boundary

The virtual test trusts the host, QEMU, firmware, bootloader and build inputs.
Atom owns guest protection after handoff, not isolation from its host.
On physical hardware, firmware and system-management facilities remain
outside ordinary kernel control and part of the trust assumptions. Firmware
is not described using RISC-V machine/supervisor privilege terminology.

Before normal fault delivery exists, boot failure emits a bounded diagnostic
and reaches a finite halt/reset path. Never continue using guessed RAM.
Keep additional physical CPUs unstarted or safely parked under the chosen
handoff contract; one vCPU does not validate that physical startup behavior.

## Acceptance and next experiment

1. Trace reset, firmware/loader handoff, ring-0 entry and first ring-3 return,
   retaining exact image identities and privilege evidence.
2. Compare normalized reservations against firmware/image layout and probe
   allocator boundaries without freeing unknown ranges.
3. Fuzz the selected handoff and table parser in a hosted harness, then test
   selected malformed records in the guest.
4. Change guest RAM or CPU features and require validated discovery or a
   clear unsupported-configuration failure.
5. Reproduce from a clean artifact bundle with no hidden guest host-OS services.

The next artifact is a pinned boot record plus a reset-to-entry trace.
Board and architecture selection are complete; bootloader, ABI, address layout and
successful execution are not. A qualified single-CPU physical CLI test can
follow virtual M1 without waiting for SMP or a second ISA.

## Connections

[Freestanding images](freestanding-build-and-static-images.md) defines the
payload. [Protected user return](privilege-entry-memory-and-user-return.md)
completes the transition to the CLI. The broader
[boot-handoff component](../kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md)
retains multi-protocol goals beyond this first target.
