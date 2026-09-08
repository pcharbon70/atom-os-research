---
title: "Proof-of-Concept Implementation Planning"
kind: map
created: "2026-09-06"
tags:
  - archive-navigation
  - directory-index
  - implementation-planning
  - proof-of-concept
aliases:
  - "CLI-first OS planning stream"
---

# Proof-of-Concept Implementation Planning (`01-proof-of-concept`)

## Purpose

Translate the existing M0–M4 proof-of-concept roadmap into milestone-scoped
phased implementation plans. The first delivery is a bootable native user-mode
CLI; the completed PoC also demonstrates the required compiled-BEAM profile,
unprivileged process-local tracing GC, protected services, and recovery.

## What belongs here

- A subdirectory named for each milestone with a substantive definition of its
  required outcomes; phase documents are added when dependencies justify them.
- Milestone READMEs describing scope, entry decisions, dependencies, ordered
  phases, and exit evidence.
- Phase notes using the described four-level work hierarchy and ending in
  integration tests, with links back to research and forward to evidence.

Graphical UI, desktop work, an AtomVM implementation path, and unrequested
implementation-repository scaffolding are excluded. Networking, writable
storage, SMP/NUMA, and a second ISA are later capability programs rather than
implicit requirements for the first CLI.

## Current planning state

Five detailed milestone definitions were authored on 2026-09-08. Each names
its required artifacts, observable acceptance cases, open decisions, trust
boundary, exclusions, and handoff evidence. Each now includes a draft phased
implementation plan: M0 has 3 phases, M1 has 4 (including separate physical
qualification), M2 has 4, M3 has 4, and M4 has 3. The 18 phases map artifacts and
acceptance cases to described tasks, dependencies, and final integration gates.
These are conditional plans, not accepted technical decisions or executed work.

All M0–M4 delivery gates remain open and all acceptance cases are not run.
Writing or reviewing these definitions closes none of them. They neither
select the implementation language or bootloader nor initiate implementation.

## Authoritative inputs

- [Readiness assessment](../../20-notes/proof-of-concept-research-readiness.md) —
  defines the M0–M4 outcomes, first CLI delivery, and limits of the PoC claim.
- [Minimal bootable-system inquiry](../../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md) —
  tracks open acceptance gates and demonstrated evidence.
- [Dell Precision T7500 target and minimal QEMU profile](../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) —
  controls the Intel Xeon / Intel 64 target and minimum virtual fixture.
- [Requirement studies](../../20-notes/proof-of-concept-requirements/README.md) —
  supplies proposed contracts, failure cases, and remaining experiments.
- [Proof-of-concept map](../../10-maps/proof-of-concept.md) —
  connects the implementation questions to broader layer research.
- [Planning convention](../README.md) — controls directory naming, descriptions,
  phase-ending integration tests, evidence, and plan review.

## Milestone definitions and dependencies

Read these definitions in order. They explain what each milestone must
accomplish without pretending that later implementation choices are settled.
Phase/task decomposition is linked from each milestone README. Counts reflect
separate decision, implementation, integration, and qualification outcomes;
they are not a quota for future revisions or other milestones.

| Milestone | Detailed definition | Required outcome | Planning dependency |
| --- | --- | --- | --- |
| M0 — Boot inputs | [M0 definition](m0-boot-inputs/README.md) | Pinned build/target/firmware inputs, static CLI image contract, console/time ABI, limits, and exercised validation harness. | Existing target decision and research; remaining choices must be resolved explicitly. |
| M1 — Boot to CLI | [M1 definition](m1-boot-to-cli/README.md) | Atom kernel launches a native user-mode CLI; `help`, `version`, `uptime`, bounded input, invalid commands, and timer progress pass. | M0 contracts and reproducible fixture. |
| M2 — Protected service nucleus | [M2 definition](m2-protected-service-nucleus/README.md) | Protected domains, capabilities, accounts, bounded transport, fault delivery, independent recovery, and real CLI inspection/control. | M1 plus concrete lifecycle, authority, and budget contracts. |
| M3 — Project BEAM runtime | [M3 definition](m3-project-beam-runtime/README.md) | CLI-launched compiler-produced BEAM in the unprivileged project runtime; pinned-profile conformance and automatic local tracing GC. | M2 substrate for guest integration; hosted profile experiments may run earlier when requested. |
| M4 — Integrated recovery and resource campaign | [M4 definition](m4-integrated-recovery-and-resource-campaign/README.md) | Integrated CLI/actor/service/runtime failures, resource limits, reclamation, generation safety, and repeated recovery evidence. | Integrated M2 and M3 with predeclared test budgets and observables. |

