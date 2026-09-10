---
title: "Project manifest, object identity, and history"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - persistence
  - project-graph
  - visual-computing
aliases: []
---

# Project manifest, object identity, and history

This study decomposes [User-owned project graph and composition](../user-owned-project-graph-and-composition.md).

Research question: What durable record preserves project meaning without
persisting live actor, surface, or capability identity?

## Research basis and status

Persistent programming supports typed reachability from explicit roots, while
the Dexter model separates durable components and links from run-time
presentation. FSCQ demonstrates that crash guarantees require a precise
persistent-state specification rather than a successful-looking reopen.
[1](../../../30-sources/atkinson-et-al-1983-persistent-programming.md)
[2](../../../30-sources/halasz-schwartz-1994-dexter-hypertext-reference-model.md)
[3](../../../30-sources/chen-et-al-2015-fscq.md)

The design below is an Atom OS proposal. No project format, recovery proof, or
long-lived migration corpus has been implemented.

## Development

### Owned state and trust boundary

The manifest service owns project identity, root object IDs, schema generation,
history head, retention policy, provider requirements, and content revisions.
Object lifecycle generation distinguishes deletion/recreation; state revision
orders mutations within one lifecycle. Actor PIDs, memory addresses, surface
IDs, focus tokens, and bearer capabilities are forbidden durable fields.

### Admission, transitions, and completion

Open first validates framing and bounded schema, then resolves immutable object
records from a committed manifest revision. Mutation binds one operation ID to
expected revisions and a typed change before journal admission. Completion
publishes a new history head atomically or returns durable evidence that the
named change did not commit; timeout alone is not failure evidence.

### Failure and adversarial behavior

Malformed graphs can amplify traversal, recursive schemas, or retention cost.
Reused object IDs can redirect stale commands, and partial history publication
can make two roots disagree. Bounds apply before allocation; lifecycle and
manifest revisions are checked at every sink; recovery exposes corruption or
indeterminacy rather than silently selecting a plausible branch.

### Alternatives and unresolved tradeoffs

A single image snapshot simplifies closure but couples all objects, authority,
and recovery. Independent files improve tooling but weaken graph-atomic change.
An append-only history preserves provenance but needs compaction, erasure, and
schema-expiry policy. The initial chunking and checkpoint cadence remain open.

## Verification obligations

These are unexecuted falsifiers:

- Crash before and after every manifest, object, edge, and history publication
  and prove the recovered graph equals one declared committed prefix.
- Reuse actor, surface, and storage addresses after restart; no stale record may
  resolve to a new logical object.
- Fuzz cyclic, oversized, incompatible, and partially missing graphs under
  fixed memory and traversal budgets.

Evidence must name the format version, tested revision, crash model, admitted
bounds, raw history, and recovery result.

## Connections

- [Internal-service index](README.md) — sibling project responsibilities.
- [Durable semantic actors](../durable-semantic-actors-and-disposable-presentation/README.md) — materializes durable identities through replaceable activations.
- [Open visual-computing inquiry](../../../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md) — retains portability and recovery gates.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — sources and limitations.

## Sources

1. [An approach to persistent programming](../../../30-sources/atkinson-et-al-1983-persistent-programming.md).
2. [The Dexter hypertext reference model](../../../30-sources/halasz-schwartz-1994-dexter-hypertext-reference-model.md).
3. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
