from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class CumcmSpecializationContractTests(unittest.TestCase):
    @staticmethod
    def normalized_text(relative_path):
        text = (ROOT / relative_path).read_text(encoding='utf-8')
        return ' '.join(text.split())

    def test_public_descriptions_are_cumcm_only(self):
        for relative_path in ('SKILL.md', 'README.md', 'agents/openai.yaml'):
            text = (ROOT / relative_path).read_text(encoding='utf-8')
            self.assertIn('CUMCM', text, relative_path)
            for unsupported_scope in ('MCM/ICM', 'course exercises', 'generic contest'):
                self.assertNotIn(unsupported_scope, text, relative_path)

    def test_all_active_guidance_is_cumcm_only(self):
        active_files = [ROOT / 'SKILL.md', ROOT / 'manifest.yaml', ROOT / 'README.md',
                        ROOT / 'agents' / 'openai.yaml']
        active_files.extend((ROOT / 'static').rglob('*'))
        active_files.extend((ROOT / 'references').rglob('*'))
        rejected = ('mcm/icm', 'course exercises', 'unknown contests', 'generic contest')
        generic_patterns = {
            'contest-profile dependency': r'contest-profile',
            'contest profile wording': r'\b(?:selected )?contest profile\b',
            'profile-based packaging': r'\bprofile-based\b',
            'profile delivery wording': r"\bprofile's permitted delivery form\b",
            'course compatibility': r'\bcourse work\b',
            'all-contest compatibility': r'\ball contests\b',
            'non-CUMCM letter/memo delivery': r'\bletters?(?:/memos| or printed materials)\b',
            'generic adaptation': r'\badapt to the problem and contest\b',
        }
        for path in active_files:
            if not path.is_file():
                continue
            text = path.read_text(encoding='utf-8').lower()
            for phrase in rejected:
                self.assertNotIn(phrase, text, str(path.relative_to(ROOT)))
            for label, pattern in generic_patterns.items():
                self.assertIsNone(
                    re.search(pattern, text),
                    f'{path.relative_to(ROOT)}: {label}',
                )

    def test_obsolete_contest_profile_is_removed_from_files_and_routes(self):
        self.assertFalse((ROOT / 'references' / 'contest-profile.md').exists())
        active_files = [ROOT / 'SKILL.md', ROOT / 'manifest.yaml', ROOT / 'README.md',
                        ROOT / 'agents' / 'openai.yaml']
        active_files.extend((ROOT / 'static').rglob('*'))
        active_files.extend((ROOT / 'references').rglob('*'))
        for path in active_files:
            if path.is_file():
                self.assertNotIn(
                    'contest-profile', path.read_text(encoding='utf-8').lower(),
                    str(path.relative_to(ROOT)),
                )

    def test_authority_guidance_distinguishes_rules_from_editorial_advice(self):
        authority_paths = (
            'references/year-selection.md',
            'references/requirements.md',
            'references/cumcmthesis-template.md',
            'static/core/contest-baseline.md',
        )
        for path in authority_paths:
            authority = self.normalized_text(path).lower()
            for phrase in ('binding cumcm rule', 'non-binding editorial guidance',
                           'selected year', 'official notice', 'supplied template'):
                self.assertIn(phrase, authority, f'{path}: {phrase}')

        requirements = self.normalized_text('references/requirements.md').lower()
        for year in ('2019', '2025', '2026'):
            self.assertIn(year, requirements)
        self.assertIn('unverified research pointers', requirements)
        self.assertIn('never automatic defaults', requirements)

    def test_code_policy_is_subordinate_to_verified_cumcm_rules(self):
        text = self.normalized_text('references/code-appendix.md').lower()
        for value in ('full', 'core', 'none', 'unresolved'):
            self.assertRegex(text, rf'\b{value}\b')
        self.assertIn('subordinate to verified cumcm rules', text)

    def test_manifest_exposes_only_current_axes_and_tasks(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        self.assertEqual(manifest['version'], '2.0.0')
        self.assertNotIn('contest', manifest['axes'])
        self.assertNotIn('language', manifest['axes'])
        self.assertEqual(set(manifest['axes']), {'task', 'delivery', 'section', 'model_family'})
        self.assertEqual(
            set(manifest['axes']['task']['values']),
            {
                'plan', 'draft-section', 'draft-paper', 'polish', 'restructure',
                'audit', 'preflight', 'submission-package',
            },
        )
        self.assertEqual(
            manifest['axes']['task']['values']['polish'],
            'static/fragments/task/polish.md',
        )

    def test_readme_layout_names_every_manifest_routing_axis(self):
        readme = self.normalized_text('README.md').lower()
        self.assertIn(
            '`manifest.yaml` maps task, delivery, section, and model-family fragments',
            readme,
        )

    def test_abstract_omits_citations_and_invented_numbers(self):
        abstract = self.normalized_text('static/fragments/section/abstract.md').lower()
        self.assertIn('use no invented numbers', abstract)
        self.assertIn('do not include citations or reference markers', abstract)
        self.assertIn('main text and reference list', abstract)
        self.assertNotIn('cite only when necessary', abstract)

    def test_section_axis_routes_each_requested_section(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        self.assertEqual(
            manifest['axes']['section']['values'],
            {
                'abstract': 'static/fragments/section/abstract.md',
                'problem-analysis': 'static/fragments/section/problem-analysis.md',
                'assumptions-notation': 'static/fragments/section/assumptions-notation.md',
                'model-formulation': 'static/fragments/section/model-formulation.md',
                'solution-results': 'static/fragments/section/solution-results.md',
                'validation-sensitivity': 'static/fragments/section/validation-sensitivity.md',
                'model-evaluation': 'static/fragments/section/model-evaluation.md',
                'conclusion': 'static/fragments/section/conclusion.md',
                'references': 'static/fragments/section/references.md',
                'appendix': 'static/fragments/section/appendix.md',
            },
        )
        self.assertTrue(manifest['axes']['section']['multi'])
        self.assertNotIn('default', manifest['axes']['section'])

    def test_section_fragments_use_the_shared_contract_headings(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        headings = ('## Purpose', '## Required inputs', '## Structure',
                    '## Evidence boundary', '## Common failures')
        for relative_path in manifest['axes']['section']['values'].values():
            text = self.normalized_text(relative_path)
            for heading in headings:
                self.assertIn(heading, text, relative_path)

    def test_draft_paper_routes_sections_in_argument_order_and_drafts_abstract_last(self):
        text = self.normalized_text('static/fragments/task/draft-paper.md').lower()
        section_values = (
            'problem-analysis', 'assumptions-notation', 'model-formulation',
            'solution-results', 'validation-sensitivity', 'model-evaluation',
            'conclusion', 'references', 'appendix', 'abstract',
        )
        positions = [text.index(section) for section in section_values]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('abstract prose is drafted after results and validation stabilize', text)

    def test_router_does_not_use_calendar_year_as_rule_authority(self):
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('current calendar year', skill)
        self.assertRegex(skill, r'current calendar year[^.]*must not select')

    def test_always_loaded_core_supports_argument_coverage_and_terminology(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        self.assertEqual(
            manifest['always_load'],
            [
                'static/core/stance.md',
                'static/core/workflow.md',
                'static/core/output-format.md',
                'static/core/reader-contract.md',
                'static/core/terminology-notation-ledger.md',
            ],
        )

        reader_contract = self.normalized_text('static/core/reader-contract.md')
        for anchor in ('what is answered', 'why this model', 'what result',
                       'why it is credible', 'where it applies'):
            self.assertIn(anchor, reader_contract.lower())

        ledger = self.normalized_text('static/core/terminology-notation-ledger.md')
        for column in ('Canonical form', 'Definition/first use',
                       'Symbol or abbreviation', 'Unit', 'Precision',
                       'Variants/collisions', 'Decision'):
            self.assertIn(column.lower(), ledger.lower())
        for anchor in ('one concept per canonical name',
                       'one symbol per quantity within a model',
                       'definition before use', 'stable units',
                       'one numeric precision per repeated metric',
                       'genuinely ambiguous', 'dominant source form'):
            self.assertIn(anchor, ledger.lower())

        workflow = self.normalized_text('static/core/workflow.md').lower()
        for anchor in ('one-sentence argument', 'problem coverage matrix',
                       'terminology and notation ledger', 'evidence outward',
                       'abstract last', 'targeted revision',
                       'whole-paper consistency sweep'):
            self.assertIn(anchor, workflow)

        stance = self.normalized_text('static/core/stance.md').lower()
        for anchor in ('clear chinese academic prose', 'canonical technical forms',
                       'binding cumcm rules', 'non-binding editorial guidance'):
            self.assertIn(anchor, stance)

        output = self.normalized_text('static/core/output-format.md').lower()
        for anchor in ('manuscript content', 'section map',
                       'material assumptions/missing inputs', 'claim-evidence map',
                       'terminology/notation decisions', 'compact structural notes'):
            self.assertIn(anchor, output)
        self.assertIn('do not pad outputs with empty sections', output)

    def test_model_family_axis_routes_multiple_families_without_a_default(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        self.assertEqual(
            manifest['axes']['model_family']['values'],
            {
                'evaluation': 'static/fragments/model_family/evaluation.md',
                'prediction': 'static/fragments/model_family/prediction.md',
                'optimization': 'static/fragments/model_family/optimization.md',
                'mechanistic': 'static/fragments/model_family/mechanistic.md',
                'simulation': 'static/fragments/model_family/simulation.md',
                'hybrid': 'static/fragments/model_family/hybrid.md',
            },
        )
        self.assertTrue(manifest['axes']['model_family']['multi'])
        self.assertNotIn('default', manifest['axes']['model_family'])
        self.assertTrue(manifest['axes']['model_family']['detect'])

    def test_model_family_fragments_have_validation_contracts(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        headings = (
            '## Required inputs', '## Primary diagnostics', '## Validation',
            '## Sensitivity', '## Failure boundary', '## Do not claim',
        )
        required_anchors = {
            'evaluation': ('indicator direction', 'scaling', 'weight method',
                           'consistency', 'weight stability', 'ranking stability',
                           'objective-best claim', 'subjective weighting'),
            'prediction': ('target', 'split protocol', 'leakage controls', 'baseline',
                           'metric', 'train', 'validation/test', 'extrapolation',
                           'calibration', 'residual', 'forecast diagnostics',
                           'causality from prediction'),
            'optimization': ('variables/domains', 'objective', 'complete constraints',
                             'solver/stopping rule', 'feasibility', 'objective/bound checks',
                             'perturb constraints', 'global-optimum claim', 'valid certificate'),
            'mechanistic': ('governing equations', 'units', 'initial and boundary conditions',
                            'parameter sources', 'dimensional/numerical checks',
                            'parameter identifiability', 'mechanism proof from fit alone'),
            'simulation': ('state transitions/events', 'distributions', 'calibration',
                           'random seed', 'replications', 'convergence/monte carlo error',
                           'single-run conclusion', 'real-world causal claim'),
            'hybrid': ('each component', 'interface variables/units', 'calibration order',
                       'component and end-to-end checks', 'propagated uncertainty',
                       'cross-model consistency', "one component's fit", 'full pipeline'),
        }
        for family, relative_path in manifest['axes']['model_family']['values'].items():
            text = self.normalized_text(relative_path)
            self.assertEqual(
                tuple(line for line in (ROOT / relative_path).read_text(encoding='utf-8').splitlines()
                      if line.startswith('## ')),
                headings,
                relative_path,
            )
            normalized = text.lower()
            for anchor in required_anchors[family]:
                self.assertIn(anchor, normalized, f'{relative_path}: {anchor}')

    def test_router_loads_requested_model_families_once_and_expands_hybrids(self):
        skill = self.normalized_text('SKILL.md').lower()
        for anchor in ('model_family', 'one or more model families',
                       'deduplicated loading', 'hybrid',
                       'component families actually used'):
            self.assertIn(anchor, skill)
        self.assertNotIn('model_family routing arrives later', skill)

        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        routed_paths = set(manifest['axes']['model_family']['values'].values())
        self.assertTrue(routed_paths.isdisjoint(manifest['always_load']))

        model_validation = next(
            entry for entry in manifest['references']['on_demand']
            if entry['path'] == 'references/model-validation.md'
        )
        for family in ('evaluation', 'prediction', 'optimization',
                       'mechanistic', 'simulation', 'hybrid'):
            self.assertIn(family, model_validation['condition'])

    def test_shared_model_validation_reference_has_cross_family_rules(self):
        text = self.normalized_text('references/model-validation.md').lower()
        for anchor in ('define the output/estimand', 'separate calibration and validation',
                       'justified baseline', 'quantify uncertainty',
                       'material assumptions', 'failure cases',
                       'propagate uncertainty through hybrid interfaces'):
            self.assertIn(anchor, text)

    def test_on_demand_routes_load_result_consistency_and_layout_guidance(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        routes = {entry['path']: entry['condition'] for entry in manifest['references']['on_demand']}
        expected = {
            'references/main-text-discipline.md': (
                'results', 'full-paper drafting', 'compression', 'result placement',
                'repeated tables',
            ),
            'references/consistency-sweep.md': (
                'full-paper', 'multi-round consistency',
                'abstract/body/conclusion disagreement',
            ),
            'references/layout-diagnosis.md': (
                'layout/typesetting', 'table walls', 'sparse pages',
                'stranded headings', 'float', 'overflow',
            ),
        }
        for path, phrases in expected.items():
            self.assertIn(path, routes)
            condition = routes[path].lower()
            for phrase in phrases:
                self.assertIn(phrase, condition, path)


if __name__ == '__main__':
    unittest.main()
