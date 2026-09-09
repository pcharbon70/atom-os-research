---
title: "NAPI"
kind: source
created: "2026-09-08"
authors:
  - "Linux kernel development community"
published: null
citation_key: "linux-kernel-community-2026-napi-contracts"
container: "The Linux Kernel documentation"
edition: null
isbn: null
doi: null
url: "https://docs.kernel.org/networking/napi.html"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# NAPI

## Reference

Linux kernel development community. [NAPI](https://docs.kernel.org/networking/napi.html). The Linux Kernel documentation; publication date not stated. Accessed 2026-09-08.

## Research question or contribution

How interrupt notification and budgeted network polling coordinate ownership and completion.

## Method

Official API documentation; reviewed scheduling, budget, completion, masking and teardown rules.

## Findings

Ownership must be acquired consistently with masking. Completing polling releases ownership, which is not identical to the poll function returning. Exact-budget work and a zero budget require special treatment.

## Relevance

Model masking, notification, budget exhaustion and ownership transfer explicitly rather than treating them as one Boolean enabled state.

## Limits

The network-specific contract is a precedent, not a general interrupt-controller specification or proof of the proposed event fabric. It supplies no universal optimum for polling versus interrupts.

## Derived work

- [Polling and interrupt handoff](../20-notes/kernel-hardware-and-architecture-components/interrupt-event-fabric/polling-and-interrupt-handoff.md) — architecture synthesis constrained by this source.
