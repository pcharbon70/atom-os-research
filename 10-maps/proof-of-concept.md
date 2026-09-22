---
title: "Proof of concept"
kind: map
created: "2026-09-05"
tags:
  - beam
  - operating-systems
  - proof-of-concept
  - research-program
aliases:
  - "From research to a bootable Kay OS prototype"
---

# Proof of concept

## Scope

A selective path from architectural research to a minimal bootable OS. First
boot into a native user-mode CLI, then add protected services, compiled BEAM,
unprivileged tracing GC, bounded resources, and independent recovery. AtomVM is
excluded by project decision. Graphical UI and desktop work are outside this
proof of concept. Broader layer inquiries retain their evidence requirements.

## Start here

- [Kernel-language comparison](../20-notes/proof-of-concept-requirements/zig-versus-c-kernel-language-comparison.md) weighs Zig/C pros and cons, qualification risk and decision-changing conditions.
- [C kernel-development map](c-kernel-development.md) evaluates the alternative
  language and C-component path without changing the selected Zig decision.
- [Zig kernel-development map](zig-kernel-development.md) connects the accepted
  kernel-language decision to its feasibility evidence and remaining M0/M1
  compiler, ABI and privilege-transition qualification.
- [M0 build-closure execution](../50-journal/2026-09-17-m0-phase-01-build-closure.md)
  records the demonstrated bounded compiler/ABI/reproducibility result without
  treating the non-bootable ELF as kernel or guest evidence.
- [M0 Phase 2 boot, image, and interface contracts](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-02-boot-image-and-interface-contracts.md)
  records the accepted Limine, higher-half ELF, restricted ABI, bounded
  console/time authority, fault, and deterministic read-only ISO decisions and
  tracks their executable integration evidence.
- [M0 Phase 2 contract-integration execution](../50-journal/2026-09-18-m0-phase-02-contract-integration.md)
  records the clean 24-case hosted result, independent no-blocker review,
  exact identities, explicit guest/physical boundary and accepted handoff.
- [M0 Phase 3 acceptance harness and input qualification](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-03-acceptance-harness-and-input-qualification.md)
  records the accepted fixed watchdog, controlled PTY protocol, evidence,
  process cleanup and virtual/physical boundary; its clean assembled gate
  passes and the owner selected proceed on 2026-09-21.
- [M0 Phase 3 integration evidence](../50-journal/2026-09-21-m0-phase-03-integration.md)
  records the clean 24 inherited, nine harness and seven assembled results,
  bundle identities, retained tool-runtime failure and physical-inventory
  exclusion.
- [M1 boot-to-CLI plan](../60-planning/01-proof-of-concept/m1-boot-to-cli/README.md)
  is accepted for execution. Phase 1 binds the merged M0 baseline, immediate
  Kay ownership of stacks/descriptors/paging and conservative memory release;
  Phase 1 completed six registered guest boots at clean Kay OS commit
  `4766582`, retained its ring-0/paging evidence, and has a proceed handoff to
  Phase 2 decision M1-D02.
- [Proof-of-concept implementation planning](../60-planning/01-proof-of-concept/README.md)
  provides five detailed M0–M4 definitions and maps the readiness gaps to their
  required artifacts and acceptance cases. The
  [planning convention](../60-planning/README.md) requires descriptions
  at all four work levels and integration tests at the end of every phase;
  18 phase plans now provide that hierarchy. M0 Phase 1 is complete and M0
  Phase 2 completed after its reviewed clean contract integration and the
  user's proceed decision; M0 is merged and M1's entry plan is accepted,
  while all M1 implementation and later milestone evidence remain outstanding.
- [x86-64 compatibility envelope and test fixtures](../20-notes/proof-of-concept-requirements/x86-64-compatibility-envelope-and-test-fixtures.md)
  controls the generic target, runtime discovery, minimum virtual baseline,
  capability-driven matrix and independent physical fixtures.
- [T7500 target-correction journal](../50-journal/2026-09-06-t7500-target-correction.md)
  records the confirmed Intel platform, archived AMD detour and remaining inventory.
- [Research readiness](../20-notes/proof-of-concept-research-readiness.md)
  explains why implementation should start, the remaining decision gates, the
  first CLI boot contract, integrated OS demonstration, and what can wait.
- [Minimal bootable-system inquiry](../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md)
  tracks the M0–M4 acceptance gates.
- [Requirement studies](../20-notes/proof-of-concept-requirements/README.md)
  inventories nineteen reports and maps every assessment requirement to
  proposed contracts, failure cases and next experiments.
- [Requirement research journal](../50-journal/2026-09-06-proof-of-concept-requirements-deep-dive.md)
  records the paper/specification/article comparison, exact source manifest,
  retrieval limitations and remaining executable evidence.
