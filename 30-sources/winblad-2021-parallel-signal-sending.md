---
title: "The Many-to-One Parallel Signal Sending Optimization"
kind: source
created: "2026-09-02"
authors:
  - "Kjell Winblad"
published: "2021-11-05"
citation_key: "winblad-2021-parallel-signals"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/parallel-signal-sending-optimization/"
accessed: "2026-09-02"
tags:
  - erlang
  - erts
  - mailboxes
  - multicore
  - scalability
aliases:
  - "Parallel signal sending optimization"
---

# The Many-to-One Parallel Signal Sending Optimization

## Reference

Kjell Winblad. “[The Many-to-One Parallel Signal Sending
Optimization](https://www.erlang.org/blog/parallel-signal-sending-optimization/).”
*Erlang/OTP Blog*, 2021-11-05. Accessed 2026-09-02.

## Contribution

The article explains an adaptive OTP 25 optimization for the contention that
many concurrent senders can create on one receiving process’s off-heap signal
queue. It demonstrates how a weak public ordering guarantee can permit a more
parallel implementation.

## Method

The author describes the old lock and queue paths, the replacement array of
sender-hashed buffers, adaptive activation and deactivation, and a configurable
many-to-one microbenchmark on a 32-core, 64-hardware-thread machine.

## Findings

- The older off-heap path serialized senders on one outer-signal-queue lock;
  on-heap delivery could additionally contend on the receiver’s main lock.
- Because order is required only within each sender-destination pair, senders
  can be hashed into separate FIFO buffers without imposing a total order among
  senders.
- The optimization activates after observing lock contention and later
  deactivates when enqueue density falls, limiting its cost in uncontended
  cases.
- In the extreme small-message benchmark, reported receive throughput at 16
  senders was 520 times the old implementation. The advantage was smaller for
  larger messages, and one receiver thread remained the ultimate processing
  bottleneck.
- The author explicitly warns that real applications do more work and should
  not be expected to reproduce the microbenchmark ratio.

## Relevance

The result recommends a semantic-first mailbox design. Atom OS should specify
only the ordering applications require, then allow striped ingress queues,
batching, and adaptive contention control behind that contract. The benchmark
also shows why send throughput, queue admission, and receiver drain rate must
be reported separately: making producers faster can worsen backlog when the
single consumer cannot keep up.

## Limits

This is an official maintainer article and focused microbenchmark, not an
independent application study. It covers one ERTS implementation path and
off-heap queue setting. It does not evaluate bounded admission, selective
receive scan cost, garbage-collection tails, adversarial fan-in, NUMA placement,
or end-to-end service recovery.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Signal ingress, mailboxes, and selective receive](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
