---
title: "Domain lifecycle and safe reclamation"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Domain lifecycle and safe reclamation

Requirement R07, M2–M4. Domain restart must reclaim safe resources without admitting new work into an object being dismantled or redirecting stale work to its replacement.

## Evidence and its limits

[Read-copy update](../../30-sources/mckenney-slingwine-1998-read-copy-update.md) separates removal from reclamation after earlier readers become quiescent. This is a useful lifecycle principle, not a complete domain-destruction algorithm: software-reader quiescence does not establish device, translation or timer completion.

[Kernel timing analysis](../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) shows why deletion and lazy cleanup deserve explicit bounded-work analysis. The [x86 system-programming study](../../30-sources/intel-2026-system-programming-documentation.md) supplies translation-invalidation context. The [T7500 / Intel x86-64 profile](dell-precision-t7500-target-and-minimal-qemu-profile.md) requires qualifying the exact Intel local invalidation sequence for the installed Xeon and integrating it into address-space reuse; a RISC-V fence is not the current backend.

The first profile is single-CPU and has no untrusted bus-mastering device. That removes remote shootdown and DMA obligations from this test envelope, not interrupt races or local stale translations.

## Proposed lifecycle state machine

Use explicit states such as constructing, live, closing, draining, reclaimable and dead. These are proposed implementation names, not existing kernel behavior.

Construction reserves all indispensable objects and publishes no externally callable endpoint until initialization succeeds. A failed construction unwinds staged ownership without invoking a partially initialized child.

Closing first disables new invocation, capability derivation and resource acquisition. Only then begin a bounded cleanup walk. Existing operations retain identities and defined terminal dispositions. Make close idempotent and safe to resume after an interrupt or recovery-service retry.

Stop execution and prevent return into the old domain. Retire its timers, close endpoints, dispose of outstanding completions, and detach namespace entries. Distinguish logical cancellation from callbacks that may already be queued.

Before reusing pages, establish that execution cannot access them, local translations are appropriately invalidated, and kernel references or queued callbacks cannot reach old contents. Zero pages before exposing them to a different protection domain. Retiring an address-space identifier does not automatically flush every relevant cached mapping.

Only after these obligations hold may accounting transfer ownership to the free pool. A new service generation is published after its replacement is fully initialized. Handle validation includes generation; neither a recycled slot nor a familiar service name restores old authority.

## Bounded cleanup and resource conservation

Choose a maximum number of objects or references processed per cleanup step. Charge cleanup CPU and memory to a reserve that survives the child. A child may have exhausted its own budget and pages before it dies.

Record each resource as free, owned, reserved for an in-flight operation, or quarantined. These categories must sum to configured capacity without double counting. A bounded quarantine is an explicit non-reuse state with a release condition and exhaustion policy; it is not a mechanism for restarting indefinitely while leaking pages.

Specify generation-wrap and reference-counter overflow handling. Use small identifier widths in a test build to force wrap paths that ordinary campaigns would never reach.

## Acceptance and next exploration

Model close racing with admission, timer expiry, reply, capability revocation and a second close. Check that no transition publishes new work after close's admission barrier and that every reclamation transition has its required quiescence evidence.

In the guest, repeat 1,000 child-domain restart cycles with fixed capacity. Verify post-recovery free/owned/quarantined counts, not only successful new launches. Inject faults during construction and between cleanup steps; deliberately retain stale handles and delayed completions.

A failing cleanup may escalate under a documented policy, but it must not silently reuse uncertain memory. Later DMA and SMP work must extend the state machine before enabling those features.

The next artifact is the executable lifecycle model and a fake page/timer/endpoint backend. No model-checking or restart evidence exists from this reading session.

## Connections

[IPC terminal states](capabilities-syscalls-and-bounded-ipc.md), [recovery reserves](supervision-and-independent-recovery.md), and the later [DMA](dma-driver-isolation-and-recovery.md) and [multicore](multicore-and-platform-portability.md) studies define the surrounding obligations.
