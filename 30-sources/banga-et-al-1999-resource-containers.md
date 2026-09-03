---
title: "Resource containers: A new facility for resource management in server systems"
kind: source
created: "2026-09-03"
authors:
  - "Gaurav Banga"
  - "Peter Druschel"
  - "Jeffrey C. Mogul"
published: 1999
citation_key: "banga-et-al-1999-resource-containers"
container: "3rd Symposium on Operating Systems Design and Implementation"
edition: "OSDI '99"
isbn: null
doi: null
url: "https://www.usenix.org/conference/osdi-99/resource-containers-new-facility-resource-management-server-systems"
accessed: "2026-09-03"
tags:
  - accounting
  - operating-systems
  - resource-control
  - scheduling
aliases:
  - "Resource containers"
---

# Resource containers: A new facility for resource management in server systems

## Reference

Gaurav Banga, Peter Druschel, and Jeffrey C. Mogul. “[Resource Containers: A
New Facility for Resource Management in Server
Systems](https://www.usenix.org/conference/osdi-99/resource-containers-new-facility-resource-management-server-systems).”
*3rd Symposium on Operating Systems Design and Implementation*, 1999.

## Research question or contribution

The paper identifies a mismatch between execution/protection units and the
activities to which server resource use should be charged. It introduces a
resource container as an independently named, hierarchical resource principal
that can follow work across process and kernel boundaries.

## Method

The authors modify a general-purpose operating system, add container-aware CPU
and network accounting, and evaluate primitive costs, Web-server throughput,
prioritized clients, CGI control, SYN-flood resistance, and virtual-server
isolation.

## Findings

- A process or thread is often the wrong accounting principal for event-driven
  servers handling many independent requests.
- Separating the scheduling entity from the resource principal allows work to
  retain its charge identity across asynchronous execution and kernel work.
- Hierarchical containers let policy aggregate child activities while keeping
  finer attribution.
- Accurate attribution still requires every execution path to propagate the
  container. Unlabeled deferred work, shared caches, and interrupt work can
  escape the model.

## Relevance

The abstraction maps directly to a runtime where actors are scheduling
entities but applications, supervisors, gateways, and requests can be the
resource principals. Atom OS should carry an explicit `ChargeContext` through
message copying, garbage collection, timers, table work, native requests, and
trace generation, then roll actor ledgers into kernel-enforced domain accounts.
Protection domains and accounting domains deliberately remain distinct.

## Limits

The prototype is a late-1990s server OS, not a managed actor runtime. Its
experiments do not establish accounting precision for shared binaries, garbage
collector reserve, JIT code, actor mailboxes, or ETS-like tables. A ledger
cannot itself guarantee admission control or select an overload response; those
remain separate mechanisms and policy.

## Derived work

- [Resource accounting and overload control](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control.md)
- [Reduction scheduler and kernel scheduling contexts](../20-notes/managed-actor-runtime-components/reduction-scheduler-and-kernel-scheduling-contexts.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
