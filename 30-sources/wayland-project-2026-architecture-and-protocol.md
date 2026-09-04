---
title: "Wayland Architecture and Protocol"
kind: source
created: "2026-09-04"
authors:
  - "Wayland Project"
published: null
citation_key: "wayland-project-2026-architecture-and-protocol"
container: "Wayland documentation"
edition: null
isbn: null
doi: null
url: "https://wayland.freedesktop.org/architecture.html"
accessed: "2026-09-04"
tags:
  - compositor
  - desktop-architecture
  - input-routing
  - wayland
aliases:
  - "Wayland architecture"
---

# Wayland Architecture and Protocol

## Reference

Wayland Project. “[Wayland
Architecture](https://wayland.freedesktop.org/architecture.html),” “[Wayland
Protocol and Model of
Operation](https://wayland.freedesktop.org/docs/book/Protocol.html),” and the
[project overview](https://wayland.freedesktop.org/). Accessed 2026-09-04.

## Contribution

The official documentation describes a representative current Linux desktop
display boundary: kernel device mechanisms, a compositor/display server,
client-rendered buffers and surfaces, scene-graph hit testing, input focus, and
protocol-mediated coordination.

## Method

This source note treats the official architecture description and protocol
manual as engineering documentation. It records the intended contract, not an
independent security, performance, or interoperability evaluation.

## Findings

- Kernel input drivers normalize device events and deliver them to the
  compositor.
- The Wayland compositor is the display server. It uses its scene graph to
  choose a receiving surface, transforms coordinates, and routes input to the
  client.
- Clients render their own content into buffers, commit buffers and damage to
  surfaces, and do not ask the display server to understand their widgets or
  domain models.
- The compositor combines client buffers into the final display. A particular
  compositor/shell implementation may also integrate launch, task-switching,
  and lock-screen policy; those functions are not guaranteed by the core
  protocol.
- Seats group input devices; focus and event serials constrain operations such
  as interactive move, resize, selection, and data transfer.
- Wayland is a protocol and composition architecture, not by itself a complete
  application sandbox or semantic accessibility model.

## Relevance

Wayland makes the modern separation vivid: the desktop authority sees surfaces,
geometry, focus, damage, and buffers, while application meaning remains inside
clients. Atom OS should retain this narrow trusted rendering and input boundary
but add a separate capability-safe semantic/project protocol above it.

## Limits

The pages describe core architecture, not every compositor, desktop shell,
toolkit, accessibility bridge, extension, or security policy. Wayland-based
systems vary materially, and core protocol documentation must not be cited as
proof of sandboxing.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