M1 is the first delivery, not completion of the BEAM-capable PoC. The milestone
exit criteria remain those in the readiness assessment; writing plans must not
silently weaken them.

## Coverage-by-area traceability

The [readiness assessment's coverage table](../../20-notes/proof-of-concept-research-readiness.md#coverage-by-area)
lists missing decisive artifacts, not eight equally mandatory implementation
programs. The mapping below assigns the in-scope artifacts and preserves the
explicit deferrals. Within each definition, `Mn-Axx` identifies a required
artifact and `Mn-Txx` an acceptance case. These are future delivery obligations,
not implemented artifacts, phase/task IDs, or recorded passing tests.

| Coverage area | Owning milestone artifacts | Required evidence or explicit boundary |
| --- | --- | --- |
| Hardware and architecture | [M0](m0-boot-inputs/README.md): A01–A04, A06–A07 fix the fixture, build, handoff, ABI, harness, and installed-unit record. [M1](m1-boot-to-cli/README.md): A01–A06 supply the actual boot image, protected entry, serial path, and timer. | M0-T01–T06 check executable inputs; M1-T01–T08 check the real guest. Physical T7500 qualification remains separately evidenced; neither q35 nor a second ISA is a motherboard qualification result. |
| Minimal kernel | [M2](m2-protected-service-nucleus/README.md): A01–A02 are the executable object/ABI specification and bounded lifecycle/accounting models; A03–A05 implement their protection, transport, and reclamation contract, extending M0/M1. | M2-T01–T06 require contract/model, authority, race, exhaustion, CPU, and reuse evidence. [M4](m4-integrated-recovery-and-resource-campaign/README.md)-T02 and T04–T06 exercise their integrated behavior under pressure. |
| Managed runtime | [M3](m3-project-beam-runtime/README.md): A01–A06 cover the machine-readable BEAM/OTP profile, compiled corpus, project runtime, automatic process-local tracing GC, guest adapter, and resource ledger. | M3-T01–T07 require actual conformance, loader rejection, GC, asynchronous-call, overload, recovery, and substrate evidence. M4-T02–T05 test the admitted profile under combined load. AtomVM remains excluded. |
| System services | [M2](m2-protected-service-nucleus/README.md): A06–A07 deliver the running volatile supervisor/registry nucleus and real CLI control. [M3](m3-project-beam-runtime/README.md): A07 adds actor and whole-runtime recovery demonstrations. | M2-T07–T08, M3-T06, and M4-T01/T06 distinguish child, actor, CLI, and whole-runtime recovery. Root failure may reset; persistence and universal supervisor survival are not implied. |
| Storage | No writable storage backend or durability barrier is assigned to M0–M4. Read-only boot media is not this missing artifact. | [R14 durability](../../20-notes/proof-of-concept-requirements/durable-state-and-crash-consistency.md) is the proposed first post-M4 capability program. Power-loss and durable-state claims remain blocked until its backend and crash tests exist. |
| Networking | No NIC/stack, secure-channel, or interoperability implementation is assigned to this local PoC. | [R15 networking](../../20-notes/proof-of-concept-requirements/networking-and-remote-actor-boundaries.md) remains a later capability gate. Local IPC evidence does not establish network distribution. |
| Authentication and authorization | [M0](m0-boot-inputs/README.md): A05 declares the trusted-local-development profile. [M2](m2-protected-service-nucleus/README.md): A03/A06/A07 implement and check static authority, bootstrap grants, and permitted CLI operations. | M0-T04 and M2-T02/T04/T08 test that restricted end-to-end authority graph; M4-T02 rechecks isolation under load. Human login, federation, and broader [R18 authority deployment](../../20-notes/proof-of-concept-requirements/authentication-and-administration-profile.md) are not delivered by static grants. |
| Applications and visual computing | [M1](m1-boot-to-cli/README.md): A05 supplies the native CLI; [M3](m3-project-beam-runtime/README.md): A07 supplies a CLI-launched compiled workload; [M4](m4-integrated-recovery-and-resource-campaign/README.md): A02/A06 supply the integrated volatile workload and outcome report. | M1-T02–T03, M3-T01/T06, and M4-T01/T07 require real interaction and repeatable workload evidence. Graphical UI, desktop, and visual user evaluation remain outside this PoC. |

The [requirement studies](../../20-notes/proof-of-concept-requirements/README.md)
provide the supporting R01–R13 contracts and failure cases linked inside these
definitions. R14–R19 cover later durability, networking, DMA, multicore/
portability, broader administration, and update/root-survival programs. They
are not silently added to M0–M4 merely because their research exists. Applicable
PoC constraints, such as static authority and safely leaving extra CPUs unused,
still apply and are called out above and in the milestone definitions.

## Next decision and execution work

Begin with [M0 Phase 1](m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md)
and resolve its repository, language/toolchain, fixture, and inventory decisions.
Later plans are deliberately conditional on those inputs and predecessor
evidence. Before executing each phase, review its decision register and bind
accepted interface versions; revise affected dependencies and tests together
if a decision changes the planned mechanism.

M1 Phase 3 is the first virtual CLI delivery. M1 Phase 4 is its separate physical
T7500 qualification branch; M2 virtual acceptance depends on M1 Phase 3, not
physical qualification or SMP. All physical obligations stay visible and open
until supported by their own evidence.

Every artifact and acceptance case has a phase mapping; its task and evidence
ownership must stay synchronized as decisions resolve. Use the mandatory
milestone/phase templates, descriptions at every
phase/section/task/sub-task level, and a final integration-tests section in
each phase. Determine counts from dependencies, risk, and verifiable outcomes;
do not turn the artifact tables into an arbitrary one-artifact-per-phase quota.

The authored decision tasks must settle these open choices before dependent
implementation, rather than require another broad research cycle:

- Implementation language, freestanding toolchain, linker, reproducible build
  environment, and implementation-repository location.
- Bootloader/handoff, static kernel and user image format, startup memory map,
  and pinned QEMU machine/firmware versions.
- Minimum user/kernel console and time ABI, privilege transition, exception
  handling, interrupt/timer strategy, and initial context-switch requirements.
- Serial test harness, success/failure criteria, resource bounds, and evidence
  artifacts for the first native CLI boot.
- Installed T7500 inventory and the safety/readiness criteria for a later
  physical single-CPU check. Hardware qualification remains distinct from the
  minimal virtual fixture; q35 is not a motherboard replica.

Select and close the exact BEAM workload and compatibility profile in M3 Phase 1
before dependent interpreter commitments; that work does not block M0 or M1. Retain
the selected Intel target and start virtual tests small: one CPU, 128 MiB,
serial I/O, with the full fixture controlled by the linked target profile.
Do not enlarge QEMU topology simply because the lab machine has two packages.

## Stream completion and evidence

Each phase must end with integration tests and a truthful handoff decision.
Physical single-CPU CLI qualification can follow virtual M1 without waiting
for SMP. Do not claim physical qualification from a virtual test, or hosted
runtime conformance as guest M3 evidence.

Close the stream only when the declared M0–M4 acceptance evidence exists and
the governing inquiry records the outcome. Planning completeness, document
counts, and a privileged boot banner are not substitutes for that evidence.

## Index

### Subdirectories

- [M0 — Boot inputs](m0-boot-inputs/README.md) — executable fixture, build,
  handoff, interface, harness, and physical-inventory obligations.
- [M1 — Boot to CLI](m1-boot-to-cli/README.md) — first real user-mode CLI,
  protected boot, serial/time behavior, and guest acceptance.
- [M2 — Protected service nucleus](m2-protected-service-nucleus/README.md) —
  bounded kernel contracts, models, authority, resources, and native recovery.
- [M3 — Project BEAM runtime](m3-project-beam-runtime/README.md) — compiled
  compatibility, interpreter, process-local GC, and guest runtime integration.
- [M4 — Integrated recovery and resource campaign](m4-integrated-recovery-and-resource-campaign/README.md) —
  combined fault/load evidence, repeated reclamation, and PoC acceptance.

### Documents

- None yet.

## Maintaining this index

When a milestone is decomposed, extend its existing definition with ordered
phase links and inventory the new phase notes in that milestone's README.
Preserve artifact/test identities and map them to task and evidence IDs. Update
dependencies, the coverage mapping, and planning/execution state without
implying completion. Keep this stream, the readiness assessment, inquiry,
proof-of-concept map, and journal evidence consistent when scope or acceptance
changes. Do not renumber delivered milestones or phases.
