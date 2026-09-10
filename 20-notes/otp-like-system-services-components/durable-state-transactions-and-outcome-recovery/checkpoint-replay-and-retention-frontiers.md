---
title: "Checkpoint replay and retention frontiers"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Checkpoint replay and retention frontiers

This study decomposes [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery.md).

Research question: When can log history be reclaimed without invalidating recovery, readers or promised outcomes?

## Research basis and status

Crash-aware recovery and retained immutable roots separate creating a checkpoint
from safely selecting and collecting it. [1](../../../30-sources/chen-et-al-2015-fscq.md) [2](../../../30-sources/dolstra-et-al-2008-nixos.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The checkpoint service owns private images, included-LSN frontier, schema identity,
active selector and retention claims from readers, retries, migration and audit. A
compacted state image is not automatically a substitute for all historical
obligations.

### Admission, transitions and completion

Build against a coherent committed frontier, force the complete image, then publish
a validated redundant selector or transactional pointer. Recovery selects a valid
root and replays complete transactions strictly after its frontier. Truncation
requires every relevant retention claim to release the prefix.

### Failure and adversarial behavior

Crash during recovery must allow idempotent restart. A corrupt newest image cannot
justify silently dropping previously acknowledged state. Dangling blob references or
removed retry records make an apparently valid checkpoint semantically incomplete;
validate closure as well as checksums.

### Alternatives and unresolved tradeoffs

Frequent checkpoints bound replay time but increase write amplification and
concurrent memory. Incremental images reduce copying but complicate dependency
retention. Storage pressure may reject new work; it cannot retroactively shorten
existing durability or retry promises.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash during image write, selector write and subsequent log truncation; at least one valid required recovery path must remain.
- Hold an old reader and retry-result lease while compacting; neither required record may be collected prematurely.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Device-service policy and management](../device-service-policy-and-management/README.md) — settles hardware outcomes and buffer custody.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
2. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
