---
title: "Dynamic instrumentation of production systems"
kind: source
created: "2026-09-03"
authors:
  - "Bryan M. Cantrill"
  - "Michael W. Shapiro"
  - "Adam H. Leventhal"
published: 2004
citation_key: "cantrill-et-al-2004-dtrace"
container: "2004 USENIX Annual Technical Conference"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/2004-usenix-annual-technical-conference/dynamic-instrumentation-production-systems"
accessed: "2026-09-03"
tags:
  - diagnostics
  - dynamic-tracing
  - observability
  - operating-systems
aliases:
  - "DTrace paper"
---

# Dynamic instrumentation of production systems

## Reference

Bryan M. Cantrill, Michael W. Shapiro, and Adam H. Leventhal. “Dynamic
Instrumentation of Production Systems.” *2004 USENIX Annual Technical
Conference*, Boston, 2004.
[USENIX publication record and paper](https://www.usenix.org/conference/2004-usenix-annual-technical-conference/dynamic-instrumentation-production-systems).

## Research question or contribution

Can an operating system expose broad, dynamically selected observability on
production systems without allowing tracing programs to compromise the kernel
and without paying an ongoing probe cost while instrumentation is disabled?
The paper presents DTrace and its probe, provider, consumer, aggregation, and
safe in-kernel execution model.

## Method

The authors describe the architecture and safety mechanisms, report the scale
of available instrumentation, and give production debugging cases that could
not be resolved with existing tools. The evaluation is an engineering case
study rather than a formal noninterference proof or a bounded worst-case
execution-time analysis.

## Findings

- Disabled probes are designed to have no probe effect, while enabled probes
  can span kernel and user software through one model.
- A constrained, validated tracing language permits predicates, actions,
  thread-local state, associative arrays, aggregation, and speculation without
  admitting arbitrary kernel code.
- Per-consumer state and destructive-action controls help separate tracing
  consumers and their privileges.
- In-kernel aggregation can reduce data volume and post-processing, an
  important response to high event rates.
- Production cases show the value of correlating events across subsystem
  boundaries rather than exposing only isolated counters.

## Relevance

The minimal kernel should preserve DTrace's lessons about typed probe sites,
safe programs, per-consumer state, and aggregation, but expose a far smaller
baseline. Every observation right must be a capability with explicit target,
field, rate, and lifetime limits. Disabled sites should collapse to a static
branch or patchable no-op, while enabled work is charged and bounded.

## Limits

DTrace's breadth and programmable language are not automatically compatible
with a small verifiable kernel or hard latency bounds. Its safety claims do not
make trace values non-sensitive, prevent timing channels, or prove that a
crash record survives a failed kernel. Dynamic tracing is therefore distinct
from the preallocated terminal crash capsule and from ordinary unprivileged
runtime telemetry. Atom OS must evaluate probe overhead, buffer-loss semantics,
redaction, and authority composition on its own implementation.

## Derived work

- [Observability and crash evidence](../20-notes/minimal-privileged-kernel-components/observability-and-crash-evidence.md)
- [Fault capture and containment](../20-notes/minimal-privileged-kernel-components/fault-capture-and-containment.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
