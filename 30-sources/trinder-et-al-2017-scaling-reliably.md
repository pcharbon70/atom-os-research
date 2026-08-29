---
title: "Scaling Reliably: Improving the Scalability of the Erlang Distributed Actor Platform"
kind: source
created: "2026-08-28"
authors:
  - "Phil Trinder"
  - "Natalia Chechina"
  - "Nikolaos Papaspyrou"
  - "Konstantinos Sagonas"
  - "Simon Thompson"
  - "Stephen Adams"
  - "Stavros Aronis"
  - "Robert Baker"
  - "Eva Bihari"
  - "Olivier Boudeville"
  - "Francesco Cesarini"
  - "Maurizio Di Stefano"
  - "Sverker Eriksson"
  - "Viktória Fordós"
  - "Amir Ghaffari"
  - "Aggelos Giantsios"
  - "Rickard Green"
  - "Csaba Hoch"
  - "David Klaftenegger"
  - "Huiqing Li"
  - "Kenneth Lundin"
  - "Kenneth MacKenzie"
  - "Katerina Roukounaki"
  - "Yiannis Tsiouris"
  - "Kjell Winblad"
published: "2017-08-17"
citation_key: "trinder-et-al-2017-scaling-reliably"
container: "ACM Transactions on Programming Languages and Systems"
edition: "39(4), Article 17, 17:1-17:46; preprint arXiv:1704.07234v2"
isbn: null
doi: "10.1145/3107937"
url: "https://doi.org/10.1145/3107937"
accessed: "2026-08-28"
tags:
  - distributed-systems
  - erlang
  - fault-tolerance
  - scalability
aliases:
  - "Scaling Reliably"
---

# Scaling Reliably: Improving the Scalability of the Erlang Distributed Actor Platform

## Reference

Phil Trinder et al. “[Scaling Reliably: Improving the Scalability of the Erlang
Distributed Actor Platform](https://doi.org/10.1145/3107937).” *ACM
Transactions on Programming Languages and Systems* 39, no. 4 (2017), Article
17, pages 17:1–17:46. DOI 10.1145/3107937. The complete [arXiv
preprint](https://arxiv.org/abs/1704.07234), version 2, was read. Work from the
RELEASE EU FP7 STREP project.

## Research question or contribution

The article asks where Erlang's reliable actor model stops scaling on large
multicore, NUMA, and distributed systems, then reports coordinated changes at
the VM, language/library, and tooling levels. Its central distributed-language
contribution is Scalable Distributed Erlang and the s_group construct.

## Method

The project combines:

- measurement and optimization of VM structures on multicore and NUMA hosts;
- a semantics and executable model for s_group operations with generated
  QuickCheck tests against the implementation;
- distributed Orbit and ant-colony-optimization case studies;
- Chaos Monkey process-failure experiments; and
- performance runs on several systems, with the largest key experiments using
  the Athos cluster at 256 hosts and 6,144 cores.

Some reported distributed experiments used Erlang/OTP 17.4 and project-specific
SD Erlang libraries and tools.

## Findings

- Standard distributed Erlang tends toward a fully connected node graph and a
  global process-name namespace. Both create coordination and communication
  costs as node counts grow.
- s_groups partition connections and names into explicit groups while allowing
  nodes to belong to multiple groups. This reduces mandatory global state and
  lets topology follow application structure.
- In the selected Orbit and ant-colony workloads, partitioning improved scale
  beyond the standard distributed-Erlang limits observed by the project. Some
  configurations were still scaling at 256 hosts and 6,144 cores.
- Maintaining global recovery information dramatically constrained the
  ant-colony workload. Partitioning recovery data restored scalability,
  demonstrating tension between global fault-tolerance metadata and scale.
- Chaos Monkey experiments showed the evaluated supervised variants recovering
  from injected process failures. This validates those recovery paths under the
  tested faults, not arbitrary node, storage, network, or correlated failures.
- Scalability work also required VM and tooling changes; a language-level actor
  abstraction did not eliminate runtime, observability, deployment, or
  persistent-state bottlenecks.

## Relevance

The paper supports explicit failure domains, partitioned namespaces, and local
recovery data as OS design principles. A new distribution layer should not make
all nodes mutually connected and mutually authoritative merely to preserve a
uniform send syntax.

It also demonstrates that supervision metadata has a cost. Reliability policy
should be hierarchical and colocated with the scope it protects, with only the
minimum necessary state coordinated globally.

## Limits

This source is a peer-reviewed project synthesis with many authors and
components, not a clean comparison of one isolated mechanism. The largest results are
application-, topology-, hardware-, tool-, and OTP-version-specific. They do
not establish a current 60-node Erlang limit or guarantee that arbitrary
applications scale to 256 hosts. Injected process failures are narrower than
machine loss, Byzantine behavior, storage corruption, or network partitions.
The s_group API and exact VM optimizations are historical design evidence, not
requirements for a new kernel.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
