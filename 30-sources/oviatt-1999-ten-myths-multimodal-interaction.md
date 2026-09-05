---
title: "Ten Myths of Multimodal Interaction"
kind: source
created: "2026-09-04"
authors:
  - "Sharon L. Oviatt"
published: "1999-11-01"
citation_key: "oviatt-1999-ten-myths-multimodal-interaction"
container: "Communications of the ACM 42(11)"
edition: null
isbn: null
doi: "10.1145/319382.319398"
url: "https://doi.org/10.1145/319382.319398"
accessed: "2026-09-04"
tags:
  - human-computer-interaction
  - multimodal-interaction
  - speech-interface
  - user-interface
aliases:
  - "Multimodal interaction myths"
---

# Ten Myths of Multimodal Interaction

## Reference

Sharon L. Oviatt. “[Ten Myths of Multimodal
Interaction](https://doi.org/10.1145/319382.319398).” *Communications of the
ACM* 42(11), pages 74–81, 1 November 1999. An [archived
copy](https://www.cs.columbia.edu/~coms6998-11/papers/p74-oviatt.pdf) was read.

## Contribution

Oviatt synthesizes empirical multimodal-interaction findings to challenge
simple assumptions that speech, pointing, writing, gaze, and other modalities
are interchangeable, simultaneous, or universally preferred. Effective
systems use complementary strengths and adapt to user, task, context, and
recognition uncertainty.

## Method

The article draws on a body of experimental systems and user studies,
including multimodal maps and coordinated speech/pen interaction. It is a
research synthesis from 1999 rather than a current whole-population study.

## Findings

- People often distribute complementary information across modalities instead
  of redundantly expressing the same content.
- Multimodal inputs are frequently sequential and temporally related rather
  than perfectly simultaneous.
- Preferred and effective modality depends on user, task, environment, error,
  and cognitive load.
- Combining channels can disambiguate recognition and improve robustness, but
  a weak fusion model can also compound errors.
- Natural interaction does not eliminate the need for learned conventions,
  feedback, correction, and explicit system state.

## Relevance

Atom OS should preserve one semantic object and command space while permitting
modality-specific interaction sessions, context, timing, confidence, and
confirmation. A voice view is not a spoken serialization of a visual tree, and
cross-view equivalence must concern available meaning and effects rather than
identical steps.

## Limits

The systems and devices are historically bounded, and the article does not
cover capability security, screen-reader APIs, collaborative replicas,
generative models, or restart recovery. Its myths are design warnings, not a
complete multimodal protocol.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
