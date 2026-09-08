# Repository instructions

These instructions apply to the entire repository. This is a Markdown research
archive, not a conventional software project. Preserve room for exploratory
thought while keeping provenance, navigation, and document structure reliable.

Follow an explicit user request when it conflicts with this file. Otherwise,
use these conventions for every document and organizational change.

For any phased implementation plan, use the mandatory
[phase template](templates/implementation-phase.md) and
[milestone README template](templates/milestone-plan-readme.md). Before creating,
expanding, revising, or reviewing such a plan, read both templates and follow
[Phased implementation planning](#phased-implementation-planning) below. This
applies to every milestone and planning stream, not only the proof of concept.

## Project goal

This project researches and develops a new kernel and operating system based on
the principles embodied by Erlang/OTP and the BEAM virtual machine. It is not
tied to a particular BEAM implementation or intended merely to run an existing
runtime as an application on top of another operating system.

Running compiled BEAM code is a platform requirement. Preserve BEAM's managed
execution contract, including automatic process-local tracing garbage
collection, while keeping the collector and ordinary BEAM processes outside
the privileged kernel. Compatibility does not make the BEAM instruction set a
kernel ABI or require one particular VM implementation; record the exact BEAM
and OTP compatibility profile and verify it with conformance tests.

AtomVM has been explicitly rejected as an implementation foundation. Do not
propose an AtomVM port, reuse experiment, dependency, or comparison milestone
for the proof of concept. Preserve existing AtomVM research as historical
provenance rather than an active implementation path.

The proof of concept targets a minimal bootable operating system with a CLI.
Its first delivery boots into a minimal interactive command environment;
graphical UI and desktop work are outside this proof-of-concept scope. A
native CLI can precede the managed runtime, but the completed proof of concept
must still meet its declared compiled-BEAM and process-local tracing-GC profile.

The initial physical target is the Dell Precision T7500 with Intel Xeon
processors and Intel 64/x86-64. The user explicitly corrected the AMD-processor
assumption. Follow the target profile in
`20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md`.
Start QEMU tests with the Nehalem-v1 fixture, one CPU, 128 MiB and serial I/O;
add SMP, socket/SMT topology and NUMA only when their tests require them.
Two multicore packages are user-reported; exact Xeon SKUs, enabled threads,
RAM, board revision, firmware and device inventory remain unverified.
Use Intel architecture and processor-family references for this target.
“AMD64” remains valid in shared ISA/ABI names, but AMD-specific processor
research and the former Opteron fixture do not gate this PoC. RISC-V/OpenSBI
remains comparative and historical first-target research.

Keep research and implementation work oriented toward carrying principles such
as lightweight isolated processes, message passing, supervision, fault
containment, responsiveness, and distribution into the kernel and the wider
system architecture. Relevant areas include boot and bring-up, hardware
abstraction and drivers, scheduling, memory management, isolation and
capabilities, persistence, networking, tooling, and the path from a research
prototype to a bootable system.

Distinguish clearly among:

- principles inherited from OTP and the BEAM model;
- behavior specific to existing OTP or BEAM implementations;
- behavior inherited by a prototype from a host operating system or platform
  port;
- behavior the new kernel and operating system would need to own;
- evidence demonstrated by an experiment; and
- proposed architecture that remains unverified.

## Archive principles

- Folders describe what a document is doing; maps, links, and tags describe
  what it is about.
- Prefer a small stable top-level structure over speculative subject folders.
- Preserve provenance. Separate a source's claims, our synthesis, local
  experimental evidence, and unresolved questions.
- Keep navigation useful at two levels: directory READMEs are complete local
  inventories, while maps are selective conceptual paths.
- Treat `frontmatter.schema.json` as the authoritative metadata contract.
- Keep related changes atomic: change a document and every affected index,
  link, and map together.

## Canonical structure

```text
00-inbox/       Unprocessed, temporary captures
10-maps/        Curated paths through subjects and questions
20-notes/       Ideas and syntheses in the author's own words
30-sources/     Reading notes and bibliographic records
40-inquiries/   Active questions and research workbenches
50-journal/     Dated observations and research-session evidence
60-planning/    Milestone-scoped phased implementation plans
90-archive/     Inactive or superseded material worth retaining
assets/         Images, PDFs, diagrams, datasets, and attachments
templates/      Starting points for documents and directory indexes
```

Do not add or rename a top-level directory unless the user asks or a repeated,
demonstrated need makes the existing structure inadequate. Organize subjects
through tags, links, and maps first.

## Sources of truth

Use these files for different decisions:

1. `frontmatter.schema.json` defines valid metadata fields and values.
2. `templates/` defines the minimum starting structure for each artifact.
3. The root `README.md` explains the archive to human readers.
4. Each directory's `README.md` describes and inventories that directory.
5. `10-maps/` provides curated thematic navigation.
6. `validate_archive.py` performs deterministic structural checks.

If documentation and the filesystem disagree, inspect the intended change and
bring them back into sync. Never preserve a stale index merely because it was
previously written.

## Directory README invariant

Every archive directory, including a future nested directory, must contain a
`README.md`. Create it from `templates/directory-readme.md` as part of creating
the directory, except milestone-plan directories, which must use
[`templates/milestone-plan-readme.md`](templates/milestone-plan-readme.md).
That specialized template preserves the same directory README invariant.

Directory READMEs must:

- use valid frontmatter with `kind: map` (the root README is the exception);
- include `## Purpose`, `## What belongs here`, `## Index`, and
  `## Maintaining this index`;
- list `### Subdirectories` and then `### Documents`, `### Files`, or
  `### Templates` under the index;
- inventory every direct child except the README itself;
- link entries relatively and explain their role;
- state an explicit empty state when a category has no entries; and
- link a child directory through its README rather than its bare path.

Whenever content is added, moved, renamed, archived, or removed, update every
affected directory README, map, and meaningful body link in the same change.
Do not index `.git`, generated caches, editor state, or similar machinery.

## Frontmatter contract

Every durable knowledge document and directory README begins with YAML
frontmatter that validates against `frontmatter.schema.json`:

```yaml
---
title: "A human-readable title"
kind: note
created: "2026-08-28"
tags: []
aliases: []
---
```

Additional requirements depend on `kind`:

- `note` requires `maturity: seed | developing | stable`.
- `inquiry` requires `status: open | paused | resolved`.
- `source` may use `authors`, `published`, `citation_key`, `container`,
  `edition`, `isbn`, `doi`, `url`, and `accessed`.
- `map` and `journal` use the common fields.

Quote dates in `YYYY-MM-DD` form. Use the archive document's creation date,
not its subject's publication date. Use lowercase kebab-case tags, YAML lists
for tags and aliases, `[]` for an intentionally empty list, and `null` for an
unknown nullable value. Never invent missing source metadata. Do not add an
`updated` field by hand; revision control records history.

The root `README.md`, `AGENTS.md`, validation scripts, and validation
requirements are repository documentation or tooling and do not use archive
frontmatter. Template placeholders are exempt until copied and filled. A
transient inbox capture may be incomplete, but it must validate before
promotion. Binary assets do not use frontmatter; document them in their local
directory README.

## Document roles and templates

| Artifact | Destination | Template | Intended result |
| --- | --- | --- | --- |
| Directory index | Any archive directory's `README.md` | `templates/directory-readme.md` | An exhaustive local inventory |
| Conceptual map | `10-maps/` | `templates/map.md` | A selective route through related work |
| Note | `20-notes/` | `templates/note.md` | An idea, argument, model, or synthesis |
| Source note | `30-sources/` | `templates/source.md` | A bibliographic record and evidence-focused analysis |
| Inquiry | `40-inquiries/` | `templates/inquiry.md` | A live question, hypotheses, findings, and outcome |
| Journal entry | `50-journal/` | `templates/journal.md` | A dated observation or reproducible research-session record |
| Milestone plan index | `60-planning/<stream>/<milestone>/README.md` | `templates/milestone-plan-readme.md` | Scope, decisions, ordered phases, and milestone acceptance |
| Implementation phase | `60-planning/<stream>/<milestone>/phase-NN-<name>.md` | `templates/implementation-phase.md` | Described work hierarchy ending in integration tests |

Copy the closest template, replace every placeholder, and adapt its headings
only as the material requires. Do not add a document kind when an existing role
plus links or tags expresses the same work.

## Phased implementation planning

### Mandatory templates and workflow

Before drafting or reviewing a phased implementation plan, read the
[planning convention](60-planning/README.md) and both required templates in full:

- [Milestone plan README](templates/milestone-plan-readme.md) — the required
  starting point for each milestone directory's `README.md`.
- [Implementation phase](templates/implementation-phase.md) — the required
  starting point for every phase document, including its described work
  hierarchy and final integration-tests section.

Do not substitute a generic note template, flat task list, or prose-only
roadmap for a requested phased implementation plan. For a new plan, copy and
fill the appropriate templates. For an existing plan, check and adapt its
structure against them without recreating the document, renumbering accepted
work, erasing evidence, or resetting verified completion state. Replace all
placeholders before handoff. An explicit user request for a different format
takes precedence over this default.

### Required location and structure

Use `60-planning/` to translate research milestones into phased implementation
plans. Follow its README for the full convention. Planning streams use a stable
number and descriptive name, such as `01-proof-of-concept`. Each milestone has
its own subdirectory named for its existing ID and milestone name, such as
`m0-boot-inputs`; do not rename milestones merely to fit a template.

- A stream README records scope, milestone order, dependencies, and current
  planning state. A milestone README uses the specialized directory template
  and records authoritative research, entry decisions, ordered phases, and exit
  evidence. Both remain `kind: map` and satisfy the directory README invariant.
- Each phase is one `kind: note`, initially `maturity: developing`, named
  `phase-NN-<descriptive-name>.md`. Phase numbering restarts within each
  milestone. Use a numbered checkbox hierarchy: phase, section, task, sub-task.
- Every phase, section, task, and sub-task starts with a descriptive paragraph
  immediately below its label and before its children or other content. A
  title, checkbox, or imperative alone is not the description. Explain the
  intended result and relevant boundary; tasks and sub-tasks identify concrete
  deliverables and how completion will be checked.
- The last section of every phase is `Phase N Integration Tests`. It has its
  own description, tasks, and described sub-tasks. Cover the assembled phase,
  relevant earlier behavior, failure cases, reproducible evidence, and the
  handoff decision. Place references and other context before the work hierarchy
  so nothing follows this final section in the phase document.
- Determine the number of phases, sections, tasks, and sub-tasks from the actual
  work required: scope, dependencies, complexity, risks, and independently
  verifiable outcomes. Counts may differ between milestones, phases, sections,
  and tasks. Never impose an arbitrary number, uniform count, or template-derived
  quota at any level. Do not pad, split, merge, or omit necessary work merely to
  reach a target count; template examples illustrate structure, not quantities.
- Use stable hierarchical IDs; do not renumber delivered work or silently
  change acceptance after a failed test.
- Give every task a stable milestone/phase-qualified symbolic ID in addition
  to its hierarchy number, including integration and handoff tasks. Use
  `[id: ...]`, `[repo: ...]`, and `[after: ...]` in task labels and maintain the
  phase ownership/traceability table. Link requirements, artifacts, acceptance
  cases, responsible roles, and evidence expectations. These IDs are not
  automatic Markdown anchors; cross-phase references include the document link.
  Review dependency targets and cycles. Unselected repositories and unassigned
  roles stay explicit, with decision blockers; never invent acceptance.
- Maintain the milestone decision register and gate/artifact-to-phase mapping.
  Map every required obligation to actual tasks, or mark decomposition pending
  when phases are not authored. Record exclusions explicitly. This mapping
  neither closes gates nor changes needs-based counts.
- Keep plan review, implementation progress, and test results distinct in body
  text. Checkboxes record verified delivery, not the act of writing a plan.
  A parent is complete only when its children and applicable gates pass. Required
  tests that are blocked or not run remain open; they are not implied passes.
- Link each phase to its milestone and the research/decisions it implements.
  Record local execution evidence in dated `50-journal/` entries and artifacts
  in `assets/` (or an explicitly selected implementation repository). Link exact
  evidence to task IDs and update indexes together.
- Do not create empty milestone directories or placeholder phase documents to
  make a roadmap look implemented. Decompose the near-term milestone first and
  keep later milestones at roadmap depth until their inputs justify detail.
- A plan does not itself authorize implementation, commits, pushes, PRs,
  publishing, installation, or physical-device writes. Follow the user's actual
  request and preserve the existing authorization and safety rules.

The archive validator checks planning metadata, placement, links, and directory
inventories. Description quality, hierarchy completeness, and integration-test
adequacy require review; no automated phase-shape enforcement is claimed.

The optional [phase execution record](templates/phase-execution-record.md)
specializes the journal template for actual implementation evidence. Use
`kind: journal` in `50-journal/`, update its index, and link records from the
phase and milestone. Record task/case IDs, tested revision and dirty state,
environment, commands, actual results, raw artifacts, limitations, review, and
handoff. Distinguish tested, plan, and later merge revisions; missing required
merged-baseline evidence keeps closure pending. Preserve failed attempts and
gate-reopening conditions. Deep-dive sessions retain their source-manifest
rules. The template is optional, required evidence is not, and it does not
authorize a commit-per-section or PR-per-phase workflow.

## Filenames and paths

- Use lowercase kebab-case Markdown filenames.
- Name notes and maps for their subject, not their creation date.
- Name inquiries as concise questions in kebab case.
- Name journal entries `YYYY-MM-DD.md`; add a short suffix if needed.
- Prefer `<author>-<year>-<short-title>.md` or
  `<lead-author>-et-al-<year>-<short-title>.md` for source notes.
- Use relative Markdown links for local documents and assets.
- Before moving a file, find and repair every incoming link.

## Markdown viewing

Open Markdown documents for interactive viewing with the MarkText utility.

## Producing research

Before creating a durable document, read this file, the root README, the
destination README, the relevant template, and the schema. Search for an
existing document that already serves the need. Add a meaningful body
connection or place the document on a relevant map, then update the destination
README in the same change.

A deep dive should preserve both its evidence trail and resulting model.
Unless the user requests another shape, create or update this connected bundle:

1. a synthesis note in `20-notes/`;
2. a source note in `30-sources/` for each substantively used primary work;
3. an inquiry in `40-inquiries/` while the central question remains open;
4. a topic map in `10-maps/`;
5. the home map when the topic belongs at the archive entry point;
6. journal evidence for material local experiments; and
7. every affected directory README.

Every deep-dive journal must contain an exhaustive `## Source manifest` with
`### Newly introduced sources` and `### Reused sources`. “Newly introduced”
means the source note first entered the archive during that exact dated
session; “reused” means a source note already existed and substantively
informed the session. Name deep-dive journal files with the `-deep-dive.md`
suffix. In each category, use one Markdown list item per source with exactly
one inline relative source-note link, followed by an em dash and a concise role
description. Use exactly `- None.` when a category is empty. A source may be
reused by many sessions but may have only one introducing session. Topic maps
remain selective conceptual routes; the journal manifest is the authoritative
curated session-level provenance record. Matching creation dates are only a
consistency check, not proof that a source originated in a session; use the
journal evidence and revision history to resolve ambiguous ordering.
Every local source-note link outside `## Threads` and `## Follow-ups` is treated
as substantive session evidence and must appear in one manifest category.
Prospective or merely contextual source-note links belong under those two
sections; an incidental external citation does not require a source note.

Research method:

- Define the question, scope, terminology, and an operational standard for the
  conclusion.
- Search current sources when facts, software, papers, standards, or product
  behavior may have changed.
- Prefer primary papers, official specifications, and official project
  documentation. Use surveys to locate primary evidence or context.
- Record exact authorship, title, year, venue, DOI or canonical URL, and access
  date when available.
- Read enough of a source to support the claim for which it is cited. Search
  snippets and abstracts are not evidence for detailed claims.
- Distinguish reported results from interpretation, extrapolation, proposal,
  and cross-source synthesis.
- Compare approaches and include negative results, limitations, evaluation
  weaknesses, and unresolved questions.
- Preserve experimental method, versions, commands, output, and artifacts in a
  journal entry.
- For OS claims, identify the trust boundary, privilege level, hardware or
  simulator target, host dependencies, failure model, and reproducibility
  conditions.

## Maps, inquiries, and lifecycle

- Maps are curated explanations, not file dumps.
- Keep the home map selective: major active inquiries, topic maps, and
  developed syntheses belong there.
- Promote independently useful conclusions from inquiries or journals to
  notes.
- Move dormant or superseded work to `90-archive/` rather than silently
  deleting useful context. Record why and link replacements.
- Do not call a note `stable` or inquiry `resolved` merely because a writing
  pass is complete; evidence must support the lifecycle state.

## Verification and handoff

Before reporting archive work complete:

1. inspect repository status when version control is present and preserve
   unrelated changes;
2. run `python3 validate_archive.py` from the repository root;
3. run `python3 -m unittest test_validate_archive.py` when validation code or
   schema behavior changes;
4. verify newly introduced external citations against primary sources;
5. run `git diff --check` when this is a Git worktree; and
6. review the complete change for stale paths and accidental rewrites.

For any phased implementation plan created or changed, also review it against
both planning templates: confirm the milestone-named directory and index,
needs-based counts at all four work levels, a description before children at
every phase/section/task/sub-task level, and a
final integration-tests section with acceptance criteria and evidence/handoff
requirements in every phase. Archive validation alone does not establish these
planning requirements.

Whenever the user asks for a URL to a document or other content on GitHub,
include the complete, visible, absolute `https://github.com/...` URL in the
response. Do not provide only linked display text, a local filesystem path, a
relative path, or shorthand such as a pull-request number. Resolve and verify
the repository, revision or branch, and path before presenting the URL. If the
content has not been pushed and therefore has no online GitHub URL, say so
explicitly instead of inventing one.

Do not commit, push, open a pull request, or publish unless the user asks. In
the final handoff, summarize documents created or changed, indexes updated,
validation performed, and whether changes remain uncommitted.
