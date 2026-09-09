---
title: "Charged reaper and resumable cursors"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Charged reaper and resumable cursors

How can cleanup make bounded progress without monopolizing privileged execution or depending on the failed owner?

## Research basis and status

Kernel timing analysis motivates explicit preemption points; logical closure is not a bound on total cleanup work. [1](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md), [2](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../teardown-revocation-and-safe-reclamation.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A ReapToken names one immutable teardown operation, protected cursor, charged work allowance and current recovery authority. The token retains object generations and committed stage receipts so a successor can continue without rescanning from untrusted pointers. Cleanup capacity was reserved at admission.

### Admission, transitions and completion

Process a bounded number of ledger nodes or bytes per invocation, stop only at a consistent checkpoint and publish cursor progress before relinquishing ownership. Revalidate the caller's current recovery lease on continuation, while retaining the original teardown epoch. Destructive stages record their committed outcome exactly once; duplicate requests may query or assist rather than repeat them.

### Failure and adversarial behavior

A cursor into a reusable array can point at unrelated work after compaction. Returning before recording completion may make a takeover repeat a reset or free. Charging every slice to a dead child's unavailable CPU context prevents progress despite correct metadata accounting.

### Alternatives and unresolved tradeoffs

A caller-driven reaper makes work and authority explicit but needs scheduling by an independent service. A kernel background reaper would require its own finite admission and accounting contract rather than invisible unlimited maintenance. Neither design guarantees eventual hardware completion.

## Verification obligations

Stop and replace the reaper after every cursor update, exhaust one slice, and repeat every request. Verify monotonic progress, exact-once destructive transitions and bounded work per call. Report blocked hardware dependencies as blocked, not as an empty ready queue that implies success.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sanitization and generation-safe reuse](../typed-object-storage-and-explicit-memory/sanitization-and-generation-safe-reuse.md) — Only the allocator completes sanitization and fresh publication.
- [Device completion and reset composition](../memory-mappings-and-architecture-resource-bindings/device-completion-and-reset-composition.md) — Device-specific graphs supply physical completion evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Timing analysis of a protected operating system kernel](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Kernel design for isolation and assurance of physical memory](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) — comparative evidence; its methods and limits are recorded in the source note.
