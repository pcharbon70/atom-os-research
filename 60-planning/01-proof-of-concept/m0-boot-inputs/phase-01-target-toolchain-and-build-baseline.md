---
title: "M0 Phase 1 — Target, toolchain, and build baseline"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m0
  - proof-of-concept
aliases: []
---

# M0 Phase 1 — Target, toolchain, and build baseline

Turn the selected Intel target into a versioned, reproducible development fixture and
installed-unit record. This phase qualifies inputs and native link fixtures, not a user-mode
OS.

Back to milestone: [M0 definition and plan](README.md).

## Entry, scope, and dependencies

Accepted CLI-first scope, T7500 target and Zig kernel language decision;
repository, compiler/backend/linker/translator pins and individual owners remain open.

Entry gate `accepted-scope-entry`: the milestone's accepted Intel target and CLI-first scope; this is not a prerequisite implementation task.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M0-D01 is partially decided: Zig is the selected kernel language.
Resolve the remaining choices through m0-p01-decisions: select the implementation
repository and qualify the Zig compiler/backend/linker/translator using
freestanding support, C ABI/helper closure, instruction control, reproducibility, and
maintenance cost; assign execution/review roles. Verify exact QEMU/firmware availability and
installed-unit inventory rather than relying on family specifications. Until resolution,
downstream code and passing acceptance claims are blocked.

The host owns build tools, validation fixtures, emulation and capture; M0 does not claim
kernel enforcement. Firmware/loader/kernel ownership is fixed in the contract.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M0-A01, M0-A02, M0-A07; its case coverage is M0-T01, M0-T02, M0-T06. Partial/model/hosted results do not close a case requiring later guest integration.

