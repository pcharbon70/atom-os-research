---
title: "Operating system framed in case of mistaken identity"
kind: source
created: "2026-09-04"
authors:
  - "Cristian Bravo-Lillo"
  - "Lorrie Faith Cranor"
  - "Julie Downs"
  - "Saranga Komanduri"
  - "Stuart Schechter"
  - "Manya Sleeper"
published: 2012
citation_key: "bravo-lillo-et-al-2012-operating-system-framed"
container: "Proceedings of the 19th ACM Conference on Computer and Communications Security"
edition: null
isbn: null
doi: "10.1145/2382196.2382237"
url: "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osframed.pdf"
accessed: "2026-09-04"
tags:
  - authentication
  - trusted-path
  - usable-security
aliases:
  - "OS framed"
---

# Operating system framed in case of mistaken identity

## Reference

Cristian Bravo-Lillo, Lorrie Faith Cranor, Julie Downs, Saranga Komanduri,
Stuart Schechter, and Manya Sleeper. “[Operating System Framed in Case of
Mistaken Identity: Measuring the Success of Web-based Spoofing Attacks on OS
Password-entry Dialogs](https://doi.org/10.1145/2382196.2382237).” *ACM CCS
2012*, pages 365–377.

## Research question or contribution

The study asks whether web content that imitates operating-system credential
dialogs can elicit genuine device-login passwords and whether interface
variants materially protect users.

## Method

The researchers recruited 504 U.S. Mechanical Turk participants to evaluate
online games. A controlled third-party page presented spoofed Windows or macOS
credential-entry dialogs. A second experiment more tightly measured one strong
Windows treatment.

## Findings

- In the strongest attacks, more than 20% of participants entered credentials
  they later said were their genuine device-login credentials.
- Many non-victims were not aware of the spoof; declining the prompt did not
  necessarily show that the trusted-path distinction was understood.
- Cosmetic prompt differences and a cancel control were not sufficient
  defenses under the study conditions.
- The authors conclude that providing a trusted path is insufficient if the OS
  also habituates users to enter device credentials into spoofable paths; less
  secure paths must be forbidden from collecting the same credential.

## Relevance

Atom OS needs a secure-attention mechanism and a tiny trusted interaction
service, but also a credential-use rule: no application, browser, CLI plugin,
or compatibility environment may receive the device-login secret. Sensitive
approval must display the principal, requester, exact resource/action, scope,
duration, and consequence on a protected surface and bind the response to that
specific grant request.

## Limits

The participants, operating systems, interfaces, and password-centric threat
model are from 2012. The study does not evaluate passkeys, hardware tokens,
modern platform authenticators, or the proposed Atom OS UI. Its result supports
the architectural need for trusted interaction, not one timeless visual design.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
