---
title: "Measuring Erlang-Based Scalability and Fault Tolerance on the Edge"
kind: source
created: "2026-08-28"
authors:
  - "Daniel Ferenczi"
  - "Gergely Ruda"
  - "Melinda Tóth"
published: "2025-08-06"
citation_key: "ferenczi-et-al-2025-edge"
container: "Sensors 25(15), 4843"
edition: null
isbn: null
doi: "10.3390/s25154843"
url: "https://doi.org/10.3390/s25154843"
accessed: "2026-08-28"
tags:
  - atom-vm
  - embedded-systems
  - fault-tolerance
  - performance
  - research-paper
aliases:
  - "AtomVM edge scalability measurements"
---

# Measuring Erlang-Based Scalability and Fault Tolerance on the Edge

## Reference

Ferenczi, Daniel, Gergely Ruda, and Melinda Tóth. "[Measuring Erlang-Based
Scalability and Fault Tolerance on the
Edge](https://doi.org/10.3390/s25154843)." *Sensors* 25, no. 15 (2025): 4843.
The [measurement code and raw
data](https://gitlab.com/d-ferenczi/atomvm-measurements) are public.

## Research question or contribution

The paper asks whether AtomVM can support the concurrency, supervision, data
processing, and LoRa communication needed for purpose-built, fault-tolerant
edge software within microcontroller resource limits.

## Method

The authors used Heltec WiFi LoRa 32 V3 and Wireless Tracker boards built on an
ESP32-S3 with two cores and 512 KB application RAM. They measured current with
a TC66 tester at 100 ms intervals and reported memory through AtomVM's ESP32
API. Process-scaling experiments ran ten times with a one-minute observation
before increasing load. Other experiments were repeated five or more times;
LoRa no-loss cases ran at least 20 minutes. A vendor-derived C++ sender served
as a reference implementation.

## Findings

- The board fit approximately 370 unmonitored, 350 monitored, 360 linked, or
  195 OTP-supervised worker processes. OTP supervision left about 83 KB unused
  despite failing to add more workers, indicating a limit other than raw free
  memory in that runtime/workload.
- Ten workers sampling every 50 ms overwhelmed an aggregator mailbox and led
  to out-of-memory failures. Intervals above 300 ms were sustainable in that
  setup; the default experiments used 500 ms.
- Message-queue growth and excess computation could make the VM unresponsive
  until a watchdog reset. The authors argue that queue monitoring,
  rate-limiting, complete receive patterns, and work distribution remain
  application responsibilities.
- With their LoRa settings, single-byte messages were stable every 290 ms.
  Payloads above 27 bytes at that interval lost data; increasing the interval
  to 350 ms resolved the observed loss. The C++ sender did not lose 27-byte
  payloads under the same test.
- AtomVM left 210,092 bytes free in the LoRa test, versus 364,220 bytes for
  C++, a difference of 154,128 bytes. Both stacks were usable within the much
  slower legal duty cycles relevant to their LoRa deployment assumptions.
- The authors found Erlang development and CLI automation faster than their
  C++/Arduino workflow, but reported missing OTP behavior features and a
  process-cleanup memory leak in the AtomVM version they tested.

## Relevance

This is the strongest located quantitative evidence that AtomVM's process and
supervision model is usable on a small MCU. It also identifies the OS-relevant
failure surfaces: mailbox backpressure, global OOM, native driver throughput,
watchdog policy, and the resource cost of supervision.

## Limits

The results are specific to ESP32-S3 boards, the authors' AtomVM state,
applications, heap behavior, LoRa driver and radio configuration. The paper
does not supply a concise immutable AtomVM commit in its main text. Some of its
feature descriptions are now obsolete: current development code includes
256-bit integers, substantially expanded supervision, and distribution in
mainline. Process maxima are exhaustion tests, not recommended operating
points. Power measurements include the whole board and software stack, and the
authors explicitly flag unexpected C++/AtomVM radio-power results as a likely
configuration or software issue.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [Kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
