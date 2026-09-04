---
title: "Atom OS Research"
kind: map
created: "2026-08-28"
tags:
  - beam
  - operating-systems
  - otp
aliases:
  - "Home"
---

# Atom OS Research

This is the selective entry point to research on a new kernel and operating
system informed by Erlang/OTP and BEAM principles. See the [archive
guide](../README.md) for the repository structure and working conventions.

## Research objective

Determine which actor, isolation, scheduling, recovery, upgrade, and
distribution principles should shape the kernel and wider system, then
establish a credible path from research prototypes to a bootable system. The
platform must run compiled BEAM code with BEAM-compatible process semantics,
including automatic process-local tracing garbage collection, without making
one existing VM implementation the kernel foundation.

## Active inquiries

- [What contract should system-wide authentication and authorization
  provide?](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md) —
  defines falsifiable human, workload, policy, capability, revocation,
  recovery, distributed-consistency, and assurance criteria across all five
  layers.
- [What contract should the OTP-like system-services layer
  provide?](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) —
  defines falsifiable lifecycle, durability, outcome, naming, distributed
  authority, update, overload, evidence, and recovery criteria for the fourth
  system layer.
- [What contract should the managed actor runtime
  provide?](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) —
  defines falsifiable compatibility, actor-memory, signal, scheduling,
  resource, native-isolation, distribution, and replay criteria for the third
  system layer.
- [What contract should the minimal privileged kernel
  provide?](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) —
  defines falsifiable capability, domain, IPC, CPU-budget, fault, teardown,
  recovery-independence, portability, and BEAM-compatibility criteria.
- [What contract should the kernel hardware and architecture layer
  provide?](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) —
  defines falsifiable authority, completion, isolation, ordering, portability,
  failure, and performance criteria for the privileged mechanism boundary.
- [Which BEAM, ERTS, and OTP principles belong in a new
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md) —
  defines the experiments needed to place required BEAM-compatible runtime
  mechanisms at the right system layer and choose between runtime strategies.
- [Can AtomVM serve as the kernel-facing runtime of a new embedded operating
  system?](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md) —
  retains AtomVM as one concrete implementation case and defines its boot,
  substrate, resource, fault, trust, and lifecycle evidence requirements.

## Topic maps

- [Authentication and authorization](authentication-and-authorization.md) —
  routes from human, workload, node, and recovery evidence through typed
  policy and bounded grants to capability enforcement, revocation, audit,
  update, and recovery.
- [OTP-like system services](otp-like-system-services.md) — routes through
  behaviours, supervision, application lifecycle, names, configuration,
  durable outcomes, device/network policy, distributed coordination, releases,
  overload, telemetry, audit, and operator control.
- [Managed actor runtime](managed-actor-runtime.md) — routes through compiled
  BEAM compatibility, private heaps and collection, signal and mailbox design,
  two-level scheduling, code publication, native boundaries, distribution,
  testing, and evaluation.
- [Minimal privileged kernel](minimal-privileged-kernel.md) — routes through
  the capability, protected-domain, bounded-IPC, temporal-authority, failure,
  driver-containment, teardown, and assurance evidence for the layer above
  architecture support.
- [Kernel hardware and architecture
  support](kernel-hardware-and-architecture-support.md) — routes through the
  kernel-level evidence for entry/context, translation, ordering and code
  publication, interrupts, time, CPU lifecycle, protected I/O, and faults while
  excluding board and physical-component engineering.
- [BEAM, ERTS, and OTP](beam-erts-and-otp.md) — separates the instruction
  machine, runtime mechanisms, and OTP policy, then routes through current
  documentation, source, foundational papers, scalability evidence, and the OS
  design synthesis.
- [AtomVM foundation](atomvm-foundation.md) — routes through the current
  architecture, measurements, and open questions for one compact BEAM
  implementation.

## Recently developed

- [Authentication and authorization across the five-layer
  architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md) —
  proposes an identity/policy control plane plus a capability data plane, with
  explicit anonymous authority, trusted interaction, exact grant contracts,
  distributed freshness, recovery, and a staged assurance program.
- [2026-09-04 authentication and authorization research
  session](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md) —
  records the scientific and standards search, current source revisions,
  independent architecture review, and absence of implementation evidence.
- [OTP-like system services
  layer](../20-notes/otp-like-system-services-layer.md) — proposes thirteen
  unprivileged policy components with explicit generations, effect outcomes,
  sink-enforced fencing, staged updates, overload control, and separate
  telemetry and audit paths.
- [2026-09-03 OTP-like system services research
  session](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md) —
  records the current OTP baseline, papers, standards, engineering evidence,
  synthesis method, and absence of prototype evidence.
