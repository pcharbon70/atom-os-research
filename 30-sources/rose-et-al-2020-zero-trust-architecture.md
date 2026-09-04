---
title: "Zero trust architecture"
kind: source
created: "2026-09-04"
authors:
  - "Scott Rose"
  - "Oliver Borchert"
  - "Stu Mitchell"
  - "Sean Connelly"
published: 2020
citation_key: "rose-et-al-2020-zero-trust-architecture"
container: "NIST Special Publication 800-207"
edition: null
isbn: null
doi: "10.6028/NIST.SP.800-207"
url: "https://csrc.nist.gov/pubs/sp/800/207/final"
accessed: "2026-09-04"
tags:
  - authorization
  - network-security
  - zero-trust
aliases:
  - "NIST SP 800-207"
---

# Zero trust architecture

## Reference

Scott Rose, Oliver Borchert, Stu Mitchell, and Sean Connelly. “[Zero Trust
Architecture](https://doi.org/10.6028/NIST.SP.800-207).” NIST Special
Publication 800-207, August 2020.

## Research question or contribution

The publication defines zero-trust principles and conceptual deployment models
for making resource-access decisions without granting implicit trust from
network location, ownership, or prior presence inside a perimeter.

## Method

This is architectural guidance and a migration model, not a protocol
specification, implementation proof, or product benchmark.

## Findings

- Resources, not network segments, are the primary protection focus.
- Subject and device authentication and authorization are distinct decisions
  made before a session to a protected resource is established.
- A policy decision point and policy enforcement point have different duties;
  enforcement must sit on the actual access path.
- Trust is evaluated from explicit identity, device, resource, policy, and
  contextual evidence rather than inferred from internal network placement.
- Continuous or repeated evaluation requires inventory, telemetry, policy, and
  lifecycle support; “zero trust” is not synonymous with adding mutual TLS.

## Relevance

Atom OS should apply the principle below the network: no process, actor, user,
service, driver, node, recovery path, or debug tool gains authority merely by
being local, booted, named, supervised, or authenticated. The policy plane can
evaluate changing evidence, while resource services and the kernel remain the
enforcement points for bounded capabilities and generation fences.

## Limits

The document is enterprise-network guidance. Its logical components do not
select a microkernel capability representation, solve distributed consistency,
define a trusted human path, or prove that continuous re-evaluation is complete
or race-free. Atom OS must translate the principles rather than copy the
enterprise reference diagrams.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
