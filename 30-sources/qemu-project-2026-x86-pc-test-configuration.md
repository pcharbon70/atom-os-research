---
title: "QEMU x86 PC test configuration documentation"
kind: source
created: "2026-09-06"
authors:
  - "QEMU contributors"
published: null
citation_key: "qemu-project-2026-x86-pc-test-configuration"
container: "QEMU system documentation"
edition: "Moving master documentation; displayed version 11.1.50"
isbn: null
doi: null
url: "https://www.qemu.org/docs/master/system/invocation.html"
accessed: "2026-09-06"
tags:
  - hardware-profile
  - proof-of-concept
  - x86-64
aliases: []
---

# QEMU x86 PC test configuration documentation

## Reference

QEMU contributors. [QEMU x86 PC test configuration documentation](https://www.qemu.org/docs/master/system/invocation.html). Moving master documentation; displayed version 11.1.50. Read alongside [CPU model configuration](https://www.qemu.org/docs/master/system/qemu-cpu-models.html) and [PC platform documentation](https://www.qemu.org/docs/master/system/i386/pc.html).

## Research question or contribution

Which emulator controls define a minimal Intel x86-64 test fixture without claiming a physical motherboard replica?

## Method

Read the relevant specification, setup or configuration sections. No hardware, firmware update or guest execution was performed.

## Findings

Documents explicit CPU topology, separately assigned NUMA resources, optional-device suppression, serial backends and shutdown handling. Named CPU models and versioned machine types support explicit test configurations. The CPU-model table lists Nehalem-v1 as well as Opteron_G1-v1. The current T7500 profile selects Nehalem-v1 as an older-generation Intel fixture; the prior Opteron choice was superseded. Neither model name is an installed-hardware inventory result.

## Relevance

Separates guest ISA/features, machine devices and resource limits from the lab unit's unknown inventory.

## Limits

A q35 virtual platform is not a Dell T7500 / Intel 5520 motherboard replica. Documentation is not an installed QEMU pin or proof that an untested command boots. Guest topology is not host affinity or physical timing.

## Derived work

- [Dell Precision T7500 target and minimal QEMU profile](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
