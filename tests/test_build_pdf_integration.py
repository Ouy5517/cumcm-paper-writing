from pathlib import Path
import importlib.util
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('builder', ROOT / 'scripts' / 'build_pdf.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


@unittest.skipUnless(shutil.which('xelatex'), 'xelatex/MiKTeX is not installed')
class RealXeLaTeXBuildTests(unittest.TestCase):
    def test_real_xelatex_build_produces_fresh_pdf(self):
        with tempfile.TemporaryDirectory(prefix='cumcm-integration-') as directory:
            root = Path(directory)
            source = root / 'paper.tex'
            output = root / 'paper.pdf'
            source.write_text(
                (ROOT / 'tests' / 'fixtures' / 'minimal-xelatex.tex').read_text(encoding='utf-8'),
                encoding='utf-8',
            )
            result = builder.build(source, output)
            self.assertEqual(result, output.resolve())
            self.assertTrue(output.is_file())
            self.assertTrue(output.read_bytes().startswith(b'%PDF-'))
            self.assertEqual(list(root.glob('cumcm-build-*')), [])


if __name__ == '__main__':
    unittest.main()
