---
title: "Private heaps and tracing garbage collection"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Private heaps and tracing garbage collection

Requirement R10, M3–M4. Long-lived BEAM processes must reclaim unreachable terms automatically through process-local tracing GC outside the privileged kernel. Process exit reclamation or explicit user frees cannot substitute for this requirement.

## Evidence and the latency distinction

The [OTP GC reference](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) describes private generational copying heaps and separately managed binary/literal storage. These are useful implementation precedents, not a requirement to copy ERTS's exact collector.

[Sagonas and Wilhelmsson](../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md) study private heaps combined with a shared message area and incremental work. Their timing results depend on the chosen collector region, scheduling policy and historical workloads; they do not establish a pause bound for every private-heap collection in a new interpreter.

Choose a simple precise copying collector first. Incremental or generational refinements are alternatives to evaluate against a measured envelope, not prerequisites for the first correct tracing implementation. An incremental collector adds barriers, resumable state and progress obligations that deserve separate conformance tests.

## Proposed heap and root contract

Describe the term representation and all roots before implementing collection: live registers, stacks, exception state, saved continuations, mailboxes or message fragments, dictionary/state objects, timer payloads and native-adapter references. A root map must agree with compiler/interpreter safe points.

Reserve destination space and required metadata before destructive forwarding changes the source heap. Bound live-data growth and temporary copying space. If reservation fails before collection, apply the declared resource policy; failure after destructive mutation must not resume a corrupted process.

Forward each reachable object exactly once and preserve sharing, cycles if the admitted representation permits them, and binary/sub-binary references. Distinguish managed terms from unboxed values and opaque capability handles. Native code may not retain movable pointers across a collection without an explicit rooting or stable-handle mechanism.

Private heap collection must not silently reclaim objects still referenced from an admitted message or pending native request. Conversely, retired aliases, timers and continuations must stop retaining terms when their semantic lifetime ends.

## Shared and global storage

Start with copied messages to simplify ownership. If large binaries use shared backing, define reference acquisition/release, charging and sub-binary retention. A tiny view retaining a large backing allocation must remain visible in the resource ledger.

Code, literals and atoms may outlive an actor heap. State their release rules and limits rather than attributing them to a leak in the local collector or excluding them from memory accounting. A heap plateau can coexist with unbounded global retention.

Collector work runs in the runtime's user domain. Kernel budgets can protect recovery from a long collection, but actors on the same scheduler can still wait for the collector to finish. Measure those two delays separately.

## Acceptance and workload envelope

Use a long-lived actor with a fixed reachable set and at least one million transient allocations as a proposed campaign input. Force collection at varied safe points. Verify live term contents, identity/sharing where observable, message contents and binary lifetimes after repeated movement.

Sweep live heap, allocation rate, mailbox backlog, binary size and CPU budget. Record allocation totals, live bytes, peak reserved bytes, post-collection bytes, GC duration and same-runtime heartbeat delay. Include empty heaps, nearly full destination space, failure before reservation and actor death during pending adapter work.

A bounded post-collection steady state under a fixed live set demonstrates reclamation for that workload; it is not a proof of leak freedom across all term forms. Predeclare acceptable p99 and maximum-observed pauses for the admitted workload.

The next artifact is the root/term specification plus a hosted moving-GC stress harness. Introduce incremental collection only if measured results fail the declared envelope, then retest its new barriers and progress conditions.

## Connections

[Accounting](resource-accounting-and-mailbox-overload.md) pays for copying space and globals. [Compatibility](beam-profile-loader-and-conformance.md) supplies observable term semantics. [Time](time-preemption-and-cpu-budgets.md) separates actor and domain responsiveness.
