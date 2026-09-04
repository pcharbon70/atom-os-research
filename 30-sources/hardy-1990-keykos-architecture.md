---
title: "The KeyKOS architecture"
kind: source
created: "2026-09-04"
authors:
  - "Norman Hardy"
published: 1990
citation_key: "hardy-1990-keykos-architecture"
container: "Key Logic technical paper; earlier form in Operating Systems Review"
edition: "Eighth edition"
isbn: null
doi: null
url: "https://pdos.csail.mit.edu/6.828/2010/readings/keykos-osr.pdf"
accessed: "2026-09-04"
tags:
  - capabilities
  - command-line-interface
  - operating-systems
  - resource-accounting
aliases:
  - "KeyKOS architecture"
---

# The KeyKOS architecture

## Reference

Norman Hardy. “[The KeyKOS Architecture](https://pdos.csail.mit.edu/6.828/2010/readings/keykos-osr.pdf).”
Eighth edition, December 1990; an earlier form appeared in *Operating Systems
Review* in September 1985.

## Research question or contribution

The paper describes a persistent capability operating system in which opaque
keys combine object designation with permitted operations and most policy,
administration, command, and resource-allocation facilities live outside a
small kernel.

## Method

This is an implementation architecture and practitioner account of KeyKOS,
including domains, key invocation and transfer, space banks, meters, keepers,
persistence, and command-system composition.

## Findings

- Domains receive no implicit address-space, CPU-meter, keeper, or service
  authority; these powers arrive through explicit keys.
- Hierarchical space banks and meters make storage and computation authority
  delegable and accountable.
- The command system is an unprivileged domain. Programs receive explicit
  directory or object keys instead of inheriting all authority held by an
  operator shell.
- Recovery and administrative functions can be implemented as ordinary
  capability-confined services rather than a kernel superuser.

## Relevance

This is direct precedent for placing the Atom OS CLI at the application layer.
The shell should hold a session namespace and command-launch authority, while
each command receives a newly constructed, attenuated capability set and
budget. Administrative work should create a separate, short-lived, audited
session after step-up authentication rather than mutate a process-wide UID.

## Limits

KeyKOS targeted historical mainframe hardware and has different performance,
persistence, I/O, multicore, and network assumptions. Its architecture is
evidence of feasibility, not a proof that every KeyKOS mechanism fits Atom OS
or satisfies modern side-channel and usability requirements.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
