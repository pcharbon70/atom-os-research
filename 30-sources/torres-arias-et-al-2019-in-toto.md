---
title: "in-toto: Providing farm-to-table guarantees for bits and bytes"
kind: source
created: "2026-09-04"
authors:
  - "Santiago Torres-Arias"
  - "Hammad Afzali"
  - "Trishank Karthik Kuppusamy"
  - "Reza Curtmola"
  - "Justin Cappos"
published: 2019
citation_key: "torres-arias-et-al-2019-in-toto"
container: "28th USENIX Security Symposium (USENIX Security 19)"
edition: null
isbn: "978-1-939133-06-9"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias"
accessed: "2026-09-04"
tags:
  - provenance
  - software-supply-chain
  - software-update
  - security
aliases:
  - "in-toto paper"
---

# in-toto: Providing farm-to-table guarantees for bits and bytes

## Reference

Santiago Torres-Arias, Hammad Afzali, Trishank Karthik Kuppusamy, Reza
Curtmola, and Justin Cappos. “[in-toto: Providing Farm-to-Table Guarantees for
Bits and Bytes](https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias).”
*28th USENIX Security Symposium*, pages 1393–1410, 2019.

## Research question or contribution

The paper asks how a consumer can verify that software passed through an
authorized supply-chain sequence, not merely that the final artifact was
signed by a release key.

## Method

The authors define signed layout and link metadata for supply-chain steps,
analyze thirty reported software-supply-chain compromises against the design,
implement the framework, and report integrations and performance.

## Findings

- A final artifact signature cannot show which builders, tests, or transforms
  produced the artifact.
- A layout can constrain authorized functionaries, step order, expected
  materials/products, and inspection rules; signed link metadata records what
  happened at each step.
- Compromise resistance depends on which functionary keys and build
  environments remain trustworthy.
- Provenance verification complements, rather than replaces, secure delivery
  metadata.

## Relevance

Atom's update/release service should require an approved provenance predicate
and builder identity before treating TUF-authorized bytes as eligible for
staging. Activation still needs target compatibility, rollback policy,
quiescence, state-migration, health, and kernel boot authorization checks.

## Limits

in-toto attests that declared steps and artifact relations were signed; it does
not prove source correctness, compiler correctness, build-host integrity, or
safe runtime behavior. Its compromise analysis cannot cover undisclosed or
future attack classes.

## Derived work

- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
