---
title: "Logical-CPU coordination and lifecycle: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Logical-CPU coordination and lifecycle: internal-service research

## Purpose

This directory decomposes [component 7: Logical-CPU coordination and lifecycle](../logical-cpu-coordination-and-lifecycle.md) into 6 independently reviewable architecture services. Separate CPU identity, admission, bounded remote work, removal, policy eligibility and uncertain recovery. The six services share one lifecycle authority; none independently declares a CPU safely stopped.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [CPU identity, incarnation and membership](identity-incarnation-and-membership.md) — A logical CPU is a durable identity whose execution incarnations have separate authority. Membership is a coherent publication, not a collection of independently updated flags.
- [Secondary preparation and admission](secondary-preparation-and-admission.md) — Starting execution and admitting a CPU are different operations. A secondary must demonstrate that its local execution substrate is ready before any subsystem may target it as online.
- [Bounded cross-CPU request fabric](cross-cpu-request-fabric.md) — Remote work should use closed request kinds, bounded storage and incarnation-bound completion records. A notification says work may be available; it does not itself prove that the requested effect happened.
- [CPU drain, stop and reclamation](drain-stop-and-reclamation.md) — CPU removal is a multi-owner drain followed by an irreversible stop commitment. Software ineligibility, no further kernel execution and physical power-off are distinct facts.
- [Topology and feature eligibility](topology-and-feature-eligibility.md) — Topology describes relationships; eligibility grants permission to execute a class of work. Keeping these separate avoids turning a discovery hint into scheduling or security authority.
- [CPU quarantine and recovery ledger](quarantine-and-recovery-ledger.md) — Quarantine records what remains unsafe to reuse when CPU progress or stop evidence is missing. It is an owned recovery state, not a synonym for an offline flag.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
