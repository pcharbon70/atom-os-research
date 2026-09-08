---
title: "M3 — Project BEAM runtime"
kind: map
created: "2026-09-08"
tags:
  - archive-navigation
  - beam
  - directory-index
  - implementation-planning
  - m3
  - proof-of-concept
aliases: []
---

# M3 — Project BEAM runtime

## Purpose

Make the operating system genuinely capable of executing compiler-produced
BEAM, rather than merely demonstrating a native prompt or an actor-inspired
library. An operator must be able to inspect the supported compatibility
profile and launch a bounded workload through the CLI. That workload must run
inside the project's unprivileged interpreter, exchange messages, handle
failures, and reclaim unreachable data automatically while its actors remain
alive.

M3 supplies the runtime implementation and machine-readable, tested BEAM/OTP
profile missing from the readiness assessment's managed-runtime coverage row.
It also supplies the managed part of the CLI-operated application and connects
actor supervision to the independent recovery substrate established by
[M2](../m2-protected-service-nucleus/README.md).

## What belongs here

The milestone includes a project-owned loader and reference interpreter,
compiler-produced workload and conformance corpus, managed actor semantics,
private heaps and tracing GC, finite resource accounts, and the adapter to
Atom's kernel and native services. The interpreter direction follows the
readiness assessment; AtomVM is neither a dependency nor a comparison gate.

The initial deployment retains one CPU, serial operation, and static boot
bundles. It does not require a JIT, full OTP compatibility, dynamic package
loading, networking, writable storage, SMP, or a graphical interface. A custom
restart loop is OTP-inspired behavior, not evidence that the upstream
`supervisor` module works unchanged. Compatibility claims cover only admitted,
tested paths. The shared runtime is not claimed to sandbox hostile BEAM code.

## Planning and delivery state

This milestone now has a draft phased implementation plan. The detailed outcome,
artifact IDs and acceptance criteria below remain authoritative. All tasks are
unchecked, implementation has not started, and every acceptance case is not run.
Open decisions must be resolved before dependent execution; writing or reviewing
a plan neither closes a delivery gate nor authorizes implementation or publication.

## Authoritative inputs

- [Planning stream](../README.md) and [readiness assessment](../../../20-notes/proof-of-concept-research-readiness.md) — milestone order, missing artifacts, and the completed-PoC boundary.
- [BEAM profile, loader, and conformance](../../../20-notes/proof-of-concept-requirements/beam-profile-loader-and-conformance.md) — R08, exact compiler/workload closure and atomic admission.
- [Runtime adapter, signals, and native services](../../../20-notes/proof-of-concept-requirements/runtime-adapter-signals-and-native-services.md) — R09, nonblocking integration and signal semantics.
- [Private heaps and tracing garbage collection](../../../20-notes/proof-of-concept-requirements/private-heaps-and-tracing-garbage-collection.md) — R10, roots, automatic reclamation, and latency limits.
- [Resource accounting and mailbox overload](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md) — R11, complete charging and explicit overload outcomes.
- [Supervision and independent recovery](../../../20-notes/proof-of-concept-requirements/supervision-and-independent-recovery.md) — R12, actor failure versus protection-domain failure.
- [T7500 target and QEMU profile](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) — Intel x86-64 target and controlled guest fixture.

## Entry decisions and dependencies

Guest acceptance depends on M2's real domains, capability-scoped calls, memory
and CPU accounts, fault delivery, registry generations, and funded outer
recovery. Hosted semantic experiments may precede that substrate when separately
authorized; they cannot close the guest milestone.

Before interpreter scope is committed, the runtime implementer and reviewer
must resolve the following decisions; individuals are not assigned here:

- Select the smallest useful counter/job workload and whether selected upstream
  OTP behaviors are claimed. Inspect success, exception, timeout, and restart
  paths before accepting its transitive dependency closure. This blocks the
  opcode/BIF/library implementation boundary, not M0 or M1.
- Pin the exact compiler, flags, upstream runtime oracle, library sources, and
  hashes. The archive's documentation baseline is not an installed or tested
  compiler. Align the oracle and fixtures before treating differential results
  as conformance evidence.
- Resolve term/root representation, heap growth and collection policy, mailbox
  overload behavior, global limits, and reduction charging. Compare correctness,
  bounded failure, implementation complexity, and the declared workload envelope;
  record accepted choices before implementing dependent paths.
- Bind the guest adapter to accepted M2 ABI and lifecycle versions. Predeclare
  capacities, responsiveness thresholds, and evidence locations before acceptance
  runs. Do not invent numerical results or move limits after a failure.

