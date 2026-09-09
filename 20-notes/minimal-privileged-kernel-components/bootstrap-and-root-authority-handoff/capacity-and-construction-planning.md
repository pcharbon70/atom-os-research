---
title: "Capacity and construction planning"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Capacity and construction planning

How can initialization promise that exceptional paths remain funded before any service is allowed to run?

## Research basis and status

Explicit kernel-memory research makes indirect metadata a resource-management concern rather than invisible allocator overhead. [1](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md), [2](../../../30-sources/kuz-et-al-2010-capdl.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bootstrap-and-root-authority-handoff.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The construction planner owns an exact, versioned bill of resources, not an allocator policy. It names object backing, capability slots, lineage nodes, domain membership, per-CPU stop records, reply and fault capacity, trace reservations, cleanup cursors and independently held recovery escrow. Accounts, lifetime owners and physical extents appear as separate fields.

### Admission, transitions and completion

Compute checked upper bounds from the validated graph and the selected kernel object-layout profile. Include alignment loss, maximum participant sets and failure records, then reserve all resources in one private construction scope. Each constructor consumes a named reservation and returns a typed receipt. Reconcile planned, reserved and consumed quantities before publication; unused reserved capacity is explicitly released or assigned to a declared reserve.

### Failure and adversarial behavior

Counting only visible objects can produce a root that boots but cannot stop its first failed child. Reservations reachable through the child's revocation anchors do not provide independent recovery capacity. Layout-version mismatch or arithmetic overflow rejects the plan before public objects exist.

### Alternatives and unresolved tradeoffs

Static maximal reservation eases reasoning but can waste memory; demand allocation is more economical but makes failure admission conditional. A bounded profile can reserve worst-case exceptional work while allowing ordinary pools to remain dynamic. It must state which maximum simultaneous failures it admits.

## Verification obligations

Construct manifests that fit object backing but exhaust lineage, slots, stop acknowledgements or recovery credits. Require explicit rejection at the correct reservation. Compare calculated size against actual constructor consumption for every object type and verify that a child cannot charge or revoke the recovery reserve.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Construction must preserve effect-bearing authority.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Bootstrap must provision an independently usable recovery path.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Kernel design for isolation and assurance of physical memory](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [capDL: A language for describing capability-based systems](../../../30-sources/kuz-et-al-2010-capdl.md) — comparative evidence; its methods and limits are recorded in the source note.
