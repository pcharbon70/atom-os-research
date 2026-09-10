---
title: "Focus, selection, virtualization, and consumer continuity"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - accessibility
  - focus-management
  - semantic-ui
aliases: []
---

# Focus, selection, virtualization, and consumer continuity

This study decomposes [Semantics-first accessible UI protocol](../semantics-first-accessible-ui-protocol.md).

Research question: How do assistive and other semantic clients retain task
continuity across virtual collections, locale changes, adapter restart, and
model progress?

## Research basis and status

WAI-ARIA and WCAG define focus, selection, name/role/value, status, and keyboard
requirements. AccessKit carries tree focus and text-selection structures, while
Core-AAM shows platform mappings can differ.
[1](../../../30-sources/w3c-2023-wai-aria-1-2.md)
[2](../../../30-sources/w3c-2024-wcag-2-2.md)
[3](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)
[4](../../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md)

No large-collection or real-assistive-client Atom experiment exists.

## Development

### Owned state and trust boundary

Semantic focus names a current view node and logical target; trusted input
focus remains a separate broker lease. Selection, caret, active descendant,
viewport anchor, and pending operation cursors carry independent revisions.
Virtualized nodes may be absent from presentation while logical collection
positions remain addressable through bounded navigation operations.

### Admission, transitions, and completion

Focus changes validate node visibility, current revisions, and requested
authority. A restart snapshot carries a recovery anchor rather than reusing
platform handles. If the target vanished, the publisher applies a declared
fallback rule and emits the reason; it never silently focuses a similarly
named replacement.

### Failure and adversarial behavior

Focus thrash, huge collections, stale selection ranges, localized reorder, and
event floods can trap or disorient users. Rate limits do not discard terminal
status; navigation windows are bounded; lifecycle generation prevents
delete/recreate confusion; adapters announce continuity loss.

### Alternatives and unresolved tradeoffs

Materializing every node simplifies random access but exhausts memory.
Presentation-only indices break under filtering and sorting. Logical anchors
plus bounded range materialization are preferred; fallback semantics require
testing with screen readers, magnifiers, switch, and voice users.

## Verification obligations

- Navigate million-item virtual collections under fixed memory and restore
  focus/selection after adapter and publisher restart.
- Change locale, ordering, filtering, and object lifecycle while focused;
  verify explicit continuity or explicit fallback.
- Flood focus/live-region events while a durable operation completes; the
  terminal result remains reachable and correctly attributed.

## Connections

- [Internal-service index](README.md) — consumer state.
- [Focus/capture leases](../input-focus-and-trusted-interaction-authority/focus-capture-leases-and-generation-fencing.md) — trusted routing distinction.
- [Multimodal sessions](../plural-representations-and-cross-view-consistency/multimodal-session-fusion-clarification-and-temporal-order.md) — cross-modality cursors.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [WAI-ARIA 1.2](../../../30-sources/w3c-2023-wai-aria-1-2.md).
2. [WCAG 2.2](../../../30-sources/w3c-2024-wcag-2-2.md).
3. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
4. [Core-AAM 1.2](../../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md).
