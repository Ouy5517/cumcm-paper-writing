from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]


class EnvironmentReadinessContractTests(unittest.TestCase):
    def read(self, relative):
        return ' '.join((ROOT / relative).read_text(encoding='utf-8').lower().split())

    def test_reference_is_routed_for_engine_and_render_questions(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        paths = {item['path'] for item in manifest['references']['on_demand']}
        self.assertIn('references/environment-readiness.md', paths)

    def test_statuses_and_boundaries_are_explicit(self):
        text = self.read('references/environment-readiness.md')
        for phrase in (
            'ready', 'ready_with_author_checks', 'blocked',
            'selected-year official authority', 'current calendar year',
            'must not select', 'synthetic fixture',
            'not scientific validity', 'absent pdf', 'unverified',
            'xelatex is missing', 'do not silently switch to reportlab',
        ):
            self.assertIn(phrase, text)

    def test_latex_workflow_points_to_readiness_gate(self):
        workflow = self.read('references/latex-production-workflow.md')
        preflight = self.read('references/preflight.md')
        output = self.read('static/core/output-format.md')
        self.assertIn('environment-readiness.md', workflow)
        self.assertIn('environment-readiness.md', preflight)
        self.assertIn('ready_with_author_checks', output)

    def test_no_claim_of_rendered_pass_without_a_fresh_pdf(self):
        text = self.read('references/environment-readiness.md')
        self.assertIn('source compilation alone', text)
        self.assertIn('cannot claim visual', text)
        self.assertIn('older pdf', text)


if __name__ == '__main__':
    unittest.main()
