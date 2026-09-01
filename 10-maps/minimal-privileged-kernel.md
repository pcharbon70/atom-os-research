---
title: "Minimal privileged kernel"
kind: map
created: "2026-08-31"
tags:
  - capabilities
  - fault-containment
  - microkernels
  - operating-systems
aliases:
  - "Capability microkernel research"
---

# Minimal privileged kernel

## Scope

This map covers the privileged enforcement layer immediately above the
[kernel hardware and architecture support
layer](kernel-hardware-and-architecture-support.md) and below the managed BEAM
runtime and unprivileged system services. It routes through capability
authority, protected invocation, CPU budgets, failure boundaries, teardown,
driver containment, and assurance. It excludes BEAM actor implementation, OTP
restart policy, device protocols, filesystems, and physical board design.

## Start here

- [Minimal privileged kernel
  layer](../20-notes/minimal-privileged-kernel-layer.md) — proposes the full
  capability-microkernel contract, object model, component boundaries,
  bounded stop and teardown state machines, passive-call admission/failure
  policy, recovery escrow, DMA quarantine, BEAM mapping, and implementation
  sequence.
- [What contract should the minimal privileged kernel
  provide?](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) —
  keeps the proposal falsifiable through explicit authority, isolation,
  recovery, boundedness, portability, and compatibility criteria.
- [2026-08-31 minimal privileged-kernel deep
  dive](../50-journal/2026-08-31-minimal-privileged-kernel-deep-dive.md) — records
  the literature search, synthesis method, source scope, and absence of local
  implementation evidence.

## Selected contract

The baseline makes domain termination a bounded event: `CLOSING` atomically
closes the already installed fixed vector of execution,
relationship/lifetime-derivation, outbound-call, and session root gates,
freezes the admitted membership set, creates the stop epoch, and dispatches
preallocated per-CPU stop requests before any capability or object traversal.

One `DmaAddressSpace` covers the complete immutable atomic requester/trust set;
inseparable mutually distrustful requesters are not claimed as isolated.
Global frame quarantine permanently stales every old mutating facet and
mapping. Release requires all physical paths to be quiescent, destroys the old
`Frame`, and retypes its backing as a new generation rather than reopening old
authority.

## Trails

### Where privilege stops

- [The protection of information in computer
  systems](../30-sources/saltzer-schroeder-1975-protection-information.md) gives
  the reference-monitor principles used as inclusion and review tests.
- [On micro-kernel
  construction](../30-sources/liedtke-1995-microkernel-construction.md) argues
  for functional minimality and protected address spaces, threads, and IPC.
- [From L3 to seL4](../30-sources/elphinstone-heiser-2013-l4-lessons.md) traces
  why capabilities, user-level policy, bounded paths, and architecture-aware
  fast paths survived successive microkernel designs.
- [seL4 design
  principles](../30-sources/heiser-2020-sel4-design-principles.md) is a
  practitioner explanation of minimizing the privileged mechanism surface.
- [Exokernel](../30-sources/engler-et-al-1995-exokernel.md) separates enforceable
  protection from user-level resource-management policy.

### Capabilities and explicit resources

- [seL4 reference manual, version
  16.0.0](../30-sources/sel4-foundation-2026-reference-manual.md) documents a
  concrete modern object, capability, untyped-memory, IPC, fault, and
  scheduling-context API.
- [EROS: A fast capability
  system](../30-sources/shapiro-et-al-1999-eros.md) demonstrates a pure
  capability object model and fast invocation while raising a different
  persistence trade-off.
- [Capability myths
  demolished](../30-sources/miller-et-al-2003-capability-myths.md) explains how
  indirection and application structure support confinement and revocation.
- [Capsicum](../30-sources/watson-et-al-2010-capsicum.md) supplies pragmatic
  evidence for capability mode and rights-limited descriptors in a Unix
  environment.
- [Kernel design for isolation and assurance of physical
  memory](../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) links
  explicit kernel-object memory to isolation and proof tractability.

The synthesis turns these precedents into a stricter product-lifetime rule:
each kernel product retains the stable lineage of every input that supplies
future-effect authority. Consumed guards are classified explicitly, and an
effect-bearing dependency can be detached only through separately authorized
durable creation and lifetime consent.

### IPC, time, and availability

- [Scheduler activations](../30-sources/anderson-et-al-1992-scheduler-activations.md)
  separates kernel processor allocation from a runtime's fine-grained thread
  scheduler and records upcall and reentrancy costs.
- [Vulnerabilities in synchronous IPC
  designs](../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md) maps
  call-chain, dependency, and denial-of-service risks that reply and
  cancellation semantics must address.
- [Scheduling-context
  capabilities](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)
  makes CPU budget explicit and supports caller-funded passive servers.
- [Time protection](../30-sources/ge-et-al-2019-time-protection.md) distinguishes
  bounded CPU consumption from protection against microarchitectural timing
  channels.
- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md) motivates
  explicit cross-core communication and local state on heterogeneous
  multicore systems.
