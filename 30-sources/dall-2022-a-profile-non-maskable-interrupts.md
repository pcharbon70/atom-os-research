---
title: "A-profile non-maskable interrupts"
kind: source
created: "2026-09-08"
authors:
  - "Christoffer Dall"
published: "2022-05-23"
citation_key: "dall-2022-a-profile-non-maskable-interrupts"
container: "Arm Community"
edition: null
isbn: null
doi: null
url: "https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-profile-non-maskable-interrupts"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# A-profile non-maskable interrupts

## Reference

Christoffer Dall. [A-profile non-maskable interrupts](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-profile-non-maskable-interrupts). Arm Community, 2022-05-23. Accessed 2026-09-08.

## Research question or contribution

How Arm's A-profile NMI extension changes interrupt masking and exception handling.

## Method

First-party engineering article explaining FEAT_NMI and related mask/stack controls.

## Findings

NMI handling has feature-specific mask and acknowledgement behavior. ALLINT and SPINTMASK address conditions not captured by ordinary interrupt-mask reasoning, including fragile stack-state transitions.

## Relevance

Specify nested-event admission and emergency-state handling by architecture profile, not by the word NMI alone.

## Limits

The article is explanatory rather than a complete normative specification. Non-maskable does not mean immune to every architectural mask, overwritten exception state or corrupted software dependency.

## Derived work

- [Early vector and stack admission](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/early-vector-stack-admission.md) — architecture synthesis constrained by this source.
- [Nested-event and terminal handoff](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/nested-event-and-terminal-handoff.md) — architecture synthesis constrained by this source.
