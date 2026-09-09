---
title: "Sequence counters and sequential locks"
kind: source
created: "2026-09-08"
authors:
  - "Linux kernel development community"
published: null
citation_key: "linux-kernel-community-2026-sequence-counter-contracts"
container: "The Linux Kernel documentation"
edition: null
isbn: null
doi: null
url: "https://docs.kernel.org/locking/seqlock.html"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# Sequence counters and sequential locks

## Reference

Linux kernel development community. [Sequence counters and sequential locks](https://docs.kernel.org/locking/seqlock.html). The Linux Kernel documentation; publication date not stated. Accessed 2026-09-08.

## Research question or contribution

When retry-based snapshots give consistent observations and what they do not protect.

## Method

Official locking documentation; reviewed ordinary sequence counters, writer restrictions and latch sequence counters.

## Findings

An interrupting reader that retries against a suspended writer can prevent progress. Sequence validation does not protect pointer-target lifetime. Latch schemes address some interrupted-writer cases but are not generic reclamation mechanisms.

## Relevance

Keep conversion-snapshot consistency, bounded reader progress and backing-storage lifetime as separate obligations.

## Limits

Linux's synchronization rules do not automatically apply to Zig. A retry after conflicting non-atomic access does not retroactively make an illegal language-level race valid; that is our cross-source synthesis.

## Derived work

- [Conversion snapshot publication and lifetime](../20-notes/kernel-hardware-and-architecture-components/raw-time-and-deadline-programming/conversion-snapshot-publication.md) — architecture synthesis constrained by this source.
- [CPU identity, incarnation and membership](../20-notes/kernel-hardware-and-architecture-components/logical-cpu-coordination-and-lifecycle/identity-incarnation-and-membership.md) — architecture synthesis constrained by this source.
