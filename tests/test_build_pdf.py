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
                messages = {'glyph': 'Missing character: x', 'citation': "LaTeX Warning: Citation `missing' on page 1 undefined"}
                (work / 'paper.log').write_text(messages.get(mode, ''))
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
                    self.assertTrue(all('-no-shell-escape' in c for c in calls))
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

    def test_unresolved_citation_blocks_publication(self):
        self.exercise('citation')

    def test_success_runs_twice_and_replaces_pdf(self):
        self.exercise('success')

    def test_missing_template_is_actionable(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'paper.tex'
            source.touch()
            with self.assertRaisesRegex(FileNotFoundError, 'Template directory'):
                builder.build(source, source.with_suffix('.pdf'), Path(directory) / 'missing')

    def bibliography(self, backend, mode='success'):
        with tempfile.TemporaryDirectory(prefix='bibliography test ') as directory:
            root = Path(directory)
            source, output = root / 'paper.tex', root / 'published' / 'paper.pdf'
            source.touch()
            output.parent.mkdir()
            output.write_bytes(b'%PDF-old')
            calls = []
            work = None

            def compiler(command, **kwargs):
                nonlocal work
                calls.append(command)
                if command[0] == 'xelatex':
                    self.assertIn('-no-shell-escape', command)
                    work = Path(next(x.split('=', 1)[1] for x in command if x.startswith('-output-directory=')))
                    (work / 'paper.log').write_text('')
                    (work / 'paper.pdf').write_bytes(b'%PDF-new')
                    if backend == 'biber':
                        (work / 'paper.bcf').write_text('<controlfile/>')
                    else:
                        (work / 'paper.aux').write_text('\\bibdata{refs}\\bibstyle{plain}')
                else:
                    self.assertEqual(command[0], backend)
                    self.assertTrue(kwargs['env']['BIBINPUTS'].startswith(str(root) + os.pathsep))
                    self.assertTrue(kwargs['env']['BSTINPUTS'].startswith(str(root) + os.pathsep))
                    if mode == 'fail':
                        return subprocess.CompletedProcess(command, 1, 'bibliography failed', '')
                    if mode != 'missing_bbl':
                        (work / 'paper.bbl').write_text('bibliography')
                return subprocess.CompletedProcess(command, 0, '', '')

            def which(command, **kwargs):
                return None if mode == 'unavailable' and command == backend else command

            with patch.object(builder.shutil, 'which', side_effect=which), patch.object(builder.subprocess, 'run', side_effect=compiler):
                if mode == 'success':
                    builder.build(source, output)
                    self.assertEqual(output.read_bytes(), b'%PDF-new')
                    self.assertEqual([c[0] for c in calls], ['xelatex', backend, 'xelatex', 'xelatex'])
                else:
                    with self.assertRaises((FileNotFoundError, RuntimeError)):
                        builder.build(source, output)
                    self.assertEqual(output.read_bytes(), b'%PDF-old')
            self.assertEqual(list(output.parent.glob('cumcm-build-*')), [])

    def test_bibliography_backends_run_between_tex_passes(self):
        for backend in ('bibtex', 'biber'):
            with self.subTest(backend=backend):
                self.bibliography(backend)

    def test_bibliography_failure_preserves_existing_pdf(self):
        for backend in ('bibtex', 'biber'):
            for mode in ('fail', 'missing_bbl', 'unavailable'):
                with self.subTest(backend=backend, mode=mode):
                    self.bibliography(backend, mode)
