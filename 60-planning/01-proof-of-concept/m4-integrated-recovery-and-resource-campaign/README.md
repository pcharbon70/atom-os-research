---
title: "M4 — Integrated recovery and resource campaign"
kind: map
created: "2026-09-08"
tags:
  - archive-navigation
  - directory-index
  - implementation-planning
  - m4
  - proof-of-concept
aliases: []
---

# M4 — Integrated recovery and resource campaign

## Purpose

M4 demonstrates that the assembled CLI-operated, BEAM-capable operating system
contains its declared failures and resource pressures. It combines the working
CLI from [M1](../m1-boot-to-cli/README.md), protection and recovery substrate from
[M2](../m2-protected-service-nucleus/README.md), and compiled-BEAM runtime and
tracing collector from [M3](../m3-project-beam-runtime/README.md). Successful
components are necessary inputs, not evidence that their combination works.

The outcome is a reproducible guest campaign with distinct actor, CLI,
native-service and whole-runtime failure results; bounded resource ownership;
safe repeated replacement; and measured responsiveness against limits declared
before testing. More research, a hosted runtime demonstration, or a responsive
boot prompt alone cannot close this milestone.

## What belongs here

This milestone covers a volatile job/counter workload launched through the CLI,
cross-layer fault injection, pressure sweeps, regression checks, measurements,
and evidence sufficient to accept or revise the declared PoC envelope.

It does not add writable storage, networking, DMA drivers, SMP/NUMA, a second
ISA, graphical UI, production authentication, updates, or universal supervisor
survival. AtomVM remains excluded. Later capabilities must not become accidental
dependencies of this single-CPU proof, nor receive claims from its results.

## Planning and delivery state

This is a draft milestone definition, not a decomposed phase plan. It defines
deliverables and acceptance obligations; no implementation or campaign execution
is recorded here. Plan review remains pending, execution is not started, and
all acceptance cases below are not run. Artifact and case IDs support future
traceability, not completed-task claims or authorization to implement.

## Authoritative inputs

