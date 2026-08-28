---
title: "What's on your mind for AtomVM v0.7?"
kind: source
created: "2026-08-28"
authors:
  - "Davide Bettio"
  - "AtomVM community participants"
published: "2025-12-17"
citation_key: "atomvm-discussion-2040"
container: "GitHub Discussions"
edition: "Discussion 2040"
isbn: null
doi: null
url: "https://github.com/atomvm/AtomVM/discussions/2040"
accessed: "2026-08-28"
tags:
  - atom-vm
  - community-discussion
  - embedded-systems
  - project-status
aliases:
  - "AtomVM v0.7 priorities discussion"
---

# What's on your mind for AtomVM v0.7?

## Reference

Bettio, Davide, and AtomVM community participants. "[What's on your mind for
AtomVM v0.7?](https://github.com/atomvm/AtomVM/discussions/2040)" AtomVM GitHub
Discussion 2040, opened 2025-12-17. Accessed 2026-08-28.

## Contribution

The project creator asked users and collaborators what should be improved
before a stable v0.7. The replies provide a dated view of practitioner and
maintainer priorities around performance, tooling, compatibility, peripherals,
power, and flash organization.

## Method

The complete visible discussion was read and its linked work was compared with
the v0.7 alpha release notes and the inspected main changelog. The thread was
used as community evidence, not as a systematic survey or current feature
matrix.

## Findings

- One participant singled out function-call overhead as painful enough to need
  significant reduction.
- Collaborators prioritized ESP32/Pico tooling, Wi-Fi scan and reconnect
  behavior, Elixir `gen_server`/supervisor work, consistent GPIO errors, and
  ESP32 light-sleep support.
- A collaborator proposed a more flexible ESP32 partition layout so NVS could
  survive image flashing, be resized or removed, and leave more flash for
  applications and libraries.
- Several linked supervisor and networking items later landed in v0.7
  prereleases or current main. The thread records pressure and sequencing, not
  necessarily remaining gaps.

## Relevance

The concerns align closely with an OS foundation's difficult edges: call and
driver overhead, deployment tools, network lifecycle, consistent device APIs,
power management, and durable flash layout. They also show that a clean VM
core is insufficient without operational tooling and hardware policy.

## Limits

The participants are self-selected, the thread is small, and requests vary in
specificity. Comments were made before later v0.7 work, and some are now
obsolete. No claim here establishes prevalence, performance impact, or release
completion without separate source or experimental evidence.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [Kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
- [2026-08-28 source audit](../50-journal/2026-08-28-atomvm-deep-dive.md)
