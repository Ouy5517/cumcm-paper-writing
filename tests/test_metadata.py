import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_skill.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class MetadataTests(unittest.TestCase):
    def temporary_skill(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for name in ('SKILL.md', 'manifest.yaml'):
            shutil.copyfile(ROOT / name, root / name)
        for name in ('agents', 'static', 'references'):
            shutil.copytree(ROOT / name, root / name)
        return root

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

    def test_missing_section_fragment_is_detected(self):
        root = self.temporary_skill()
        path = 'static/fragments/section/abstract.md'
        (root / path).unlink()
        self.assertIn(f'Missing route: {path}', validator.validate(root))

    def test_missing_model_family_fragment_is_detected(self):
        root = self.temporary_skill()
        path = 'static/fragments/model_family/prediction.md'
        (root / path).unlink()
        self.assertIn(f'Missing route: {path}', validator.validate(root))

    def test_absolute_route_is_detected(self):
        root = self.temporary_skill()
        manifest_path = root / 'manifest.yaml'
        manifest = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))
        path = str(root / 'static/core/stance.md')
        manifest['always_load'][0] = path
        manifest_path.write_text(yaml.safe_dump(manifest), encoding='utf-8')
        self.assertIn(f'Route escapes skill: {path}', validator.validate(root))

    def test_repository_escaping_route_is_detected(self):
        root = self.temporary_skill()
        manifest_path = root / 'manifest.yaml'
        manifest = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))
        path = '../outside.md'
        manifest['always_load'][0] = path
        manifest_path.write_text(yaml.safe_dump(manifest), encoding='utf-8')
        self.assertIn(f'Route escapes skill: {path}', validator.validate(root))

    def test_duplicate_always_load_route_is_detected(self):
        root = self.temporary_skill()
        manifest_path = root / 'manifest.yaml'
        manifest = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))
        path = manifest['always_load'][0]
        manifest['always_load'].append(path)
        manifest_path.write_text(yaml.safe_dump(manifest), encoding='utf-8')
        self.assertIn(f'Duplicate route: {path}', validator.validate(root))

    def test_default_absent_from_axis_is_detected(self):
        root = self.temporary_skill()
        manifest_path = root / 'manifest.yaml'
        manifest = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))
        manifest['axes']['task']['default'] = 'missing-task'
        manifest_path.write_text(yaml.safe_dump(manifest), encoding='utf-8')
        self.assertIn('Invalid default: task', validator.validate(root))

    def test_deleted_language_fragments_are_not_manifest_targets(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        route_targets = list(manifest['always_load'])
        for axis in manifest['axes'].values():
            route_targets.extend(axis['values'].values())
        route_targets.extend(item['path'] for item in manifest['references']['on_demand'])
        self.assertNotIn('static/fragments/language/zh.md', route_targets)
        self.assertNotIn('static/fragments/language/en.md', route_targets)
