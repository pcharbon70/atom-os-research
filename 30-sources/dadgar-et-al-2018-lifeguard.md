---
title: "Lifeguard: Local Health Awareness for More Accurate Failure Detection"
kind: source
created: "2026-09-10"
authors:
  - "Armon Dadgar"
  - "James Phillips"
  - "Jon Currey"
published: "2018-04-03"
citation_key: "dadgar-et-al-2018-lifeguard"
container: "arXiv preprint"
edition: "arXiv:1707.00788v2; first submitted 2017"
isbn: null
doi: null
url: "https://arxiv.org/abs/1707.00788v2"
accessed: "2026-09-10"
tags:
  - system-services
  - reliability
  - service-architecture
aliases: []
---

# Lifeguard: Local Health Awareness for More Accurate Failure Detection

## Reference

Armon Dadgar, James Phillips and Jon Currey. [Lifeguard](https://arxiv.org/abs/1707.00788v2), revised preprint, 3 April 2018. [Full text](https://arxiv.org/pdf/1707.00788v2).

## Research question or contribution

Can failure detection account for a slow observer?

## Method

Sections III–V describe adaptive probing, suspicion and notification, with controlled message-processing delays and a separate CPU-stress scenario.

## Findings

Local-health feedback reduces false suspicion in the evaluated settings. Independent suspicion reports shorten an initially conservative timer; notifying the suspected member helps refutation.

## Relevance

Proposed Atom OS use: qualify observer progress before triggering recovery; keep suspicion separate from ownership.

## Limits

The controlled experiments use Consul agents sharing a Linux VM and loopback. Results do not prove arbitrary network behavior, Byzantine safety or an Atom OS detection deadline.

## Derived work

- [Internal-service study](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination/observer-health-and-adaptive-failure-suspicion.md).
- [Research session](../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md).
