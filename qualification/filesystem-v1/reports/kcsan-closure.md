# Final KCSAN attribution and Filesystem Authority v1 decision

## Decision and scope

**CONDITIONAL GO** for the established experimental Filesystem Authority v1
scope. Both recovered families are classified **UPSTREAM_EXISTING_INDEPENDENT**
for the current Authority delta. This accepts independent native Linux behavior
as a bounded dependency limitation; it does **not** declare either full kernel
sanitizer-clean, prove every upstream access benign, or claim production readiness.

The independent temporal verdict remains EXPECTED_VALID_DELEGATION. The invariant
A_out ⊆ A_in and its creation-time, independent-capability versus shared-state,
LSM/provenance and non-revocation rules are unchanged.

## Interruption: what was actually blocked

The session record shows provider/model response generation to the previous
request stopped with a cybersecurity-risk error **before any tool call**.
No shell command, source edit or QEMU invocation was rejected in that turn.
RESTRICTION.md and restriction-record.json quote the exact error, identify the
request by digest and explain the boundary. No rejected operation was retried.
The last successful checkpoint was the temporal archive/content verification.

This continuation performed only independent file/log/source/ELF inspection,
hash checks and evidence/documentation work. **New kernel executions: zero.**
A new rare-event/device-toggle campaign is BLOCKED/NOT EXECUTED under the current
instruction, not claimed attempted and not described as a proven KVM denial.
Attribution is supported by source and machine-code evidence plus the existing
executions, not by substituting an unobserved pristine runtime reproduction.

## Exact baseline and preservation

HEAD/master: e767a4ea70a3992c37ed604157d32f0dfbf9b1e3, Linux 7.3.0-rc5, with the
preserved uncommitted prototype. baseline-status/baseline.patch and the initial
ledger copy identify the starting state. All 32 changed/new production paths
match the temporal qualified production hashes. **No production code changed.**
Only the qualification ledger and new evidence files change in this checkpoint.
Earlier closure, temporal, LSM and archived reports remain untouched.

Fourteen relevant timer/idle/serial/tty source/type files compare byte-identical
between current tree, git HEAD and the retained pristine staging source.
Five complete compiled .text sections compare byte-identical between the
matched original strict current/pristine outputs:

* timer_migration.o, tick-sched.o;
* 8250_port.o, 8250_core.o, serial_core.o.

DWARF type layouts for tmigr_cpu, tmigr_event and uart_8250_port match exactly.
Target PCs resolve to the same lines/field operations in both ELFs; absolute
link addresses differ normally. Whole object debug hashes can differ because
build/source paths and link context differ; only actual code identity is claimed.
source-object-config-comparison.json and layout-comparison.json record checks.

Original strict configs match byte-for-byte: PREEMPT_DYNAMIC, SMP/NO_HZ_IDLE,
HOTPLUG_CPU, KCSAN_STRICT, DWARF5, KCSAN task/IRQ delays 80/20 us, skip-watch
4000 randomized, log buffer shift18, serial console enabled, KUNIT=n. Expanded
verbose strict configs also match each other but are a separate cohort, not
interchangeable with the original. Retained guest banners identify GCC
14.2.0-19/binutils 2.44. QEMU q35/KVM, -cpu host, 4 CPUs/4096 MiB, no NIC/shared
host filesystem; exact existing commands are retained. No kernel/tool rebuild
or new workload is reported.

## Finding A: timer migration

Raw report: control-fixed/serial.log, unique timestamp 1.246757 s; target byte
0xffffa1ebfbc1d2c4, tmigr_cpu.cpuevt.ignore, offset132 in a 136-byte tmigr_cpu.
CPU1 timer softirq reads READ_ONCE(evt->ignore) under group.lock at
c:609/tmigr_next_groupevt+0x5f. CPU0 idle exit writes true at
c:718/__tmigr_cpu_activate+0x97 under tmc.lock with local IRQs disabled.
These are different locks; CPU0 IRQ exclusion does not serialize CPU1.

The field is an expressly documented hint. Activation deliberately avoids
parent queue locking; stale queue selection may lead to unnecessary remote
handling. Before expiration, the native handler takes target tmc.lock and
rechecks available/remote/ignore/expiry, then rechecks state before republication.
Atomic group migrator/active sequencing and bottom-up queue locking remain.
Per-CPU state and group lifetime rules exclude Authority ownership/freeing.
See TIMER.md for complete stacks, ordering and compiler/annotation limits.

