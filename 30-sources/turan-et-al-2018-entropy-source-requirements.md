---
title: "Recommendation for the Entropy Sources Used for Random Bit Generation"
kind: source
created: "2026-09-06"
authors: ["Meltem Sönmez Turan","Elaine Barker","John Kelsey","Kerry A. McKay","Mary L. Baish","Mike Boyle"]
published: "2018-01"
citation_key: "turan-et-al-2018-entropy-source-requirements"
container: "NIST Special Publication 800-90B"
edition: null
isbn: null
doi: "10.6028/NIST.SP.800-90B"
url: "https://doi.org/10.6028/NIST.SP.800-90B"
accessed: "2026-09-05"
tags:
  - cryptography
  - entropy
  - security
aliases: []
---

# Recommendation for the Entropy Sources Used for Random Bit Generation

## Reference

Meltem Sönmez Turan, Elaine Barker, John Kelsey, Kerry A. McKay, Mary L. Baish, Mike Boyle. [Recommendation for the Entropy Sources Used for Random Bit Generation](https://doi.org/10.6028/NIST.SP.800-90B). NIST Special Publication 800-90B. 2018-01. DOI: 10.6028/NIST.SP.800-90B. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to authentication and administration profile in the CLI-first operating-system proof of concept.

## Method

Read sections 3–4 on source requirements and health testing.

## Findings

The specification separates noise-source modeling, entropy assessment, conditioning and health tests. Startup and continuous tests assess raw-source behavior; persistent failures require an output policy. Tests cannot replace a defensible source model.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

Passing health tests does not guarantee unpredictability of every sample or repair a compromised source. The document does not choose an Atom hardware entropy source, DRBG or emulator trust policy.

## Derived work

- [Authentication and administration profile](../20-notes/proof-of-concept-requirements/authentication-and-administration-profile.md)
