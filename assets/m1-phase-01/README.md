---
title: "M1 Phase 01 kernel-entry integration evidence"
kind: map
created: "2026-09-22"
tags:
  - archive-navigation
  - directory-index
  - implementation-evidence
  - m1
aliases: []
---

# M1 Phase 01 kernel-entry integration evidence

## Purpose

Retain the review-critical textual evidence from the clean Kay OS M1 Phase 1
integration run at commit `4766582e5ddff36b141b8787a29569e31c76ace6`.

## What belongs here

This directory contains the exact aggregate result and case table plus
newline-normalized transcriptions of the positive serial/register output and
all negative serial streams, tool/input identity record and retained-file
hashes. The full generated build tree remained outside version control under
`/tmp/kay-m1-phase-01-evidence`; original-file hashes, kernel and ISO identities
remain in the journal and case table. This is QEMU evidence, not
physical-machine or CLI evidence.

## Index

### Subdirectories

- None.

### Files

- [Run summary](summary.json) — exact clean revision, fixture, limits, cases and evidence boundary.
- [Case results](case-results.tsv) — exact six-case outcomes and per-image hashes.
- [Positive serial stream](normal-serial.log) — newline-normalized successful guest/loader transcript.
- [Positive register snapshot](normal-registers.txt) — newline-normalized QEMU monitor state after the guest pass record.
- [Missing-memory-map serial stream](missing-memmap-serial.log) — newline-normalized terminal diagnostic.
- [Overflow serial stream](memmap-overflow-serial.log) — newline-normalized checked-arithmetic diagnostic.
- [Overlap serial stream](memmap-overlap-serial.log) — newline-normalized ambiguous-ownership diagnostic.
- [Missing-CPUID serial stream](missing-cpuid-serial.log) — newline-normalized mandatory-feature diagnostic.
- [Bad-RSDP serial stream](bad-rsdp-serial.log) — newline-normalized firmware-checksum diagnostic.
- [Environment and input identities](environment.txt) — exact Zig, LLD, QEMU, SeaBIOS and signed Limine identities plus inherited M0 result.
- [Retained-file hashes](retained.sha256) — SHA-256 identities for every retained file except itself.

## Maintaining this index

Keep the observed bytes immutable. Later runs belong in a new evidence group or
must explicitly identify a superseding tested revision; never rewrite this run
to match a later merge.
