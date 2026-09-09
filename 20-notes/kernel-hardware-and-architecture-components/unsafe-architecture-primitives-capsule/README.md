---
title: "Unsafe architecture-primitives capsule: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Unsafe architecture-primitives capsule: internal-service research

## Purpose

This directory decomposes [component 1: Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md) into 5 independently reviewable architecture services. Separate the contract inventory, privileged state, memory effects, device/wait effects and binary boundary. These are private mechanism services, never a second capability or policy layer.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Primitive contract registry](primitive-contract-registry.md) — Every raw primitive should have an inspectable effect contract and a narrow set of authorized importers. An instruction mnemonic or an unsafe marker is insufficient to explain the state in which execution is valid.
- [Register, control and local-mask leaves](register-control-and-mask-leaves.md) — Control-register and interrupt-mask primitives should preserve the caller's established state rather than expose arbitrary numeric writes. Each allowed transition needs a feature, field and execution-context contract.
- [Ordering and maintenance leaves](ordering-and-maintenance-leaves.md) — The capsule should expose distinct local effects for compiler ordering, CPU-memory ordering, translation maintenance and instruction-context synchronization. Semantic components assemble these leaves into larger protocols.
- [Device, counter and wait leaves](device-counter-and-wait-leaves.md) — Device accesses, counter observations and wait/terminal instructions belong in a small leaf family whose side effects are explicit. These facilities expose mechanisms; they do not own driver servicing, timer policy or recovery decisions.
- [Generated ABI and binary assurance](generated-abi-and-binary-assurance.md) — The assembly boundary should be derived from one representation schema and checked against the linked binary. Correct source declarations cannot establish what a compiler emitted at entry, interrupt or foreign-function boundaries.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
