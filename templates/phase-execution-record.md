---
title: "{YYYY-MM-DD} — {milestone} phase {NN} execution record"
kind: journal
created: "{YYYY-MM-DD}"
tags:
  - implementation-planning
aliases: []
---

# {YYYY-MM-DD} — {milestone} phase {NN} execution record

{Describe what was actually attempted and the bounded conclusion supported by
this run. Copy into 50-journal/YYYY-MM-DD-{milestone}-phase-{NN}.md when recording
execution, not to manufacture prospective evidence. Update the journal index
and link this record from the phase and milestone.}

## Plan and acceptance baseline

{Link the milestone and phase with exact revisions, stable task IDs, artifacts,
requirements, and gate cases evaluated. Record predeclared limits and expected
outcomes, not limits adjusted after failure.}

## Environment and provenance

{Record implementation repository, full tested commit and dirty state, build
inputs and hashes, tools, host, guest/physical target, firmware, configuration,
seeds, resource limits, and clocks. Distinguish hosted, QEMU, and physical
evidence and identify host-provided services. Redact secrets and device IDs.}

## Execution and results

| Task / case IDs | Fixture and exact command | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- | --- |
| {stable task and case IDs} | {reproducible invocation} | {predeclared criterion} | {observed output or why not run} | {pass / fail / blocked / not run} | {relative link or exact implementation artifact reference} |

{Include assembled-phase tests, earlier regressions, negative cases, and all
required blocked/unrun cases. Preserve unsuccessful attempts, outputs, sample
counts, and limitations. Commands without observations are not execution
evidence. Store attachments in assets or the selected implementation repository
and update affected inventories.}

## Review and handoff

{Record reviewer/role or review pending, actual proceed/revise/blocked decision,
unresolved failures, corrective work, and the next entry gate. Identify changes
that reopen acceptance. Required blocked/unrun tests stay open; parents close
only after all children and applicable gates pass.}

{Distinguish tested commit, evidence-record revision, and any later merge SHA
and date. Record merge provenance only if it exists and is relevant; do not
infer merged-candidate verification from pre-merge tests. If required evidence
is absent, closure stays pending. Update checkboxes only from verified results.
This record authorizes no commit, push, PR, or device write.}

## Source manifest

{For deep-dive research, use the required -deep-dive.md filename and the journal
template's exhaustive manifest rules. Otherwise remove this section if not
applicable. Use one list item per source, exactly one relative source-note link,
an em dash and its role. Use exactly "- None." for an empty category.}

### Newly introduced sources

{List sources first introduced in this exact session, or - None.}

### Reused sources

{List existing sources substantively used in this session, or - None.}

## Follow-ups

{Link unresolved questions, corrective work, and prospective reading. Preserve
this run's observations when subsequent execution supersedes its outcome.}
