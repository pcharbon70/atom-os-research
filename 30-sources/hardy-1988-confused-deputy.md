---
title: "The confused deputy"
kind: source
created: "2026-09-04"
authors:
  - "Norm Hardy"
published: 1988
citation_key: "hardy-1988-confused-deputy"
container: "ACM SIGOPS Operating Systems Review 22(4), 36–38"
edition: null
isbn: null
doi: "10.1145/54289.871709"
url: "https://dl.acm.org/doi/10.1145/54289.871709"
accessed: "2026-09-04"
tags:
  - ambient-authority
  - capabilities
  - confused-deputy
aliases:
  - "Why capabilities might have been invented"
---

# The confused deputy

## Reference

Norm Hardy. “[The Confused Deputy: (or why capabilities might have been
invented)](https://doi.org/10.1145/54289.871709).” *ACM SIGOPS Operating
Systems Review* 22(4), pages 36–38, October 1988.

## Research question or contribution

The note explains how a program entrusted with its own authority can be induced
to exercise that authority for a caller when the request names a resource but
does not carry the authority intended for that use.

## Method

Hardy analyzes a compiler-like service that possesses both client-requested
output authority and unrelated accounting authority, then compares name-based
selection with capability-based designation.

## Findings

- Authentication of the caller does not tell a deputy which of the caller’s or
  deputy’s authorities should justify a particular effect.
- Ambient authority plus caller-controlled names lets a request redirect a
  deputy’s privilege toward an unintended object.
- Passing a capability for the intended object joins designation and authority,
  making the request’s authority provenance explicit.

## Relevance

Every Atom OS service API should receive the specific authority for the
requested effect or a tightly scoped grant from which that authority can be
derived. An authenticated principal, trace context, path, service name, PID, or
command string is context, not permission. The CLI and managed runtime must not
silently add their own broader capabilities to a caller’s request.

## Limits

The short note is an explanatory counterexample, not a full delegation,
revocation, distributed-token, or information-flow model. Capabilities still
need confinement, lifecycle, accounting, usable consent, and recovery rules.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
