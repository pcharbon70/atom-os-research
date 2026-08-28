---
title: "Atom OS Research"
kind: map
created: "2026-08-28"
tags:
  - atom-vm
  - operating-systems
aliases:
  - "Home"
---

# Atom OS Research

This is the selective entry point to research on using `atom-vm` as the
foundation of a new operating system. See the [archive guide](../README.md) for
the repository structure and working conventions.

## Research objective

Determine which operating-system responsibilities can live in, beneath, or
alongside `atom-vm`, and establish a credible path from the existing runtime to
a bootable system whose core execution model is the VM itself.

## Active inquiries

- None yet. Initial inquiries should turn the broad objective into answerable
  architectural and experimental questions.

## Topic maps

- None yet. Add maps as research develops around boot, hardware abstraction,
  scheduling, memory, isolation, persistence, drivers, networking, or tooling.

## Recently developed

- None yet.

## Unsettled threads

- Identify the minimum substrate `atom-vm` requires when no conventional host
  operating system is present.
- Separate VM facilities from services currently supplied by platform ports,
  libraries, firmware, or a host kernel.
- Define the smallest reproducible boot experiment that would falsify or
  strengthen the foundational-VM hypothesis.
