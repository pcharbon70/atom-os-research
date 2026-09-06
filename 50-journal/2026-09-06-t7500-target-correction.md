---
title: "Dell Precision T7500 target correction"
kind: journal
created: "2026-09-06"
tags:
  - hardware-profile
  - proof-of-concept
  - x86-64
aliases: []
---

# Dell Precision T7500 target correction

## Observations

The user explicitly confirmed the Dell Precision T7500 and its architecture,
stating that the AMD assumption was wrong. The initial physical machine is
therefore the Intel Xeon / Intel 64 (x86-64) T7500, not an unidentified AMD
motherboard. Two multicore processor packages remain user-reported;
installed SKUs, enabled cores/threads, board revision, memory, BIOS and device
IDs remain unverified.

The [active specification](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
now controls research and tests. Its
[manufacturer reference](../20-notes/proof-of-concept-requirements/dell-precision-t7500-platform-reference.md)
distinguishes supported configurations from installed-unit evidence.

The [former AMD target](../90-archive/amd64-lab-target-and-minimal-qemu-profile.md)
was moved to the archive with a supersession notice and repaired relative
links. The [previous session](2026-09-06-amd64-retargeting-deep-dive.md)
retains its original evidence and source-introduction manifest. No research
was deleted. Valid AMD64 ELF/ABI terminology remains applicable to Intel
x86-64; AMD-specific processor research no longer gates this target.

## Environment and configuration

The [configuration-intent JSON](../assets/qemu-minimal-x86-64.json) now names
the Dell Precision T7500 and Intel platform. Its minimum virtual profile is:

- `qemu-system-x86_64`, TCG, and a versioned q35 machine still to be pinned;
- `Nehalem-v1`, replacing the superseded `Opteron_G1-v1` fixture;
- one socket, one core, one thread and 128 MiB guest RAM;
- explicit SeaBIOS, serial console, no default graphics or NIC;
- a future read-only boot ISO, with no writable guest data disk.

Nehalem is a generation-level fixture, not the installed Xeon's exact model.
Q35 does not emulate the Intel 5520/T7500 chipset or its LSI controller.
QEMU topology is neither host affinity nor proof of physical NUMA behavior.
One-CPU physical CLI bring-up can follow virtual bring-up before SMP; full
topology is enabled only for tests that need it and after inventory.

No QEMU installation, guest launch, kernel build, hardware inventory,
firmware change or disk write occurred. Firmware/bootloader/binary hashes,
native ABI and run evidence remain open. The intended kernel and native
services use CPL 0 and CPL 3; firmware and the emulator host remain trusted
dependencies. CLI-first scope, AtomVM rejection, compiled BEAM and
unprivileged tracing GC are unchanged.

## Evidence and checks

Rechecked the official Dell specification sheet for the Intel platform and
QEMU's CPU-model documentation for Nehalem naming. Reused existing Intel
architecture research rather than claiming a new full SDM or Xeon errata
audit. This is a correction session, not a new architecture deep dive.

Updated the active readiness assessment, hardware-facing requirements,
hardware-layer entry points, inquiries, repository instructions and maps.
Directory inventories and incoming links were changed with the archived
profile. Prior unrelated changes were preserved against a fresh dirty-tree
snapshot.

Handoff validation passed:

- `python3 validate_archive.py`: 505 completed documents, 19 directories,
  4,810 local links and 320 source notes; the 19 existing deep-dive manifests
  still classify 308 introduced and 343 reused source uses.
- JSON syntax and eight profile assertions: selected machine/vendor,
  Nehalem command agreement, one CPU/128 MiB, topology product, reported
  versus verified package count, unresolved pins and minimal device settings.
- `git diff --check` and separate whitespace checks for the new/moved files.
- No stale incoming link to the former active profile remained. Active
  AMD mentions are shared ABI names or explicit supersession statements.
- Readback of the 36 affected/snapshotted files matched the intended changes;
  no unexpected content drift was found.

These are documentation/configuration checks, not a successful boot or
M0–M4 completion.

## Follow-ups

Inventory the selected T7500's exact Xeon SKUs, enabled topology, firmware,
memory and serial path. Then pin Intel SDM/processor-family references,
bootloader, toolchain and virtual artifacts and implement the first
single-CPU CLI tests. No AMD manual retrieval is required for that first
Intel backend.

Changes remain local and uncommitted; no publication was requested.
