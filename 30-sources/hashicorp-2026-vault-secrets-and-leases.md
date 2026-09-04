---
title: "Vault secrets, leases, and security model"
kind: source
created: "2026-09-04"
authors:
  - "HashiCorp"
published: null
citation_key: "hashicorp-2026-vault-secrets-and-leases"
container: "Vault documentation"
edition: "Vault v2.x current documentation; lease, security-model, token, and key-rotation pages"
isbn: null
doi: null
url: "https://developer.hashicorp.com/vault/docs/concepts/lease"
accessed: "2026-09-04"
tags:
  - credential-rotation
  - leases
  - secrets
  - security
  - workload-identity
aliases:
  - "Vault lease documentation"
---

# Vault secrets, leases, and security model

## Reference

HashiCorp. “[Lease, Renew, and
Revoke](https://developer.hashicorp.com/vault/docs/concepts/lease),”
“[Security
Model](https://developer.hashicorp.com/vault/docs/internals/security),”
“[Tokens](https://developer.hashicorp.com/vault/docs/concepts/tokens),” and
“[Key Rotation](https://developer.hashicorp.com/vault/docs/internals/rotation).”
Vault v2.x documentation, accessed 2026-09-04.

## Research question or contribution

The selected official documentation explains how a production secret service
binds dynamic credentials and service tokens to renewable, revocable
time-to-live leases; authenticates and authorizes requests; encrypts backend
state; rotates internal keys; and records accountable access. It is used here
as practitioner evidence about credential lifecycle, not as a blueprint for an
Atom OS root authority.

## Method

The current rendered pages were read together because a lease without its
security and token context is easy to misinterpret. Documented behavior was
separated from the stronger properties Atom OS would need to prove. No Vault
instance, storage backend, plugin, benchmark, failure injection, or source-code
audit was performed. The pages are living product documentation and therefore
record the access date and displayed version family.

## Findings

- Each dynamic secret and service-type token has a lease with an identifier,
  duration, renewability, and expiry. A renewal request proposes a new interval
  from the current time; the backend may return a shorter interval, so clients
  must inspect the response rather than assume success or additive extension.
- Expiry causes automatic revocation, and authorized operators can revoke one
  lease or a prefix tree. Revoking a parent service token normally revokes its
  descendants and associated leases, which makes delegation topology relevant
  to incident response.
- Dynamic credentials can let each workload use a distinct, short-lived
  principal rather than sharing a static secret. Actual invalidation depends
  on the external secret engine completing its revoke operation; a local lease
  record alone cannot erase a copied credential or force a remote sink to
  reject it.
- The documented security model requires authenticated and authorized client
  requests, encrypted and integrity-protected storage, protected transport,
  and auditable interactions. It explicitly excludes several powerful threats,
  including arbitrary backend control, host code execution, running-process
  memory inspection, malicious plugins, and compromised clients.
- Vault distinguishes keys used for stored-data encryption, sealing, unsealing,
  and online upgrade. Key rotation is a lifecycle with availability and
  persistence consequences, not a single in-memory replacement.
- Audit-before-release can improve accountability, but the documentation's
  guarantee depends on enabled and healthy audit devices and on the surrounding
  storage/export path.

## Relevance

Atom OS should keep ordinary immutable configuration separate from sensitive
credential delivery. A confined identity/secret broker derives caller identity
from a generation-bound local channel, authorizes a narrowly scoped request,
and returns a non-exportable key handle where possible or a protected secret
lease otherwise. The response names credential generation, audience/resource,
expiry, renewability, and revocation lineage. Consumers enter jeopardy before
expiry and must tolerate issuer unavailability according to an explicit
service profile.

Vault's limitations are equally instructive. Revocation becomes effective only
where enforcement occurs, so Atom OS must name the validating sink and its
freshness behavior. A copied bearer secret cannot be recalled by deleting a
registry row. The broker needs an outer recovery holder and reserved resources,
while no service should receive a universal root token merely because it is a
supervisor or operator tool.

## Limits

These pages document one evolving product. They are not a formal model or an
independent security evaluation, and some features vary by edition and storage
backend. Vault assumes an underlying host, TLS stack, storage system,
administrative ceremony, and plugin boundary unlike Atom OS. Its explicit
threat-model exclusions prevent inferring protection after host compromise or
client secret exfiltration. TTL expiry and requested revocation do not prove
instant external invalidation. The version must be repinned if product
semantics materially change.

## Derived work

- [Configuration, workload identity, and secrets](../20-notes/otp-like-system-services-components/configuration-workload-identity-and-secrets.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)
- [Key and secret service](../20-notes/authentication-and-authorization-components/key-and-secret-service.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