- [Minimal privileged kernel component deep
  dives](minimal-privileged-kernel.md#component-implementation-deep-dives) —
  develops one evidence-backed implementation recommendation for each of the
  eleven capability-microkernel components while preserving the hardware,
  managed-runtime, and OTP-policy boundaries.
- [2026-09-03 minimal privileged kernel component research
  session](../50-journal/2026-09-03-minimal-privileged-kernel-components-deep-dive.md) —
  records the expanded primary-source review, common lifecycle and authority
  method, proposed state machines, falsifiers, and explicit absence of
  prototype evidence.
- [Managed actor runtime component deep
  dives](managed-actor-runtime.md#component-implementation-deep-dives) —
  develops one evidence-backed implementation recommendation for each of the
  thirteen runtime components while preserving the capability-kernel and
  OTP-policy boundaries.
- [2026-09-03 managed actor runtime component research
  session](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md) —
  records the expanded primary-source review, cross-component method, proposed
  state machines, and explicit absence of prototype evidence.
- [Managed actor runtime
  layer](../20-notes/managed-actor-runtime-layer.md) — proposes an unprivileged
  BEAM-compatible runtime with thirteen components, explicit critical paths,
  private tracing heaps, sender-ordered signals, kernel-time reconciliation,
  isolated native services, and a staged conformance program.
- [2026-09-02 managed actor runtime deep
  dive](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md) — records
  the OTP 29.0.6 baseline, papers and engineering articles reviewed,
  comparative-runtime assumptions, and absence of implementation evidence.
- [Minimal privileged kernel
  layer](../20-notes/minimal-privileged-kernel-layer.md) — proposes a capability
  microkernel with explicit object resources, coordinated execution-stop
  domains, bounded invocation and CPU budgets, typed fault routes, and clean or
  quarantined reaping outcomes.
- [2026-08-31 minimal privileged-kernel deep
  dive](../50-journal/2026-08-31-minimal-privileged-kernel-deep-dive.md) — records
  the primary literature, articles, design review trails, and evidence limits
  behind the proposal.
- [Kernel hardware and architecture support
  layer](../20-notes/kernel-hardware-and-architecture-support-layer.md) —
  proposes eleven semantic components, explicit authority and quiescence
  lifecycles, a cross-architecture comparison, and a phased verification plan.
- [Kernel hardware and architecture component deep
  dives](kernel-hardware-and-architecture-support.md#component-implementation-deep-dives) —
  develops one evidence-backed implementation recommendation for each of the
  eleven components while preserving the capability-kernel and managed-runtime
  boundaries.
- [2026-09-02 component implementation research
  session](../50-journal/2026-09-02-kernel-architecture-components-deep-dive.md) —
  records the expanded source review, cross-component synthesis method, and
  explicit absence of prototype evidence.
- [2026-08-30 kernel hardware and architecture support deep
  dive](../50-journal/2026-08-30-kernel-hardware-and-architecture-support-deep-dive.md) —
  records the literature search, exact kernel-level scope, primary sources,
  method, and absence of implementation evidence.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  proposes a layered design with actor-friendly kernel mechanisms, required
  BEAM-compatible managed execution and process-local tracing collection, and
  user-space OTP recovery policy while strengthening security and resource
  control.
- [2026-08-28 BEAM, ERTS, and OTP deep
  dive](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md) — records the
  pinned OTP 29.0.5 source audit, literature search, practitioner survey, and
  evidence limits.
- [AtomVM as an operating-system
  foundation](../20-notes/atomvm-as-an-operating-system-foundation.md) —
  assesses one possible compact execution nucleus and its native isolation
  limits.

## Unsettled threads

- Select the first security deployment profile and model the complete
  anonymous-to-authenticated-to-capability authority graph before building a
  login UI or compatibility superuser.
- Specify native trusted interaction, pre-boot storage unlock, credential and
  data-key recovery, policy activation, revocation watermarks, and maximum
  stale-authority windows for each protected operation class.
- Model capability derivation, call cancellation, scheduling-context donation,
  SMP domain freeze, and quiescence-gated reaping before choosing kernel data
  structures or optimizing fast paths.
- Define a checked initial authority manifest and prove that each supervisor's
  CPU, memory, fault path, and teardown reserve remains outside the child's
  reach.
- Validate the proposed architecture-support contracts with executable state
  models, one virtual target, and eventually a materially different second ISA.
- Define completion and failure budgets for cross-CPU mapping, code
  publication, interrupt delivery, CPU quiescence, and DMA revocation.
- Decide whether the first compatibility prototype should port a pinned ERTS
  or execute a declared BEAM/OTP profile in a new runtime; a principles-only
  runtime no longer satisfies the platform goal.
- Define the exact OTP 29.0.6 compatibility profile, mailbox-limit behavior,
  shared-binary charging, and native boundary before calling the managed layer
  compatible.
- Turn the thirteen managed-runtime component state machines and falsifiers
  into executable models, conformance fixtures, and measured prototypes.
- Turn the thirteen OTP-like system-service components, effect-outcome states,
  distributed leases/fences, and update lifecycle into executable models and
  fault-injected prototypes.
- Validate the proposed capability, quota, bounded-transport, and
  failure-domain semantics against a BEAM runtime without making each actor a
  kernel object.
- Measure reduction-style accounting against wall-clock latency, interrupt
  pre-emption, native work, and priority inversion.
- Demonstrate boot, driver-fault containment, crash-consistent persistence,
  authenticated distribution, atomic update/rollback, and retained diagnostics.
