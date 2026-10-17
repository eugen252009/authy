<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Filesystem v1 qualification reference

**CONDITIONAL GO — Experimental v1**, `filesystem-v1-experimental-20261017-r1`.
This is a bounded kernel-prototype decision, not production readiness or a
sanitizer-clean whole kernel. Source packaging/reconstruction is separately
verified; historical functional results have not thereby been rerun.

## Portable verification inputs shipped here

* [baseline.json](baseline.json): exact base, qualified tree, artifact identities
  and hashes of verification inputs.
* `expected-source.json.gz`: losslessly compressed **complete original** frozen
  file/content/Git-mode/symlink-target manifest, 96,086 entries. Its uncompressed
  SHA-256 is `0cdb148324ec115555aaaa404b7e56fe5dca8e0d5f227414cd8ac43431d71448`.
  It is metadata, not a kernel source archive or replacement Linux dependency.
* [production.json](production.json): the 32 qualified production hashes.
* [standalone-checks.json](standalone-checks.json): fresh-clone source equivalence
  and compile-only results for the independent repository tooling.
* `configs/`: full retained regular, KASAN, strict and control configurations.
  Fragments alone do not identify qualified images. `pristine` means a different
  **source tree**, not a feature-off switch in the patched tree.
* [frozen-version.json](frozen-version.json): original source-package identity.
* [external-artifacts.json](external-artifacts.json): names/hashes/sizes of retained
  archives; not download links or a claim those assets are publicly accessible.
* [closure checkpoint](reports/closure.md), [temporal checkpoint](reports/temporal-authority.md),
  [final KCSAN disposition](reports/kcsan-closure.md): verbatim chronological
  reports. Earlier NO-GO decisions are preserved, not rewritten as passes.

The frozen complete-source archive SHA-256 is
`af0a5fb7b35c11bc0256759a5fa32c71403dc8b6ecefd87363ece80abb4f3f40`.
That **archive is not needed** to reconstruct/verify source from the pinned
submodule and patches; the full manifest travels with Authy.

## Evidence availability — explicit limitation

Large historical raw serial logs, images, rootfs/LSM fixtures and toolchain/LTP
assets are retained in maintainer-controlled local archives, **not shipped or
published here**. No off-machine durable backup or public artifact URL is
asserted. The original reports' `/tmp`, `/var/tmp` and absolute paths are
historical provenance, not working paths on a reader's computer. Do not run old
hard-coded orchestration unreviewed or treat local paths as public evidence links.
Maintainers must separately authorize/review any archive redistribution and
third-party source/license obligations. Some archives exceed 2 GiB and cannot be
single GitHub release assets; none belongs in Git as a normal blob.

Readers can reproduce source independently, compile the available nine tests and
run the checked-in QEMU runner in a suitably isolated environment. This does not
promise automatic reproduction of every historical specialized LSM/XFS/namespace
fixture without its external dependencies. If unavailable, record it BLOCKED,
not PASS. New results require their own source/config/tool/policy/log hashes.
Use [developer commands](../../docs/development.md), not a second test framework.

## Accepted boundaries

Final A/B/C/D/G gates PASS; E/F/H ACCEPTED_LIMITATION. The two native timer/serial
KCSAN families are attributed UPSTREAM_EXISTING_INDEPENDENT by source/layout/
instruction/synchronization analysis, not observed exact pristine recurrences,
universal harmlessness or new device-off/equal-duration trials. Remaining old
case-identity, filesystem/LSM/config/architecture/async coverage limits persist.
Authority is always built; configuration B/feature-off is absent, not passing.
Global revocation and future resource classes are not implemented.
