---
title: "OpenSBI firmware handoff: FW_DYNAMIC and FW_JUMP"
kind: source
created: "2026-09-06"
authors: ["OpenSBI contributors"]
published: null
citation_key: "opensbi-project-2026-firmware-handoff"
container: "OpenSBI project documentation"
edition: "master documentation accessed 2026-09-05"
isbn: null
doi: null
url: "https://github.com/riscv-software-src/opensbi/blob/master/docs/firmware/fw_dynamic.md"
accessed: "2026-09-05"
tags:
  - boot
  - firmware
  - risc-v
aliases: []
---

# OpenSBI firmware handoff: FW_DYNAMIC and FW_JUMP

## Reference

OpenSBI contributors. [OpenSBI firmware handoff: FW_DYNAMIC and FW_JUMP](https://github.com/riscv-software-src/opensbi/blob/master/docs/firmware/fw_dynamic.md). OpenSBI project documentation. Publication date not established. master documentation accessed 2026-09-05. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to target, firmware, and boot handoff in the CLI-first operating-system proof of concept.

## Method

Read FW_DYNAMIC and [FW_JUMP](https://github.com/riscv-software-src/opensbi/blob/master/docs/firmware/fw_jump.md) descriptions and configuration fields.

## Findings

FW_DYNAMIC receives next-stage information from its predecessor. FW_JUMP uses configured next-stage addresses without embedding the payload. Its FDT relocation settings can overlap a kernel unless layout is checked.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

The two handoffs are alternatives, not interchangeable command-line recipes. Source documentation does not pin firmware bytes, establish latency, or demonstrate an Atom kernel boot.

## Derived work

- [Target, firmware, and boot handoff](../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md)
