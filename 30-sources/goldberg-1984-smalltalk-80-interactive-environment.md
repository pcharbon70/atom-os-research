---
title: "Smalltalk-80: The Interactive Programming Environment"
kind: source
created: "2026-09-04"
authors:
  - "Adele Goldberg"
published: 1984
citation_key: "goldberg-1984-smalltalk-80-interactive-environment"
container: "Addison-Wesley"
edition: null
isbn: "0-201-11372-4"
doi: null
url: "https://onlinebooks.library.upenn.edu/webbin/book/lookupid?key=olbp46519"
accessed: "2026-09-04"
tags:
  - development-tools
  - live-programming
  - smalltalk
  - user-interface
aliases:
  - "Smalltalk-80 Orange Book"
---

# Smalltalk-80: The Interactive Programming Environment

## Reference

Adele Goldberg. *[Smalltalk-80: The Interactive Programming
Environment](https://onlinebooks.library.upenn.edu/webbin/book/lookupid?key=olbp46519)*.
Addison-Wesley, 1984. ISBN 0-201-11372-4.

## Contribution

Goldberg documents the working Smalltalk-80 environment from the user's and
programmer's perspective: display and input, projects, workspaces, inspectors,
browsers, debuggers, change management, source access, snapshots, and extension
of the environment itself.

## Method

This is a book-length technical manual with procedures, screenshots, and class
descriptions. It is authoritative for Smalltalk-80 behavior but not an
experimental comparison of usability or reliability.

## Findings

- The bitmapped display, keyboard, and pointer present compiler, debugger,
  editor, and application facilities as rectangular views in one environment.
  Editing, accepting, compiling, evaluating, and testing occur without a
  separate build/run mode.
- A graphical interaction identifies an object and chooses a message. The
  virtual image contains compiled methods, live objects, and display state;
  source and change history also use external files, and the VM remains a
  distinct implementation layer.
- Projects collect a screenful of windows, history, and changes into a working
  context. Classes remain shared across projects, so a project is not a
  process, security compartment, or independent failure boundary.
- An inspector can be opened on any ordinary object, expose its state, navigate
  to related objects, and evaluate messages in context.
- Browsers organize categories, classes, protocols, and methods and support
  incremental compilation plus sender and implementor queries.
- Snapshots, change sets, and an audit trail support recovery and exchange.
- System and user code are deliberately malleable. The manual also warns that
  changing core behavior can crash the environment and recommends saving first.
- Goldberg credits the many contributors responsible for the browser,
  debugger, change manager, inspectors, file list, and graphical editors.

## Relevance

This book makes Kay's “user as author” principle concrete. It shows the
components needed for a live visual environment and the operational costs of
making them one mutable world. Atom OS should preserve inspectors, browsers,
change history, immediate evaluation, and reconstructible work contexts while
replacing global implicit authority with capabilities and supervision.

## Limits

The book describes a historical programming environment whose typical user was
already operating close to source code. It does not demonstrate that ordinary
non-programmers could safely evolve the whole system, and it predates modern
adversarial, accessibility, localization, and deployment requirements.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
