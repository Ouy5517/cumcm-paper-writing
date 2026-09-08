import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('builder', Path(__file__).resolve().parents[1] / 'scripts/build_pdf.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
    def test_permission_denied_path_entry_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / 'paper.tex', root / 'paper.pdf'
            source.write_text('test source', encoding='utf-8')
            restricted = r'C:\Users\14564\AppData\Local\Microsoft\WindowsApps'
            calls = []

            def compiler(command, **kwargs):
                calls.append(command)
                work = Path(next(x.split('=', 1)[1] for x in command
                                 if x.startswith('-output-directory=')))
                (work / 'paper.log').write_text('', encoding='utf-8')
                (work / 'paper.pdf').write_bytes(b'%PDF-new')
                return subprocess.CompletedProcess(command, 0, '', '')

            original_is_dir = builder.Path.is_dir

            def guarded_is_dir(path):
                if str(path) == restricted:
                    raise PermissionError('access denied')
                return original_is_dir(path)

            with patch.object(builder.Path, 'is_dir', guarded_is_dir), \
                 patch.object(builder.shutil, 'which', return_value='xelatex') as which, \
                 patch.object(builder.subprocess, 'run', side_effect=compiler), \
                 patch.dict(os.environ, {'PATH': os.pathsep.join([restricted, str(root)])}, clear=False):
                builder.build(source, output)

            self.assertEqual(output.read_bytes(), b'%PDF-new')
            self.assertEqual(len(calls), 2)
            self.assertNotIn(restricted, which.call_args.kwargs['path'])

    def exercise(self, mode):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / 'paper.tex', root / 'paper.pdf'
            source.write_text('test source')
            output.write_bytes(b'%PDF-old')
            calls = []

            def compiler(command, **kwargs):
                calls.append(command)
                work = Path(next(x.split('=', 1)[1] for x in command if x.startswith('-output-directory=')))
                (work / 'paper.log').write_text('Missing character: x' if mode == 'glyph' else '')
                if mode != 'missing':
                    (work / 'paper.pdf').write_bytes(b'%PDF-new')
                code = 1 if mode == 'fail' else 0
                return subprocess.CompletedProcess(command, code, 'compiler output', '')

            with patch.object(builder.shutil, 'which', return_value='xelatex'), patch.object(builder.subprocess, 'run', side_effect=compiler):
                if mode == 'success':
                    # An ordinary template directory need not contain CUMCM files.
                    builder.build(source, output, template=root)
                    self.assertEqual(output.read_bytes(), b'%PDF-new')
                    self.assertEqual(len(calls), 2)
                else:
                    with self.assertRaises(RuntimeError):
                        builder.build(source, output)
                    self.assertEqual(output.read_bytes(), b'%PDF-old')
            self.assertEqual(list(root.glob('cumcm-build-*')), [])

    def test_failed_compiler_preserves_existing_pdf(self):
        self.exercise('fail')

    def test_missing_output_cannot_reuse_old_pdf(self):
        self.exercise('missing')

    def test_missing_glyph_blocks_publication(self):
        self.exercise('glyph')

    def test_success_runs_twice_and_replaces_pdf(self):
        self.exercise('success')

    def test_missing_template_is_actionable(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'paper.tex'
            source.touch()
            with self.assertRaisesRegex(FileNotFoundError, 'Template directory'):
                builder.build(source, source.with_suffix('.pdf'), Path(directory) / 'missing')
