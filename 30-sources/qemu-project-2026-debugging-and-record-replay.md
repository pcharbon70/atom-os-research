---
title: "QEMU debugging and record/replay"
kind: source
created: "2026-09-06"
authors: ["QEMU contributors"]
published: null
citation_key: "qemu-project-2026-debugging-and-record-replay"
container: "QEMU documentation"
edition: "master documentation; displayed version 11.1.50"
isbn: null
doi: null
url: "https://www.qemu.org/docs/master/system/replay.html"
accessed: "2026-09-05"
tags:
  - debugging
  - emulation
  - record-replay
aliases: []
---

# QEMU debugging and record/replay

## Reference

QEMU contributors. [QEMU debugging and record/replay](https://www.qemu.org/docs/master/system/replay.html). QEMU documentation. Publication date not established. master documentation; displayed version 11.1.50. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to models, fault injection, and measurement in the CLI-first operating-system proof of concept.

## Method

Read replay input/device requirements and GDB launch/state-inspection documentation.

## Findings

Record/replay logs nondeterministic inputs and uses instruction counting; device configuration must match its supported replay arrangements. The [GDB guide](https://www.qemu.org/docs/master/system/gdb.html) distinguishes opening a debugger endpoint from pausing guest startup.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

Replay is not automatic coverage of all schedules, nor a physical timing model. The exact machine, devices, accelerator and executable version must be qualified. The initially attempted /docs/master/replay.html URL failed; the system/replay.html page was used.

## Derived work

- [Models, fault injection, and measurement](../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md)
