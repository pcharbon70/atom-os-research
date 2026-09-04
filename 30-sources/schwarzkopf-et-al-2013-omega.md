---
title: "Omega: Flexible, scalable schedulers for large compute clusters"
kind: source
created: "2026-09-04"
authors:
  - "Malte Schwarzkopf"
  - "Andy Konwinski"
  - "Michael Abd-El-Malek"
  - "John Wilkes"
published: 2013
citation_key: "schwarzkopf-et-al-2013-omega"
container: "Proceedings of the Eighth European Conference on Computer Systems"
edition: "EuroSys '13, pages 351–364"
isbn: "978-1-4503-1994-2"
doi: "10.1145/2465351.2465386"
url: "https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/"
accessed: "2026-09-04"
tags:
  - cluster-management
  - concurrency-control
  - controllers
  - orchestration
  - scheduling
  - system-services
aliases:
  - "Omega scheduler paper"
---

# Omega: Flexible, scalable schedulers for large compute clusters

## Reference

Malte Schwarzkopf, Andy Konwinski, Michael Abd-El-Malek, and John Wilkes.
“[Omega: Flexible, Scalable Schedulers for Large Compute
Clusters](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/).”
*Proceedings of the Eighth European Conference on Computer Systems (EuroSys
'13)*, pages 351–364, 2013. DOI
[10.1145/2465351.2465386](https://doi.org/10.1145/2465351.2465386).

## Research question or contribution

Omega asks whether a cluster can avoid both a single monolithic scheduler and
independent schedulers that hide their decisions from one another. It proposes
multiple specialized schedulers operating in parallel over a shared cell-state
representation. Each scheduler plans against a snapshot and commits changes
with optimistic concurrency control; conflicting decisions are rejected and
retried against newer state.

## Method

The authors describe Omega's shared-state architecture, compare it with
two-level and monolithic schedulers, analyze the frequency and cost of
scheduling interference, and evaluate the design with production-derived
Google workloads. The paper is evidence about control-plane decomposition and
concurrent desired-state decisions at datacenter scale. It is not evidence
about kernel privilege, embedded boot, persistent service effects, or actor
compatibility.

## Findings

- A monolithic controller can make globally informed decisions but becomes a
  development and scaling bottleneck as unrelated policies accumulate.
  Partitioning policy among specialized schedulers permits independent
  evolution without forcing those schedulers to operate on mutually
  inconsistent private worlds.
- Schedulers read a shared state snapshot, calculate a placement, and submit a
  transaction containing the state versions on which the calculation relied.
  The cell-state service accepts nonconflicting changes and rejects stale or
  conflicting ones. Rejection is therefore an ordinary concurrency outcome,
  not proof that the scheduler or workload failed.
- Optimistic concurrency works best when scheduling decisions touch a small
  part of state and conflicts are uncommon or cheap to retry. Workloads that
  make broad, tightly coupled placements can conflict more often and may need
  policy-specific mitigation.
- Shared state makes cross-policy interference visible, but it does not remove
  the need to decide which fields are authoritative, who may mutate them, how
  transactions survive control-plane crashes, or what happens after a task has
  produced an external effect.
- The design separates the mechanism that serializes accepted state changes
  from policy modules that choose changes. This allows a smaller authoritative
  core while retaining multiple higher-level reconcilers.

## Relevance

Omega supports an Atom OS service layer made from several capability-confined
controllers rather than one all-powerful application manager. A small manifest
authority can own immutable desired state and publication revisions while
specialized lifecycle, resource, update, device, and network controllers plan
from snapshots. Their writes should name the input revisions and be accepted
only if the relevant objects still match; conflict then returns a typed
`StalePlan` outcome for recomputation.

The inference is deliberately narrower than Omega. Atom OS should not expose
one writable global object store to every service. Each controller should
receive attenuated mutation capabilities for a typed subset of state, and
publication of a prepared service generation should remain one explicit
linearization point. A controller must not retry an operation after a stale
plan if the first attempt may already have crossed an external effect boundary;
that case needs an operation ledger and reconciliation.

## Limits

Omega's evaluation uses large Google cluster workloads, not embedded systems
or actor-runtime services. Optimistic retry can starve under adversarial or
highly contended changes, and a shared cell state is a correlated dependency.
The paper does not give Byzantine security, capability confinement, bounded
recovery time, a crash-consistency proof for the state service, or a protocol
for controller self-recovery. It therefore motivates controller decomposition
and version-checked commits, not wholesale adoption of its storage or
scheduling implementation.

## Derived work

- [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md)
- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)
- [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
