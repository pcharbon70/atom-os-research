---
title: "SWIM: Scalable weakly-consistent infection-style process group membership protocol"
kind: source
created: "2026-09-03"
authors:
  - "Abhinandan Das"
  - "Indranil Gupta"
  - "Ashish Motivala"
published: 2002
citation_key: "das-et-al-2002-swim"
container: "Proceedings of the 2002 International Conference on Dependable Systems and Networks"
edition: "DSN 2002, 303–312"
isbn: "0-7695-1597-5"
doi: "10.1109/DSN.2002.1028914"
url: "https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf"
accessed: "2026-09-03"
tags:
  - distributed-systems
  - failure-detection
  - membership
aliases:
  - "SWIM"
---

# SWIM: Scalable weakly-consistent infection-style process group membership protocol

## Reference

Abhinandan Das, Indranil Gupta, and Ashish Motivala. “[SWIM: Scalable
Weakly-Consistent Infection-Style Process Group Membership
Protocol](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf).”
*DSN 2002*, pages 303–312. DOI
[10.1109/DSN.2002.1028914](https://doi.org/10.1109/DSN.2002.1028914).

## Research question or contribution

Can a large process group maintain useful, weakly consistent membership and
detect crash failures without the per-member load or hot spots of traditional
all-to-all or centralized heartbeating?

## Method

The paper separates randomized peer probing from infection-style membership
dissemination, analyzes detection and message-load properties, and evaluates a
prototype on a commodity-PC cluster. It also adds indirect probes, a suspicion
period, incarnation numbers, and a round-robin target-selection variant.

## Findings

- Failure detection and membership dissemination are distinct functions and
  need not share one all-to-all heartbeat protocol.
- Under the paper's model, expected detection time at some non-faulty member
  and expected message load per member do not grow with group size.
- Suspicion before confirmation reduces, but does not eliminate, false
  positives. A member can refute suspicion with an `Alive` update carrying a
  higher incarnation number.
- Membership views are deliberately weakly consistent. Stronger agreement is a
  separate and potentially less scalable problem.
- A joining member still needs a trusted contact or well-known rendezvous; the
  membership algorithm does not create admission policy or identity.

## Relevance

Atom OS can use a SWIM-like service as a scalable source of reachability
observations and cluster-view hints. Its output must remain typed as
`Suspect`, `Alive`, or `ProtocolDeclaredFailed`, with observer and time
evidence, and must not call the last state a confirmed physical crash or
authorize a restart, leader takeover, namespace write, or device action. Node
incarnation numbers align with the wider architecture's stale-reference
defenses.

## Limits

The prototype and network model are historical, non-Byzantine, and narrower
than an adversarial or resource-starved deployment. Weak membership does not
provide linearizable naming, consensus, durable configuration, secure node
admission, or proof that an unreachable process has crashed. WAN adaptation
was future work in the paper.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
