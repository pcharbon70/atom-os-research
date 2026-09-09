---
title: "Learn the architecture — AArch64 Exception Model"
kind: source
created: "2026-09-08"
authors:
  - "Arm Limited"
published: 2025
citation_key: "arm-2025-aarch64-exception-model"
container: "Arm Learn the Architecture"
edition: "Version 1.3"
isbn: null
doi: null
url: "https://documentation-service.arm.com/static/67ac57fb091bfc3e0a9479cc"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# Learn the architecture — AArch64 Exception Model

## Reference

Arm Limited. [Learn the architecture — AArch64 Exception Model](https://documentation-service.arm.com/static/67ac57fb091bfc3e0a9479cc). Arm Learn the Architecture, 2025. Version 1.3. Accessed 2026-09-08.

## Research question or contribution

How exception entry and return relate to architectural state and software context preservation.

## Method

Official tutorial; reviewed chapter 5, especially pages 24–34, on exception capture, vectors and return.

## Findings

Hardware captures selected exception return/status information; software must preserve other context it needs. Vector entries contain instructions, and return correctness depends on the relevant saved architectural state.

## Relevance

Separate minimal hardware capture from generated software frames, stack admission and validated return.

## Limits

This tutorial is not the complete Arm Architecture Reference Manual or an exhaustive treatment of every optional extension. It does not establish a full context-switch or nested-fault proof.

## Derived work

- [Frame normalization and bounded dispatch](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/frame-normalization-and-dispatch.md) — architecture synthesis constrained by this source.
- [Validated less-privileged return](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/validated-user-return.md) — architecture synthesis constrained by this source.
