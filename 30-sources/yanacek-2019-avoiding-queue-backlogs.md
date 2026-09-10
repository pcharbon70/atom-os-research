---
title: "Avoiding insurmountable queue backlogs"
kind: source
created: "2026-09-10"
authors:
  - "David Yanacek"
published: 2019
citation_key: "yanacek-2019-avoiding-queue-backlogs"
container: "Amazon Builders' Library"
edition: "First-party engineering article; official PDF"
isbn: null
doi: null
url: "https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/"
accessed: "2026-09-10"
tags:
  - system-services
  - reliability
  - service-architecture
aliases: []
---

# Avoiding insurmountable queue backlogs

## Reference

David Yanacek. [Avoiding insurmountable queue backlogs](https://d1.awsstatic.com/builderslibrary/pdfs/avoiding-insurmountable-queue-backlogs.pdf). Amazon Builders' Library; available at its [December 2019 launch](https://aws.amazon.com/blogs/aws/check-out-the-amazon-builders-library-this-is-how-we-do-it/). Exact original publication day is unspecified.

## Research question or contribution

How can asynchronous systems avoid prolonged recovery from excess work?

## Method

First-party operational article; the official eleven-page PDF supplied readable text when the canonical web route redirected to an empty rendered page.

## Findings

Queue age, first-attempt latency, workload isolation, delayed retries and backlog separation expose different failure dimensions. Per-customer queues add operational cost; shuffle sharding is an alternative.

## Relevance

Proposed Atom OS use: independently budget fresh, retry and retained work without dropping accepted semantic obligations.

## Limits

Patterns depend on workload semantics. Fresh-first scheduling and backpressure are not universally appropriate, and the article supplies no Atom OS fairness or hard-latency proof.

## Derived work

- [Internal-service study](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance/queue-age-credit-return-and-backlog-isolation.md).
- [Research session](../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md).
