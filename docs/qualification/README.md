<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Qualification is not publication readiness

Current kernel decision: **CONDITIONAL GO — Experimental Filesystem v1**.
The source/distribution checks assess whether this repository can be published;
they do not promote the experimental kernel to production-ready.

[Portable baseline and evidence](../../qualification/filesystem-v1/README.md)
includes the full frozen file manifest, exact configs and chronological reports.
Earlier NO-GO checkpoints remain historical. Final A/B/C/D/G gates PASS and
E/F/H ACCEPTED_LIMITATION apply only to their recorded scope/configurations.

The remaining timer/serial KCSAN pairs were attributed
UPSTREAM_EXISTING_INDEPENDENT through source/instruction/layout/synchronization
review. No exact pristine recurrence, universal benignness, sanitizer-clean
whole kernel or new intrusive campaign is claimed. Always-built/no-feature-off-B,
missing old case identities, restricted architecture/FS/LSM/async coverage and
absence of global revocation remain limits.

The standalone prepare/verify workflow establishes complete source equivalence.
Tooling unit tests and native selftest compilation are separate from executing
kernel assertions. No historical PASS is relabeled a fresh runtime result.

The original baseline/status/matrix/LSM audit and temporal documents remain
exactly in the patch series and reconstructed source. Historical absolute evidence
paths are preserved provenance, not dependencies of Authy's portable scripts.
Raw historical evidence is explicitly not publicly distributed here.

See [developer workflow](../development.md) for optional isolated QEMU use and
[release checks](../release-readiness.md) for the source-package assessment.
