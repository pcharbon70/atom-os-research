---
title: "Workflows, process managers, timers, and compensation: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Workflows, process managers, timers, and compensation: internal services

## Purpose

Decompose durable control state, step outcomes, timers, compensation and structured
concurrent obligations.

This directory decomposes [Workflows, process managers, timers, and compensation](../workflows-process-managers-timers-and-compensation.md)
into 5 separately reviewable research responsibilities. These are service
contracts, not a mandate for one actor, protected domain or deployable package
per document.

## What belongs here

Keep owned state, authority boundaries, transition and completion semantics,
failure cases, alternatives and falsifiers here. Primary findings remain in
source notes; the [session manifest](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md)
records exact provenance. This is full-system architecture research, not
implementation delivery or a proof-of-concept gate.

Layer 5 declares domain meaning and required evidence. Layer 4 supplies generic
policy and durability services; Layers 2–3 enforce protection, resources and
managed execution. Proposed guarantees remain conditional on those contracts.

## Index

### Subdirectories

- None yet.

### Documents

- [Workflow definitions and durable control state](workflow-definitions-and-durable-control-state.md) — What survives when the actor coordinating a long use case disappears?
- [Step dispatch, receipt correlation, and resume](step-dispatch-receipt-correlation-and-resume.md) — How is a workflow step retried without creating another business action?
- [Durable timer meaning and retry budgets](durable-timer-meaning-and-retry-budgets.md) — What does a timer firing mean after restart, clock change or delayed delivery?
- [Compensation, pivots, and manual repair](compensation-pivots-and-manual-repair.md) — How can interrupted work be amended without pretending its visible effects never happened?
- [Fan-out, joins, and cancellation responsibility](fan-out-joins-and-cancellation-responsibility.md) — When may a parallel workflow finish while child work is still running?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
