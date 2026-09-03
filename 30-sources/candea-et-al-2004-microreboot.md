---
title: "Microreboot—A technique for cheap recovery"
kind: source
created: "2026-08-31"
authors:
  - "George Candea"
  - "Shinichi Kawamoto"
  - "Yuichi Fujiki"
  - "Greg Friedman"
  - "Armando Fox"
published: 2004
citation_key: "candea-et-al-2004-microreboot"
container: "6th Symposium on Operating Systems Design and Implementation"
edition: null
isbn: "1-931971-16-0"
doi: null
url: "https://www.usenix.org/conference/osdi-04/microreboot%E2%80%94-technique-cheap-recovery"
accessed: "2026-08-31"
tags:
  - fault-containment
  - recovery
  - restart
  - state-management
aliases:
  - "Microreboot"
---

# Microreboot—A technique for cheap recovery

## Reference

George Candea, Shinichi Kawamoto, Yuichi Fujiki, Greg Friedman, and Armando
Fox. “Microreboot—A Technique for Cheap Recovery.” *OSDI '04*, pages 31–44.
[USENIX record and paper](https://www.usenix.org/conference/osdi-04/microreboot%E2%80%94-technique-cheap-recovery).
[arXiv record](https://arxiv.org/abs/cs/0406005).

## Research question or contribution

Can restarting a fine-grained component restore service faster and with less
lost work than restarting its whole process or machine?

## Method

The authors restructure an Internet auction service running on JBoss so that
components can restart independently, important state lives in external stores,
and short calls can be retried. Fault injection and a workload generator compare
microreboot, process restart, and machine reboot.

## Findings

- Separating process recovery from data recovery makes fine-grained restart
  practical for the evaluated components.
- Microreboots were roughly an order of magnitude faster and lost roughly an
  order of magnitude less work than broader restarts in that system.
- Names were temporarily rebound to an unavailable sentinel, and recovery
  escalated through progressively larger restart scopes.
- Recovery depends on isolation, short requests, externalized state, and safe
  retry semantics; reboot does not create those properties.

## Relevance

Kernel domains should have externally invocable stop and teardown paths,
incarnation-specific endpoints, and an explicit escalation parent. OTP-style
restart intensity and strategy remain user-space policy. The kernel must expose
uncertain request outcomes rather than automatically retry them.

## Limits

The evaluation concerns a Java Internet application, not kernel services,
devices, BEAM runtimes, or malicious failures. Results cannot be transferred to
stateful protocols or irreversible I/O. Restart can reproduce a deterministic
bug or corrupt external state.

## Derived work

- [Failure translation and the OTP boundary](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
