---
title: "Bidirectional projection, lens laws, and conflict rejection"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - bidirectional-transformation
  - data-consistency
  - visual-computing
aliases: []
---

# Bidirectional projection, lens laws, and conflict rejection

This study decomposes [Plural representations and cross-view consistency](../plural-representations-and-cross-view-consistency.md).

Research question: When may an edit to a projection update the model, and how
are ambiguity, hidden information, and invalid round trips rejected?

## Research basis and status

Bidirectional tree transformations formalize round-trip laws and complements.
Cambria provides a practitioner/research bridge for schema lenses and retained
original data. Collaborative-editing work separates convergence, causality, and
intention preservation.
[1](../../../30-sources/foster-et-al-2007-bidirectional-tree-transformations.md)
[2](../../../30-sources/litt-et-al-2020-cambria.md)
[3](../../../30-sources/sun-et-al-1998-cooperative-editing-consistency.md)

No Atom lens language, proof profile, or destructive-edit experiment exists.

## Development

### Owned state and trust boundary

A bidirectional provider owns source/view schemas, exact base versions,
get/put transformations, complements or retained hidden state, declared
lossiness, validation, conflict representation, and required mutation facet.
The domain model remains final authority over invariants and effects.

### Admission, transitions, and completion

Read derives a projection at one source revision. Edit validates the projection
and computes a proposed model patch against that exact base. Round-trip and
preservation checks run before domain admission. Ambiguous, stale, or
information-destroying changes return explicit conflict or require user
selection; they are not resolved by arbitrary overwrite.

### Failure and adversarial behavior

Edits can delete hidden data, reorder unrelated elements, exploit stale
complements, amplify authority through generated references, or violate domain
constraints despite lens laws. Property tests, capability filtering, exact
base checks, bounded transforms, and domain validation remain separate gates.

### Alternatives and unresolved tradeoffs

Read-only projections are safe but limit authorship. Handwritten imperative
synchronizers are flexible but hard to reason about. Law-checked lenses are
preferred only for suitable structures; complex semantic edits should use
typed domain commands instead.

## Verification obligations

- Property-test get/put laws, complements, validation, and rejection over
  generated source/view states.
- Fuzz edits that omit, aggregate, reorder, or redact source data and prove
  hidden information is preserved or loss is explicit.
- Apply concurrent source progress before put; stale projections must conflict
  or rebase through a separately validated transformation.

## Connections

- [Internal-service index](README.md) — editable projection scope.
- [Project schema negotiation](../user-owned-project-graph-and-composition/provider-discovery-binding-and-schema-negotiation.md) — version context.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Combinators for bidirectional tree transformations](../../../30-sources/foster-et-al-2007-bidirectional-tree-transformations.md).
2. [Project Cambria](../../../30-sources/litt-et-al-2020-cambria.md).
3. [Cooperative-editing consistency](../../../30-sources/sun-et-al-1998-cooperative-editing-consistency.md).
