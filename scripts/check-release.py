#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Read-only local release checks; never pushes or installs dependencies."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import authy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    root = authy.ROOT
    meta, manifest, _ = authy.inputs()
    authy.dependency(meta)
    authy.verify_source(args.source, meta, manifest)
    if authy.git(root, 'status', '--porcelain=v1', '--untracked-files=all'):
        authy.fail('Standalone repository is not clean')
    if authy.git(root, 'rev-parse', '--is-shallow-repository') != 'false':
        authy.fail('Authy history itself must not be shallow')
    wanted = 'git@github.com:eugen252009/authy.git'
    if authy.git(root, 'remote', 'get-url', 'origin') != wanted or authy.git(root, 'remote', 'get-url', '--push', 'origin') != wanted:
        authy.fail('Unexpected publication remote')
    ancestry = authy.git(root, 'rev-list', '--all').splitlines()
    if meta['linux_commit'] in ancestry:
        authy.fail('Linux ancestry was imported')
    test = subprocess.run(['git', '-C', str(root), 'cat-file', '-e', meta['linux_commit'] + '^{commit}'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=authy.environment())
    if test.returncode == 0:
        authy.fail('Linux commit unexpectedly exists in Authy own object database')
    subprocess.run(['git', '-C', str(root), 'fsck', '--connectivity-only', '--no-reflogs'],
                   check=True, env=authy.environment())
    entries = subprocess.check_output(['git', '-C', str(root), 'ls-files', '--stage', '-z'], env=authy.environment()).split(b'\0')
    files = []
    for entry in entries:
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        path = raw_path.decode()
        if metadata.startswith(b'160000 '):
            if path != 'linux': authy.fail('Unexpected dependency gitlink')
            continue
        files.append(path)
    sensitive = []
    broken = []
    patterns = {
        'private-key': rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----',
        'github-token': rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b',
        'cloud-key': rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
        'credential-url': rb'(?i)\bhttps?://[^\s/:<>]+:[^\s/@<>]+@',
    }
    maximum = 0
    for name in files:
        path = root / name
        data = path.read_bytes()
        maximum = max(maximum, len(data))
        if len(data) > 100 * 1024**2:
            authy.fail('Oversized Git blob: ' + name)
        if data.startswith((b'\x7fELF', b'QFI\xfb', b'SQLite format 3\0')):
            authy.fail('Unexpected binary/database/image: ' + name)
        for category, pattern in patterns.items():
            if re.search(pattern, data): sensitive.append({'path': name, 'category': category})
        # Historical reports/patches preserve old local references verbatim; active landing/docs links must resolve.
        if name.endswith('.md') and (name == 'README.md' or name.startswith('docs/') or name.endswith('/README.md')):
            for target in re.findall(r'\]\(([^)]+)\)', data.decode('utf-8')):
                target = target.split('#', 1)[0]
                if target and '://' not in target and not target.startswith('mailto:') and not (path.parent / target).exists():
                    broken.append({'path': name, 'target': target})
    if sensitive or broken:
        print(json.dumps({'sensitive_candidates': sensitive, 'broken_active_links': broken}, indent=2))
        authy.fail('Publication hygiene/link review required; values are not printed')
    print(json.dumps({'local_publication_checks': 'PASS', 'own_commits': len(ancestry),
                      'tracked_files_excluding_linux_gitlink': len(files), 'largest_tracked_file_bytes': maximum,
                      'linux_history_imported': False, 'sensitive_pattern_candidates': [], 'broken_active_links': [],
                      'remote_content_check': 'Run git ls-remote separately immediately before any authorized push',
                      'push_executed': False}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('BLOCKED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
