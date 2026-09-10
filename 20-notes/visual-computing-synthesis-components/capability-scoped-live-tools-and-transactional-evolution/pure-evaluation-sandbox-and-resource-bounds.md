---
title: "Pure-evaluation sandbox and resource bounds"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - live-programming
  - sandboxing
  - visual-computing
aliases: []
---

# Pure-evaluation sandbox and resource bounds

This study decomposes [Capability-scoped live tools and transactional evolution](../capability-scoped-live-tools-and-transactional-evolution.md).

Research question: How can exploratory evaluation provide immediate feedback
without ambient effects, hidden nondeterminism, or unbounded resource use?

## Research basis and status

Smalltalk workspaces motivate immediate evaluation, while liveness research
distinguishes several forms and outcomes of live feedback. WASI design
principles provide a current capability-import precedent for making external
facilities explicit.
[1](../../../30-sources/goldberg-1984-smalltalk-80-interactive-environment.md)
[2](../../../30-sources/rein-et-al-2019-liveness-literature-study.md)
[3](../../../30-sources/wasi-project-2026-design-principles.md)

No Atom evaluator, language subset, or determinism profile exists.

## Development

### Owned state and trust boundary

An evaluation service owns immutable input values, language/compiler digest,
declared pure libraries, reduction/heap/depth/time/result budgets, seed if
randomness is explicitly modeled, and output provenance. The default sandbox
has no clock, entropy, I/O, spawning, message send, native call, secret, or
commit facet.

### Admission, transitions, and completion

Parse and compile in isolated workers under separate budgets, validate imports
and bytecode/native helpers, then execute against copied values. Completion
returns a typed value or explicit parse, policy, resource, cancellation, or
worker-failure outcome tied to the evaluator generation.

### Failure and adversarial behavior

Compiler bugs, exponential types, recursion, decompression, huge results,
covert timing, and unsafe native helpers can cross the boundary. Independent
process/domain isolation, verifier rules, output caps, deterministic
scheduling, and destroying workers after risky compilation constrain the
profile.

### Alternatives and unresolved tradeoffs

Evaluating inside the target preserves identity but lets exploratory code
destabilize it. A hosted general-purpose shell is familiar but inherits host
authority. A restricted evaluator with explicit imports is preferred; which
language and BEAM/Zig interoperability profile remains a separate decision.

## Verification obligations

- Exhaust parser, compiler, reductions, heap, recursion, wall budget, result
  size, and cancellation paths while targets and recovery remain responsive.
- Attempt every ambient effect and covert imported capability through values,
  exceptions, callbacks, and native helpers.
- Replay the same admitted evaluation under the declared deterministic profile
  and compare canonical results and resource evidence.

## Connections

- [Internal-service index](README.md) — live-tool separation.
- [Inspection facets](inspection-facets-redaction-and-copied-state.md) — input snapshots.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence boundary.

## Sources

1. [Smalltalk-80 interactive environment](../../../30-sources/goldberg-1984-smalltalk-80-interactive-environment.md).
2. [Liveness literature study](../../../30-sources/rein-et-al-2019-liveness-literature-study.md).
3. [WASI design principles](../../../30-sources/wasi-project-2026-design-principles.md).
