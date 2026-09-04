---
title: "Large-scale cluster management at Google with Borg"
kind: source
created: "2026-09-03"
authors:
  - "Abhishek Verma"
  - "Luis Pedrosa"
  - "Madhukar R. Korupolu"
  - "David Oppenheimer"
  - "Eric Tune"
  - "John Wilkes"
published: "2015-04-21"
citation_key: "verma-et-al-2015-borg"
container: "Proceedings of the Tenth European Conference on Computer Systems"
edition: "EuroSys '15, Article 18, 18:1–18:17"
isbn: "978-1-4503-3238-5"
doi: "10.1145/2741948.2741964"
url: "https://doi.org/10.1145/2741948.2741964"
accessed: "2026-09-03"
tags:
  - admission-control
  - cluster-management
  - desired-state
  - fault-tolerance
  - orchestration
  - resource-governance
  - system-services
aliases:
  - "Borg paper"
---

# Large-scale cluster management at Google with Borg

## Reference

Abhishek Verma, Luis Pedrosa, Madhukar R. Korupolu, David Oppenheimer,
Eric Tune, and John Wilkes. “[Large-scale Cluster Management at Google with
Borg](https://research.google.com/pubs/archive/43438.pdf).” *Proceedings of
the Tenth European Conference on Computer Systems (EuroSys '15)*, Article 18,
pages 18:1–18:17, Bordeaux, France, April 21–24, 2015. DOI
[10.1145/2741948.2741964](https://doi.org/10.1145/2741948.2741964).

## Research question or contribution

The paper asks how one cluster manager can admit, place, start, monitor,
restart, update, and account for heterogeneous production services and batch
jobs across cells containing tens of thousands of machines. It documents
Borg's architecture and policy choices and extracts lessons from more than a
decade of production operation at Google.

## Method

The source combines an architecture and mechanism description with production
measurements, retrospective operational experience, and policy experiments.
The quantitative evaluation uses checkpoints from fifteen production cells
and the high-fidelity Fauxmaster simulator to compare packing policies while
retaining actual constraints, limits, reservations, and usage. It also reports
a week-scale live experiment that changed resource-reclamation parameters.
The reported workload and eviction measurements principally date from
2013–2014; the system account is therefore evidence about the Borg generation
described in 2015, not a specification of current Google infrastructure.

## Findings

- A Borg job is a declarative desired-state object containing tasks,
  constraints, resource requests, priority, ownership, and update policy.
  Mutating operations are designed to be idempotent so a client can safely
  resubmit a request whose outcome it did not observe.
- A cell has one logical control authority, but the Borgmaster is replicated
  five ways and records its state in a Paxos-based store. One elected replica
  serializes state changes. Scheduling is a separate process operating from a
  cached state copy; the master rejects assignments made stale by concurrent
  changes and lets the scheduler reconsider them.
- Each machine runs a Borglet agent that starts and stops tasks, manages local
  resource controls, reports complete observed state, and continues existing
  tasks during loss of contact with the master. The master rate-limits
  replacement after unreachable machines because it cannot immediately tell a
  large machine failure from a network partition. If the old machine returns,
  duplicate tasks that were rescheduled are killed.
- Availability is shared responsibility. Borg restarts and reschedules tasks,
  spreads replicas over failure domains, and limits simultaneous disruptions,
  but applications are expected to replicate, store durable state elsewhere,
  and checkpoint when appropriate. Running tasks survive a control-plane
  outage, while submission, update, and replacement of failed tasks do not.
- Priority and quota are distinct. Quota is an admission-control entitlement;
  priority determines relative access to resources and preemption. This keeps
  overload policy explicit rather than treating all accepted work as equally
  recoverable.
- Borg distinguishes compressible resources, such as CPU and I/O bandwidth,
  which can be throttled, from non-compressible resources, such as memory and
  disk space, whose exhaustion can require termination. It reclaims predicted
  slack for lower-quality work and protects production work from reliance on
  reclaimed capacity.
- Stable service names, health checks, event history, logs, resource metrics,
  “why pending?” explanations, snapshots, simulation, and drill-down views are
  part of the operating model rather than optional diagnostics. The authors
  identify introspection as necessary for users to diagnose a system at this
  scale.
- The authors' retrospective cautions that a fixed job abstraction became too
  restrictive and that Borg's roughly 230 configuration parameters burdened
  casual users and constrained API evolution. They also report that separating
  the scheduler, admission control, autoscaling, workflow, archival, and UI
  services from a smaller authoritative core improved scalability and
  maintainability.

## Relevance

Borg supports an OTP-like system-services layer organized as unprivileged,
desired-state reconcilers above a small actor runtime. Durable intent and
observed state should be separate, reconciliation operations should be
idempotent, and control-plane failure should not revoke already granted
resources merely because the controller is unavailable. A replicated state
authority can serialize intent while specialized schedulers and node-local
agents work from snapshots and report outcomes.

The resource evidence also argues that supervision alone is insufficient.
Admission limits, quotas, throttling, preemption, failure-domain placement,
bounded disruption, and explicit degraded service are policy services that
must cooperate with runtime and kernel enforcement. Borg's use of the word
“kernel” for its distributed-system core is architectural metaphor, not
evidence that these policies belong in a privileged operating-system kernel.

## Limits

Borg was proprietary and the paper cannot make its implementation or full
failure semantics independently reproducible. Much of the evaluation uses a
high-fidelity simulator rather than interventions on live production cells;
the one reported live reclamation experiment is narrow. Results reflect
Google's workloads, hardware, internal storage and naming services, and 2015
software. The paper reports practical availability and utilization, not a
formal safety proof, Byzantine tolerance, hard real-time bounds, or exactly-once
task execution. In particular, rescheduling can create a duplicate interval,
so an external side effect still needs idempotency or fencing. Its contemporary
chroot and cgroup isolation account must not be treated as a sufficient modern
security boundary.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [OTP-like system-services deep-dive journal](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
