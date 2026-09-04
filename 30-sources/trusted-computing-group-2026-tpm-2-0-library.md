---
title: "Trusted Platform Module 2.0 Library specification"
kind: source
created: "2026-09-04"
authors:
  - "Trusted Computing Group"
published: 2026
citation_key: "trusted-computing-group-2026-tpm-2-0-library"
container: "Trusted Computing Group specification"
edition: "Version 185"
isbn: null
doi: null
url: "https://trustedcomputinggroup.org/resource/tpm-library-specification/"
accessed: "2026-09-04"
tags:
  - hardware-root-of-trust
  - key-protection
  - measured-boot
  - tpm
aliases:
  - "TPM 2.0 Library version 185"
---

# Trusted Platform Module 2.0 Library specification

## Reference

Trusted Computing Group. “[Trusted Platform Module 2.0 Library
Specification](https://trustedcomputinggroup.org/resource/tpm-library-specification/).”
Version 185, Parts 0–3, March 2026. The
[Part 1 architecture](https://trustedcomputinggroup.org/wp-content/uploads/Trusted-Platform-Module-2.0-Library-Part-1-Architecture_Version-185_pub.pdf)
was reviewed with the release index.

## Research question or contribution

The TPM library specifies protected objects, cryptographic operations,
authorization sessions, platform measurements, key policies, and persistent or
volatile state exposed by a TPM 2.0 implementation.

## Method

This is a normative family of command and data-structure specifications. The
architecture and current release index were used to bound which properties an
OS may request from a TPM; no certification or attack-resistance claim is
inferred for an unspecified implementation.

## Findings

- TPM objects can keep private key material behind protected operations rather
  than requiring the OS to export raw keys.
- Platform configuration registers and quote operations support measured-boot
  evidence whose interpretation depends on event logs, reference values,
  freshness, and verifier policy.
- Authorization policies can bind object use to measurements, locality,
  commands, counters, or multiple factors, but policy-session complexity is
  itself part of the trusted design.
- NV state and counters can help detect rollback, subject to endurance,
  provisioning, ownership, and platform-profile constraints.

## Relevance

The Atom OS hardware profile should expose a narrow root-of-trust service:
non-exportable key handles, fresh quote requests, measured-boot registers,
rollback-resistant epochs where available, and device entropy. A confined
system service—not the kernel—should parse TPM wire structures, manage
endorsements, and decide whether evidence satisfies policy.

## Limits

The specification is not evidence that every TPM, firmware stack, event log,
provisioning process, or endorsement chain is trustworthy. A discrete TPM does
not observe all execution, prevent runtime compromise, provide application
authorization, or guarantee resistance to physical and side-channel attack.
Its large protocol surface should not be imported wholesale into the kernel.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
