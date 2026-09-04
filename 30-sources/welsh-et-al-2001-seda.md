---
title: "SEDA: An architecture for well-conditioned, scalable Internet services"
kind: source
created: "2026-09-03"
authors:
  - "Matt Welsh"
  - "David Culler"
  - "Eric Brewer"
published: 2001
citation_key: "welsh-et-al-2001-seda"
container: "Proceedings of the 18th ACM Symposium on Operating Systems Principles"
edition: "SOSP '01, 230–243"
isbn: "1-58113-389-8"
doi: "10.1145/502034.502057"
url: "https://people.eecs.berkeley.edu/~brewer/papers/SEDA-sosp.pdf"
accessed: "2026-09-03"
tags:
  - admission-control
  - overload
  - system-services
aliases:
  - "SEDA"
---

# SEDA: An architecture for well-conditioned, scalable Internet services

## Reference

Matt Welsh, David Culler, and Eric Brewer. “[SEDA: An Architecture for
Well-Conditioned, Scalable Internet
Services](https://people.eecs.berkeley.edu/~brewer/papers/SEDA-sosp.pdf).”
*SOSP '01*, pages 230–243. DOI
[10.1145/502034.502057](https://doi.org/10.1145/502034.502057). An
[alternate open copy](https://www.cs.princeton.edu/courses/archive/fall05/cos518/papers/seda.pdf)
was used when the author-hosted PDF timed out.

## Research question or contribution

Can explicit queues, staged event handling, admission policy, and dynamic
resource control keep highly concurrent services responsive and predictable
when offered load exceeds capacity?

## Method

SEDA decomposes services into event-driven stages with incoming queues,
handlers, bounded thread pools, and controllers. The paper evaluates dynamic
thread-pool sizing, event batching, and load conditioning in a Java HTTP server
and a Gnutella packet router under changing load.

## Findings

- Making queues and stage boundaries explicit exposes backlog, resource use,
  and semantic points where a service can block, reject, shed, reorder, batch,
  or degrade work.
- Finite queues allow overload to be handled before resources are
  overcommitted. Rejection still requires application-specific policy; the
  framework cannot decide which work is safe to discard.
- Stage isolation and independent control improve modularity and observability,
  but each queue boundary may add latency and dataflow complexity.
- In the two evaluated services, the design retained throughput and degraded
  more gracefully across large load changes than the compared implementations.
- The HTTP response-time controller did not meet its five-second target: it
  rejected 98 percent of requests, yet only 90 percent of accepted requests
  completed within 11.8 seconds and the maximum was 22.1 seconds. Bursts while
  the queue threshold was high prevented a hard latency guarantee.
- Explicit queues were not automatically bounded. The original Gnutella router
  exhausted memory after per-socket output queues grew without bound; the
  authors corrected this by imposing a queue threshold and closing connections
  that exceeded it.

## Relevance

OTP supervision needs a sibling resource-governance policy rather than using
crash and restart as the only overload response. Atom OS services should expose
finite queues, credits, queue age, admission outcomes, and explicit degraded
modes while the kernel and runtime enforce underlying CPU and memory limits.

## Limits

The evidence is from two early-2000s Internet services, Java, and specific
operating-system I/O facilities. It does not prove one queue per actor, a
universal controller, hard real-time bounds, fair shedding, or suitability for
irreversible operations. Dynamic feedback complements but does not replace
hard resource containment.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
