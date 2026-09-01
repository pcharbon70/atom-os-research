---
title: "2026-08-31 minimal privileged-kernel deep dive"
kind: journal
created: "2026-08-31"
tags:
  - capabilities
  - fault-containment
  - literature-review
  - microkernels
  - operating-systems
aliases:
  - "Minimal privileged kernel research session"
---

# 2026-08-31 minimal privileged-kernel deep dive

## Observations

This session investigated the privileged layer immediately above the existing
[kernel hardware and architecture support
research](../20-notes/kernel-hardware-and-architecture-support-layer.md). The
scope was kernel mechanism, not board design, physical components, a complete
BEAM runtime, or OTP policy.

The strongest cross-source synthesis is that capability enforcement and
failure recovery cannot be designed independently. A capability revocation can
deny new calls while old CPU translations, synchronous calls, interrupts, and
DMA remain active. Conversely, a supervisor cannot recover a component if its
control authority, CPU budget, memory, or teardown capacity was placed inside
the failed component's resource subtree.

The resulting proposal therefore treats the following as one contract:

- typed capabilities with stable caller-funded revocation anchors, bounded
  anchor paths, explicit product-lifetime dependencies, scoped generations,
  and explicit kernel-object memory;
- first-class multicore domains whose fixed root gates close and dispatch
  bounded stop requests before incremental cleanup, without claiming shared or
  external state is fail-stop;
- generation-safe CPU/DMA mapping objects and exclusive domain roots;
- bounded IPC with pre-accept call records, origin gates, one-shot reply
  authority bound to the exact receiver, caller/server funding modes, exact
  active-thread donation reservation, finite passive admission credits,
  preauthorized failure scope, and success/cancellation drainage that cannot
  re-enter an aborted passive handler;
- scheduling-context capabilities, exclusive donation state, admitted-kernel
  work reserves, and non-donatable recovery contexts;
- typed fault routes that distinguish resolvable faults, fatal events, and
  proof from suspicion;
- sealed epoch-fenced recovery ownership extending through registry and
  state-repair sessions, with successor authority held in an independently
  derived recovery escrow;
- immutable device profiles and atomic requester/trust attachment sets,
  independently resourced management routes, and separately escrowed
  reset-domain control whose logical lease takeover remains distinct from
  terminal stop or completed revocation of an old manager's direct aliases;
- logical invalidation followed by architecture-visible quiescence or bounded
  global frame quarantine that permanently stales old mutating facets; and
- user-space supervision that relates a distinct replacement domain to a new
  logical-service epoch.

The work produced the [minimal privileged kernel
synthesis](../20-notes/minimal-privileged-kernel-layer.md), its [topic
map](../10-maps/minimal-privileged-kernel.md), and an open [contract
inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md).

## Environment

- Repository: `atom-os-research`
- Research date: 2026-08-31
- Host time zone: America/Toronto
- Activity: documentation, literature search, source reading, and architecture
  synthesis only
- Kernel target: none selected or executed
- ISA target: none executed; the proposed contract is intended to compose with
  the previously researched architecture facade
- BEAM runtime: none built or executed in this session
- Hardware or simulator: none used
- Local code changes: Markdown research artifacts and indexes only

Temporary reading copies of available papers were used for detailed review but
are not durable archive assets. The source notes retain canonical or
author-hosted URLs and exact metadata where the primary record supplied them.

## Evidence

### Search and selection method