- [Planning stream](../README.md) and [readiness assessment](../../../20-notes/proof-of-concept-research-readiness.md) — milestone order, coverage gaps, integrated demonstration and negative acceptance.
- [Measurement study](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — R13 model limits, campaign cases and reproducible measurements.
- [Lifecycle](../../../20-notes/proof-of-concept-requirements/domain-lifecycle-and-safe-reclamation.md) and [independent recovery](../../../20-notes/proof-of-concept-requirements/supervision-and-independent-recovery.md) — R07/R12 quiescence, generations, resource reserves and restart topology.
- [Accounting](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md), [time](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) and [tracing GC](../../../20-notes/proof-of-concept-requirements/private-heaps-and-tracing-garbage-collection.md) — R05/R10/R11 load, ownership and responsiveness obligations.
- [T7500 target profile](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) and [M0](../m0-boot-inputs/README.md) — adopted Intel x86-64 constraints and still-required exact executable fixture.

These are existing research inputs, not newly executed experiments. Prior
milestone evidence must be linked at entry once it exists.

## Entry decisions and dependencies

M4 needs accepted M1–M3 guest evidence, including the static authority graph,
funded recovery reserves, executable lifecycle/accounting contract, conformance
manifest, and GC root/ownership specification. A missing substrate mechanism
returns to its owning milestone; campaign code must not simulate that mechanism.

Before execution, resolve and freeze the following in M4-A01. Responsible
implementation and review roles remain unassigned.

- Pin the inherited image, toolchain, QEMU, versioned machine, SeaBIOS and OTP
  corpus/oracle identities. Preserve the initial TCG, Nehalem-v1, one-CPU,
  128 MiB serial fixture; changes require an explicit decision and comparable
  reruns, not silent enlargement after failure.
- Set workload seeds, durations, repetitions, sweep points, memory partitions,
  queue limits, cleanup reserves, priorities, CPU periods/budgets and overrun
  allowances. Adopt or revise the research's proposed 128 actors, at least one
  million transient allocations and 1,000 child restarts before testing. These
  numbers are proposed inputs, not demonstrated capacity or mandatory phase counts.
- Freeze mailbox admission/failure semantics, restart intensity/backoff,
  readiness/shutdown deadlines, quarantine release/exhaustion rules, and the
  outcome reported for requests whose accepted effects become indeterminate.
- Define each measured interval, clock and p99/maximum-observed target, including
  treatment of warmup, timeout, missing samples and host descheduling. Missing
  target values block a passing performance claim; they are not invented here.

## Integrated trust and failure boundary

The ring-0 kernel owns guest protection, scheduling, accounting, transport and
teardown. Four separate ring-3 domains operate within that boundary:

| Domain or fault location | Required integrated outcome |
| --- | --- |
| CLI domain crashes or floods input | Kernel and outer heartbeat continue; outer control restores the CLI and reports its new generation. |
| Outer recovery/control domain | Launches and replaces configured children from independent reserves; its own failure may escalate to the declared machine-reset policy. |
| BEAM actor inside the runtime | Selected supervision replaces the actor without replacing the runtime; profile-compatible signals and resource cleanup remain observable. |
| Whole managed-runtime domain | Outer control creates a fresh runtime generation; an in-runtime supervisor is not credited with recovering its failed address space. |
| Native test/I/O domain crashes, loops or delays replies | Outer control contains and replaces it; stale, duplicate or malformed completions cannot affect its replacement. |

Firmware, emulator, development image and kernel are trusted. Actor isolation
inside one runtime trusts that runtime; hostile-module sandboxing is not
established. Root/kernel failure may reset rather than recover transparently.
Volatile state loss is reported explicitly, and timeout after admission never
automatically means “no effect.” Physical attacks and speculative channels
remain outside the declared development profile.

## Required artifacts

| ID | Deliverable and required content |
| --- | --- |
| M4-A01 | Executable campaign manifest: requirement-to-case mapping, exact fixture/corpus identities, seeds, quotas, measurement definitions, predeclared limits, and required environments. |
| M4-A02 | CLI-operated integrated workload and fault controls: normal requests and each failure class, real domain/actor generations, permitted administrative authority, and visible volatile/indeterminate outcomes. |
| M4-A03 | Pressure and accounting suite: per-category exhaustion, combined GC/mailbox/call/fault pressure, CPU attribution and overrun, same-runtime delay and independent-domain progress. |
| M4-A04 | Recovery/reclamation suite: construction failure, admission/close races, interrupted cleanup, quiescence before reuse, stale generations, and fixed-capacity restart ledgers. |
| M4-A05 | Reproducible evidence bundle: raw serial/event/timing data, ledger snapshots, commands, harness outcomes, model-to-guest trace mapping, repeated-build identities and retained failures. |
| M4-A06 | Acceptance and limitation report: results against every case, unresolved failures, physical-qualification state, and the proceed/revise/blocked decision linked to the governing inquiry. |

The capacity ledger includes pages, mappings, kernel/capability slots, calls,
timers, faults, buffers and cleanup metadata; runtime heaps, copying workspace,
mailboxes, messages in transit, atoms, code/literals, shared binaries,
continuations and allocator slack. Unsupported categories need an explicit
profile exclusion and rejection test, not disappearance from the ledger.

## Acceptance cases

Each case specifies assembled behavior, not merely an isolated unit test.
Required regressions include the complete admitted M3 conformance corpus and
M1/M2 CLI, protection, authority and lifecycle gates.

| ID | Acceptance obligation | Artifacts |
| --- | --- | --- |
| M4-T01 | Boot the pinned image unattended; start the compiled workload through the CLI; inspect actual services/accounts; reproduce normal requests and the four distinct child/actor failure outcomes above. | A01, A02, A05 |
| M4-T02 | Re-run conformance and hostile-boundary cases under admitted load: invalid profiles cannot publish partial runtime state; unauthorized mappings, capability guesses and malformed buffers cannot modify other domains or kernel state. | A01–A03, A05 |
| M4-T03 | Sweep live set, allocations, mailbox backlog and GC space. Reachable terms survive forced movement; fixed live sets reach bounded post-GC retention; global retention is separately charged. Measure same-runtime actor delay independently of outer-heartbeat progress. | A01, A03, A05 |
| M4-T04 | Exhaust each applicable ledger category, including simultaneous pressure during fault reporting and cleanup. Denied admission leaves no partial ownership/authority; admitted local messages are not silently lost; error paths retain funded capacity. | A01, A03, A05 |
| M4-T05 | Run non-yielding children, syscall/serial floods and allocation storms. Verify CPU consumption plus the declared kernel/interrupt overrun and context ownership; a child cannot spend recovery's reserve. Exercise replenishment-boundary bursts rather than inferring a sliding-window bound from aligned periods. | A01, A03, A05 |
| M4-T06 | Inject failed construction, duplicate/delayed replies, timer cancellation, peer death, close/revocation races and cleanup interruption. Repeated fixed-capacity restarts conserve free/owned/reserved/quarantined totals; local translation, execution and reference quiescence precede zeroing/reuse. Tiny-generation tests cover wrap; stale handles/readiness cannot authorize replacements. | A01, A04, A05 |
| M4-T07 | Rebuild cleanly a second time and repeat the unattended semantic/fault campaign. Reproduce image identities or explain allowed nondeterminism; report numerical CLI, heartbeat, timer, GC, fault-delivery and recovery observations against frozen targets. | A01, A05, A06 |

Table artifact abbreviations A01–A06 refer to M4-A01–M4-A06 above. Bounded
quarantine requires a release condition and exhaustion/escalation policy;
ever-growing allocation to fund successful restarts fails M4-T06. Preserve
model bounds, fairness assumptions and counterexample regressions, but do not
substitute model or fake-backend success for the guest cases.

## Ordered phases

Not decomposed yet. No phase documents or task checkboxes have been authored.
Once predecessor interfaces and the campaign envelope support decomposition,
use the [phase template](../../../templates/implementation-phase.md), with
needs-based phase/section/task/sub-task counts, descriptions at every level,
and integration tests as each phase's final section. Map every artifact and
acceptance case above to those future task IDs.

## Milestone exit

Close M4 only when all required cases pass on the declared integrated fixture,
regressions hold, and reviewed evidence supports the exact workload envelope.
Blocked or unrun cases remain open; failures require correction or an explicit
scope decision, never retroactively relaxed acceptance. Stop or revise for
cross-domain corruption, lost recovery reserves, unbounded cleanup/quarantine,
stale-generation effects, hidden message loss or violated declared limits.

Retain raw observations, sample counts, revision/dirty state, build and binary
hashes, host/acceleration configuration, commands and limitations in dated
[journal evidence](../../../50-journal/README.md), with artifacts in
[assets](../../../assets/README.md) or the selected implementation repository.
Label maxima “maximum observed”; QEMU regression timing is not physical WCET.

The T7500's installed inventory and physical qualification remain distinct from
virtual results. Physical single-CPU CLI qualification can occur after M1;
M4 neither requires SMP nor silently cancels a required physical test when the
machine is unavailable. Any physical claim needs its own qualified fixture and
recorded runs. This definition authorizes no device writes.

The handoff records the PoC outcome in the
[governing inquiry](../../../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md),
retains broader inquiries as open, and identifies remaining capabilities. A
durable local CLI service is the readiness assessment's proposed next program,
not a delivered M4 feature or automatic authorization to begin it.

## Index

### Subdirectories

- None yet.

### Documents

- None yet; this README is the substantive milestone definition.

## Maintaining this index

Inventory every future phase and direct child, preserve artifact/case IDs,
and link implementation evidence without replacing failure history. Keep phase
order, dependencies, scope and actual gate state synchronized with the parent
stream, readiness assessment and governing inquiry. Replace empty states when
documents are created; writing or reviewing this definition closes no gate.
