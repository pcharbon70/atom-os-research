---
title: "Timecounters: Efficient and precise timekeeping in SMP kernels"
kind: source
created: "2026-09-02"
authors:
  - "Poul-Henning Kamp"
published: 2002
citation_key: "kamp-2002-timecounters"
container: "EuroBSDCon 2002"
edition: null
isbn: null
doi: null
url: "https://phk.freebsd.dk/pubs/timecounter.pdf"
accessed: "2026-09-02"
tags:
  - concurrency
  - operating-systems
  - timekeeping
aliases:
  - "FreeBSD timecounters paper"
---

# Timecounters: Efficient and precise timekeeping in SMP kernels

## Reference

Poul-Henning Kamp. “Timecounters: Efficient and Precise Timekeeping in SMP
Kernels.” *EuroBSDCon 2002*, Amsterdam, 2002.
[Author-hosted paper](https://phk.freebsd.dk/pubs/timecounter.pdf).

## Research question or contribution

How can a multiprocessor kernel turn varied wrapping hardware counters into a
precise, architecture-independent timescale while keeping the dominant read
path lock-free?

## Method

The paper explains the mathematical representation and then-current FreeBSD
implementation of timecounters. It derives counter-to-time scaling, describes
periodic anchoring before hardware wrap creates ambiguity, and presents a
generation-checked ring of immutable-enough “timehands” snapshots for readers.
It is primarily a design and implementation report, not a comparative
benchmark study.

## Findings

- A hardware source can be described by a read operation, frequency, and valid
  bit mask. Its wrapping delta can be converted into a canonical binary
  timescale without exposing hardware units to callers.
- Counter width and frequency jointly determine the maximum safe interval
  between software updates. A narrow counter cannot be extended correctly if
  software may miss enough wraps to make the delta ambiguous.
- Time reads greatly outnumber changes to conversion or synchronization state.
  The design therefore publishes matching anchor-count, anchor-time, scale,
  mask, and source fields as a generation-checked snapshot instead of taking a
  global lock on each read.
- A reader samples the generation before and after conversion and retries if
  the snapshot was being updated or recycled. Old snapshots remain usable
  briefly, which tolerates preemption in the read path.
- Publishing the counter source inside the same snapshot permits a live source
  switch without combining a count from one source with conversion state from
  another.
- The paper separates the raw counter-based timeline from later real-time
  discipline. Frequency correction changes conversion state; it does not turn
  a hardware counter into civil time by itself.

## Relevance

The proposed raw-time component should use one generation-published conversion
snapshot containing source identity, mask, anchor count, anchor monotonic time,
and fixed-point conversion parameters. Its validity interval must be derived
from counter width and frequency, and a source switch must preserve continuity
in one publication transaction. The technique is precedent for a fast
read-mostly path, not a reason to copy FreeBSD structures verbatim.

## Limits

The paper predates modern invariant architectural counters, deep power states,
common virtualization, heterogeneous CPU packages, and contemporary timing
side-channel concerns. It does not specify one-shot deadline cancellation,
cross-CPU skew qualification, suspend semantics, or a hard real-time latency
bound. A new implementation needs its own language-memory-model proof and
target-specific counter validation.

## Derived work

- [Raw time and deadline programming](../20-notes/raw-time-and-deadline-programming.md)
