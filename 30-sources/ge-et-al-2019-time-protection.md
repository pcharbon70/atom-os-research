---
title: "Time protection: The missing OS abstraction"
kind: source
created: "2026-08-31"
authors:
  - "Qian Ge"
  - "Yuval Yarom"
  - "Tom Chothia"
  - "Gernot Heiser"
published: 2019
citation_key: "ge-et-al-2019-time-protection"
container: "Proceedings of the Fourteenth EuroSys Conference"
edition: null
isbn: "978-1-4503-6281-8"
doi: "10.1145/3302424.3303976"
url: "https://www.sel4.systems/Research/pdfs/time-protection-missing-os-abstraction.pdf"
accessed: "2026-08-31"
tags:
  - microarchitectural-security
  - operating-systems
  - side-channels
  - temporal-isolation
aliases:
  - "Time protection paper"
---

# Time protection: The missing OS abstraction

## Reference

Qian Ge, Yuval Yarom, Tom Chothia, and Gernot Heiser. “Time Protection: The
Missing OS Abstraction.” *EuroSys '19*, Article 1, 17 pages. DOI
[10.1145/3302424.3303976](https://doi.org/10.1145/3302424.3303976).
[Open PDF](https://www.sel4.systems/Research/pdfs/time-protection-missing-os-abstraction.pdf).

## Research question or contribution

What operating-system mechanisms are required to prevent information leakage
through microarchitectural timing interference, rather than merely allocating
bounded CPU time?

## Method

The work defines time protection, implements kernel-image cloning,
cache partitioning, state flushing, interrupt partitioning, and time padding in
seL4, then constructs and measures channels on Arm and x86 platforms.

## Findings

- CPU budgets prevent monopolization but do not close timing channels through
  caches, TLBs, predictors, kernel state, interrupts, or shared interconnects.
- Stateful resources must be spatially partitioned or flushed between security
  domains; variable cleanup latency must be padded if it is observable.
- Shared kernel code and data can themselves form channels, motivating
  per-security-domain kernel replicas in the evaluated design.
- The implementation substantially reduced the measured channels, but one x86
  residual channel exposed hardware state the software could not fully control.
- Time protection therefore depends on an honest hardware-software contract,
  not solely on a scheduler algorithm.

## Relevance

The project must distinguish resource temporal isolation from timing-channel
noninterference. The baseline kernel needs hard budgets for availability. A
declared high-security profile may additionally ask the architecture layer for
partition, flush, interrupt-isolation, and padded-switch operations.

## Limits

Measurements cover two historical platforms and selected channels. They do not
prove the absence of all timing channels, and some mechanisms are unavailable
on current hardware. Full time protection may reduce utilization and increase
domain-switch cost, so it should not be silently claimed by the baseline
capability model.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
