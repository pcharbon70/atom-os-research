---
title: "Proof-carrying code"
kind: source
created: "2026-09-03"
authors:
  - "George C. Necula"
published: 1997
citation_key: "necula-1997-proof-carrying-code"
container: "24th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages"
edition: "POPL '97, 106-119"
isbn: null
doi: "10.1145/263699.263712"
url: "https://doi.org/10.1145/263699.263712"
accessed: "2026-09-03"
tags:
  - code-loading
  - formal-verification
  - language-safety
  - virtual-machines
aliases:
  - "PCC"
---

# Proof-carrying code

## Reference

George C. Necula. “[Proof-Carrying
Code](https://doi.org/10.1145/263699.263712).” *Proceedings of the 24th ACM
SIGPLAN-SIGACT Symposium on Principles of Programming Languages*, pages
106–119, 1997.

## Research question or contribution

The paper asks how a host can check that untrusted binary code obeys a defined
safety policy without trusting the producer, its compiler, or a heavyweight
runtime monitor. Its answer separates a producer-generated proof from a small
consumer-side validator: code is admitted only when the proof checks against
the host's policy.

## Method

Necula develops the proof-carrying-code protocol formally and reports case
studies for safely linking hand-optimized assembly with an ML program. The work
defines concrete safety predicates and proof representations, then places the
trusted burden on the policy, verification-condition generator, and proof
checker rather than on the code producer.

## Findings

- Admission can be a local, deterministic check whose trusted implementation
  is much smaller than the untrusted producer toolchain.
- The proof is meaningful only relative to an explicit safety policy and
  machine semantics; “verified” is not an unqualified property of a binary.
- Producer effort can be high while consumer checking remains comparatively
  simple, which is useful when one runtime loads many modules.
- A successful safety proof establishes only the encoded properties. It does
  not establish functional correctness, resource boundedness, liveness, or
  compatibility with a language runtime unless those are represented in the
  policy.

## Relevance

The result supports keeping the Atom OS BEAM loader's trusted admission path
small and explicit. Ordinary BEAM modules will initially be checked by a
structural verifier rather than carrying PCC proofs, but the same division
applies: parse into private staging memory, derive obligations for control
flow, operands, roots, safe points, and profile features, then publish only an
immutable checked image. A future certified compiler may attach independently
checkable certificates, but a signature or compiler identity is not a
substitute for validation.

## Limits

The evaluated policies and assembly case studies are not BEAM semantics, a
garbage-collector root proof, or an end-to-end verified loader. Proof
production, proof size, policy evolution, and faithful modeling of a modern
JIT remain substantial engineering problems. The paper therefore motivates a
trust decomposition, not an immediate requirement that all compatible BEAM
artifacts carry formal proofs.

## Derived work

- [Compatibility manifest, BEAM loader, and verifier](../20-notes/managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier.md)
- [Code execution, safe points, and version publication](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
