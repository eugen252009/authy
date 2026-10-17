# Temporal Authority and io_uring qualification

## Decision

**EXPECTED_VALID_DELEGATION** — the pre-confinement personality finding is
resolved within the tested ordinary/IOSQE_ASYNC scope. It retains legitimately
supplied historical context, not identity-only permission reconstruction.
No Authority amplification defect was confirmed; **no production code changed**.
Whole Filesystem Authority v1 remains **NO-GO** because the separately retained
rare timer-migration/serial-IRQ KCSAN dispositions are still unresolved.

## Formal selected contract

**A_out ⊆ A_in**, evaluated at each transformation's effective creation point.
A_in means all effective, legitimately supplied and delegable authority,
including source provenance, current rights/scopes, applicable LSM state,
explicit delegation and independently authorized grants. Native UNHANDLED is
not a zero-right context. A saved UID is not sufficient evidence of Authority.

**A later reduction of the source's Authority does not retroactively invalidate a previously legitimate independent capability.**

**A historical identity or credential snapshot is not automatically equivalent to a legitimately delegated Authority capability.**

At T1 an independent B may retain source A's valid RW. At T2 A reduces to R.
B remains RW. A T3 clone from A cannot yield W; an explicit clone from B may,
because B is the actual valid input. F_CLONEFD_CAP requests are maxima: a late
request for RW may return a valid R-only child, not necessarily fail the entire
syscall. Its WRITE must fail. No global retroactive attenuation was added.

Successful **explicit** IORING_REGISTER_PERSONALITY is selected as a ring-bound
execution-context delegation boundary. Recognition requires actual full-context
capture, ownership/lifetime, bounded use and LSM checks. This does not turn every
saved identity/get_cred pointer into a capability. In particular the old ring
opener credential does not supply default submissions with old authority.

## Source provenance and audit

HEAD/master: e767a4ea70a3992c37ed604157d32f0dfbf9b1e3, Linux 7.3.0-rc5, with the
preserved uncommitted prototype. baseline-* captures the initial tracked diff,
untracked files and status. production-baseline.json checks all 32 relevant
changed/new production paths against the existing image source; final checks
remain identical. Only documentation and a new temporal selftest/registration
changed. Existing production LSM/Authority fixes remain unmodified.

The detailed lifecycle table and ten provenance answers are in repository
Documentation/authority/temporal-semantics.md, integrated into architecture.md
and the qualification ledger. Key source anchors:

* fs/file_capability.c: get observes; restrict publishes via cmpxchg/atomic AND;
  clone snapshots source bits, intersects requested/mode, creates private state
  and independent subsequent offset, retaining inode/open/post-open/clone checks.
* kernel/authority.c + kernel/sys.c: immutable refcounted Authority and pinned
  scope state; scope grants explicitly require CAP_SYS_ADMIN; confinement and
  drops prepare/commit replacement credentials. A grant is not alleged to be
  derived from a zero-right FD: it has a separately authorized source.
* kernel/cred.c, include/linux/cred.h: prepare/copy references Authority;
  put_cred_rcu releases it. fork context and per-task future replacement are
  distinct from mutable file state. fs/exec.c preserves confined domains.
* io_uring/register.c: io_register_personality gets **registrar current cred**,
  not ring creator cred, and publishes the ref in ctx->personalities. This holds
  Authority via the complete credential, not a UID-only copy or separate new
  Authority allocation. Registration failure puts; unregister xa_erases/puts.
* io_uring/io_uring.c: io_init_req resolves under ring serialization, gets a
  request ref and checks security_uring_override_creds. __io_issue_sqe overrides
  subjective credentials, runs normal filesystem acquisition and reverts.
  io_prep_async_work preserves selected request creds or captures default issuer
  creds. Request cleanup puts; ring kill unregisters remaining entries under
  uring_lock before asynchronous destruction.
* security/selinux/hooks.c and security/apparmor/lsm.c: current adoption vetoes
  remain independent. Captured file-policy restrictions and Landlock credential
  state still restrict the selected subject. No credential rebasing or LSM
  disabling was needed.

The ring+ID is the context capability. IDs are ring-local names, not secrets.
Ring duplication shares the registry, and registration into a shared ring
intentionally makes that context available to eligible ring holders. Current
ring restriction/issuer rules and LSM checks apply; an Authority no-delegation
flag is NOT implemented. Launch hygiene must account for broader ring contexts
as well as established files/brokers.

## Concurrency, aliasing, lifetime and revocation

FD aliases share mutable attenuation; independent clones do not. Forked task
contexts reference immutable state: parent COW reduction does not mutate child.
Clone's source-rights observation bounds an overlapping derivation. A clone
started after completed restriction must not recover W. Other LSM checks occur
before publication under their own synchronization; no universal atomic policy
reload/namespace transaction is claimed.

Registration's current credential capture and successful xarray publication
create its context. Another thread is another credential subject. Current
confinement rejects a live multithreaded attempt with EBUSY; the focused test
confirms no state change, then enters after the registering peer exits.

Lookup/get_cred versus unregister is ordered under uring_lock. A deliberately
IO_DRAIN-deferred request prepared before unregister succeeds afterward using
its own reference; subsequent ID lookup returns EINVAL. An already acquired FD
also remains valid. New ring numeric reuse cannot resurrect the old context.
64 teardown cycles and 64 clone/restriction overlaps run per suite.

