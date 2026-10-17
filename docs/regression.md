<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Mandatory future regression contract

**A_out ⊆ A_in** at every transformation's creation point, with actual legitimate
sources/delegation permissions, provenance and effective restrictions identified.
Every future class must demonstrate this invariant with reproducible tests.

Preserve independent clone/delegation and retained complete-credential snapshots;
do not compare them to a source's later reduced state. Shared open descriptions
share attenuation. Credential replacement, alias mutation, registry removal and
global revocation are different contracts. No UID-0 authority recreation or silent
LSM weakening is permitted.

Before a candidate changes Core, credentials, filesystem scopes, FD derivation,
transfer, async execution, LSM cache state, namespaces, UAPI or lifetime/locking:

1. Record exact base, complete delta and source/config/tool/policy hashes.
2. Specify input/holder/provenance, output, alias/independence, constraints and
   concurrent ordering. Separate absent/unhandled/claimed-but-unimplemented cases.
3. Rerun affected Core KUnit, native/compat, filesystem/FD, temporal, LSM and
   concurrency instrumentation checks; include allowed controls and negative cases.
4. Retain failed fixtures and BLOCKED/SKIP/BROKEN separately. No pass-count pooling
   across assertions/executables/configurations and no warning-string dismissal.
5. Reuse `tools/testing/selftests/authority/` and its QEMU runner. Do not create
   a second general qualification framework.
6. Version a new candidate/decision; never edit the frozen v1 reference to hide
   mismatches or automatically inherit its PASS.

Source equality establishes applicability of retained evidence, not a fresh test
execution or bit-identical binary. Unrelated expensive suites need not be repeated
without technical cause. The complete original requirements remain reconstructed
as `Documentation/authority/FUTURE-REGRESSION.md`.
