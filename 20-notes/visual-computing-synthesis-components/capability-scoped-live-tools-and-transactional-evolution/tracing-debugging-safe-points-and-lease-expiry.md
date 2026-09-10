---
title: "Tracing, debugging, safe points, and lease expiry"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - debugging
  - live-programming
  - observability
aliases: []
---

# Tracing, debugging, safe points, and lease expiry

This study decomposes [Capability-scoped live tools and transactional evolution](../capability-scoped-live-tools-and-transactional-evolution.md).

Research question: How can tracing and interactive control observe a live
system without permanent suspension, unbounded perturbation, or secret
disclosure?

## Research basis and status

DTrace demonstrates verified typed probes, aggregation, and per-consumer
budgets. Live-programming studies show exploratory value but do not erase the
remote-object problem. OTP tracing research in the corpus establishes that
observation has scheduling, mailbox, and disclosure cost.
[1](../../../30-sources/cantrill-et-al-2004-dtrace.md)
[2](../../../30-sources/rein-et-al-2017-living-in-programming-environment.md)

The Atom trace/debug contract and safe-point semantics remain unimplemented.

## Development

### Owned state and trust boundary

Trace authority names probes, fields, targets, audience, sampling, rate,
duration, and disclosure. Debug-control authority separately names pause, step,
inspect, and resume rights. A recovery holder outside the tool owns lease
expiry and forced resume/termination policy.

### Admission, transitions, and completion

Attach validates target/code generations and reserves buffer plus perturbation
budgets. Trace delivery is lossy only when marked with per-consumer loss
counters. Pause occurs at declared runtime safe points, records stopped
resources, and begins an independent deadline. Detach or expiry removes probes
and proves target disposition.

### Failure and adversarial behavior

Probe storms, recursive tracing, full-mailbox capture, dead target locks,
debugger crash, and secrets in arguments can destabilize or disclose the
system. Verifier rules, aggregation, per-target budgets, redaction, nonblocking
delivery, and externally enforced lease cleanup are mandatory.

### Alternatives and unresolved tradeoffs

Always-on full event logs improve replay but are costly and privacy-sensitive.
Stop-the-world debugging simplifies consistency but violates responsiveness.
Typed bounded probes plus selective safe-point control are preferred; required
deterministic replay scope remains open.

## Verification obligations

- Compare trace-off/on latency and scheduling, including dropped-event and
  aggregation evidence under maximum admitted load.
- Crash the debugger while every supported resource is stopped; the external
  lease holder must recover or terminate it by deadline.
- Attempt probe recursion, secret capture, target expansion, and buffer
  exhaustion with weaker trace facets.

## Connections

- [Internal-service index](README.md) — live diagnosis scope.
- [Observability system services](../../otp-like-system-services-components/observability-audit-alarms-and-operator-control/README.md) — audit and evidence custody.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — limitations.

## Sources

1. [DTrace](../../../30-sources/cantrill-et-al-2004-dtrace.md).
2. [Living in a programming environment](../../../30-sources/rein-et-al-2017-living-in-programming-environment.md).
