<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Developer workflow

## Dependencies and initialization

Source preparation needs Git, GNU tar, gzip and Python 3.11+ (standard library
only). No tools/packages are downloaded by the scripts. Linux initialization
alone uses the network:

```sh
git clone git@github.com:eugen252009/authy.git
cd authy
git submodule update --init --depth 1 linux
git -C linux rev-parse HEAD
```

The result must be `e767a4ea70a3992c37ed604157d32f0dfbf9b1e3`. If Git's shallow
submodule initialization cannot retrieve the pin, inspect the failure and fetch
the exact object explicitly—without updating Authy's gitlink or using a branch:

```sh
git -C linux fetch --depth=1 origin e767a4ea70a3992c37ed604157d32f0dfbf9b1e3
git -C linux checkout --detach e767a4ea70a3992c37ed604157d32f0dfbf9b1e3
```

Do not force a dirty checkout; stop and inspect it. If the canonical remote
cannot provide the pin, record BLOCKED and investigate provenance. Never choose
a nearby revision. No full Linux history fetch is needed for this baseline.

## Reconstruction and verification

```sh
./scripts/prepare.sh --output "$PWD/.work/source"
./scripts/verify.sh --source "$PWD/.work/source"
python3 scripts/test_tooling.py
```

Outputs must be NEW; failed partial outputs are preserved for diagnosis, never
cleaned/reset by the scripts. Use another new name for a later attempt. Linux is
archived from its committed pin and not patched in place. Patch order/content,
original record identities, all frozen verification inputs and the dependency
URL/gitlink/clean checkout are checked. Parent Git discovery is deliberately
bounded while applying inside ignored `.work/`.

Verification includes missing/extra files and directories, Git modes, symlink
targets, complete content, 32 production files, 14 test/build/runner/README files
and 15 design/qualification documents. The manifest's uncompressed SHA-256 is
checked against its frozen identity. It is source equivalence, not a promise of
bit-identical compiler output. Do not run make in the source tree or add artifacts
there: they correctly fail strict source verification.

## Kernel configuration and build

Retained qualified configs are x86_64. Existing evidence used GCC 14.2.0-19 and
binutils 2.44; other hosts must record differences, not inherit binary identity.
Dependencies include make, GCC/binutils, Perl, bc, flex/bison, libelf/libssl
development headers and rsync. Static selftests additionally need libc development
libraries. Install prerequisites yourself using normal distribution facilities;
scripts do not invoke package managers, sudo, deployment or host reboot.

Explicit manual configuration, always with separate output:

```sh
mkdir -p .work/manual-build
cp qualification/filesystem-v1/configs/regular.config .work/manual-build/.config
make -C .work/source O="$PWD/.work/manual-build" olddefconfig
cmp qualification/filesystem-v1/configs/regular.config .work/manual-build/.config
make -C .work/source O="$PWD/.work/manual-build" -j4 bzImage
```

Or use the optional wrapper, which refuses an existing output and fails if
olddefconfig changes the supplied full config:

```sh
./scripts/build.sh --source "$PWD/.work/source" --output "$PWD/.work/kernel-build" \
  --config "$PWD/qualification/filesystem-v1/configs/regular.config" --jobs 4
```

It then installs UAPI headers into that output and compiles the existing nine
selftests statically. It records commands and binary hashes; it never executes
them. KASAN/strict variants use separate outputs/configs. Source/config/tool/
timestamps/build identity and policy/fixture state affect actual results.
Authority is always built: pristine/control configs do not become a feature-off B.

## Compile-only tests

```sh
./scripts/build.sh --source "$PWD/.work/source" \
  --output "$PWD/.work/test-build" --selftests-only --jobs 4
```

No kernel image is built by this mode. It freshly exports headers and uses the
original kernel test Makefile. Available tests: authority_test, qualification_test,
landlock_fd_test, temporal_test, idmapped_test, callback_test, establishment_test,
dac_fd_test and handle_test. Builds/runner records stay under ignored output.

## Optional isolated execution — not performed automatically

Supply a matching test kernel and static BusyBox. QEMU/KVM permissions and
GNU cpio/gzip are also required. With four focused tests compiled as above:

```sh
S="$PWD/.work/source"
T="$PWD/.work/test-build/tests"
bash "$S/tools/testing/selftests/authority/run-qemu.sh" \
  /absolute/path/to/bzImage /absolute/path/to/busybox-static \
  "$PWD/.work/guest-new" "$T/authority_test" "$T/qualification_test" \
  "$T/landlock_fd_test" "$T/temporal_test"
```

Use the existing runner and reconstructed test README for markers/error accounting.
No guest host disks/network/shares are needed. Idmap/callback/handle and specialized
LSM/XFS cases have explicit config/policy/fixture requirements. Full historical
fixtures/logs are not shipped; unavailable steps are BLOCKED, not PASS. Do not
work around execution restrictions, weaken negative assertions or relabel
historical results as new executions.

## Future Linux upgrades

Treat any base change as a new candidate, not an in-place v1 update. In a separately
authorized development branch, inspect upstream changes, port the ordered series,
record the new exact gitlink/source/provenance and regenerate a complete manifest
only from a reviewed new source state. Apply the [regression contract](regression.md)
to affected Core/credentials/VFS/FD/LSM/async/lifetime/config changes and qualify the
new candidate. Do not merely change a hash to bypass a mismatch. Keep original
v1 patches, metadata and external evidence immutable. Linux stays an external
dependency; Authy does not import its ancestry.
