---
title: "What evidence would change the kernel language choice?"
kind: inquiry
created: "2026-09-08"
status: open
tags: [zig, c-language, kernel-language, language-comparison]
aliases: []
---

# What evidence would change the kernel language choice?

## Why this matters

The user selected Zig and subsequently requested a comparative recommendation.
The [comparison](../20-notes/proof-of-concept-requirements/zig-versus-c-kernel-language-comparison.md)
supports retaining Zig conditionally, not defending it regardless of evidence.

## Operational question

What demonstrated toolchain, interface, maintenance, assurance or workload
constraint would make C preferable for the same kernel architecture?

## Working hypotheses

- Zig's integrated error/cleanup idioms are useful for a small newly written
  kernel if its exact implementation profile can be qualified.
- C is preferable when independent compiler substitution, a required supported
  proof workflow or extensive actual C reuse dominates.
- Generic language benchmarks and unequal tiny fixtures cannot decide this
  project's execution or delivery tradeoffs.

## Paths to explore

1. Establish actual team ownership, debugging workflow and maintenance limits.
2. Use the existing [Zig](can-zig-meet-the-kernel-qualification-contract.md) and
   [C](can-c-meet-the-kernel-qualification-contract.md) qualification inquiries
   for compiler/ABI/boot evidence; do not duplicate whole implementations.
3. Minimize any required Zig failure, assess a bounded wrapper or assembly
   workaround, then compare a C alternative under the same contract.
4. If a proof tool or extensive donor subsystem becomes required, inspect its
   exact supported subset and environment before changing the language.
5. Measure equivalent workloads only when a performance/resource gap could
   change the decision.

## Findings

The [session](../50-journal/2026-09-08-zig-versus-c-kernel-language-deep-dive.md)
found a meaningful tradeoff between integrated source-level idioms and
established C tooling/assurance. Existing probes do not rank safety, speed,
binary size, debugging quality or schedule.

## Outcome

Open as a decision-monitoring inquiry, not an automation or extra milestone.
No present decisive blocker requires a primary-language switch. Revisit when
a stated assumption fails or concrete evidence crosses the comparison's
decision conditions. Any change remains an explicit user decision.
