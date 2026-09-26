---
title: "Landlock: unprivileged access control"
kind: source
created: "2026-09-26"
authors:
  - "Mickaël Salaün"
published: "2026-08"
citation_key: "linux-kernel-2026-landlock"
container: "The Linux Kernel documentation"
edition: null
isbn: null
doi: null
url: "https://docs.kernel.org/userspace-api/landlock.html"
accessed: "2026-09-26"
tags:
  - capability-security
  - linux
  - operating-systems
  - sandboxing
aliases: []
---

# Landlock: unprivileged access control

## Reference

Mickaël Salaün. “[Landlock: unprivileged access
control](https://docs.kernel.org/userspace-api/landlock.html).” *The Linux
Kernel documentation*, dated August 2026; accessed 26 September 2026.

## Research question or contribution

The documentation specifies how a process can restrict its ambient
filesystem and network rights using a Linux security module.

## Method

Read the official rules, enforcement, inheritance, file-descriptor,
compatibility, and limitations sections. This is interface documentation.

## Findings

- Unprivileged processes can restrict file-hierarchy actions and TCP or UDP
  port operations. UDP rights require ABI version 10; supported rights must
  be detected at runtime (§“Landlock rules,” §“Compatibility”).
- Restrictions extend to children and cannot be removed. Every stacked
  layer and other system controls must permit access (§“Layers of file path
  access rights,” §“Inheritance”).
- Selected signals and abstract Unix-domain socket operations can be scoped
  to the same or nested domain (§“IPC scoping”).
- Already open file descriptors retain prior access; a ruleset does not
  retrospectively confine them (§“Rights associated with file descriptors”).

## Relevance

An existing kernel can restrict agent resource use, informing the
[safe agent delegation and execution
synthesis](../20-notes/safe-agent-delegation-and-execution.md) and the
[Kay OS inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md).

## Limits

This living page is access-date pinned. Rights depend on kernel configuration
and ABI; best-effort fallback may leave older hosts less restricted. Landlock
does not evaluate natural-language intent, and self-restriction does not ensure
every agent installs a ruleset.

## Derived work

- [Safe agent delegation and execution](../20-notes/safe-agent-delegation-and-execution.md)
- [How can Kay OS safely delegate work to agents?](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