## Required artifacts

The identifiers below name delivery obligations, not completed tasks. The
phases below map each artifact to described tasks and their integration gates.

### M3-A01 — Versioned compatibility profile and compiled corpus

Deliver a machine-readable manifest linking exact compiler inputs and bundle
hashes to supported chunks, external opcodes, term forms and limits, imports/BIF
arities, exceptions, signal rules, timers, and selected library exports. Separate
implemented, excluded, and untested behavior, including intentional resource
differences. Inspect emitted code and transitive callbacks, dynamic calls, helper
functions, and error paths; static imports alone do not establish closure.
Include aliases, monitors, and any other features required by selected finite
OTP calls. Preserve reproducible oracle outputs and comparison rules.

### M3-A02 — Bounded loader with atomic publication

Deliver validated parsing and admission for the declared bundle format, including
lengths, arithmetic, table/register references, control-flow targets, operands,
and the chosen treatment of optional chunks. Stage atoms, literals, code, and
exports under finite accounts. Failure must publish no partial module; rollback
or an explicitly bounded retained-interning policy must account for every
allocation. A trusted bundle hash does not replace validation.

### M3-A03 — Interpreter and actor semantics

Deliver executable support for the admitted compiler output: terms, calls,
exceptions, spawn/exit, copied messages, selective receive, links/monitors,
timers, and the selected supervision paths. Distinguish per-sender ordering
from ordering across unrelated senders. Specify reduction charging and safe
points for dispatch, BIFs, copying, mailbox scans, and adapter work. Kernel
preemption protects other domains; it does not by itself make actors sharing
one runtime scheduler responsive.

### M3-A04 — Root contract and automatic local tracing collector

Deliver a term/root specification and unprivileged collector covering registers,
stacks, continuations, exceptions, mailbox terms, timers, and native-adapter
references. Reserve collection workspace before destructive movement, preserve
reachable values and observable sharing, and define reservation-failure behavior.
Native code must not retain unrooted movable pointers. Reclamation must occur
inside long-lived actors without explicit application frees; reclaiming only
when an actor exits does not satisfy M3.

### M3-A05 — Audited guest adapter and asynchronous native requests

Deliver an import/replacement inventory, including linked compiler/library
helpers, for allocation, clocks, waits, synchronization, entropy, image access,
logging, and termination. Explicitly disable unsupported filesystem, socket,
host-thread, and dynamic-library paths. Map a waiting actor to a bounded
continuation without blocking the runtime's only scheduler. Correlate replies
with actor/request and service generation; resolve completion, timeout,
cancellation, and death once. Retire late-reply delivery authority without
claiming an accepted server effect was undone.

### M3-A06 — Runtime resource ledger and overload contract

Deliver finite ownership and reservation records for heaps, copying space,
mailbox storage, in-flight copies, shared binaries/sub-binaries, atoms,
code/literals, actor records, monitors/aliases, timers, continuations, and
allocator slack. Distinguish physical backing from logical attribution and
report runtime-global retention separately from local heap collection. Choose
an explicit mailbox admission-failure policy: an admitted local message cannot
be silently discarded as apparent success. Protect M2's independent recovery
reserve from every runtime allocation and failure path.

### M3-A07 — CLI-operated workload and recovery integration

Deliver real `beam-profile` and `run <module>` commands against the static bundle,
with honest unsupported-module errors. Expose runtime accounts and generations
through existing inspection interfaces. Demonstrate an actor restart within a
surviving runtime, then whole-runtime replacement by the separate recovery
domain. Document volatile state loss, changed identities, and indeterminate
outcomes for requests accepted before a failure.

## Responsibility and trust boundaries

The ring-0 kernel owns protection, domain scheduling, bounded transport, and
physical resource enforcement. The ring-3 runtime owns BEAM execution, actor
isolation, reductions, signal processing, and GC. A native function linked into
the interpreter shares its failure boundary; the native test service resides
in another domain. Outer recovery must remain outside the runtime it replaces.
Upstream OTP supplies compiler/oracle evidence on the host, not guest kernel
services. QEMU evidence does not qualify the physical T7500.

## Integrated acceptance cases

These milestone-level cases are mapped to the phase-ending gates below.
Each remains open until its artifacts and reproducible guest evidence exist.

