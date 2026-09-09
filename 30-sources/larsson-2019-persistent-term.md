---
title: "Clever use of persistent_term"
kind: source
created: "2026-09-09"
authors:
  - "Lukas Larsson"
published: "2019-09-09"
citation_key: "larsson-2019-persistent-term"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/persistent_term/"
accessed: "2026-09-09"
tags:
  - beam
  - managed-runtime
  - concurrency
aliases: []
---

# Clever use of persistent_term

## Reference

Lukas Larsson. [Clever use of persistent_term](https://www.erlang.org/blog/persistent_term/). Erlang/OTP Blog.
Published 2019-09-09.
Accessed 2026-09-09.

## Research question or contribution

Where does read-mostly global term storage move its cost?

## Method

Read the first-party article's global-counter and Logger examples and its replacement warning. Treat the examples as OTP 22-era engineering evidence, not current performance qualification.

## Findings

Literal-style access avoids copies and reference-count updates in the examples. Replacing or deleting retained values can trigger expensive runtime-wide reclamation work. Stable counters and infrequently changed read-mostly configuration benefit under the author's tested conditions.

## Relevance

Make persistent terms, counter references and pending generations explicit global resources. Process-local tracing does not eliminate cross-process work caused by retiring shared immutable values. Research should compare read cost with replacement tails and retained memory rather than extrapolating from a hot-path microbenchmark.

## Limits

The article is not a formal lifetime specification or a universal performance result. Reported percentages are not adopted as Atom OS targets. No replacement stress test or reproduction was performed.

## Derived work

- [Service study](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control/persistent-terms-and-shared-counter-lifecycle.md).
- [Managed-runtime map](../10-maps/managed-actor-runtime.md).
- [Introducing research session](../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md).
