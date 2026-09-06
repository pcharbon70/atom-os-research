---
title: "Dell Precision T7500 platform reference"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - hardware-profile
  - proof-of-concept
  - x86-64
aliases: []
---

# Dell Precision T7500 platform reference

## Status and provenance

The user has explicitly confirmed the **Dell Precision T7500** as the initial
physical target and corrected the intervening AMD-processor assumption.
The [T7500 target and QEMU profile](dell-precision-t7500-target-and-minimal-qemu-profile.md)
controls implementation planning.

This reference records the selected platform's manufacturer specifications:
Intel Xeon processors, Intel 5520 chipset and Intel 64/x86-64 architecture.
Machine selection is settled. Installed CPU models, enabled topology, memory,
firmware and devices still require inventory; published options are not proof
of what is fitted to this unit.

## Physical platform specification

| Item | Documented platform capability | Project-unit status |
| --- | --- | --- |
| CPU family | Intel Xeon 5500; later offerings include 5600 | Two multicore CPUs reported; exact models unverified |
| Topology | Dual-processor capable; second processor on an optional riser | Socket/core/thread layout must be inventoried |
| Chipset | Intel 5520 | Board revision and PCI IDs unverified |
| Memory | DDR3 ECC, three channels per processor; six base and six riser DIMM slots; up to 192 GB in qualified configurations | Installed capacity, speed and distribution unknown |
| Console | Native serial connector, PS/2, USB 2.0 | Serial enablement, address/IRQ and cable path unverified |
| Storage | LSI 1068e SAS/SATA; optional PERC 6/i | Controller and attached disks unverified |
| Network | Gigabit Ethernet; later sheet identifies Broadcom 5761 | Verify PCI ID; older guide also names 5754 |
| Expansion/power | Two PCIe 2.0 x16 graphics slots; 1100 W supply rating | Installed cards and hardware health unverified |

Evidence: [later specification sheet](../../30-sources/dell-2026-precision-t7500-specification-sheet.md),
[original technical guide](../../30-sources/dell-2026-precision-t5500-t7500-technical-guide.md)
and [service manual](../../30-sources/dell-2026-precision-t7500-service-manual.md).
Maximums are manufacturer configuration claims, not Atom capacity results.

[Dell's A18 release](../../30-sources/dell-2018-precision-t7500-bios-a18.md)
is dated 2018-11-02. The installed version is unknown. This decision does not
authorize flashing firmware, changing BIOS settings or writing physical disks.

The actual firmware boot modes require inspection. Neither a generic Dell
firmware-update instruction nor the processor ISA establishes UEFI support
or its absence on this unit.

## Required installed-unit inventory

Record exact CPU models and enabled threads, motherboard revision, populated
DIMMs and memory distribution, firmware revision/mode, PCI vendor/device IDs,
serial enablement and connector/cable path. The user reported two multicore
packages; no physical inspection or command output has verified that topology.

A18's publication is not evidence that it is installed or should be flashed.
The maximum memory and power-supply rating are manufacturer specifications,
not recommended first-test allocations or measured consumption. The first
virtual test remains one CPU and 128 MiB under the active profile.

## Connections

- [T7500 target and minimum tests](dell-precision-t7500-target-and-minimal-qemu-profile.md) separates ISA, emulator fixture and physical inventory.
- [Target-correction journal](../../50-journal/2026-09-06-t7500-target-correction.md) records the confirmed machine and supersession.
