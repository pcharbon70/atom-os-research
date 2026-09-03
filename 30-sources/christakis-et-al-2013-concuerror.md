---
title: "Systematic testing for detecting concurrency errors in Erlang programs"
kind: source
created: "2026-09-03"
authors:
  - "Maria Christakis"
  - "Alkis Gotovos"
  - "Konstantinos Sagonas"
published: 2013
citation_key: "christakis-et-al-2013-concuerror"
container: "2013 IEEE Sixth International Conference on Software Testing, Verification and Validation"
edition: null
isbn: null
doi: "10.1109/ICST.2013.50"
url: "https://doi.org/10.1109/ICST.2013.50"
accessed: "2026-09-03"
tags:
  - concurrency-testing
  - erlang
  - model-checking
  - reproducibility
aliases:
  - "Concuerror"
---

# Systematic testing for detecting concurrency errors in Erlang programs

## Reference

Maria Christakis, Alkis Gotovos, and Konstantinos Sagonas. “[Systematic Testing
for Detecting Concurrency Errors in Erlang
Programs](https://doi.org/10.1109/ICST.2013.50).” *2013 IEEE Sixth
International Conference on Software Testing, Verification and Validation*,
2013. [Author-hosted
paper](https://people.csail.mit.edu/alkisg/files/christakis13systematic.pdf).

## Research question or contribution

The paper presents Concuerror, a stateless model-checking tool that reuses
ordinary Erlang tests while systematically exploring actor interleavings and
reporting replayable histories for failures.

## Method

Concuerror instruments selected concurrency operations, controls scheduling,
and explores process interleavings from a test entry point. The paper explains
the actor-specific instrumentation and search strategy and evaluates the tool
on Erlang programs with abnormal exits, assertion failures, and stuck-process
states in which all live processes are blocked and which may indicate a
deadlock.

## Findings

- Repeated execution under an ordinary scheduler may repeat similar schedules
  and miss feasible races; controlled interleaving exploration finds and
  reproduces classes of faults more reliably.
- Stateless search avoids snapshotting complete runtime state, but still faces
  state-space explosion and depends on which operations are visible to the
  scheduler.
- A useful failure report contains the scheduling/interleaving history, not
  only the terminal assertion or exit.
- Instrumented actor scheduling does not control native threads, external
  systems, wall time, hardware faults, or opaque side effects.

## Relevance

The result supports a deterministic Atom OS runtime mode whose choice points
include runnable-actor selection, message visibility, timer delivery, failure
delivery, and selected external completions. The runtime should store a seed
and compact choice schedule and expose it to shrinking and differential tests.
Production scheduling remains separate.

## Limits

Concuerror tests executions reachable through its model and instrumentation;
it is not a proof of arbitrary Erlang programs. Search pruning and unsupported
side effects can omit behaviors. Atom OS must combine actor-level exploration
with kernel model tests, native-service fault injection, network simulation,
and hardware/emulator tests.

## Derived work

- [Observability, deterministic testing, and crash evidence](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
