---
title: "Verified security for the Morello capability-enhanced prototype Arm architecture"
kind: source
created: "2026-09-04"
authors:
  - "Thomas Bauereiss"
  - "Brian Campbell"
  - "Thomas Sewell"
  - "Alasdair Armstrong"
  - "Lawrence Esswood"
  - "Ian Stark"
  - "Graeme Barnes"
  - "Robert N. M. Watson"
  - "Peter Sewell"
published: 2022
citation_key: "bauereiss-et-al-2022-verified-morello-security"
container: "Programming Languages and Systems, ESOP 2022, LNCS 13240, 174–203"
edition: null
isbn: "978-3-030-99335-1"
doi: "10.1007/978-3-030-99336-8_7"
url: "https://www.research.ed.ac.uk/en/publications/verified-security-for-the-morello-capability-enhanced-prototype-a/"
accessed: "2026-09-04"
tags:
  - capabilities
  - cheri
  - formal-verification
  - memory-safety
aliases:
  - "Verified Morello security"
---

# Verified security for the Morello capability-enhanced prototype Arm architecture

## Reference

Thomas Bauereiss et al. “[Verified Security for the Morello Capability-enhanced
Prototype Arm Architecture](https://doi.org/10.1007/978-3-030-99336-8_7).”
*ESOP 2022*, Lecture Notes in Computer Science 13240, pages 174–203.

## Research question or contribution

The paper defines reachable capability monotonicity for Morello, translates the
industrial-scale ISA specification into Isabelle/HOL, and proves that the
architecture model satisfies the property.

## Method

The proof factors the roughly 210,000-line generated Isabelle model through a
narrow abstraction for CHERI ISAs. Model-based instruction-sequence tests and
Arm’s internal test suite are used to validate the model and implementation
development.

## Findings

- Tagged, bounded, permission-bearing architectural capabilities can prevent
  software from constructing authority not reachable from existing
  capabilities under the proved ISA model.
- A high-level monotonicity proof can be carried through a full-scale
  industrial architecture specification rather than only a toy ISA.
- Model validation and implementation testing remain necessary companions to
  proof.

## Relevance

A future CHERI-enabled Atom OS target could strengthen memory safety and
fine-grained compartmentalization inside the kernel, runtime, and native
services. The architecture should nevertheless express its security contract
in ISA-independent typed kernel capabilities first, with CHERI as a stronger
hardware profile rather than a prerequisite.

## Limits

Morello is a prototype architecture, and the proof is not a proof of an entire
processor, compiler, kernel, allocator, temporal-memory-safety discipline, or
Atom OS. Reachable capability monotonicity does not supply human authentication,
policy, revocation, availability, side-channel freedom, or distributed trust.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
