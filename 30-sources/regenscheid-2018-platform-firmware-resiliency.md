---
title: "Platform firmware resiliency guidelines"
kind: source
created: "2026-09-04"
authors:
  - "Andrew Regenscheid"
published: 2018
citation_key: "regenscheid-2018-platform-firmware-resiliency"
container: "NIST Special Publication 800-193"
edition: null
isbn: null
doi: "10.6028/NIST.SP.800-193"
url: "https://csrc.nist.gov/pubs/sp/800/193/final"
accessed: "2026-09-04"
tags:
  - firmware
  - recovery
  - roots-of-trust
  - security
aliases:
  - "NIST SP 800-193"
---

# Platform firmware resiliency guidelines

## Reference

Andrew Regenscheid. “[Platform Firmware Resiliency
Guidelines](https://doi.org/10.6028/NIST.SP.800-193).” NIST Special Publication
800-193, May 2018.

## Research question or contribution

The publication gives technical guidance for protecting platform firmware and
critical data from unauthorized changes, detecting corruption, and recovering
rapidly and securely after destructive attacks.

## Method

This is government technical guidance. It defines roots/chains of trust for
protection, detection, and recovery and derives requirements for update,
integrity checking, authenticated recovery images, rollback protection, and
event reporting.

## Findings

- Firmware resiliency requires protection, detection, and recovery capabilities
  rooted below software that an attacker may have compromised.
- Recovery images and recovery actions must themselves be authenticated and
  protected from unauthorized modification or rollback.
- Roots of trust and critical data need independent protection and controlled
  update paths.
- Platform recovery differs from restoring an application account or data key.

## Relevance

Atom's Layer-4 recovery coordinator can request and report platform recovery,
but it cannot be the sole recovery root when the OS may be compromised. The
hardware/firmware/boot layers must authenticate a narrowly selected recovery
image and protect rollback state independently.

## Limits

The document is broad platform guidance, not a protocol, implementation, formal
proof, or account-recovery design. Concrete guarantees depend on OEM hardware,
firmware, provisioning, and physical-threat assumptions.

## Derived work

- [Recovery coordinator](../20-notes/authentication-and-authorization-components/recovery-coordinator.md)
- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
