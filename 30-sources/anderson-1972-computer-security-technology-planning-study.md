---
title: "Computer security technology planning study, Volume II"
kind: source
created: "2026-09-04"
authors:
  - "James P. Anderson"
published: 1972
citation_key: "anderson-1972-computer-security-technology-planning-study"
container: "Electronic Systems Division, Air Force Systems Command"
edition: "ESD-TR-73-51, Volume II"
isbn: null
doi: null
url: "https://csrc.nist.gov/files/pubs/conference/1998/10/08/proceedings-of-the-21st-nissc-1998/final/docs/early-cs-papers/ande72.pdf"
accessed: "2026-09-04"
tags:
  - assurance
  - reference-monitor
  - security-kernel
aliases:
  - "Anderson report"
---

# Computer security technology planning study, Volume II

## Reference

James P. Anderson. “[Computer Security Technology Planning Study, Volume
II](https://csrc.nist.gov/files/pubs/conference/1998/10/08/proceedings-of-the-21st-nissc-1998/final/docs/early-cs-papers/ande72.pdf).”
ESD-TR-73-51, Volume II, Electronic Systems Division, Air Force Systems
Command, October 1972.

## Research question or contribution

The report develops a research and engineering program for secure multi-user
computing and articulates the reference-validation mechanism later summarized
as the reference-monitor concept.

## Method

This is a planning study and architectural analysis informed by early secure
systems, not a modern implementation evaluation.

## Findings

- A reference-validation mechanism must mediate relevant references to data,
  programs, and peripherals.
- To serve as a security foundation, the mechanism must always be invoked,
  resist tampering, and remain small enough for analysis, testing, or proof.
- Containment and mediation are mechanism; initial authorization, physical
  protection, communication security, and complete policy remain separate
  concerns.

## Relevance

Atom OS should make the privileged kernel a small reference monitor for
capabilities, domains, memory, IPC, CPU budgets, interrupts, and devices. It
should not move password parsing, federation, relationship policy, recovery
decisions, or audit retention into privilege merely because those functions
are security-sensitive.

## Limits

The terminology and threat setting are historical, and “always invoked” does
not itself identify every modern path through DMA, speculative state, firmware,
distributed caches, or trusted UI. Smallness is necessary for assurance but is
not a proof of correctness.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
