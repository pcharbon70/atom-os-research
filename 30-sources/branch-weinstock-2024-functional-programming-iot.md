---
title: "Functional Programming for the Internet of Things: A Comparative Study of Implementation of a LoRa-MQTT Gateway Written in Elixir and C++"
kind: source
created: "2026-08-28"
authors:
  - "Philip Branch"
  - "Phillip Weinstock"
published: "2024-08-29"
citation_key: "branch-weinstock-2024-lora-mqtt"
container: "Electronics 13(17), 3427"
edition: null
isbn: null
doi: "10.3390/electronics13173427"
url: "https://doi.org/10.3390/electronics13173427"
accessed: "2026-08-28"
tags:
  - atom-vm
  - embedded-systems
  - performance
  - research-paper
aliases:
  - "AtomVM LoRa-MQTT comparison"
---

# Functional Programming for the Internet of Things: A Comparative Study of Implementation of a LoRa-MQTT Gateway Written in Elixir and C++

## Reference

Branch, Philip, and Phillip Weinstock. "[Functional Programming for the
Internet of Things: A Comparative Study of Implementation of a LoRa-MQTT
Gateway Written in Elixir and
C++](https://doi.org/10.3390/electronics13173427)." *Electronics* 13, no. 17
(2024): 3427.

## Research question or contribution

The paper compares Elixir and C++ implementations of a LoRa-to-MQTT gateway on
a Raspberry Pi and an ESP32. It asks whether functional programming improves
development structure and how its performance and support ecosystem compare on
low-end IoT hardware.

## Method

The authors built four gateways with the same high-level role. The Raspberry
Pi and ESP32 versions received LoRa messages and forwarded them to MQTT over
Wi-Fi. Offered traffic increased deterministically, with ten-minute runs. The
paper reports throughput, mean interarrival time, and loss. Its ESP32 had about
520 KB RAM and a 160 MHz processor; the AtomVM system mixed Elixir and Erlang.

## Findings

- On the Raspberry Pi, both Elixir and C++ gateways had negligible loss and
  latency up to four messages/s in the tested range.
- On ESP32, both delivered close to all traffic at 0.5 messages/s. At one
  message/s, the Elixir system delivered about 70% of offered traffic. It
  approached collapse above two messages/s.
- At 0.5 messages/s, the authors estimated 0.1–0.2 s latency for both ESP32
  systems. At one message/s, they estimated about 0.5 s for Elixir versus 0.1 s
  for C++.
- The authors valued pattern matching and the direct expression of complex
  logic, but found missing libraries, limited documentation and diagnostics,
  and GPIO/driver problems. Their ESP32 C++ implementation was shorter overall
  because mature libraries hid more low-level work.
- They conclude that functional programming is promising for IoT, while the
  supporting low-end VM and driver ecosystem needed substantial improvement.

## Relevance

The study supplies an early end-to-end workload rather than a microbenchmark.
It reinforces that native drivers, protocol stacks, queueing, and library
maturity can dominate an AtomVM appliance even when the managed application is
small and clear.

## Limits

The paper cites the AtomVM website as accessed 2024-06-04 but does not identify
an exact VM revision, build configuration, heap policy, SDK, or execution mode.
Raw data are available only on request, and the paper calls for more detailed
statistical reproducibility. It is unclear how much loss comes from AtomVM,
application design, LoRa, drivers, or MQTT/Wi-Fi integration. Current AtomVM
has changed substantially, including JIT/AOT work and expanded drivers, so the
numbers are a reproduction target rather than a current capacity limit.

## Derived work

- [AtomVM as an operating-system foundation](../20-notes/atomvm-as-an-operating-system-foundation.md)
- [AtomVM foundation map](../10-maps/atomvm-foundation.md)
- [Kernel-facing-runtime inquiry](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md)
