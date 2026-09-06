---
title: "Phase {N} — {phase name}"
kind: note
created: "{YYYY-MM-DD}"
maturity: developing
tags:
  - implementation-planning
aliases: []
---

# Phase {N} — {phase name}

{Describe the phase outcome, its system boundary, and why it is needed now.}

Back to milestone: [README](README.md).

## Entry, scope, and dependencies

{Record prerequisites, accepted and unresolved decisions, implementation
location, privilege/host boundary, target fixture, included work, and non-goals.
Keep plan review state, execution state, and test results separate.}

## Research and acceptance traceability

{Add relative links to governing requirements, decisions, predecessor evidence,
and the parent planning convention. Map requirements to task IDs and gate cases.
Put all contextual references here, before the work hierarchy.}

## Planned work

<!-- Replace N with the phase number. Add as many substantive sections, tasks,
and sub-tasks as necessary; the two-section shape below is only a scaffold.
Keep labels and descriptions separate at all four levels. Keep the final
Integration Tests section last, moving its number as sections are added. -->

- [ ] {N} Phase — {phase name}.

  {Describe the integrated change this work will establish and the outcome
  that the phase-ending gate must demonstrate.}

  - [ ] {N}.1 Section — {coherent work section}.

    {Describe this section's responsibility, boundaries, and contribution to
    the phase before listing its tasks.}

    - [ ] {N}.1.1 Task — {concrete deliverable}.

      {Describe the artifact or behavior to deliver, its constraints, and the
      completion check before listing sub-tasks.}

      - [ ] {N}.1.1.1 Subtask — {bounded action}.

        {Describe the inputs, change or experiment, expected result, and how
        it will be verified. A detailed title alone does not fill this role.}

  - [ ] {N}.2 Section — Phase {N} Integration Tests.

    {Describe how the assembled phase and relevant earlier behavior will be
    exercised together, including negative cases and the handoff decision.}

    - [ ] {N}.2.1 Task — Verify the integrated outcome and regressions.

      {Describe the system/contracts under test, success criteria, failure
      model, predeclared limits, and required target environments.}

      - [ ] {N}.2.1.1 Subtask — Run the integrated acceptance path.

        {Specify fixture, setup, pinned inputs, exact command or harness
        deliverable, observable outputs, and pass/fail criteria. For an early
        contract phase, test the combined contracts without claiming a boot.}

      - [ ] {N}.2.1.2 Subtask — Exercise negative cases and inherited behavior.

        {Specify relevant faults, malformed input, bounds, timeout/exhaustion,
        and earlier behavior to recheck. Define expected rejection/containment
        and observables; justify cases that are genuinely not applicable.}

    - [ ] {N}.2.2 Task — Record evidence and decide phase handoff.

      {Describe the reproducible evidence and review needed to proceed, revise,
      or stop. A required blocked or unrun test keeps the gate open.}

      - [ ] {N}.2.2.1 Subtask — Publish the execution record.

        {Link a dated journal and exact artifacts to task/test IDs. Record
        revision and dirty state, tool versions, configuration, commands,
        outputs, hashes, limits, and actual pass/fail/not-run/blocked outcomes.
        Distinguish hosted, QEMU, and physical results.}

      - [ ] {N}.2.2.2 Subtask — Review completion and update the milestone.

        {Check every deliverable and required gate against evidence; record
        unresolved issues, accepted scope changes, and the next phase's entry
        conditions. Update checkboxes and the milestone index truthfully.
        This decision does not itself authorize new implementation or Git actions.}
