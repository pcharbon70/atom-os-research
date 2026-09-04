---
title: "Exponential backoff and jitter"
kind: source
created: "2026-09-04"
authors:
  - "Marc Brooker"
published: "2015-03-04"
citation_key: "brooker-2015-exponential-backoff-jitter"
container: "AWS Architecture Blog"
edition: "Updated May 2023"
isbn: null
doi: null
url: "https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/"
accessed: "2026-09-04"
tags:
  - backoff
  - overload
  - recovery
  - retries
aliases:
  - "Backoff and jitter"
---

# Exponential backoff and jitter

## Reference

Marc Brooker. “[Exponential Backoff and
Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/).”
AWS Architecture Blog, 4 March 2015; updated May 2023.

## Research question or contribution

The article asks how many concurrent clients should retry after conflicting
optimistic-concurrency operations. It demonstrates why capped exponential
backoff alone preserves synchronized retry clusters and compares several ways
of randomizing the delay.

## Method

Brooker uses a small published simulator of clients contending on one remote
database row over a network with ten-millisecond mean delay and four-millisecond
variance. The post compares immediate retry, capped exponential backoff, Full
Jitter, Equal Jitter, and Decorrelated Jitter in total calls and completion
time. This is practitioner simulation evidence, not a production supervisor
benchmark.

## Findings

- With one winner per contention round, completion time grows linearly with
  contenders while aggregate attempted work grows quadratically.
- Capped exponential backoff reduces frequency but keeps retry attempts
  clustered because clients retain correlated schedules. It creates idle gaps
  and later bursts instead of smoothing demand.
- Random jitter spreads retry traffic. In the presented 100-client case it
  reduced calls by more than half and improved completion time relative to
  unjittered exponential backoff.
- Full and Decorrelated Jitter give different work/time trade-offs; Equal
  Jitter performed worse in the reported comparison. The author recommends
  jittered backoff while acknowledging it does not change the underlying
  quadratic worst-case contention.
- A retry delay controls offered work; it does not determine whether retry is
  semantically safe after an unknown remote outcome.

## Relevance

Atom OS native supervisors and reconcilers should use capped Full Jitter as an
initial default after a restartable transient failure, with the cap, random
source, retry budget, deadline, and cooldown recorded in policy. Siblings that
fail from one dependency outage must not all restart at the same deterministic
instants. The reserved control and recovery paths need separate admission so
their own jittered retries cannot starve ordinary progress.

Jitter applies only after policy classifies the action as retryable. Unknown
device, storage, network, or update outcomes must be reconciled first. OTP
compatibility supervisors should retain documented OTP timing; the jittered
policy belongs to the native extension.

## Limits

The simulation is narrow and assumes one style of contention and network
delay. It does not prove Full Jitter optimal for local actors, establish hard
latency bounds, model adversarial randomness, or include client deadlines and
priorities. Randomness can also harm deterministic replay unless choices are
recorded. Atom OS must benchmark failure bursts and suspend/resume behavior on
its own scheduler and monotonic-clock profiles.

## Derived work

- [Supervision and recovery policy](../20-notes/otp-like-system-services-components/supervision-and-recovery-policy.md)
- [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance.md)
