---
title: "Atom OS Research"
kind: map
created: "2026-08-28"
tags:
  - atom-vm
  - operating-systems
aliases:
  - "Home"
---

# Atom OS Research

This is the selective entry point to research on using `atom-vm` as the
foundation of a new operating system. See the [archive guide](../README.md) for
the repository structure and working conventions.

## Research objective

Determine which operating-system responsibilities can live in, beneath, or
alongside `atom-vm`, and establish a credible path from the existing runtime to
a bootable system whose core execution model is the VM itself.

## Active inquiries

- [Can AtomVM serve as the kernel-facing runtime of a new embedded operating
  system?](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md) —
  defines the boot, substrate, resource, fault, trust, and lifecycle evidence
  required to demonstrate the foundational-runtime hypothesis.

## Topic maps

- [AtomVM foundation](atomvm-foundation.md) — routes through the current
  architecture, source audit, measurements, community priorities, and open OS
  questions.

## Recently developed

- [AtomVM as an operating-system
  foundation](../20-notes/atomvm-as-an-operating-system-foundation.md) —
  concludes that AtomVM is a plausible execution nucleus for a trusted,
  single-purpose embedded OS, but not yet a complete kernel or protected
  multi-tenant boundary.
- [2026-08-28 AtomVM deep
  dive](../50-journal/2026-08-28-atomvm-deep-dive.md) — records the pinned
  revision, source and literature search, commands, and local build limitation.

## Unsettled threads

- Extract a complete substrate contract from `sys.h`, `smp.h`, startup, libc,
  allocator, interrupt, entropy, flash, watchdog, and vendor-SDK dependencies.
- Choose between an explicitly trusted single-tenant appliance and a larger
  MPU/PMP-backed capability design.
- Reproduce mailbox, scheduler, memory, native-driver, and whole-node failure
  behavior on a pinned current revision.
- Demonstrate boot, secure update/rollback, persistence, and retained
  diagnostics before treating the result as an operating-system foundation.
