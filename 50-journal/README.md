---
title: "Journal"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Journal index"
---

# Journal (`50-journal`)

## Purpose

The journal records dated observations, research sessions, experiments, and
exploratory writing.

## What belongs here

Put time-bound observations and reproducibility evidence here. Promote durable
ideas into notes, questions into inquiries, and source analysis into source
notes.

Every deep-dive entry includes an exhaustive source manifest separating notes
first introduced in that exact session from pre-existing notes reused by it.
Maps remain selective; these manifests are the authoritative session-level
provenance record.

## Index

### Subdirectories

- None yet.

### Documents

- [2026-08-28 AtomVM deep dive](2026-08-28-atomvm-deep-dive.md) — records the
  pinned source audit, release check, literature and community search, host
  environment, and failed prerequisite-limited build attempt.
- [2026-08-28 BEAM, ERTS, and OTP deep dive](2026-08-28-beam-erts-and-otp-deep-dive.md) —
  records the pinned OTP 29.0.5 audit, paper acquisition, web and practitioner
  search, evidence boundaries, and follow-up experiments.
- [2026-08-30 kernel hardware and architecture support deep dive](2026-08-30-kernel-hardware-and-architecture-support-deep-dive.md) —
  records the kernel-level scope, primary literature and official architecture
  sources, synthesis method, and explicit lack of implementation evidence.
- [2026-08-31 minimal privileged-kernel deep dive](2026-08-31-minimal-privileged-kernel-deep-dive.md) —
  records the capability, IPC, scheduling, failure-containment, recovery, and
  assurance literature search, synthesis checks, and lack of implementation
  evidence.
- [2026-09-02 kernel architecture components deep dive](2026-09-02-kernel-architecture-components-deep-dive.md) —
  records the expanded research across all eleven architecture components,
  shared review questions, implementation synthesis, source families, and
  explicit lack of executable or hardware evidence.
- [2026-09-02 managed actor runtime deep dive](2026-09-02-managed-actor-runtime-deep-dive.md) —
  records the current OTP/ERTS baseline, scientific and engineering source
  review, comparative-runtime assumptions, synthesis method, and explicit
  lack of runtime or hardware experiments.
- [2026-09-03 managed actor runtime components deep dive](2026-09-03-managed-actor-runtime-components-deep-dive.md) —
  records the expanded research across all thirteen runtime components, shared
  implementation criteria, new primary sources, cross-component synthesis,
  and explicit lack of prototype evidence.
- [2026-09-03 minimal privileged kernel components deep dive](2026-09-03-minimal-privileged-kernel-components-deep-dive.md) —
  records the expanded research across all eleven capability-microkernel
  components, source and design review method, cross-component lifecycle
  synthesis, falsifiers, and explicit lack of prototype evidence.
- [2026-09-03 OTP-like system services deep dive](2026-09-03-otp-like-system-services-deep-dive.md) —
  records the current OTP baseline, scientific papers, standards and
  engineering evidence, thirteen-component synthesis method, architectural
  distinctions, and explicit lack of prototype evidence.
- [2026-09-04 authentication and authorization deep dive](2026-09-04-authentication-and-authorization-deep-dive.md) —
  records the cross-layer literature and standards search, current source
  revisions, security synthesis and independent review, and explicit absence
  of implementation or hardware evidence.
- [2026-09-04 authentication and authorization components deep dive](2026-09-04-authentication-and-authorization-components-deep-dive.md) —
  records the expanded research across all sixteen proposed security services,
  exact source provenance, shared authority and lifecycle contracts,
  falsifiers, and absence of prototype evidence.
- [2026-09-04 OTP-like system services components deep dive](2026-09-04-otp-like-system-services-components-deep-dive.md) —
  records the expanded research across all thirteen service components, exact
  source provenance, shared lifecycle and outcome model, implementation
  recommendations, falsifiers, and absence of prototype evidence.
- [2026-09-04 Alan Kay and Smalltalk UI deep dive](2026-09-04-alan-kay-smalltalk-ui-deep-dive.md) —
  records the historical, implementation, HCI, current-platform, security, and
  accessibility research; attribution controls; complete source provenance;
  architectural synthesis; and absence of prototype or user-study evidence.

## Maintaining this index

Name entries by date, index every direct entry, and retain commands, versions,
outputs, target details, and artifact links needed to reproduce experiments.
For deep dives, keep both source-manifest categories exhaustive and explain
each source's role; use exactly `- None.` when a category is empty. Deep-dive
journal filenames end in `-deep-dive.md` so structural validation can identify
them without adding provenance metadata to every source note.
Local source-note links under `## Threads` or `## Follow-ups` are prospective
or contextual and are excluded from manifest-completeness checks; source-note
links elsewhere in a deep-dive journal count as substantive evidence.
