---
title: "Lease takeover and operation adoption"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Lease takeover and operation adoption

How can a new manager take control without losing valid completion evidence from already admitted work?

## Research basis and status

Failure-detector theory permits mistaken suspicion; authority fencing must therefore work even when the old manager resumes. [1](../../../30-sources/chandra-toueg-1996-failure-detectors.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../failure-boundaries-and-recovery-topology.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The protected recovery lease has one current epoch and sealed Use facet. An in-progress teardown or device operation has its own immutable operation epoch. These identities answer different questions: who may mutate now versus which previously admitted effect a completion describes.

### Admission, transitions and completion

Takeover compares the expected lease epoch, reserves successor slots, closes old session anchors, advances the control epoch and installs the successor's escrowed facets at one logical commit. Precommit failure leaves the old lease current. Revalidate the retained cursor against the same operation epoch and adopt valid progress without relabeling it or rerunning destructive stages.

### Failure and adversarial behavior

If the old manager can commit after takeover, both may publish replacements or reset shared hardware. If every old-epoch completion is discarded, the new manager can remain stuck despite real device completion. A partly public takeover is worse than either clean success or unchanged failure.

### Alternatives and unresolved tradeoffs

Terminating the old supervisor before transfer simplifies some races but is not always possible and still leaves admitted external effects. Epoch fencing allows control transfer under uncertainty; direct hardware aliases additionally require physical exclusion.

## Verification obligations

Suspend the old manager before each mutation, take over and resume it. Deliver a valid old-operation completion alongside a stale new mutation. Require acceptance of the former, rejection of the latter, atomic lease installation and no duplication of a non-idempotent operation.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sealed use facets and epoch sessions](../capability-spaces-and-authority/sealed-use-facets-and-epoch-sessions.md) — Lease enforcement relies on protected facets and closed sessions.
- [Charged reaper and resumable cursors](../teardown-revocation-and-safe-reclamation/charged-reaper-and-resumable-cursors.md) — A successor must continue the same teardown operation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Unreliable failure detectors for reliable distributed systems](../../../30-sources/chandra-toueg-1996-failure-detectors.md) — comparative evidence; its methods and limits are recorded in the source note.
