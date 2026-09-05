---
title: "A portable kernel abstraction for low-overhead ephemeral mapping management"
kind: source
created: "2026-09-04"
authors:
  - "Khaled Elmeleegy"
  - "Anupam Chanda"
  - "Alan L. Cox"
  - "Willy Zwaenepoel"
published: 2005
citation_key: "elmeleegy-et-al-2005-ephemeral-mapping-management"
container: "2005 USENIX Annual Technical Conference"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/legacy/publications/library/proceedings/usenix05/tech/general/full_papers/elmeleegy/elmeleegy_html/text.html"
accessed: "2026-09-04"
tags:
  - kernels
  - operating-systems
  - performance
  - tlb
  - virtual-memory
aliases:
  - "sf_buf ephemeral mappings"
---

# A portable kernel abstraction for low-overhead ephemeral mapping management

## Reference

Khaled Elmeleegy, Anupam Chanda, Alan L. Cox, and Willy Zwaenepoel. “A
Portable Kernel Abstraction for Low-Overhead Ephemeral Mapping Management.”
*2005 USENIX Annual Technical Conference*, pages 223–236.
[Open paper](https://www.usenix.org/legacy/publications/library/proceedings/usenix05/tech/general/full_papers/elmeleegy/elmeleegy_html/text.html).

## Research question or contribution

Can one opaque kernel abstraction combine temporary virtual-address allocation
and physical-page mapping while allowing architecture-specific implementations
to avoid costly remapping and cross-CPU invalidation?

## Method

The paper introduces FreeBSD's opaque `sf_buf` interface, implements it
differently on 32-bit i386 and 64-bit amd64, replaces several subsystem-
specific mapping paths, and measures pipes, memory disks, networking, and web
workloads.

## Findings

- Temporary mapping lifetime and virtual-address allocation belong in one
  object; callers should not manipulate implementation fields independently.
- CPU-private mappings can avoid remote invalidation, while shared mappings
  require a different scope and lifetime.
- The amd64 implementation reused a permanent direct map and avoided mapping
  changes entirely; the i386 implementation cached bounded temporary mappings.
- The paper reports substantially fewer invalidations and workload-dependent
  throughput improvements, including up to 168% for one pipe benchmark.

## Relevance

This work supports a lexical, opaque access-window abstraction and shows why
its backend should be free to use a private temporary slot, a safe existing
alias, or another architecture-specific mechanism. The optimization choice
must remain subordinate to Atom's authority and alias-isolation requirements.

## Limits

The evaluation targets FreeBSD 5.3 and early i386/amd64 systems. Its amd64
direct map is a performance technique, not a security boundary, and later
attacks demonstrate risks from privileged aliases of user-controlled frames.
The historical throughput results are not portable to current machines.

## Derived work

- [Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md)
- [Invalidation planner](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/invalidation-planner.md)
