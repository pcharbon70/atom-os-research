---
title: "2026-09-03 minimal privileged kernel components deep dive"
kind: journal
created: "2026-09-03"
tags:
  - capabilities
  - literature-review
  - microkernels
  - research-method
  - recovery
aliases:
  - "Minimal privileged kernel component research session"
---

# 2026-09-03 minimal privileged kernel components deep dive

## Observations

This session expanded all eleven proposed components in the [minimal privileged
kernel layer](../20-notes/minimal-privileged-kernel-layer.md) into individual
implementation research reports under the [minimal privileged kernel components
directory](../20-notes/minimal-privileged-kernel-components/README.md).

The common result is a capability microkernel whose fast path is intentionally
small but whose lifecycle semantics are explicit. Authority admission,
generation identity, resource payment, logical closure, physical quiescence,
failure evidence, recovery ownership, and service identity are separate
dimensions. This separation prevents several recurring category errors:

- revoking a capability does not undo an already admitted effect;
- a stopped domain is not yet a reclaimable domain;
- an IOMMU invalidation is not proof that a device stopped;
- a timeout is not proof that a CPU, peer, or service failed;
- restart is not repair of durable, shared, device, or external state;
- a generation number rejects stale software but does not reverse physical
  effects; and
- a BEAM actor, ERTS scheduler thread, native service domain, device reset
  domain, and logical service epoch are different scopes.

The recommended architecture uses a declarative auditable bootstrap, caller-
backed typed objects, local generational CSpaces, pre-funded close anchors,
first-class protection domains, bounded call records, capability-mediated CPU
budgets, generation-safe mapping/device bindings, typed fault routes,
independent recovery escrow, charged split-phase reaping, and bounded crash
evidence.

These are research recommendations. No kernel object, syscall, state machine,
proof, benchmark, emulator target, device model, or BEAM integration was
implemented or executed in this session.

## Environment

- Repository: `atom-os-research`
- Research date: 2026-09-03
- Host time zone: America/Toronto
- Activity: scientific-paper, official-specification, technical-article/blog
  review, cross-source synthesis, and archive editing
- Kernel implementation: none
- Emulator or physical target: none
- ISA backend exercised: none
- Device/IOMMU/reset profile exercised: none
- Formal or executable model: none
- Benchmarks and fault injection: none
- Local artifacts: Markdown component reports, six source records, map/index
  and inquiry updates, and this journal entry

## Evidence

### Research question and operational standard

For every component, the question was:

> Which implementation best preserves a small reference-monitor boundary while
> making authority, resource consumption, acceptance, cancellation, closure,
> quiescence, recovery, and evidence precise enough to model and test?

A recommendation was accepted only when the report:

- separated claims demonstrated by a source from cross-source synthesis and
  Atom OS-specific proposal;
- identified protected objects, authority facets, generations, payer and
  lifetime ownership, linearization points, terminal outcomes, and teardown
  obligations;
- specified what happens under concurrency, exhaustion, timeout, peer failure,
  missing acknowledgement, and stale completion;
- preserved the lower architecture-support contract and kept BEAM actors and
  OTP policy above privilege;
- compared material alternatives and retained limitations or negative results;
  and
- stated a staged implementation path plus experiments that could falsify the
  preferred design.

### Method

The existing component decomposition supplied the scope. Evidence collection
used three independent source passes:

1. bootstrap, explicit object storage, capabilities, and protection domains;
2. invocation, scheduling contexts, mappings/device bindings, and fault capture;
3. recovery topology, teardown/reclamation, and observability/crash evidence.

Primary papers, current official specifications, and official project manuals
were preferred. Maintainer articles and engineering documentation were used for
implementation constraints and negative operational evidence. Search snippets
located sources but did not support detailed claims. Each source was checked
for the claim actually used and its scope, assumptions, date, implementation,
and evaluation limits.

The archive already contained most source records from the integrated kernel
and architecture research. Six new records were created where this pass
substantively depended on previously unpreserved primary work: capDL, verified
system initialisation, RCU, hazard pointers, DTrace, and the Linux tracing
ring-buffer design.

### Component reports

#### Authority, resources, and execution

- [Bootstrap and root-authority handoff](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff.md)
- [Typed object storage and explicit memory](../20-notes/minimal-privileged-kernel-components/typed-object-storage-and-explicit-memory.md)
- [Capability spaces and authority](../20-notes/minimal-privileged-kernel-components/capability-spaces-and-authority.md)
- [Protection domains, threads, and address spaces](../20-notes/minimal-privileged-kernel-components/protection-domains-threads-and-address-spaces.md)

