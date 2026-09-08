---
title: "M2 — Protected service nucleus"
kind: map
created: "2026-09-08"
tags:
  - archive-navigation
  - directory-index
  - implementation-planning
  - m2
  - proof-of-concept
aliases: []
---

# M2 — Protected service nucleus

## Purpose

Turn the bootable CLI into a small protected operating system whose services
can fail and be replaced without taking away the kernel, recovery controller,
or all operator access. M2 must demonstrate real authority checks, finite
resource ownership, bounded communication, and safe domain replacement—not
just multiple programs printing messages.

The operator should be able to inspect actual resources and services, request
an authorized restart, observe a new service generation, and continue using
the CLI. A crashing or non-yielding native child must not consume the capacity
needed to diagnose, stop, and replace it. This supplies the substrate on which
[M3](../m3-project-beam-runtime/README.md) can integrate managed execution.

## What belongs here

M2 includes the minimal executable object/ABI contract, bounded lifecycle
models, kernel-enforced domains and capabilities, memory/CPU accounts, copied
bounded transport, fault delivery, and a volatile supervisor/registry nucleus.
Its initial ring-3 services are the CLI, independent outer recovery/control,
and a native test service. Reserve a defined integration path for the later
runtime; do not present a native stand-in as compiled-BEAM execution.

Nested scheduling-context donation, the full proposed kernel object vocabulary,
writable storage, networking, DMA driver recovery, SMP/NUMA, and GUI remain
outside this milestone. Actor supervision and tracing GC belong to M3; their
integration with whole-domain failures belongs to M4. Human login, remote
administration, and recovery-root takeover are not hidden M2 dependencies.

## Planning and delivery state

This is a draft milestone definition, not an authored phased implementation
plan. Required artifacts and acceptance cases below are obligations, not
completed work. Implementation has not started here; no M2 model, guest test,
restart transcript, or performance result is claimed. Writing this definition
does not close an evidence gate or authorize implementation or device writes.

## Authoritative inputs

