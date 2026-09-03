---
title: "Scaling symbolic evaluation for automated verification of systems code with Serval"
kind: source
created: "2026-09-02"
authors:
  - "Luke Nelson"
  - "James Bornholt"
  - "Ronghui Gu"
  - "Andrew Baumann"
  - "Emina Torlak"
  - "Xi Wang"
published: 2019
citation_key: "nelson-et-al-2019-serval"
container: "Proceedings of the 27th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "978-1-4503-6873-5"
doi: "10.1145/3341301.3359641"
url: "https://www.microsoft.com/en-us/research/publication/scaling-symbolic-evaluation-for-automated-verification-of-systems-code-with-serval/"
accessed: "2026-09-02"
tags:
  - assembly
  - formal-verification
  - instruction-set
  - systems-software
aliases:
  - "Serval"
---

# Scaling symbolic evaluation for automated verification of systems code with Serval

## Reference

Luke Nelson et al. “Scaling Symbolic Evaluation for Automated Verification of
Systems Code with Serval.” *SOSP '19*, 18 pages, 2019. DOI
[10.1145/3341301.3359641](https://doi.org/10.1145/3341301.3359641).
[Author record and paper](https://www.microsoft.com/en-us/research/publication/scaling-symbolic-evaluation-for-automated-verification-of-systems-code-with-serval/).

## Research question or contribution

Can executable instruction-set interpreters and symbolic evaluation make
verification of low-level systems binaries more automated and scalable?

## Method

Serval lifts interpreters for RISC-V, x86-32, LLVM, and BPF into symbolic
verifiers. The authors retrofit CertiKOS and Komodo, verify Keystone monitor
code, and examine Linux BPF JIT compilers.

## Findings

- The framework expresses refinement and noninterference properties over
  executable machine models and can reason directly about binary images.
- Applying the tools uncovered 18 previously unknown bugs that developers
  confirmed and fixed, including undefined behavior and compiler defects.
- Verification scalability depends on representation choices, bounded control
  flow, and symbolic profiling; arbitrary systems code does not become cheap to
  verify automatically.
- The instruction-set interpreter and its semantics become trusted artifacts
  and require their own validation and tests.

## Relevance

A small architecture-primitives capsule is a tractable unit for executable
models, symbolic tests, and binary-level contracts. The result supports making
the capsule's state, clobbers, and completion semantics explicit and keeping
policy and unbounded parsing out of the verification target.

## Limits

Serval does not provide a verified model for every current ISA extension,
device, compiler, or microarchitectural effect. Its successful case studies do
not prove that this project's future capsule will verify without significant
modeling work.

## Derived work

- [Unsafe architecture-primitives capsule](../20-notes/kernel-hardware-and-architecture-components/unsafe-architecture-primitives-capsule.md)
