---
title: "Living in Your Programming Environment: Towards an Environment for Exploratory Adaptations of Productivity Tools"
kind: source
created: "2026-09-04"
authors:
  - "Patrick Rein"
  - "Jens Lincke"
  - "Stefan Ramson"
  - "Toni Mattis"
  - "Robert Hirschfeld"
published: "2017-10-22"
citation_key: "rein-et-al-2017-living-in-programming-environment"
container: "Proceedings of the 3rd ACM SIGPLAN International Workshop on Programming Experience (PX/17.2)"
edition: null
isbn: "978-1-4503-5522-3"
doi: "10.1145/3167108"
url: "https://doi.org/10.1145/3167108"
accessed: "2026-09-04"
tags:
  - end-user-programming
  - exploratory-programming
  - live-programming
  - productivity-tools
aliases:
  - "Living in your programming environment"
---

# Living in Your Programming Environment: Towards an Environment for Exploratory Adaptations of Productivity Tools

## Reference

Patrick Rein, Jens Lincke, Stefan Ramson, Toni Mattis, and Robert Hirschfeld.
“[Living in Your Programming Environment: Towards an Environment for
Exploratory Adaptations of Productivity
Tools](https://doi.org/10.1145/3167108).” *Proceedings of PX/17.2*, pages
17–27, 22 October 2017. The [author
copy](https://www.patrickrein.de/publications/ReinLinckeRamsonMattisHirschfeld_2017_LivingInYourProgrammingEnvironmentTowardsAnEnvironmentForExploratoryAdaptationsOfProductivityTools_AcmDL.pdf)
was read.

## Contribution

The paper adapts a Squeak/Smalltalk-derived exploratory environment for
everyday productivity tasks. It asks which live-programming mechanisms help
knowledge workers alter tools in the same environment in which they use them.

## Method

The authors report design and use experience over eight months, including
productivity-tool examples, direct object manipulation, scripting, and
integration with remote data. The evidence is reflective use by system
builders rather than a controlled novice study.

## Findings

- Immediate feedback, inspectable objects, examples, and direct transitions
  between use and programming support exploratory adaptation.
- Ordinary work requires durable data, external-service integration, error
  handling, and understandable object identity—not only a live evaluator.
- Remote object lifecycle and local copies create unresolved reconciliation
  questions when an external system changes or deletes an object.
- The integrated environment improves malleability but also exposes complexity
  and assumes programming knowledge.

## Relevance

The report connects Smalltalk-style live tools to practical project work while
showing why Atom OS needs capability-scoped object access, explicit remote
provenance, durable staging, and conflict policy around the live experience.

## Limits

Eight months of builder use does not establish safety, non-expert
learnability, or comparative productivity. The environment's shared object
world and web-service assumptions should not be copied as Atom OS trust or
failure boundaries.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
