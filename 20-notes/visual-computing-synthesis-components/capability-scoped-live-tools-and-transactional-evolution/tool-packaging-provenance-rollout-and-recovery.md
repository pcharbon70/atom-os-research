---
title: "Tool packaging, provenance, rollout, and recovery"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - live-programming
  - software-supply-chain
  - software-update
aliases: []
---

# Tool packaging, provenance, rollout, and recovery

This study decomposes [Capability-scoped live tools and transactional evolution](../capability-scoped-live-tools-and-transactional-evolution.md).

Research question: How does a local live experiment become a reusable,
confined, attributable tool without presenting provenance as behavioral proof?

## Research basis and status

NixOS supplies immutable dependency closures and deployment generations. TUF
and in-toto provide role-separated metadata, freshness, and supply-chain
provenance. Current canarying research in the corpus separates representative
cohorts and attribution from rollout confidence.
[1](../../../30-sources/dolstra-et-al-2008-nixos.md)
[2](../../../30-sources/samuel-et-al-2010-tuf.md)
[3](../../../30-sources/torres-arias-et-al-2019-in-toto.md)
[4](../../../30-sources/warner-davidovic-2018-canarying-releases.md)

No Atom tool registry, package profile, or rollout evidence exists.

## Development

### Owned state and trust boundary

The registry owns immutable artifact closures, interfaces, requested
capabilities, resource profiles, supported schemas/protocols, provenance,
signatures, compatibility, revocation, and rollout state. A signature says who
authorized bytes; it does not prove safety, usability, or semantic correctness.

### Admission, transitions, and completion

Publish verifies artifact closure and role/freshness metadata, then runs
isolated validation and human-readable authority/resource diffs. Installation
creates no ambient grants. Binding derives project-specific facets. Rollout
uses attributed cohorts and explicit inconclusive states; rollback retains
data-migration and effect limits from the changeset.

### Failure and adversarial behavior

Dependency confusion, stale metadata, compromised builders, capability
underdeclaration, telemetry bias, poisoned migration, and rollback after schema
advance threaten users. Threshold roles, immutable digests, sandboxed
validation, cohort attribution, compatibility gates, and retention closure
bound the protocol.

### Alternatives and unresolved tradeoffs

Publishing source snippets preserves malleability but weakens reproducibility.
Central review improves consistency but can become a monopoly. Open immutable
packages with user-selectable trust policy are preferred; reproducible-build
and ecosystem-governance requirements remain open.

## Verification obligations

- Tamper with artifacts, metadata roles, timestamps, provenance links, and
  dependency closure; detect before binding.
- Install a validly signed malicious or overprivileged package and ensure UI
  never presents signature as behavioral approval.
- Crash and revoke during staged rollout, migration, rollback, and retention
  cleanup; affected projects remain attributable and recoverable.

## Connections

- [Internal-service index](README.md) — reusable tool lifecycle.
- [Changeset publication](changeset-validation-migration-and-atomic-publication.md) — local commit protocol.
- [Project provider binding](../user-owned-project-graph-and-composition/provider-discovery-binding-and-schema-negotiation.md) — per-project admission.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence.

## Sources

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [The Update Framework](../../../30-sources/samuel-et-al-2010-tuf.md).
3. [in-toto](../../../30-sources/torres-arias-et-al-2019-in-toto.md).
4. [Canarying releases](../../../30-sources/warner-davidovic-2018-canarying-releases.md).
