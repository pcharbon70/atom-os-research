---
title: "Thread Progress"
kind: source
created: "2026-09-09"
authors:
  - "Erlang/OTP contributors"
published: null
citation_key: "erlang-otp-team-2026-thread-progress-contracts"
container: "Erlang/OTP ERTS internal documentation"
edition: "Rendered OTP 29.0.6 / ERTS 17.0.6 on access"
isbn: null
doi: null
url: "https://www.erlang.org/doc/apps/erts/threadprogress.html"
accessed: "2026-09-09"
tags:
  - beam
  - managed-runtime
  - concurrency
aliases: []
---

# Thread Progress

## Reference

Erlang/OTP contributors. [Thread Progress](https://www.erlang.org/doc/apps/erts/threadprogress.html). Erlang/OTP ERTS internal documentation.
Publication date not established.
Accessed 2026-09-09.

## Research question or contribution

What does a runtime grace-period observation actually establish?

## Method

Read problems, managed/unmanaged participants, progress events, API and implementation. The page identifies OTP 29.0.6; this does not update the separate OTP 29.0.5 static audit.

## Findings

Managed participants report return to a known state and memory-ordering progress. Unmanaged threads can explicitly delay completion. Per-thread confirmation and a leader reduce shared communication. A future progress token requires more than observing the next global counter value.

## Relevance

Keep a generation-qualified participant set and tracked native leases. Removing code from an index does not immediately permit freeing it; neither does software progress establish DMA quiescence or remote instruction-fetch completion. Worker withdrawal must reconcile participation before resources are returned.

## Limits

The guide is implementation precedent, not verification of Atom OS. A stalled participant can retain resources. No progress algorithm, weak-memory model or worker-lifecycle test was executed.

## Derived work

- [Service study](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication/logical-purge-fun-invalidation-and-literal-reclamation.md).
- [Managed-runtime map](../10-maps/managed-actor-runtime.md).
- [Introducing research session](../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md).
