---
title: "xv6: a simple, Unix-like teaching operating system"
kind: source
created: "2026-09-06"
authors: ["Russ Cox","Frans Kaashoek","Robert Morris"]
published: null
citation_key: "cox-et-al-2026-xv6-risc-v-book"
container: "MIT PDOS teaching book"
edition: "Online RISC-V draft accessed 2026-09-05"
isbn: null
doi: null
url: "https://mit-pdos.github.io/xv6-riscv-book/"
accessed: "2026-09-05"
tags:
  - boot
  - risc-v
  - operating-systems
aliases: []
---

# xv6: a simple, Unix-like teaching operating system

## Reference

Russ Cox, Frans Kaashoek, Robert Morris. [xv6: a simple, Unix-like teaching operating system](https://mit-pdos.github.io/xv6-riscv-book/). MIT PDOS teaching book. Publication date not established. Online RISC-V draft accessed 2026-09-05. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to privilege entry, memory protection, and user return in the CLI-first operating-system proof of concept.

## Method

Read the authors' online organization, trap, interrupt and sleep/wakeup chapters. This is explanatory implementation evidence, not an independent security or latency evaluation.

## Findings

Chapters 2, 4, 6 and 9 explain protection, software trap entry, buffered UART I/O, and atomic sleep/wakeup. xv6 keeps console line editing inside its monolithic kernel; Atom's proposed user-space parser is a different placement.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

The online draft and linked source evolve. xv6's machine-mode startup, Unix API, filesystem and scheduler must not be silently imported into the OpenSBI/capability profile.

## Derived work

- [Privilege entry, memory protection, and user return](../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md)
