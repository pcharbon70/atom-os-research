---
title: "Protection"
kind: source
created: "2026-09-04"
authors:
  - "Butler W. Lampson"
published: 1971
citation_key: "lampson-1971-protection"
container: "Proceedings of the 5th Princeton Conference on Information Sciences and Systems"
edition: "Reprinted in ACM Operating Systems Review 8(1), 1974"
isbn: null
doi: null
url: "https://bwlampson.site/08-Protection/WebPage.html"
accessed: "2026-09-04"
tags:
  - access-control
  - operating-systems
  - protection
aliases:
  - "Lampson protection model"
---

# Protection

## Reference

Butler W. Lampson. “[Protection](https://bwlampson.site/08-Protection/WebPage.html).”
*Proceedings of the 5th Princeton Conference on Information Sciences and
Systems*, 1971; reprinted in *ACM Operating Systems Review* 8(1), pages 18–24,
January 1974.

## Research question or contribution

The paper gives abstract models for protection domains, objects, rights, and
the changing protection state of a computer system. It separates the general
question “which subject may perform which operation on which object?” from one
particular ACL, capability, file, or supervisor-mode implementation.

## Method

This is a conceptual and comparative model derived from contemporary systems,
not a security proof or empirical evaluation.

## Findings

- A protection context determines the powers available to a program; different
  programs as well as different users require different contexts.
- The access matrix is a useful abstract protection state whose rows associate
  authority with domains and whose columns associate authority with objects.
- Protection must cover destruction, disclosure, and degradation of service;
  CPU and storage exhaustion are therefore authorization concerns, not merely
  performance concerns.
- The model exposes authority creation, copying, and removal as state-changing
  operations that themselves require control.

## Relevance

Atom OS should represent protection state explicitly while refusing to make a
user name, BEAM PID, service name, or authenticated session equal to a row of
ambient power. Policy may reason in access-matrix terms, but the kernel should
install typed, object-specific capabilities in protected domains. CPU, memory,
queue, and recovery budgets belong in the same authority review as read, write,
invoke, or map rights.

## Limits

The work predates distributed authorization, modern cryptographic credentials,
multicore hardware, DMA, speculative execution, and contemporary usability
research. It describes protection-state structure but does not solve identity
proofing, policy consistency, revocation races, or trusted interaction.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
