---
title: "Platform Firmware Resiliency Guidelines"
kind: source
created: "2026-08-29"
authors:
  - "Andrew Regenscheid"
published: 2018
citation_key: "regenscheid-2018-platform-firmware-resiliency"
container: "NIST Special Publication 800-193"
edition: null
isbn: null
doi: "10.6028/NIST.SP.800-193"
url: "https://csrc.nist.gov/pubs/sp/800/193/final"
accessed: "2026-08-29"
tags:
  - boot
  - firmware
  - recovery
  - security
  - updates
aliases:
  - "NIST SP 800-193"
---

# Platform Firmware Resiliency Guidelines

## Reference

Andrew Regenscheid. *Platform Firmware Resiliency Guidelines*. NIST Special
Publication 800-193, May 2018. DOI
[10.6028/NIST.SP.800-193](https://doi.org/10.6028/NIST.SP.800-193).
[NIST publication page](https://csrc.nist.gov/pubs/sp/800/193/final).

## Research question or contribution

What security properties must a platform provide so destructive or persistent
firmware modification can be prevented, detected, and recovered?

## Method

The publication defines platform firmware, roots of trust, authenticated
update, integrity detection, recovery, protected storage, and management
requirements as technical guidance rather than reporting an OS experiment.

## Findings

- Resilience has three distinct jobs: protect against unauthorized change,
  detect change that occurs, and recover securely. Image signature checking
  covers only part of that lifecycle.
- Recovery code and data need protection independent of the mutable image they
  repair, and update must address interruption and rollback.
- Platform firmware sits below the OS and can render it inoperable regardless
  of runtime supervision. The boot chain therefore needs its own failure and
  evidence model.
- The guidance separates platform and software while requiring coordinated
  update and recovery policy across the boundary.

## Relevance

The hardware layer should preserve verified/measured boot evidence, immutable
recovery entry, image generations, reset reasons, and a minimal crash/update
store. OTP-style restarts begin only after these machine-level mechanisms
succeed.

## Limits

This is general guidance, not a complete protocol, proof, bootloader, or
hardware implementation. It does not prescribe one TPM, UEFI, SBI, or flash
layout and predates some current platform standards.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
