---
title: "Managed actor runtime internal-service research"
kind: journal
created: "2026-09-09"
tags:
  - actor-model
  - beam
  - managed-runtime
  - research-session
  - system-architecture
aliases: []
---

# Managed actor runtime internal-service research

## Context

The user requested the same deeper component decomposition already used for
the hardware and minimal privileged-kernel layers. Inventory found thirteen
managed-runtime parent reports and no internal-service subdirectories.
This session adds 56 developing service studies in thirteen matching directories,
each with a complete README, parent backlink, cross-component connections,
source basis and unexecuted verification obligations.

This is research into the full system architecture. No proof-of-concept plan,
boot configuration, implementation milestone or selected kernel language changes.
Ordinary actors and automatic process-local tracing collection remain outside
the privileged kernel. A compromised loader, collector, execution engine or
in-process NIF can compromise the runtime domain; actor isolation is conditional
on that trusted implementation.

## Question and operational standard

Can each runtime component be divided into state owners whose admission,
visibility, completion, failure and reclamation rules compose without changing
the declared BEAM/OTP contract?

A useful decomposition must identify who owns every intermediate object, where
an observation becomes visible, what survives cancellation or actor death, what
is charged, what authority is required, and which experiment could falsify the
proposal. Writing these contracts does not demonstrate their correctness.

## Research method and reading depth

Read the existing thirteen parent contracts, their directory inventory, relevant
source records, archive conventions and document templates. Reuse existing
bibliographic records rather than introducing duplicate notes for the same work.
The source manifest below is exhaustive for substantive source use this session;
the map is intentionally selective.

Web searches included Erlang process-local collection and heap architectures,
actor scheduling/benchmark literature, actor replay and systematic testing,
parallel signal ingress, persistent terms, decentralized ETS counters, yielding
native helpers and thread progress. Primary papers, official documentation and
first-party engineering blogs supplied evidence; secondary search hits were
discovery leads, not support for detailed claims.

Fresh primary reading included:

- Sagonas/Wilhelmsson's author-hosted paper: architecture context and
  work/time-based incremental collector progress sections. Its shared-message
  collector is not silently substituted for the proposed private-heap baseline.
- Barghi/Karsten's preprint: placement, victim selection, experimental setup
  and affinity limitations. Hardware and CAF-specific observations are comparative.
- Concuerror's paper: spawn/BIF/receive instrumentation and bounded exploration.
- Aumayr and colleagues' paper: external nondeterministic input and thread-local
  trace ordering. The attempted HTML preprint failed; the PDF was accessible.
- PARTISAN's paper: channel/topology and ordering/failure discussion.
- Official message-passing and parallel-signal articles, plus the four new
  documentation/blog records below.

Other reused works were consumed through the archive's existing evidence-focused
source notes; their prior methods and limits were retained. This is not a claim
to have repeated every earlier full-text review, re-audited the complete OTP
source tree, or reproduced any published benchmark. Savina search results were
useful discovery context but no new Savina paper claim or source record was
introduced without a sufficient primary reading.

The public-contract reference remains OTP 29.0.6 as qualified by the parent
studies; the separate static source audit remains OTP 29.0.5 at
5cf5f9725452f4e1b6a4890e8ff0305d76924b98. The newly consulted yielding,
thread-progress and erlang module pages rendered OTP 29.0.6 on access; some
search results still displayed older patch labels. Moving documentation is not
an implicit upgrade of either baseline. No claim of checking every patch-specific
timer, ETS or purge implementation is made in this session.

## Resulting decomposition

Counts follow distinct state and lifecycle responsibilities, not a fixed quota.
Parent numbering and previously recorded research remain intact.

