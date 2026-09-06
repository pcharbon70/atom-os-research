---
title: "RISC-V from scratch 3: Writing a UART driver in assembly (1 / 3)"
kind: source
created: "2026-09-06"
authors: ["twilco"]
published: "2019-07-08"
citation_key: "twilco-2019-risc-v-uart-driver"
container: "twilco's blog"
edition: null
isbn: null
doi: null
url: "https://twilco.github.io/riscv-from-scratch/2019/07/08/riscv-from-scratch-3.html"
accessed: "2026-09-05"
tags:
  - boot
  - risc-v
  - serial-console
aliases: []
---

# RISC-V from scratch 3: Writing a UART driver in assembly (1 / 3)

## Reference

twilco. [RISC-V from scratch 3: Writing a UART driver in assembly (1 / 3)](https://twilco.github.io/riscv-from-scratch/2019/07/08/riscv-from-scratch-3.html). twilco's blog. 2019-07-08. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to serial console and minimal cli in the CLI-first operating-system proof of concept.

## Method

Read the first-party walkthrough and displayed commands/output. No local reproduction was performed.

## Findings

The author inspects QEMU's DTB, identifies an NS16550-compatible device, builds a UART skeleton, and exposes startup/linker dependencies. The post intentionally postpones interrupts.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

Its addresses and tools describe a historical configuration. General multi-cell addresses require ordered concatenation, not the article's simple addition; UART clock frequency does not establish CPU or timer frequency. Use the example for discovery workflow and check normative bindings.

## Derived work

- [Serial console and minimal CLI](../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md)
