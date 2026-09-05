---
title: "Single Application Model, Multiple Synchronized Views"
kind: source
created: "2026-09-04"
authors:
  - "Rafah Hosn"
  - "Stéphane H. Maes"
  - "T. V. Raman"
published: "2001-08"
citation_key: "hosn-et-al-2001-single-application-model-multiple-views"
container: "Proceedings of the 2001 IEEE International Conference on Multimedia and Expo (ICME 2001)"
edition: null
isbn: null
doi: "10.1109/ICME.2001.1237813"
url: "https://doi.org/10.1109/ICME.2001.1237813"
accessed: "2026-09-04"
tags:
  - accessibility
  - multimodal-interaction
  - synchronized-views
  - user-interface
aliases:
  - "Single model synchronized views"
---

# Single Application Model, Multiple Synchronized Views

## Reference

Rafah Hosn, Stéphane H. Maes, and T. V. Raman. “[Single Application Model,
Multiple Synchronized
Views](https://doi.org/10.1109/ICME.2001.1237813).” *Proceedings of ICME
2001*, Tokyo, August 2001.

## Contribution

The paper proposes one modality-independent application model behind several
synchronized access paths, particularly visual and speech interfaces. User
intent updates the common model and the resulting state is reflected in each
view rather than maintained independently in modality-specific applications.

## Method

The authors present an architectural framework and example implementation for
multi-device, multimodal access. It establishes feasibility and a useful role
split, not broad comparative usability, accessibility, security, or
fault-recovery evidence.

## Findings

- A shared application model can reduce duplicated modality-specific business
  logic and keep visual and speech interaction synchronized.
- Views translate modality-specific input into model intent and translate model
  results back into appropriate presentation.
- Synchronization belongs at the model boundary; copying final presentation
  between channels loses semantic structure.
- A shared model does not require identical view shape or interaction sequence.

## Relevance

The work supports an authoritative Atom OS semantic/model layer with plural
visual, voice, assistive, and remote projections. Atom OS must add durable
identity, capability-bearing actions, revisions, replay and gap handling,
resource bounds, and supervised restart.

## Limits

The framework predates current platform APIs and does not address multi-writer
conflicts, user-intent ambiguity, untrusted view providers, capability
attenuation, or external-effect outcomes. “Synchronized” should not be read as
bit-identical or simultaneously updated under all failures.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
