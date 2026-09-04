---
title: "Cedar: a new language for expressive, fast, safe, and analyzable authorization"
kind: source
created: "2026-09-04"
authors:
  - "Joseph W. Cutler"
  - "Craig Disselkoen"
  - "Aaron Eline"
  - "Shaobo He"
  - "Kyle Headley"
  - "Michael Hicks"
  - "Kesha Hietala"
  - "Eleftherios Ioannidis"
  - "John Kastner"
  - "Anwar Mamat"
  - "Darin McAdams"
  - "Matt McCutchen"
  - "Neha Rungta"
  - "Emina Torlak"
  - "Andrew Wells"
published: 2024
citation_key: "cutler-et-al-2024-cedar"
container: "Proceedings of the ACM on Programming Languages 8(OOPSLA1), 670–697"
edition: null
isbn: null
doi: "10.1145/3649835"
url: "https://arxiv.org/abs/2403.04651"
accessed: "2026-09-04"
tags:
  - authorization
  - formal-methods
  - policy-language
aliases:
  - "Cedar policy language"
---

# Cedar: a new language for expressive, fast, safe, and analyzable authorization

## Reference

Joseph W. Cutler et al. “[Cedar: A New Language for Expressive, Fast, Safe,
and Analyzable Authorization](https://doi.org/10.1145/3649835).” *Proceedings
of the ACM on Programming Languages* 8(OOPSLA1), pages 670–697, 2024.
[Extended version](https://arxiv.org/abs/2403.04651).

## Research question or contribution

The paper presents a purpose-built authorization language intended to combine
readable RBAC-, ABAC-, and relation-oriented policies with bounded evaluation,
schema validation, high request throughput, and precise formal analysis.

## Method

The authors define Cedar’s syntax and semantics, implement a Rust engine and
validator, encode the design in Lean, prove properties of the model, and
compare readability and performance with OpenFGA and Rego on selected
benchmarks.

## Findings

- Separating policy from application code makes decisions independently
  inspectable, testable, versionable, and analyzable.
- The language uses an explicit principal, action, resource, and context request
  with permit and forbid policies; forbid can override permit.
- Schema-aware validation catches mismatched entity, action, and attribute use
  before deployment.
- A sound and complete logical encoding supports equivalence and change-impact
  questions that an unconstrained general-purpose policy language makes harder.

## Relevance

Atom OS should adopt Cedar-like design constraints, not necessarily Cedar’s
syntax unchanged: total deterministic evaluation, no network or time I/O inside
the evaluator, typed schemas, explicit deny precedence, versioned policy and
entity snapshots, explainable decision identifiers, and analyzable
non-escalation properties. Decisions then mint attenuated capabilities rather
than returning an ambient boolean to be trusted indefinitely.

## Limits

The proofs apply to the modeled language and the paper’s connection to its
implementation, not to an Atom OS port, policy data provenance, deployment,
resource service, or entire authorization lifecycle. Expressiveness,
administrative usability, and benchmark comparisons are workload-dependent.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
