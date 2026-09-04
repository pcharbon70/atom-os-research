---
title: "Anvil: Verifying liveness of cluster management controllers"
kind: source
created: "2026-09-04"
authors:
  - "Xudong Sun"
  - "Wenjie Ma"
  - "Jiawei Tyler Gu"
  - "Zicheng Ma"
  - "Tej Chajed"
  - "Jon Howell"
  - "Andrea Lattuada"
  - "Oded Padon"
  - "Lalith Suresh"
  - "Adriana Szekeres"
  - "Tianyin Xu"
published: "2024-07-10"
citation_key: "sun-et-al-2024-anvil"
container: "18th USENIX Symposium on Operating Systems Design and Implementation"
edition: "OSDI '24, pages 649–666"
isbn: "978-1-939133-40-3"
doi: null
url: "https://www.usenix.org/conference/osdi24/presentation/sun-xudong"
accessed: "2026-09-04"
tags:
  - controllers
  - formal-verification
  - liveness
  - orchestration
aliases:
  - "Anvil controller verification"
---

# Anvil: Verifying liveness of cluster management controllers

## Reference

Xudong Sun, Wenjie Ma, Jiawei Tyler Gu, Zicheng Ma, Tej Chajed, Jon Howell,
Andrea Lattuada, Oded Padon, Lalith Suresh, Adriana Szekeres, and Tianyin Xu.
“[Anvil: Verifying Liveness of Cluster Management
Controllers](https://www.usenix.org/conference/osdi24/presentation/sun-xudong).”
*18th USENIX Symposium on Operating Systems Design and Implementation (OSDI
'24)*, pages 649–666, July 2024.

## Research question or contribution

Anvil asks how controller implementations—not only abstract protocols—can be
proved to converge despite concurrency, asynchronous APIs, and crashes. It
defines *eventually stable reconciliation*: once desired state stops changing
and the modeled environment eventually behaves, the controller eventually
reaches the goal and remains there.

## Method

The framework combines a temporal specification, a verified controller model,
executable Rust generation, and trusted wrappers around external APIs. The
authors verify three Kubernetes controllers for ZooKeeper, RabbitMQ, and
FluentBit and compare their features and performance with widely used
unverified controllers. Verification exposed progress bugs that ordinary happy
path testing missed.

## Findings

- Reconciliation correctness includes liveness. A controller can preserve
  every local safety assertion yet become permanently stranded in an
  intermediate state after one unlucky crash or concurrent change.
- Eventually stable reconciliation states a useful minimum progress property:
  under eventual environmental stability, repeated reconciliation must reach
  and retain the desired state. It intentionally supplies no fixed convergence
  deadline.
- Controller steps are modeled so an action makes at most one external API
  request before persisting enough state to resume. This reduces the number of
  effect interleavings and makes crash boundaries explicit.
- Observed resource versions and idempotent external operations let the
  controller retry or recompute after conflict. Verification still depends on
  accurate environment and API models.
- Proof artifacts improve assurance for the covered state machine, but
  wrappers, compiler, runtime, operating system, remote services, and liveness
  assumptions remain outside the proved core.

## Relevance

The Atom OS manifest controller should be specified against two obligations:
safety of every published generation and eventual stable reconciliation after
desired state stops changing. Each step should perform one class of external
effect, durably record its operation identity and observed revision, and return
to a replayable state. A timeout leaves an unknown outcome that must be
observed before another effect is attempted.

This property also belongs in component-level controllers. Device reset,
release rollout, configuration adoption, and lifecycle drain can share a
small verified reconciliation skeleton while retaining type-specific safety
rules. Atom OS additionally needs bounded progress profiles for boot and
recovery; ESR alone cannot promise a deadline.

## Limits

The verified controllers target Kubernetes APIs and modeled crash-fault
environments. ESR depends on eventual stability and fairness and does not by
itself prove authorization, secrecy, resource bounds, deadline response,
Byzantine tolerance, storage durability, or correctness of external effects.
Generated code inherits a trusted computing base. The work supports a
verification strategy and liveness property, not direct reuse of Kubernetes or
Anvil as the Atom OS service manager.

## Derived work

- [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md)
- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
