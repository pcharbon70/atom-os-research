---
title: "Causal charging and independent recovery reserves"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Causal charging and independent recovery reserves

Which work must remain attributable, and what resource independence makes recovery possible?

## Research basis and status

Resource containers motivate following work across protection boundaries rather than billing only the executing thread. [1](../../../30-sources/banga-et-al-1999-resource-containers.md), [2](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../scheduling-contexts-and-temporal-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A charge context follows attributable work across service boundaries, while an independently held recovery reserve funds fault handling, stop coordination and reaping. Hard-interrupt work uses a declared bounded reserve when immediate attribution is unavailable. Ordinary domain budgets, cleanup credit and emergency execution have separate ledgers.

### Admission, transitions and completion

At asynchronous handoff, explicitly accept a delegated payer and finite work allowance rather than borrowing an ambient current thread account. Admit recovery capacity against the maximum simultaneously protected failure scopes, including metadata and capability slots. Keep the reserve's scheduling context non-donatable and its authority lineage outside both child and replaceable supervisor.

### Failure and adversarial behavior

A supervisor with a nominal budget but no available fault slot or authority after child revocation is not independent. Unlabeled deferred work can exhaust shared capacity despite perfect thread accounting. Recovery work cannot simply be billed to a dead context whose execution is no longer eligible.

### Alternatives and unresolved tradeoffs

Fine-grained attribution improves fairness but adds bookkeeping; coarse charging is acceptable only with named residual costs and bounded shared reserves. Independent recovery should be admitted against realistic concurrent failures, not a single favorable example.

## Verification obligations

Exhaust child and supervisor ordinary resources simultaneously, saturate fault routes and trigger multiple admitted failures. Verify the reserve remains usable and bounded. Trace deferred work through its accepted payer and check that cancellation does not orphan its remaining charge or let it consume unrelated reserves.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Kernel activation checkpoints](../protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — Kernel work must reach a consistent, bounded checkpoint.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Recovery needs authority and metadata as well as CPU time.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Resource containers: A new facility for resource management in server systems](../../../30-sources/banga-et-al-1999-resource-containers.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Timing analysis of a protected operating system kernel](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — comparative evidence; its methods and limits are recorded in the source note.
