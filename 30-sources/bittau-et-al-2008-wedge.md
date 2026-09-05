---
title: "Wedge: Splitting Applications into Reduced-Privilege Compartments"
kind: source
created: "2026-09-05"
authors:
  - "Andrea Bittau"
  - "Petr Marchenko"
  - "Mark Handley"
  - "Brad Karp"
published: 2008
citation_key: "bittau-et-al-2008-wedge"
container: "5th USENIX Symposium on Networked Systems Design and Implementation"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/nsdi-08/wedge-splitting-applications-reduced-privilege-compartments"
accessed: "2026-09-05"
tags:
  - application-compartmentalization
  - least-privilege
  - security
aliases:
  - "Wedge compartments"
---

# Wedge: Splitting Applications into Reduced-Privilege Compartments

## Reference

Andrea Bittau, Petr Marchenko, Mark Handley, and Brad Karp. “[Wedge: Splitting
Applications into Reduced-Privilege
Compartments](https://www.usenix.org/conference/nsdi-08/wedge-splitting-applications-reduced-privilege-compartments).”
*5th USENIX Symposium on Networked Systems Design and Implementation*, 2008.

## Research question or contribution

Wedge asks how legacy monolithic applications can be divided into small,
default-deny compartments with explicit memory privilege.

## Method

The system adds OS compartment primitives and Crowbar runtime-analysis tools,
then partitions Apache/OpenSSL and OpenSSH and evaluates security and
performance consequences.

## Findings

- Fine-grained privilege separation prevented sensitive-data leakage scenarios
  that coarser separation did not.
- Default-deny compartments force otherwise hidden privilege dependencies into
  the design.
- Dynamic analysis can help discover required memory access, but observed
  executions do not prove a policy complete.

## Relevance

High-risk Layer 5 adapters and extensions should live in independently
supervised protected domains with narrow imports. Actor isolation and a
supervision subtree alone are not confidentiality or integrity boundaries.

## Limits

Wedge targets Linux and C applications, focuses heavily on memory privilege,
and predates modern side channels. Its measured costs and partitioning tools
do not transfer to BEAM-compatible Atom OS domains.

## Derived work

- [Extension points, plugins, and live-tooling confinement](../20-notes/applications-and-domain-services-components/extension-points-plugins-and-live-tooling-confinement.md)
- [Cross-layer placement, tenancy, overload, and recovery topology](../20-notes/applications-and-domain-services-components/cross-layer-placement-tenancy-overload-and-recovery-topology.md)
