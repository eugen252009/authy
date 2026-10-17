# Filesystem Authority v1 closure qualification — NO-GO

## 1. Exact source and safety

HEAD/master: e767a4ea70a3992c37ed604157d32f0dfbf9b1e3 (Linux 7.3.0-rc5), plus
preserved uncommitted prototype. Initial status, binary patch and untracked
archive are baseline-*; source-provenance.json compares all 32 modified/new
production paths with the read-only staging tree used for the actual images.
They match. Only the existing AppArmor include/file.h + lsm.c and SELinux
hooks.c differ in production from the old 533-case source-fixed.tar checkpoint.
No production code was changed in this closure task. No Core/UAPI/class/right
or caller-credential/revocation redesign was made. The earlier candidate fixes
remain in place; their results were rerun rather than borrowed from old images.

Test-only repository additions: idmapped_test, callback_test,
establishment_test, dac_fd_test and handle_test; Makefile/README/config fragment
updated. Tests separate native and API-dependent cases before callbacks and do
not promote SKIPs. Existing three sources are unchanged and freshly built for
native testing; compat32 binaries have identical-source earlier compilation
provenance and were executed anew, not claimed freshly recompiled.

Toolchain: GCC 14.2.0-19/binutils 2.44; actual container IDs and compile logs are
retained. A prior full-tools image tag was unavailable; failed build exit 125
is retained, not a classifier block. The available authority-v1-toolchain
image built current static tests. QEMU 10.0.13/KVM/q35/host CPU; commands record
4 CPUs/4 GiB for ordinary tests, 6 GiB for full userspace XFS fixtures. No guest
NIC, host disk exposure or shared host filesystem. XFS /dev/vda is only a new
512 MiB file-backed synthetic guest disk, formatted inside the guest. No host
kernel install, boot change, reboot, commit, reset/clean/stash or publication.

## 2. Exact results

Counts are TAP groups per execution, not syscall assertions. Different rows
and instrumentation passes are not independent discoveries to add together.
all-runtime-results.json contains individual counts/exits/hash/diagnostics.

| Suite/configuration | PASS/FAIL/SKIP | Diagnostic/result distinction |
|---|---:|---|
| Current regular full original/upstream set | 536/0/11 | All exits 0; Core separately 10/0/0 |
| Current KASAN/lockdep full set | 536/0/11 | Core 10/0/0; no observed kernel diagnostic |
| Earlier-shaped current strict config | 533/0/14 | Functional success; 141 unique KCSAN reports; runner exit 1 |
| Expanded verbose strict full + idmap/callback/establishment | 560/0/11 | Core 10/0/0; 171 unique KCSAN reports; runner exit 1 |
| Current compat32 three Authority suites | 42/0/0 | Executed current image; existing unchanged-source static binaries |
| Final new four suites, regular | 35/0/0 | idmap 9 + callback 4 + establishment 11 + DAC/FD 11 |
| Final new four suites, KASAN | 35/0/0 | No observed kernel diagnostic |
| Final new four suites, expanded strict rerun | 35/0/0 | This rerun clean; earlier new-suite accounting race retained |
| Final new four suites, pristine A | 8/0/27 | Native controls run; API cases skip before assertions |
| XFS generic/ioctl handles, regular | 12/0/0 | Four native + eight handled denial/grant groups |
| XFS handles, KASAN | 12/0/0 | No observed kernel diagnostic |
| XFS handles, pristine A | 4/0/8 | No API-dependent passes invented |
| Focused AppArmor probe regular/KASAN, each | 7/0/2 | SELinux-only cases skip |
| Focused SELinux probe regular/KASAN, each | 9/0/0 | Separate native/FD-use checks |
| Focused pristine AppArmor / SELinux | 3/0/6; 4/0/5 | Same regular config as modified |
| Enforcing major + Landlock FD suite, each major/config | 7/0/0 | Actual enforcement asserted; cached TRUNCATE regression included |
| Extended SELinux fixture, each regular/KASAN | 38/0/0 | Landlock 7 + idmap 9 + DAC/FD 11 + establishment 11 |
| Extended AppArmor namespace/import fixture, each | 38/0/0 | Explicit setup mount and same-profile ptrace permissions |