#### Communication, time, architecture resources, and faults

- [Bounded invocation and transport](../20-notes/minimal-privileged-kernel-components/bounded-invocation-and-transport.md)
- [Scheduling contexts and temporal authority](../20-notes/minimal-privileged-kernel-components/scheduling-contexts-and-temporal-authority.md)
- [Memory mappings and architecture-resource bindings](../20-notes/minimal-privileged-kernel-components/memory-mappings-and-architecture-resource-bindings.md)
- [Fault capture and containment](../20-notes/minimal-privileged-kernel-components/fault-capture-and-containment.md)

#### Recovery, reclamation, and evidence

- [Failure boundaries and recovery topology](../20-notes/minimal-privileged-kernel-components/failure-boundaries-and-recovery-topology.md)
- [Teardown, revocation, and safe reclamation](../20-notes/minimal-privileged-kernel-components/teardown-revocation-and-safe-reclamation.md)
- [Observability and crash evidence](../20-notes/minimal-privileged-kernel-components/observability-and-crash-evidence.md)

### Newly preserved primary sources

- [capDL](../30-sources/kuz-et-al-2010-capdl.md) supports expressing the initial
  kernel-object and capability distribution as explicit analysable data.
- [Formally verified system initialisation](../30-sources/boyton-et-al-2013-verified-system-initialisation.md)
  supplies the model-level precedent for proving an initialiser reaches a
  declarative target while leaving implementation coverage explicit.
- [Read-copy update](../30-sources/mckenney-slingwine-1998-read-copy-update.md)
  separates logical removal from reclamation after pre-existing software readers
  pass quiescence.
- [Hazard pointers](../30-sources/michael-2004-hazard-pointers.md) supplies an
  alternative bounded explicit-reference scheme for lock-free software objects.
- [DTrace](../30-sources/cantrill-et-al-2004-dtrace.md) contributes safe dynamic
  probe, per-consumer, aggregation, and disabled-probe lessons while making its
  larger trusted and timing surface visible.
- [Linux lockless tracing ring-buffer
  design](../30-sources/rostedt-2009-lockless-ring-buffer-design.md) supplies a
  concrete per-CPU nested-writer and record-commit design while making its
  portability, security, and timing limits explicit.

### Strongest cross-component conclusions

1. **Bootstrap is a finite transaction.** The kernel should validate and size a
   canonical authority plan completely, privately construct charged objects,
   publish one graph, obtain a root acknowledgement, and irreversibly seal
   temporary installer authority.
2. **Object memory is never ambient.** Each object has explicit backing, one
   payer, one lifetime group, and reserved failure/teardown state before
   publication.
3. **Immediate revocation needs explicit indirection.** A pre-funded fixed-depth
   anchor can close in constant work; physical lineage removal remains charged
   traversal. This exact construction is a proposal, not a seL4 property.
4. **Products preserve effect-bearing lineage.** A borrowed frame or temporary
   session cannot be laundered into a durable mapping or device relationship.
   Durable detachment requires separately authorized lifetime transfer.
5. **Domain stop begins with fixed gates.** Close admission and dispatch
   preallocated SMP stop requests before walking members, capabilities, or
   objects. A stuck CPU means `STOP_FAILED`, not implied completion.
6. **IPC exposes acceptance and uncertainty.** Calls distinguish rejection,
   reply, and accepted-without-reply. Caller-funded passive handling needs
   server consent, bounded admission, positive budget, and exact donation return.
7. **Time is authority but not confidentiality.** Scheduling contexts enforce
   budget; reductions schedule actors inside runtime capacity; microarchitectural
   time protection is a separate target-specific profile.
8. **Architecture effects are relationships.** Mapping, IRQ, timer, DMA, queue,
   and reset objects retain generations, endpoints, authority, charge, and
   completion evidence. “IOMMU enabled” is not a lifecycle.
9. **Fault evidence is typed and bounded.** Raw and normalized records, certainty,
   loss, containment, and authority are distinct. A resolver receives one exact
   attenuated action, not ambient debug or lifecycle power.
10. **Recovery is an externally funded topology.** Current lease, escrow,
    successor slots, budgets, and effectful fence targets must survive outside
    the child and replaceable supervisor. Missing cooperation defines a wider
    escalation boundary.
