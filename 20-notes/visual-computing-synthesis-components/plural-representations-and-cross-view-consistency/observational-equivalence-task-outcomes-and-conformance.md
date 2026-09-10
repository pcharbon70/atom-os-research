---
title: "Observational equivalence, task outcomes, and conformance"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - accessibility
  - multimodal-interaction
  - visual-computing
aliases: []
---

# Observational equivalence, task outcomes, and conformance

This study decomposes [Plural representations and cross-view consistency](../plural-representations-and-cross-view-consistency.md).

Research question: When different view trees and interaction sequences are
allowed, what evidence shows they preserve essential meaning and outcomes?

## Research basis and status

Direct-manipulation analysis distinguishes semantic and articulatory distance.
Single-model visual/speech work demonstrates synchronized views, while WCAG
supplies task-relevant operability and semantic criteria. CAMELEON warns that
final presentations legitimately differ by target.
[1](../../../30-sources/hutchins-et-al-1985-direct-manipulation-interfaces.md)
[2](../../../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md)
[3](../../../30-sources/w3c-2024-wcag-2-2.md)
[4](../../../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md)

No Atom conformance suite or participant study exists.

## Development

### Owned state and trust boundary

An equivalence profile names essential task objects, discoverable operations,
preconditions, domain outcomes, error/repair paths, disclosure class, latency
and accessibility bounds, and explicitly presentation-specific information.
Tree shape, event sequence, and visual layout are not required to match.

### Admission, transitions, and completion

Each provider declares the profile and any deliberate loss. Conformance
executes tasks through only that representation, observes model outcomes and
semantic evidence, and checks that unavailable operations are disclosed rather
than silently altered. Human evaluation tests comprehension, recovery, and
transfer in addition to speed.

### Failure and adversarial behavior

Happy-path automation can miss inaccessible errors, focus loss, ambiguity,
privacy disclosure, or modality-specific dead ends. Tests include restart,
overload, stale state, locale, alternate input, and consequential actions with
representative users and real assistive clients.

### Alternatives and unresolved tradeoffs

Pixel equivalence is irrelevant to nonvisual views. Identical semantic trees
prevent useful adaptation. Task/outcome equivalence is preferred, but choosing
essential tasks embeds value judgments that require domain experts and affected
users.

## Verification obligations

- Execute every essential task through visual, keyboard, screen reader, text,
  voice, and remote profiles and compare durable outcomes plus recovery.
- Change locale, provider, provider version, and modality mid-task; preserve
  target identity and pending operation state.
- Include participants with relevant disabilities and report population,
  assistive technology, errors, comprehension, and transfer—not preference alone.

## Connections

- [Internal-service index](README.md) — equivalence scope.
- [Projection adapters](../semantics-first-accessible-ui-protocol/projection-filtering-redaction-and-platform-adapters.md) — platform tree differences.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence limits.

## Sources

1. [Direct manipulation interfaces](../../../30-sources/hutchins-et-al-1985-direct-manipulation-interfaces.md).
2. [Single application model, multiple views](../../../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md).
3. [WCAG 2.2](../../../30-sources/w3c-2024-wcag-2-2.md).
4. [CAMELEON framework](../../../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md).
