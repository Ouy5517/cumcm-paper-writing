from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
FAQ_PATH = "references/cumcm-practical-faq.md"


class PracticalFaqContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        path = ROOT / relative_path
        if not path.is_file():
            self.fail(f"missing required file: {relative_path}")
        return path.read_text(encoding="utf-8")

    def normalized(self, relative_path: str) -> str:
        text = self.read(relative_path).lower()
        return " ".join(text.split())

    def decision_table(self, heading: str) -> dict[str, dict[str, str]]:
        faq = self.read(FAQ_PATH)
        marker = f"## {heading}"
        self.assertIn(marker, faq)
        block = faq.split(marker, 1)[1].split("\n## ", 1)[0]
        lines = [line for line in block.splitlines() if line.startswith("|")]
        self.assertGreaterEqual(len(lines), 3, f"missing rows under {marker}")

        def cells(line: str) -> list[str]:
            return [cell.strip() for cell in line.strip().strip("|").split("|")]

        headers = [header.lower() for header in cells(lines[0])]
        rows = [dict(zip(headers, cells(line))) for line in lines[2:]]
        self.assertNotIn("", (row.get("case", "") for row in rows))
        return {row["case"]: row for row in rows}

    @staticmethod
    def mandatory_volatile_defaults(text: str) -> list[str]:
        patterns = (
            r"\b(?:must|shall|required|limited to|no more than)\b[^.?!\n]{0,60}\b(?:20|twenty)\s+pages?\b",
            r"(?:正文|论文)[^。！？\n]{0,30}(?:必须|不得超过|不超过)[^。！？\n]{0,20}(?:20|二十)\s*页",
            r"\b(?:must|shall|required|threshold is|below|under)\b[^.?!\n]{0,60}\b25\s*(?:%|percent\b)",
            r"(?:查重率|相似度)[^。！？\n]{0,30}(?:必须|不得|低于|不超过)[^。！？\n]{0,20}(?:25\s*[%％]|百分之二十五)",
            r"\b(?:must|shall|required|limited to|no more than)\b[^.?!\n]{0,60}\b20\s*(?:mb\b|megabytes?\b)",
            r"(?:支撑材料|文件)[^。！？\n]{0,30}(?:必须|不得|不超过)[^。！？\n]{0,20}20\s*(?:mb\b|兆字节)",
        )
        findings = []
        for line in text.lower().splitlines():
            if line.strip().endswith(("?", "？")):
                continue
            if any(re.search(pattern, line) for pattern in patterns):
                findings.append(line.strip())
        return findings

    @staticmethod
    def ethical_policy_violations(text: str) -> list[str]:
        patterns = {
            "recommend-similarity": (
                r"\brecommend(?:s|ed|ing)?\b[^.。!?？\n]{0,80}"
                r"\b(?:similarity|aigc)\b[^.。!?？\n]{0,80}"
                r"\b(?:evasion|bypass|evade|reduce(?:\s+the)?\s+"
                r"(?:ai\s+)?detection|规避|绕过)\b"
            ),
            "rewrite-to-bypass": (
                r"\brewrite\b[^.。!?？\n]{0,100}\bsynonyms?\b"
                r"[^.。!?？\n]{0,80}\b(?:bypass|evade)\b"
            ),
            "omit-from-disclosure": (
                r"\bomit(?:s|ted|ting)?\b[^.。!?？\n]{0,100}"
                r"\b(?:routine\s+)?ai interactions?\b[^.。!?？\n]{0,50}"
                r"\bfrom\s+(?:the\s+)?disclosure\b"
            ),
        }
        negative_prefixes = (
            "reject ", "refuse ", "do not ", "never ", "forbid ",
            "prohibit ", "不得", "不要", "拒绝", "禁止",
        )
        findings = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            lowered = line.lower()
            if lowered.startswith("|") and "| reject |" in lowered:
                continue
            prose = lowered.lstrip("-* ")
            if prose.startswith(negative_prefixes):
                continue
            for label, pattern in patterns.items():
                if re.search(pattern, lowered):
                    findings.append(f"{label}: {line}")
        return findings

    def test_practical_faq_is_on_demand_and_never_always_loaded(self) -> None:
        self.assertTrue((ROOT / FAQ_PATH).is_file())
        manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertNotIn(FAQ_PATH, manifest["always_load"])

        routes = {
            entry["path"]: entry["condition"]
            for entry in manifest["references"]["on_demand"]
        }
        self.assertIn(FAQ_PATH, routes)
        condition = routes[FAQ_PATH].lower()
        for trigger in ("preflight", "validation", "appendix", "support package", "submission"):
            self.assertIn(trigger, condition)

        skill = self.normalized("SKILL.md")
        self.assertIn(FAQ_PATH, skill)
        self.assertIn("on demand", skill)

    def test_faq_preserves_the_authority_boundary(self) -> None:
        faq = self.normalized(FAQ_PATH)
        for label in ("verified rule", "non-binding guidance", "unverified claim"):
            self.assertIn(label, faq)
        for boundary in (
            "output.md",
            "non-authoritative",
            "not instructions",
            "selected-year official notice",
            "competition package",
            "supplied template",
        ):
            self.assertIn(boundary, faq)

    def test_volatile_claims_are_selected_year_verification_questions(self) -> None:
        faq = self.read(FAQ_PATH).lower()
        heading = "## selected-year verification questions"
        self.assertIn(heading, faq)
        question_block = faq.split(heading, 1)[1].split("\n## ", 1)[0]
        questions = [line for line in question_block.splitlines() if line.startswith("- ")]
        for subject in (
            "page count",
            "similarity threshold",
            "file-size limit",
            "dates",
            "delivery forms",
            "ai-use declaration",
            "md5 or hash",
        ):
            matches = [line for line in questions if subject in line]
            self.assertEqual(len(matches), 1, subject)
            self.assertTrue(matches[0].rstrip().endswith("?"), matches[0])

        rows = self.decision_table("Volatile-claim decision table")
        expected_forms = {
            "page-count": ("20 pages", "twenty pages", "20页", "二十页"),
            "similarity-threshold": ("25%", "25 percent", "25％", "百分之二十五"),
            "file-size-limit": ("20 mb", "20mb", "20兆字节"),
        }
        for case, forms in expected_forms.items():
            self.assertEqual(rows[case]["decision"], "VERIFY_SELECTED_YEAR")
            representative_forms = rows[case]["representative forms"].lower()
            for form in forms:
                self.assertIn(form, representative_forms, f"{case}: {form}")
        self.assertEqual([], self.mandatory_volatile_defaults(faq))

    def test_volatile_default_detector_catches_mutations_but_allows_questions(self) -> None:
        mandatory_mutations = (
            "The paper must be no more than 20 pages.",
            "The paper shall be limited to twenty pages.",
            "正文不得超过20页。",
            "论文必须控制在二十页以内。",
            "The similarity threshold is below 25%.",
            "The similarity score must be under 25 percent.",
            "查重率必须低于25％。",
            "相似度不得超过百分之二十五。",
            "The support file must be no more than 20 MB.",
            "支撑材料不得超过20兆字节。",
        )
        for mutation in mandatory_mutations:
            self.assertEqual([mutation.lower()], self.mandatory_volatile_defaults(mutation))

        verification_questions = (
            "Does the selected-year notice impose a limit such as 20 pages?",
            "Does it state a 25 percent similarity threshold?",
            "所选年份通知是否规定正文不得超过二十页？",
            "所选年份材料包是否规定20 MB限制？",
        )
        for question in verification_questions:
            self.assertEqual([], self.mandatory_volatile_defaults(question))

    def test_faq_retains_only_normalized_practical_guidance(self) -> None:
        faq = self.normalized(FAQ_PATH)
        for principle in (
            "appendix",
            "support package",
            "model-family-specific validation",
            "validation near the corresponding result",
            "in-text citation",
            "three-line tables",
            "conditional editorial guidance",
        ):
            self.assertIn(principle, faq)
        self.assertIn("no ordinary artifact-hash requirement", faq)

    def test_faq_rejects_evasion_but_allows_legitimate_tool_use(self) -> None:
        raw_faq = self.read(FAQ_PATH)
        self.assertIn("Ethical stance: REJECT", raw_faq)
        self.assertEqual([], self.ethical_policy_violations(raw_faq))

        rows = self.decision_table("Advice decision table")
        rejected_examples = {
            "similarity-aigc-evasion": ("lower", "ai detection score"),
            "copied-text-disguise": ("disguise", "copied text"),
            "generated-text-synonym-rewrite": ("rewrite", "generated text", "synonyms"),
            "code-evasion": ("change code", "evade checks"),
            "disclosure-omission": ("omit", "routine ai interactions", "disclosure"),
            "weak-enforcement-exploit": ("exploit", "weak enforcement"),
            "commercial-tool-recommendation": ("named commercial", "rewriting tool", "evade checks"),
        }
        for case, anchors in rejected_examples.items():
            self.assertEqual(rows[case]["decision"], "REJECT", case)
            advice = rows[case]["representative advice"].lower()
            for anchor in anchors:
                self.assertIn(anchor, advice, f"{case}: {anchor}")

        positive = rows["verified-disclosure-scope"]
        self.assertEqual(positive["decision"], "VERIFY_SELECTED_YEAR")
        self.assertEqual(
            positive["representative advice"],
            "Only disclose AI-use records required by the verified selected-year notice.",
        )
        self.assertNotEqual(positive["decision"], "REJECT")
        self.assertEqual(rows["legitimate-tool-use"]["decision"], "ALLOW_WITH_VERIFIED_RULES")

        mutations = {
            "stance reversal": (
                raw_faq.replace("Reject similarity", "Recommend similarity", 1),
                "recommend-similarity",
            ),
            "appended prose evasion": (
                raw_faq
                + "\nTo reduce the AI detection score, rewrite generated passages "
                "using synonyms and omit routine AI interactions from the disclosure.\n",
                "omit-from-disclosure",
            ),
            "appended list evasion": (
                raw_faq
                + "\n- Rewrite generated passages using synonyms to bypass AIGC checks.\n",
                "rewrite-to-bypass",
            ),
        }
        for label, (mutated_faq, expected_violation) in mutations.items():
            with self.subTest(mutation=label):
                findings = self.ethical_policy_violations(mutated_faq)
                self.assertEqual(
                    [expected_violation],
                    [finding.split(":", 1)[0] for finding in findings],
                )
                with self.assertRaises(AssertionError):
                    self.assertEqual([], findings)

        compliant_controls = (
            "Reject similarity or AIGC evasion.",
            "Do not rewrite generated passages using synonyms to bypass AIGC checks.",
            "不得改写生成文本并使用同义词绕过 AIGC 检测。",
            "Only disclose AI-use records required by the verified selected-year notice.",
            "仅按经核验的年度规则披露 AI 使用记录。",
            "Recommend similarity checks to identify unattributed passages.",
        )
        for control in compliant_controls:
            with self.subTest(compliant_control=control):
                self.assertEqual([], self.ethical_policy_violations(control))

        faq = self.normalized(FAQ_PATH)
        for commercial_name in ("doubao", "deepseek", "chatgpt", "claude", "biling ai"):
            self.assertNotIn(commercial_name, faq)

    def test_related_references_connect_the_normalized_principles(self) -> None:
        expected = {
            "references/preflight.md": (
                "cumcm-practical-faq.md",
                "selected-year",
                "verification questions",
            ),
            "references/model-validation.md": (
                "cumcm-practical-faq.md",
                "model-family-specific",
                "near the corresponding result",
            ),
            "references/code-appendix.md": (
                "cumcm-practical-faq.md",
                "appendix",
                "support package",
            ),
        }
        for relative_path, anchors in expected.items():
            text = self.normalized(relative_path)
            for anchor in anchors:
                self.assertIn(anchor, text, f"{relative_path}: {anchor}")


if __name__ == "__main__":
    unittest.main()
