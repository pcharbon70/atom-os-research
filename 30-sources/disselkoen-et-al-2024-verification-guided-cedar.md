---
title: "How we built Cedar: a verification-guided approach"
kind: source
created: "2026-09-04"
authors:
  - "Craig Disselkoen"
  - "Aaron Eline"
  - "Shaobo He"
  - "Kyle Headley"
  - "Michael Hicks"
  - "Kesha Hietala"
  - "John Kastner"
  - "Anwar Mamat"
  - "Matt McCutchen"
  - "Neha Rungta"
  - "Bhakti Shah"
  - "Emina Torlak"
  - "Andrew Wells"
published: 2024
citation_key: "disselkoen-et-al-2024-verification-guided-cedar"
container: "Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering"
edition: null
isbn: "979-8-4007-0658-5"
doi: "10.1145/3663529.3663854"
url: "https://arxiv.org/abs/2407.01688"
accessed: "2026-09-04"
tags:
  - authorization
  - differential-testing
  - formal-methods
  - policy-language
aliases:
  - "Verification-guided Cedar"
---

# How we built Cedar: a verification-guided approach

## Reference

Craig Disselkoen et al. “[How We Built Cedar: A Verification-Guided
Approach](https://doi.org/10.1145/3663529.3663854).” *FSE Companion 2024*.
[Author manuscript](https://arxiv.org/abs/2407.01688).

## Research question or contribution

The paper describes verification-guided development: prove properties of a
small executable policy model, differentially test a production engine against
that model, and property-test production components that lack a model.

## Method

Cedar components are modeled in Lean, the Rust implementation is exercised
with millions of generated policies, entities, and requests, and unmodeled
parts are subjected to property-based testing.

## Findings

- Proof and implementation testing address different gaps; a verified model
  does not establish that production code implements it.
- The reported process found four validator defects during proof work and 21
  additional defects through differential and property-based testing.
- Generator coverage and input distributions are explicit assurance concerns,
  not incidental test harness details.

## Relevance

Atom OS should build its policy evaluator and capability-grant compiler from a
small executable semantics, prove fail-closed and non-amplification properties
there, and continually differentially test the production implementation. The
same method should compare a decision with the exact grant installed at a
resource boundary.

## Limits

The method increases confidence but cannot cover policies, data, cryptographic
verification, resource-service bugs, or environmental assumptions omitted from
both model and generators. The reported bug counts are not a comparative
security score.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
