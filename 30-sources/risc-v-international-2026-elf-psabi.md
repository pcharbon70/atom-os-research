---
title: "RISC-V ABIs Specification"
kind: source
created: "2026-09-06"
authors: ["RISC-V International"]
published: null
citation_key: "risc-v-international-2026-elf-psabi"
container: "RISC-V non-ISA specifications"
edition: "Online document; LP64 family status and calling conventions read"
isbn: null
doi: null
url: "https://riscv-non-isa.github.io/riscv-elf-psabi-doc/"
accessed: "2026-09-05"
tags:
  - abi
  - risc-v
  - toolchains
aliases: []
---

# RISC-V ABIs Specification

## Reference

RISC-V International. [RISC-V ABIs Specification](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/). RISC-V non-ISA specifications. Publication date not established. Online document; LP64 family status and calling conventions read. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to privilege entry, memory protection, and user return in the CLI-first operating-system proof of concept.

## Method

Read ABI status, integer and floating-point calling conventions, named ABIs, and syscall-scope section.

## Findings

The standard integer convention specifies argument and preserved registers and 128-bit stack alignment. LP64 and LP64D have different floating-point calling conventions. The syscall calling convention is explicitly outside this specification.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

An ABI's callee-save set is not the complete state needed after an asynchronous interrupt. A soft-float calling convention alone does not prohibit emitted floating-point instructions. Pin ISA flags, libraries and disassembly separately.

## Derived work

- [Privilege entry, memory protection, and user return](../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md)
