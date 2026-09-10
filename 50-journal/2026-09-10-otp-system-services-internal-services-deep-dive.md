---
title: "2026-09-10 OTP-like system-service internal services deep dive"
kind: journal
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
  - research-method
aliases: []
---

# 2026-09-10 OTP-like system-service internal services deep dive

## Observations

All thirteen parent reports in the [component index](../20-notes/otp-like-system-services-components/README.md)
existed without nested decomposition at the start of this session. This pass
adds 55 internal-service studies in thirteen component-named subdirectories,
each with a complete README. It preserves the parent reports and adds direct
navigation rather than replacing their architecture with a different roadmap.

Scope is the full-system unprivileged Layer 4 architecture. This is not a PoC,
QEMU configuration, kernel implementation, phase execution or readiness signoff.
BEAM execution and process-local tracing collection remain in Layer 3;
privileged protection remains below it; Layer 5 owns domain invariants and the
meaning of compensation and migration.

The decomposition follows independently meaningful state, authority and
completion boundaries, not a document quota. Most components separate four
responsibilities; behaviours, releases and operations need five. Logical
services do not imply one new protected process for every note.

| Parent component | Studies | Responsibility split |
| --- | --- | --- |
| [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller/README.md) | 4 | Separate pure desired-state compilation, constrained preparation, public selection and recovery of the controller itself. |
| [Behaviour engines and capability-gated management](../20-notes/otp-like-system-services-components/behaviour-engines-and-capability-gated-management/README.md) | 5 | Distinguish serialized requests, state-machine scheduling, event delivery, cooperative management and callback evolution. |
| [Supervision and recovery policy](../20-notes/otp-like-system-services-components/supervision-and-recovery-policy/README.md) | 4 | Separate evidence classification, restart admission, state recovery and escalation outside the failed subtree. |
| [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration/README.md) | 4 | Separate graph planning, attempt ownership, readiness publication and irreversible shutdown obligations. |
| [Naming, registry, and local discovery](../20-notes/otp-like-system-services-components/naming-registry-and-local-discovery/README.md) | 4 | Separate namespace authority, unique publication, watch continuity and bounded candidate views. |
| [Configuration, workload identity, and secrets](../20-notes/otp-like-system-services-components/configuration-workload-identity-and-secrets/README.md) | 4 | Separate immutable configuration construction, actual adoption, attested caller binding and credential lifetime. |
| [Durable state, transactions, and outcome recovery](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery/README.md) | 4 | Separate the storage fault contract, transactional log, recoverable checkpoint and durable retry-result lifetime. |
| [Device-service policy and management](../20-notes/otp-like-system-services-components/device-service-policy-and-management/README.md) | 4 | Separate inventory/reset scope, client virtualization, issue outcomes and safe replacement. |
| [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services/README.md) | 4 | Separate endpoint authority, bounded parsing, authenticated session lifecycle and application outcomes. |
| [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination/README.md) | 4 | Separate observer health, replay-resistant membership, quorum metadata and effect-sink ownership. |
| [Release, update, rollback, and state migration](../20-notes/otp-like-system-services-components/release-update-rollback-and-state-migration/README.md) | 5 | Separate release provenance, transition compatibility, canary evidence, state migration and irreversible retention decisions. |
| [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance/README.md) | 4 | Separate causal accounting, pressure-based admission, queue-credit conservation and bounded retry/recovery feedback. |
| [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control/README.md) | 5 | Separate lossy telemetry, retained crash facts, persistent alarm state, integrity-protected audit and bounded operator/probe authority. |

## Environment

Repository: `/home/ducky/code/atom-os-research`. The working tree was clean
on `main` before this work. Research uses the archive schema and note, source,
directory, map, inquiry and journal conventions. No implementation repository,
compiler, runtime, simulator, device or network deployment was changed or run.
No commit, push or publication is part of this request.

The deep-research skill was used to preserve a connected multi-document
artifact, explicit evidence limitations and source provenance. The established
corpus format takes precedence over a standalone report export.

## Evidence

### Search and reading method

The research questions are the concrete admission, authority, completion,
failure and retention questions at each internal-service boundary. A proposed
contract is adequate only if it names who owns state, where an effect becomes
accepted or committed, how uncertainty is retained, which bounds hold and what
observation would falsify the design.

Searches covered scientific controller verification, observer-aware failure
detection, software-supply-chain provenance, schema evolution, first-party
canary guidance and queue-backlog engineering. Representative queries included
“Lifeguard SWIM local health awareness”, “Anvil verifying liveness controllers”,
“in-toto farm-to-table guarantees”, and first-party searches for canarying,
backlogs and retry jitter. Existing source records prevented duplicate notes.

Parent reports and the twenty-four reused source records were read for this
decomposition. Fresh primary checks included:

