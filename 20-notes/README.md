---
title: "Notes"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Notes index"
---

# Notes (`20-notes`)

## Purpose

Notes preserve ideas, arguments, models, and syntheses in the author's own
words.

## What belongs here

Put independently useful conclusions and developing interpretations here.
Source summaries belong in `30-sources`; unresolved workbenches belong in
`40-inquiries`.

## Index

### Subdirectories

- [Applications and domain services components](applications-and-domain-services-components/README.md) —
  contains the fourteen detailed component-level syntheses for application
  composition, domain modeling, identity, protocols, invariants, persistence,
  workflows, effects, presentation, collaboration, extensions, evolution,
  assurance, tenancy, overload, and recovery, plus 60 internal-service studies
  across all fourteen component subdirectories. These remain research
  proposals with unexecuted verification obligations.
- [Authentication and authorization components](authentication-and-authorization-components/README.md) —
  contains the sixteen detailed component-level implementation syntheses for
  the authentication, identity, policy, grant, revocation, secret, audit,
  recovery, update, and federation control plane.
- [Kernel hardware and architecture components](kernel-hardware-and-architecture-components/README.md) —
  contains eleven component-level architecture syntheses and seventy
  internal-service reports across all eleven component subdirectories.
  These are full-system research contracts, not implementation results.
- [Managed actor runtime components](managed-actor-runtime-components/README.md) —
  contains thirteen component syntheses and 56 internal-service studies across
  all thirteen component subdirectories. Proposed contracts remain distinct
  from implementation and conformance evidence.
- [Minimal privileged kernel components](minimal-privileged-kernel-components/README.md) —
  contains eleven component-level syntheses and 54 internal-service reports
  across all eleven component subdirectories of the capability-microkernel
  layer. These are full-system research contracts, not implementation results.
- [OTP-like system services components](otp-like-system-services-components/README.md) —
  contains thirteen component syntheses and 55 internal-service studies across
  all thirteen component subdirectories of the unprivileged service-policy
  layer. These are full-system proposals with unexecuted falsifiers.
- [Proof-of-concept requirements](proof-of-concept-requirements/README.md) —
  contains nineteen requirement studies, the Zig and C kernel-language feasibility
  studies and comparison, and the T7500 target and manufacturer reference, covering CLI boot, bounded kernel
  contracts, BEAM/GC, integrated recovery and all six later capability gates,
  with evidence, alternatives, failure cases and next experiments.
- [Visual computing synthesis components](visual-computing-synthesis-components/README.md) —
  contains seven parent syntheses and 34 internal-service studies for user-owned
  projects, restartable presentation, semantic UI, trusted input, live tools,
  cross-layer recovery, and plural views.

### Documents

- [Proof-of-concept research readiness](proof-of-concept-research-readiness.md) —
  assesses research coverage and missing implementation evidence, proposes a
  minimal bootable OS with the CLI as its first delivery, excludes AtomVM and
  graphical UI, defines subsequent BEAM/recovery evidence gates, and connects
  the requirement-level deep dives.
- [Applications and domain services layer](applications-and-domain-services-layer.md) —
  develops an unprivileged Layer 5 with fourteen components, stable domain and
  operation identities, invariant-selected consistency, explicit workflows
  and external outcomes, disposable presentation, confined extensions,
  migration, semantic assurance, and cross-layer recovery.
- [Alan Kay's Smalltalk visual interface and the modern desktop](alan-kay-smalltalk-visual-interface-and-modern-desktop.md) —
  reconstructs Kay's metamedium and learning vision, distinguishes it from the
  collective Smalltalk and Star implementations, compares it with current
  desktop boundaries, and proposes a capability-safe actor-oriented synthesis.
- [Authentication and authorization across the five-layer architecture](authentication-and-authorization-across-the-five-layer-architecture.md) —
  proposes an unprivileged identity/policy control plane and a capability data
  plane, then defines human and workload authentication, exact grant contracts,
  trusted interaction, revocation, recovery, audit, and assurance across every
  layer.
- [BEAM, ERTS, and OTP principles for a new operating system](beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  separates the three layers, makes compiled-BEAM compatibility and
  process-local tracing collection explicit, identifies needed security and
  resource-control changes, and proposes a layered architecture.
- [Managed actor runtime layer](managed-actor-runtime-layer.md) — develops the
  unprivileged BEAM-compatible runtime contract, thirteen component design,
  critical execution paths, implementation stages, and conformance,
  responsiveness, overload, and fault evaluation plan.
- [Kernel hardware and architecture support layer](kernel-hardware-and-architecture-support-layer.md) —
  develops the kernel-level contracts for privileged entry, execution context,
  translation, ordering and code publication, interrupts, time, logical CPUs,
  protected I/O, faults, and a portable typed facade.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) —
  proposes a capability microkernel with explicit object memory, first-class
  execution-stop domains, bounded IPC and CPU budgets, revocation anchors,
  structured fault routes, and quiescence- or quarantine-gated recovery, with
  each component linked to its detailed evidence and implementation report.
- [OTP-like system services layer](otp-like-system-services-layer.md) —
  develops thirteen unprivileged policy components for lifecycle, behaviours,
  supervision, naming, configuration and identity, durable outcomes, device
  and network services, distributed coordination, updates, overload, and
  operations, with each component linked to a detailed evidence and
  implementation report.

## Maintaining this index

Index every direct note and describe its claim or role. Keep maturity values
honest and connect each note to evidence, related notes, or a map.
