---
title: "Minimal privileged-kernel internal-service research"
kind: journal
created: "2026-09-09"
tags: [capabilities, deep-dive, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Minimal privileged-kernel internal-service research

## Question and scope

How should each previously undecomposed component of the minimal privileged
kernel be divided into internal services with explicit state ownership,
authority, completion and failure contracts?

The starting [component inventory](../20-notes/minimal-privileged-kernel-components/README.md)
contained eleven parent reports, numbered 0–10, and no internal-service
subdirectories. This session adds a decomposition for every component. It
follows the existing hardware-architecture service-report pattern while
remaining at the higher privileged enforcement boundary.

This is full-system architecture research, not a PoC, QEMU or physical-board
qualification pass. It does not implement a kernel, amend a milestone plan,
choose a compiler pin or change the selected Zig language. BEAM actors,
compiled-BEAM execution, automatic process-local tracing GC and OTP supervision
remain outside the privileged kernel. The reports are developing proposals,
not accepted implementation results.

## Research method

Read the repository conventions, artifact templates, schema, existing
component contracts and relevant source records. Extract services by their
distinct owned state and admission/completion obligations, preserving the
parents' integrated lifecycles. Counts vary with the required boundaries:
for example, architecture-resource binding has six reports while fault
handling and teardown each have four. A shared template supplies questions,
not a quota of services.

Search families included declarative initialization and capability-graph
validation; capability-table delegation and revocation policy; protected IPC,
passive-server donation and cancellation; bounded scheduling/refills;
stalled-participant reclamation; service-state recovery; hardware-effect
containment; and trace/crash evidence. Scientific work supplies formal models,
algorithms and experimental limitations. Official technical documentation
supplies concrete contracts. First-party blogs contribute design alternatives,
not proof or universal performance claims.

Read relevant primary sections rather than treating search snippets as
evidence. Reuse existing bibliographic notes instead of duplicating papers.
New records distinguish the capDL loader's documentation from the already
archived capDL and initialization papers. Each service report links source
notes near its research basis and records its own proposed protocol separately.

No local kernel, language, model-checking, emulator, hardware or performance
experiment was run. Verification cases in the reports are proposals for
falsifying their contracts; none is represented as a pass.

## Reading depth and access limitations

New primary readings covered:

- Brown's PODC 2015 work in its 2017 arXiv full version, especially the system
  model, reclamation alternatives and DEBRA+ neutralization/recovery sections.
  The author's Toronto-hosted PDF timed out; the arXiv PDF supplied the
  readable full text. The recorded DOI identifies that full version.
- The capDL loader's formal-correctness and implementation sections, including
  model-versus-C coverage, well-formedness and inert remaining capabilities.
- Microkit's manual as displayed at version 2.3.0, including static domain
  configuration, initialization, protected calls and notifications. The
  latest URL is moving documentation, not a pinned repository checkout.
- The seL4 proof-assumptions explanation, including hardware management, boot,
  DMA, information channels and configuration-specific binary assurance.
- Heiser's IPC article, including its 2021 correction about passive-server
  queue depth, and Parmer's capability creation/destruction and Composite
  resource-table discussion. These are attributed engineering viewpoints.

Fresh section-level checks of reused works included capDL, the initialization
paper's model/implementation qualification, the scheduling-context paper's
replenishment discussion, seL4 manual 16.0.0's donation-retention caveat and
CuriOS's state-management/recovery limitations. Other reused evidence was
reviewed through existing source notes. This manifest is an exhaustive record
of substantive use, not a claim that all twenty-seven works were freshly read
cover to cover.

No new measurements or exact performance constants are transferred from old
papers. No current seL4 verification claim is inferred for every configuration.
The Microkit protected-call scheduling prose is not used to establish Atom's
donation semantics; the versioned seL4 manual and scheduling-context paper are
the comparative sources for that question. Full specification/code refinement
of any selected implementation still remains to be done.

## Resulting decomposition

- [0. Bootstrap and root-authority handoff](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff/README.md) — 5 service reports. Turn sealed machine facts and an authorized construction description into a private, audited authority graph, then permanently remove bootstrap admission.
- [1. Typed object storage and explicit memory](../20-notes/minimal-privileged-kernel-components/typed-object-storage-and-explicit-memory/README.md) — 5 service reports. Give every privileged object explicit backing, accounting and lifetime, with allocator reuse dependent on completed teardown rather than capability count alone.
- [2. Capability spaces and authority](../20-notes/minimal-privileged-kernel-components/capability-spaces-and-authority/README.md) — 5 service reports. Resolve current typed authority, fund its propagation and preserve effect-bearing lifetime dependencies through logical closure and eventual revocation.
- [3. Protection domains, threads and address spaces](../20-notes/minimal-privileged-kernel-components/protection-domains-threads-and-address-spaces/README.md) — 5 service reports. Make domains exact execution-stop boundaries while keeping accounting, actors, service identity and recovery policy separate.
- [4. Bounded invocation and transport](../20-notes/minimal-privileged-kernel-components/bounded-invocation-and-transport/README.md) — 5 service reports. Keep small protected calls, coalescing notifications and shared-buffer transport finite, explicitly funded and honest about accepted effects.
- [5. Scheduling contexts and temporal authority](../20-notes/minimal-privileged-kernel-components/scheduling-contexts-and-temporal-authority/README.md) — 5 service reports. Conserve execution budget across binding and donation, separately fund causal work and recovery, and avoid confusing availability budgets with timing confidentiality.
- [6. Memory mappings and architecture-resource bindings](../20-notes/minimal-privileged-kernel-components/memory-mappings-and-architecture-resource-bindings/README.md) — 6 service reports. Bind current authority to lower-layer mapping, interrupt and device effects while preserving exact generations and profile-specific completion evidence.
- [7. Fault capture and containment](../20-notes/minimal-privileged-kernel-components/fault-capture-and-containment/README.md) — 4 service reports. Produce bounded fault evidence, route it independently and grant only the narrow repair or termination authority justified by the fault contract.
- [8. Failure boundaries and recovery topology](../20-notes/minimal-privileged-kernel-components/failure-boundaries-and-recovery-topology/README.md) — 5 service reports. Keep recovery authority and resources outside the failed scope, fence replacement managers, and leave application-state recovery policy unprivileged.
- [9. Teardown, revocation and safe reclamation](../20-notes/minimal-privileged-kernel-components/teardown-revocation-and-safe-reclamation/README.md) — 4 service reports. Turn logical closure into a charged, resumable proof of effect completion or exact quarantine custody before the allocator can reuse backing.
- [10. Observability and crash evidence](../20-notes/minimal-privileged-kernel-components/observability-and-crash-evidence/README.md) — 5 service reports. Expose bounded, authorized operational evidence and enrich the lower architecture's single terminal record without adding unsafe crash-time dependencies.

The result is 54 internal-service reports, eleven new directory indexes and six
new source notes. All eleven parent reports gain decomposition links. The
component and notes inventories, minimal-kernel map, home map, inquiry and
related indexes are updated together. The inquiry remains open.

Internal service means a research boundary, not necessarily a separate
privileged process, exported ABI or source file. Reusing a shared lifecycle
object is deliberate; no child report may independently declare a domain
stopped, a device quiescent or memory reusable.

## Cross-service synthesis and claim ledger

| Boundary | Evidence constraint | Proposed consequence | Remaining decisive evidence |
| --- | --- | --- | --- |
| Initialization | capDL construction and policy correctness are different questions | Validate structure and security predicates before private construction; audit and seal authority separately | Manifest adversarial corpus and implementation-refinement argument |
| Resources | Explicit-memory and resource-container work separate backing and attribution | One payer, explicit indirect costs and independently consented charge transfer | Conservation under constructor/transfer/close races |
| Capability products | Existing capability mechanisms do not prove Atom's proposed multi-input algebra | Classify effect-bearing inputs, transient guards and durable detachment consent | Executable authority model and counterexamples for every product schema |
| Domain stop | Stalled-participant algorithms require a legitimate recovery/checkpoint contract | Never acknowledge an abandoned lock-holding activation merely because a CPU halted | Complete checkpoint invariants and SMP membership/stop model |
| Calls and time | Donated time can remain with a non-replying server | Finite passive admission, preauthorized abort scope and drain before return | Reply/cancel/stop/suspend interleavings and exact budget ownership |
| Temporal claims | Budget conservation, response bounds and timing channels are distinct | Separate admission/refill, recovery-reserve and timing-protection studies | Profile-specific timing and confidentiality evidence |
| Device bindings | Translation boundaries and shared-buffer protocols do not prove completion | Immutable requester/profile scope and complete direct-alias fencing | Device-specific drain/reset DAGs and exact completion-token matching |
| Faults | A report, timeout and proven fatal condition have different meanings | Preserve certainty and separate observation, repair and termination rights | Overflow/fallback and one-shot resolver race model |
| Recovery | Old managers can resume and external state can remain affected | Fence at recipient commit; retain immutable operation epochs across takeover | Lease/session/publication model plus external protocol reconciliation |
| Reclamation | Software quiescence covers only one class of effects | Join every applicable class; quarantine only a proven confined set | Exact effect ledger, independent custody and generation-safe release proof |
| Evidence | Lockless snapshots and prepared crash resources have limited assumptions | Protect reader lifetime; enrich the lower layer's one sealed fatal record | Memory-model analysis, interrupted-writer and partial-record tests |

These are cross-source and parent-contract syntheses, not claims that any cited
system implements the combined Atom protocol. At-most-once outcome selection
does not guarantee eventual progress. Fixed-work gate publication does not
bound total descendant traversal, CPU response or device completion.

## Confidence and next research

Confidence is strongest in the negative distinctions: a payer is not a lifetime
owner; closing authority does not complete old effects; stopping execution is
not reclaiming memory; and a recovered service does not imply every external
operation can be retried. The literature offers concrete counterexamples and
mechanisms for these boundaries.

The combined model remains provisional. Prioritize the product-authority
algebra, kernel activation checkpoints, passive-call drainage and lease versus
operation-epoch composition. Next, validate exact device confinement and
diagnostic reader lifetimes. These joins affect multiple components and can
invalidate apparently correct local services.

The [open inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
names the decisive artifacts and links the relevant reports. Numerical capacity
limits, generation widths, performance budgets, platform profiles and compiler
qualification must be selected and justified by their own evidence. No count
or design sketch in this session establishes them.

## Verification and handoff

The first run of `python3 validate_archive.py` passed: 738 completed documents,
49 directories, 7,392 local links and 375 source notes; 25 deep-dive manifests
classify 363 introduced and 452 reused source uses. Twelve source notes retain
their documented pre-manifest provenance. `git diff --check` also passed.

The cross-service review clarified that generic passive abort still requires
the domain-stop contract, that the allocator owns final sanitization after the
reaper's eligibility receipt, and that Microkit's initialization caveat is
cross-domain, not reentrant execution before a domain's own init finishes.
Final archive validation passed again with the same counts after these
clarifications. Tracked diff and untracked-file whitespace checks passed.
The filesystem inventory confirms 54 reports and eleven service READMEs;
all 72 new files are research documents or indexes. The changed-file review
found no implementation, planning, validator or unrelated repository changes.

No implementation test has been run. Validator code and schema are unchanged,
so validator unit tests are not required. Changes remain uncommitted; no
commit, push or pull request was requested for this session.

## Source manifest

### Newly introduced sources

- [capDL Loader](../30-sources/sel4-foundation-2026-capdl-loader-contract.md) — Where does declarative initialization assurance stop?
- [What the Proofs Assume](../30-sources/sel4-foundation-2026-proof-assumptions.md) — What remains outside a kernel correctness or security theorem?
- [Microkit User Manual (v2.3.0)](../30-sources/sel4-foundation-2026-microkit-system-contracts.md) — Which static configuration restrictions simplify protected service composition?
- [How to (and how not to) use seL4 IPC](../30-sources/heiser-2019-sel4-ipc-design.md) — Which communication responsibilities should a minimal privileged IPC mechanism own?
- [Capability-based OS Design](../30-sources/parmer-2016-capability-based-os-design.md) — Must recursive delegation policy reside inside the privileged kernel?
- [Reclaiming memory for lock-free data structures: there has to be a better way](../30-sources/brown-2015-reclaiming-lock-free-memory.md) — Can reclamation tolerate stalled participants without invalidating interrupted operations?

### Reused sources

- [capDL: A language for describing capability-based systems](../30-sources/kuz-et-al-2010-capdl.md) — Declarative capability graphs and the distinction between structure and security policy.
- [Kernel design for isolation and assurance of physical memory](../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) — Explicit backing, indirect metadata and resource-isolation responsibilities.
- [Formally verified system initialisation](../30-sources/boyton-et-al-2013-verified-system-initialisation.md) — Model-level construction assurance and the separate implementation obligation.
- [seL4 reference manual, version 16.0.0](../30-sources/sel4-foundation-2026-reference-manual.md) — Versioned typed-capability, mapping, fault, notification and donation API comparison.
- [Resource containers: A new facility for resource management in server systems](../30-sources/banga-et-al-1999-resource-containers.md) — Resource attribution distinct from thread and protection-domain identity.
- [Hazard pointers: Safe memory reclamation for lock-free objects](../30-sources/michael-2004-hazard-pointers.md) — Precise software-reference retention and bounded participant slots.
- [Read-copy update: Using execution history to solve concurrency problems](../30-sources/mckenney-slingwine-1998-read-copy-update.md) — Logical removal versus software grace periods and physical reuse.
- [Zig 0.16.0 language reference](../30-sources/zig-project-2026-language-reference-0-16.md) — Selected-language facilities do not enforce protected capability linearity or object lifetime.
- [Timing analysis of a protected operating system kernel](../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — Configuration-specific timing analysis and bounded/preemptible lifecycle work.
- [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — Budget objects, passive execution and finite replenishment mechanisms.
- [Vulnerabilities in synchronous IPC designs](../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md) — Adversarial synchronous dependencies and timeout/outcome concerns.
- [CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer](../30-sources/haecki-et-al-2019-cleanq.md) — Shared-buffer ownership transitions and the limits of the data-transfer contract.
- [Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../30-sources/markettos-et-al-2019-thunderclap.md) — Hostile shared DMA protocols, temporal exposure and unsafe reuse counterexamples.
- [Time protection: The missing OS abstraction](../30-sources/ge-et-al-2019-time-protection.md) — Timing-channel protection as a separate contract from CPU-budget enforcement.
- [VFIO - Virtual Function I/O](../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — Requester/trust groups distinct from device handles and reset scopes.
- [Unreliable failure detectors for reliable distributed systems](../30-sources/chandra-toueg-1996-failure-detectors.md) — Mistaken failure suspicion and the need for safe takeover despite old-manager progress.
- [CuriOS: Improving reliability through operating system structure](../30-sources/david-et-al-2008-curios.md) — Recoverable state organization, damaged client state and external-effect limits.
- [Kdump: A kexec-based kernel crash dumping mechanism](../30-sources/goyal-et-al-2005-kdump.md) — Prepared crash resources and remaining platform/survival dependencies.
- [Dynamic instrumentation of production systems](../30-sources/cantrill-et-al-2004-dtrace.md) — Scoped instrumentation as a comparison to a smaller static-probe design.
- [Lockless ring buffer design](../30-sources/rostedt-2009-lockless-ring-buffer-design.md) — Nested-writer publication and explicit buffer-overflow semantics.
- [Sequence counters and sequential locks](../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — Snapshot consistency distinct from storage lifetime and bounded retry.