- [Lifeguard v2](https://arxiv.org/pdf/1707.00788v2), particularly the algorithm,
  controlled delay experiments, CPU-stress scenario and their model limits.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/),
  particularly population, duration, attribution, absolute indicators and
  asynchronous work-unit boundaries.
- [Yanacek's official PDF](https://d1.awsstatic.com/builderslibrary/pdfs/avoiding-insurmountable-queue-backlogs.pdf),
  including first-attempt metrics, workload isolation and queue-policy limits.
  The canonical article route redirected to a page with no extracted body;
  the official PDF supplied readable evidence. The 2019 launch announcement
  establishes availability then, not an invented exact publication day.
- [in-toto](https://www.usenix.org/system/files/sec19-torres-arias.pdf),
  especially layouts, functionary thresholds, artifact relationships and
  verification; and [Anvil](https://www.usenix.org/system/files/osdi24-sun-xudong.pdf)
  for eventual-stability and fairness assumptions.
- Current [sys](https://www.erlang.org/doc/apps/stdlib/sys.html) and
  [gen_statem](https://www.erlang.org/doc/apps/stdlib/gen_statem.html) manuals,
  [xDS](https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol.html),
  [etcd v3.5 guarantees](https://etcd.io/docs/v3.5/learning/api_guarantees/),
  [TUF 1.0.36](https://theupdateframework.github.io/specification/v1.0.36/index.html)
  and [QUIC](https://www.rfc-editor.org/rfc/rfc9000.html).
- [sDDF ownership protocol](https://trustworthy.systems/projects/drivers/sddf-design.pdf),
  [F1 schema-version constraints](https://www.vldb.org/pvldb/vol6/p1045-rae.pdf)
  and [Brooker's first-party blog](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/).

This is targeted primary reading plus reuse of evidence-focused archive
records, not a claim to have reread every historical PDF in full or performed
a systematic review of all publications. Search snippets were used to find
sources, not as evidence for detailed protocol claims. Third-party summaries
and unsupported numerical recommendations were not adopted.

### Synthesis and consistency findings

1. A controller must preserve safety and make progress under stated stable-input
   and fairness assumptions. Neither obligation supplies a universal deadline.
2. Recovery needs a bootstrap dependency cut: registry, issuer and durable-state
   outages cannot leave the controller's only replacement authority inside
   itself. The exact independent recovery nucleus remains unqualified.
3. Snapshot/watch loss must be observable outside the queue that overflowed.
   Notification delay and a valid cached name do not establish current authority.
4. xDS NACK can coexist with partial resource acceptance. The existing source
   note's blanket last-valid interpretation is clarified; Atom OS complete-
   snapshot rejection remains a proposed stronger native policy. ACK still
   cannot stand for successful adoption.
5. A fence rejects future stale admission but does not erase operations that
   already crossed an effect boundary. Every takeover must retain their outcomes.
6. Result collection must preserve stale-request rejection. A collected result
   cannot make an old logical request look new. Pending status may advance
   without executing the operation again.
7. The release parent's provenance gap now has a route to the existing in-toto
   study, and canary practice has direct first-party evidence. This does not
   select an attestation implementation or a statistically qualified controller.
8. Identity, configuration, telemetry and audit have different validity,
   authority, retention and outage contracts. Their common use of generations
   does not make them one interchangeable service.

The [topic map](../10-maps/otp-like-system-services.md) adds selective routes
through these boundaries. The [inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
remains open. Parent, component, notes, maps, home, source and journal
navigation is updated together.

### Verification status

The 55 studies contain 110 concrete unexecuted falsifiers. They require
implementation revisions, admitted bounds, trust profiles, injected histories
and raw results before any delivery or correctness claim.

The completed integration checks were:

- `python3 validate_archive.py` — passed: 963 completed documents, 89
  directories, 9981 local links and 386 source notes; 28 deep-dive manifests
  classify 374 introduced and 526 reused source uses, plus twelve historical
  sources introduced outside a manifest.
- `git diff --check` — passed for tracked changes.
- Per-file `git diff --no-index --check -- /dev/null <new-file>` plus
  final-newline checks — passed for all 72 new files.
- Inventory review — thirteen new component directories, 55 unique studies,
  110 unexecuted falsifiers and all 27 cited source records represented in
  exactly one manifest category for this session.
- Change review — 23 existing files updated; no planning, implementation,
  schema or validator changes. The substantive prior-text repairs are the xDS
  NACK qualification and the release report's now-connected evidence gaps.

These are archive checks only. No runtime tests, model checks, benchmarks,
cryptographic audit, interoperability checks or hardware experiments were
executed. All changes remain uncommitted.

## Source manifest

### Newly introduced sources

- [Lifeguard](../30-sources/dadgar-et-al-2018-lifeguard.md) — observer-local slowness, adaptive suspicion and controlled-evaluation limits.
- [Canarying releases](../30-sources/warner-davidovic-2018-canarying-releases.md) — cohort attribution, representative observation and inconclusive rollout decisions.
- [Avoiding insurmountable queue backlogs](../30-sources/yanacek-2019-avoiding-queue-backlogs.md) — backlog age, retry isolation and workload-dependent queue policies.

### Reused sources

- [OTP 29.0.6 system-services documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) — compatibility boundaries for behaviours, supervision, applications, groups, distribution and management.
- [Anvil](../30-sources/sun-et-al-2024-anvil.md) — conditional reconciliation progress and version-sensitive external steps.
- [TOSCA 2.0](../30-sources/oasis-2025-tosca-2.md) — typed service graphs and validation/execution separation.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — immutable generation selection and non-atomic live activation.
- [Capability myths demolished](../30-sources/miller-et-al-2003-capability-myths.md) — attenuation, designation, revocation and independent recovery authority.
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md) — state-separated fine-grained recovery and escalation limits.
- [Exponential backoff and jitter](../30-sources/brooker-2015-exponential-backoff-jitter.md) — randomized retry pacing and workload-dependent stability limits.
- [etcd API guarantees](../30-sources/etcd-project-2026-api-guarantees.md) — publication revisions, watch continuity, stale reads and finite history.
- [xDS protocol](../30-sources/envoy-project-2026-xds-protocol.md) — response correlation, ACK/adoption distinction and partial-resource NACK caveat.
- [SPIFFE Workload API](../30-sources/spiffe-project-2026-workload-api.md) — endpoint-attributed identity, full credential snapshots and export limitations.
- [FSCQ](../30-sources/chen-et-al-2015-fscq.md) — crash conditions, durable commit, checkpoint selection and repeatable recovery.
- [RIFL](../30-sources/lee-et-al-2015-rifl.md) — atomic outcome records, retry rendezvous and safe stale-client rejection.
- [sDDF design](../30-sources/heiser-et-al-2026-sddf-design.md) — driver/virtualizer separation, bounded queues and buffer custody.
- [QUIC RFC 9000](../30-sources/iyengar-thomson-2021-quic.md) — transport flow-control scopes, path migration and connection lifecycle.
- [Raft](../30-sources/ongaro-ousterhout-2014-raft.md) — crash-fault metadata ordering, quorum assumptions and safe reconfiguration.
- [Chubby](../30-sources/burrows-2006-chubby.md) — lease uncertainty, generation-sensitive handles and resource-side fences.
- [TUF specification 1.0.36](../30-sources/tuf-project-2026-specification-1-0-36.md) — bounded metadata verification and the separation of delivery from activation.
- [in-toto](../30-sources/torres-arias-et-al-2019-in-toto.md) — build-step provenance complementary to authenticated release bytes.
- [Online schema change in F1](../30-sources/rae-et-al-2013-online-schema-change-f1.md) — compatible intermediate schemas and limitations of endpoint-only compatibility.
- [SEDA](../30-sources/welsh-et-al-2001-seda.md) — explicit queues, stage costs and negative evidence against automatic latency guarantees.
- [DAGOR](../30-sources/zhou-et-al-2018-dagor.md) — local pressure and upstream admission feedback with policy-dependent fairness.
- [Secure audit logs](../30-sources/schneier-kelsey-1999-secure-audit-logs.md) — forward integrity, witness progress and truth/completeness limitations.
- [Dapper](../30-sources/sigelman-et-al-2010-dapper.md) — causal correlation, privacy-conscious sampling and incomplete trace coverage.
- [DTrace](../30-sources/cantrill-et-al-2004-dtrace.md) — constrained instrumentation and its remaining timing/authority obligations.

## Threads

The [component inventory](../20-notes/otp-like-system-services-components/README.md)
is the complete local route. The [full-system layer](../20-notes/otp-like-system-services-layer.md)
retains the integrated architecture and prior evidence. No historical source
is reclassified as newly introduced merely because it informed this session.

## Follow-ups

- Model controller recovery with simultaneous loss of normal registry and
  issuer service, including the durable-store bootstrap dependency.
- Specify and test effect admission versus fencing at each actual sink.
- Select concrete storage, secure-channel, attestation and consensus profiles;
  literature alone does not qualify their implementations.
- Evaluate observer health, admission feedback and recovery together under
  asymmetric delay, saturation and repeated failures.
- Select canary statistical decision rules, cohort independence and minimum
  evidence requirements; test Inconclusive and shared-dependency failure.
- Qualify retry-result collection, witness rollback detection and independent
  recovery capacity before claiming bounded safe long-term operation.
