---
title: "Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time"
kind: source
created: "2026-08-31"
authors:
  - "Anna Lyons"
  - "Kent McLeod"
  - "Hesham Almatary"
  - "Gernot Heiser"
published: 2018
citation_key: "lyons-et-al-2018-scheduling-context-capabilities"
container: "Proceedings of the Thirteenth EuroSys Conference"
edition: null
isbn: "978-1-4503-5584-1"
doi: "10.1145/3190508.3190539"
url: "https://www.sel4.systems/Research/pdfs/scheduling-context-capabilities.pdf"
accessed: "2026-08-31"
tags:
  - capabilities
  - operating-systems
  - scheduling
  - temporal-isolation
aliases:
  - "Scheduling-context capabilities paper"
---

# Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time

## Reference

Anna Lyons, Kent McLeod, Hesham Almatary, and Gernot Heiser.
“Scheduling-Context Capabilities: A Principled, Light-Weight Operating-System
Mechanism for Managing Time.” *EuroSys '18*, Article 26, 16 pages. DOI
[10.1145/3190508.3190539](https://doi.org/10.1145/3190508.3190539).
[Open PDF](https://www.sel4.systems/Research/pdfs/scheduling-context-capabilities.pdf).

## Research question or contribution

Can CPU time become explicit capability-mediated authority, providing temporal
isolation while leaving scheduling and mixed-criticality policy at user level?

## Method

The authors define scheduling-context objects with budgets and periods,
implement them in seL4's MCS branch, add passive-server donation and timeout
handling, then evaluate microbenchmarks and interference workloads on Arm and
x86 systems.

## Findings

- A scheduling-context capability controls a replenished budget rather than
  merely a priority. Depleted contexts cannot continue monopolizing a core.
- Passive servers can run on a caller's donated context, preserving accounting
  through synchronous call chains and supporting user-level scheduling policy.
- Maximum-controlled-priority authority bounds which priorities a scheduler
  may assign.
- Budget expiry can produce a timeout exception at a configured handler.
- Table 2 reports platform- and operation-dependent overhead: compared with
  baseline seL4, MCS `call`/`replyRecv` overhead was 21%/8% on the evaluated Arm
  platform and 1%/4% on x64, while the measured scheduling operation was
  45%/38% slower. Absolute costs and end-to-end effects remained
  workload-specific.

## Relevance

Spatial capabilities alone do not protect the BEAM runtime or its supervisors
from CPU starvation. The minimal kernel should make budgets first-class,
reserve independent time for recovery, and charge synchronous service work to
the initiating domain. Runtime reductions remain a second, actor-level
accounting mechanism.

## Limits

The work targets mixed-criticality and real-time systems, not BEAM workloads.
Donation is intra-core in the design and can be nested; a server that fails to
reply creates a cancellation and authority-return problem. The project must
bound call depth and outstanding reply objects and add supervisor-controlled
cancellation rather than assuming all servers are trusted.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
