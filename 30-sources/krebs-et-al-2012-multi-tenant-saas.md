---
title: "Architectural Concerns in Multi-Tenant SaaS Applications"
kind: source
created: "2026-09-05"
authors:
  - "Rouven Krebs"
  - "Christof Momm"
  - "Samuel Kounev"
published: 2012
citation_key: "krebs-et-al-2012-multi-tenant-saas"
container: "Proceedings of CLOSER 2012"
edition: null
isbn: null
doi: "10.5220/0003957604260431"
url: "https://www.scitepress.org/Link.aspx?doi=10.5220%2F0003957604260431"
accessed: "2026-09-05"
tags:
  - application-architecture
  - multi-tenancy
  - resource-isolation
aliases:
  - "Multi-tenant SaaS concerns"
---

# Architectural Concerns in Multi-Tenant SaaS Applications

## Reference

Rouven Krebs, Christof Momm, and Samuel Kounev. “[Architectural Concerns in
Multi-Tenant SaaS Applications](https://doi.org/10.5220/0003957604260431).”
*Proceedings of the 2nd International Conference on Cloud Computing and
Services Science*, 2012, pages 426–431.

## Research question or contribution

The paper identifies interacting architectural concerns in applications where
one running system serves several tenants.

## Method

The authors synthesize a concern model covering tenant-private views,
configuration, persistence, resource sharing, performance isolation, QoS,
customization, and affinity. It is an architectural analysis rather than a
benchmark of one solution.

## Findings

- Multi-tenancy crosses data, configuration, performance, placement, and
  quality-of-service concerns.
- Sharing choices made at one layer affect isolation and customization at
  others.
- “One application instance” does not imply that every resource or state must
  be shared identically.

## Relevance

Atom OS must bind tenant/security realm into domain identity, authority,
persistence, budgets, telemetry, and recovery. A tenant, bounded context,
supervision subtree, and protected domain remain separate design decisions.

## Limits

The evidence is cloud SaaS-oriented and predates the proposed capability-secure
actor OS. It does not validate a particular protection granularity or threat
model.

## Derived work

- [Cross-layer placement, tenancy, overload, and recovery topology](../20-notes/applications-and-domain-services-components/cross-layer-placement-tenancy-overload-and-recovery-topology.md)
