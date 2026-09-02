---
title: "BootStomp: On the security of bootloaders in mobile devices"
kind: source
created: "2026-09-02"
authors:
  - "Nilo Redini"
  - "Aravind Machiry"
  - "Dipanjan Das"
  - "Yanick Fratantonio"
  - "Antonio Bianchi"
  - "Eric Gustafson"
  - "Yan Shoshitaishvili"
  - "Christopher Kruegel"
  - "Giovanni Vigna"
published: 2017
citation_key: "redini-et-al-2017-bootstomp"
container: "26th USENIX Security Symposium"
edition: null
isbn: "978-1-931971-40-9"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/redini"
accessed: "2026-09-02"
tags:
  - boot
  - bootloader
  - security
  - static-analysis
aliases:
  - "BootStomp"
---

# BootStomp: On the security of bootloaders in mobile devices

## Reference

Nilo Redini et al. “BootStomp: On the Security of Bootloaders in Mobile
Devices.” *26th USENIX Security Symposium*, pages 781–798, 2017.
[USENIX record and open paper](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/redini).

## Research question or contribution

Can combined taint analysis and symbolic execution find paths by which
attacker-controlled inputs compromise mobile bootloaders or their verified-
boot properties?

## Method

The authors model security-relevant sources and sinks in bootloader binaries,
combine static taint analysis with targeted symbolic execution, and evaluate
four manufacturers' bootloaders.

## Findings

- The analysis found six previously unknown vulnerabilities, five confirmed by
  vendors, and rediscovered an earlier issue.
- Reported consequences included arbitrary execution in a bootloader,
  persistent compromise of the chain of trust, denial of service, and paths
  that could alter device lock state.
- Hardware coupling, proprietary binaries, missing metadata, and complex input
  handling make boot code unusually difficult to analyze dynamically.
- A verified-boot policy does not imply that all parsing and state transitions
  after signature verification are safe.

## Relevance

The direct subject is mobile bootloader implementation, not an OS handoff
parser. The justified inference is narrower: early privileged parsing deserves
an adversarial input model even when the preceding image was authenticated.
Keeping protocol adapters small, bounded, fuzzable, and disposable reduces the
amount of unverified parser logic that can corrupt the kernel's initial state.

## Limits

The evaluated bootloaders and vulnerabilities are platform-specific. The paper
does not compare UEFI, ACPI, device tree, or a normalized `BootInfo` design and
does not show that authenticated firmware should always be treated as actively
malicious.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/normalized-boot-handoff-and-feature-discovery.md)
