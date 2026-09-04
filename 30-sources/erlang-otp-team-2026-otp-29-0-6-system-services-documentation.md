---
title: "Erlang/OTP 29.0.6 system-services documentation"
kind: source
created: "2026-09-03"
authors:
  - "Erlang/OTP project"
published: 2026
citation_key: "erlang-otp-team-2026-otp-29-0-6-system-services-documentation"
container: "Erlang/OTP 29.0.6 documentation"
edition: "OTP 29.0.6; stdlib 8.0.4; kernel 11.0.3; SASL 4.4; SSL 11.7.5"
isbn: null
doi: null
url: "https://www.erlang.org/doc/system/design_principles.html"
accessed: "2026-09-03"
tags:
  - erlang
  - otp
  - supervision
  - system-services
aliases:
  - "OTP 29.0.6 service documentation"
---

# Erlang/OTP 29.0.6 system-services documentation

## Reference

Erlang/OTP project. *Erlang/OTP 29.0.6 Documentation*. The primary reading set,
all accessed 2026-09-03, comprised:

- [OTP design principles](https://www.erlang.org/doc/system/design_principles.html),
  [supervisor behaviour](https://www.erlang.org/doc/system/sup_princ.html),
  [`supervisor`](https://www.erlang.org/doc/apps/stdlib/supervisor.html),
  [applications](https://www.erlang.org/doc/system/applications.html), and the
  [application API](https://www.erlang.org/doc/apps/kernel/application.html);
- the [application resource-file
  format](https://www.erlang.org/doc/apps/kernel/app.html) and [distributed
  applications](https://www.erlang.org/doc/system/distributed_applications.html);
- [`gen_server`](https://www.erlang.org/doc/apps/stdlib/gen_server.html),
  [`gen_statem`](https://www.erlang.org/doc/apps/stdlib/gen_statem.html),
  [`gen_event`](https://www.erlang.org/doc/apps/stdlib/gen_event.html), and
  [`sys`](https://www.erlang.org/doc/apps/stdlib/sys.html);
- [release handling](https://www.erlang.org/doc/system/release_handling.html),
  [`release_handler`](https://www.erlang.org/doc/apps/sasl/release_handler.html),
  [`appup`](https://www.erlang.org/doc/apps/sasl/appup.html), and [code
  loading](https://www.erlang.org/doc/system/code_loading.html);
- [registered processes and process
  aliases](https://www.erlang.org/doc/system/ref_man_processes.html),
  [`global`](https://www.erlang.org/doc/apps/kernel/global.html), and
  [`pg`](https://www.erlang.org/doc/apps/kernel/pg.html);
- [distributed Erlang](https://www.erlang.org/doc/system/distributed.html),
  the [distribution
  protocol](https://www.erlang.org/doc/apps/erts/erl_dist_protocol.html),
  [TLS distribution](https://www.erlang.org/doc/apps/ssl/ssl_distribution.html),
  and the [secure coding
  guidelines](https://www.erlang.org/doc/system/secure_coding.html); and
- [Logger](https://www.erlang.org/doc/apps/kernel/logger.html), the
  [logging guide](https://www.erlang.org/doc/apps/kernel/logger_chapter.html),
  [SASL](https://www.erlang.org/doc/apps/sasl/sasl_app.html),
  [`proc_lib`](https://www.erlang.org/doc/apps/stdlib/proc_lib.html), and
  [`alarm_handler`](https://www.erlang.org/doc/apps/sasl/alarm_handler.html).

## Research question or contribution

What public behaviour does contemporary OTP provide above ERTS for reusable
servers, state machines, supervision, application lifecycle, releases,
distribution, configuration, and operational logging?

## Method

The current rendered manuals were read as public semantic and operational
documentation. Behaviour callback protocols, supervisor flags, application
start and stop rules, registry guarantees, release workflows, distribution
warnings, and Logger overload controls were compared with the older pinned OTP
29.0.5 documentation and source audit already in this archive. Statements were
classified as public behavior, documented implementation, or Atom OS
inference. No OTP node was started, no benchmark was run, and no implementation
detail was inferred solely from a module name.

## Findings

- OTP behaviours separate a reusable protocol engine from application callback
  code. `gen_server` distinguishes correlated synchronous calls from
  asynchronous casts. A caller time-out stops waiting but does not cancel work
  accepted by the server; aliases prevent many late replies from polluting the
  caller's mailbox. `terminate/2` is not guaranteed on every abrupt exit.
- `gen_statem` makes states, event types, delayed replies, postponed events,
  internal events, time-outs, state entry, and code change explicit. Postponed
  events can remain postponed indefinitely, and a code-change state rewrite is
  not an ordinary state transition.
- `gen_event` runs a dynamic handler set through one event-manager process.
  Handler failure can be isolated logically, but a slow handler can delay the
  manager and other handlers. `sys` supplies a common cooperative management
  protocol; suspension, inspection, code change, and termination still depend
  on the target servicing system messages. A successful `sys:terminate`
  request is asynchronous and does not itself prove the target has terminated.
- Supervisors start children in specification order, stop them in reverse
  order, apply `one_for_one`, `one_for_all`, or `rest_for_one` restart policy,
  and terminate when configured restart intensity is exceeded so policy can
  escalate upward.
- Supervisor start, restart, and manual termination operations execute
  synchronously in the supervisor process. Long child start or shutdown paths
  can therefore make the supervisor unresponsive. With the default
  `auto_shutdown = never`, a child cannot be significant.
  `any_significant` initiates shutdown when one significant child terminates
  by itself, whereas `all_significant` waits until the last significant child
  has done so. A `transient` significant child counts after a normal or
  shutdown exit but restarts after an abnormal exit; a `temporary` significant
  child counts after any exit; and a `permanent` significant child is invalid.
  Manual termination and termination caused by a sibling restart strategy do
  not trigger automatic shutdown.
- The application controller coordinates application loading and lifecycle.
  It checks declared dependencies and, for a startable non-library application,
  creates an application master around the top process returned by the application
  callback. That process is commonly a supervisor but is not required to be
  one; a library application has no callback or application master. The
  application master is the group leader for associated application processes;
  when the master terminates, those processes can be killed even if they are
  not in a supervision tree, and that association supports
  `application:get_application/1`.
  `application:start` checks required applications but does not recursively
  start them. `ensure_all_started` performs recursive startup and can start
  independent dependencies concurrently, but rollback stops only applications
  started by that operation, not their external effects.
- OTP application `restart_type` is `permanent`, `transient`, or
  `temporary` and determines whether application termination escalates to
  stopping the runtime system. Independently, the application callback receives
  `normal`, `takeover`, or `failover` as its `start_type`. These axes
  must not be collapsed into one generic restart reason.
- Application resource files declare modules, dependency classes, registered
  names, environment values, callback modules, and runtime dependencies.
  Loading the resource does not load all code. Mutable `set_env` updates are
  neither reactive nor one transaction across consumers.
- A local registered name aliases one current process and is removed on death;
  `via` permits alternate registries. Lookup and send remain separate, and a
  name is not authority. `global` aims at unique replicated names over a
  connected node set, but its registration and lock services are documented
  as unreliable unless both `connect_all` and
  `prevent_overlapping_partitions` are enabled; the affected API calls can
  still return rather than reporting that their result is unreliable. `pg`
  provides temporarily divergent, strongly eventually consistent groups and
  does not make membership transitive across merely indirect connections.
  They are not interchangeable.
- OTP release handling stages packages and executes explicit upgrade
  instructions. State-format changes require suspension, a `code_change`
  callback, and resumption; core runtime changes require a restart of the
  Erlang runtime system through `restart_new_emulator`/`heart`, not necessarily
  a hardware or host-operating-system reboot. The manual
  warns that circular dependencies and concurrently running unaffected
  processes make upgrades difficult. Each node has its own release handler and
  nodes can run different releases. Loading a third module version requires
  purging the old one and can terminate processes still executing it.
  Low-level `appup`/`relup` instructions can also invoke arbitrary
  `{M,F,A}` code, so they are executable migration programs rather than a
  declarative or automatically attenuated transaction.
- Standard distribution makes remote actor messaging convenient, but the
  manuals describe connected nodes as fully trusted. Default distribution
  traffic is cleartext and the cookie challenge is not cryptographically
  secure. TLS with peer verification can authenticate connections, but
  authenticated nodes still receive ambient node authority; authentication is
  not per-operation authorization.
- Distributed applications separate placement/failover from naming and can
  have an old and new instance alive during takeover. The documented mechanism
  is not consensus, a fencing lease, or proof of singleton external effects.
- Logger is itself a configurable service with filters and handlers. The
  built-in standard and disk handlers use synchronization, rate limits, event
  dropping, and optional termination/restart as distinct overload responses.
  Arbitrary handler callbacks can execute work in the emitting process,
  handler order is unspecified, and proxy paths may drop events.
- `proc_lib` crash reports and supervisor/progress events flow through Logger
  and inherit its delivery limits; since OTP 21 these are Logger events rather
  than reports owned by SASL. The standard alarm handler explicitly lacks a
  complete alarm-management model and its retained list can grow without a
  system-level cardinality policy.

## Relevance

These pages define the compatibility vocabulary for an OTP-like Atom OS
service layer, but they do not require copying OTP's current application
controller, global registry, release scripts, ambient node trust, or mutable
configuration model. The proposed layer can preserve behaviour protocols and
supervision structure while adding capability authorization, domain
incarnations, durable lifecycle records, explicit overload state, and secure
distribution.

The sharpest reusable lessons are negative as well as positive: a call time-out
is not cancellation; supervisor restart is not persistent-state recovery;
distributed takeover is not sink fencing; `global` and `pg` express
different consistency goals; release installation is not cluster-atomic; and
Logger is not a complete audit log.

## Limits

Documentation describes supported behaviour, not a proof, representative
performance result, or complete failure model. Some semantics are specific to
the current OTP implementation and host operating system. The pages do not
establish crash consistency for application state, safe retry of external
effects, Byzantine tolerance, or hardware isolation between actors.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