Attribution is not based on source-directory location: the access instructions,
field layout, state/lock ownership and timer/idle call paths exist unchanged in
pristine. No Authority memory access, asynchronous callback, IRQ or lifetime
change reaches that state. The occurrence precedes /init at 7.504735 s;
KUNIT=n, initial Authority=NULL, no Authority boot grant/initcall, and NULL
credential hooks do not queue Authority cleanup. Instrumentation/global timing
may change when the existing pair is observed, but do not create the pair.

**Classification: UPSTREAM_EXISTING_INDEPENDENT.** The intended hint/recheck
contract supports stale-hint tolerance; no universal BENIGN or INSTRUMENTATION
ARTIFACT designation is needed to establish independent native origin.

## Finding B: serial startup/IRQ

Raw report: full-kcsan-fixed/serial.log, unique timestamp 7.266288 s; address
0xffffffff9a45112e, the software IER shadow byte at uart_8250_port offset718.
CPU0 PID1 console_on_rootfs startup writes UART_IER_RLSI|UART_IER_RDI at
8250_port.c:2390/startup+0x919. CPU3 hard IRQ tests UART_IER_THRI at
line1857/handle_irq_locked+0x104 while otherwise in idle.

The guest identifies the default q35 serial device as 16550A ttyS0 at 0x3f8,
IRQ4. Startup is serialized by a per-port/tty mutex; IRQ read holds port.lock.
setup_irq precedes the unguarded software-shadow assignment, which is outside
startup's earlier scoped port locks. A pending/console/test-generated IRQ is
therefore reachable without Authority. Deferring hardware RX enable is not a
proof that this software byte cannot race. Hardware register writes and the
software shadow must not be conflated. General benignness is not established.

Unlike timer, the ancestry passes through modified VFS opening code. This can
alter timing/layout and was not ignored. File initialization writes its separate
f_capability=NULL; console is S_IFCHR, not a supported managed regular file.
Authority=NULL gives native continuation. No change touches IER, port state,
port mutex/spinlock, IRQ setup or serial lifetime; matching full serial-core
and driver text/layout confirms the native access relationship, not merely a
matching warning title. The report precedes /init at 7.409368 s, before any
userspace Authority grant/domain. See SERIAL.md for the complete analysis.

**Classification: UPSTREAM_EXISTING_INDEPENDENT.** No serial driver fix, arbitrary
lock, warning suppression, credential change or LSM adjustment was introduced.

## Differential evidence: observations, not fabricated passes

110 available existing serial-log files were scanned and hashed. These are
not 110 independent matched trials: they include different configs, historical
states, reruns and ordinary non-KCSAN images. Only two logs contain the target
families, once each after console/dmesg deduplication. **No existing pristine
log contains either exact report.** This is explicitly not proof of absence.

| Historical cohort | Last logged guest kernel time | All unique KCSAN | Target events |
|---|---:|---:|---|
| Original strict native current | 74.420778 s | 143 | timer 1 |
| Original strict native pristine | 73.155624 s | 139 | 0 |
| Original strict full current | 84.223584 s | 141 | serial 1 |
| Expanded verbose full current | 127.370977 s | 171 | 0 |
| Expanded verbose native pristine | 86.497459 s | 136 | 0 |
| Four expanded pristine boot smokes | 12.791795/12.841803/12.651143/12.642221 s | 0 each | 0 |

Logged times are approximate observation-window endpoints, not measured equal
wall durations or event rates. The original native pair has identical initramfs
SHA/workload executables as well as matching config/device/CPU/memory settings.
The full and expanded native rows do not have identical workloads/windows.
There is no device-disabled historical control. New equal-count/duration boot,
serial-toggle or timer-idle trials remain unexecuted. Reproduction statistics
and functional TAP groups are separate in existing-comparison-cohorts.json.

Why this can dispose attribution despite an unobserved pristine event: both
native instruction/control-flow pairs, types, synchronization and lifetime
exist in pristine, and the affected code/contexts have no Authority state edge.
This is source-level origin evidence, not an inference from negative testing.
Exact pristine runtime recurrence would strengthen confidence but is not claimed
or substituted. The narrow verdict concerns whether the Authority delta creates
the accesses/ordering/lifetime defect; upstream correctness is a separate concern.