- [Assessment journal](../50-journal/2026-09-05-proof-of-concept-readiness-deep-dive.md)
  records the assessed revision, evidence limits, checks, and source provenance.

## Trails

### Boot into a minimal CLI

The [first CLI delivery](../20-notes/proof-of-concept-research-readiness.md#first-delivery-boot-into-the-cli)
defines native user-mode command handling, the console/time interface,
`help`, `version`, `uptime`, bounded input, and automated serial acceptance.
The first prompt does not depend on completion of the managed runtime.

The focused [target and firmware study](../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md)
and [freestanding build study](../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md)
define the first decision records. The [CLI study](../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md)
connects user-space placement to parser, wait and serial-harness tests.

Read the [architecture implementation
sequence](../20-notes/kernel-hardware-and-architecture-support-layer.md#suggested-implementation-sequence)
and [bootstrap authority
contract](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff.md)
when implementing the selected generic Intel-compatible x86-64 backend. The earlier
[QEMU RISC-V candidate](../30-sources/qemu-project-2026-risc-v-virt-platform.md)
is retained as comparative evidence, not the active first target. A qualified
physical single-CPU CLI check on a named fixture can follow virtual bring-up
without waiting for SMP; the T7500 is only candidate P1.

### Make compatibility an executable input

The [compatibility/loader
report](../20-notes/managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier.md)
defines the profile dimensions. The [runtime
adapter](../20-notes/managed-actor-runtime-components/runtime-domain-bootstrap-and-kernel-adapter.md)
defines the substrate inventory. The [managed-runtime
implementation program](../20-notes/managed-actor-runtime-layer.md#implementation-program)
provides the independent-interpreter direction. Pinned upstream OTP supplies
the compiler and semantic oracle; no rejected-runtime comparison gates this
work.

The focused [BEAM profile study](../20-notes/proof-of-concept-requirements/beam-profile-loader-and-conformance.md)
explains why compiler-generated closure and selected OTP alias/monitor paths
matter. The [runtime adapter study](../20-notes/proof-of-concept-requirements/runtime-adapter-signals-and-native-services.md)
connects asynchronous actors to bounded native services without blocking the
only managed scheduler.

### Test the composition that matters

Combine the [small transport
contract](../20-notes/minimal-privileged-kernel-components/bounded-invocation-and-transport.md),
[kernel temporal
authority](../20-notes/minimal-privileged-kernel-components/scheduling-contexts-and-temporal-authority.md),
[runtime scheduling](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md),
and [tracing collection](../20-notes/managed-actor-runtime-components/terms-private-heaps-shared-binaries-and-tracing-collection.md).
Their individual designs do not establish responsiveness when composed.

Use the focused [IPC contract](../20-notes/proof-of-concept-requirements/capabilities-syscalls-and-bounded-ipc.md),
[lifecycle study](../20-notes/proof-of-concept-requirements/domain-lifecycle-and-safe-reclamation.md)
and [GC study](../20-notes/proof-of-concept-requirements/private-heaps-and-tracing-garbage-collection.md)
to fix admission, reuse, collector reserves and separate actor/domain latency.

Use [resource accounting](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control.md)
and [outer recovery](../20-notes/minimal-privileged-kernel-components/failure-boundaries-and-recovery-topology.md)
to test overload, independent reserves, and replacement of CLI, native service,
and runtime domains. The
[reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
explains why stopping execution is not sufficient evidence for safe reuse.

The [integrated validation study](../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md)
defines the minimum model properties, CLI-operated fault campaign, raw
measurements and limits on assurance claims.

### Expand only with a new evidence claim

The next routes are [durable local
state](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md),
[network services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md),
and [authentication and authorization](authentication-and-authorization.md).
Each needs additional backend/profile evidence. They need not delay the first
CLI boot. Graphical UI remains a separate program.

The focused [durability study](../20-notes/proof-of-concept-requirements/durable-state-and-crash-consistency.md)
is the recommended first post-M4 route. The [requirements index](../20-notes/proof-of-concept-requirements/README.md)
also covers network actors, DMA recovery, multicore/portability, administration
and update/root survival as distinct evidence gates.

## Open questions

- Which physical fixture should M1 Phase 4 qualify first, and which installed
  CPU, firmware, board and device facts must its external and Kay OS reports
  reconcile against the declared compatibility envelope?
- Does the first native CLI pass interactive and malformed-input tests?
- Which minimum BEAM profile supports the first CLI-launched workload?
- Can the selected GC, mailbox, and scheduler design meet measured resource
  and responsiveness limits while preserving independent recovery?
- After the [minimal proof](../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md),
  does durable state or distribution supply the next most useful experiment?
