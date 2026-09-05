---
title: "Revisiting memory errors in large-scale production data centers: Analysis and modeling of new trends from the field"
kind: source
created: "2026-09-05"
authors:
  - "Justin Meza"
  - "Qiang Wu"
  - "Sanjeev Kumar"
  - "Onur Mutlu"
published: 2015
citation_key: "meza-et-al-2015-revisiting-memory-errors"
container: "45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks"
edition: null
isbn: null
doi: "10.1109/DSN.2015.57"
url: "https://doi.org/10.1109/DSN.2015.57"
accessed: "2026-09-05"
tags:
  - fault-containment
  - hardware-errors
  - memory
  - reliability
aliases:
  - "Facebook memory-error study"
---

# Revisiting memory errors in large-scale production data centers: Analysis and modeling of new trends from the field

## Reference

Justin Meza, Qiang Wu, Sanjeev Kumar, and Onur Mutlu. “Revisiting Memory
Errors in Large-Scale Production Data Centers: Analysis and Modeling of New
Trends from the Field.” *45th Annual IEEE/IFIP International Conference on
Dependable Systems and Networks*, 2015. DOI
[10.1109/DSN.2015.57](https://doi.org/10.1109/DSN.2015.57).

## Research question or contribution

What do long-running production measurements show about memory-error patterns
and the operational effect of page offlining?

## Method

The study analyzes 14 months of hardware-error records across billions of
device-days in Facebook data centers and evaluates page-offlining behavior on
12,276 servers.

## Findings

- Memory errors correlate with hardware age, density, workload, and prior
  errors; the population is heterogeneous and simple independent transient-
  bit models do not explain all field behavior.
- Persistently recording retired pages across reboot prevents known-bad pages
  from returning silently to service.
- In the reported deployment, page offlining reduced logged errors by about
  67 percent on the evaluated servers, while capacity thresholds determined
  when a host required repair.
- Page retirement is useful operational mitigation, not universal recovery:
  locked/unmovable pages and wider device or channel failures remain.
- Fleet correlation supports maintenance policy but does not prove the cause,
  propagation, or safety of resuming one particular machine-check event.

## Relevance

Atom should retain persistent physical-component and retired-extent identity,
track repeated events across boot generations, and expose threshold evidence
to a maintenance service. It must still decide each event using current
precision, ownership, consumption, and containment facts. Historical rate is
policy input, never a `LocalResumePostcondition`.

## Limits

The study is observational and reports one operator's hardware population and
policies. Logged events depend on platform instrumentation and do not reveal
every silent corruption. Aggregate error reduction is not a formal proof that
offlining contained any individual event or its prior effects.

## Derived work

- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
- [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
