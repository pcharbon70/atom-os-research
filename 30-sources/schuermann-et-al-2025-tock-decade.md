---
title: "Tock: From Research to Securing 10 Million Computers"
kind: source
created: "2026-09-08"
authors:
  - "Leon Schuermann"
  - "Brad Campbell"
  - "Branden Ghena"
  - "Philip Levis"
  - "Amit Levy"
  - "Pat Pannuto"
published: 2025
citation_key: "schuermann-et-al-2025-tock-decade"
container: "ACM SIGOPS 31st Symposium on Operating Systems Principles (SOSP 2025)"
edition: null
isbn: null
doi: "10.1145/3731569.3764828"
url: "https://www.tockos.org/assets/papers/2025-sosp-tock-decade.pdf"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# Tock: From Research to Securing 10 Million Computers

## Reference

Leon Schuermann, Brad Campbell, Branden Ghena, Philip Levis, Amit Levy, Pat Pannuto. [Tock: From Research to Securing 10 Million Computers](https://www.tockos.org/assets/papers/2025-sosp-tock-decade.pdf). ACM SIGOPS 31st Symposium on Operating Systems Principles (SOSP 2025), 2025. DOI: [10.1145/3731569.3764828](https://doi.org/10.1145/3731569.3764828). Accessed 2026-09-08.

## Research question or contribution

What a decade of deployment taught the Tock project about isolation, interfaces and engineering practice.

## Method

Primary project retrospective; reviewed §§2.1, 3 and 5.1–5.4, including interface and memory-protection evolution.

## Findings

The account describes runtime checks and ABI redesign needed around untrusted aliasing despite Rust's typed interfaces. It also discusses timer and protection logic errors and constraints arising from asynchronous design.

## Relevance

Treat type-level structure, boundary validation and operational evidence as complementary rather than equivalent assurance.

## Limits

Deployment scale is the authors' reported experience, not a formal correctness result. Tock's embedded design and Rust implementation do not directly validate a Zig architecture facade.

## Derived work

- [Canonical object and lifetime registry](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade/canonical-object-and-lifetime-registry.md) — architecture synthesis constrained by this source.
- [Split-phase operation and terminal ownership](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade/split-phase-operation-and-terminal-ownership.md) — architecture synthesis constrained by this source.
