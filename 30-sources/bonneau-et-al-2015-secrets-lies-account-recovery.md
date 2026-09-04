---
title: "Secrets, lies, and account recovery"
kind: source
created: "2026-09-04"
authors:
  - "Joseph Bonneau"
  - "Elie Bursztein"
  - "Ilan Caron"
  - "Rob Jackson"
  - "Mike Williamson"
published: 2015
citation_key: "bonneau-et-al-2015-secrets-lies-account-recovery"
container: "Proceedings of the 24th International Conference on World Wide Web (WWW '15)"
edition: null
isbn: "978-1-4503-3469-3"
doi: "10.1145/2736277.2741691"
url: "https://research.google/pubs/secrets-lies-and-account-recovery-lessons-from-the-use-of-personal-knowledge-questions-at-google/"
accessed: "2026-09-04"
tags:
  - account-recovery
  - authentication
  - empirical-security
  - usability
aliases:
  - "Personal knowledge questions at Google"
---

# Secrets, lies, and account recovery

## Reference

Joseph Bonneau, Elie Bursztein, Ilan Caron, Rob Jackson, and Mike Williamson.
“[Secrets, Lies, and Account Recovery: Lessons from the Use of Personal
Knowledge Questions at
Google](https://research.google/pubs/secrets-lies-and-account-recovery-lessons-from-the-use-of-personal-knowledge-questions-at-google/).”
*Proceedings of the 24th International Conference on World Wide Web*, pages
141–150, 2015. DOI
[10.1145/2736277.2741691](https://doi.org/10.1145/2736277.2741691).

## Research question or contribution

The authors test whether personal-knowledge questions provide a useful
combination of security and memorability for account recovery.

## Method

The study analyzes hundreds of millions of recovery-question answers and
millions of recovery claims from Google's deployed system. It measures answer
distributions, attackability, recall, and user behavior across languages and
countries, then compares knowledge questions with alternative recovery
signals.

## Findings

- Many answers have low effective entropy because popular responses and
  cultural distributions make them guessable.
- Users sometimes supply false answers for privacy or security, but those
  answers are harder to remember later.
- Memorability is poor enough that stronger questions can become unusable;
  weakening the question to improve recall generally makes guessing easier.
- Combining questions does not automatically repair the trade-off and may
  sharply reduce successful legitimate recovery.

## Relevance

Atom OS should not make personal questions a root recovery authenticator. The
recovery coordinator should instead use predeclared possession factors,
threshold custodians, cooling-off and cancellation, independent notification,
and narrow one-shot envelopes. The study also justifies measuring both attacker
success and legitimate recovery completion rather than declaring a ceremony
secure from cryptographic structure alone.

## Limits

The dataset concerns Google's account ecosystem and personal-knowledge
questions, not local OS recovery, hardware keys, social recovery, or encrypted
storage. It does not prove a particular alternative safe or determine when
destructive reset is acceptable.

## Derived work

- [Recovery coordinator](../20-notes/authentication-and-authorization-components/recovery-coordinator.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
