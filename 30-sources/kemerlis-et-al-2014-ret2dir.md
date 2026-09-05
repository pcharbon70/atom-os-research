---
title: "ret2dir: Rethinking kernel isolation"
kind: source
created: "2026-09-04"
authors:
  - "Vasileios P. Kemerlis"
  - "Michalis Polychronakis"
  - "Angelos D. Keromytis"
published: 2014
citation_key: "kemerlis-et-al-2014-ret2dir"
container: "23rd USENIX Security Symposium"
edition: null
isbn: "978-1-931971-15-7"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity14/technical-sessions/presentation/kemerlis"
accessed: "2026-09-04"
tags:
  - kernels
  - memory-protection
  - operating-systems
  - security
  - virtual-memory
aliases:
  - "ret2dir"
---

# ret2dir: Rethinking kernel isolation

## Reference

Vasileios P. Kemerlis, Michalis Polychronakis, and Angelos D. Keromytis.
“ret2dir: Rethinking Kernel Isolation.” *23rd USENIX Security Symposium*, pages
957–972, 2014.
[USENIX paper and artifacts](https://www.usenix.org/conference/usenixsecurity14/technical-sessions/presentation/kemerlis).

## Research question or contribution

Can an attacker bypass protections against kernel access or control transfer
to user virtual addresses by using the privileged direct-map alias of the same
user-controlled physical frame?

## Method

The authors develop the return-to-direct-map exploitation technique, construct
exploits for x86, x86-64, AArch32, and AArch64 Linux targets, and propose an
exclusive page-frame-ownership defense that prevents implicit sharing between
user mappings and a privileged direct map.

## Findings

- One physical frame mapped at both a user address and a supervisor direct-map
  address creates implicit sharing that virtual-address-based protections may
  not block.
- The evaluated exploits bypassed software defenses and hardware mechanisms
  including SMEP, SMAP, and PXN by targeting the privileged alias.
- The paper demonstrates the technique across multiple ISA families, making
  the aliasing problem broader than one instruction set.
- Exclusive page-frame ownership can remove the dangerous alias with low
  overhead in the evaluated Linux prototype.

## Relevance

Atom's safe-access helper cannot claim isolation merely because SMAP, PAN, or
SUM is normally restrictive. User-owned frames should not have an ambient
dereferenceable privileged alias; a temporary alias must be capability-bound,
non-executable, lexically scoped, and closed before its frame can change role.

## Limits

The exploits assume another memory-corruption or control primitive and target
historical Linux designs. They do not show that every direct map is exploitable
or measure Atom's proposed approach. Exclusive ownership and temporary aliases
still need proofs covering DMA, speculative behavior, and teardown.

## Derived work

- [Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md)
- [Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md)