- [target firmware and boot handoff](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — contract and failure-case input for this phase.
- [freestanding build and static images](../../../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md) — contract and failure-case input for this phase.
- [Zig feasibility and C interoperability](../../../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md) — selected language, candidate profile and limited research evidence; neither the compiler pin nor this phase is accepted by those probes.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m0-p01-decisions | atom-os-research | Unassigned; resolve in m0-p01-decisions | accepted-scope-entry | M0-A01, M0-A02; phase cases below | Select and record the development baseline output and verification; not run |
| m0-p01-inventory | unresolved-implementation | Unassigned; resolve in m0-p01-decisions | m0-p01-decisions | M0-A07; phase cases below | Inventory the installed T7500 output and verification; not run |
| m0-p01-build | unresolved-implementation | Unassigned; resolve in m0-p01-decisions | m0-p01-decisions | M0-A02; phase cases below | Build and audit freestanding fixtures output and verification; not run |
| m0-p01-integration | unresolved-implementation | Unassigned test reviewer | m0-p01-build, m0-p01-inventory | M0-T01, M0-T02, M0-T06 | Registered driver, raw positive/negative results; not run |
| m0-p01-handoff | atom-os-research | Unassigned acceptance reviewer | m0-p01-integration | M0-A01, M0-A02, M0-A07; M0-T01, M0-T02, M0-T06 | Dated evidence and proceed/revise/blocked review; not run |

Build fixtures and read-only inventory both depend on the decisions task, but
not on each other. Virtual build experiments can proceed while inventory is
unavailable; the required inventory and full M0 gate remain open. This is a
logical independence statement, not authorization for parallel agents.

## Planned work

- [ ] 1 Phase — Target, toolchain, and build baseline.

  Turn the selected Intel target into a versioned, reproducible development fixture and
  installed-unit record. This phase qualifies inputs and native link fixtures, not a user-mode
  OS. Completion requires the assembled phase gate below, not just its component tasks.

  - [ ] 1.1 Section — Execution profile.

    Resolve inputs before later code assumes a compiler, loader, or installed processor.

    - [ ] 1.1.1 Task [id: m0-p01-decisions] [repo: atom-os-research] [after: accepted-scope-entry] — Select and record the development baseline.

      Produce the M0-D01 decision record and bind the locations and owners used by every later
      task.

      - [ ] 1.1.1.1 Subtask — Qualify the selected Zig development profile.

        Preserve the user's Zig kernel-language decision. Evaluate the researched 0.16.0
        candidate and any justified pinned profile revision through freestanding compile/link
        fixtures. Record compiler/backend/linker/translator identities, C and runtime helpers,
        license constraints, instruction controls, ownership and source location. Language
        selection does not accept those remaining inputs or close this subtask.

      - [ ] 1.1.1.2 Subtask — Pin the virtual fixture.

        Record exact QEMU and versioned q35, Nehalem-v1, TCG, SeaBIOS, one CPU, 128 MiB,
        serial and read-only media identities. Reject missing versions and host-native feature
        drift in the launch manifest.

    - [ ] 1.1.2 Task [id: m0-p01-inventory] [repo: unresolved-implementation] [after: m0-p01-decisions] — Inventory the installed T7500.

      Deliver M0-A07 from observations, with explicit unknowns and a safe qualification path.

      - [ ] 1.1.2.1 Subtask — Collect installed-unit evidence.

        Record CPU SKU/stepping/features, enabled topology, RAM, board, firmware, relevant
        devices, and serial/debug availability using read-only inspection. Redact service
        identifiers; unavailable hardware leaves this obligation open.

      - [ ] 1.1.2.2 Subtask — Separate virtual and physical assumptions.

        Document the physical boot-media prerequisites and additional-CPU policy. Verify the
        record never claims q35 reproduces T7500 wiring or qualifies physical timing.

  - [ ] 1.2 Section — Build closure.

    Make the chosen build reproduce outside the author’s checkout and expose every guest
    dependency.

    - [ ] 1.2.1 Task [id: m0-p01-build] [repo: unresolved-implementation] [after: m0-p01-decisions] — Build and audit freestanding fixtures.

      Deliver M0-A02 with actual compiler/linker results and a machine-checkable dependency
      census.

      - [ ] 1.2.1.1 Subtask — Constrain code generation.

        Create the selected flags/linker layout and native fixture; enumerate symbols,
        compiler helpers, calling convention, FP/SIMD policy, and unsupported instructions.
        Undefined helpers or accidental host syscalls must fail. Verify C/Zig boundary
        sizes, alignment, offsets, supported arguments/results and callbacks in both directions;
        compile consumers of the intended translated declarations. Retain fixed-signature
        wrappers for unqualified interfaces and a custom panic/stack-support contract.

      - [ ] 1.2.1.2 Subtask — Reproduce independent builds.

        Build in two clean absolute directories, compare hashes/maps, and explain any narrowly
        permitted nondeterminism. Preserve commands and binary identities rather than claiming
        reproducibility from one build.

  - [ ] 1.3 Section — Phase 1 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 1.3.1 Task [id: m0-p01-integration] [repo: unresolved-implementation] [after: m0-p01-build, m0-p01-inventory] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 1.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run environment resolution and clean native fixture builds
        against the exact manifest; cross-check installed-unit evidence and qualified virtual
        assumptions. M0-T01/T02/T06 are preliminary here where image/ABI inputs are completed
        in Phase 2 and rerun in Phase 3.

      - [ ] 1.3.1.2 Subtask — Exercise failures and inherited behavior.

        Remove a pinned input, request unavailable CPU/machine features, introduce an
        undefined helper, and alter instruction flags. Each must fail explicitly. An unknown
        physical inventory item must stay open rather than be filled from a product brochure.
        Retain actual observations and finite watchdog outcomes, not only intended commands.

    - [ ] 1.3.2 Task [id: m0-p01-handoff] [repo: atom-os-research] [after: m0-p01-integration] — Record evidence and decide phase handoff.

      Release the accepted build/fixture inputs to Phase 2. Missing required inventory keeps
      full M0 acceptance open; exploratory virtual work must be labelled provisional.

      - [ ] 1.3.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 1.3.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
