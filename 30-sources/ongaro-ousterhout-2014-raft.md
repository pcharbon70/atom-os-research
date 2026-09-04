---
title: "In search of an understandable consensus algorithm"
kind: source
created: "2026-09-03"
authors:
  - "Diego Ongaro"
  - "John Ousterhout"
published: 2014
citation_key: "ongaro-ousterhout-2014-raft"
container: "2014 USENIX Annual Technical Conference"
edition: "USENIX ATC '14, 305–319"
isbn: "978-1-931971-10-2"
doi: null
url: "https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro"
accessed: "2026-09-03"
tags:
  - consensus
  - distributed-systems
  - replication
aliases:
  - "Raft paper"
---

# In search of an understandable consensus algorithm

## Reference

Diego Ongaro and John Ousterhout. “[In Search of an Understandable Consensus
Algorithm](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro).”
*USENIX ATC '14*, pages 305–319. [Open-access
paper](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf).

## Research question or contribution

Can replicated-log consensus be decomposed into a complete practical
algorithm whose states, safety argument, leader election, replication, and
membership changes are easier to understand than common Paxos descriptions?

## Method

The paper constructs Raft around a strong leader, randomized election timeouts,
log-matching rules, and term numbers. It states safety properties, describes
normal and recovery behavior, proposes overlapping-majority membership
changes, and evaluates understandability with a 43-student comparison.

## Findings

- A deterministic state machine applied to the same committed command order on
  every replica can provide one replicated service state.
- Terms and log indices reject stale Raft leaders and constrain obsolete
  protocol messages and conflicting log histories. They do not by themselves
  deduplicate client operations. Safety does not rely on message timing;
  availability does rely on an operational, mutually communicating majority.
- The paper assumes non-Byzantine stop failures and stable storage for term,
  vote, and log state. A five-member cluster can normally tolerate two stopped
  members, not arbitrary corruption.
- Joint consensus overlaps old and new majorities during membership change so
  two disjoint configurations cannot both decide independently.
- Consensus orders commands; it does not by itself define client identity,
  authorization, failure detection, service naming, external-effect fencing,
  or application semantics.

## Relevance

A small Atom OS coordination service can use a Raft-class replicated log for
authoritative service publications, release decisions, and lease generations
that must survive node loss. It should not put bulk storage, telemetry, or all
actor traffic through consensus. Membership suspicion remains a separate input,
and external resources still require fencing tokens.

## Limits

The conference paper omits some client-interaction and log-compaction detail
available in the extended report. Its user study measures comprehension, not
implementation correctness. Real systems still need snapshots, storage-error
handling, transport security, admission control, reconfiguration tooling, and
systematic fault tests.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