## Requalification applicability and historical results

New runtime tests: **NOT EXECUTED**. New verification: production equality,
source/code/layout/config comparison, 110-log inventory and integrity checks.
Temporal archive SHA and all 230 evidence manifest files were reverified. The
prior results remain historical, newly checked for applicability to unchanged
production code, not relabeled as freshly run:

* temporal regular/KASAN/strict: 15/0/1 each; pristine regular/strict 2/0/14;
* Authority/filesystem/Landlock: 42/0/0 regular/KASAN; Core separately 10/10;
* temporal AppArmor/SELinux: 3/0/0 each selected config;
* prior complete regular/KASAN set 536/0/11 (distinct upstream/fixture groups),
  compat32 42/0/0; bounded LTP 24 successful executable exits and 331 modern
  summary passes per image, legacy fcntl01 without invented assertion count.

No test count is combined across unrelated units or configs. Existing warnings,
SKIPs, initial fixture failures, accepted filesystem/LSM/configuration boundaries,
GCC analyzer/source-review limits and absent global revocation remain documented.
No unrelated expensive suite was rerun and no result was manufactured from a
powered-off QEMU or a toolchain/config comparison.

## Final gates and conditions

| Gate | Assessment | Basis |
|---|---|---|
| A Functional | PASS | Applicable unchanged-source retained qualification |
| B Security invariants | PASS | Temporal EXPECTED_VALID_DELEGATION resolves the earlier scoped ambiguity; existing LSM/FD invariants retained |
| C Kernel compatibility | PASS | Applicable native/UNHANDLED/pristine and bounded LTP comparisons |
| D LSM integration | PASS | Exact qualified Landlock/SELinux/AppArmor policies and configurations, not arbitrary LSMs |
| E Concurrency/memory safety | ACCEPTED_LIMITATION | Two native pre-existing independent families accepted as baseline dependency behavior; no clean-kernel claim |
| F Regression coverage | ACCEPTED_LIMITATION | Existing named invariants; original 21/47 individual identities unrecovered |
| G Reproducibility | PASS after manifest/archive verification | Source/config/code comparison and complete referenced evidence preserved |
| H Configuration support | ACCEPTED_LIMITATION | Always-built supported x86_64 + compat scope; unavailable feature-off B not credited |

**CONDITIONAL GO**, not unrestricted GO. Conditions/boundaries:

1. Only the established experimental v1 filesystem operations, simple-FS FD
   support, tested generic/callback/exceptional paths and recorded LSM/config
   matrix are claimed; no universal Linux/process/kernel security certification.
2. The underlying Linux baseline's independent timer/serial KCSAN findings are
   explicitly retained and accepted, not fixed, suppressed or called harmless.
   Any new Authority state/synchronization/lifetime connection or functional
   symptom requires reassessment; a sanitizer-clean baseline needs separate work.
3. Temporal delegation, input provenance, source-versus-alias semantics and
   independent LSM restrictions remain unchanged. No retroactive attenuation,
   no-delegation CLI, global revocation, new class, Rescue/sealing or restricted
   native-module isolation is inferred.
4. New intrusive reproduction remains blocked/not attempted under this session
   instruction; exact pristine recurrence/device-off comparisons are unqualified,
   not hidden as PASS. This limits runtime confidence, not the demonstrated
   unchanged origin of the observed native access pairs.

There is no remaining confirmed Authority-specific release blocker within this
bounded attribution scope. The earlier NO-GO reports are historical checkpoints,
not overwritten. A stricter release requiring a wholly sanitizer-clean kernel or
fresh runtime recurrence cannot use this conditional decision as satisfaction.

## Evidence

restriction-record.json, RESTRICTION.md, TIMER.md, SERIAL.md, classification.json,
source-object-config-comparison.json, DWARF/PC/disassembly files, full original
raw reports, copied retained runs, existing comparison cohorts and log inventory
support this report. Prior archives remain intact. Final SHA256SUMS and a new
separate kcsan-closure archive retain the result; integrity must be checked,
not inferred from successful file creation. No host deployment, reboot, commit,
push/publication, security weakening or production source modification occurred.