| Case | Required demonstration | Artifacts |
| --- | --- | --- |
| M3-T01 | Cleanly compile the declared corpus; match pinned-oracle observable results and required ordering in hosted and CLI-launched guest runs. Enumerate exclusions separately. | A01, A03, A07 |
| M3-T02 | Reject truncation, unsupported opcodes/imports, oversized tables, invalid references, and failures after staged allocations without partial exports or uncharged growth. | A01, A02, A06 |
| M3-T03 | Force collections at varied safe points in long-lived actors: roots survive, fixed-live-set transient garbage reaches a bounded post-collection plateau, and reserved/global bytes remain separately visible. Exercise insufficient collection space. | A03, A04, A06 |
| M3-T04 | Stall a native request while another actor allocates and advances a heartbeat. Exercise finite-timeout/reply races, peer death, malformed responses, and duplicate/old-generation replies without scheduler-wide blocking or misdelivery. | A03, A05, A07 |
| M3-T05 | Force mailbox, heap, global-table, and continuation exhaustion with tiny capacities. Verify declared outcomes, reservation conservation, funded diagnostics, and continued outer-recovery progress. | A04, A05, A06 |
| M3-T06 | Distinguish actor restart from whole-runtime recovery; verify fresh generations, honest state-loss reporting, stale-authority rejection, and working CLI/service inspection afterward. | A03, A05, A06, A07 |
| M3-T07 | Audit guest imports and rerun inherited CLI/M2 checks alongside the workload. Record GC and same-runtime actor delay separately from independent-domain heartbeat progress. | A01–A07 |

## Ordered phases

4 phases separate independently verifiable outcomes; their section/task/sub-task
counts follow the work rather than a quota. All are draft/not started, with no
execution evidence. Review dependencies and resolve decisions before execution.

| Phase | Integrated outcome | Entry dependency | State / evidence |
| --- | --- | --- | --- |
| [Phase 1 — Compiled profile and atomic loader](phase-01-compiled-profile-and-atomic-loader.md) | Freeze an executable BEAM compatibility boundary and admit its compiler-produced modules atomically under finite loader accounts. | m2-p04-handoff | Draft; not started; tests not run |
| [Phase 2 — Actor interpreter and tracing GC](phase-02-actor-interpreter-and-tracing-gc.md) | Execute admitted BEAM semantics and automatically trace/reclaim private-heap garbage in long-lived actors outside the kernel. | m3-p01-handoff | Draft; not started; tests not run |
| [Phase 3 — Guest adapter and runtime accounting](phase-03-guest-adapter-and-runtime-accounting.md) | Replace host dependencies with the bounded guest substrate and finish runtime accounting without blocking the sole actor scheduler on native work. | m3-p02-handoff | Draft; not started; tests not run |
| [Phase 4 — CLI BEAM and guest conformance](phase-04-cli-beam-and-guest-conformance.md) | Launch the compiled workload from the real CLI and qualify the complete BEAM/GC profile with actor and whole-runtime recovery evidence. | m3-p03-handoff | Draft; not started; tests not run |

Work within each phase follows its task dependencies. The serial order provides
a conservative baseline, not authorization for parallel agents. Independent
experiments may be proposed separately; their results cannot bypass a gate.

## Decision register

The entry choices above remain open. Each row names its resolution task,
evaluation criteria and blocked work; responsible individuals are unassigned.
M0-D01 owns the initial implementation repository and toolchain selection.

