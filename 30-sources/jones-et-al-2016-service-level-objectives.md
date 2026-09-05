---
title: "Service Level Objectives"
kind: source
created: "2026-09-05"
authors:
  - "Chris Jones"
  - "John Wilkes"
  - "Niall Murphy"
  - "Cody Smith"
published: 2016
citation_key: "jones-et-al-2016-service-level-objectives"
container: "Site Reliability Engineering: How Google Runs Production Systems"
edition: null
isbn: "978-1-4919-2909-4"
doi: null
url: "https://sre.google/sre-book/service-level-objectives/"
accessed: "2026-09-05"
tags:
  - observability
  - reliability-engineering
  - service-level-objectives
aliases:
  - "Google SRE SLOs"
---

# Service Level Objectives

## Reference

Chris Jones, John Wilkes, and Niall Murphy, with Cody Smith. “[Service Level
Objectives](https://sre.google/sre-book/service-level-objectives/).” In *Site
Reliability Engineering: How Google Runs Production Systems*, O'Reilly, 2016.

## Research question or contribution

The chapter explains service-level indicators, objectives, and agreements and
argues that measurement should begin with behavior users care about rather
than metrics easiest for operators to collect.

## Method

This is first-party practitioner guidance based on Google SRE experience, with
worked examples rather than a controlled scientific comparison.

## Findings

- An SLI is a measured behavior; an SLO is a target or range for that measure;
  an SLA adds consequences and is a separate contract.
- Objectives need an exact population, time window, measurement point, and
  validity conditions.
- Availability, latency, throughput, error rate, correctness, and durability
  can matter differently to different services.

## Relevance

Layer 5 should define semantic indicators such as committed-correct outcomes,
indeterminate results, projection freshness, workflow age, and reconciliation
lag. Layer 4 transports and aggregates telemetry but cannot invent business
success from CPU or request counters.

## Limits

The guidance is not a proof, and proxies can be gamed or omit harmed users.
Telemetry may be sampled or lost and therefore cannot replace the durable
outcome or audit ledger.

## Derived work

- [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
