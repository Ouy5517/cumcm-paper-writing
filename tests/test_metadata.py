import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_skill.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class MetadataTests(unittest.TestCase):
    def test_repository_routes_resolve(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_missing_axis_target_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('SKILL.md', 'manifest.yaml'):
                shutil.copyfile(ROOT / name, root / name)
            for name in ('agents', 'static', 'references'):
                shutil.copytree(ROOT / name, root / name)
            (root / 'static/fragments/task/plan.md').unlink()
            self.assertTrue(any('plan.md' in message for message in validator.validate(root)))
