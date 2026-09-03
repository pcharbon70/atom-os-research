---
title: "Crash-only software"
kind: source
created: "2026-09-03"
authors:
  - "George Candea"
  - "Armando Fox"
published: 2003
citation_key: "candea-fox-2003-crash-only-software"
container: "9th Workshop on Hot Topics in Operating Systems"
edition: "HotOS IX"
isbn: null
doi: null
url: "https://radlab.cs.berkeley.edu/people/fox/static/pubs/pdf/c22.pdf"
accessed: "2026-09-03"
tags:
  - fault-containment
  - recovery
  - restart
  - state-management
aliases:
  - "Crash-only design"
---

# Crash-only software

## Reference

George Candea and Armando Fox. “[Crash-Only
Software](https://radlab.cs.berkeley.edu/people/fox/static/pubs/pdf/c22.pdf).”
*9th Workshop on Hot Topics in Operating Systems*, 2003.

## Research question or contribution

The position paper asks whether software becomes more predictable when graceful
shutdown and crash recovery are unified: components stop safely by failing and
start through one recovery path, so restart is exercised during normal
operation rather than reserved for emergencies.

## Method

The authors synthesize system-design practices into crash-only component rules
and discuss how idempotent or retryable requests, externally managed state,
leases, timeouts, and fine-grained restart can mask component failures.

## Findings

- One well-tested startup/recovery path can reduce the difference between
  planned and unplanned restart.
- Fast fine-grained restart depends on explicit component boundaries and on
  persistent or authoritative state living outside the failed volatile
  component.
- Timeouts, leases, retries, and self-describing requests help release stale
  state, but retries are safe only when operation semantics permit them.
- “Crash-only” does not mean data loss is harmless. Irreversible external
  actions, corrupt durable state, deterministic bugs, dependency cycles, and
  restart storms remain.

## Relevance

The argument reinforces a strict Atom OS boundary: actors may be restarted by
OTP policy, but corruption of the runtime requires an outer service to replace
the entire runtime incarnation. Bootstrap and teardown should converge on the
same idempotent object-creation and release protocol, and gateways must reject
stale incarnations. Crash evidence and ambiguous requests must survive outside
the component that failed.

## Limits

This short paper is primarily an architectural argument, not a controlled
evaluation or formal recovery proof. Later microreboot work supplies empirical
evidence for one application class. Neither work demonstrates transparent
recovery for arbitrary actors, devices, distributed transactions, or corrupted
runtime memory.

## Derived work

- [Failure translation and the OTP boundary](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary.md)
- [Runtime-domain bootstrap and kernel adapter](../20-notes/managed-actor-runtime-components/runtime-domain-bootstrap-and-kernel-adapter.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