11. **Reclamation is a conjunction of quiescence classes.** Software grace
    periods, CPU stop, TLB, calls, IRQ/timer, DMA/IOMMU, device queues/reset,
    diagnostic pins, sanitization, and custody are checked separately.
12. **Observability has failure semantics.** Fixed buffers declare overwrite,
    drop, coalesce, or snapshot behavior; higher-level sections enrich the
    architecture layer's one sealed terminal record and preserve missing CPUs,
    ongoing DMA, truncation, and authenticity limits rather than implying a
    complete trustworthy dump.

### Evidence gaps and falsifiers

The strongest unresolved claims are the Atom OS-specific composition points:

- verified manifest-to-installed-graph relation including recovery and resource
  objects;
- formal authority algebra for bounded anchor paths, product-lineage unions,
  consumed guards, and durable detachment;
- generation no-alias bounds and stable tombstone lifecycle;
- linearizable whole-domain close versus member creation, migration, syscall
  admission, and cross-core stop;
- exact caller-funded acceptance, handler abort, nested donation, and context
  return under every terminal race;
- conserved CPU admission, bounded refill arithmetic, and recovery latency under
  hostile saturation;
- cross-ISA refinement of mapping, TLB, interrupt, timer, and IOMMU completion;
- complete alias enumeration and device-class drain/reset evidence;
- lease takeover across kernel, registry, pager, state service, and device
  commit points;
- idempotent reaping across reaper failure and takeover;
- precise quarantine confinement and custody; and
- cross-layer terminal-record/enrichment concurrency, persistence,
  confidentiality, integrity, and hostile-DMA limitations.

Any prototype that silently assumes completion after timeout, redirects a stale
token to a replacement, creates an uncharged privileged record, loses a donated
context, reuses a frame before all access paths close, or lets an old recovery
epoch mutate a current target falsifies the baseline contract.

### Evidence boundary

This session did not:

- implement or boot a kernel;
- execute a capability, domain, IPC, scheduler, mapping, fault, recovery,
  teardown, or trace state machine;
- run an emulator, architecture conformance suite, TLB shootdown, IOMMU, DMA,
  interrupt, timer, device-reset, or persistent-crash experiment;
- prove a manifest installer, authority algebra, state machine, refinement,
  information-flow property, or worst-case execution bound;
- benchmark syscall, IPC, scheduling, cancellation, mapping, fault, teardown,
  tracing, or recovery latency;
- inject a CPU, domain, runtime, driver, device, firmware, memory, or kernel
  fault; or
- run compiled BEAM code over the proposed contract.

Consequently, paper measurements apply only to their evaluated systems and
hardware; architecture specifications define mechanisms, not platform routing
or implementation correctness; and the component recommendations remain
developing syntheses with explicit experiments rather than transferred proofs.

## Threads

- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) routes
  through the eleven detailed reports and their evidence families.
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
  remains open and now names the component models and experiments needed to
  resolve it.
- [Kernel hardware and architecture support](../20-notes/kernel-hardware-and-architecture-support-layer.md)
  owns the privileged machine mechanisms refined by mapping, event, CPU, and
  device completion objects.
- [Managed actor runtime](../20-notes/managed-actor-runtime-layer.md) consumes
  domains, budgets, calls, faults, and recovery evidence while keeping actors,
  garbage collection, mailboxes, and OTP policy unprivileged.

## Follow-ups

1. Formalize the capability/anchor/product-lineage algebra and generate the
   object-operation authority matrix from one schema.
2. Build executable models for bootstrap, domain stop, call cancellation and
   donation, lease takeover, and typed reaping before selecting data structures.
3. Implement a single-CPU object/capability/domain kernel with fixed resources,
   then add SMP stop and cross-CPU mapping completion.
4. Build one emulated device profile with IRQ, finite queue ownership, IOMMU,
   delayed completion, failed reset, and quarantine.
5. Demonstrate an independently resourced supervisor takeover and fresh-domain
   publication while a stale old supervisor resumes and is fenced.
6. Instrument the prototype with the minimal typed events and validate their
   post-seal enrichment of the architecture layer's terminal record, including
   truncation and survival semantics on each named target.
7. Run a BEAM-compatible runtime domain over the contract and measure actor
   responsiveness, native service failure, and recovery under kernel budgets.
