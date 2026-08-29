---
title: "A brief introduction to BEAM"
kind: source
created: "2026-08-28"
authors:
  - "John Högberg"
published: "2020-10-20"
citation_key: "hogberg-2020-beam-primer"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/a-brief-BEAM-primer/"
accessed: "2026-08-28"
tags:
  - beam
  - erts
  - instruction-sets
  - virtual-machines
aliases:
  - "BEAM primer"
---

# A brief introduction to BEAM

## Reference

John Högberg. “[A brief introduction to
BEAM](https://www.erlang.org/blog/a-brief-BEAM-primer/).” Erlang/OTP Blog,
2020-10-20. Accessed 2026-08-28.

## Contribution

This official engineering primer introduces the BEAM instruction machine so
readers can follow the OTP 24 JIT series. Its most important contribution to
this archive is a precise boundary between BEAM and ERTS.

## Method

Högberg compiles small Erlang functions to symbolic BEAM instructions and
walks through registers, calls, allocation, garbage-collection liveness,
exceptions, and selective receive.

## Findings

- BEAM is frequently confused with ERTS. In the author's distinction, BEAM is
  the VM that executes instructions and has no direct notion of processes,
  ports, or ETS; those are ERTS facilities.
- BEAM is a register machine. X registers carry temporary values, arguments,
  and results; Y registers are tied to stack frames.
- Allocation instructions carry liveness information so garbage collection
  can retain valid registers. Calls are scheduling points and constrain which
  registers remain live.
- The instruction stream makes recursion, function calls, exception handlers,
  heap checks, and selective mailbox scanning explicit.

## Relevance

The article prevents a category error at the center of the OS research. Cheap
processes, signals, mailboxes, and supervision are not properties of the BEAM
instruction set alone. A project can adopt those principles without using
BEAM bytecode, or execute BEAM bytecode without having implemented the broader
ERTS and OTP behavior users expect.

The explicit register and liveness model is still useful design material for a
portable managed-code layer and for predictable safe points.

## Limits

This is a concise tutorial, not an instruction-set specification, compatibility
contract, or performance evaluation. It predates the production release of
BeamAsm in OTP 24 and intentionally leaves ERTS implementation details to other
material.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
