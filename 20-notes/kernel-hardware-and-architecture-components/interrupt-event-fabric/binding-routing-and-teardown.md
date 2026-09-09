---
title: "Binding, routing and teardown"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - interrupt-event-fabric
aliases: []
---

# Binding, routing and teardown

Changing a destination or CPU route should be an explicit lifetime transition. Replacing a pointer is insufficient while hard-path code, old notifications or device remapping can still name the previous binding.

## Scope and research question

When may a binding generation and its storage be replaced safely?

This report refines [component 5: Interrupt event fabric](../interrupt-event-fabric.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

The IRQBinding aggregate holds source/route/binding records, one account and lifetime group, completion authority, EventSink, CPU incarnation and device/remapping dependencies. A teardown ledger records delivery closure, source stabilization, active handler references, deferred records and management-route retention. Component 7 owns CPU eligibility; component 8 owns device reassignment.

### Protocol and publication points

Close new delivery/admission → stabilize source under its flow → close completion authority → drain hard-path and deferred references → coordinate CPU/device/remapping transitions → publish replacement generation or release aggregate. Route migration may retain masked pending work until the new route is coherent. A teardown timeout retains the old aggregate and records missing evidence.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An old completion token can accidentally rearm a newly bound source if only a vector matches. Removing a CPU from a mask does not stop in-flight delivery. NAPI supplies a useful warning: release of a processing ownership flag need not mean the executing code has exited or stopped touching its storage.

### Alternatives and tradeoffs

Never reusing source IDs simplifies ABA reasoning but does not release referenced memory safely. Global stop/rebind reduces concurrency but increases disruption. Generation-tagged local transitions need more state yet preserve independent service recovery.

### Cross-architecture realization

Wired routes, MSI identities and interrupt-remapping caches have different retirement mechanisms. Their exact completion predicates stay backend-specific and must be joined before shared identity reuse.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Complete an old notice after rebinding and verify no replacement state changes.
- Migrate affinity during active service and verify one coherent route generation.
- Retain deferred/handler references after logical disable; prevent aggregate or sink storage reuse.

Binding teardown composed with CPU removal and device reset remains an unverified cross-component protocol.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Interrupt accounting and quarantine](interrupt-accounting-and-quarantine.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux NAPI](../../../30-sources/linux-kernel-community-2026-napi-contracts.md) — Budgeted processing and explicit masking/ownership handoff.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [VFIO isolation groups](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — Device functions do not necessarily form independent isolation units.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
