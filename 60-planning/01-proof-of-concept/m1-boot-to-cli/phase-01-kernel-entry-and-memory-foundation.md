---
title: "M1 Phase 1 — Kernel entry and memory foundation"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# M1 Phase 1 — Kernel entry and memory foundation

Bring up the real ring-0 kernel, validated boot-memory state and bounded runtime
hardware-discovery report on the M0 baseline, with no host OS inside the guest.

Back to milestone: [M1 definition and plan](README.md).

## Entry, scope, and dependencies

M0 qualified virtual/build/contracts and exercised its watchdog. Research
merge `9c0653b` records the accepted handoff; Kay OS merge `28408e8` contains
the executable baseline. Provisional experiments cannot be accepted M1 evidence.

Required predecessor: [M0 Phase 3](../m0-boot-inputs/phase-03-acceptance-harness-and-input-qualification.md), task `m0-p03-handoff`.

Plan state: accepted for execution; M1-D01 was selected by the user/project
owner on 2026-09-21. Section 1.1 implementation completed at Kay OS commit
`64740540e04b862336a70cc65a5dd02d1eb61240`; its positive boot and five
fault-injected development boots passed. Section 1.2 evidence and handoff are
recorded separately. Implementation lives in the
public [Kay OS repository](https://pushin.eu/pcharbon70/kay-os). Codex is the
implementation/test role; the user/project owner is the decision and acceptance
reviewer. Later execution still requires the accepted M1-D01 record.

Decision M1-D01 is resolved by `m1-p01-decisions`: Kay takes immediate
ownership of entry stacks and descriptor/exception state, copies and validates
the Limine handoff, constructs Kay-owned page tables, and withholds general
allocation until conservative reservations are established. The accepted
profile below binds downstream work; changing it reopens this decision and its
dependent evidence.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 64 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Accepted M1-D01 entry ownership profile

The user/project owner selected immediate Kay ownership (option 1) on
2026-09-21. Limine v12.9.0/base revision 6 remains responsible for the
BIOS-to-long-mode transition, but loader-provided execution state is temporary
input rather than Kay's operating state.

The first assembly path keeps maskable interrupts disabled, validates the
minimum entry identity needed to continue, and switches to Kay's statically
reserved, 16-byte-aligned 16 KiB bootstrap stack. Before general allocation,
Kay installs its own GDT, IDT and TSS plus statically reserved 16 KiB IST stacks
for double fault, NMI and machine check. `TSS.rsp0` is Kay-owned from this point
but is not evidence of the Phase 2 ring-3 transition. FP/SIMD remains disabled
and unowned, and additional processors remain unstarted.

Kay bounds, validates and copies the required Limine response data into
kernel-owned storage. It then constructs and activates Kay-owned page tables
from a statically reserved bootstrap page-table pool before enabling the
general physical-page allocator. The initial mappings cover only the admitted
kernel image, bootstrap/IST stacks, current handoff-copy storage, page tables,
and explicitly required early console/firmware access; later permissions and
user mappings remain Phase 2 work.

Memory begins reserved unless validated as usable and outside every owned or
borrowed range. Kernel image/BSS, bootstrap and IST stacks, page tables,
handoff copies, modules, firmware-reserved/NVS ranges, ACPI tables in use and
all unknown/conflicting ranges are excluded from allocation. Limine
bootloader-reclaimable memory stays reserved until no borrowed pointer remains,
all required data has been copied, and Kay-owned paging is active. ACPI
reclaimable memory stays reserved until required tables have been validated and
copied; permanently reserved/NVS ranges are never released by this phase.

Versioned serial milestones identify `entry`, `handoff`, `descriptors`,
`paging`, `memory` and `discovery-ready`. A startup failure emits one bounded
record naming the last completed milestone and stable reason code, then enters
the accepted stable halt. The host watchdog treats silence, timeout and reboot
loops as failure. These records are diagnostic evidence only; none is a
`kay>` prompt or user-mode success.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M1-A01, M1-A06; its case coverage is M1-T06, M1-T07, M1-T08 and the discovery portion of M1-T09. Partial/model/hosted results do not close a case requiring later guest integration.

- [target firmware and boot handoff](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — contract and failure-case input for this phase.
- [privilege entry memory and user return](../../../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m1-p01-decisions | atom-os-research | Codex implementer; user/project owner decision reviewer | m0-p03-handoff | M1-A01; phase cases below | M1-D01 immediate Kay ownership accepted 2026-09-21; profile recorded above |
| m1-p01-memory | kay-os | Codex implementer/tester | m1-p01-decisions | M1-A01, M1-A06; phase cases below | Kay `6474054`: copied 19-entry map, 15,936 usable pages, Kay CR3/GDT/IDT/TSS and bounded failure boots |
| m1-p01-discovery | kay-os | Codex implementer/tester | m1-p01-memory | M1-A01, M1-A06; M1-T09 | Kay `6474054`: CPUID and RSDT/MADT report reached `discovery-ready` on the declared baseline |
| m1-p01-integration | kay-os | Codex implementer/tester; user/project owner acceptance review | m1-p01-discovery | M1-T06, M1-T07, M1-T08, M1-T09 discovery portion | Registered driver, raw positive/negative results; not run |
| m1-p01-handoff | atom-os-research | User/project owner acceptance reviewer | m1-p01-integration | M1-A01, M1-A06; M1-T06, M1-T07, M1-T08, M1-T09 discovery portion | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 1 Phase — Kernel entry and memory foundation.

  Bring up the real ring-0 kernel, validated boot-memory state and runtime
  discovery report on the M0 baseline, with bounded diagnostics and no host OS
  inside the guest. Completion requires the assembled phase gate below.

  - [x] 1.1 Section — Controlled kernel startup.

    Replace contract-only fixtures with kernel-owned entry state and conservative
    physical-memory initialization.

    - [x] 1.1.1 Task [id: m1-p01-decisions] [repo: atom-os-research] [after: m0-p03-handoff] — Bind the exact M0 execution contract.

      Resolve M1-D01 by accepting the tested predecessor revision and resolving
      implementation-specific entry ownership.

      - [x] 1.1.1.1 Subtask — Audit startup assumptions.

        Check loader guarantees against CPU feature checks, descriptors, stacks, interrupt
        state, and preserved register components. Return incompatible assumptions to M0 rather
        than silently choosing a different ABI.

      - [x] 1.1.1.2 Subtask — Specify bounded diagnostic failure.

        Select identifiable startup milestones and finite fault halt/reset reporting under the
        host watchdog; a repeated reboot must not be interpreted as success.

    - [x] 1.1.2 Task [id: m1-p01-memory] [repo: kay-os] [after: m1-p01-decisions] — Implement boot parsing and memory reservation.

      Deliver kernel entry and normalized usable/reserved memory with inspectable ownership.

      - [x] 1.1.2.1 Subtask — Initialize trusted entry state.

        Install the selected descriptor/exception setup and capture a bounded handoff
        snapshot. Validate required tables and image lifetimes before using their memory.

      - [x] 1.1.2.2 Subtask — Construct conservative memory ownership.

        Reserve kernel, boot images, firmware, page tables, stacks, and devices; reject
        overflow/overlap or unknown regions. Check allocator totals against the normalized
        snapshot.

      - [x] 1.1.2.3 Subtask — Exercise corrupted boot inputs.

        Feed malformed handoffs and forced initialization failure through a test boot. Confirm
        bounded diagnostics and no continued execution on ambiguous memory.

    - [x] 1.1.3 Task [id: m1-p01-discovery] [repo: kay-os] [after: m1-p01-memory] — Discover and report the presented platform.

      Establish the minimum generic x86-64 discovery path without consulting a
      physical-fixture inventory or hard-coding the QEMU baseline's values.

      - [x] 1.1.3.1 Subtask — Validate CPU and firmware descriptions.

        Query CPUID, validate the Limine-provided ACPI root, parse only the
        bounded tables needed for the current APIC/timer/console path, and
        reject absent or malformed mandatory data with explicit diagnostics.

      - [x] 1.1.3.2 Subtask — Emit a bounded discovery report.

        Record the discovered CPU feature subset, logical topology, usable and
        reserved memory summary, ACPI/APIC identities and relevant early
        console/timer resources. Bound lengths and counts so malformed firmware
        cannot create unbounded serial output or work.

  - [ ] 1.2 Section — Phase 1 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 1.2.1 Task [id: m1-p01-integration] [repo: kay-os] [after: m1-p01-discovery] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 1.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Boot the actual kernel using M0's driver and correlate serial
        startup markers with debugger state and memory ledgers. Run the startup portions of
        M1-T06/T07/T08 and the discovery portion of M1-T09; these are not yet
        full CLI or matrix acceptance.

      - [ ] 1.2.1.2 Subtask — Exercise failures and inherited behavior.

        Truncate/overlap reservations and remove required features. Confirm safe failure and
        watchdog detection; repeat M0 build/version/handoff checks so a fixture change cannot
        mask a kernel defect. Retain actual observations and finite watchdog outcomes, not
        only intended commands.

    - [ ] 1.2.2 Task [id: m1-p01-handoff] [repo: atom-os-research] [after: m1-p01-integration] — Record evidence and decide phase handoff.

      Pass a reproducible kernel-entry and memory baseline to Phase 2. Do not close M1-T01
      merely because a ring-0 banner appears.

      - [ ] 1.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 1.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
