---
title: "Caches and self-modifying code: Working with threads"
kind: source
created: "2026-09-02"
authors:
  - "Jacob Bramley"
published: "2025-01-21"
citation_key: "bramley-2025-arm-self-modifying-code-threads"
container: "Arm Community Architectures and Processors Blog"
edition: null
isbn: null
doi: null
url: "https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/caches-self-modifying-code-working-with-threads"
accessed: "2026-09-02"
tags:
  - aarch64
  - cache-maintenance
  - instruction-fetch
  - just-in-time-compilation
aliases:
  - "Arm multi-threaded self-modifying code guidance"
---

# Caches and self-modifying code: Working with threads

## Reference

Jacob Bramley. “[Caches and Self-Modifying Code: Working with
Threads](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/caches-self-modifying-code-working-with-threads).”
Arm Community Architectures and Processors Blog, 2025-01-21.

## Contribution

The article explains why the standard single-core Arm cache-maintenance
sequence does not by itself synchronize pipelines on other cores and compares
full synchronization with deliberately best-effort code replacement.

## Method

This is an official Arm engineering explanation grounded in the Arm
architecture manual. It develops simplified multi-core examples and separates
data/instruction cache visibility from the executing core's pipeline state.

## Findings

- Data-cache cleaning, instruction-cache invalidation, and broadcast-capable
  barriers can make new bytes visible beyond the writing core, but the writer's
  local instruction-synchronization barrier is not broadcast.
- A core that might execute changed instructions must perform a suitable local
  synchronization action or participate in an equivalent protocol.
- Full cross-thread synchronization is easiest to reason about but requires
  cooperation and has a cost.
- Best-effort replacement is valid only when both the old and new instruction
  streams remain semantically acceptable; it cannot implement a security
  revocation or an atomic incompatible update.

## Relevance

The safe baseline should publish immutable code versions, synchronize every
eligible execution CPU, and expose completion. An optional in-place patch path
may be added only for explicitly compatible old/new semantics with separate
tests and no reuse or permission-revocation claim.

## Limits

This is an engineering article, not a formal model or benchmark. It covers
AArch64 concepts and does not replace the exact versioned architecture manual,
the Arm instruction-fetch formal work, or experiments on the selected cores.

## Derived work

- [Ordering, coherence, and code publication](../20-notes/kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication.md)
