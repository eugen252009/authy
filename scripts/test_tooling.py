#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Small reconstruction-tool tests; not kernel qualification tests."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import authy


class ToolingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='authy-tool-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'source'
        self.source.mkdir()
        (self.source / 'file').write_bytes(b'qualified\n')
        (self.source / 'run').write_bytes(b'#!/bin/sh\n')
        (self.source / 'run').chmod(0o755)
        (self.source / 'link').symlink_to('file')
        self.entries = []
        for name, mode in [('file', '100644'), ('run', '100755'), ('link', '120000')]:
            p = self.source / name
            data = os.fsencode(os.readlink(p)) if p.is_symlink() else p.read_bytes()
            self.entries.append({'path': name, 'mode': mode, 'sha256': hashlib.sha256(data).hexdigest()})
        self.qual = self.base / 'qual'
        self.qual.mkdir()
        (self.qual / 'production.json').write_text(json.dumps([self.entries[0]]))

    def verify(self):
        with patch.object(authy, 'QUAL', self.qual), contextlib.redirect_stdout(io.StringIO()):
            return authy.verify_source(self.source, {'baseline': 'synthetic-tool-test'}, {'entries': self.entries})

    def test_complete(self):
        self.assertTrue(self.verify()['verified'])

    def test_content_change(self):
        (self.source / 'file').write_bytes(b'changed\n')
        with self.assertRaises(ValueError): self.verify()

    def test_missing(self):
        (self.source / 'run').unlink()
        with self.assertRaises(ValueError): self.verify()

    def test_extra(self):
        (self.source / 'unexpected.rej').write_text('not allowed')
        with self.assertRaises(ValueError): self.verify()

    def test_extra_directory(self):
        (self.source / 'unexpected').mkdir()
        with self.assertRaises(ValueError): self.verify()

    def test_mode(self):
        (self.source / 'run').chmod(0o644)
        with self.assertRaises(ValueError): self.verify()

    def test_link(self):
        (self.source / 'link').unlink()
        (self.source / 'link').symlink_to('run')
        with self.assertRaises(ValueError): self.verify()

    def test_existing_output(self):
        with self.assertRaises(ValueError): authy.safe_new_output(str(self.source))

    def test_build_inside_source(self):
        with self.assertRaises(ValueError): authy.safe_new_output(str(self.source / 'out'), self.source)

    def test_repository_output_guard(self):
        with self.assertRaises(ValueError): authy.safe_new_output(str(authy.ROOT / 'unsafe-output'))


if __name__ == '__main__':
    unittest.main()
