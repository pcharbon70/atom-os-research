---
title: "Dapper, a large-scale distributed systems tracing infrastructure"
kind: source
created: "2026-09-03"
authors:
  - "Benjamin H. Sigelman"
  - "Luiz André Barroso"
  - "Mike Burrows"
  - "Pat Stephenson"
  - "Manoj Plakal"
  - "Donald Beaver"
  - "Saul Jaspan"
  - "Chandan Shanbhag"
published: 2010
citation_key: "sigelman-et-al-2010-dapper"
container: "Google Technical Report dapper-2010-1"
edition: null
isbn: null
doi: null
url: "https://research.google.com/archive/papers/dapper-2010-1.pdf"
accessed: "2026-09-03"
tags:
  - distributed-systems
  - distributed-tracing
  - observability
  - sampling
aliases:
  - "Dapper"
---

# Dapper, a large-scale distributed systems tracing infrastructure

## Reference

Benjamin H. Sigelman, Luiz André Barroso, Mike Burrows, Pat Stephenson, Manoj
Plakal, Donald Beaver, Saul Jaspan, and Chandan Shanbhag. “Dapper, a
Large-Scale Distributed Systems Tracing Infrastructure.” Google Technical
Report dapper-2010-1, April 2010.
[Official publication record](https://research.google.com/pubs/pub36356.html).
[Primary report](https://research.google.com/archive/papers/dapper-2010-1.pdf).

## Research question or contribution

Can one tracing substrate reconstruct causally related work across a very large
distributed system while imposing low application changes and sufficiently low
production overhead? Dapper combines trace and span identifiers, parent-child
relationships, timestamped annotations, common-library instrumentation, local
collection, sampling, and centralized query facilities.

## Method

The report is a retrospective engineering study after more than two years of
production operation at Google. It describes Dapper's data model and
deployment, reports coverage and usage, benchmarks span creation and collection
costs, measures the effect of several sampling rates on a web-search cluster,
and presents diagnostic use cases. It is neither a controlled comparison of
all tracing designs nor a proof of complete causal capture.

## Findings

- A trace identifier shared by all spans, plus each span's identifier and
  parent identifier, reconstructs a tree of RPC and other causally related
  operations.
- Instrumenting common RPC, threading, and control-flow libraries made tracing
  effectively transparent for most of Google's comparatively homogeneous
  production environment. Non-standard control flow and uninstrumented
  transports still required manual propagation or remained invisible.
- Sampling is necessary at high request rates. In the reported web-search
  experiment, latency and throughput changes below a 1-in-16 sampling rate fell
  within experimental error, while a 1-in-1024 rate still supported many
  high-volume analyses.
- The production collector consumed less than 0.3% of one CPU core under the
  reported load test, and collected trace data accounted for less than 0.01%
  of production network traffic. These are measurements of that deployment,
  not universal bounds.
- Hashing a common trace identifier for collection-stage sampling preserves or
  discards a whole trace rather than producing a disconnected subset of spans.
- Dapper deliberately omitted RPC payloads by default for privacy and security;
  application annotations were opt-in.

## Relevance

**Atom OS inference:** trace context belongs in the managed message and service
invocation envelope so that asynchronous actor work, IPC, device calls, and
remote calls can share one causal model. The runtime can provide propagation,
bounded local buffers, typed event emission, and accounting. The OTP-like
observability service should own sampling, collection, indexing, access policy,
retention, and export. The kernel should emit only minimal capability-controlled
events and sealed crash facts rather than host a general trace database or
policy engine.

Whole-trace sampling and explicit sampling probabilities are useful defaults,
but audit and rare safety events need a separate, unsampled path. Trace IDs are
correlation data, not authority: accepting an inbound identifier must never
grant access or establish caller identity.

## Limits

The deployment benefited from common Google libraries and a homogeneous control
flow model. Unsupported transports and unusual concurrency could break trace
propagation or assign the wrong causal parent. Aggressive sampling can miss a
rare, one-off failure, so the evidence does not justify treating traces as a
complete audit record. Asynchronous clocks and partial traces complicate event
ordering. The paper reports performance and operational utility, not
confidentiality, tamper evidence, real-time latency bounds, or resistance to a
malicious service forging context and annotations.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [OTP-like system-services deep-dive journal](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