The full current count is **536/0/11**, not the old 533/0/14: enabling overlay
runs three previously skipped upstream Landlock groups. The earlier progress
estimate of 533 was corrected from exact logs. The older-shaped strict config
still lacks that overlay coverage; configurations are not interchangeable.

LTP 20250930: on each modified regular/pristine A, 24 executable exits zero;
23 modern summaries give 331 PASS / 0 FAIL / 0 BROKEN / 0 SKIP / 0 WARNINGS.
Legacy fcntl01 supplies no success summary and receives no invented assertion
count. These are native/UNHANDLED comparisons, not managed-FD or full LTP.
Exact replay argv/results are in ltp-final/.

Initial stacked runs failed at argv[0] realpath setup; preserved then corrected
without changing production checks. A further extended AppArmor setup denied
mount propagation (nine failures) and pidfd ptrace (three failures). These were
real independent LSM fixture denials, not Authority regressions or passes. A
separate aa-namespace.profile explicitly permits only the needed mount/peer
ptrace prerequisites, retaining protected file denials and mac_admin denial.
Original aa.profile and its probe remain unchanged. Successful reruns are
stacked-ns-*; the failed stacked-all AppArmor logs remain visible. Outer shell
echoes are not used to hide individual failing suite exits.

## 3. Idmapped mounts and callback audit

Tmpfs FS_ALLOW_IDMAP, uid/gid 0 -> 1000 mapping in a separate user namespace.
A detached open_tree mount is idmapped and move_mount-attached. Replacing an
already-visible map is rejected EPERM with root privilege before UID drop.
Source and alias share inode/dev but not mount identity: a valid scope on one
cannot authorize the other. Native DAC and POSIX ACL identity translation,
UNHANDLED equivalence, READ/WRITE ceilings, scope grants over bounded generic
DAC denial, directory traversal denial, create ownership on disk/view, exact
parents, NOREPLACE/EXCHANGE, LINK, EXDEV, unlink, fd lifetime, dup and independent
clone attenuation are executed. Nested userns root cannot construct scopes
requiring initial-userns CAP_SYS_ADMIN. Major LSM fixture reruns also pass.
This is not all idmapped filesystems, mount replacements, userns combinations
or enforcing distro policies. Unsupported combinations remain explicit limits.

callback-matrix.json separates acquisition, import, derivation, namespace,
established use and unmodeled metadata. Overlay i_op->permission denials are
not overridden by semantic grants; readable/creatable controls succeed when
Linux allows them. Overlay custom FD-cap commands fail EOPNOTSUPP. Independent
LSM checks remain; clone's inode/open/post-open/clone callbacks serve distinct
purposes. NFS/FUSE and unrelated LSM configurations are not promoted to passing.
Metadata remains legacy Linux, not an invented revocation or new class.

## 4. KCSAN and memory safety

See KCSAN.md, kcsan-classification.json and kcsan-reports.json. Original 137
unique findings are recovered, not confused with 274 duplicate console/dmesg
occurrences. Matched current/pristine controls give 143/139 reports; expanded
verbose full/pristine control give 171/136. Classifications use exact memory,
widths, stacks, synchronization, source/layout/instruction and matched config
comparison, not presence in pristine alone. Constant-zero committed-cred
non_rcu W/W is BENIGN_WITH_EVIDENCE; d_flags/parent/hash, idle tick and task flags
families are UPSTREAM_EXISTING with field-specific synchronization analysis.
Authority can change timing/instrumentation span; no changed locks or writes
to those words were found. No confirmed AUTHORITY_INTRODUCED family.

Two rare findings remain UNRESOLVED: timer migration cpuevt.ignore and serial
IER shadow startup/IRQ access. Their machine code matches pristine and they
occur before any active Authority domain, but four short matched pristine
boots did not reproduce them and full synchronization disposition is absent.
They are not called harmless or sanitizer-clean. No report was suppressed.

