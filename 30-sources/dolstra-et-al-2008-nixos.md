---
title: "NixOS: A Purely Functional Linux Distribution"
kind: source
created: "2026-09-03"
authors:
  - "Eelco Dolstra"
  - "Andres Löh"
published: "2008-09-22"
citation_key: "dolstra-et-al-2008-nixos"
container: "Proceedings of the 13th ACM SIGPLAN International Conference on Functional Programming"
edition: "ICFP '08, 367–378"
isbn: "978-1-59593-919-7"
doi: "10.1145/1411204.1411255"
url: "https://doi.org/10.1145/1411204.1411255"
accessed: "2026-09-03"
tags:
  - configuration-management
  - declarative-systems
  - deployment
  - release-management
  - reproducibility
  - system-services
aliases:
  - "NixOS ICFP paper"
---

# NixOS: A Purely Functional Linux Distribution

## Reference

Eelco Dolstra and Andres Löh. “[NixOS: A Purely Functional Linux
Distribution](https://nixos.org/~eelco/pubs/nixos-icfp2008-final.pdf).”
*Proceedings of the 13th ACM SIGPLAN International Conference on Functional
Programming (ICFP '08)*, pages 367–378, Victoria, British Columbia, Canada,
September 22–24, 2008. DOI
[10.1145/1411204.1411255](https://doi.org/10.1145/1411204.1411255).

## Research question or contribution

The paper asks whether the static configuration of a realistic operating
system—not only individual packages—can be built and managed using a purely
functional deployment model. It presents NixOS, explains its lazy functional
configuration language and input-addressed store model, and evaluates how
closely real Nix builds satisfy the assumed purity.

## Method

The authors construct a working Linux distribution whose package builds,
kernel, initial ramdisk, service descriptions, and most configuration files are
outputs of Nix derivations. They explain the derivation and profile mechanisms,
walk through an NTP service configuration, measure the dependency graph and
evaluation cost of a representative system, and rebuild 485 non-fetch
derivations on two machines to compare 165,927 output files and directories.

## Findings

- Nix derivations describe a graph of build actions and declared inputs. Build
  outputs live in immutable store paths whose names include a cryptographic
  hash of their inputs. Different versions and configurations therefore coexist
  rather than overwrite one another.
- Fixed references between store paths make dependency identity explicit.
  Nix can copy a runtime dependency closure to another machine and garbage
  collect unreachable store objects using profiles as roots. The paper's
  scanner discovers references conservatively from hash strings in outputs;
  this is practical evidence, not a typed proof of every runtime dependency.
- Profiles add an indirection over immutable store generations. Switching one
  symlink exposes a new package set atomically, and switching it back selects a
  previous generation, provided garbage collection has not removed it. Users
  do not observe a half-updated profile namespace.
- NixOS extends this model to static operating-system artifacts. The same
  dependency graph can produce the kernel, initial ramdisk, boot scripts,
  service definitions, configuration files, and top-level system closure.
  Optional configuration changes the dependency graph, so an artifact is kept
  precisely when the generated configuration refers to it.
- Building a configuration is side-effect-free in the intended model, but
  activating it is not. The activation script creates users and mutable links,
  and starts, stops, or restarts services. It compares generated service paths
  to decide which services changed and leaves unaffected services running.
  Mutable runtime state such as `/var` remains conventionally stateful.
- The system profile separates testing from permanence. A configuration can be
  activated without selecting it for the next boot; installing it into the
  profile makes it a boot generation. The bootloader exposes retained
  generations, and rollback can be performed at boot or by selecting an older
  profile and re-running activation.
- The implementation did not enforce pure builds at the operating-system
  boundary. Builders could consult time, network, host paths, environment, or
  `/proc`; Nix reduced these influences with isolated store paths, cleared
  environments, compiler/linker wrappers, and unprivileged build users.
- The two-machine rebuild found content differences in 5,059 regular files
  (3.4%), mostly timestamps and embedded host information. After filtering
  known timestamp-bearing types, 644 files (0.4%) still differed, and 42
  (0.03%) differed in size. The authors observed no behavioral difference, but
  the result demonstrates that assumed functional purity was not equivalent to
  bit-for-bit reproducibility.

## Relevance

The paper supports treating a system-service release as an immutable,
content-identified closure of code, static configuration, schemas, and declared
dependencies. A small mutable pointer can select the intended generation while
older generations remain available for rollback and in-flight actor migration.
Build-time dependency identity should be distinct from runtime service state,
and release preparation should finish before activation mutates the live
system.

For Atom OS, this is a system-services concern above the managed runtime, not a
reason to move a package manager or release policy into the kernel. The kernel
may help enforce hermetic builders through capabilities, restricted namespaces,
deterministic clocks, and denied network access. An unprivileged release
service should evaluate manifests, verify artifacts, maintain generation roots,
and coordinate service transitions; supervisors retain responsibility for live
actor state and health.

## Limits

The paper studies a 2008 NixOS prototype on Linux, with Upstart, GRUB, a modest
package collection, and a representative configuration rather than a broad
deployment trial. Its input-addressed store path does not by itself certify the
bytes produced by an impure build, and the authors explicitly show residual
non-reproducibility. “Atomic upgrade” applies cleanly to switching the profile
reference and immutable static artifacts; the activation script's effects on
users, links, services, devices, and mutable state are not one atomic
transaction and may require service-specific migration or compensation. A
rollback cannot undo arbitrary external effects, restore mutable application
data, or help after required old artifacts have been garbage collected. The
paper is about functional configuration management, not an operating system
implemented in a pure language and not a complete distributed rollout
protocol.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [OTP-like system-services deep-dive journal](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
