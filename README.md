<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Authy

An **experimental capability-based Authority Framework for the Linux kernel**.
Linux is an external, exactly pinned dependency; this repository contains Authy
patches, provenance, reconstruction tools and qualification metadata—not Linux's
source history.

**Qualification: CONDITIONAL GO — Experimental Filesystem v1**  
Baseline: `filesystem-v1-experimental-20261017-r1`.

This is **not production-ready**, not a sanitizer-clean-kernel claim, not a
replacement for Linux, and not a complete process/network/IPC Authority system.
Publication readiness means the source package can be published, not that the
kernel prototype is suitable for production deployment.

## Security model

**A_out ⊆ A_in**

Each transformation preserves or reduces legitimately supplied effective
Authority at its creation point. Additional authority requires a separately
valid explicit grant/delegation. Delegation need not attenuate. Independent
clones and retained credential snapshots retain legitimately supplied rights;
shared open-file descriptions share mutable attenuation. Local reduction is
not global revocation. Identity (including UID 0) alone cannot recreate omitted
handled Authority. Independent Linux and LSM restrictions remain applicable.

## Current implementation

* Immutable Authority Core, class dispatch, credential ownership and KUnit checks.
* Object-bound filesystem scopes and bounded VFS data/namespace operations.
* FD capability query, monotonic attenuation and independent description cloning.
* Credential inheritance and temporal delegation, including saved io_uring contexts.
* Selected Landlock, SELinux and AppArmor interoperability and regression coverage.
* Nine kernel selftests, configuration fragments and the existing isolated QEMU runner.

Only the filesystem production class exists. Global revocation, complete
mediation, mandatory traversal everywhere and future permission CLI options are
not implemented. See [architecture](docs/architecture/README.md) and
[qualification boundaries](docs/qualification/README.md).

## Reconstruct the exact qualified source

Requirements: Git, Python **3.11+**, GNU tar and gzip. No additional tools are
automatically installed. Network access is needed only to initialize Linux:

```sh
git clone git@github.com:eugen252009/authy.git
cd authy
git submodule update --init --depth 1 linux
./scripts/prepare.sh --output "$PWD/.work/source"
./scripts/verify.sh --source "$PWD/.work/source"
```

`linux/` is pinned to upstream commit
`e767a4ea70a3992c37ed604157d32f0dfbf9b1e3` from
<https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git>.
No mutable upstream branch is substituted. If a shallow submodule clone cannot
retrieve that older commit automatically, fetch **that exact object** as described
in [development](docs/development.md); never update to a nearby revision.

Preparation archives the verified base into a **new disposable directory**, then
applies the nine checksummed patches in order. It never patches the submodule or
overwrites an existing output. Verification checks **96,086 files/symlinks**,
content, Git modes, link targets, unexpected/missing paths, all **32 production
hashes**, and required tests/runners/docs using the complete frozen manifest.
It requires neither the old development checkout nor local qualification archives.
This proves source equivalence, **not bit-identical kernel binaries**.

## Build and tests

```sh
# Compile all nine userspace selftests; does not run them or build a kernel:
./scripts/build.sh --source "$PWD/.work/source" \
  --output "$PWD/.work/test-build" --selftests-only

# Optional kernel build using a retained full qualification config:
./scripts/build.sh --source "$PWD/.work/source" \
  --output "$PWD/.work/kernel-build" \
  --config "$PWD/qualification/filesystem-v1/configs/regular.config" --jobs 4
```

See [developer workflow](docs/development.md) for build prerequisites, explicit
configuration, the existing QEMU runner, fixture limits and dependency upgrades.
Nothing installs a host kernel, changes `/boot` or reboots the host. Raw historical
qualification archives are **not distributed here**; see
[evidence availability](qualification/filesystem-v1/README.md).

## Roadmap

**Planning only:** Process → IPC → shared memory → Network → Device.
The immediate milestone is a reviewed **Process/pidfd Authority contract and
regression plan**, before production implementation or public ABI commitment.
Ordinary private computation/allocation is not external Authority. Reuse Linux
lifecycle, testing, LSM and Audit infrastructure; no parallel OS/services.
See the [roadmap](docs/roadmap/README.md) and [regression contract](docs/regression.md).

## Provenance and licensing

The nine patches preserve original subjects, authorship, ordering and commit IDs
from the signed local Authority series ending at
`c8b8dde1d872f7ced4169b7a1109f44577a31c2b`. Original signed commit records are
retained as provenance **data**, not Authy Git ancestors. Patch files do not carry
Git commit-signature verification; see [provenance](docs/provenance.md).

Linux notices, [COPYING](COPYING), [GPL-2.0](LICENSES/preferred/GPL-2.0) and the
[Linux syscall exception](LICENSES/exceptions/Linux-syscall-note) are preserved.
File-specific SPDX identifiers remain authoritative; the syscall exception is
not a blanket exception for Authy kernel code. New reconstruction tooling and
landing documentation use GPL-2.0-only. See [licensing](LICENSES/README.md).
Independent Git history does not remove modified-kernel licensing obligations.
