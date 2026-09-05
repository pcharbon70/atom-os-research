---
title: "Semantic Observability, Testing, and Assurance"
kind: note
created: "2026-09-05"
maturity: developing
tags:
  - formal-methods
  - observability
  - reliability-engineering
  - software-testing
aliases:
  - "Layer 5 assurance surface"
---

# Semantic Observability, Testing, and Assurance

## Executive decision

Layer 5 should define observability and assurance in **domain terms**. The
application specifies which user-visible outcomes, invariants, pending work,
freshness, reconciliation, and degraded behavior matter. Layer 4 provides
bounded telemetry pipelines, alarms, durable audit, and outcome services; the
managed runtime provides deterministic scheduling controls and low-level traces
where supported. Telemetry is never the authoritative audit or commit ledger.

Every component ships an executable assurance bundle: reference state machine,
properties, generators and shrinkers, deterministic time/random/message
controls, compatibility fixtures, authorization tests, and crash/partition/
overload fault scenarios. Formal models are used selectively where consequence
or protocol complexity warrants them. Neither model checking nor random testing
alone proves the implementation correct.

## Question and operational standard

The component asks: **how will we know an application preserved meaning—not
merely stayed alive—through concurrency, failure, upgrade, and overload?**

It succeeds only if:

- semantic SLIs begin with user-relevant outcomes rather than easy CPU metrics;
- committed, rejected-before-admission, expired-before-admission, fenced,
  accepted-pending, not-committed, terminated, and indeterminate results are
  counted separately, including deadline-elapsed status after acceptance;
- every metric states population, window, measurement point, dimensions, and
  loss/sampling behavior;
- traces correlate work but never authorize it or negate durable evidence;
- redaction and cardinality prevent observability from becoming a data leak or
  denial vector;
- each invariant and protocol has an executable property or explicitly stated
  reason it does not;
- deterministic test controls reproduce actor schedules, time, randomness,
  retries, and message failures;
- native/device/storage/power failures are injected below the pure actor model;
- old/new compatibility is exercised as histories, not only serializer round
  trips;
- model assumptions and implementation conformance are reviewed separately;
  and
- production telemetry is evidence for behavior, not a formal proof.

## Evidence and limits

[QuickCheck](../../30-sources/claessen-hughes-2000-quickcheck.md) demonstrates
executable properties, generated inputs, and counterexample shrinking.
[QuickCheck/PULSE](../../30-sources/claessen-et-al-2009-quickcheck-pulse.md),
[Concuerror](../../30-sources/christakis-et-al-2013-concuerror.md), and [actor
record/replay](../../30-sources/aumayr-et-al-2018-actor-record-replay.md) provide
actor-concurrency precedents with different coverage and overhead limits.

[How AWS Uses Formal Methods](../../30-sources/newcombe-et-al-2015-aws-formal-methods.md)
reports design errors found with small TLA+ specifications in critical
distributed systems. It is first-party experience and the model is not the
code. [Google SRE SLO guidance](../../30-sources/jones-et-al-2016-service-level-objectives.md)
supports starting from behaviors users care about. [Dapper](../../30-sources/sigelman-et-al-2010-dapper.md)
and [OpenTelemetry](../../30-sources/opentelemetry-project-2026-specification-1-60.md)
support correlation and bounded telemetry while retaining sampling and
instrumentation limits.

## Semantic SLI catalog

| SLI | Numerator / observation | Denominator / population | Required dimensions |
| --- | --- | --- | --- |
| Committed-correct outcome rate | operations with durable semantic commit satisfying postcondition | admitted operations whose deadline/window closed | command class, tenant class, application generation |
| Rejection rate | rejected before admission by stable reason | attempted operations | reason, caller class, dependency state |
| Pre-admission expiry rate | operations proven unadmitted because their deadlines elapsed | attempted operations | command class, queue/admission path, caller class |
| Accepted deadline-elapsed rate | accepted pending or indeterminate operations observed after their usefulness deadline | admitted operations with elapsed deadlines | command class, workflow/effect stage, age bucket |
| Not-committed proof rate | operations with terminal proof that the named semantic commit did not occur | admitted operations reaching terminal evidence | command class, proof source, retry-policy class |
| Termination rate | workflows/use cases ending under an explicit domain rule, with surviving effects classified | accepted workflows/use cases | reason, compensation/manual-repair state, pivot status |
| Indeterminate rate | outcomes unresolved at observation deadline | admitted external/workflow operations | port, endpoint generation, age bucket |
| Commit latency | admission to durable semantic commit | committed operations | command class, contention, durability profile |
| Terminal workflow latency | durable workflow acceptance to terminal state | terminal workflows | type, result, compensation, pivot status |
| Projection freshness | current authoritative frontier minus observed frontier | projection/query observations | projection, tenant, degraded state |
| Reconciliation lag | age of oldest accepted unknown/pending effect | adapter/workflow partitions | endpoint, operation class, retry state |
| Degraded time | duration in declared semantic degraded mode | service window | dependency, functionality retained/lost |
| Invariant violation | any detected impossible state/history | all validation/recovery observations | invariant ID, generation, source transition |
| Stale/fenced attempt rate | generation/policy/revision rejections | invocations | boundary and stale generation type |