- [For a microkernel, a big lock is
  fine](../30-sources/peters-et-al-2015-big-lock-microkernel.md) compares kernel
  locking strategies and makes its moderate-core, workload-dependent conclusion
  explicit.

For this platform, caller-funded passive IPC is a privileged deployment mode,
not the default client API. It requires finite shared admission credits, a
preauthorized failure-scope object, an atomic accepted/ready/donation commit,
reply authority bound to the exact accepted receiver, and a domain-fatal
generic abort path. Endpoint close is represented as another funded
failure-propagation trigger. Only manifest-validated isolated worker profiles
may use thread-local terminal abort; ordinary untrusted clients use
server-funded endpoints.

### Fault containment and recovery

- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
  supplies the isolation and supervision model that remains above the kernel.
- [Unreliable failure
  detectors](../30-sources/chandra-toueg-1996-failure-detectors.md) distinguishes
  proven failure from time-dependent suspicion.
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md) evaluates
  fine-grained component restart and exposes the importance of state and
  dependency design.
- [CuriOS](../30-sources/david-et-al-2008-curios.md) isolates client-associated
  state to improve service recovery.
- [Construction of a highly dependable operating
  system](../30-sources/herder-et-al-2006-dependable-operating-system.md) moves
  drivers into restartable user-space processes.
- [Nooks](../30-sources/swift-et-al-2003-nooks.md) and [recovering device
  drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md) provide
  contrasting compatibility-oriented driver recovery evidence.
- [Hive](../30-sources/chapin-et-al-1995-hive.md) shows why shared-memory and
  correlated hardware failure complicate fault containment.
- [Tolerating malicious device drivers in
  Linux](../30-sources/boyd-wickizer-zeldovich-2010-malicious-device-drivers.md) tests a
  stronger adversarial driver model than accidental-crash recovery alone.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) and
  [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md) connect
  explicit buffer ownership with the limits of IOMMU-only DMA containment.

Recovery authority is split deliberately: sealed current lease-use facets
fence mutations, while independently derived `RecoveryEscrow` and
`ResetControl` objects hold only the attenuated authority, resources, and
protected destination slots needed for successor takeover. Neither successor
path depends on extracting authority from a failed child or replaceable
manager. Reset takeover fences mediated manager admissions immediately, while
physical fencing remains split-phase: the old manager must be terminally
stopped or every profile-declared writable alias revoked through completed TLB
invalidation before the successor can reset, attest completion, or release a
frame.

### Assurance and configuration

- [Timing analysis of a protected operating-system
  kernel](../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)
  shows how configuration, executable paths, cache/pipeline models, and target
  hardware bound a claim of worst-case kernel latency.
- [Comprehensive formal verification of an OS
  microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
  establishes a proof ladder while making trusted assumptions visible.
- [seL4 information-flow
  enforcement](../30-sources/murray-et-al-2013-sel4-information-flow.md) shows
  that secure kernel mechanisms still require a correct configured authority
  graph.
- [CertiKOS](../30-sources/gu-et-al-2016-certikos.md) supplies layered
  observable specifications and contextual refinement.
- [Design and verification of secure
  systems](../30-sources/rushby-1981-design-verification-secure-systems.md)
  motivates an explicit abstract separation machine and policy.

### Layer connections

- [Kernel hardware and architecture
  support](kernel-hardware-and-architecture-support.md) covers the lower entry,
  context, translation, interrupt, timer, CPU, I/O, DMA, and fault mechanisms.
- [BEAM, ERTS, and OTP](beam-erts-and-otp.md) covers the required managed actor
  semantics and the policy that must remain outside privilege.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
  places this layer within the complete platform decomposition.

## Open questions

- Can stable, caller-funded revocation anchors with bounded protected paths and
  incremental physical traversal scale to realistic runtime, driver, and
  service object graphs?
- Which synchronous-call and scheduling-context donation rules remain safe and
  usable across cores once finite passive admission, conditional domain-fatal
  policy, ready-before-dispatch budget checks, and cancellation drainage are
  included?
- How should the boot authority checker bound cycles and blast radius in the
  graph of passive-call failure policies without making useful call patterns
  impossible?
- How can recovery-lease takeover fence an old supervisor across kernel state,
  service publication, state repair, and devices when it was suspected but
  later resumes; how are escrow and protected destination slots recovered if a
  control holder fails; and which external effects cannot participate?
- What is the minimum privileged resource ledger that permits supervisor
  recovery while keeping quota payer, ownership/lifetime, and recovery control
  distinct?
- Which device classes admit immutable trusted drain/reset profiles, complete
  revocation of direct submission aliases, trustworthy completion evidence,
  immutable atomic requester/trust sets, independently fenced shared-reset
  leases, and permanent invalidation of pre-quarantine frame authority—and
  when must a remaining effect force quarantine or node reset?
- How should language-level actor authority be brokered without treating a PID
  as authority or making the runtime a confused deputy?
- What security configurations can be checked automatically from the initial
  capability manifest?
- Which properties should be modeled, tested, and proved at each prototype
  phase?

The active [minimal privileged-kernel contract
inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
tracks these questions and their required evidence.
