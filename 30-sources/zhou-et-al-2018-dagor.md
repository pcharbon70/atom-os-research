---
title: "Overload control for scaling WeChat microservices"
kind: source
created: "2026-09-03"
authors:
  - "Hao Zhou"
  - "Ming Chen"
  - "Qian Lin"
  - "Yong Wang"
  - "Xiaobin She"
  - "Sifan Liu"
  - "Rui Gu"
  - "Beng Chin Ooi"
  - "Junfeng Yang"
published: 2018
citation_key: "zhou-et-al-2018-dagor"
container: "Proceedings of the ACM Symposium on Cloud Computing (SoCC '18)"
edition: null
isbn: "978-1-4503-6011-1"
doi: "10.1145/3267809.3267823"
url: "https://www.cs.columbia.edu/~junfeng/papers/dagor-socc18.pdf"
accessed: "2026-09-03"
tags:
  - admission-control
  - load-shedding
  - microservices
  - overload-control
aliases:
  - "DAGOR"
---

# Overload control for scaling WeChat microservices

## Reference

Hao Zhou, Ming Chen, Qian Lin, Yong Wang, Xiaobin She, Sifan Liu, Rui Gu,
Beng Chin Ooi, and Junfeng Yang. “Overload Control for Scaling WeChat
Microservices.” *Proceedings of the ACM Symposium on Cloud Computing
(SoCC '18)*, pages 149–161, 2018. DOI
[10.1145/3267809.3267823](https://doi.org/10.1145/3267809.3267823).
[Author-hosted paper](https://www.cs.columbia.edu/~junfeng/papers/dagor-socc18.pdf).

## Research question or contribution

How can overload control remain service-agnostic and scalable when one user
request fans out through many changing microservices? DAGOR combines local
overload detection with priority-based admission and communicates downstream
admission levels to upstream services so they can reject doomed work before
performing partial call-path processing.

## Method

The paper describes operational experience after DAGOR had run in the WeChat
backend for more than five years. Its controlled evaluation uses an in-house
cluster, a synthetic messaging workload, and an encryption service deployed on
three servers with about 750 requests per second of saturated throughput.
Single- and repeated-downstream-call workloads compare queue-delay detection
with response-time detection and compare DAGOR with CoDel, SEDA, and random
admission baselines.

## Findings

- DAGOR measures local queueing time between request arrival and processing
  start. In its evaluation this distinguished local saturation from downstream
  response delay more accurately than end-to-end response time.
- Detection is decentralized per server. Admission is collaborative: a
  downstream service piggybacks its current admission level on responses, and
  upstream services cache that level and avoid sending work that would be
  rejected.
- Entry services assign business and user priorities, and all requests on the
  same call path inherit them. Rejecting an entire low-priority path early
  avoids wasting capacity on partial work whose final request would fail.
- User priority changes by a periodically varied hash, giving a user consistent
  treatment during one interval while rotating preferred users across
  intervals. This is the paper's fairness mechanism, not a general fairness
  theorem.
- The experiments report success rates closer to the calculated optimum than
  the comparison schemes, particularly when a task invokes the overloaded
  downstream service multiple times.

## Relevance

**Atom OS inference:** the managed actor runtime should expose bounded mailbox
depth, queue residence time, execution delay, deadlines, cancellation, and
resource accounting as mechanisms. The OTP-like admission service should own
the policies that interpret those signals, assign service-class priorities,
choose degradation or rejection, and distribute current admission state.
Propagation should follow the complete actor call or request graph so that
upstream services can reject work before it consumes downstream capacity.

Priority and admission metadata must be integrity-protected and derived from
the caller's capability or authenticated service identity; an application must
not promote itself by writing a more favorable header. Recovery supervisors
also need independent restart and resource budgets so overload does not become
a restart storm.

## Limits

DAGOR is tailored to WeChat's account-oriented request model and highly
structured top-down call paths. Its one-second-or-2,000-request windows,
20-millisecond queue threshold, 500-millisecond task timeout, and priority
taxonomy are empirical deployment choices, not portable constants. The
controlled workloads are synthetic and small relative to the production system.
Rejected invocations were retried up to three times, which could amplify load
without a retry budget and jitter. Priority policy can starve lower classes or
encode organizational bias, and feedback can be stale during rapid changes.
Queueing delay is an admission signal, not a hard CPU, memory, or I/O guarantee;
lower layers still need enforceable resource limits.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [OTP-like system-services deep-dive journal](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
