---
title: "Device profiles and requester trust sets"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Device profiles and requester trust sets

What deployment facts are required before separate device handles can be advertised as isolated authority?

## Research basis and status

VFIO documentation identifies isolation groups that may exceed apparent function boundaries. [1](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md), [2](../../../30-sources/markettos-et-al-2019-thunderclap.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../memory-mappings-and-architecture-resource-bindings.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

An immutable trusted DeviceProfile identifies the platform and device revision, requester/trust attachment set, submission and configuration aliases, drain/reset dependencies, permitted completion evidence and quarantine scope. A DmaSpace attaches one indivisible trust set rather than an arbitrary collection inferred from software handles.

### Admission, transitions and completion

Validate profile provenance and applicability before granting driver mappings or enabling submission. Check that every requester path is covered by the selected translation/protection backend and that reset collateral is represented independently of endpoint naming. Derive driver capabilities from that validated profile; a replaceable driver cannot edit the profile to declare its own completion or reduce its reset scope.

### Failure and adversarial behavior

PCI function separation does not prove requester separation, and requester isolation does not prove reset isolation. Peer-to-peer paths or aliasing can bypass the assumed boundary. Unknown board or topology facts must remain unsupported or conservatively grouped rather than being filled from a generic device class.

### Alternatives and unresolved tradeoffs

Per-device profiles permit stronger guarantees but require maintenance and exact matching. Broad class profiles can simplify support only where the hardware contract genuinely matches. Unsupported isolation is an explicit admission failure, not a performance fallback to unprotected DMA.

## Verification obligations

Supply conflicting requester aliases, a shared reset boundary and an unlisted direct configuration window. Require rejection or explicit correlated scope. Verify profile immutability after admission and ensure that no user-supplied Boolean can substitute for a protected completion token.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [VFIO - Virtual Function I/O](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../../../30-sources/markettos-et-al-2019-thunderclap.md) — comparative evidence; its methods and limits are recorded in the source note.