There is no global/object revocation API. The corresponding case is **SKIP**,
not PASS. Unlink, local attenuation, unregister and close are tested as their
actual lifecycle mechanisms. Source review and KASAN/strict stress found no
unintended reference use; CONFIG_DEBUG_KMEMLEAK is disabled, so no universal
absence-of-leaks proof or fault-injection coverage is claimed.

## Reproducible regression results

Counts are grouped kselftests per execution, not individual assertions, and
must not be summed across configs as independent security discoveries.

| Final-source execution | PASS / FAIL / SKIP | Kernel diagnostics |
|---|---:|---|
| Temporal regular | 15 / 0 / 1 | none observed; Core separately 10/0 |
| Temporal KASAN/lockdep | 15 / 0 / 1 | none observed; Core separately 10/0 |
| Temporal strict KCSAN | 15 / 0 / 1 | none observed in focused run; Core 10/0 |
| Pristine A regular | 2 / 0 / 14 | native identity and ring-registry controls |
| Pristine A strict | 2 / 0 / 14 | native controls, no observed diagnostic |
| Existing Authority/qualification/Landlock suites, regular | 42 / 0 / 0 | 13 + 22 + 7; Core separately 10/0 |
| Same existing suites, KASAN/lockdep | 42 / 0 / 0 | no observed diagnostic; Core 10/0 |
| AppArmor temporal interop regular/KASAN/pristine, each | 3 / 0 / 0 | enforce mode verified |
| SELinux temporal interop regular/KASAN/pristine, each | 3 / 0 / 0 | enforce mode verified |

The one custom skip is absent global revocation. Pristine additional skips are
custom-API groups before callback invocation, not late skips hiding native
assertions. Relevant real LL regression coverage remains 7 passing groups.
Ordinary native credentials, custom Authority and LSM assertions are separate.
The strict focused run does not erase prior unrelated full-workload KCSAN
findings or establish whole-v1 concurrency qualification.

Tests cover independent pre-attenuation clone retention and re-delegation,
post-attenuation/zero-source ceilings, shared dup/SCM state, fork/exec contexts,
register-before versus register-after confinement, bounded RW/R/zero saved
contexts, retained UID 0 versus explicit READ-only Authority, async/default
issuer distinction, in-flight/unregister ordering, teardown, concurrency and
captured LL restrictions. Dedicated major-LSM controls test allowed adoption,
current adoption veto, and saved file denials with synchronous/async requests.

## AppArmor fixture root cause, not an expectation change

The initial AppArmor interop run was **2 PASS / 1 FAIL**, retained in
lsm-first-apparmor/. The explicit override-deny was not mediated by the parser's
default policy ABI: shipped ABI 4.0 lacks io_uring in its feature set, and the
kernel returns legacy allow when RULE_MEDIATES(AA_CLASS_IO_URING) is absent.

The corrected fixture explicitly opts into the kernel-advertised
`io_uring { mask { sqpoll override_creds } }` policy feature through
--override-policy-abi. Kernel feature output is logged. It does NOT weaken a
rule, drop a denial, skip the assertion, or alter kernel checks. The unchanged
negative expectation then returns -EACCES on both modified/pristine engines.
The original profile, first rootfs and failed log remain. SELinux policy uses
uringblock_t with fd access allowed but io_uring override_creds denied, avoiding
confusion with FD_USE or fixture-access failures. Captured file-denial cases
have a direct privileged-parent success control.

## Configurations, tooling and execution limits

Current regular/pristine .configs match byte-for-byte, as do expanded strict
configs. config-*, image-hashes.txt and every runner command/argv preserve exact
artifacts. Existing tested kernels are reused only after 32-path production
source equality, not promoted across unknown source changes. No production
correction required a new kernel build. Native tests compile with GCC 14.2.0-19,
-Wall -Wextra -O2 -pthread -static and current UAPI headers; final build log has
zero diagnostics. LSM fixture binary uses retained guest libselinux/libapparmor.
The unavailable/nonapplicable global revocation and broad leak proof are not
called tested. SQPOLL/IOPOLL, arbitrary new classes, all policy-reload races and
other LSMs remain outside this focused verdict.

All kernel execution is isolated q35/KVM, host CPU, four vCPUs/4 GiB, no NIC,
shared host FS or host disk attachment. Offline AppArmor parsing used -Q
(skip kernel load); it did not load policy on the host. No host kernel install,
reboot, commit, reset/clean/stash, push/publication, Core redesign, new class,
UAPI change, delegation CLI, Rescue/sealing or restricted-module work occurred.

## Evidence and impact

results.json contains exact totals/exits/log hashes. classification.json selects
exactly EXPECTED_VALID_DELEGATION. Initial/final source, full patches/configs,
compiled programs, guest rootfs, policies/ABI, commands and logs are retained
here; SHA256SUMS and a separate persistent archive establish integrity.
Previous closure/LSM/KCSAN evidence is preserved unchanged.

The personality contract blocker is closed; source-scope reduction is not
retroactive revocation. Whole Filesystem Authority v1 remains NO-GO for the two
previous rare KCSAN families. No production-readiness claim or complete process
confinement is made. Remaining ambiguities are explicitly out-of-scope mechanisms
(global revocation, future delegation prohibitions, other async modes/classes),
not an unresolved identity-only interpretation of the tested personality path.
