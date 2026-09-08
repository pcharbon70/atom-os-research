---
title: "M3 Phase 2 — Actor interpreter and tracing GC"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m3
  - proof-of-concept
aliases: []
---

# M3 Phase 2 — Actor interpreter and tracing GC

Execute admitted BEAM semantics and automatically trace/reclaim private-heap garbage in
long-lived actors outside the kernel.

Back to milestone: [M3 definition and plan](README.md).

## Entry, scope, and dependencies

M3 Phase 1 admitted corpus/loader; guest claims also require M2 protected runtime domain.
Hosted tests remain distinct.

Required predecessor: [M3 Phase 1](phase-01-compiled-profile-and-atomic-loader.md), task `m3-p01-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M3-D02 is resolved by m3-p02-decisions: Choose term/root representation,
collection/growth/workspace failure policy, reductions and safe points by correctness, bounded
memory, latency risks and implementation complexity. Until resolution, downstream code and
passing acceptance claims are blocked.

The kernel enforces domain protection and backing; the interpreter, actors and tracing
collector remain ring 3. A hosted oracle supplies comparison results, not guest kernel
services.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M3-A03, M3-A04, M3-A06; its case coverage is M3-T01, M3-T03, M3-T05. Partial/model/hosted results do not close a case requiring later guest integration.

- [private heaps and tracing garbage collection](../../../20-notes/proof-of-concept-requirements/private-heaps-and-tracing-garbage-collection.md) — contract and failure-case input for this phase.
- [runtime adapter signals and native services](../../../20-notes/proof-of-concept-requirements/runtime-adapter-signals-and-native-services.md) — contract and failure-case input for this phase.
- [beam profile loader and conformance](../../../20-notes/proof-of-concept-requirements/beam-profile-loader-and-conformance.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m3-p02-decisions | atom-os-research | Unassigned; resolve in m3-p02-decisions | m3-p01-handoff | M3-A03, M3-A04, M3-A06; phase cases below | Freeze term, root, and scheduling contracts output and verification; not run |
| m3-p02-interpreter | unresolved-implementation | Unassigned; resolve in m3-p02-decisions | m3-p02-decisions | M3-A03; phase cases below | Implement admitted interpreter and signals output and verification; not run |
| m3-p02-gc | unresolved-implementation | Unassigned; resolve in m3-p02-decisions | m3-p02-interpreter | M3-A04, M3-A06; phase cases below | Implement local tracing and root relocation output and verification; not run |
| m3-p02-integration | unresolved-implementation | Unassigned test reviewer | m3-p02-gc | M3-T01, M3-T03, M3-T05 | Registered driver, raw positive/negative results; not run |
| m3-p02-handoff | atom-os-research | Unassigned acceptance reviewer | m3-p02-integration | M3-A03, M3-A04, M3-A06; M3-T01, M3-T03, M3-T05 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 2 Phase — Actor interpreter and tracing GC.

  Execute admitted BEAM semantics and automatically trace/reclaim private-heap garbage in
  long-lived actors outside the kernel. Completion requires the assembled phase gate below,
  not just its component tasks.

  - [ ] 2.1 Section — Managed execution.

    Implement only the admitted semantics while keeping scheduling and root ownership
    explicit.

    - [ ] 2.1.1 Task [id: m3-p02-decisions] [repo: atom-os-research] [after: m3-p01-handoff] — Freeze term, root, and scheduling contracts.

      Resolve M3-D02 before moving managed objects or retaining native references.

      - [ ] 2.1.1.1 Subtask — Specify root ownership.

        List register, stack, continuation, exception, mailbox, timer and native-adapter
        roots, shared binary ownership and transfer rules. Define safe handling of movable
        pointers and collection workspace reservations.

      - [ ] 2.1.1.2 Subtask — Select safe-point and quota policy.

        Choose reductions for dispatch, BIFs, copying, scans and adapter work; record heap
        growth and failed-workspace outcomes. Kernel preemption does not establish fairness
        among actors sharing one runtime.

    - [ ] 2.1.2 Task [id: m3-p02-interpreter] [repo: unresolved-implementation] [after: m3-p02-decisions] — Implement admitted interpreter and signals.

      Deliver term operations, calls/exceptions and the actor operations required by the
      corpus.

      - [ ] 2.1.2.1 Subtask — Execute compiled control flow.

        Implement admitted instruction/BIF semantics and exception paths, checking oracle
        observations and refusing unsupported behavior honestly.

      - [ ] 2.1.2.2 Subtask — Implement actor scheduling and messages.

        Support spawn/exit, copied messages, selective receive, links/monitors, timers and
        required aliases. Verify per-sender ordering without inventing cross-sender order;
        charge long scans and copying.

  - [ ] 2.2 Section — Automatic reclamation.

    Reclaim unreachable terms without requiring application frees or actor death.

    - [ ] 2.2.1 Task [id: m3-p02-gc] [repo: unresolved-implementation] [after: m3-p02-interpreter] — Implement local tracing and root relocation.

      Deliver an unprivileged collector tied to the interpreter safe points and finite heap
      accounts.

      - [ ] 2.2.1.1 Subtask — Reserve and trace safely.

        Secure collection workspace before destructive movement and update every root class.
        Preserve reachable values/sharing and forbid unrooted native pointers.

      - [ ] 2.2.1.2 Subtask — Exercise long-lived heaps.

        Force collections at varied safe points while actors retain a fixed live set and
        allocate transient garbage. Require a bounded post-GC plateau and explicit failure
        when collection space is insufficient.

      - [ ] 2.2.1.3 Subtask — Separate local and global retention.

        Report code, atoms, shared binaries, allocator slack and reserved space separately.
        Actor-local reclamation cannot hide unbounded runtime-global growth.

  - [ ] 2.3 Section — Phase 2 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 2.3.1 Task [id: m3-p02-integration] [repo: unresolved-implementation] [after: m3-p02-gc] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 2.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute the admitted semantic corpus and forced-root/GC cases
        for M3-T01/T03 with finite accounts. Show automatic collection in living actors,
        oracle-compatible observations and measured same-runtime scheduling delays.

      - [ ] 2.3.1.2 Subtask — Exercise failures and inherited behavior.

        Force insufficient collection space, root relocation at exception/receive boundaries,
        large mailbox scans and heap pressure. Reachable terms must survive and failures
        remain bounded; rerun loader rejection and inherited native protection. Retain actual
        observations and finite watchdog outcomes, not only intended commands.

    - [ ] 2.3.2 Task [id: m3-p02-handoff] [repo: atom-os-research] [after: m3-p02-integration] — Record evidence and decide phase handoff.

      Pass a tested interpreter/collector to Phase 3. Full guest adapter,
      mailbox/global/continuation accounting and all M3 guest cases remain necessary.

      - [ ] 2.3.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 2.3.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