Focused W=1 succeeds. GCC -fanalyzer fails Werror on nine retained findings;
static-analysis.md explains infeasible error-pointer and immutable-clone/registry
paths individually. This is not advertised as an analyzer-clean kernel or
allocation-failure-injection proof. Sparse/clang unavailable. KASAN/lockdep
runtime produced no observed defect; no universal memory-safety proof follows.

## 5. Credential-token boundary requiring a decision

An additional unscored direct io_uring observation registers a credential
personality before confinement. Thereafter default OPENAT returns -EACCES,
direct open returns -1, but explicit old-personality OPENAT returns a readable
FD; GET_CONFINED remains 1. See personality-observation/serial.log.

io_register_personality stores get_current_cred(); requests with that ID acquire
it and override subjective credentials in io_issue_sqe. The old immutable
Authority snapshot is UNHANDLED. This is distinct from fixed-file import and
pinned-object F_CLONEFD_CAP, and it does not erase the task's objective domain.
It is plausibly retained delegated credential authority, analogous to an old
privileged broker, but the existing fresh-open wording does not explicitly
settle this broad token. It is not silently called an implementation bypass,
revoked/rebased, or counted as a security PASS. Before release, explicitly
resolve the v1 threat boundary/launch preconditions or approve a narrow monotonic
request-credential rule. No future process class or CLI was implemented.

## 6. Historical coverage and configuration B

Original 21/47 temporary harnesses were not recovered from branches/worktrees,
Git history/unreachable records or three archived source snapshots. There is
one worktree/branch; earlier untracked temporary harnesses never entered Git.
historical-case-map.json inventories all 68 claimed slots with unknown original
case IDs/assertions, never fabricated names or old PASS results. The 21 group
partition is known; new acquisition tests cover its reported invariants with
native controls, not numerical equality. historical-invariants.json maps DAC
narrative claims to current tests, including new groups/FSUID/transfer checks.
Exact original individual assertion provenance remains unverifiable.

Configuration B: ACCEPTED_ARCHITECTURAL_LIMITATION for built-in v1. Its requested
feature-off build remains BLOCKED/not selectable/not executed with zero passes.
configuration-B.md justifies gate H: actual unconditional linkage, stable Core
registry/credential integration, no promised disable ABI/config, pristine A
and UNHANDLED comparisons. No switch was added and A was not renamed B.

## 7. Independent gates and final decision

| Gate | Assessment | Boundary/reason |
|---|---|---|
| A Functional | PASS | Exact supported operations and stated configs; current runs above |
| B Security invariants | BLOCKED | Broad pre-existing credential-token/fresh-acquisition boundary unresolved |
| C Kernel compatibility | PASS | Bounded native/UNHANDLED matched controls and LTP subset |
| D LSM integration | PASS | Exact Landlock, synthetic enforcing SELinux/AppArmor and stacked configurations; not all LSMs/policies |
| E Memory/concurrency | BLOCKED | Two rare KCSAN families lack complete matched runtime/synchronization disposition |
| F Regression | ACCEPTED_LIMITATION | Current named invariants covered; original per-case identities unavailable; no claim of restored 21/47 or all Linux |
| G Reproducibility | PASS after integrity verification | Source snapshot/patch, configs/images/binaries/logs, exact argv and manifest/archive |
| H Configuration | ACCEPTED_LIMITATION | Always-built x86_64 + compat32 scope; nonexistent B explicitly excluded, never passed |

**Final decision: NO-GO.** Do not change gates merely to obtain GO. Concrete
remaining blockers are the two rare KCSAN dispositions and the credential-token
scope/launch-contract decision. Other listed unqualified configurations and
broader integration/failure-injection cases define limits, not passing tests.
No production readiness or complete process confinement is claimed.

## 8. Evidence integrity

Current source and snapshots are identified by source-provenance.json,
baseline-* and final-source manifests. Exact .configs, kernel hashes, test
binaries, initial/final failures, guest rootfs and QEMU argv are retained in
/tmp/authority-v1-final/closure and referenced earlier trees. The prior 7 GiB
persistent archive is preserved, not overwritten. A separate closure archive
and SHA-256 sidecar retain this continuation. Manifest verification establishes
retention; compilation or QEMU poweroff alone never establishes a passing test.
