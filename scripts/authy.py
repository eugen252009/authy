#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Pinned-source reconstruction/verification; uses the existing kernel tests."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
QUAL = ROOT / 'qualification/filesystem-v1'


def fail(message):
    raise ValueError(message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def environment(ceiling=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_OPTIONAL_LOCKS'] = '0'
    if ceiling is not None:
        env['GIT_CEILING_DIRECTORIES'] = str(ceiling)
    return env


def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args],
                                   env=environment(), text=True).strip()


def inputs():
    meta = json.loads((QUAL / 'baseline.json').read_text())
    provenance = json.loads((ROOT / 'provenance/patches.json').read_text())
    series = (ROOT / 'patches/series').read_text().splitlines()
    rows = provenance['patches']
    if len(series) != 9 or len(set(series)) != 9:
        fail('Expected exactly nine unique ordered patches')
    if series != [x['patch'] for x in rows]:
        fail('Patch order differs from original commit provenance')
    if meta['linux_commit'] != provenance['linux_base']:
        fail('Linux pin/provenance mismatch')
    parent = meta['linux_commit']
    for name, row in zip(series, rows):
        if not re.fullmatch(r'[0-9]{4}-[A-Za-z0-9_.-]+\.patch', name):
            fail('Invalid patch basename: ' + name)
        if sha(ROOT / 'patches' / name) != row['sha256']:
            fail('Patch hash mismatch: ' + name)
        if row['parent'] != parent:
            fail('Original commit dependency chain mismatch')
        raw = (ROOT / row['original_signed_record']).read_bytes()
        identity = hashlib.sha1(b'commit ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if identity != row['original_commit'] or hashlib.sha256(raw).hexdigest() != row['record_sha256']:
            fail('Original signed record identity mismatch')
        parent = identity
    if parent != provenance['original_tip']:
        fail('Original tip mismatch')
    for path, digest in meta['input_sha256'].items():
        if sha(QUAL / path) != digest:
            fail('Qualification input hash mismatch: ' + path)
    compressed = QUAL / meta['source_manifest']
    data = gzip.decompress(compressed.read_bytes())
    if hashlib.sha256(data).hexdigest() != meta['source_manifest_uncompressed_sha256']:
        fail('Frozen full-source manifest hash mismatch')
    manifest = json.loads(data)
    if manifest['base_head'] != meta['linux_commit'] or len(manifest['entries']) != 96086:
        fail('Unexpected frozen manifest base/count')
    return meta, manifest, series


def dependency(meta):
    linux = ROOT / 'linux'
    url = git(ROOT, 'config', '-f', '.gitmodules', '--get', 'submodule.linux.url')
    path = git(ROOT, 'config', '-f', '.gitmodules', '--get', 'submodule.linux.path')
    if url != meta['linux_url'] or path != 'linux':
        fail('Unexpected .gitmodules URL/path')
    if not (linux / '.git').is_file():
        fail('Initialize the managed linux submodule first; see docs/development.md')
    if git(linux, 'remote', 'get-url', 'origin') != url:
        fail('Dependency origin URL differs from the canonical pin')
    if git(linux, 'rev-parse', 'HEAD') != meta['linux_commit']:
        fail('Linux checkout differs from exact qualified commit')
    expected = '160000 ' + meta['linux_commit']
    if not git(ROOT, 'ls-files', '--stage', '--', 'linux').startswith(expected + ' '):
        fail('Index gitlink differs from the qualified pin')
    if not git(ROOT, 'ls-tree', 'HEAD', '--', 'linux').startswith(expected.replace(' ', ' commit ', 1)):
        fail('Committed gitlink differs from the qualified pin')
    if git(linux, 'status', '--porcelain=v1', '--untracked-files=all'):
        fail('Linux dependency is dirty; leave it untouched and inspect separately')
    return linux


def safe_new_output(value, source=None):
    out = Path(value).expanduser().resolve()
    if out.exists() or out.is_symlink():
        fail('Refusing existing output: ' + str(out))
    if out == ROOT or ROOT / 'linux' in out.parents or ROOT / '.git' in out.parents:
        fail('Output would endanger repository/dependency metadata')
    if ROOT in out.parents and ROOT / '.work' not in out.parents:
        fail('Inside Authy, use ignored .work/ outputs only')
    if source is not None and (out == source or source in out.parents):
        fail('Build output must be outside reconstructed source')
    return out


def verify_source(source, meta, manifest):
    source = Path(source).resolve()
    if not source.is_dir():
        fail('Missing reconstructed source directory')
    actual = set()
    directories = set()
    for parent, dirs, files in os.walk(source, followlinks=False):
        parent = Path(parent)
        for name in list(dirs):
            path = parent / name
            if path.is_symlink():
                actual.add(path.relative_to(source).as_posix())
                dirs.remove(name)
            else:
                directories.add(path.relative_to(source).as_posix())
        actual.update((parent / name).relative_to(source).as_posix() for name in files)
    expected = {x['path']: x for x in manifest['entries']}
    expected_dirs = {str(p) for name in expected for p in Path(name).parents if str(p) != '.'}
    mismatches = []
    for name in sorted(actual & expected.keys()):
        row = expected[name]
        path = source / name
        mode = path.lstat().st_mode
        if row['mode'] == '120000':
            if not stat.S_ISLNK(mode):
                mismatches.append([name, 'not symlink'])
                continue
            digest = hashlib.sha256(os.fsencode(os.readlink(path))).hexdigest()
        else:
            if not stat.S_ISREG(mode):
                mismatches.append([name, 'not regular file'])
                continue
            gitmode = '100755' if mode & stat.S_IXUSR else '100644'
            if gitmode != row['mode']:
                mismatches.append([name, 'Git file mode'])
            digest = sha(path)
        if digest != row['sha256']:
            mismatches.append([name, 'content/symlink target'])
    production = json.loads((QUAL / 'production.json').read_text())
    production_bad = [r['path'] for r in production if r['path'] not in actual or sha(source / r['path']) != r['sha256']]
    relevant = [x for x in expected if x.startswith('tools/testing/selftests/authority/')]
    doc_count = sum(x.startswith(('Documentation/authority/', 'Documentation/authority-prototype/')) for x in expected)
    result = {'baseline': meta['baseline'], 'expected_files_and_symlinks': len(expected),
              'missing': sorted(expected.keys() - actual), 'extra': sorted(actual - expected.keys()),
              'extra_directories': sorted(directories - expected_dirs), 'mismatches': mismatches,
              'production_paths': len(production), 'production_mismatches': production_bad,
              'selftest_build_runner_readme_paths': len(relevant), 'qualification_documentation_paths': doc_count}
    result['verified'] = not any(result[k] for k in ['missing', 'extra', 'extra_directories', 'mismatches', 'production_mismatches'])
    print(json.dumps(result, indent=2), flush=True)
    if not result['verified']:
        fail('Source differs from frozen baseline; do not change qualified code to hide it')
    return result


def prepare(args):
    meta, manifest, series = inputs()
    linux = dependency(meta)
    out = safe_new_output(args.output)
    out.mkdir(parents=True)
    archive = subprocess.Popen(['git', '-C', str(linux), 'archive', '--format=tar', meta['linux_commit']],
                               stdout=subprocess.PIPE, env=environment())
    try:
        subprocess.run(['tar', '--no-same-owner', '-xf', '-', '-C', str(out)], stdin=archive.stdout, check=True)
    finally:
        archive.stdout.close()
        archive_status = archive.wait()
    if archive_status:
        fail('Pinned Linux archive failed')
    env = environment(out.parent)  # Prevent discovery of Authy/.git when using .work/source.
    for name in series:
        patch = ROOT / 'patches' / name
        for flags in [['--check'], []]:
            subprocess.run(['git', 'apply', *flags, str(patch)], cwd=out, env=env, check=True)
    verify_source(out, meta, manifest)
    print('Prepared ' + str(out) + '; dependency was not patched.', flush=True)


def build(args):
    meta, manifest, _ = inputs()
    dependency(meta)
    source = Path(args.source).resolve()
    verify_source(source, meta, manifest)
    out = safe_new_output(args.output, source)
    if args.jobs < 1:
        fail('jobs must be positive')
    config = Path(args.config).resolve() if args.config else None
    if not args.selftests_only and (config is None or not config.is_file()):
        fail('Kernel build requires an explicit existing full --config')
    out.mkdir(parents=True)
    kernel = out / 'kernel'
    kernel.mkdir()
    command_log = []
    def run(command):
        command_log.append(command)
        subprocess.run(command, check=True)
    make = ['make', '-C', str(source), 'O=' + str(kernel)]
    if not args.selftests_only:
        shutil.copyfile(config, kernel / '.config')
        shutil.copyfile(config, out / 'requested.config')
        run(make + ['olddefconfig'])
        if (kernel / '.config').read_bytes() != config.read_bytes():
            fail('olddefconfig changed the supplied config; inspect output, do not claim the qualified config')
        run(make + ['-j' + str(args.jobs), 'bzImage'])
    headers = out / 'headers'
    tests = out / 'tests'
    tests.mkdir()
    run(make + ['headers_install', 'INSTALL_HDR_PATH=' + str(headers)])
    run(['make', '-C', str(source / 'tools/testing/selftests/authority'),
         'OUTPUT=' + str(tests) + '/', '-j' + str(args.jobs),
         'CFLAGS=-static -Wall -O2 -isystem ' + str(headers / 'include')])
    binaries = {p.name: sha(p) for p in sorted(tests.iterdir()) if p.is_file()}
    if len(binaries) != 9:
        fail('Expected nine selftest binaries')
    record = {'commands': command_log, 'selftest_binaries_sha256': binaries,
              'kernel_built': not args.selftests_only, 'tests_executed': False,
              'binary_reproducibility_claim': False}
    (out / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('prepare'); p.add_argument('--output', required=True)
    p = commands.add_parser('verify'); p.add_argument('--source', required=True)
    p = commands.add_parser('build'); p.add_argument('--source', required=True); p.add_argument('--output', required=True)
    p.add_argument('--config'); p.add_argument('--jobs', type=int, default=4); p.add_argument('--selftests-only', action='store_true')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args)
    elif args.command == 'build':
        build(args)
    else:
        meta, manifest, _ = inputs()
        dependency(meta)
        verify_source(args.source, meta, manifest)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('BLOCKED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
