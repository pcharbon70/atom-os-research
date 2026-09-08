---
title: "{milestone ID} — {milestone name}"
kind: map
created: "{YYYY-MM-DD}"
tags:
  - archive-navigation
  - directory-index
  - implementation-planning
aliases: []
---

# {milestone ID} — {milestone name}

## Purpose

{Describe the milestone outcome, the integrated system boundary, and why this
milestone is needed. Explain how its phases establish the outcome.}

## What belongs here

{Describe included responsibilities and explicit non-goals. Keep the milestone
consistent with its governing roadmap rather than silently expanding it.}

## Planning and delivery state

{Record plan review state separately from execution state and gate results.
An authored plan starts with unchecked work and no claimed test results.}

## Authoritative inputs

{Link the parent stream, governing research, requirements, target profile,
accepted decisions, and predecessor evidence. Explain each input's role.}

## Entry decisions and dependencies

{Separate accepted decisions from assumptions and unresolved choices. For each
open choice record criteria, resolution task, responsible person/role if known,
and the work that cannot begin until it is resolved. Do not invent approval.}

| Decision ID | Choice and evaluation criteria | Resolution task / location | Responsible role | Blocks | State and evidence |
| --- | --- | --- | --- | --- | --- |
| {milestone}-D{NN} | {alternatives and acceptance criteria} | {actual task and phase link, or decomposition pending} | {assigned role or unassigned} | {dependent tasks or gates} | {open, or accepted decision and evidence} |

{Record accepted inputs separately from open choices. Unselected repositories,
toolchains, owners, and limits remain explicit. Rows follow actual decisions.}

## Gate-to-phase and artifact mapping

| Gate / acceptance ID | Required combined result | Artifact IDs | Owning phase and task IDs | Entry dependencies | Evidence and gate state |
| --- | --- | --- | --- | --- | --- |
| {governing gate or case} | {observable result and failure boundary} | {required artifacts} | {authored phase link and stable tasks, or decomposition pending} | {predecessor gates and decisions} | {not run, or actual result and evidence} |

{Map every required artifact and acceptance case without inventing phase files.
Shared artifacts may support several gates. Name exclusions and the authority
for deferral; unmapped obligations are not optional.}

## Ordered phases

{List only actual phase plans in dependency order, each linked relatively.
Include phase ID, outcome, entry dependency, plan/execution state, and evidence
link when available. Add no empty phases merely to fill a fixed phase count.}

{Explain dependency order, permitted independent work, and handoff blockers.
Counts follow scope, risk, and verifiable outcomes. A milestone definition may
say "not decomposed yet" but must not claim to be an executable phase plan.}

## Milestone exit

{Define observable combined acceptance, regression and negative-test coverage,
required environments, evidence, and stop/revise conditions. Link these to the
governing milestone criteria. A writing pass is not completion evidence.}

{State who reviews closure, which evidence revision is accepted, and what
changes reopen a gate. Keep plan, tested, and later merge revisions distinct.
If the selected workflow requires merged-baseline evidence, closure remains
pending until it exists; a merge alone does not demonstrate a passing test.}

## Index

### Subdirectories

- None yet.

### Documents

- None yet.

## Maintaining this index

{Inventory every direct child, including every phase. Keep order, dependencies,
status, scope, and evidence links synchronized with the parent stream and
governing research. Preserve delivered IDs and record supersession explicitly.
Replace every placeholder and empty state that no longer applies.}
