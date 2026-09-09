---
title: "Slot mutation and consented transfer"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Slot mutation and consented transfer

How can authority be delegated without allowing a sender to exhaust or overwrite a receiver's namespace?

## Research basis and status

Parmer's resource-table discussion makes both parties' consent explicit in delegation. [1](../../../30-sources/parmer-2016-capability-based-os-design.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../capability-spaces-and-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Slot mutation authority is separate from object use authority. The receiver owns destination capacity and chooses a reserved slot; the sender supplies a transferable, attenuable source facet. Copy, mint, move and delete have different lineage and ownership effects and must not share an ambiguous generic update operation.

### Admission, transitions and completion

Resolve both capability spaces and the source entry, reserve destination storage and lineage metadata, and verify rights attenuation. A move preserves the protected lineage identity while changing placement; a copy or mint follows the declared derivation schema. During IPC, transfer commits at call acceptance with the receiver's reserved slot, not when the sender merely queues. A failed admission releases the reservation without publishing authority.

### Failure and adversarial behavior

Unsolicited insertion is a capability-space denial of service. Deleting a slot is not necessarily object destruction or descendant revocation. A transfer that succeeds while call acceptance reports NotAccepted gives the receiver an effect outside the reported outcome. Generic transfer must reject protected non-transferable lease-use and reply facets.

### Alternatives and unresolved tradeoffs

An allocator-selected destination is convenient but still requires an explicit receiver budget and consent protocol. A caller-selected fixed slot is more predictable, although applications then manage fragmentation. Neither alternative justifies silently replacing an occupied entry.

## Verification obligations

Race destination reuse, source revocation and acceptance cancellation. Exhaust intermediate table nodes independently of final slots. Require atomic transfer/outcome agreement, attenuation and unchanged destination state on pre-accept failure.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Lookup admission must acquire a safe object lifetime.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Current authority and original operation identity remain distinct.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Capability-based OS Design](../../../30-sources/parmer-2016-capability-based-os-design.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
