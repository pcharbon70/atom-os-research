---
title: "Midas: Systematic kernel TOCTTOU protection"
kind: source
created: "2026-09-04"
authors:
  - "Atri Bhattacharyya"
  - "Uros Tesic"
  - "Mathias Payer"
published: 2022
citation_key: "bhattacharyya-et-al-2022-midas"
container: "31st USENIX Security Symposium"
edition: null
isbn: "978-1-939133-31-1"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity22/presentation/bhattacharyya"
accessed: "2026-09-04"
tags:
  - kernels
  - operating-systems
  - security
  - toctou
  - user-access
aliases:
  - "Midas"
---

# Midas: Systematic kernel TOCTTOU protection

## Reference

Atri Bhattacharyya, Uros Tesic, and Mathias Payer. “Midas: Systematic Kernel
TOCTTOU Protection.” *31st USENIX Security Symposium*, pages 107–124, 2022.
[USENIX paper and artifacts](https://www.usenix.org/conference/usenixsecurity22/presentation/bhattacharyya).

## Research question or contribution

Can the kernel enforce a stable view of user memory throughout a system call,
eliminating double-fetch races even in existing modules?

## Method

Midas creates on-demand snapshots or copies for user data accessed during a
system call, instruments the Linux kernel's relevant memory accesses, and
evaluates exploit resistance and performance across compute- and system-call-
heavy workloads.

## Findings

- A check followed by a second read from the same user object is unsafe because
  sibling threads, remapping, file-backed updates, kernel paths, or DMA may
  change the bytes between observations.
- The system's stated invariant is that each read of one user object during a
  system call returns the same value.
- The prototype reports no noticeable compute-bound slowdown, 0.2–14%
  overhead on system-call-heavy workloads, and about 3.4% average overhead
  over the two evaluated benchmark suites.
- Page-granular snapshotting broadens the protected region and can impose work
  beyond the bytes the kernel actually consumes.

## Relevance

Midas provides a strong upper bound for an Atom user-access profile: one
operation may require snapshot consistency, not merely fault safety. The
baseline should obtain it cheaply by copying small control inputs once; a
page-snapshot or fetch-cache profile remains optional for compatibility paths.

## Limits

Midas is a Linux prototype rather than a proof, and complete coverage depends
on mediating all relevant reads. Stable data does not preserve object
generation or authority. Reported overheads and attack coverage do not
transfer automatically to Atom's microkernel and capability boundaries. The
paper explicitly excludes device/DMA modification from the protected threat
model; it notes a possible IOMMU extension but does not implement or
evaluate device-complete snapshot protection.

## Derived work

- [Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md)
