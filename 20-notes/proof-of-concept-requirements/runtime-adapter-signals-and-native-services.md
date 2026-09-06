---
title: "Runtime adapter, signals, and native services"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Runtime adapter, signals, and native services

Requirement R09, M3. The managed runtime owns BEAM execution and actor semantics in user space; the kernel owns protection, bounded transport and domain resources. The adapter must connect these without importing an undeclared host operating system.

## Evidence and alternatives

The [OTP runtime reference](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) documents per-sender signal ordering, native-code failure exposure and cooperative yielding. Dirty scheduling changes execution placement, not a native function's memory-isolation boundary.

[Winblad's signal-sending article](../../30-sources/winblad-2021-parallel-signal-sending.md) describes optimizing concurrent ingress while retaining receiver-side signal handling. Its multicore workload results do not establish this single-CPU interpreter's mailbox capacity or fairness.

Proceed with a small project interpreter, copied messages and one managed scheduler thread initially. A broader ERTS port remains an architectural alternative in historical research, but it is not a prerequisite or comparison milestone here. AtomVM is excluded.

## Proposed substrate inventory

List every external call used by the hosted interpreter, its purpose, its guest replacement and its failure behavior. Cover allocation/free, mapping, clocks, waiting, threads, synchronization, entropy, image access, logging, termination and native extension loading. Inspect linked symbols as well as handwritten imports: compiler helpers and libraries can add dependencies.

In the guest, allocate only from assigned pages and finite runtime accounts. Read time through the declared monotonic interface. Receive events through bounded kernel transport. Load only the static BEAM bundle at first. Disable unimplemented filesystem, socket, dynamic-library and host-thread paths explicitly.

Hosted execution is valuable for differential semantics and fuzzing. It does not validate Atom's scheduler, memory protection or IPC, even when the same interpreter sources compile for both environments.

## Signals, continuations and completion

Assign actor identities independently of kernel-domain handles. Maintain ordering required for signals from one sender to one receiver without promising a total order across senders. Distinguish signal arrival/handling from selective-receive choice. If priority-message features are admitted, model their mailbox placement separately instead of assuming simple FIFO covers the entire contract.

An actor requesting a native service records a continuation and operation identity, submits a bounded request, and becomes waiting. The runtime remains runnable for other actors. Completions carry the actor/request and service generation; stale or duplicate results cannot attach to a replacement actor or domain.

Finite OTP calls need the actual alias/monitor semantics used by [the selected generic-call path](../../30-sources/erlang-otp-team-2026-otp-29-0-6-generic-behaviour-call-protocol.md). Closing a wait must retire reply delivery authority without erasing a server effect that may already have occurred.

Specify reduction charging and safe points for dispatch, BIFs, message copying, mailbox scanning and adapter work. Long native loops either become resumable, receive a strict admitted bound, or move to a separately protected service. Kernel preemption alone does not make the managed scheduler fair.

## Native service boundary

Place the test echo/counter or optional narrow UART service in another user domain. Marshal finite copied values; never accept arbitrary runtime pointers from it. Its crash should produce a defined request outcome and recovery event, not corrupt the interpreter heap.

Validate service responses even when the service is project code. Grant only its own endpoint and necessary device access. No DMA device belongs in the first containment claim. A native function linked into the runtime remains inside its failure boundary regardless of its API name.

## Acceptance and next exploration

Run actor A waiting on a permanently stalled native service while actor B allocates, exchanges messages and advances a heartbeat. Then crash the native domain, inject a late old-generation reply and restart it. Separately crash the whole runtime and verify outer recovery, not an internal actor supervisor, replaces it.

Audit every guest substrate call and exercise unavailable-service, full-queue and allocation-failure paths. Retain ordering tests with multiple senders and timeout/reply races.

The next artifact is the import/replacement table and asynchronous adapter state machine. No runtime adapter or native-containment experiment was implemented during this session.

## Connections

[Compatibility closure](beam-profile-loader-and-conformance.md), [IPC](capabilities-syscalls-and-bounded-ipc.md) and [independent recovery](supervision-and-independent-recovery.md) define the interfaces.
