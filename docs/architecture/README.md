<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Architecture

Permanent invariant: **A_out ⊆ A_in**, evaluated per transformation against its
legitimately supplied effective Authority at creation. Explicit independent grants
must be identified as inputs; identity alone is not a hidden grant.

The implemented Core owns immutable, refcounted credential-associated state and
a static class dispatcher. Unhandled requests continue native Linux; handled
implemented requests use the owning evaluator; handled unimplemented requests
fail closed. Only filesystem is a production class; synthetic KUnit state does
not create another public resource class.

Filesystem scopes pin object identity (mount and dentry), not a replaceable path
string. Bounded operations cover regular-file data establishment and selected
namespace mutations. Rights, applicable scope and independent Linux/LSM restrictions
remain distinct. This is not complete filesystem mediation or a universal sandbox.

FD aliases share mutable restrictions on an open file description. Independent
clones have their own ceilings, offsets and lifetime. Legitimate delegation may
preserve rights without attenuation; later source reduction does not rewrite old
independent capabilities. Saved fork/io_uring credentials retain legitimate complete
contexts. The qualified personality result is EXPECTED_VALID_DELEGATION, not a
permission-restoration defect or identity-only credential snapshot.

Local attenuation is not global revocation. No revocation API, automatic
credential rebasing, new class or blanket UID-0 bypass is added by this package.
DAC/ACL, LSM, mount/filesystem/namespace/structural restrictions retain their
documented composition and error boundaries.

The full original design is reconstructed byte-for-byte at
`Documentation/authority/architecture.md`, `temporal-semantics.md`,
`design-history.md` and `Documentation/authority-prototype/` in the prepared
kernel. These are not paths in the unmodified linux submodule. Keeping them in the
patches avoids maintaining a second inconsistent architecture source.

See [qualification](../qualification/README.md),
[regression requirements](../regression.md) and [roadmap](../roadmap/README.md).
