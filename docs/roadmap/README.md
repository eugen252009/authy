<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Roadmap — planning only

Recommended order: **Process → IPC → shared memory → Network → Device**.

The immediate milestone is a reviewed minimal Process/pidfd Authority contract
and reproducible regression plan: actor/target/provenance, stable task identity,
inheritance, lifetime, transfer, attenuation, saved contexts, namespaces and LSM
composition, before production implementation or public ABI commitment.

IPC then resolves endpoint use versus inbound/outbound delegation and queued
capabilities. Shared-memory work distinguishes externally shared resources from
ordinary private allocation. Network reuses stable socket/lifecycle/async
semantics. Heterogeneous ioctl/mmap/DMA devices come last, narrowly audited.

Each class must use the same Core model and prove **A_out ⊆ A_in** through
reproducible provenance, alias/independence, temporal, transfer/inheritance,
effective-restriction, concurrency/lifetime and Linux/LSM regression tests.
See [regression contract](../regression.md).

Future `permission run --none` versus `--no-delegation` are **not implemented**:
no initial external grant and a no-delegation policy are different contracts.
Ordinary private computation/allocation should not require external Authority.
Rescue Authority, irreversible object sealing, TPA declarations, service-manager
integration and richer Linux Audit reporting remain future work. Native Linux
module restriction/isolation is not supplied or an active implementation goal.

Use Linux descriptors, credentials, namespaces, Audit, LSM, Kbuild, KUnit and
kselftest—not a parallel OS, process manager, audit store or network stack.
The full reviewed planning document is reconstructed as
`Documentation/authority/NEXT-PHASE.md`; no future functionality is introduced here.
