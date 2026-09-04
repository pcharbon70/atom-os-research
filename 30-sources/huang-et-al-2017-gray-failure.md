---
title: "Gray failure: The Achilles' heel of cloud-scale systems"
kind: source
created: "2026-09-04"
authors:
  - "Peng Huang"
  - "Chuanxiong Guo"
  - "Lidong Zhou"
  - "Jacob R. Lorch"
  - "Yingnong Dang"
  - "Murali Chintalapati"
  - "Randolph Yao"
published: "2017-05-08"
citation_key: "huang-et-al-2017-gray-failure"
container: "Proceedings of the 16th Workshop on Hot Topics in Operating Systems"
edition: "HotOS '17, six pages"
isbn: "978-1-4503-5068-6"
doi: "10.1145/3102980.3103005"
url: "https://doi.org/10.1145/3102980.3103005"
accessed: "2026-09-04"
tags:
  - failure-detection
  - fault-tolerance
  - observability
  - operations
aliases:
  - "Gray failure paper"
---

# Gray failure: The Achilles' heel of cloud-scale systems

## Reference

Peng Huang, Chuanxiong Guo, Lidong Zhou, Jacob R. Lorch, Yingnong Dang,
Murali Chintalapati, and Randolph Yao. “[Gray Failure: The Achilles' Heel of
Cloud-Scale
Systems](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/paper-1.pdf).”
*Proceedings of the 16th Workshop on Hot Topics in Operating Systems (HotOS
'17)*, 2017. DOI
[10.1145/3102980.3103005](https://doi.org/10.1145/3102980.3103005).

## Research question or contribution

The paper characterizes failures that are neither cleanly correct nor
fail-stop: degraded, intermittent, partial, or path-specific behavior that
hurts clients while conventional health detectors still report success. Its
central concept is differential observability—different components perceive
the same underlying condition differently.

## Method

The authors synthesize operational experience from cloud-scale production
systems, present representative failure patterns, explain why redundancy,
heartbeat detection, and reboot can fail or amplify harm, and outline research
directions. It is a six-page HotOS position and experience paper rather than a
controlled evaluation of one detector or recovery algorithm.

## Findings

- A request-serving path may be stalled while a lightweight heartbeat path
  remains responsive. Treating the heartbeat as a complete health oracle can
  keep bad instances in service or trigger recovery against the wrong target.
- Gray failures include severe slowdown, selective packet loss, flaky I/O,
  memory pressure, and nonfatal exceptions. Redundancy can hide these from the
  entity responsible for replacement while clients accumulate damage.
- Failure is relational: the affected client, peer, local monitor, and
  controller can each observe different evidence. Detection should compare
  perspectives and service-path outcomes rather than collapse them prematurely
  into one boolean.
- Recovery based on an oversimplified fail-stop model can aggravate failure,
  for example by sending more work to a degraded dependency or repeatedly
  restarting healthy replicas.
- Byzantine replication can mask some arbitrary behavior, but cost, complexity,
  and slow-operation behavior prevent treating it as a universal answer.

## Relevance

Atom OS supervisors, device managers, network services, membership protocols,
and operators should carry typed evidence with observer, path, time,
generation, and confidence. A readiness probe, actor monitor, watchdog, client
timeout, device completion error, and peer suspicion are separate observations.
Policy can correlate them and quarantine a suspect generation, but one weak
signal must not revoke authority or declare irreversible failure by itself.

This supports multi-perspective health checks and a diagnostic state between
healthy and dead. A service may stop admitting new work, preserve existing
outcomes, run a bounded self-test on the affected path, or shift traffic before
restart. Recovery decisions must themselves be rate-limited and observable so
the control loop cannot create a restart or failover storm.

## Limits

The paper gives no complete taxonomy, detector implementation, formal model,
or quantitative guarantee. Its evidence comes from cloud systems and may not
transfer directly to constrained hardware. Differential observation can also
be produced by overload, malicious reporting, or incompatible versions, not
only component failure. Atom OS must define evidence authenticity, collection
cost, decision thresholds, and false-positive consequences for each component
and then test them under target-specific fault injection.

## Derived work

- [Supervision and recovery policy](../20-notes/otp-like-system-services-components/supervision-and-recovery-policy.md)
- [Device-service policy and management](../20-notes/otp-like-system-services-components/device-service-policy-and-management.md)
- [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md)
- [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)
