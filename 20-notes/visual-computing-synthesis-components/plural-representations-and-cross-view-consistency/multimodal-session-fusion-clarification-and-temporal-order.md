---
title: "Multimodal session fusion, clarification, and temporal order"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - multimodal-interaction
  - semantic-ui
  - visual-computing
aliases: []
---

# Multimodal session fusion, clarification, and temporal order

This study decomposes [Plural representations and cross-view consistency](../plural-representations-and-cross-view-consistency.md).

Research question: How can voice, pointer, keyboard, touch, switch, and
assistive events cooperate without silently guessing user intent or broadening
authority?

## Research basis and status

Oviatt's synthesis rejects simplistic assumptions that multimodal inputs are
simultaneous or redundant. Single-model visual/speech work demonstrates one
coordinated architecture. User-interaction security research requires authentic
principals and explicit consequential authorization.
[1](../../../30-sources/oviatt-1999-ten-myths-multimodal-interaction.md)
[2](../../../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md)
[3](../../../30-sources/yee-2002-user-interaction-design-secure-systems.md)

No Atom fusion policy or accessibility study exists.

## Development

### Owned state and trust boundary

The multimodal manager owns an interaction session ID, participating seats and
modalities, semantic context revision, partial hypotheses, confidence,
temporal windows, clarification history, and expiry. It receives modality-
specific evidence but does not own domain authority or reinterpret a low-
confidence hypothesis as confirmation.

### Admission, transitions, and completion

Events enter with provenance and exact semantic/focus generations. Fusion may
produce an unambiguous typed action, request clarification, or cancel. A
clarification displays or speaks the proposed principal, target, parameters,
and consequence through a trusted path when required. Completion binds one
client action ID; late modality events cannot append to a closed session.

### Failure and adversarial behavior

Delayed speech, pointer drift, crosstalk, spoofed audio, modality takeover,
locale ambiguity, and broker restart can combine unrelated intent. Bounded
windows, explicit speaker/seat identity, confidence floors, cancellation on
context change, and no effect before domain admission constrain the profile.

### Alternatives and unresolved tradeoffs

Requiring one modality per command is predictable but excludes complementary
interaction. Aggressive probabilistic fusion is fluid but unsafe for
consequential actions. Conservative typed fusion with clarification is
preferred; thresholds and latency must be task- and population-specific.

## Verification obligations

- Delay and reorder modalities across focus, locale, target, and session
  changes; never combine events from incompatible contexts.
- Inject ambiguous and adversarial speech/pointer sequences; consequential
  operations must clarify or reject.
- Study representative motor, vision, speech, and cognitive-access profiles
  for error recovery, workload, timing, and comprehension.

## Connections

- [Internal-service index](README.md) — plural interaction.
- [Trusted event provenance](../input-focus-and-trusted-interaction-authority/device-normalization-event-provenance-and-seat-routing.md) — input origins.
- [Semantic actions](../semantics-first-accessible-ui-protocol/action-description-invocation-and-durable-outcomes.md) — typed intent.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence.

## Sources

1. [Ten myths of multimodal interaction](../../../30-sources/oviatt-1999-ten-myths-multimodal-interaction.md).
2. [Single application model, multiple views](../../../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md).
3. [User interaction design for secure systems](../../../30-sources/yee-2002-user-interaction-design-secure-systems.md).
