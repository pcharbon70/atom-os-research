---
title: "2026-09-22 — M1 phase 01 execution record"
kind: journal
created: "2026-09-22"
tags:
  - implementation-evidence
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# 2026-09-22 — M1 phase 01 execution record

The clean Kay OS M1 Phase 1 gate passed all six registered guest boots. The
positive boot executed at CPL 0 after loading Kay-owned descriptor state and a
nonzero Kay CR3; negative boots halted with their exact bounded reasons. This
supports the kernel-entry, conservative-memory and discovery foundation only,
not a ring-3 program, interactive CLI, compatibility matrix or physical boot.

## Plan and acceptance baseline

The run implements [M1 Phase 1](../60-planning/01-proof-of-concept/m1-boot-to-cli/phase-01-kernel-entry-and-memory-foundation.md),
tasks `m1-p01-memory`, `m1-p01-discovery` and `m1-p01-integration`, following
accepted decision M1-D01. It contributes the startup portions of M1-T06,
M1-T07 and M1-T08 plus the discovery portion of M1-T09; it does not close those
whole milestone cases.

The versioned case manifest predeclared six unique cases, an eight-second boot
deadline, three-second cleanup deadline, 24 protocol-line maximum and 32,768
serial-byte maximum. The fixture was `pc-q35-8.2`, TCG, `Nehalem-v1`, one CPU,
64 MiB, SeaBIOS, read-only ISO and serial output. The predecessor was the
accepted M0 baseline at Kay OS merge `28408e8` and research merge `9c0653b`.

## Environment and provenance

- Implementation repository: `https://pushin.eu/pcharbon70/kay-os`.
- Section 1.1 implementation commit: `64740540e04b862336a70cc65a5dd02d1eb61240`.
- Clean tested integration commit: `4766582e5ddff36b141b8787a29569e31c76ace6`; dirty-file count `0`.
- Zig 0.16.0 SHA-256: `2317bbb91798556d9d0f38aabdac23db83f0979b25f767259ae474546724087c`.
- LLD: `21.1.0`.
- QEMU package: `1:8.2.2+ds-0ubuntu1.18`; executable SHA-256 `8a35ccba41582fc6c38b9df85fc9e35fa1d42f414d2d7d8090ee9b2f5e7c0854`.
- SeaBIOS package: `1.16.3-2`; image SHA-256 `4d597f68e06a0e28498e12e96e1f2ce64aee88a519685c61da92eb775c95a445`.
- Limine v12.9.0 archive SHA-256: `9a738586bff5790bd8bfef4a4868a2939cba3f81f22f121306d668c97f1c85d8`; detached signature SHA-256 `c2ece24344e8b59350d8e7d9b70ce46b71f2c0cda3668096c14ff83f1f773e3d`; fingerprint `05D29860D0A0668AAEFB9D691F3C021BECA23821`; signature valid.
- Host services built the ISO, ran QEMU, applied deadlines and captured output.
  The guest itself supplied the claimed ring-0 entry, descriptor, paging,
  memory and discovery behavior.

The exact command was:

```console
LD_LIBRARY_PATH=/tmp/kay-xorriso-root/usr/lib/x86_64-linux-gnu \
XORRISO=/tmp/kay-xorriso-root/usr/bin/xorriso \
python3 scripts/m1/verify-phase-01.py \
  /tmp/kay-m1-phase-01-evidence \
  /tmp/limine-binary-12.9.0.tar.xz \
  /tmp/limine-binary-12.9.0.tar.xz.sig
```

## Execution and results

