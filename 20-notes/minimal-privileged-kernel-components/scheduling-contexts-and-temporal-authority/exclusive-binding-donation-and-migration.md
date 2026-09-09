---
title: "Exclusive binding, donation and migration"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Exclusive binding, donation and migration

How can one execution budget follow a call chain or migrate without becoming usable in two places?

## Research basis and status

Passive scheduling contexts provide the migration-of-time precedent; Atom adds explicit failure and incarnation constraints. [1](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../scheduling-contexts-and-temporal-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A context has one protected binding owner and a bounded donation stack whose entries identify exact caller, call and context generations. CPU placement and admission-domain ownership are recorded separately. Donation transfers scheduling use, not object-lifetime or recovery authority.

### Admission, transitions and completion

Commit donation with accepted caller-funded invocation. The receiver becomes Ready on that context but may execute only after dispatch revalidation. Unwind in reverse order after the corresponding handler and descendants drain. Restore to a predecessor only if its generation, gates and state remain valid; otherwise skip terminal predecessors and retain the unique context safely unbound. Migration excludes concurrent dispatch and validates destination capacity before ownership changes.

### Failure and adversarial behavior

A context returned to an old caller incarnation can fund an unrelated replacement. Migrating while a stale run-queue entry remains eligible permits concurrent spending. A suspended predecessor is not necessarily dead: its saved logical state and context relation must survive correctly.

### Alternatives and unresolved tradeoffs

Restricting donation to one CPU simplifies accounting but limits placement. Cross-CPU movement requires explicit timebase, run-queue and stop-membership composition. Increasing donation depth is not free; it increases retained metadata and worst-case unwind work.

## Verification obligations

Race migration, nested reply, cancellation, predecessor suspension and domain stop. Assert exactly one binding owner and conservation of residual credit at each transition. Replay stale run-queue entries and require generation/gate rejection before execution.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Kernel activation checkpoints](../protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — Kernel work must reach a consistent, bounded checkpoint.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Recovery needs authority and metadata as well as CPU time.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
