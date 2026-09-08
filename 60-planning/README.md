---
title: "Implementation Planning"
kind: map
created: "2026-09-06"
tags:
  - archive-navigation
  - directory-index
  - implementation-planning
aliases:
  - "Planning index"
---

# Implementation Planning (`60-planning`)

## Purpose

Turn research milestones into phased implementation plans with explicit scope,
dependencies, described work, and phase-ending integration tests. A plan states
what must be built and demonstrated; it is not evidence that either happened.
The first stream is the [CLI-first proof of concept](01-proof-of-concept/README.md).

## What belongs here

- Numbered planning streams grouping related milestones.
- Milestone-named subdirectories containing a substantive definition and
  exhaustive README, with one note per phase when the work is decomposed.
- Entry decisions, dependencies, task-level acceptance criteria, test plans,
  and links to the research and execution evidence they depend on.

Research arguments remain in `20-notes/`, primary-source records in
`30-sources/`, open research questions in `40-inquiries/`, and local experimental
evidence in `50-journal/` with attachments in `assets/`. This directory is not
the kernel source tree and does not select an implementation repository.

## Directory and identity convention

Use a stable stream number and name, then the existing milestone ID and name.
For example, [M0 — Boot inputs](01-proof-of-concept/m0-boot-inputs/README.md)
contains a detailed milestone definition. Its directory is
`01-proof-of-concept/m0-boot-inputs/`; phase/task decomposition and implementation
remain distinct: authored phases are linked there, but no implementation
progress is implied by their existence.

Each milestone directory contains `README.md`; authored phases use files named
`phase-01-<descriptive-name>.md`, `phase-02-<descriptive-name>.md`, and so on.
Phase numbers restart at 01 in each milestone. Keep delivered identifiers
stable; record supersession explicitly instead of renumbering history.

Use the [milestone README template](../templates/milestone-plan-readme.md) for
scope, decisions, phase ordering, dependencies, status, and milestone exit
evidence. It extends the ordinary directory README invariant; every direct
child still belongs in its index. Use the
[phase template](../templates/implementation-phase.md) for each phase.
Create no empty milestone directories or dummy phase files simply to populate
an index. A substantive milestone definition can precede phase documents, but
must identify that state explicitly and explain the required outcomes and
acceptance evidence. There is no required number of phases or children per
work item.

Directory READMEs use `kind: map`. Phase notes use `kind: note`, initially
`maturity: developing`, and the tag `implementation-planning`. Keep planning
status and decision state in the body, not in invented frontmatter fields.

## Work hierarchy and descriptions

Each phase document contains one numbered checkbox hierarchy:

| Level | Example identity | Description required immediately below the label |
| --- | --- | --- |
| Phase | `1 Phase` | Integrated outcome, scope, and what the phase establishes. |
| Section | `1.1 Section` | Coherent responsibility and its contribution to the phase. |
| Task | `1.1.1 Task` | Concrete deliverable, important constraints, and completion check. |
| Sub-task | `1.1.1.1 Subtask` | Bounded action, expected result, and verification or parent-test reference. |

At every level, put a descriptive paragraph before children, commands, or
acceptance bullets. Labels such as “Implement loader” are not descriptions.
Sub-tasks need their own descriptions even when their titles are detailed.
Indent descriptions with their list item so the hierarchy renders correctly.

Identify the responsible layer, privilege boundary, target, and host-provided
services where relevant. Link the requirement or decision being implemented.
An unresolved choice must have a decision task, alternatives/evaluation
criteria, a resolution point, and the dependent work it blocks. Do not write
later work as though an unselected language or bootloader has been accepted.

## Task identity and gate mapping

Every task, including integration and handoff work, has a stable symbolic ID
qualified by milestone and phase, such as `m0-p01-build-inputs`. Preserve the
numbered hierarchy as well. Task labels use `[id: ...]`, `[repo: ...]`, and
`[after: ...]`; the phase's ownership/traceability table records responsible
roles, requirements, artifact/case IDs, and expected completion evidence.
These fields are body conventions, not new frontmatter or executable directives.

IDs are not automatic Markdown anchors. Cross-phase references include the
owning document link and exact ID. Review dependencies for missing targets,
cycles, and incompatible entry gates. Use `none` for genuine independence;
use an explicit unresolved state and decision blocker when inputs are unknown.
Do not invent an implementation repository or assigned person.

The milestone README maps every artifact and acceptance obligation to actual
phases/tasks, records decision owners and blockers, and explains phase order.
Use `decomposition pending` where phase plans do not yet exist. Independent
work may be identified when dependencies and edit ownership permit it; a plan
does not itself authorize delegation or execution. Counts at all levels remain
needs-based. Preserve existing IDs and verified state when extending a plan.

## Phase-ending integration tests

