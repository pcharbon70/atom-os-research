---
title: "A Conversation with Alan Kay"
kind: source
created: "2026-09-04"
authors:
  - "Stuart Feldman"
  - "Alan C. Kay"
published: 2004
citation_key: "feldman-kay-2004-conversation-alan-kay"
container: "ACM Queue 2(9)"
edition: null
isbn: null
doi: "10.1145/1039511.1039523"
url: "https://doi.org/10.1145/1039511.1039523"
accessed: "2026-09-04"
tags:
  - human-computer-interaction
  - live-programming
  - personal-computing
  - smalltalk
aliases:
  - "Alan Kay Queue interview"
---

# A Conversation with Alan Kay

## Reference

Stuart Feldman and Alan C. Kay. “[A Conversation with Alan
Kay](https://doi.org/10.1145/1039511.1039523).” *ACM Queue* 2(9), pages
20–30, 2004. A [public transcript](https://www.doc.ic.ac.uk/~susan/475/AlanKay.html)
was used to check the interview text.

## Contribution

This interview records Kay's later evaluation of user interfaces, Smalltalk,
and commercial personal computing. It is useful because he explicitly
distinguishes an interface for accessing accumulated functions from a
changing, explorable environment that supports learning and authorship across
a user's lifetime.

## Method

The source is a technical interview and design reflection, not a specification
or empirical study. Feldman's questions draw out Kay's assessment of what the
PARC work achieved, what Smalltalk lost as it became a programmer's vehicle,
and what later systems still lacked.

## Findings

- Kay argues that an interface organized around access to an expanding catalog
  of functions tends toward a control panel whose complexity grows with every
  feature.
- The PARC ambition was a learning environment whose representations and
  conceptual leverage could evolve with the user rather than a fixed set of
  commands learned once.
- He says Smalltalk's evolution toward professional programming deemphasized
  some features intended for children and end-user authors.
- Reflection and a self-sufficient live environment remain important, but Kay
  also describes a protective boundary before users modify meta-level parts of
  the system. Malleability need not imply undifferentiated authority.
- The interview treats existing Smalltalk systems as evidence of a useful live
  toolchain while continuing to call the broader personal-computing project
  incomplete.

## Relevance

The interview prevents a nostalgic “restore Smalltalk exactly” conclusion. It
supports a safer Atom OS interpretation: keep causal connection, inspection,
and user authorship, while requiring an explicit capability step, transaction,
or recovery boundary for changes that can affect the runtime or other users.

## Limits

The claims are Kay's judgments in conversation. They do not measure usability,
security, or programming outcomes and should be separated from the behavior of
current Smalltalk implementations.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
