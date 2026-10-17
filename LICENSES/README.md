<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Licensing and upstream attribution

Authy contains Linux modifications, not a relicensing of Linux. Preserve all
original notices/SPDX identifiers in the patches and reconstructed kernel.
`COPYING`, `preferred/GPL-2.0` and `exceptions/Linux-syscall-note` are copied
verbatim from the pinned upstream Linux tree. The complete upstream license
collection remains in the external `linux/LICENSES/` dependency.

New Authority C/headers/tests/runner identify GPL-2.0. Existing kernel and UAPI
files retain their original, file-specific identifiers/exceptions. New standalone
scripts/docs identify GPL-2.0-only; this does not grant a syscall exception to
kernel modifications. Historical documentation and qualification reports remain
unmodified contributions under their original Linux COPYING context; adding a
wrapper does not invent new notices or third-party permissions.

No new third-party binary is vendored. Building requires separately obtained
Linux/toolchain packages; testing may require BusyBox, QEMU, LTP and policy tools
under their own licenses. Their binaries and historical multi-gigabyte archives
are not shipped in this repository. Any later binary/evidence distribution needs
its corresponding-source, notice and dependency-license review.

Complete upstream Git history is not a substitute for applicable license texts,
notices or corresponding source. An independent patch repository does not remove
modified-kernel obligations. See the pinned Linux
`Documentation/process/license-rules.rst` for its contribution rules.
No legal certification or blanket redistribution guarantee is asserted here.
