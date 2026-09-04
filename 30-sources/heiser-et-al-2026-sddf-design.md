---
title: "sDDF design: Design, implementation and evaluation of the seL4 device driver framework"
kind: source
created: "2026-09-04"
authors:
  - "Gernot Heiser"
  - "Peter Chubb"
  - "Alex Brown"
  - "Tristan Clinton-Muehr"
  - "Courtney Darville"
  - "Alwin Joshy"
  - "Craig McLaughlin"
  - "Bill Nguyen"
  - "Lesley Rossouw"
  - "Lucy Fletcher"
  - "Julia Vassiliki"
  - "Ivan Velickovic"
  - "Jade Zhou"
published: "2026-08-19"
citation_key: "heiser-et-al-2026-sddf-design"
container: "Trustworthy Systems Group technical report"
edition: "Release 0.7"
isbn: null
doi: null
url: "https://trustworthy.systems/projects/drivers/sddf-design.pdf"
accessed: "2026-09-04"
tags:
  - device-drivers
  - isolation
  - microkernels
  - sel4
  - zero-copy
aliases:
  - "seL4 Device Driver Framework design"
---

# sDDF design: Design, implementation and evaluation of the seL4 device driver framework

## Reference

Gernot Heiser, Peter Chubb, Alex Brown, Tristan Clinton-Muehr, Courtney
Darville, Alwin Joshy, Craig McLaughlin, Bill Nguyen, Lesley Rossouw, Lucy
Fletcher, Julia Vassiliki, Ivan Velickovic, and Jade Zhou. “[sDDF Design:
Design, Implementation and Evaluation of the seL4 Device Driver
Framework](https://trustworthy.systems/projects/drivers/sddf-design.pdf).”
Release 0.7, Trustworthy Systems Group, 19 August 2026.

## Research question or contribution

The report defines a framework for native isolated device-driver components on
seL4, including a device model, asynchronous transport, driver and virtualizer
roles, synchronization patterns, threat model, device-class protocols, and a
preliminary performance evaluation. Its explicit hardware and driver
assumptions are intended to support later formal specification and
verification.

## Method

The design and evaluation report was read across its aims, threat model,
transport, component roles, synchronization, device classes, security
analysis, implementation status, and performance chapters. No sDDF build,
hardware reproduction, or independent verification was performed.

## Findings

- Drivers and clients are isolated native components. A virtualizer mediates a
  shared device when policy or multiplexing cannot safely live in the driver.
  This keeps each component's trusted role narrower than an in-kernel driver.
- The transport separates bounded metadata queues from data regions. Producer
  and consumer exchange ownership through single-producer/single-consumer
  queues, including return paths, which avoids a hidden shared allocator in
  the fast path.
- Memory is shared selectively. A component maps only the payload and metadata
  regions required for its role; an IOMMU is needed where hardware DMA must be
  confined to the same authority boundary.
- Active and passive driver-thread models trade scheduling overhead against
  latency and temporal isolation. The choice is an explicit system design
  parameter rather than an invisible property of a callback.
- The reported network experiments show that modular isolation can approach
  Linux throughput with a limited overhead in the evaluated configurations,
  but results depend on hardware, topology, batching, and device class.
- Discovery, initialization, several device classes, and eventual component
  verification remain incomplete. The authors label the evaluation and report
  as work in progress.

## Relevance

Atom OS should place each physical device or reset-coupled group in a protected
driver domain and expose a separate class virtualizer or validator where
clients need multiplexing. Queue entries should transfer explicit buffer
ownership and include caller, service, device, and operation generations. A
return queue makes reclamation observable; queue exhaustion must have a stated
backpressure result.

sDDF also supports keeping mechanism and policy apart. The lower layers grant
MMIO, interrupts, DMA windows, scheduling context, and reset facets. The
unprivileged service manager selects the driver, meters clients, records
outcomes, performs recovery, and publishes the current generation. Atom OS
adds a persistent in-flight ledger and fencing protocol because isolated
restart alone cannot decide whether hardware accepted an effect.

## Limits

Release 0.7 is explicitly preliminary and tied to seL4 and its trusted
framework assumptions. The performance section does not prove uniform cost
across devices or workloads, and the design does not solve all discovery,
initialization, crash recovery, or external-effect ambiguity. Isolation does
not make a compromised trusted virtualizer safe, retract DMA already accepted
by a device, or establish Atom OS compatibility. The report is a strong design
reference, not an implementation result for this repository.

## Derived work

- [Device-service policy and management](../20-notes/otp-like-system-services-components/device-service-policy-and-management.md)
- [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
