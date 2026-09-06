---
title: "All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications"
kind: source
created: "2026-09-06"
authors: ["Thanumalayan Sankaranarayana Pillai","Vijay Chidambaram","Ramnatthan Alagappan","Samer Al-Kiswany","Andrea C. Arpaci-Dusseau","Remzi H. Arpaci-Dusseau"]
published: 2014
citation_key: "pillai-et-al-2014-crash-consistent-applications"
container: "USENIX OSDI 2014"
edition: "Pages 433–448"
isbn: null
doi: null
url: "https://www.usenix.org/conference/osdi14/technical-sessions/presentation/pillai"
accessed: "2026-09-05"
tags:
  - crash-consistency
  - file-systems
  - storage
aliases: []
---

# All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications

## Reference

Thanumalayan Sankaranarayana Pillai, Vijay Chidambaram, Ramnatthan Alagappan, Samer Al-Kiswany, Andrea C. Arpaci-Dusseau, Remzi H. Arpaci-Dusseau. [All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/pillai). USENIX OSDI 2014. 2014. Pages 433–448. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to durable state and crash consistency in the CLI-first operating-system proof of concept.

## Method

Read [full paper](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-pillai.pdf), particularly sections 2–3.6 and 4.4.4; publication record verifies title, authors and venue.

## Findings

Persistence properties varied across the studied filesystem configurations. BOB explored persisted block reorderings; ALICE related application traces and checkers to required persistence properties. File-content persistence can be insufficient when directory changes also matter.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

Results depend on the tested workloads, checkers and storage model. They do not certify a new device or demonstrate that terminating an emulator reproduces power loss.

## Derived work

- [Durable state and crash consistency](../20-notes/proof-of-concept-requirements/durable-state-and-crash-consistency.md)
