---
title: "User interaction design for secure systems"
kind: source
created: "2026-09-04"
authors:
  - "Ka-Ping Yee"
published: 2002
citation_key: "yee-2002-user-interaction-design-secure-systems"
container: "University of California, Berkeley Technical Report UCB/CSD-02-1184"
edition: null
isbn: null
doi: null
url: "https://www2.eecs.berkeley.edu/Pubs/TechRpts/2002/5658.html"
accessed: "2026-09-04"
tags:
  - authentication
  - human-computer-interaction
  - security
  - trusted-path
aliases:
  - "Secure interaction design"
---

# User interaction design for secure systems

## Reference

Ka-Ping Yee. “[User Interaction Design for Secure
Systems](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2002/5658.html).”
Technical Report UCB/CSD-02-1184, University of California, Berkeley, May
2002.

## Research question or contribution

Yee asks how user-interface design can make security-relevant authority and
consequences understandable enough for a human to act safely. The work models
actors, actions, and each actor's subjective ability to perform an action, then
derives ten principles for secure interaction design.

## Method

The report develops an interaction model, derives design principles, and
applies them to case studies. It is a conceptual security/HCI analysis, not a
controlled user study or a proof that following the principles defeats all
spoofing and coercion.

## Findings

- A user needs an authentic, unambiguous channel to the party whose authority
  is being exercised; an interface that hides the acting principal invites
  mistaken delegation.
- Authority should be granted explicitly and in a form that corresponds to the
  user's current intent, rather than inferred from ambient context.
- Security-relevant effects should be visible, revocable where possible, and
  placed close to the action that causes them.
- The interface should not create powers the user cannot understand or control,
  and it should minimize the need to remember security state across actions.

## Relevance

The proposed Atom trusted-interaction broker should bind a protected input and
display lease to one canonical request digest, identify the requesting actor
and relying party, show the exact authority being requested, and return an
operation-bound approval rather than a reusable “user clicked yes” fact. Yee's
principles also support treating accessibility and multi-seat ownership as
part of the security contract instead of UI decoration.

## Limits

The report predates contemporary authenticators, composited desktops, mobile
permission systems, and remote administration. Its principles constrain a
design but do not select a hardware trusted path, quantify usability, or prove
that an Atom ceremony is unspoofable.

## Derived work

- [Trusted-interaction broker](../20-notes/authentication-and-authorization-components/trusted-interaction-broker.md)
- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
