---
title: "OTP 29.0.6 generic behaviour call protocol"
kind: source
created: "2026-09-06"
authors: ["Erlang/OTP contributors"]
published: null
citation_key: "erlang-otp-team-2026-otp-29-0-6-generic-behaviour-call-protocol"
container: "Erlang/OTP source repository"
edition: "Tag OTP-29.0.6; selected gen.erl paths only"
isbn: null
doi: null
url: "https://raw.githubusercontent.com/erlang/otp/OTP-29.0.6/lib/stdlib/src/gen.erl"
accessed: "2026-09-05"
tags:
  - beam
  - compatibility
  - otp
  - signals
aliases: []
---

# OTP 29.0.6 generic behaviour call protocol

## Reference

Erlang/OTP contributors. [OTP 29.0.6 generic behaviour call protocol](https://raw.githubusercontent.com/erlang/otp/OTP-29.0.6/lib/stdlib/src/gen.erl). Erlang/OTP source repository. Publication date not established. Tag OTP-29.0.6; selected gen.erl paths only. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to beam profile, loader, and conformance in the CLI-first operating-system proof of concept.

## Method

Read tagged lib/stdlib/src/gen.erl, especially lines 217–262, and cross-check the finite/infinite branches. No compiled artifact was generated.

## Findings

The finite-timeout do_call path uses monitor-linked aliases, send/3 options, demonitor flushing and a final zero-time receive. Its local infinite-timeout path avoids aliases. This changes the runtime feature closure of superficially similar workloads.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

One source file is not an OTP 29.0.6 source-tree audit or an exact opcode census. The older 29.0.5 source record retains its original scope; other failed fetches were not treated as evidence.

## Derived work

- [BEAM profile, loader, and conformance](../20-notes/proof-of-concept-requirements/beam-profile-loader-and-conformance.md)
