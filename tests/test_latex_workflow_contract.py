from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LatexWorkflowContractTests(unittest.TestCase):
    def test_cumcmthesis_and_three_line_table_rules_require_supplied_template(self) -> None:
        template = (ROOT / "references" / "cumcmthesis-template.md").read_text(
            encoding="utf-8"
        ).lower()
        normalized = " ".join(template.split())
        self.assertIn(
            "apply the following only when the supplied template contains the corresponding behavior",
            normalized,
        )
        self.assertIn("they are not automatic cumcm requirements", normalized)
        self.assertRegex(
            normalized,
            r"when (?:required by the supplied template|the supplied template uses)"
            r"[^.]*three-line table",
        )

    def test_latex_year_style_and_limits_require_selected_year_verification(self) -> None:
        workflow = (ROOT / "references" / "latex-production-workflow.md").read_text(
            encoding="utf-8"
        ).lower()
        normalized = " ".join(workflow.split())
        self.assertNotIn("current-year size limits", normalized)
        for phrase in (
            "selected-year verified size limits",
            "inspected supplied template actually uses `cumcm2026`",
            "otherwise select the template's supplied year style or omit the year style",
        ):
            self.assertIn(phrase, normalized)

    def test_manifest_routes_rendering_to_latex_workflow(self) -> None:
        manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("references/latex-production-workflow.md", manifest)
        self.assertTrue((ROOT / "references" / "latex-production-workflow.md").is_file())

    def test_workflow_preserves_real_math_and_uses_cumcmthesis(self) -> None:
        workflow = (ROOT / "references" / "latex-production-workflow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(r"\documentclass[withoutpreface,bwprint]{cumcmthesis}", workflow)
        self.assertIn(r"n_{bk}=\sum_i", workflow)
        self.assertIn(r"\frac{n_{bk}}{N_b^+}", workflow)
        self.assertNotIn("n_(bk)", workflow)
        self.assertRegex(workflow.lower(), r"xelatex.*(twice|two passes|两次)")

    def test_workflow_requires_rendered_pdf_and_package_verification(self) -> None:
        workflow = (ROOT / "references" / "latex-production-workflow.md").read_text(
            encoding="utf-8"
        ).lower()
        workflow = " ".join(workflow.split())
        for required in ("pdfinfo", "pdftoppm", "anonym", "support"):
            self.assertIn(required, workflow)

        for required_policy in (
            "reproduction commands",
            "fresh compilation",
            "every-page visual review",
            "anonymity inspection",
            "archive inspection",
            "cross-file consistency checks",
        ):
            self.assertIn(required_policy, workflow)


if __name__ == "__main__":
    unittest.main()
