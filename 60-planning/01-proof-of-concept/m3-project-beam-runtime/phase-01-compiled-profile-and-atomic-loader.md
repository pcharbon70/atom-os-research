---
title: "M3 Phase 1 — Compiled profile and atomic loader"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m3
  - proof-of-concept
aliases: []
---

# M3 Phase 1 — Compiled profile and atomic loader

Freeze an executable BEAM compatibility boundary and admit its compiler-produced modules
atomically under finite loader accounts.

Back to milestone: [M3 definition and plan](README.md).

## Entry, scope, and dependencies

M0 build location and native profile; M2 guest interfaces for guest acceptance. Hosted
corpus/loader experiments may precede M2 only when authorized and remain hosted evidence.

Required predecessor: [M2 Phase 4](../m2-protected-service-nucleus/phase-04-recovery-nucleus-and-cli-control.md), task `m2-p04-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M3-D01 is resolved by m3-p01-decisions: Select workload and claimed OTP behavior,
exact compiler/oracle/flags/library closure, supported term/opcode/BIF/chunk subset, loader
staging and bounded retained-interning policy. Until resolution, downstream code and passing
acceptance claims are blocked.

The kernel enforces domain protection and backing; the interpreter, actors and tracing
collector remain ring 3. A hosted oracle supplies comparison results, not guest kernel
services.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M3-A01, M3-A02, M3-A06; its case coverage is M3-T01, M3-T02. Partial/model/hosted results do not close a case requiring later guest integration.

- [beam profile loader and conformance](../../../20-notes/proof-of-concept-requirements/beam-profile-loader-and-conformance.md) — contract and failure-case input for this phase.
- [resource accounting and mailbox overload](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m3-p01-decisions | atom-os-research | Unassigned; resolve in m3-p01-decisions | m2-p04-handoff | M3-A01; phase cases below | Freeze the workload and oracle output and verification; not run |
| m3-p01-loader | unresolved-implementation | Unassigned; resolve in m3-p01-decisions | m3-p01-decisions | M3-A02, M3-A06; phase cases below | Implement the atomic loader output and verification; not run |
| m3-p01-integration | unresolved-implementation | Unassigned test reviewer | m3-p01-loader | M3-T01, M3-T02 | Registered driver, raw positive/negative results; not run |
| m3-p01-handoff | atom-os-research | Unassigned acceptance reviewer | m3-p01-integration | M3-A01, M3-A02, M3-A06; M3-T01, M3-T02 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 1 Phase — Compiled profile and atomic loader.

  Freeze an executable BEAM compatibility boundary and admit its compiler-produced modules
  atomically under finite loader accounts. Completion requires the assembled phase gate below,
  not just its component tasks.

  - [ ] 1.1 Section — Compatibility closure.

    Let emitted compiler output and observable semantics determine interpreter work, not a
    guessed opcode subset.

    - [ ] 1.1.1 Task [id: m3-p01-decisions] [repo: atom-os-research] [after: m2-p04-handoff] — Freeze the workload and oracle.

      Resolve M3-D01 before dependent interpreter scope is accepted.

      - [ ] 1.1.1.1 Subtask — Compile the smallest useful workload.

        Pin compiler/oracle and library sources, flags and hashes. Include counter/job
        success, error, timeout and restart paths; inspect dynamic callbacks and helpers as
        well as static imports.

      - [ ] 1.1.1.2 Subtask — Publish the machine-readable profile.

        Enumerate chunks, opcodes, terms, BIF arities, exports, exceptions, signals, timers,
        limits and exclusions. Include aliases/monitors if selected finite OTP calls require
        them; custom restart is not upstream supervisor compatibility.

      - [ ] 1.1.1.3 Subtask — Capture oracle expectations.

        Compile and execute the admitted corpus on the pinned oracle and record values,
        exceptions and required ordering with comparison rules. Resource-policy differences
        must be explicit rather than normalized away.

  - [ ] 1.2 Section — Bounded module admission.

    Implement validated parsing and staged publication before the interpreter can observe
    code.

    - [ ] 1.2.1 Task [id: m3-p01-loader] [repo: unresolved-implementation] [after: m3-p01-decisions] — Implement the atomic loader.

      Deliver M3-A02 with every atom/code/literal/export allocation charged and failure-safe.

      - [ ] 1.2.1.1 Subtask — Validate complete module structure.

        Check lengths, arithmetic, references, register indices, control-flow targets,
        operands, unsupported opcodes/imports and optional chunks. Reject invalid data before
        it can dispatch.

      - [ ] 1.2.1.2 Subtask — Stage and commit under finite accounts.

        Reserve loader/global capacity, publish exports only after validation, and unwind
        every staged failure. If interning survives rejection, bound and charge it explicitly.

      - [ ] 1.2.1.3 Subtask — Build hostile loader fixtures.

        Mutate/truncate the compiled corpus and inject allocation failure at staged steps.
        Compare publication tables and resource deltas before and after rejection.

  - [ ] 1.3 Section — Phase 1 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 1.3.1 Task [id: m3-p01-integration] [repo: unresolved-implementation] [after: m3-p01-loader] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 1.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Reproduce the compiler/oracle corpus and validate/admit its
        modules under the declared manifest. Run hosted M3-T02 and the corpus/oracle portion
        of T01; guest execution and final runtime-ledger integration remain open.

      - [ ] 1.3.1.2 Subtask — Exercise failures and inherited behavior.

        Reject oversized tables, bad references, unsupported instructions and imports, and
        failures after partial allocation without partial exports or uncharged growth. Recheck
        M0 native helper/instruction closure. Retain actual observations and finite watchdog
        outcomes, not only intended commands.

    - [ ] 1.3.2 Task [id: m3-p01-handoff] [repo: atom-os-research] [after: m3-p01-integration] — Record evidence and decide phase handoff.

      Give Phase 2 a pinned compiled corpus, oracle, term/profile boundary and tested loader.
      Do not label loader admission as interpreter conformance.

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
