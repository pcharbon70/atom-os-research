---
title: "Sagas"
kind: source
created: "2026-09-03"
authors:
  - "Hector Garcia-Molina"
  - "Kenneth Salem"
published: 1987
citation_key: "garcia-molina-salem-1987-sagas"
container: "Proceedings of the 1987 ACM SIGMOD International Conference on Management of Data"
edition: "SIGMOD '87, 249–259; ACM SIGMOD Record 16(3)"
isbn: "0-89791-236-5"
doi: "10.1145/38713.38742"
url: "https://doi.org/10.1145/38713.38742"
accessed: "2026-09-03"
tags:
  - compensation
  - fault-tolerance
  - recovery
  - system-services
  - transactions
  - workflow
aliases:
  - "Saga transactions"
---

# Sagas

## Reference

Hector Garcia-Molina and Kenneth Salem.
“[Sagas](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf).”
*Proceedings of the 1987 ACM SIGMOD International Conference on Management of
Data (SIGMOD '87)*, pages 249–259, San Francisco, California, May 27–29,
1987; also *ACM SIGMOD Record* 16, no. 3. DOI
[10.1145/38713.38742](https://doi.org/10.1145/38713.38742). The complete
conference paper and the longer [Princeton technical report
TR-070-87](https://www.cs.princeton.edu/techreports/1987/070.pdf) were
consulted.

## Research question or contribution

The paper asks how a long-lived transaction can release database resources
between steps without abandoning a system guarantee that unfinished work will
be completed or amended. It introduces the saga as a sequence of ordinary
atomic transactions paired with application-defined compensating transactions
and discusses backward recovery, forward recovery, logging, implementation on
an existing database, parallel sagas, and application design.

## Method

This is a conceptual transaction model and implementation analysis rather than
an empirical performance evaluation. The authors define valid execution
sequences, work through airline, banking, purchase-order, and other examples,
and show how a saga execution component can use a durable log and a conventional
transaction execution component. They then sketch an add-on implementation
using database tables and a restartable saga daemon, and generalize the
sequential model to parallel execution.

## Findings

- A saga decomposes a long-lived transaction into committed transactions
  `T1 ... Tn` that may interleave with other transactions. For each transaction
  that may need undoing, the application supplies a compensating transaction
  `Ci`. A successful execution completes every `Ti`; an interrupted prefix is
  amended by executing corresponding compensations in reverse order.
- Compensation is semantic, not restoration of an old physical snapshot. A
  cancellation transaction must preserve current database consistency after
  intervening work; it cannot blindly restore the value that existed before
  its forward transaction.
- Sagas deliberately give up isolation at the outer level. Other transactions
  may observe a partially executed saga, and the model neither aborts nor
  notifies those observers when a later compensation runs. A compensated
  history is therefore not equivalent to the partial history having been
  invisible.
- Recovery requires durable control state. Saga commands and compensation
  identifiers and parameters are logged before their actions. After a crash,
  ordinary transaction recovery completes first; the saga executor then scans
  the log, discovers unfinished work, and resumes forward execution or runs
  outstanding compensations.
- Backward recovery uses compensations. Forward recovery uses reliable code
  and save points and assumes missing transactions will eventually succeed if
  retried enough. The paper also permits mixed recovery: compensate back to a
  save point, restore process state, and execute forward again.
- The code and parameters needed for future forward or compensating steps are
  part of the recoverability obligation. The authors propose reliably retaining
  saga code or storing it with the database, because a durable log is useless
  if the implementation of an old outstanding compensation disappears.
- Compensation can itself contain a persistent bug or encounter an
  unrecoverable condition. The paper does not hide this: the saga can become
  stuck, requiring alternate recovery code or manual intervention. While it is
  pending, it need not retain the long-lived database locks that motivated the
  model.
- The mechanism need not be built into a database. The paper sketches saga
  tables plus an always-running daemon that is restarted after a crash, scans
  pending saga state, and issues the next forward or compensating transaction.
  Parallel sagas are possible, but their fork/join structure constrains safe
  compensation ordering.

## Relevance

An OTP-like workflow or release coordinator cannot obtain atomicity merely by
supervising and restarting actors. For operations that cross persistent stores,
devices, network peers, or service versions, it needs a durable workflow record,
explicit step outcomes, stable operation identities, and application-defined
forward and compensating actions. Retries and compensations should be
idempotent, and the exact code/schema needed to finish an already-started
workflow must remain available.

The paper also gives a clean placement result: saga coordination can be an
ordinary restartable service above existing transactional storage. The kernel
and managed actor runtime need not know workflow policy. They provide isolation,
durable-storage access, actor identity, messaging, and failure notification;
the system-services layer owns the log, recovery choice, compensation graph,
deadlines, escalation, and operator repair state.

## Limits

The primary treatment assumes a centralized database system and transactions
with conventional atomicity and durability. It is not a proof of the later
microservice “saga pattern,” does not supply consensus across autonomous
services, and does not solve atomic publication of a database update and a
message. The model weakens isolation and allows observers to act on intermediate
state. It assumes each forward or compensating step can preserve database
consistency and, for pure forward recovery, that retries eventually succeed.
Irreversible actions may have no true compensation, and a compensating action
can fail permanently. The paper offers no exactly-once execution guarantee,
automatic conflict semantics, bounded recovery time, or empirical evaluation
of the proposed performance benefit.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [OTP-like system-services deep-dive journal](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
