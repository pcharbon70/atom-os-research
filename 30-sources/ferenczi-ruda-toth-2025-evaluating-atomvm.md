---
title: "Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems"
kind: source
created: "2026-08-28"
authors:
  - "Daniel Ferenczi"
  - "Gergely Ruda"
  - "Melinda Tóth"
published: "2025-10-09"
citation_key: "ferenczi-et-al-2025-fault-tolerant-esp32"
container: "Proceedings of the 24th ACM SIGPLAN International Workshop on Erlang, 52-61"
edition: null
isbn: null
doi: "10.1145/3759161.3763048"
url: "https://doi.org/10.1145/3759161.3763048"
accessed: "2026-08-28"
tags:
  - atom-vm
  - distributed-systems
  - embedded-systems
  - fault-tolerance
  - research-paper
aliases:
  - "AtomVM fault-tolerant ESP32 evaluation"
---

# Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems

## Reference

Ferenczi, Daniel, Gergely Ruda, and Melinda Tóth. "[Evaluating AtomVM for
Fault-Tolerant ESP32-Based
Systems](https://doi.org/10.1145/3759161.3763048)." In *Proceedings of the 24th
ACM SIGPLAN International Workshop on Erlang*, 52–61. ACM, 2025.

## Research question or contribution

The paper studies the additional resource cost of using more than one
microcontroller and remote-node monitoring to tolerate complete endpoint
failures, comparing a single-node radio-message system with a fault-tolerant
arrangement.

## Method

This archive pass had authoritative bibliographic metadata and the conference
abstract, but not enough full-text access to extract the experimental design or
numerical results safely. The abstract says the workload receives and
processes radio messages and compares single-node and fault-tolerant variants.

## Findings

- The work moves beyond restarting an Erlang process on one MCU to handling
  complete hardware/node failure with redundant components.
- AtomVM exposes the node-monitoring features needed to attempt that design,
  but the resource cost must be measured on constrained microcontrollers.
- No quantitative result is recorded here because the accessible abstract did
  not contain one.

## Relevance

An AtomVM-based OS needs an explicit whole-node failure model. Language
supervision cannot recover from native memory corruption, power loss, or a dead
MCU. Redundant nodes and remote monitoring may form the outer fault-containment
layer for a trusted single-address-space device.

## Limits

This is an abstract-level source note. It must not be cited for detailed
methods, costs, or outcomes until the full paper has been read. It may overlap
substantially with the authors' open-access [Sensors
paper](ferenczi-ruda-toth-2025-measuring-erlang-scalability.md), but the exact
relationship has not been established here.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [Kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
