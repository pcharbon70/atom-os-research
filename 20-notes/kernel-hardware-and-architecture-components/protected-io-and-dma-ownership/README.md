---
title: "Protected I/O and DMA ownership: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Protected I/O and DMA ownership: internal-service research

## Purpose

This directory decomposes [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md) into 7 independently reviewable architecture services. Separate device identity, memory authority, transfer, maintenance, revocation, reset and fault custody. These seven services refine one protected-I/O lifecycle rather than inventing independent buffer or device owners.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Requester and endpoint scope binding](requester-endpoint-scope-binding.md) — A software device endpoint is not necessarily an independently isolatable or resettable hardware unit. Protected I/O must bind the actual requester, interrupt and reset scopes before granting authority.
- [DMA buffer registration and range authority](dma-buffer-registration-and-range-authority.md) — A DMA address is a scoped translation result, not ownership of memory. Registration must preserve frame authority, bounds, permissions and lifetime independently from whether device access is currently enabled.
- [CPU-device transfer and queue publication](cpu-device-transfer-and-queue-publication.md) — Ownership transfer has both a software protocol and an enforcement profile. Clean transfer bookkeeping is valuable, but it does not by itself stop a malicious device or a stale CPU alias.
- [IOMMU maintenance and completion](iommu-maintenance-and-completion.md) — IOMMU work needs typed maintenance plans and scoped completion evidence. Consuming a queue entry, invalidating one cache and draining prior device traffic are not interchangeable outcomes.
- [I/O revocation and reclamation](revocation-and-reclamation.md) — Revocation closes authority; reclamation reuses storage. A safe design joins every outstanding access and software-lifetime obligation between those two events.
- [Reset-domain and recovery authority](reset-domain-and-recovery-authority.md) — Reset is a scoped destructive capability, not a general permission held by every device manager. Recovery must remain possible after a manager fails without leaving that manager's stale credentials effective.
- [I/O fault attribution and quarantine](io-fault-attribution-and-quarantine.md) — Fault reporting should preserve capture-time identity while keeping diagnosis separate from containment. An informative fault record does not itself stop a requester or make its buffers safe to release.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