| Decision ID | Choice and criteria | Resolution task and phase | Responsible role | Blocks | State |
| --- | --- | --- | --- | --- | --- |
| M3-D01 | Select workload and claimed OTP behavior, exact compiler/oracle/flags/library closure, supported term/opcode/BIF/chunk subset, loader staging and bounded retained-interning policy. | [m3-p01-decisions](phase-01-compiled-profile-and-atomic-loader.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 1 work and its dependent gates | Open; no decision evidence |
| M3-D02 | Choose term/root representation, collection/growth/workspace failure policy, reductions and safe points by correctness, bounded memory, latency risks and implementation complexity. | [m3-p02-decisions](phase-02-actor-interpreter-and-tracing-gc.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 2 work and its dependent gates | Open; no decision evidence |
| M3-D03 | Bind M2 ABI/lifecycle versions, asynchronous continuation/reply rules, capacities, mailbox overload semantics, complete global accounting and responsiveness targets. | [m3-p03-decisions](phase-03-guest-adapter-and-runtime-accounting.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 3 work and its dependent gates | Open; no decision evidence |
| M3-D04 | Freeze the static workload launch catalog, inspection exposure, reproducible comparison suite and acceptance envelope against the accepted profile and M2 authority. | [m3-p04-decisions](phase-04-cli-beam-and-guest-conformance.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 4 work and its dependent gates | Open; no decision evidence |

## Gate-to-phase and artifact mapping

Rows map contributions, not automatic acceptance. The phase task tables give
stable implementation IDs; the integration task exercises the mapped cases
and the handoff task records evidence. Shared cases retain their full definition
above and close only after all required environments and dependent portions pass.

| Phase gate | Artifact contributions | Acceptance coverage | Owning tasks | Entry dependency | Evidence / state |
| --- | --- | --- | --- | --- | --- |
| [M3-P01](phase-01-compiled-profile-and-atomic-loader.md) | M3-A01, M3-A02, M3-A06 | M3-T01, M3-T02 | m3-p01-decisions, m3-p01-loader; m3-p01-integration; m3-p01-handoff | m2-p04-handoff | Not run; evidence absent |
| [M3-P02](phase-02-actor-interpreter-and-tracing-gc.md) | M3-A03, M3-A04, M3-A06 | M3-T01, M3-T03, M3-T05 | m3-p02-decisions, m3-p02-interpreter, m3-p02-gc; m3-p02-integration; m3-p02-handoff | m3-p01-handoff | Not run; evidence absent |
| [M3-P03](phase-03-guest-adapter-and-runtime-accounting.md) | M3-A05, M3-A06 | M3-T02, M3-T03, M3-T04, M3-T05, M3-T07 | m3-p03-decisions, m3-p03-adapter, m3-p03-ledger; m3-p03-integration; m3-p03-handoff | m3-p02-handoff | Not run; evidence absent |
| [M3-P04](phase-04-cli-beam-and-guest-conformance.md) | M3-A01, M3-A02, M3-A03, M3-A04, M3-A05, M3-A06, M3-A07 | M3-T01, M3-T02, M3-T03, M3-T04, M3-T05, M3-T06, M3-T07 | m3-p04-decisions, m3-p04-launch, m3-p04-conformance; m3-p04-integration; m3-p04-handoff | m3-p03-handoff | Not run; evidence absent |

The final phase reruns all M3 acceptance cases for milestone closure.
Earlier contract, fixture, model or hosted results remain partial where guest
integration is required. Scope exclusions and physical obligations in this
definition are unchanged. An acceptance reviewer must retain failure history,
record the accepted tested revision, and reopen gates on incompatible input
changes, missing required evidence or a violated invariant.

## Milestone exit

M3 exits only when all admitted conformance cases and required guest tests pass,
automatic tracing reclamation is demonstrated, and the complete guest substrate
inventory is reviewed. Retain exact revisions, dirty state, build/fixture hashes,
commands, traces, seeds, capacities, observed timing distributions, and ledger
snapshots in dated [journal evidence](../../../50-journal/README.md), with
artifacts in the selected implementation repository or indexed
[archive assets](../../../assets/README.md). Link evidence to M3-A and M3-T IDs.

Unexplained semantic mismatches, unbounded retention, missing guest replacements,
or blocked required tests mean revise or blocked—not conditional completion.
Hand the integrated workload, accepted profile, fault controls, and measured
baseline to [M4](../m4-integrated-recovery-and-resource-campaign/README.md) for
the larger repeated-recovery and resource campaign. M3 smoke demonstrations
must not be reported as that campaign's completion.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 — Compiled profile and atomic loader](phase-01-compiled-profile-and-atomic-loader.md) — Freeze an executable BEAM compatibility boundary and admit its compiler-produced modules atomically under finite loader accounts.
- [Phase 2 — Actor interpreter and tracing GC](phase-02-actor-interpreter-and-tracing-gc.md) — Execute admitted BEAM semantics and automatically trace/reclaim private-heap garbage in long-lived actors outside the kernel.
- [Phase 3 — Guest adapter and runtime accounting](phase-03-guest-adapter-and-runtime-accounting.md) — Replace host dependencies with the bounded guest substrate and finish runtime accounting without blocking the sole actor scheduler on native work.
- [Phase 4 — CLI BEAM and guest conformance](phase-04-cli-beam-and-guest-conformance.md) — Launch the compiled workload from the real CLI and qualify the complete BEAM/GC profile with actor and whole-runtime recovery evidence.

## Maintaining this index

Inventory each future phase here and in Ordered phases. Preserve artifact and
acceptance IDs, map them to actual tasks, and synchronize dependencies and
state with the parent stream. Keep definition review, implementation progress,
and test evidence separate; do not silently narrow the profile after failure.
