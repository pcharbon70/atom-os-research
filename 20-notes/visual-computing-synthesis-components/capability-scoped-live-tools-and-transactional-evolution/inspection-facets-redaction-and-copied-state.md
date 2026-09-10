---
title: "Inspection facets, redaction, and copied state"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - capability-security
  - live-programming
  - visual-computing
aliases: []
---

# Inspection facets, redaction, and copied state

This study decomposes [Capability-scoped live tools and transactional evolution](../capability-scoped-live-tools-and-transactional-evolution.md).

Research question: What may a live tool observe without acquiring mutation,
secret access, arbitrary memory access, or transitive authority?

## Research basis and status

Smalltalk's environment demonstrates continuous browsers and inspectors, while
capability research makes reachable authority—not UI labels—the security
boundary. DTrace demonstrates typed observation points and per-consumer state
for production tracing at a different layer.
[1](../../../30-sources/goldberg-1984-smalltalk-80-interactive-environment.md)
[2](../../../30-sources/miller-et-al-2003-capability-myths.md)
[3](../../../30-sources/cantrill-et-al-2004-dtrace.md)

The Atom inspection schema and disclosure policy remain proposed.

## Development

### Owned state and trust boundary

The live-tool broker owns target scope, observer identity, facet type,
field/event allowlists, disclosure labels, generation, expiry, rate, and audit
record. Public semantic inspection, selected private fields, memory/debug
control, trace attachment, and mutation are separate capabilities.

### Admission, transitions, and completion

Inspection requests validate current project, object, code, schema, and policy
generations. The target produces immutable typed snapshots or filtered semantic
records; tools do not receive live object graphs that contain hidden
capabilities. Derived observations retain target revision and redaction
metadata.

### Failure and adversarial behavior

Secret inference through relations, timing, object counts, errors, or repeated
queries can bypass field redaction. Snapshot size, frequency, traversal depth,
and join operations are bounded. Revocation closes subscriptions and prevents
cached handles from becoming current after target replacement.

### Alternatives and unresolved tradeoffs

In-process reflection maximizes liveness but collapses authority. Debug-memory
dumps are powerful but overdisclose. Typed copied observations are preferred;
some low-level diagnosis may require a separately approved, audited break-glass
facet with stricter retention.

## Verification obligations

- Attempt every inspection with each weaker facet and through transitive
  returned references; no authority amplification is permitted.
- Infer protected fields through structure, timing, aggregation, errors, and
  repeated differential queries.
- Revoke and replace targets while tools hold snapshots and subscriptions;
  stale observations remain attributable but non-operational.

## Connections

- [Internal-service index](README.md) — live-tool capability separation.
- [Semantic projection filtering](../semantics-first-accessible-ui-protocol/projection-filtering-redaction-and-platform-adapters.md) — public semantic views.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Smalltalk-80 interactive environment](../../../30-sources/goldberg-1984-smalltalk-80-interactive-environment.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
3. [DTrace](../../../30-sources/cantrill-et-al-2004-dtrace.md).
