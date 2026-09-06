---
title: "AMD64 Architecture Programmer's Manual Volume 2: System Programming"
kind: source
created: "2026-09-06"
authors:
  - "Advanced Micro Devices, Inc."
published: "2026-03-06"
citation_key: "amd-2026-amd64-system-programming-manual"
container: "AMD Technical Information Portal"
edition: "Publication 24593, revision 3.44; catalog metadata only"
isbn: null
doi: null
url: "https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2"
accessed: "2026-09-06"
tags:
  - cpu-architecture
  - privilege
  - x86-64
aliases: []
---

# AMD64 Architecture Programmer's Manual Volume 2: System Programming

## Reference

Advanced Micro Devices, Inc. *AMD64 Architecture Programmer's Manual Volume 2:
System Programming*. Publication 24593, revision 3.44. The indexed
[official catalog record](https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2)
reports release date 2026-03-06. This is the portal release date, not a claim
about a locally inspected PDF cover.

## Research question or contribution

Which AMD-specific entry, paging, interrupt, timer and CPU-startup rules must
the new AMD64 kernel implement?

## Method

Bibliographic discovery only in this session. Search located official catalog
metadata. Direct retrieval of the catalog and indexed content endpoint returned
404, including an independent HTTP check. The older TechDocs URL redirected
to AMD's documentation hub. No full-text architectural audit was possible.

## Findings

The official indexed record identifies the title, publication number, revision
and release date above. Detailed register layouts, exception behavior, ordering
rules and feature availability are **not findings from this retrieval**.

## Relevance

This is the primary reading target for the AMD backend, supplemented by the
actual CPU family's programming reference and revision guide once identified.
Obtain readable official text and pin the revision before implementing
architecture-sensitive code.

## Limits

This source note is a discovery and retrieval-limit record, not evidence that
any detailed manual section was read. Do not substitute Intel-specific MSRs or
a modern QEMU model for missing AMD/platform verification.

## Status after target correction

The user confirmed an Intel-based Dell Precision T7500 and corrected the AMD
assumption. This discovery record is retained for provenance, not as an
active first-target dependency. The earlier full-text retrieval failure no
longer blocks the selected Intel backend.

## Derived work

- [Superseded AMD lab target and minimal QEMU profile](../90-archive/amd64-lab-target-and-minimal-qemu-profile.md)
