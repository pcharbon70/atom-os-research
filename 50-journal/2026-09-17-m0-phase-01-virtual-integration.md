---
title: "2026-09-17 — M0 phase 01 virtual integration"
kind: journal
created: "2026-09-17"
tags:
  - implementation-planning
  - m0
  - proof-of-concept
  - qemu
  - zig
aliases: []
---

# 2026-09-17 — M0 phase 01 virtual integration

The M0 Phase 1 virtual-input gate assembled the selected tool/firmware baseline
and freestanding build closure under one finite driver. All nine registered
positive, negative and boundary cases passed on a clean implementation commit.
The run supports `m0-p01-integration`; it does not boot Kay OS, qualify the
physical T7500, close final M0, or supply the unassigned acceptance review.

## Plan and acceptance baseline

The governing [M0 Phase 1 plan](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md)
was at research revision `1af43bc`. That revision explicitly superseded the
unrun `m0-p01-inventory` task with Phase 3 task `m0-p03-inventory`, leaving
Phase 1 integration dependent only on `m0-p01-build`.

The implementation's `config/m0/phase-01-cases.json` declared task
`m0-p01-integration`, scope `virtual-input-and-build-integration`, nine cases,
no random workload, and deadlines of 30 seconds for baseline checks, 180
seconds for build closure, 10 seconds for QEMU rejection, and one second for
the watchdog probe. The case-manifest SHA-256 was
`83b01b41a7eafa210a698033b42d688ac7b15094a89075023d155e426733f4aa`.

The run contributes preliminary virtual evidence to M0-T01 and M0-T02. The
full cases remain open for later image/contract and final-M0 integration.

## Environment and provenance

- Implementation repository: [pcharbon70/kay-os](https://github.com/pcharbon70/kay-os)
- Tested implementation commit: `b350de962d7c4bfe237ed662549a5df101e1387f`
- Tested state: clean (`dirty_file_count=0`)
- Zig: 0.16.0 at `/home/ducky/.asdf/installs/zig/0.16.0/zig`
- QEMU: `/usr/bin/qemu-system-x86_64`, distribution version 8.2.2
- Virtual profile: `pc-q35-8.2`, `Nehalem-v1`, TCG, one CPU, 64 MiB,
  SeaBIOS 1.16.3, no network and no writable guest storage
- Host boundary: Linux supplied shell, deadlines, process execution, hashing,
  Git state and ELF inspection
- Guest/physical execution: none; the fixture ELF was built and inspected but
  not booted
- Generated evidence directory:
  `/tmp/kay-m0-phase-01-integration-b350de9`

Generated logs and binaries remained outside version control. The retained
artifact SHA-256 was
`e94b127fcc4388e73b4620a8b0908dcdeed0c3a08fbf0052d92cce58a3baf31a`;
the case-results TSV SHA-256 was
`9c88ef9f1f67c5de0a0054c75f5398c84f3811a6eb673ff392831678c5b9a794`.

## Execution and results

The exact invocation was:

```sh
ZIG=/home/ducky/.asdf/installs/zig/0.16.0/zig \
QEMU=/usr/bin/qemu-system-x86_64 \
  scripts/m0/verify-phase-01.sh \
  /tmp/kay-m0-phase-01-integration-b350de9
```

| Task / case IDs | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- |
| m0-p01-integration / m0-p01-t01-baseline | Exact Zig, LLD, QEMU, machine, CPU and SeaBIOS inputs resolve. | Baseline driver passed every version, path, package, hash, machine and CPU check. | pass | `baseline.log`; manifest hash above |
| m0-p01-integration / m0-p01-t02-clean-builds | Two absolute-path builds and normalized maps agree. | Nested build closure passed; accepted ELF hash was `e94b127f…baf31a`. | pass | `build-closure.log` and `build-closure/` |
| m0-p01-integration / m0-p01-n01-missing-qemu | Missing pinned QEMU fails. | Verifier rejected `/kay-os/missing/qemu` with nonzero status. | pass | `negative-missing-qemu.log` |
| m0-p01-integration / m0-p01-n02-missing-firmware | Changed or missing SeaBIOS path fails. | Verifier rejected `/kay-os/missing/bios.bin` with nonzero status. | pass | `negative-missing-firmware.log` |
| m0-p01-integration / m0-p01-n03-unavailable-machine | Unavailable QEMU machine fails within 10 seconds. | QEMU reported `unsupported machine type` and returned nonzero. | pass | `negative-unavailable-machine.log` |
| m0-p01-integration / m0-p01-n04-unavailable-cpu | Unavailable QEMU CPU fails within 10 seconds. | QEMU reported it could not find the CPU model and returned nonzero. | pass | `negative-unavailable-cpu.log` |
| m0-p01-integration / m0-p01-n05-build-closure | Helper, host import and CPU-option drift fail. | Nested driver matched `__udivti3`, `write`, and invalid `-Dcpu` failures. | pass | Nested negative logs under `build-closure/` |
| m0-p01-integration / m0-p01-n06-watchdog | A command exceeding one second returns 124. | Controlled sleep was terminated with timeout status 124. | pass | `negative-watchdog.log` |
| m0-p01-integration / m0-p01-b01-physical-boundary | Physical inventory is deferred and not consumed. | Driver recorded `deferred-to-m0-p03-inventory-not-consumed`; no inventory collector ran. | pass | `result.txt`, selected-input manifest and case manifest |

The driver returned zero and recorded `result=pass`. No unexpected successful
negative case, unmatched diagnostic, unregistered result, manifest-limit drift
or watchdog overrun occurred.

## Review and handoff

The executable result supports checking task `m0-p01-integration`, its two
subtasks, and evidence-record subtask 1.3.2.1. The implementation agent reviewed
the case registration, finite deadlines, positive results, negative diagnostics
and physical-boundary record.

Task `m0-p01-handoff`, Section 1.3 and the Phase 1 parent remain open because
the acceptance reviewer is unassigned. A reviewer must decide proceed, revise
or blocked against this record and the earlier
[build-closure evidence](2026-09-17-m0-phase-01-build-closure.md). This run does
not authorize Phase 2 implementation by itself.

Changes to the case manifest, limits, selected-input identities, verifier,
build flags, ABI, linker layout or physical-boundary policy reopen the virtual
integration result. No merge SHA exists yet; a later merge does not establish
that the merged tree passed without its own evidence.

## Follow-ups

- Assign the `m0-p01-handoff` acceptance reviewer and record the Phase 1
  proceed/revise/blocked decision.
- Keep `m0-p03-inventory` open until physical final-M0 qualification.
- If Phase 1 is accepted, resolve Phase 2's bootloader, handoff, static-image,
  console/time and initial-authority decisions before dependent implementation.
