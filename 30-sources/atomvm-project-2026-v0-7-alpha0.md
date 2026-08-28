---
title: "Announcing AtomVM v0.7.0-alpha.0"
kind: source
created: "2026-08-28"
authors:
  - "The AtomVM team"
published: "2026-03-20"
citation_key: "atomvm-team-2026-v070-alpha0"
container: "AtomVM news"
edition: null
isbn: null
doi: null
url: "https://atomvm.org/2026/03/20/Announcing-AtomVM-v0.7.0-alpha0.html"
accessed: "2026-08-28"
tags:
  - atom-vm
  - beam
  - project-status
  - release-notes
aliases:
  - "AtomVM v0.7 alpha announcement"
---

# Announcing AtomVM v0.7.0-alpha.0

## Reference

The AtomVM team. "[Announcing AtomVM
v0.7.0-alpha.0](https://atomvm.org/2026/03/20/Announcing-AtomVM-v0.7.0-alpha0.html)."
*AtomVM*, 2026-03-20. Accessed 2026-08-28.

## Contribution

The official project post summarizes the first v0.7 prerelease after more than
two years of development and states the intended stability boundary between
the prerelease and v0.6.x.

## Method

The announcement was read as a project-status source and checked against the
release list, `CHANGELOG.md`, development documentation, and pinned source
tree. It was not treated as independent performance evidence.

## Findings

- The team calls v0.7.0-alpha.0 an alpha whose APIs may still evolve and
  recommends v0.6.x for production deployments needing maximum stability.
- Headline additions include Erlang distribution, four execution strategies
  (emulated, JIT, native/AOT, hybrid), 256-bit integers, crypto, limited ETS,
  expanded MCU support, and native Elixir `GenServer`/`Supervisor` support.
- The post identifies breaking changes from v0.6, including the `init:boot/1`
  entry point, native ports replacing pids, overflow behavior, and a renamed C
  API.
- Prebuilt images cover numerous ESP32 variants, Pico/Pico 2 variants, and
  WebAssembly, while custom builds remain necessary for STM32.

## Relevance

The announcement establishes that papers using pre-v0.7 AtomVM cannot serve as
current feature inventories. It also shows the project is broadening from a
small interpreter toward a richer runtime, while explicitly retaining an
unstable prerelease boundary.

## Limits

This is an official release announcement, not an independent evaluation. It
summarizes availability but does not establish completeness, timing, memory
cost, fault containment, or production suitability. The inspected `main`
revision is later and identifies itself as `0.8.0-dev`.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [2026-08-28 source audit](../50-journal/2026-08-28-atomvm-deep-dive.md)
