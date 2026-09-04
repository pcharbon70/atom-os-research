---
title: "Secure audit logs to support computer forensics"
kind: source
created: "2026-09-03"
authors:
  - "Bruce Schneier"
  - "John Kelsey"
published: 1999
citation_key: "schneier-kelsey-1999-secure-audit-logs"
container: "ACM Transactions on Information and System Security, 2(2)"
edition: null
isbn: null
doi: "10.1145/317087.317089"
url: "https://doi.org/10.1145/317087.317089"
accessed: "2026-09-03"
tags:
  - audit
  - cryptography
  - forensics
  - forward-integrity
aliases:
  - "Secure audit logs"
---

# Secure audit logs to support computer forensics

## Reference

Bruce Schneier and John Kelsey. “Secure Audit Logs to Support Computer
Forensics.” *ACM Transactions on Information and System Security* 2(2),
pages 159–176, May 1999. DOI
[10.1145/317087.317089](https://doi.org/10.1145/317087.317089).
[Author-hosted paper](https://www.schneier.com/wp-content/uploads/2016/02/paper-auditlogs.pdf).

## Research question or contribution

What useful integrity and confidentiality guarantees can an audit log retain
after an attacker takes control of the machine that created and stores it? The
paper proposes an append protocol involving an untrusted logging machine, a
trusted machine, evolving authentication keys, encrypted records, and a hash
chain over prior entries.

## Method

The authors define the participants, attacker, cryptographic assumptions, log
record format, initialization and closure protocols, and verification
procedure. Security is argued from one-way key evolution, per-record encryption
keys, authenticated hash chaining, deletion of obsolete keys, and occasional
commitment to a trusted machine. The work is a protocol construction and threat
analysis; it does not include a production implementation or workload
evaluation.

## Findings

- After writing a record, the logger evolves and erases its previous
  authentication key. Under the stated assumptions, compromise of the current
  key does not reveal or permit undetectable modification of earlier records.
- A hash chain commits each new record to all preceding records, allowing a
  trusted verifier to check a log prefix using a compact authenticated value.
- Deriving encryption keys partly from a record's type permits selective
  disclosure to moderately trusted reviewers without giving them authority to
  forge records.
- Periodic interaction with a trusted machine creates an external commitment.
  How often this occurs trades communication availability and bandwidth against
  the maximum interval exposed to undetectable truncation.
- Cryptography can make deletion detectable after later verification; it cannot
  physically prevent deletion from storage controlled by the attacker.

## Relevance

**Atom OS inference:** security audit must be a distinct service and data path,
not a setting on lossy logs or sampled traces. Each record should bind an event
type, actor and protection-domain incarnation, monotonic sequence or epoch,
policy revision, and previous-chain commitment. A user-space audit service can
apply modern forward-secure constructions, encrypt by disclosure class, seal
checkpoints to a remote or independently protected verifier, and manage
retention and export.

The privileged kernel's role should remain narrow: provide trustworthy domain
identity, monotonic or rollback-resistant evidence where hardware permits,
capability-gated event sources, protected key operations, and a bounded path
for terminal crash records. It should not decide which application events are
auditable or implement forensic query policy.

## Limits

The paper explicitly cannot protect the truth or completeness of records made
after compromise: the attacker controls what the logger observes and writes.
It cannot prevent local deletion, and detects truncation only when the logger
eventually reconnects to a trusted verifier with an earlier commitment. The
model assumes reliable erasure of old key material, strong randomness, a secure
initial relationship with the trusted machine, and then-contemporary
cryptographic primitives; a current implementation must substitute modern
algorithms and analyze rollback, power loss, side channels, key recovery, and
storage exhaustion. Tamper evidence also does not establish that an event was
semantically true or appropriately redacted.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [OTP-like system-services deep-dive journal](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
