import json
import os
import re
import sys
import unittest
from pathlib import Path


PLUGIN = Path(os.environ.get("AUTODEV_PLUGIN_ROOT", Path(__file__).resolve().parents[1] / "tkapin-autodev"))
sys.path.insert(0, str(PLUGIN / "skills" / "autodev" / "scripts"))

from autodev_core import COMMANDS, Engine, model_allowed  # noqa: E402


class PackagingTests(unittest.TestCase):
    def test_manifest_uses_one_compatible_source_of_agents(self):
        manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "tkapin-autodev")
        self.assertEqual(manifest["version"], "0.1.1")
        self.assertNotIn("$schema", manifest)
        self.assertTrue((PLUGIN / manifest["agents"]).is_dir())
        self.assertTrue((PLUGIN / manifest["skills"] / "autodev" / "SKILL.md").is_file())
        agency = json.loads((PLUGIN / "agency.json").read_text(encoding="utf-8"))
        self.assertEqual(agency["engines"], ["copilot"])

    def test_role_agents_pin_permitted_models_and_lf_line_endings(self):
        expected = {"autodev", "business-analyst", "architect", "project-manager",
                    "developer", "reviewer", "tester", "auditor"}
        files = list((PLUGIN / "agents").glob("*.agent.md"))
        self.assertEqual({path.name.removesuffix(".agent.md") for path in files}, expected)
        for path in files:
            with self.subTest(agent=path.name):
                data = path.read_bytes()
                self.assertNotIn(b"\r", data)
                content = data.decode("utf-8")
                self.assertTrue(content.startswith("---\n"))
                model = re.search(r"^model: (.+)$", content, re.MULTILINE).group(1)
                self.assertTrue(model_allowed(model))
                self.assertRegex(content, r"(?m)^description: .+")

    def test_skill_and_guide_ship_with_the_helper(self):
        skill = PLUGIN / "skills" / "autodev"
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(content, r"(?m)^name: autodev$")
        for relative in ["scripts/autodev.py", "scripts/autodev_core.py", "references/operating-guide.md"]:
            self.assertTrue((skill / relative).is_file())
        self.assertNotIn("allowed-tools:", content)

    def test_every_advertised_mutation_has_an_implementation(self):
        for action in COMMANDS:
            if action != "init":
                self.assertTrue(callable(getattr(Engine, "do_" + action.replace("-", "_"), None)), action)


if __name__ == "__main__":
    unittest.main()
