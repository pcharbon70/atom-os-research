---
title: "Collaboration, replica membership, and conflict"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - collaborative-computing
  - distributed-systems
  - project-graph
aliases: []
---

# Collaboration, replica membership, and conflict

This study decomposes [User-owned project graph and composition](../user-owned-project-graph-and-composition.md).

Research question: Which project state may converge automatically, and which
membership, ownership, invariant, or effect decisions require serialized
authority?

## Research basis and status

CRDT research defines convergence conditions, JSON CRDTs show structured
replication, and collaborative-editor work demonstrates that access control
does not emerge from convergence. Local-first research supplies offline
ownership goals while preserving open access and history problems.
[1](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md)
[2](../../../30-sources/kleppmann-beresford-2017-conflict-free-json.md)
[3](../../../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md)
[4](../../../30-sources/kleppmann-et-al-2019-local-first-software.md)

No Atom OS replication profile has been modeled or tested.

## Development

### Owned state and trust boundary

Each object type declares merge algebra, fenced single-writer ownership, or an
explicit conflict representation. A separate authority log owns membership,
roles, revocation epochs, and effect rights. Replica metadata can describe
causality but cannot grant a collaborator access.

### Admission, transitions, and completion

Local edits record principal, object generation, causal context, schema, and
merge policy. Synchronization authenticates peers, filters object streams, and
validates current membership before publication. Noncommutative edits produce
a durable conflict object; external commands retain one operation ID and are
not replayed because a replica merged.

### Failure and adversarial behavior

Offline removal, replayed membership records, malicious timestamps, semantic
invariant violations, and convergent-but-surprising operations are expected.
Authority epochs fence late publication; type validators run after merge; and
conflicts remain visible rather than silently applying last-writer-wins.

### Alternatives and unresolved tradeoffs

Central serialization simplifies effects and membership but weakens offline
availability. Universal CRDTs maximize convergence but cannot supply domain
intent or authorization. Per-type policies are preferred; long-offline
retention and conflict-GC rules remain open.

## Verification obligations

- Revoke a collaborator offline, merge later content, and prove membership and
  effect authority are not reinstated.
- Generate concurrent edits that converge structurally but violate a domain
  invariant; expose conflict or reject publication.
- Lose network replies around an effect and prove replicas reconcile the same
  operation rather than execute it twice.

## Connections

- [Internal-service index](README.md) — project ownership and history.
- [Remote collaborative views](../plural-representations-and-cross-view-consistency/remote-collaborative-views-convergence-privacy-and-revocation.md) — presentation-specific replication.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Conflict-free replicated data types](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md).
2. [Conflict-free replicated JSON](../../../30-sources/kleppmann-beresford-2017-conflict-free-json.md).
3. [Access control for collaborative editors](../../../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md).
4. [Local-first software](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).
