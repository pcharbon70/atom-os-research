---
title: "Frame authority epochs and quarantine"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Frame authority epochs and quarantine

How can quarantine prevent old grants from becoming valid again when memory is eventually released?

## Research basis and status

DMA attacks show why temporal exposure and allocator reuse belong in the protection argument. [1](../../../30-sources/markettos-et-al-2019-thunderclap.md), [2](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../memory-mappings-and-architecture-resource-bindings.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A Frame has a mutating-authority epoch, exact backing identity and a ledger of admitted CPU and DMA bindings. Quarantine denies new mapping, DMA and reclaim mutations globally for that generation. Inspection and protected cleanup references are distinct from ordinary mutating facets.

### Admission, transitions and completion

Publish quarantine against the frame authority gate, making all pre-quarantine mutating facets permanently stale. Preserve already admitted bindings as cleanup obligations; some device profiles require retaining physical DMA mappings until drain or reset. Release requires a current custodian and matching effect-completion evidence, followed by sanitization and a new frame generation. Never reopen the old frame object.

### Failure and adversarial behavior

Revoking only the failed driver's cap leaves aliases held by another domain usable. Conversely, prematurely withdrawing a DMA mapping can violate a required device recovery sequence. A frame-level deny-new-access state must not erase the ledger needed to confine or finish those old effects.

### Alternatives and unresolved tradeoffs

A broad quarantine is easier to account for but retains more memory and may disable unrelated service. A narrow quarantine requires proof of the exact reachable set and every alias. If confinement is unknown, escalation is the honest result rather than a successful quarantine label.

## Verification obligations

Retain old frame caps in multiple capability spaces, enter quarantine and attempt every mutating operation. Delay an admitted DMA completion through manager takeover. Require old grants to stay stale after release and ensure retained bindings remain available only for protected cleanup.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [VFIO - Virtual Function I/O](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — comparative evidence; its methods and limits are recorded in the source note.