An SLO declares exact percentile or fraction, time window, measurement location,
excluded maintenance, and response when missed. “Availability” is not one
uptime percentage if the service returns stale, wrong, or indeterminate
business results.

## Telemetry taxonomy

| Channel | Properties | Not suitable for |
| --- | --- | --- |
| Metrics | bounded aggregates, low-cardinality dimensions, loss accounted | individual operation proof or forensic detail |
| Traces | sampled causal path with propagated context | authorization, completeness, nonrepudiation |
| Structured logs/events | selected diagnostic facts with redaction | unbounded per-object history or domain source of truth |
| Crash evidence | bounded last-state/protocol/resource snapshot | secrets, arbitrary heap dump, normal business audit |
| Durable outcome ledger | queryable semantic operation result | broad performance exploration |
| Security audit | protected policy/authority/accountability record | high-volume debug trace or proof of business correctness alone |

Trace and correlation IDs are untrusted input. At trust boundaries they are
validated, rate-limited, or replaced while retaining an internal link. A
missing span cannot turn a `Committed` receipt into failure; an emitted span
cannot manufacture a commit.

## Assurance bundle

```text
ApplicationAssuranceProfile {
  model_and_version,
  safety_properties[],
  liveness_properties[],
  generators_and_classifications[],
  history_and_state_shrinkers[],
  reference_interpreter,
  deterministic_scheduler_profile,
  time_and_randomness_profile,
  fault_scenarios[],
  authorization_noninterference_tests[],
  compatibility_fixture_matrix,
  resource_and_overload_tests[],
  implementation_conformance_hooks[],
  known_unmodeled_behavior[]
}
```

The manifest binds an assurance profile digest to an application generation.
Passing old tests is not sufficient if an invariant, authorization rule, or
protocol changes.

## Property-based state-machine testing

Generators create commands, queries, identities, revisions, deadlines, grants,
duplicates, stale generations, crashes, migrations, and dependency failures.
The reference model returns an outcome and next state; the implementation is
observed only through public contracts. Useful properties include:

- every committed state satisfies all declared invariants;
- within the advertised retention epoch, the same operation ID plus the same
  digest causes at most one logical execution, and repeated status queries
  progress monotonically to one stable terminal outcome while allowing
  `AcceptedPending` or `Indeterminate` to resolve;
- within that epoch, the same operation ID plus a different digest is rejected;
- after retention, an unknown/expired ID fails closed rather than becoming a
  fresh command unless an entity-lifetime tombstone proves the old binding;
- no `Committed` outcome lacks its named durable evidence;
- no `NotCommitted` outcome follows a known commit;
- replay and projection rebuild perform no external effect;
- stale routes, leases, views, timers, and policy epochs cannot mutate state;
- compensation never erases evidence of prior visible effects;
- presentation restart cannot change domain state by itself; and
- overload rejection happens before acceptance or leaves a queryable pending
  outcome.

Shrinking preserves causal and validity constraints so a failure reduces to a
small meaningful history rather than an impossible message sequence.

## Deterministic actor simulation

The test realm controls:

- actor scheduling and reduction boundaries;
- message delivery, loss, duplicate, reorder, and delay;
- monitor/link/down-signal order within the modeled contract;
- logical and wall time, timer delivery and lateness;
- random values and ID allocation;
- registry, lease, policy, and code generations;
- persistence completion, torn/failing operations, and recovery; and
- adapter acceptance, commit, reply, and status lookup.

Each run records a seed, model/application versions, schedule choices, and
fault script. Production logic should run in the simulator where feasible, but
simulation fidelity is itself tested against real runtime behavior.

## Formal-model selection

Use a small state/model checker when:

- several actors own a high-consequence safety property;
- cancellation, timeout, retry, migration, or compensation creates many states;
- a lease/fence, consensus, or offline merge protocol is subtle;
- failure can duplicate money, authority, publication, or device actuation; or
- testing has found irreproducible histories.

State the abstraction, safety/liveness properties, fairness assumptions,
bounds, and unmodeled behavior. Then connect model actions to implementation
telemetry and tests. A green model of the wrong system is not assurance.

## Compatibility testing

The corpus includes:

- old/new command, query, event, outcome, state, snapshot, and projection
  encodings;