The final section of every phase is named `Phase N Integration Tests`. It uses
the same description/task/sub-task structure, with no later work section or
appendix. Put scope, dependencies, research links, and other context before
the work hierarchy. Keep evidence and handoff tasks inside the final section.

Define the following before executing the gate:

- The assembled artifacts/contracts being tested and the relevant earlier
  behavior that must continue to work.
- The fixture, pinned inputs, privilege/host boundary, setup, and runnable
  command or harness deliverable. Resolve any harness placeholder before
  claiming execution.
- Observable success criteria and predeclared limits, plus relevant malformed
  input, fault, exhaustion, timeout, or other negative cases.
- Reproducibility information: revision and dirty state, tool versions,
  configuration, artifact identities, commands, outputs, and limitations.
- Evidence destination, required review, and the proceed/revise/blocked
  decision that controls handoff to the next phase.

A documentation or contract phase tests the consistency of its combined
outputs and rejection of contradictory inputs; it does not need to pretend
the OS already boots. A code phase must test the relevant components together;
unit tests and archive validation alone are not OS integration evidence.
Keep virtual, hosted, and physical results distinct. Passing QEMU checks does
not qualify the T7500 motherboard or establish physical timing guarantees.

## Status, evidence, and review

Record plan review, execution progress, and gate results separately. A useful
body record distinguishes a draft/reviewed plan, not-started/in-progress/blocked/
complete execution, and not-run/pass/fail/blocked tests. These are reporting
conventions, not new schema enums or inferred authorization.

Start all work checkboxes unchecked. Mark an item complete only when its
deliverable and required verification exist, with evidence linked by task ID.
Mark a parent complete only after its children and relevant gate pass. Record
failed attempts and unrun tests honestly. An unavailable required environment
does not automatically become optional; any scope change needs an explicit
decision and the remaining obligation must stay visible.

Keep execution evidence in a dated journal entry (the
[journal template](../templates/journal.md) applies; the optional
[phase execution record](../templates/phase-execution-record.md) specializes it
for implementation runs); link it from the phase's
final section and milestone README. Record actual outputs, not only commands
someone intends to run. An implementation repository may own test artifacts
after that location is selected; link an exact revision and artifact identity.

An execution record identifies the plan baseline, stable task/case IDs, full
tested commit and dirty state, environment, commands, raw results, limits,
review, and proceed/revise/blocked decision. Keep plan revision, tested revision,
and any later merge revision distinct. Record a merge SHA/date only when it
exists and is relevant; never infer merged-candidate verification from a merge
alone. Required evidence keeps closure pending until it is supplied. Preserve
failed attempts and explicit gate-reopening conditions.

The specialized template is optional; recording required execution evidence is
not. It creates no new metadata kind or mandatory commit-per-section,
PR-per-phase, or closure-PR policy. No execution records are created merely to
make a plan appear complete. For a session that also constitutes a deep dive,
retain the journal source-manifest and filename requirements.

Before calling a plan ready for implementation, review every level for a real
description, complete dependencies, traceable requirements, bounded work,
testable acceptance, and a final integration gate. The archive validator checks
metadata, filenames, links, and inventories, including this planning area. It
does not yet enforce the work hierarchy or assess test adequacy.

Plan acceptance is not implementation evidence and does not itself authorize
implementation, installation, commits, pushes, PRs, publishing, or device writes.
Follow the actual user request and [repository instructions](../AGENTS.md).

## Reference corpus and deliberate adaptations

The local BlazeX browser-host planning stream was inspected read-only on
2026-09-06 at
`/home/ducky/code/blazex/docs/research/60-planning/01-browser-host`.
The reference included its stream index, the BH-00 milestone README and
terminology phase, and the BH-04 authorization/handoff phase.

We adopt its stream/milestone/phase organization, numbered work hierarchy,
research traceability, and separation of plans from completion evidence. The
user's requirement is stronger than those sampled phase files: every sub-task
here also needs an opening descriptive paragraph. Phase documents here end
with the integration-tests section rather than appending delivery rules or
connections afterward.

We do not import fixed child counts, automatic per-section commits or phase
PRs, automatic environment deferrals, or BlazeX architecture/runtime choices.
AtomVM remains rejected. The reference is a planning example, not authority
over this project's technical scope or implementation permissions.

## Index

### Subdirectories

- [01 — Proof of concept](01-proof-of-concept/README.md) — five detailed M0–M4
  definitions and 18 draft phases, with decision/task dependencies,
  coverage-to-artifact mapping, and integration gates for the CLI-first OS.

### Documents

- None yet.

## Maintaining this index

Inventory every stream through its README. When a milestone or phase is
created, update its parent inventories, the stream's status, and the relevant
conceptual map together. Keep the convention synchronized with
[`AGENTS.md`](../AGENTS.md) and the planning templates. Preserve superseded
plans and evidence rather than silently rewriting accepted work.