- [Parent stream](../README.md) and [readiness assessment](../../../20-notes/proof-of-concept-research-readiness.md) — govern M2 and its contribution to the missing decisive artifacts.
- [M1 — Boot to CLI](../m1-boot-to-cli/README.md) — supplies the protected native CLI, console/time contract, and baseline regression evidence.
- [Capabilities and bounded IPC](../../../20-notes/proof-of-concept-requirements/capabilities-syscalls-and-bounded-ipc.md) — specifies authority, admission, funding, and terminal transport obligations.
- [Time and CPU budgets](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — separates domain scheduling, accounting, and observable timing limits.
- [Domain lifecycle](../../../20-notes/proof-of-concept-requirements/domain-lifecycle-and-safe-reclamation.md) — defines close, quiescence, and safe reuse requirements.
- [Independent recovery](../../../20-notes/proof-of-concept-requirements/supervision-and-independent-recovery.md) — governs reserve isolation and replacement topology.
- [Resource accounting](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md) — supplies the capacity/payer ledger and failure-path obligations.
- [Serial CLI](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) — specifies truthful inspection and narrowly authorized restart commands.
- [Administration profile](../../../20-notes/proof-of-concept-requirements/authentication-and-administration-profile.md) — distinguishes local development authority from later identity/security claims.
- [T7500 target](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) — controls Intel x86-64 and the minimal virtual fixture.

## Entry decisions and dependencies

M1's reproducible ring-3 CLI and reviewed M0 build, image, and ABI contracts
are prerequisites for guest acceptance. Keep the Nehalem-v1, one-CPU, 128 MiB,
serial fixture; q35 is not a physical T7500 replica. Hosted models may precede
guest integration but cannot substitute for it.

The following decisions remain unresolved. Their implementing owner is not
yet assigned; future phase plans must assign resolution work before dependent
code is presented as accepted:

- Freeze object/operation encodings, rights, generations, admission points,
  capacities, failure results, and bounded per-call work before implementing
  the extended ABI. Prefer the smallest contract that covers the native demo
  and eventual nonblocking runtime adapter.
- Select CPU replenishment, priorities, periods, budgets, kernel/interrupt
  attribution, and overrun limits before scheduler acceptance. Fixed-period
  budgets need an explicit boundary-burst rule, not a claimed sliding-window
  guarantee.
- Select cleanup batch bounds, identifier-wrap policy, reference/translation
  quiescence checks, quarantine limits, and escalation before enabling reuse.
- Freeze the static authority/resource graph, service readiness protocol,
  restart intensity/backoff, deadlines, and fault-delivery reserve before
  faulting children. Pin numerical response limits and model bounds before
  execution; no measured values are available to inherit from this document.

## Required artifacts and coverage

These artifacts turn the readiness table's missing kernel and system-service
evidence into concrete deliverables. Together they also supply the local
development deployment/authority profile and extend the CLI-operated workload.

### M2-A01 — Executable minimal object and ABI contract

Deliver a versioned operation/capacity table and executable transition tests
for domains/address spaces, capability slots, page/CPU accounts, endpoints,
notifications, timers, and fault records. Each operation specifies rights,
payer, identity/generation, admission point, maximum work, terminal result,
and reuse conditions. Generate or cross-check implementation constants against
the contract; a prose vocabulary alone does not satisfy this artifact.

### M2-A02 — Bounded lifecycle and accounting models

Deliver runnable finite models and fake page/timer/endpoint backends covering
construction, admission, revocation, close, completion, cancellation, and
reclamation. Preserve model versions, bounds, fairness assumptions, explored
properties, and counterexamples. Check reservation conservation and one
terminal transport disposition. Model success is bounded evidence, not proof
that every implementation interleaving is safe.

### M2-A03 — Protected authority and resource substrate

Implement kernel-controlled checked handles, fail-closed grants, domain memory
protection, and capacity/payer ledgers covering pages, page tables, execution
and capability slots, calls/replies, timers, faults, console buffers, and
cleanup metadata. Separate physical backing from attribution. Enforce CPU
accounts, including charged kernel work and declared interrupt overrun, while
keeping recovery's memory, time, fault delivery, and replacement capacity
outside child ownership.

### M2-A04 — Bounded transport and completion handling

Implement server-funded leaf requests with finite payload/copy work and
reserved completion/error capacity before admission. Cover full pools,
uncollected replies, coalesced notifications, timeout/cancel/death races, and
stale completions. Revocation denies new admission; it does not undo effects
already accepted. An unknown application effect must remain distinguishable
from a transport timeout. Expose an adaptation path that will not block M3's
only actor scheduler on one service call.

### M2-A05 — Safe teardown and resource reuse

Implement close-before-cleanup, forced execution stop, bounded cleanup steps,
timer/endpoint retirement, reference quiescence, qualified local x86 translation
invalidation, and page zeroing before transfer. Failed construction unwinds
without publishing callable partial objects. Generations change on replacement;
wrap/overflow cannot resurrect authority. Uncertain resources enter explicitly
bounded quarantine or trigger documented escalation, never silent reuse.

### M2-A06 — Volatile recovery and naming nucleus

Deliver a checked static launch/authority graph and independently funded ring-3
recovery service. Publish names with current generations only after readiness.
Implement child stop/replacement, finite restart intensity/backoff, and
startup/shutdown deadlines. Native-service and CLI faults receive independent
recovery; kernel or recovery-root failure may escalate to a documented reset.
Volatile state loss must be visible rather than described as durable recovery.

### M2-A07 — Real operator control and observation

Extend the CLI with bounded, versioned `mem`, `ps`, and `services` snapshots,
plus `restart <service>` for configured permitted targets. Report actual
accounts, execution domains, and generations; never invent actor counts before
M3. The local development profile trusts the serial operator and boot images,
but ordinary CLI authority remains narrow: no arbitrary image execution,
physical-memory access, or root-capability minting.

## Responsibility and trust boundaries

The ring-0 kernel enforces memory, handles, admission, accounting, scheduling,
fault delivery, and safe object lifecycle. Ring-3 recovery owns launch/restart
policy and volatile naming; the CLI owns parsing and display. The native test
service supplies controllable failures, not trusted enforcement. Ordinary BEAM
processes and their collector remain outside the kernel when M3 adds them.

Guest protection cannot depend on Linux supplying the demonstrated mechanisms.
The host still provides building, QEMU, debugging, and capture; firmware and
the kernel remain trusted. Domain recovery is distinct from actor supervision
inside a healthy runtime. This milestone makes no hostile-shared-runtime,
remote-authentication, physical-timing, or all-supervisor-level survival claim.

## Integration acceptance cases

Cases are proposed acceptance obligations, all not run. Future phases must map
them to described tasks and final integration gates with exact harness commands
and predeclared limits; the table is not a substitute for those phase plans.

| Case | Required integrated observation | Artifacts |
| --- | --- | --- |
| M2-T01 — Contract/model closure | Run finite lifecycle, transport, and conservation checks; retain bounds and counterexamples; cross-check selected operation behavior against fake backends and guest tests. | M2-A01, M2-A02 |
| M2-T02 — Authority rejection | Reject guessed/ungranted handles, malformed buffers, unauthorized mappings/restarts, stale generations, and post-revocation admission without changing unrelated state. | M2-A01, M2-A03, M2-A07 |
| M2-T03 — Completion races | Delay, duplicate, and reorder replies; race timeout, cancellation, revocation, and peer death. Select one terminal transport result without redirecting effects to a replacement. | M2-A02, M2-A04, M2-A05 |
| M2-T04 — Exhaustion with funded recovery | Exhaust each kernel ledger category and combine full calls/fault records with child failure. Denied admission leaves no partial ownership; recovery still has capacity. | M2-A03, M2-A04, M2-A06 |
| M2-T05 — CPU and console progress | Run a non-yielding child, expensive valid syscalls, and serial floods/backpressure. Check charged consumption, boundary bursts/overrun, CLI responses, timer progress, and independent heartbeat against frozen limits. | M2-A03, M2-A07 |
| M2-T06 — Cleanup and generation reuse | Fault construction and intermediate cleanup; retain old handles/timers/readiness messages. Reuse only after quiescence, verify cleared pages and conserved ledgers, and force wrap in a small-width test build. | M2-A02, M2-A05, M2-A06 |
| M2-T07 — Service and CLI recovery | Repeatedly crash/stall the native service and fault the CLI. Observe authorized replacement, changed generations, readiness-gated publication, visible volatile loss, and bounded restart escalation. | M2-A05, M2-A06, M2-A07 |
| M2-T08 — Operator regression | Re-run M1 command/input tests; compare inspection snapshots with kernel/recovery traces and verify permitted and denied restart paths under load. | M2-A03, M2-A06, M2-A07 |

## Ordered phases

No phase documents have been authored. The next decomposition must order
contract/model resolution before dependent enforcement and recovery integration.
Phase, section, task, and sub-task counts must follow actual dependencies and
verifiable outcomes, not the number of artifacts or cases above. Use both the
[milestone template](../../../templates/milestone-plan-readme.md) and
[phase template](../../../templates/implementation-phase.md); each phase ends
with its own described integration-tests section.

## Milestone exit

M2 exits only when M2-A01–M2-A07 exist, all M2-T01–M2-T08 gates pass in their
declared environments, M1 regressions pass, and unresolved failures are not
hidden by changed acceptance. Required blocked/not-run cases keep the milestone
open. Evidence must show actual native recovery and resource conservation,
not merely successful launches using a continually shrinking free pool.

Retain exact revisions/dirty state, tool and fixture identities, commands,
capacity/payer tables, model inputs, serial transcripts, fault schedules,
resource/generation traces, and measured response distributions in dated
[journal records](../../../50-journal/README.md) and indexed
[artifacts](../../../assets/README.md), or an explicitly selected implementation
repository. Distinguish hosted, QEMU, and physical results. QEMU acceptance does
not qualify the physical motherboard or remove a recorded hardware obligation.

The handoff to M3 is a tested user-domain substrate and narrow adapter contract.
[M4](../m4-integrated-recovery-and-resource-campaign/README.md) extends these
tests to managed actors, whole-runtime failure, GC/mailbox pressure, and the
predeclared integrated campaign, including the proposed 1,000 child restarts.
M2 must already demonstrate repeated native recovery; M4 is not permission to
postpone basic stale-handle, reclamation, or reserve-isolation correctness.

## Index

### Subdirectories

- None yet.

### Documents

- None yet; this README is the substantive milestone definition, and phase
  documents have not been decomposed.

## Maintaining this index

Inventory every future phase or other direct child and keep ordered phases,
artifact/case mappings, decisions, and evidence synchronized with the parent
stream and governing research. Preserve delivered identifiers and recorded
failures. Replace empty states when files are added; never infer delivery from
the presence of this definition or from archive validation.