- all allowed old/new endpoint pairs;
- unknown optional/critical fields and enum values;
- mixed-version workflows through every state and compensation;
- old event replay under new reducer and snapshot validation;
- migration interruption and resume at every checkpoint;
- authorization/policy changes across stored/offline work; and
- rollback before and refusal after irreversible boundaries.

Tests verify behavioral postconditions and resulting histories, not just
successful decoding.

## Infrastructure and fault injection

Actor-level deterministic tests do not model every cache, DMA, device, native
library, filesystem, or power behavior. Integration campaigns therefore:

- kill actors, runtime domains, adapters, device services, and nodes;
- inject storage error, torn/late completion, corruption, and capacity loss;
- partition, duplicate, reorder, and throttle network traffic;
- pause old lease holders beyond expiry and reuse object identifiers;
- exhaust CPU, heap, mailbox, timers, persistence, I/O, telemetry, and
  capability slots;
- crash before/after every commit, outbox, endpoint, reply, checkpoint,
  publication, and teardown transition; and
- compare host-prototype behavior with claimed Atom contracts.

## Privacy and diagnostic authority

Metric labels avoid unbounded tenant/object/user identifiers. Logs and traces
use schema-level redaction before enqueue. Inspectors receive bounded redacted
snapshots through an explicit facet; no generic production heap dump or debug
port is enabled by observability.

The application declares which subject may view semantic outcomes, workflow
state, conflicts, and repair actions. Operators need not receive user content
to learn that an invariant or adapter is failing.

## Overload and observability failure

Telemetry has finite queues and policies to aggregate, sample, coalesce, or
drop with counters. Application work never blocks indefinitely on ordinary
telemetry. Outcome and audit commits use distinct reserved services and fail
admission or enter explicit protected degradation if their required evidence
cannot be retained.

An alarm storm is rate-limited and grouped by stable cause/generation. The
system preserves one actionable current alarm and transition history rather
than an unbounded event per retry.

## Alternatives considered

| Alternative | Decision |
| --- | --- |
| Uptime/CPU alone defines application health | reject; begin with semantic user outcomes |
| Logs are the audit and outcome database | reject; lossy/operator-controlled telemetry has different guarantees |
| Unit examples only | reject for stateful/concurrent protocols; add generated histories and faults |
| Random testing proves correctness | reject; useful bug finding, not proof |
| Model checking proves implementation | reject; connect model to conformance tests and state assumptions |
| Trace context is trusted identity | reject; treat as correlation-only untrusted metadata |
| Full unsampled tracing by default | reject; resource/privacy cost requires explicit bounded profile |
| Production fault injection substitutes for model/tests | reject; use layered complementary evidence |

## Staged implementation and verification

1. Define the first domain's invariant/outcome model and semantic SLIs.
2. Build generated state-machine tests with shrinking against a reference
   interpreter.
3. Add deterministic actor scheduling, virtual time/randomness, and message
   fault control.
4. Model check one workflow/effect protocol and bind actions to implementation
   events.
5. Add persistent crash injection and permanent compatibility fixtures.
6. Emit bounded metrics/traces/logs and verify they cannot block domain work or
   leak redacted fields.
7. Exhaust telemetry while outcome/audit and recovery paths remain correct.
8. Run the same campaign against a host prototype and the first bootable target,
   recording inherited versus Atom-owned behavior.

The design is falsified if telemetry success is used as commit proof, if a
declared invariant lacks a test/model path, if an old/new allowed pair corrupts
state, or if diagnostics can acquire application authority or unbounded
resources.

## Connections

- [Applications and domain services layer](../applications-and-domain-services-layer.md)
- [Observability, audit, alarms, and operator control](../otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)
- [Observability, deterministic testing, and crash evidence](../managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md)
- [Typed commands, queries, events, and protocol contracts](typed-commands-queries-events-and-protocol-contracts.md)
- [Application evolution, schema compatibility, and migration](application-evolution-schema-compatibility-and-migration.md)

## Sources

- [QuickCheck](../../30-sources/claessen-hughes-2000-quickcheck.md)
- [QuickCheck and PULSE](../../30-sources/claessen-et-al-2009-quickcheck-pulse.md)
- [Concuerror](../../30-sources/christakis-et-al-2013-concuerror.md)
- [Actor record/replay](../../30-sources/aumayr-et-al-2018-actor-record-replay.md)
- [How AWS Uses Formal Methods](../../30-sources/newcombe-et-al-2015-aws-formal-methods.md)
- [Service Level Objectives](../../30-sources/jones-et-al-2016-service-level-objectives.md)
- [Dapper](../../30-sources/sigelman-et-al-2010-dapper.md)
- [OpenTelemetry Specification](../../30-sources/opentelemetry-project-2026-specification-1-60.md)
