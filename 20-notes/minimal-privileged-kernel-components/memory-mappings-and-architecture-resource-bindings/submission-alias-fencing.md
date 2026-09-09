---
title: "Submission alias fencing"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Submission alias fencing

When does revoking a device manager actually prevent it from submitting more work?

## Research basis and status

Shared DMA interfaces remain security protocols even when translations limit their address range. [1](../../../30-sources/markettos-et-al-2019-thunderclap.md), [2](../../../30-sources/haecki-et-al-2019-cleanq.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../memory-mappings-and-architecture-resource-bindings.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The submission fence tracks every profile-declared queue, doorbell and DMA-reconfiguration alias, including aliases held by the driver or a replaceable manager. Mediated kernel sessions and direct mapped registers are different authority paths and require different closure evidence.

### Admission, transitions and completion

Close the current mediated session immediately at takeover. To claim physical submission closure, either terminally stop every holder of direct aliases or revoke all such mappings and complete the relevant CPU translation invalidation. Retain previously admitted queue entries and posted writes in the operation ledger. Only the device profile determines how those old effects drain and whether mappings must remain installed during recovery.

### Failure and adversarial behavior

A fenced service connection does not stop a paused manager that later resumes with a valid MMIO mapping. Revoking the doorbell while leaving queue-configuration registers writable may still permit new DMA. Translation completion excludes future CPU access but does not retract already posted device writes.

### Alternatives and unresolved tradeoffs

Fully mediated control reduces direct-alias complexity but adds trusted-path cost. Direct access can be appropriate for performance-sensitive services only with a complete alias inventory and a viable terminal-stop or revocation path.

## Verification obligations

Pause a manager with each alias, advance its lease epoch, then resume and attempt submission. Delay posted writes past CPU revocation. Require separate reports for logical session fencing, physical new-submission exclusion and drainage of previously admitted work.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer](../../../30-sources/haecki-et-al-2019-cleanq.md) — comparative evidence; its methods and limits are recorded in the source note.
