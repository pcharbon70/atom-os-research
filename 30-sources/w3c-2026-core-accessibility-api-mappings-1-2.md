---
title: "Core Accessibility API Mappings 1.2"
kind: source
created: "2026-09-04"
authors:
  - "W3C Accessible Rich Internet Applications Working Group"
published: "2026-08-29"
citation_key: "w3c-2026-core-accessibility-api-mappings-1-2"
container: "W3C Candidate Recommendation Draft"
edition: "1.2"
isbn: null
doi: null
url: "https://www.w3.org/TR/2026/CRD-core-aam-1.2-20260829/"
accessed: "2026-09-04"
tags:
  - accessibility
  - interoperability
  - semantics
  - standards
aliases:
  - "Core-AAM 1.2"
---

# Core Accessibility API Mappings 1.2

## Reference

W3C Accessible Rich Internet Applications Working Group. “[Core Accessibility
API Mappings
1.2](https://www.w3.org/TR/2026/CRD-core-aam-1.2-20260829/).” W3C
Candidate Recommendation Draft, 29 August 2026.

## Contribution

Core-AAM specifies how semantic roles, states, properties, relations, actions,
focus, selection, and change events are projected into major platform
accessibility APIs, including UI Automation, AT-SPI, macOS Accessibility, and
Android accessibility.

## Method

This is a normative mapping specification maintained with platform experts and
an implementation test report. It documents interoperable adapter behavior,
not a universal domain model or an empirical comparison of assistive
technology user outcomes.

## Findings

- Platform adapters require explicit mappings for roles, properties, computed
  names, relationships, actions, focus, selection, and mutation events.
- Accessibility APIs expose both relatively durable description and transient
  interaction state; consumers need coherent snapshots plus ordered changes.
- Mapping is not lossless: platforms differ, unsupported semantics require
  defined fallback, and host-language/native semantics can override supplied
  values.
- The specification is largely a publication direction from user agent to
  assistive technology; authorized state-changing actions require a separate
  protocol and security model.

## Relevance

Atom OS can treat Core-AAM adapters as replaceable consumers of its native
semantic protocol. This avoids choosing one existing platform API as the
system's internal truth while providing concrete compatibility targets and
event behavior for assistive clients.

## Limits

Version 1.2 was still a Candidate Recommendation Draft at the accessed date and
may change. Platform support remains heterogeneous. The mapping tables do not
define durable object identity, capability checks, event replay, overload, or
recovery after publisher or adapter failure.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
