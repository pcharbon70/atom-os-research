---
title: "SafeFetch: Practical double-fetch protection with kernel-fetch caching"
kind: source
created: "2026-09-04"
authors:
  - "Victor Duta"
  - "Mitchel Josephus Aloserij"
  - "Cristiano Giuffrida"
published: 2024
citation_key: "duta-et-al-2024-safefetch"
container: "33rd USENIX Security Symposium"
edition: null
isbn: "978-1-939133-44-1"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity24/presentation/duta"
accessed: "2026-09-04"
tags:
  - kernels
  - operating-systems
  - security
  - toctou
  - user-access
aliases:
  - "SafeFetch"
---

# SafeFetch: Practical double-fetch protection with kernel-fetch caching

## Reference

Victor Duta, Mitchel Josephus Aloserij, and Cristiano Giuffrida. “SafeFetch:
Practical Double-Fetch Protection with Kernel-Fetch Caching.” *33rd USENIX
Security Symposium*, pages 1207–1224, 2024.
[USENIX paper and artifacts](https://www.usenix.org/conference/usenixsecurity24/presentation/duta).

## Research question or contribution

Can a kernel systematically prevent double-fetch vulnerabilities without the
coarse page trapping and copying overhead of prior snapshot techniques?

## Method

SafeFetch instruments kernel fetches and maintains a byte-granular, per-system-
call cache. A later fetch of overlapping user data replays cached bytes instead
of reading concurrently mutable user memory again. The authors implement the
scheme in Linux, evaluate security cases and benchmark overhead, and release
an artifact.

## Findings

- A double fetch is not merely a bad pointer: it is a consistency failure when
  authorization, length, or structure validation observes different versions
  of attacker-controlled bytes.
- Per-system-call fetch caching can give repeated reads one stable value without
  trapping every write to a whole user page.
- The prototype reports comprehensive protection in its evaluated coverage and
  a 4.4% geometric-mean overhead on LMBench.
- Correctness depends on mediating every relevant fetch path and scoping cache
  identity and lifetime to the system-call operation.

## Relevance

SafeFetch supports an Atom rule that control data crosses the boundary once
into kernel-owned storage and is then parsed and authorized from that snapshot.
It also motivates an optional per-operation fetch cache if compatibility code
must repeat reads. Neither raw pointer validation nor a pinned page makes
mutable contents stable.

## Limits

The results are from a Linux prototype and selected workloads. The paper does
not prove all possible kernel or device fetches are mediated, and the 4.4%
number is not an Atom performance prediction. Stable bytes do not establish
that their meaning, authority, or target object remains current.

## Derived work

- [Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md)
