---
title: "The Road to the JIT"
kind: source
created: "2026-08-28"
authors:
  - "Björn Gustavsson"
published: "2020-12-01"
citation_key: "gustavsson-2020-road-to-jit"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/the-road-to-the-jit/"
accessed: "2026-08-28"
tags:
  - beam
  - compiler-history
  - just-in-time-compilation
  - virtual-machines
aliases:
  - "Road to BeamAsm"
---

# The Road to the JIT

## Reference

Björn Gustavsson. “[The Road to the
JIT](https://www.erlang.org/blog/the-road-to-the-jit/).” Erlang/OTP Blog,
2020-12-01. Accessed 2026-08-28.

## Contribution

This official retrospective follows Erlang execution from the original Prolog
interpreter through JAM, TEAM, BEAM/C, interpreted BEAM, HiPE, tracing-JIT
experiments, and the BeamAsm design prepared for OTP 24.

## Method

The author combines project history with implementation explanations and
reported internal experience from successive Erlang systems. It is a
first-person engineering account rather than a controlled comparative study.

## Findings

- Early prototypes favored rapid language exploration; later abstract machines
  were introduced when the design needed production performance.
- Translating Erlang modules through C proved awkward because Erlang processes
  need their own managed stacks and control flow. Portability across C
  compilers and architectures also became costly.
- HiPE could substantially improve sequential code, but large Ericsson systems
  did not necessarily benefit because time was often dominated by messaging,
  ETS operations, garbage collection, and small cross-module calls.
- Several tracing-JIT projects struggled to avoid tracing overhead, expensive
  compilation, cold traces, and transitions between execution modes.
- BeamAsm took a simpler approach: translate all loaded BEAM instructions to
  native code, perform little optimization, preserve the BEAM stack and
  register model, and remove interpreter dispatch overhead without runtime hot
  tracing.
- Compatibility with tracing, scheduling behavior, hot loading, and diagnostic
  output constrained viable JIT designs. Execution speed was not the only
  requirement.

## Relevance

The history argues for keeping a portable execution model distinct from the
runtime services around it and for evaluating optimizations against whole
systems rather than sequential microbenchmarks alone. It also shows that
compiler/runtime choices are constrained by scheduling, code change,
observability, memory, and operational compatibility.

For a new OS, load-time lowering is an attractive middle ground between a
simple portable artifact and a complex adaptive optimizer. The larger lesson
is methodological: preserve the concurrency and failure semantics while
changing execution machinery, and test representative service workloads.

## Limits

The article is a retrospective by a central implementer and contains informal
recollections and internal results without complete benchmark artifacts. It
was written before the OTP 24 release, so current BeamAsm behavior must be
checked against current documentation and source. It does not compare kernel
architectures.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
