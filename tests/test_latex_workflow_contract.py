from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LatexWorkflowContractTests(unittest.TestCase):
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
        for required in ("pdfinfo", "pdftoppm", "anonym", "support", "sha256"):
            self.assertIn(required, workflow)


if __name__ == "__main__":
    unittest.main()
