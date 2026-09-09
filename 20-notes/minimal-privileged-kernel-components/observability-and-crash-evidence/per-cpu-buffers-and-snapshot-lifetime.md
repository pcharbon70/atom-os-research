---
title: "Per-CPU buffers and snapshot lifetime"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Per-CPU buffers and snapshot lifetime

How can readers obtain bounded diagnostic snapshots without racing an interrupted writer or freed backing?

## Research basis and status

Linux tracing documents nested-writer commit rules; sequence-counter guidance separately warns about reader progress and pointer lifetime. [1](../../../30-sources/rostedt-2009-lockless-ring-buffer-design.md), [2](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../observability-and-crash-evidence.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each CPU owns preallocated producer storage with a fixed nesting profile, reservation and commit positions, explicit overflow mode and loss state. A snapshot owns immutable backing or a protected reader lease. Object generation alone is not a lifetime pin for the bytes being read.

### Admission, transitions and completion

Reserve a record, populate bounded fields and publish commit under the declared memory-ordering contract. Readers consume only committed data. Rotate among preallocated buffers or copy into caller-funded immutable snapshots; do not let a live writer reuse a snapshot's backing until its reader obligation ends. Overwrite, drop-new and sticky-summary modes are separate configured contracts.

### Failure and adversarial behavior

A reader spinning on an interrupted odd sequence can prevent the writer from ever completing. Retrying after a data race does not repair an invalid language-level access. Nested writer assumptions must match the architecture's actual exceptional entry behavior, and CPU removal must drain snapshot references before reuse.

### Alternatives and unresolved tradeoffs

Copying snapshots costs bandwidth but makes reader lifetime clear. Zero-copy snapshots require retained buffers and admission limits on slow readers. A lockless algorithm from another kernel cannot be transplanted without its nesting, memory-model and reclamation assumptions.

## Verification obligations

Interrupt each writer stage with another producer and a reader; exhaust nesting and snapshot capacity; retain a slow snapshot through CPU reincarnation. Require valid committed prefixes, explicit loss and no reuse of reader-held storage.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Containment escalation and terminal handoff](../fault-capture-and-containment/containment-escalation-and-terminal-handoff.md) — One lower terminal protocol owns fatal disposition.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Reading evidence needs a real backing-storage lifetime.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Lockless ring buffer design](../../../30-sources/rostedt-2009-lockless-ring-buffer-design.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Sequence counters and sequential locks](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — comparative evidence; its methods and limits are recorded in the source note.
