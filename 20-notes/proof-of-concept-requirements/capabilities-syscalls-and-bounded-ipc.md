---
title: "Capabilities, syscalls, and bounded IPC"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Capabilities, syscalls, and bounded IPC

Requirement R06, M2. Establish a finite authority and transport vocabulary before expanding services. The contract must describe accepted work, denied work, outstanding effects and who can reclaim every reservation.

## Evidence and design choice

The [seL4 reference manual](../../30-sources/sel4-foundation-2026-reference-manual.md) gives concrete capability, object-memory, endpoint and notification mechanisms. [Shapiro's IPC analysis](../../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md) explains how blocking replies, buffer allocation and client-controlled faults can compromise otherwise isolated servers.

These sources motivate bounded admission and explicit funding. They do not imply that adopting synchronous invocation automatically produces a safe asynchronous actor substrate.

Use server-funded leaf services initially. Defer nested synchronous call chains and scheduling-context donation. This reduces the state space but requires a runtime completion adapter and a capacity policy for servers that are slower than callers.

## Proposed version-zero object and operation table

Start with domains/address spaces, finite capability slots, page and CPU accounts, bounded endpoint requests, notifications, timer events and fault records. Shared rings are optional later optimizations, not prerequisites for copied fixed-size requests.

For each syscall or service operation, freeze:

- the required capability type and rights;
- the object, endpoint and service generation;
- the account paying for request storage, reply storage, CPU and failure reporting;
- the admission/linearization point and all preconditions;
- the finite maximum payload and copy/validation work;
- the terminal result and the condition permitting slot and identifier reuse.

An initial invocation reserves its request record and completion capacity before becoming visible to a server. Reject admission when those resources are unavailable. A client that never collects replies cannot force unlimited retained kernel records. Define bounded disposal and notification semantics.

Capabilities are checked handles into kernel-controlled tables, not caller-supplied object addresses. Validate every operation even when a handle was valid earlier. Separate revocation of future admission from already admitted work; revocation is not retrospective undo.

Assign each admitted operation a stable identity including the relevant generation. A replacement service receives a new generation and cannot inherit old completion authority accidentally. Define wrap behavior: retire an exhausted identifier namespace or refuse new allocation instead of assuming wrap never happens.

## Completion, cancellation and actor adaptation

Reply, timeout, cancellation and peer death race to select one terminal transport disposition. Test the linearization explicitly. A timeout after server acceptance means the effect can be unknown, even if the reply slot has closed. Exactly one terminal transport result is not exactly-once application execution.

A runtime scheduler must never synchronously wait inside the kernel on behalf of one actor while unrelated runnable actors exist. Submit a bounded request, park that actor's continuation, and collect completion through a pollable queue/notification. If the chosen kernel call blocks its calling thread, introduce a separately funded adapter execution context or redesign the invocation primitive; do not hide a blocking dependency in a thin wrapper.

Notifications signal possible work and may coalesce. Receivers drain a bounded amount, recheck state and reschedule. A count of notifications is not a count of completed operations.

## Acceptance and remaining decisions

Build a fake backend that delays, duplicates and reorders completions. Exercise revocation immediately before and after admission, caller death, server death, full request/reply pools, stale capability guesses, malformed buffers, cancelled timers and generation reuse.

Check that every accepted record has one owner, one funded terminal path, and no route to an unrelated replacement. The CLI should remain responsive while a native service stalls. Set explicit maximum work per syscall; finite tables alone do not make scanning them acceptably bounded.

The next artifact is the operation table plus executable transition tests. Wire encodings, capacities and linearization points remain unselected.

## Connections

[Lifecycle](domain-lifecycle-and-safe-reclamation.md) handles retained references after close. [Runtime adaptation](runtime-adapter-signals-and-native-services.md) preserves actor semantics. [Accounting](resource-accounting-and-mailbox-overload.md) makes finite admission enforceable.
