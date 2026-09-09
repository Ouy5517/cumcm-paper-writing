"""Opt in with CUMCM_RUN_TEX_INTEGRATION=1; requires installed TeX tools."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('real_builder', Path(__file__).resolve().parents[1] / 'scripts/build_pdf.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

BIB = '''@book{knuth1984,
  author = {Donald Knuth},
  title = {The TeXbook},
  year = {1984},
  publisher = {Addison-Wesley}
}
'''


@unittest.skipUnless(os.environ.get('CUMCM_RUN_TEX_INTEGRATION') == '1', 'opt-in real TeX integration')
class RealBibliographyTests(unittest.TestCase):
    def compile(self, backend, missing=False):
        for tool in ('xelatex', backend, 'pdftotext'):
            if not shutil.which(tool):
                self.skipTest(f'{tool} unavailable')
        with tempfile.TemporaryDirectory(prefix='cumcm real bibliography ') as directory:
            root = Path(directory)
            source_dir, output_dir = root / 'source files', root / 'published pdf'
            source_dir.mkdir()
            output_dir.mkdir()
            (source_dir / 'refs').mkdir()
            (source_dir / 'refs' / 'library.bib').write_text(BIB, encoding='utf-8')
            source = source_dir / 'paper.tex'
            if backend == 'biber':
                preamble = r'\usepackage[backend=biber]{biblatex}' + '\n' + r'\addbibresource{refs/library.bib}'
                bibliography = r'\printbibliography'
            else:
                preamble = ''
                bibliography = r'\bibliographystyle{plain}' + '\n' + r'\bibliography{refs/library}'
            key = 'missing-key' if missing else 'knuth1984'
            source.write_text('\n'.join([r'\documentclass{article}', preamble, r'\begin{document}',
                r'A verified citation: \cite{' + key + '}.', bibliography, r'\end{document}']), encoding='utf-8')
            output = output_dir / 'paper.pdf'
            output.write_bytes(b'%PDF-old')
            if missing:
                with self.assertRaisesRegex(RuntimeError, 'Unresolved typesetting errors'):
                    builder.build(source, output)
                self.assertEqual(output.read_bytes(), b'%PDF-old')
            else:
                builder.build(source, output)
                self.assertTrue(output.read_bytes().startswith(b'%PDF-'))
                result = subprocess.run(['pdftotext', str(output), '-'], capture_output=True, text=True, check=True)
                self.assertIn('The TeXbook', result.stdout)
                self.assertIn('1984', result.stdout)
                self.assertNotIn('?', result.stdout)
            self.assertEqual(list(output_dir.glob('cumcm-build-*')), [])
            self.assertEqual({p.name for p in source_dir.iterdir()}, {'paper.tex', 'refs'})

    def test_real_bibtex_with_relative_bib_and_separate_output(self):
        self.compile('bibtex')

    def test_real_biber_with_relative_bib_and_separate_output(self):
        self.compile('biber')

    def test_real_missing_bibtex_citation_preserves_old_pdf(self):
        self.compile('bibtex', missing=True)

    def test_real_missing_biber_citation_preserves_old_pdf(self):
        self.compile('biber', missing=True)
