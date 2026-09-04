---
title: "Erlang/OTP 24 Highlights"
kind: source
created: "2026-09-03"
authors:
  - "Lukas Larsson"
published: "2021-05-12"
citation_key: "larsson-2021-erlang-otp-24-highlights"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/My-OTP-24-Highlights/"
accessed: "2026-09-03"
tags:
  - erlang
  - otp
  - process-aliases
  - supervision
aliases:
  - "OTP 24 highlights"
---

# Erlang/OTP 24 Highlights

## Reference

Lukas Larsson. “[Erlang/OTP 24
Highlights](https://www.erlang.org/blog/My-OTP-24-Highlights/).” *Erlang/OTP
Blog*, 2021-05-12. Accessed 2026-09-03.

## Contribution

This official release article presents selected Erlang/OTP 24 changes from a
maintainer's perspective. The parts used by the system-services research
explain why process aliases were introduced for late replies and why EEP-56
added significant children and supervisor automatic shutdown.

## Method

The author combines motivating failure scenarios, small Erlang examples, and
links to the relevant EEPs and manuals. This is an engineering release
overview, not an independent experiment or a normative specification. The
current OTP 29 manuals were read separately for exact compatibility semantics.

## Findings

- A timed-out request/reply caller can deactivate its monitor alias so a later
  reply sent to that alias is dropped rather than delivered to the caller's
  mailbox. The article states that OTP's standard behaviours adopted this
  mechanism behind their call protocols.
- The remote process can continue computing after the caller times out: the
  motivating problem is that the callee does not know the reply is no longer
  wanted. Alias deactivation controls the reply destination, not the accepted
  work.
- Before automatic shutdown, a child trying to terminate its own supervisor
  hierarchy needed knowledge of the relevant supervisor and child identifier.
  Calling synchronous `supervisor:terminate_child/2` from within that hierarchy
  could also deadlock while the supervisor attempted to terminate the caller.
- EEP-56 lets a child be marked significant so its own termination can trigger
  supervisor shutdown without that child navigating the hierarchy or making a
  synchronous self-termination request.
- The article also reports broader OTP 24 changes, including BeamAsm, improved
  receive optimization, richer error information, an optional `socket` backend
  for `gen_tcp`, and documentation chunks. Those features were not evidence for
  the system-services conclusions drawn from this source.

## Relevance

The process-alias example preserves an important contract boundary for Atom OS:
a call timeout can revoke a reply destination without cancelling work or
proving whether an effect occurred. That supports generation-bound reply
handles and explicit cancellation/outcome protocols rather than treating
timeout as abort.

The automatic-shutdown example supports finite-work supervision in ordinary
service policy. It also shows why a child should be able to signal completion
without acquiring broad knowledge or control authority over its supervisor
tree. Exact OTP compatibility still comes from the current supervisor manual,
not this historical overview.

## Limits

This is a maintainer-selected highlight article for OTP 24, not a complete
release record, formal model, peer-reviewed study, or current specification.
It does not state the full `auto_shutdown` rules for `any_significant`,
`all_significant`, restart types, manual termination, or sibling-driven
termination. It does not show that aliases cancel server work or resolve an
external effect's outcome. Performance anecdotes elsewhere in the article are
machine- and workload-specific and do not establish general bounds.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
