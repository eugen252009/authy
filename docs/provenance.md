<!-- SPDX-License-Identifier: GPL-2.0-only -->
# Dependency, patch and signature provenance

Linux is the external gitlink `linux`, pinned to
`e767a4ea70a3992c37ed604157d32f0dfbf9b1e3` from the canonical Torvalds repository:
<https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git>.

Authy has its own independent root/history. A gitlink names a dependency commit;
it does not make that commit an Authy ancestor. Dependency objects under
`.git/modules/linux/` are separate from Authy's own object database and are not
included in an Authy branch push.

[Ordered series](../patches/series) and [checksums](../patches/SHA256SUMS) preserve
the nine original patches exactly. [provenance/patches.json](../provenance/patches.json)
records full original IDs, parent order, subjects, authors, dates, paths and
SHA-256 hashes. The source series ends at
`c8b8dde1d872f7ced4169b7a1109f44577a31c2b`; its qualified full Git tree is
`7fa351dedd010e448ba7b7a12e69789cc7556e93`.

Original raw signed commit records in `provenance/commits/` are **data files**,
not commits imported into Authy's ancestry. Preparation verifies their Git object
identities and byte hashes. The original development repository retains its signed
commits unchanged. Standard patch export does **not** retain Git commit-signature
verification. Applying patches and matching hashes do not independently establish
signer trust; original-record cryptographic verification also requires the
appropriate trusted public key and verification context. No signatures are fabricated.

The [baseline metadata](../qualification/filesystem-v1/baseline.json) links the
full original frozen source manifest and archive identity. The compressed
manifest is an exact, lossless copy; no file list was reconstructed from guesses.
All required formerly untracked C/headers/tests/docs are represented in the patches.

Historical local filesystem paths inside original reports/patches are unmodified
provenance. They are not runtime requirements of this independent repository.
No source/evidence publication, tag or push happened while preparing this package.