| Task / case IDs | Fixture and exact command | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- | --- |
| `m1-p01-integration`; inherited M0 | Gate command above; baseline and M0 contract subprocesses | Pinned tools/firmware and inherited contract suite pass before guest cases | Exact tool hashes matched; signed Limine input verified; M0 Phase 2 contract verification passed | pass | [Environment](../assets/m1-phase-01/environment.txt) |
| `m1-p01-t01-entry-memory-discovery`; M1-T06/T07/T08/T09 discovery portions | Registered `normal` boot | Ordered six milestones, bounded reports, pass record, nonzero CR3 and Kay descriptor state | 19 map entries, 15,936 usable pages, one `GenuineIntel` logical CPU, ACPI RSDT/MADT with LAPIC/IOAPIC; CPL 0, HLT 1, TR `0018`, Kay GDT/IDT and CR3 `0x3f02000` | pass | [Serial](../assets/m1-phase-01/normal-serial.log), [registers](../assets/m1-phase-01/normal-registers.txt); original SHA-256 `10842bf6…` and `a13b040d…` |
| `m1-p01-n01-missing-memory-map`; M1-T07 portion | Registered `missing-memmap` boot | Stop before discovery-ready with exact missing-map reason | `failure last=descriptors reason=missing_memmap`; no pass | pass | [Transcript](../assets/m1-phase-01/missing-memmap-serial.log); original SHA-256 `2a68081c…` |
| `m1-p01-n02-memory-range-overflow`; M1-T07 portion | Registered `memmap-overflow` boot | Checked addition stops before ownership publication | `failure last=descriptors reason=range_overflow`; no pass | pass | [Transcript](../assets/m1-phase-01/memmap-overflow-serial.log); original SHA-256 `d2b8f8d5…` |
| `m1-p01-n03-overlapping-memory`; M1-T07 portion | Registered `memmap-overlap` boot | Ambiguous ownership stops before discovery-ready | `failure last=descriptors reason=injected_overlap`; no pass | pass | [Transcript](../assets/m1-phase-01/memmap-overlap-serial.log); original SHA-256 `83d60eb4…` |
| `m1-p01-n04-missing-cpu-feature`; M1-T06/T09 discovery portions | Registered `missing-cpuid` boot | Mandatory feature absence is explicit and terminal | `failure last=descriptors reason=missing_cpuid`; no pass | pass | [Transcript](../assets/m1-phase-01/missing-cpuid-serial.log); original SHA-256 `a1b3dcfc…` |
| `m1-p01-n05-invalid-acpi-checksum`; M1-T08/T09 discovery portions | Registered `bad-rsdp` boot | Firmware checksum rejection is explicit and terminal | `failure last=descriptors reason=rsdp_checksum`; no pass | pass | [Transcript](../assets/m1-phase-01/bad-rsdp-serial.log); original SHA-256 `f5f94106…` |

The aggregate [summary](../assets/m1-phase-01/summary.json) and
[case table](../assets/m1-phase-01/case-results.tsv) preserve the exact tested
revision and kernel/ISO hashes. The positive kernel was
`a918993ad791f41b79721dc09e71ba68b2b8f91d62db3275c0705795f84decce`;
its ISO was
`d9667f7db58f7dbc911415df95b3ff177d5f504800db4e0c97f44ea747a7edce`.
The retained text is newline-normalized; [its own hash manifest](../assets/m1-phase-01/retained.sha256)
does not replace the original evidence identities above.

## Review and handoff

Execution review found all predeclared Phase 1 children and failure paths
passing at a clean revision. The user/project owner had instructed that the
completed PRs be merged; under that conditional authorization, the handoff
decision is **proceed** to M1 Phase 2 after both repository PRs merge. No
failure is hidden and no full M1 acceptance case is claimed closed.

The tested revision is `4766582e5ddff36b141b8787a29569e31c76ace6`.
The implementation and research merge revisions do not yet exist in this
record and must not be inferred to have been retested. Reopen Phase 1 if the
Limine ABI, entry/descriptor layout, stack/table sizes, memory normalization,
CPUID/ACPI requirements, page-table construction, serial protocol, fixture or
registered cases change.

## Follow-ups

- Resolve M1-D02 before executing [Phase 2](../60-planning/01-proof-of-concept/m1-boot-to-cli/phase-02-protected-images-and-user-transitions.md).
- Add page permissions, user mappings, validated ring-3 entry/return and fault
  recovery evidence; Phase 1 mappings are deliberately writable/executable.
- Preserve the current boundary: no allocator release, interactive CLI,
  physical fixture, SMP, compatibility matrix, timer ownership or user-mode
  result has been demonstrated.
