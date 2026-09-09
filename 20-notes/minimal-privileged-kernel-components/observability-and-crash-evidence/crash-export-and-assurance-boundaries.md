---
title: "Crash export and assurance boundaries"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Crash export and assurance boundaries

What may a crash artifact legitimately claim about integrity, secrecy, persistence and causality?

## Research basis and status

Crash-dump engineering and explicit proof assumptions show why evidence capture has several independent assurance dimensions. [1](../../../30-sources/goyal-et-al-2005-kdump.md), [2](../../../30-sources/sel4-foundation-2026-proof-assumptions.md), [3](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../observability-and-crash-evidence.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

CrashExport is separate from debug access and lifecycle control. An artifact names schema, build and object generations, clock era/conversion identity, source certainty, loss and surviving sections. Checksums protect against some corruption; authenticity requires a trust boundary and keys not assumed intact inside the failed kernel.

### Admission, transitions and completion

Export only after the lower handoff has established a usable independent environment, or through a prequalified bounded sink. Apply field authorization and redaction before crossing the recipient boundary. Preserve original local time domains and conversion metadata rather than inventing a total order across unsynchronized CPUs. Record whether storage acknowledgement means receipt, durable persistence or merely attempted output.

### Failure and adversarial behavior

A well-formed checksum does not prove that the kernel was uncompromised, that DMA was contained or that the record survived reset. A failed sink is not evidence that no fault occurred. Secret memory included for debugging can create a disclosure channel even when the artifact is otherwise useful.

### Alternatives and unresolved tradeoffs

Raw memory dumps maximize diagnostic flexibility but require broad authority and strong handling controls. Structured summaries reduce exposure and make partial decoding easier, while losing detail. An externally signed or stored record can strengthen provenance only under explicit independent-controller assumptions.

## Verification obligations

Corrupt sections, revoke export rights, omit conversion snapshots and fail storage after receipt but before persistence. Require accurate assurance labels and no fabricated ordering or durability. Check that redacted and unavailable fields remain distinguishable from valid zero values.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Containment escalation and terminal handoff](../fault-capture-and-containment/containment-escalation-and-terminal-handoff.md) — One lower terminal protocol owns fatal disposition.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Reading evidence needs a real backing-storage lifetime.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Kdump: A kexec-based kernel crash dumping mechanism](../../../30-sources/goyal-et-al-2005-kdump.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [What the Proofs Assume](../../../30-sources/sel4-foundation-2026-proof-assumptions.md) — comparative evidence; its methods and limits are recorded in the source note.
3. [Sequence counters and sequential locks](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — comparative evidence; its methods and limits are recorded in the source note.