The review started from the system decomposition in [BEAM, ERTS, and OTP
principles for a new operating
system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
and treated the hardware/architecture layer as a fixed lower contract. Searches
then covered:

- reference-monitor principles, least privilege, and capability security;
- microkernel minimality, protected IPC, explicit object memory, and formal
  assurance;
- capability derivation, delegation, confinement, selective revocation, and
  pragmatic capability APIs;
- scheduling contexts, budget donation, temporal isolation, and timing-channel
  protection;
- recoverable services, microreboots, device-driver isolation, client-state
  recovery, and malicious drivers;
- failure detection, fail-stop assumptions, correlated multiprocessor failure,
  and recovery-resource independence;
- shared-memory queue ownership, IOMMU limits, DMA quiescence, and device reset;
  and
- the division between BEAM process semantics, runtime failure, and outer
  system supervision.

Primary papers, current official documentation, author/project-hosted copies,
and DOI records were preferred. Articles and blog posts were used for design
rationale or practitioner interpretation, not as substitutes for primary
experimental or formal claims. Search snippets and abstracts were not used as
evidence for detailed findings.

### Protection and capability foundations

- Jerome H. Saltzer and Michael D. Schroeder, “The Protection of Information
  in Computer Systems,” 1975:
  https://web.mit.edu/Saltzer/www/publications/protection/Basic.html
- Jochen Liedtke, “On Micro-Kernel Construction,” 1995:
  https://doi.org/10.1145/224056.224075
- Kevin Elphinstone and Gernot Heiser, “From L3 to seL4,” 2013:
  https://doi.org/10.1145/2517349.2522720
- Matthew Grosvenor and Adam Walker, *seL4 Reference Manual*, version 16.0.0:
  https://sel4.systems/Info/Docs/seL4-manual-16.0.0.pdf
- Gernot Heiser, “seL4 Design Principles,” 2020:
  https://microkerneldude.org/2020/03/11/sel4-design-principles/
- Jonathan S. Shapiro, Jonathan M. Smith, and David J. Farber, “EROS: A Fast
  Capability System,” 1999: https://doi.org/10.1145/319151.319163
- Mark S. Miller, Ka-Ping Yee, and Jonathan Shapiro, “Capability Myths
  Demolished,” 2003:
  https://erights.org/talks/myths/index.html
- Robert N. M. Watson et al., “Capsicum,” 2010:
  https://www.usenix.org/conference/usenixsecurity10/capsicum-practical-capabilities-unix
- Dawson R. Engler et al., “Exokernel,” 1995:
  https://doi.org/10.1145/224056.224076
- Dhammika Elkaduwe, Philip Derrin, and Kevin Elphinstone, “Kernel Design for
  Isolation and Assurance of Physical Memory,” 2008:
  https://doi.org/10.1145/1435458.1435465

### IPC, scheduling, and assurance

- Thomas E. Anderson et al., “Scheduler Activations,” 1992:
  https://doi.org/10.1145/146941.146944
- Jonathan S. Shapiro, “Vulnerabilities in Synchronous IPC Designs,” 2003:
  https://doi.org/10.1109/SECPRI.2003.1199341
- Anna Lyons et al., “Scheduling-Context Capabilities,” 2018:
  https://doi.org/10.1145/3190508.3190539
- Qian Ge et al., “Time Protection: The Missing OS Abstraction,” 2019:
  https://doi.org/10.1145/3302424.3303976
- Toby Murray et al., “seL4: From General Purpose to a Proof of Information
  Flow Enforcement,” 2013: https://doi.org/10.1109/SP.2013.35
- Gerwin Klein et al., “Comprehensive Formal Verification of an OS
  Microkernel,” 2014: https://doi.org/10.1145/2560537
- Ronghui Gu et al., “CertiKOS,” 2016:
  https://www.usenix.org/conference/osdi16/technical-sessions/presentation/gu
- John Rushby, “Design and Verification of Secure Systems,” 1981:
  https://doi.org/10.1145/800216.806586
- Andrew Baumann et al., “The Multikernel,” 2009:
  https://doi.org/10.1145/1629575.1629579
- Bernard Blackham et al., “Timing Analysis of a Protected Operating System
  Kernel,” 2011: https://doi.org/10.1109/RTSS.2011.38
- Sean Peters et al., “For a Microkernel, a Big Lock Is Fine,” 2015:
  https://doi.org/10.1145/2797022.2797042

### Failure containment and recovery

- Joe Armstrong, *Making Reliable Distributed Systems in the Presence of
  Software Errors*, 2003:
  https://erlang.org/download/armstrong_thesis_2003.pdf
- Tushar Deepak Chandra and Sam Toueg, “Unreliable Failure Detectors for
  Reliable Distributed Systems,” 1996:
  https://doi.org/10.1145/226643.226647
- George Candea et al., “Microreboot,” 2004:
  https://www.usenix.org/conference/osdi-04/microreboot%E2%80%94-technique-cheap-recovery
- Francis M. David et al., “CuriOS,” 2008:
  https://www.usenix.org/conference/osdi-08/curios-improving-reliability-through-operating-system-structure
- Jorrit N. Herder et al., “Construction of a Highly Dependable Operating
  System,” 2006:
  https://doi.org/10.1109/EDCC.2006.7
- Michael M. Swift et al., “Nooks,” 2003:
  https://doi.org/10.1145/945445.945466
- Michael M. Swift et al., “Recovering Device Drivers,” 2004:
  https://www.usenix.org/conference/osdi-04/recovering-device-drivers
- John Chapin et al., “Hive,” 1995:
  https://doi.org/10.1145/224056.224059
- Silas Boyd-Wickizer and Nickolai Zeldovich, “Tolerating Malicious Device
  Drivers in Linux,” 2010:
  https://www.usenix.org/conference/usenix-atc-10/tolerating-malicious-device-drivers-linux

### I/O, DMA, and runtime adjacency

- Reto Achermann et al., “A Least-Privilege Memory Protection Model for Modern
  Hardware,” 2019: https://doi.org/10.48550/arXiv.1908.08707
- Simon Haecki et al., “CleanQ,” 2019:
  https://doi.org/10.48550/arXiv.1911.08773
- Theodore Markettos et al., “Thunderclap,” 2019:
  https://doi.org/10.14722/ndss.2019.23194
- Erlang/OTP current system documentation:
  https://www.erlang.org/doc/system/
- Erlang/OTP source repository:
  https://github.com/erlang/otp

Each substantively used primary work has a separate record in
[the source index](../30-sources/README.md), with method, findings, relevance,
limits, and derived-work links. Secondary commentary was used conservatively
and its role is labeled in its source note.

### Synthesis checks

Three independent review passes were used to challenge the design from
different directions:

1. capability representation, delegation, revocation, and stale-authority
   defense;
2. minimal kernel objects, IPC, scheduling, mapping, and architecture
   composition; and
3. failure taxonomy, supervisor independence, teardown, driver recovery, and
   external-state reconciliation.

The passes converged on several non-negotiable distinctions:

- capability validity is not effect completion;
- authority is not ownership, identity, budget, or liveness;
- domain stop is not quiescence or safe reuse;
- cancellation selection is not callee drainage or immediate return of donated
  time; acceptance first publishes a non-executing ready state, server-funded
  calls have no donation to return, and generic failure of a caller-funded
  passive handler is domain-fatal unless a trusted isolated-worker profile
  authorizes terminal thread-local abort;
- caller-funded passive service also requires finite cleanup credit and a
  preauthorized conditional failure boundary; ordinary send authority alone
  cannot impose recovery work or termination scope on a server, while endpoint
  close authority is itself an explicit funded failure-propagation trigger;
- one recovery owner requires a sealed atomic lease epoch plus independently
  derived escrowed successor authority, not an unfenced convention or a cap
  stranded in the failed supervisor;
- device drain, reset, mapping removal, and interrupt masking have no universal
  order outside a declared device contract;
- an IOMMU translation root cannot claim isolation more narrowly than its
  immutable atomic requester/trust attachment set, and quarantine release
  cannot reactivate any old frame authority;
- reset-lease turnover denies later mediated manager calls but cannot revoke a
  writable MMIO or queue alias without terminal stop or mapping/TLB
  quiescence;
- a definite fault is not a heartbeat suspicion;
- restart is not state recovery; and
- BEAM actor isolation is not a native-code or runtime protection boundary.

### Evidence boundary

No source demonstrates this complete proposed kernel. seL4 supports important
capability, explicit-memory, IPC, scheduling, fault, and assurance precedents;
other work supplies device recovery, state placement, failure-detection, and
DMA constraints. Combining them is the archive's synthesis.

No local executable model, kernel source, build, simulator run, hardware test,
fault injection, performance benchmark, formal proof, driver implementation,
or compiled-BEAM execution was performed. Statements about the proposed object
model, state machines, API, and phase plan are therefore marked as design
decisions or hypotheses rather than demonstrated behavior.

## Threads

- The [minimal privileged-kernel contract
  inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
  needs an executable model for revocation anchors and product dependencies,
  passive admission/policy and pre-accept/reply/cancel drainage, scheduling
  donation, escrowed recovery-lease takeover and external fencing, fixed-gate
  SMP suspend/stop, thread reaping, immutable DMA attachment sets, trusted
  device profiles and reset control, and clean-versus-quarantined teardown
  before implementation choices harden.
- The lower [architecture-support contract
  inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  still needs concrete completion semantics for TLB, IRQ, IOMMU, DMA, and CPU
  quiescence on selected targets.
- A future runtime inquiry must define how opaque language-level capabilities
  map to a runtime domain without turning PIDs into authority or requiring one
  kernel object per BEAM process.
- Device selection must follow, not precede, a required reset and quiescence
  contract for the driver-containment experiment.

## Follow-ups

1. Write an executable abstract model of capability derivation, stable anchor
   closure, effect-bearing product lineage, consumed guards, physical
   traversal, and safe object generation reuse.
2. Add finite passive-admission and policy creation, accepted/ready/active
   atomicity, reply/cancel/death transitions, domain-fatal versus profiled abort,
   and prove at-most-one outcome plus exact nested scheduling-context return
   within bounded depth.
3. Model thread and domain suspension, stop, teardown, trusted completion, and
   clean-versus-quarantined reaping as distinct states.
4. Define a versioned initial capability, recovery-resource/escrow,
   cancellation-profile, immutable DMA attachment-set, device-profile, and
   reset-control manifest.
5. Select one virtual single-core architecture profile only after the model's
   required lower-layer operations are explicit.
6. Prototype explicit object memory, capability lookup, domains, and small IPC
   before adding drivers or BEAM integration.
7. Design fault-injection matrices and measurement budgets before claiming
   containment, recovery, portability, or performance.