| Parent component | New service studies | Internal-service index |
| --- | ---: | --- |
| 0. Runtime-domain bootstrap and kernel adapter | 4 | [Index](../20-notes/managed-actor-runtime-components/runtime-domain-bootstrap-and-kernel-adapter/README.md) |
| 1. Compatibility manifest, BEAM loader and verifier | 4 | [Index](../20-notes/managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier/README.md) |
| 2. Actor identity, lifecycle and process state | 4 | [Index](../20-notes/managed-actor-runtime-components/actor-identity-lifecycle-and-process-state/README.md) |
| 3. Terms, private heaps, shared binaries and tracing collection | 5 | [Index](../20-notes/managed-actor-runtime-components/terms-private-heaps-shared-binaries-and-tracing-collection/README.md) |
| 4. Signal ingress, mailboxes and selective receive | 4 | [Index](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive/README.md) |
| 5. Reduction scheduler and kernel scheduling contexts | 4 | [Index](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts/README.md) |
| 6. Timers, events and asynchronous I/O integration | 4 | [Index](../20-notes/managed-actor-runtime-components/timers-events-and-asynchronous-io-integration/README.md) |
| 7. Code execution, safe points and version publication | 6 | [Index](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication/README.md) |
| 8. Native work, ports and drivers | 4 | [Index](../20-notes/managed-actor-runtime-components/native-work-ports-and-drivers/README.md) |
| 9. Distribution gateway and remote actor semantics | 4 | [Index](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics/README.md) |
| 10. Failure translation and the OTP boundary | 4 | [Index](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary/README.md) |
| 11. Resource accounting and overload control | 5 | [Index](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control/README.md) |
| 12. Observability, deterministic testing and crash evidence | 4 | [Index](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence/README.md) |

## Cross-component findings

### Visibility and retention need separate owners

A published actor cannot disappear through spawn rollback. An admitted signal
belongs to destination-generation cleanup even if its sender dies. Logical code
purge is distinct from physical code/literal retention. An I/O request can remain
charged after its caller stops waiting. These are proposed composition rules,
not one universal transaction implementation.

### Compatibility requires precise exceptions

The reports preserve the parent distinctions between signal order and priority
mailbox placement; alias deactivation and already inserted replies; timer creator
and PID/name destination; external node creation and transport session; and
direct old-code execution versus fun-only/literal-only holders. Compatible
ordinary sends retain their existing result shape. Stronger receipts, refusal
APIs or restricted overload behavior require explicitly separate profiles.

### Native and shared work are not hidden actor-local work

NIF classification is per function and scheduled segment, not simply per module.
Dirty execution offers no memory protection. ETS atomic bulk operations may be
internally sliced or helped without exposing partial effects. Persistent terms
and counter snapshots add runtime-wide progress and retention obligations despite
ordinary private-heap collection. Their exact inclusion remains a compatibility
catalog decision, not a claim that every optional facility has been selected.

### Progress has several meanings

Reduction charging is not elapsed CPU time; kernel preemption is not a collector
safe point; a software grace period is not instruction-fetch or device
quiescence. Bounded continuation work requires preserved roots, ownership,
destruction and reserve. None of the literature measurements establishes a hard
latency guarantee for this system.

## Consistency repairs to parent prose

The code-publication parent's short W^X paragraph is aligned with its existing
detailed state graph: close and drain writers, establish data visibility, then
complete lower executable publication before exposing runtime entry points.
This removes prose that could be read as performing final instruction
synchronization before revoking writable mappings.

Failure translation now explicitly treats postpublication loss as potentially
indeterminate even without an acceptance acknowledgement. A lost acknowledgement
does not prove the service never accepted or executed the request. Related
inquiry wording is aligned without changing compatible Erlang send results.

## Decisions and evidence still missing

| Open decision | Evidence that would support resolution |
| --- | --- |
| Exact compatibility and hostile-module profile | Versioned feature catalog, malformed-input corpus and differential language histories |
| Collector pause/progress strategy | Root-completeness tests, live-ratio/reserve sweeps and worst observed safe-point intervals |
| Queue and activation ownership | Executable models of wake, stripe cutover, exit, pin and migration races |
| Long atomic shared operations | Histories proving atomic visibility while yielding/helping and actor cancellation interleave |
| Native and distributed effect boundaries | Fault injection before/after publication, acknowledgement, effect and terminal release |
| Hard accounting versus scalable telemetry | Concurrent reservation conservation and coherent snapshot/reconciliation tests |
| Code retirement composition | Direct/fun/literal/native-reference purge matrix plus lower publication/reclamation evidence |
| Evidence and replay scope | Divergence tests, recorded external inputs, explicit unsupported operations and corrupted-dump parsing |

These are next architecture experiments, not newly authorized implementation
phases. The linked inquiry remains open.

## Verification and local evidence

This session creates Markdown research artifacts only. No runtime executable,
collector, JIT, queue, timer service, gateway or native-service experiment was
run. Performance numbers were not newly measured. No compiler/runtime language
selection was inferred from the comparative source languages.

Verification performed from `/home/ducky/code/atom-os-research`:

