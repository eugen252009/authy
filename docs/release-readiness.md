<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Source-package release readiness

This independent repository packages **CONDITIONAL GO — Experimental Filesystem
v1**; publication readiness does not change kernel qualification or its limits.

## Executed verification

* Pinned Linux fetched directly from canonical kernel.org at the exact base.
* Nine patches match the previously audited 584,905-byte series exactly; original
  signed commit data/IDs/authorship/order retained without importing ancestry.
* Complete prepare/verify: **96,086 files/symlinks**, no missing/extra entries or
  unexpected directories, no content/Git-mode/link-target differences.
* **32 production**, **14 selftest/build/runner/README**, **15 design/qualification
  document** paths all match the frozen manifest.
* A separate fresh clone of committed Authy initialized Linux from the canonical
  remote, reconstructed source without the old worktree/archive, and freshly
  installed headers/compiled all **nine static selftests** successfully.
* Ten reconstruction-tool unit tests pass; existing-output refusal was also
  tested against the real prepared source without changing it.
* [Portable result record](../qualification/filesystem-v1/standalone-checks.json)
  identifies the exact tested tooling/metadata commit and script hashes. Later
  landing/release documentation does not change those tested reconstruction inputs.

**Not executed:** kernel image build/boot, selftest execution, new qualification
runtime workloads or binary-reproducibility experiments. Optional build/run
commands are documentation, not claimed results. No host deployment/reboot.

## Checks before an authorized push

From a clean committed checkout with the initialized submodule and prepared source:

```sh
python3 scripts/test_tooling.py
python3 scripts/check-release.py --source "$PWD/.work/source"
git status --short
git log --oneline --graph
git ls-remote --symref origin
```

The local release checker verifies exact reconstruction, canonical URL/gitlink,
clean independent/non-shallow Authy history, absence of the Linux commit in Authy's
own object database, Git connectivity, tracked file sizes/magic, selected credential
patterns and active documentation links. It never pushes or fetches. Hygiene is
heuristic, not a guarantee against every possible secret. Preserved patch/reports
contain historical local evidence paths; active tooling has no dependency on them.
Configured commit authorship/public signing metadata is intentional provenance,
not an API credential; maintainers should be comfortable publishing that identity.

Linux's separate submodule object store/checkout may occupy hundreds of MiB/GiB.
Those objects are not Authy ancestors or included in Authy's branch upload.
The largest Authy file is the compressed full verification manifest, below GitHub's
100 MiB blob limit. No kernel/QEMU images, databases or multi-GiB archives are
versioned. Do not stage ignored local outputs or add LFS merely to ship evidence.

Remote `origin` must be `git@github.com:eugen252009/authy.git`. Recheck advertised
refs immediately before any later push; a previous empty ref advertisement is
not a permanent guarantee. Write permission, branch protection and public/private
visibility are not proven by read-only SSH access. Resolve any independently
created remote history without force/rewrite. No push or tag has been performed.

Only after separate explicit publication authorization, and only if the reviewed
remote still has no conflicting history, the proposed first command is:

```sh
git push --set-upstream origin main:main
```

That command is a proposal, **not executed**. Raw evidence distribution, off-machine
backup, third-party binary licensing review and full runtime requalification are
separate activities; [availability limits](../qualification/filesystem-v1/README.md)
are disclosed rather than presented as completed publication or new test passes.
