---
title: "Scrash: A system for generating secure crash information"
kind: source
created: "2026-09-05"
authors:
  - "Pete Broadwell"
  - "Matt Harren"
  - "Naveen Sastry"
published: 2003
citation_key: "broadwell-et-al-2003-scrash"
container: "12th USENIX Security Symposium"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/legacy/events/sec03/tech/full_papers/broadwell/broadwell.pdf"
accessed: "2026-09-05"
tags:
  - crash-dumps
  - diagnostics
  - privacy
  - security
aliases:
  - "Scrash"
---

# Scrash: A system for generating secure crash information

## Reference

Pete Broadwell, Matt Harren, and Naveen Sastry. “Scrash: A System for
Generating Secure Crash Information.” *12th USENIX Security Symposium*, 2003.
[USENIX paper](https://www.usenix.org/legacy/events/sec03/tech/full_papers/broadwell/broadwell.pdf)
and [HTML edition](https://www.usenix.org/legacy/events/sec03/tech/full_papers/broadwell/broadwell_html/index.html).

## Research question or contribution

Can useful crash state be exported to a developer without disclosing sensitive
values that happened to reside in the failing program's heap, stack, globals,
or derived data?

## Method

Scrash applies source transformations and a secure allocator to track selected
sensitive C-program data, then postprocesses core files before release. The
paper evaluates transformed applications, overhead, retained debugging value,
and privacy limitations.

## Findings

- Crash reports can contain passwords, payment data, and other values unrelated
  to the defect; diagnostic usefulness does not imply authority to disclose
  complete memory.
- Sensitive bytes and copies can be segregated and removed from a generated
  core while leaving other execution state available for debugging.
- Derived information such as a buffer length may also be sensitive, so a
  redaction policy needs explicit classes rather than only address ranges.
- Scrash separates core generation from a cleaning phase that overwrites
  selected sensitive regions before the resulting core is released.
- Scrash deliberately does not close indirect control-flow or covert-channel
  leaks. A program counter or stack shape can reveal information even when raw
  secret bytes are removed.

## Relevance

Atom should keep the sealed capture capsule protected and derive separately
versioned operational and forensic views. Export authority, redaction policy,
key generation, retention, and recipient are part of the sink/escalation
contract. Raw addresses, registers, capability identities, BEAM heap fragments,
and event correlations must be treated as potentially sensitive.

That protected-source/derived-view split is Atom synthesis motivated by
Scrash's privacy problem; Scrash itself cleans the generated core in place and
does not demonstrate authorization-derived views over an intact protected raw
source.

## Limits

Scrash targets source-available user C programs and remote crash reports, not a
privileged kernel coping with corrupted hardware. Developer annotations can be
wrong, and the system does not solve implicit flows, malicious recipients,
record authenticity, encryption, or denial of crash collection. Its central
privacy result is a design constraint rather than a complete kernel solution.

## Derived work

- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
