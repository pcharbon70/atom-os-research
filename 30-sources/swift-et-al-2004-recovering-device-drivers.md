---
title: "Recovering device drivers"
kind: source
created: "2026-08-31"
authors:
  - "Michael M. Swift"
  - "Muthukaruppan Annamalai"
  - "Brian N. Bershad"
  - "Henry M. Levy"
published: 2004
citation_key: "swift-et-al-2004-recovering-device-drivers"
container: "6th Symposium on Operating Systems Design and Implementation"
edition: null
isbn: "1-931971-16-0"
doi: null
url: "https://www.usenix.org/conference/osdi-04/recovering-device-drivers"
accessed: "2026-08-31"
tags:
  - device-drivers
  - fault-containment
  - operating-systems
  - recovery
aliases:
  - "Shadow drivers"
---

# Recovering device drivers

## Reference

Michael M. Swift, Muthukaruppan Annamalai, Brian N. Bershad, and Henry M.
Levy. “Recovering Device Drivers.” *OSDI '04*, pages 1–16, 2004.
[USENIX record and paper](https://www.usenix.org/conference/osdi-04/recovering-device-drivers).

## Research question or contribution

Can applications continue through a driver failure when simple driver restart
would otherwise discard device and client state?

## Method

Shadow drivers observe kernel-driver traffic, preserve selected recovery state,
temporarily impersonate a failed driver, and replay initialization to a
replacement. The prototype covers more than a dozen Linux drivers and evaluates
recovery behavior and overhead.

## Findings

- Recovery metadata and control must reside outside the driver being recovered.
- A replacement needs device-class-specific state reconstruction and protocol,
  not only a fresh address space.
- Some operations can be concealed or retried, while device and application
  semantics determine whether replay is safe.
- If failure occurs after a device accepted an operation but before completion
  became observable, the result may be unknowable. Retrying can duplicate an
  external effect; suppressing retry can lose it.

## Relevance

Kernel call cancellation must report `not-executed`, `completed`, or
`indeterminate` when that status is knowable. It must never manufacture
exactly-once semantics from endpoint delivery. Driver teardown also needs a
device-specific quiescence protocol above the generic capability revocation
mechanism.

## Limits

The mechanism is Linux- and driver-class-specific and trusts the shadow and
kernel. It does not solve malicious hardware, arbitrary state corruption,
irreversible output, or the reset semantics of every device. Transparent
recovery is an evaluated possibility for selected drivers, not a universal
kernel contract.

## Derived work

- [Native work, ports, and drivers](../20-notes/managed-actor-runtime-components/native-work-ports-and-drivers.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
