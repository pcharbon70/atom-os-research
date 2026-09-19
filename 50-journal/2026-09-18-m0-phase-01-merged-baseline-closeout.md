---
title: "2026-09-18 — M0 phase 01 merged-baseline closeout"
kind: journal
created: "2026-09-18"
tags:
  - implementation-planning
  - m0
  - proof-of-concept
  - qemu
  - zig
aliases: []
---

# 2026-09-18 — M0 phase 01 merged-baseline closeout

The exact merged Kay OS `main` revision passed the complete registered M0
Phase 1 virtual integration suite with a clean working tree. The user accepted
the two merged pull requests as the Phase 1 proceed decision. This closes
`m0-p01-handoff` and permits M0 Phase 2 decision work; it does not close M0,
boot Kay OS, or qualify the physical Dell Precision T7500.

## Plan, merge and review baseline

- Research pull request: [atom-os-research PR 28](https://github.com/pcharbon70/atom-os-research/pull/28)
- Research merge revision: `862b0cfb03f6d1b9e1916e292445ca20d67c5258`
- Implementation pull request: [kay-os PR 1](https://github.com/pcharbon70/kay-os/pull/1)
- Tested implementation merge revision: `bc4c9984d776d75f23cb85193c9e3e3ff3270d61`
- Tested implementation state: clean (`dirty_file_count=0`)
- Acceptance reviewer: user/project owner
- Review decision: proceed, explicitly confirmed on 2026-09-18

The review accepts the selected virtual build/tool inputs and their declared
limits for entry into Phase 2. It does not convert preliminary M0-T01/T02
coverage into complete milestone acceptance, approve Phase 2 interface choices,
or waive the Phase 3 installed-unit inventory.

## Environment and command

- Zig: 0.16.0 at `/home/ducky/.asdf/installs/zig/0.16.0/zig`
- QEMU: 8.2.2 at `/usr/bin/qemu-system-x86_64`
- Fixture: `pc-q35-8.2`, `Nehalem-v1`, TCG, one CPU, 64 MiB,
  SeaBIOS 1.16.3, no network and no writable guest storage
- Completed evidence directory:
  `/tmp/kay-m0-phase-01-merged-bc4c998-rerun`
- Retained text evidence: [raw transcript](../assets/m0-phase-01-merged-baseline/raw-transcript.txt)

The exact completed invocation was:

```sh
ZIG=/home/ducky/.asdf/installs/zig/0.16.0/zig \
QEMU=/usr/bin/qemu-system-x86_64 \
  scripts/m0/verify-phase-01.sh \
  /tmp/kay-m0-phase-01-merged-bc4c998-rerun
```

An earlier invocation was externally interrupted by its command wrapper after
30 seconds while the bounded build-closure case was still running. It produced
no `result.txt` and is not treated as a test pass or test failure. The complete
rerun used a fresh evidence directory and allowed the driver's declared
180-second build deadline to control the result.

## Results and identities

The driver returned zero at `2026-09-18T13:24:07Z`. All nine registered cases
passed: pinned baseline resolution, two clean builds, missing QEMU, changed
firmware path, unavailable machine, unavailable CPU, build-closure negatives,
watchdog timeout, and the deferred-physical-inventory boundary.

| Evidence | SHA-256 |
| --- | --- |
| Case manifest | `83b01b41a7eafa210a698033b42d688ac7b15094a89075023d155e426733f4aa` |
| Freestanding fixture ELF | `e94b127fcc4388e73b4620a8b0908dcdeed0c3a08fbf0052d92cce58a3baf31a` |
| Case-results TSV | `9c88ef9f1f67c5de0a0054c75f5398c84f3811a6eb673ff392831678c5b9a794` |
| Evidence hash list | `b88fc380e0a2dd6678ff0b470944ec623a0c03d5f82387cc646e952795b26629` |

The fixture, case-manifest and case-results identities agree with the pre-merge
run. The evidence hash-list identity differs because it covers run-specific
metadata, including the tested revision and completion time.

## Handoff decision

Phase 1 result: **proceed**. Tasks `m0-p01-decisions`, `m0-p01-build`,
`m0-p01-integration` and `m0-p01-handoff` are accepted for their declared
virtual-development scope. M0 Phase 2 may now resolve M0-D02 and implement its
contract fixtures in the selected Kay OS repository.

The following remain open:

- loader, handoff, image, console, time, syscall and initial-fault choices;
- guest boot and user/kernel protection evidence;
- complete M0-T01 through M0-T06 acceptance;
- Phase 3 physical inventory and T7500 qualification; and
- every M1–M4 delivery gate.

Changes to the selected tool/firmware identities, case manifest, build flags,
ABI, linker layout, declared limits or physical-boundary policy reopen the
relevant Phase 1 evidence.

## Follow-ups

- Begin [M0 Phase 2](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-02-boot-image-and-interface-contracts.md)
  with task `m0-p02-decisions`.
- Assign Phase 2 execution and acceptance-review roles before dependent work.
- Keep `m0-p03-inventory` open until the physical qualification session.