- `python3 validate_archive.py`: the initial pass reported thirteen new README
  title/H1 mismatches. Corrected those metadata titles, then reran successfully:
  812 completed documents, 62 directories, 8,278 local links and 379 source notes;
  26 deep-dive manifests classify 367 introduced and 472 reused source uses,
  with twelve pre-manifest source notes.
- `git diff --check`: passed for tracked changes.
- Per-file `git diff --no-index --check` against an empty file, plus final-newline
  checks: all 74 new files had no whitespace defects. The first loop stopped
  on Git's normal difference exit status of 1; the corrected check distinguished
  that status from diagnostic output and errors and covered every new file.
- Reviewed generated service content, parent/navigation diffs and source-manifest
  coverage; no existing document was deleted. New external source URLs were
  opened and read at their primary publishers.

The change contains 56 studies, thirteen new directory READMEs, four source
notes and this journal; 21 existing files connect and clarify the research.
Validation code and schema are unchanged, so their unit suite was not rerun.
These checks establish archive structure, not runtime correctness. Changes
remain uncommitted on main; no push or pull request was requested this session.

## Source manifest

### Newly introduced sources

- [Automatic Yielding of C Code](../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md) — Which obligations survive transformation of a long native helper into a resumable routine?
- [Thread Progress](../30-sources/erlang-otp-team-2026-thread-progress-contracts.md) — What does a runtime grace-period observation actually establish?
- [Decentralized ETS counters](../30-sources/winblad-2021-decentralized-ets-counters.md) — When does distributing runtime counters improve performance, and what does observation cost?
- [Clever use of persistent_term](../30-sources/larsson-2019-persistent-term.md) — Where does read-mostly global term storage move its cost?

### Reused sources

- [OTP 29.0.6 managed-runtime documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) — versioned actor, timer, code, table and native compatibility reference.
- [Pinned OTP 29.0.5 source audit](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) — host dependency and runtime/execution boundary evidence; prior pin retained.
- [Sagonas and Wilhelmsson: memory management](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md) — private/shared heap alternatives and incremental progress limits.
- [Orca: collector and type-system co-design](../30-sources/clebsch-et-al-2017-orca.md) — stronger type assumptions behind zero-copy actor sharing.
- [Hazard pointers](../30-sources/michael-2004-hazard-pointers.md) — lookup pinning and removal-versus-reclamation distinction.
- [Proof-carrying code](../30-sources/necula-1997-proof-carrying-code.md) — policy-scoped verification and trusted helper boundary.
- [Parallel signal sending](../30-sources/winblad-2021-parallel-signal-sending.md) — sender-striped ingress and contention-based adaptation.
- [A few notes on message passing](../30-sources/hogberg-2021-message-passing.md) — signal/message separation and selective-receive cost.
- [Scheduling-context capabilities](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — kernel CPU authority beneath runtime scheduling.
- [Locality-aware actor scheduling](../30-sources/barghi-karsten-2018-locality-aware-actor-scheduling.md) — workload-dependent placement and affinity contention.
- [Hashed and hierarchical timing wheels](../30-sources/varghese-lauck-1987-timing-wheels.md) — wheel geometry, cascade and burst-work tradeoffs.
- [The Road to the JIT](../30-sources/gustavsson-2020-road-to-the-jit.md) — execution optimization constrained by whole-runtime behavior.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) — explicit buffer ownership and its surrounding protocol limits.
- [PARTISAN](../30-sources/meiklejohn-et-al-2019-partisan.md) — replaceable topology, channels and ordering scope.
- [Unreliable failure detectors](../30-sources/chandra-toueg-1996-failure-detectors.md) — suspicion versus fact and post-loss uncertainty.
- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md) — external recovery authority and state/retry assumptions.
- [Resource containers](../30-sources/banga-et-al-1999-resource-containers.md) — causal hierarchical attribution across deferred work.
- [SEDA](../30-sources/welsh-et-al-2001-seda.md) — overload boundaries and negative evidence against automatic latency guarantees.
- [Actor record and replay](../30-sources/aumayr-et-al-2018-actor-record-replay.md) — external inputs, high-level choices and replay limits.
- [Concuerror](../30-sources/christakis-et-al-2013-concuerror.md) — systematic actor interleavings and instrumentation scope.

## Follow-ups

- [Component index](../20-notes/managed-actor-runtime-components/README.md).
- [Selective runtime map](../10-maps/managed-actor-runtime.md).
- [Open runtime inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md).
