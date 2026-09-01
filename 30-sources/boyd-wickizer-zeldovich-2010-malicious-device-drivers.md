---
title: "Tolerating malicious device drivers in Linux"
kind: source
created: "2026-08-31"
authors:
  - "Silas Boyd-Wickizer"
  - "Nickolai Zeldovich"
published: 2010
citation_key: "boyd-wickizer-zeldovich-2010-malicious-device-drivers"
container: "2010 USENIX Annual Technical Conference"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/usenix-atc-10/tolerating-malicious-device-drivers-linux"
accessed: "2026-08-31"
tags:
  - device-drivers
  - dma
  - failure-containment
  - iommu
  - operating-systems
aliases:
  - "SUD device-driver isolation paper"
---

# Tolerating malicious device drivers in Linux

## Reference

Silas Boyd-Wickizer and Nickolai Zeldovich. “Tolerating Malicious Device
Drivers in Linux.” *2010 USENIX Annual Technical Conference (USENIX ATC
'10)*, Boston, Massachusetts, June 2010. USENIX Association.
[Official record and open paper](https://www.usenix.org/conference/usenix-atc-10/tolerating-malicious-device-drivers-linux).

## Research question or contribution

Can unmodified Linux drivers run as untrusted user-space processes while both
driver code and the hardware it controls are prevented from corrupting the rest
of the system?

## Method

The authors build SUD from two Linux kernel modules and a User-Mode Linux
library. They run existing Ethernet, wireless, sound, USB-host, and USB-device
drivers in separate processes, exercise explicit DMA and interrupt attacks,
and compare an e1000e driver in SUD with its in-kernel version using netperf on
a dual-core x86 laptop.

## Findings

- Moving driver code to a separate address space is insufficient by itself: a
  malicious driver can program its device to DMA into arbitrary memory or
  generate disruptive interrupts.
- SUD combines process isolation with IOMMU page tables, PCI Express
  transaction filtering, message-signalled interrupts, and controlled access
  to MMIO, I/O ports, and PCI configuration state. It assumes the physical
  device correctly implements the PCI Express specification.
- A narrow kernel proxy translates driver operations into user-level upcalls.
  Per-device interfaces map only authorised registers and DMA buffers into both
  the driver's CPU address space and the device's IOMMU address space.
- A failed driver can be killed, resource-limited, and restarted as an ordinary
  process. This contains corruption but cannot preserve service availability
  while the sole driver or device is unavailable.
- TCP streaming reached the same 941 Mbit/s in both configurations, with CPU
  use rising from 12% to 13%. Small-packet UDP tests incurred about 11% transmit
  and 30% receive CPU overhead; the request-response test roughly doubled CPU
  use while retaining similar transaction throughput.
- The prototype's test machine lacked interrupt remapping and remained
  vulnerable to a malicious-device livelock through the implicitly mapped MSI
  address. The paper identifies newer hardware support as necessary to close
  that boundary.

## Relevance

The project's driver domains must receive explicit, least-authority handles to
a device's MMIO ranges, I/O ports, DMA address space, interrupt source, and
configuration operations. The minimal privileged kernel should bind CPU and
IOMMU mappings together, mediate interrupt routing and masking, and revoke all
of those authorities before memory reuse or driver restart. Bus enumeration,
device-class policy, protocol logic, recovery orchestration, and the driver
implementation belong above the kernel. A supervisor can then replace a failed
driver without placing driver code inside the privileged failure boundary or
coupling it to the BEAM-compatible runtime.

## Limits

SUD is a 2010 Linux/x86 prototype that depends on User-Mode Linux and
commodity-kernel mechanisms, not a minimal capability kernel. Its isolation
argument is supported by constructed attacks rather than a formal proof, and
the evaluated chipset lacked the interrupt-remapping feature required for the
paper's full goal. The design trusts device hardware and PCI Express behaviour,
delegates at whole-PCI-device granularity, and leaves subdevice delegation as
future work. Results from one Gigabit Ethernet setup do not establish overheads
for modern high-rate, accelerator, storage, or multicore workloads.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
