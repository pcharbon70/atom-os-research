---
title: "Export, import, retention, and recovery"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - data-portability
  - persistence
  - project-graph
aliases: []
---

# Export, import, retention, and recovery

This study decomposes [User-owned project graph and composition](../user-owned-project-graph-and-composition.md).

Research question: What makes a project portable, interpretable, and
recoverable after provider, runtime, storage-adapter, or machine loss?

## Research basis and status

Personal dynamic media motivates user ownership; persistent programming and
Dexter supply explicit roots, typed structures, and separation from run-time
presentation. NixOS demonstrates immutable version closures and explicit
generation rollback at a different system layer.
[1](../../../30-sources/kay-goldberg-1977-personal-dynamic-media.md)
[2](../../../30-sources/atkinson-et-al-1983-persistent-programming.md)
[3](../../../30-sources/halasz-schwartz-1994-dexter-hypertext-reference-model.md)
[4](../../../30-sources/dolstra-et-al-2008-nixos.md)

Portability is a design target, not a demonstrated archive format.

## Development

### Owned state and trust boundary

Export includes manifests, object schemas and values, graph edges, history
policy, immutable provider requirements, provenance, conflicts, and disclosed
collaboration metadata. It excludes live capabilities, session secrets,
surface/focus leases, device handles, and opaque process snapshots.

### Admission, transitions, and completion

Export seals a self-describing closure at one manifest frontier and reports
omitted protected or externally retained content. Import validates framing and
digests in quarantine, resolves schema/provider availability, rechecks current
policy, assigns local storage and resource ceilings, and publishes only after a
recoverable commit record. Unknown types remain inspectable as bounded typed
records with provenance.

### Failure and adversarial behavior

Archives may be decompression bombs, cyclic graphs, malicious packages, stale
authority records, or privacy-erasure regressions. Import never executes
embedded providers, all sizes and references are bounded, and retention
tombstones remain separate from portable content when policy forbids
redisclosure.

### Alternatives and unresolved tradeoffs

Filesystem trees are inspectable but weak for graph-atomic history. One binary
image preserves closure but obscures meaning and incremental recovery. A
framed manifest plus content-addressed chunks is promising; canonical encoding,
encryption portability, and deletion-proof semantics remain open.

## Verification obligations

- Remove the original provider and machine, import elsewhere, and demonstrate
  semantic inspection plus later restoration with an independent provider.
- Truncate, reorder, duplicate, and corrupt chunks; import must fail boundedly
  without partial publication.
- Export after revocation and erasure requests and verify no reusable authority
  or forbidden historical content survives.

## Connections

- [Internal-service index](README.md) — project durability responsibilities.
- [Project manifest and history](project-manifest-object-identity-and-history.md) — defines the portable semantic closure.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — limitations.

## Sources

1. [Personal dynamic media](../../../30-sources/kay-goldberg-1977-personal-dynamic-media.md).
2. [An approach to persistent programming](../../../30-sources/atkinson-et-al-1983-persistent-programming.md).
3. [The Dexter hypertext reference model](../../../30-sources/halasz-schwartz-1994-dexter-hypertext-reference-model.md).
4. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
