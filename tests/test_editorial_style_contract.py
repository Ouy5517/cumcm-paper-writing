from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EditorialStyleContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        text = (ROOT / relative_path).read_text(encoding="utf-8").lower()
        return " ".join(text.split())

    def test_skill_rejects_four_table_montages(self) -> None:
        skill = self.read("SKILL.md")
        self.assertIn("four independent tables", skill)
        self.assertIn("2-by-2", skill)

    def test_paper_structure_limits_table_walls_and_requires_interpretation(self) -> None:
        structure = self.read("references/paper-structure.md")
        self.assertIn("no more than two tables consecutively", structure)
        self.assertIn("interpretation", structure)

    def test_layout_guidance_uses_figures_for_trends(self) -> None:
        template = self.read("references/cumcmthesis-template.md")
        self.assertIn("trend or comparison", template)
        self.assertIn("exact values", template)

    def test_bold_emphasis_is_selective_and_short(self) -> None:
        structure = self.read("references/paper-structure.md")
        for phrase in (
            "key conclusions",
            "core objectives or constraints",
            "whole paragraphs",
            "every table takeaway",
        ):
            self.assertIn(phrase, structure)

    def test_production_references_do_not_require_artifact_hashes(self) -> None:
        for relative_path in (
            "references/artifact-consistency.md",
            "references/code-appendix.md",
            "references/latex-production-workflow.md",
        ):
            with self.subTest(relative_path=relative_path):
                text = self.read(relative_path)
                self.assertNotIn("sha256", text)
                self.assertNotIn("source hash", text)
                self.assertNotIn("final pdf hash", text)

    def test_source_authority_hash_is_optional(self) -> None:
        provenance = self.read("references/year-selection.md")
        self.assertIn("a file hash is optional", provenance)
        self.assertNotIn("supplied filename and sha256", provenance)

    def test_main_text_discipline_preserves_conclusion_changing_evidence(self) -> None:
        discipline = self.read("references/main-text-discipline.md")
        for phrase in (
            "core answer",
            "necessary support",
            "qualification",
            "robustness",
            "intermediate table",
            "implementation detail",
            "main text",
            "caption",
            "appendix",
            "support material",
            "contradictory or conclusion-changing evidence",
            "replace, compress, or delete",
        ):
            self.assertIn(phrase, discipline)

    def test_consistency_sweep_counts_before_editing_and_checks_all_claim_axes(self) -> None:
        sweep = self.read("references/consistency-sweep.md")
        self.assertLess(sweep.index("count variants"), sweep.index("inspect context"))
        for phrase in (
            "abstract/body/conclusion numbers",
            "terminology",
            "notation",
            "units",
            "numeric precision",
            "equation/figure/table/reference cross-references",
            "model and metric names",
            "claims against their tables/figures",
            "do not auto-correct ambiguous variants",
        ):
            self.assertIn(phrase, sweep)
        self.assertIn("repeat until no new material inconsistency", sweep)
        self.assertLess(
            sweep.index("repeat until no new material inconsistency"),
            sweep.index("rebuild dependent artifacts"),
        )

    def test_layout_diagnosis_follows_render_first_workflow_and_template_specific_remedies(self) -> None:
        layout = self.read("references/layout-diagnosis.md")
        ordered_steps = (
            "compile",
            "read log",
            "render every page",
            "create a contact sheet",
            "inspect affected pages",
            "diagnose",
            "smallest source change",
            "rebuild and iterate",
        )
        positions = [layout.index(step) for step in ordered_steps]
        self.assertEqual(positions, sorted(positions))
        for phrase in (
            "remedies depend on the supplied cumcm template and the observed failure",
            "do not use a fixed float recipe",
            "do not prescribe universal numeric layout limits",
            "overfull/underfull content",
            "undefined references",
            "formula glyphs",
            "table walls",
            "sparse pages",
            "stranded headings",
            "caption splits",
            "float backlog",
            "unreadable tables",
            "appendix code wrapping",
        ):
            self.assertIn(phrase, layout)
        # A percentage in a real table or figure is legitimate; only a fixed
        # float-placement percentage is prohibited here.
        self.assertNotRegex(
            layout,
            r"(?:topfraction|bottomfraction|textfraction|float placement)[^.!?]{0,60}\d{1,3}%",
        )


if __name__ == "__main__":
    unittest.main()
