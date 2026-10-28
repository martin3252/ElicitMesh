"""ElicitMesh validator regression tests; no external case facts are used."""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_spec import validate_project  # noqa: E402
from render_diagram import render_project


class ValidationTests(unittest.TestCase):
    def example(self, name="legal-unfair-dismissal"):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        destination = Path(self.tmp.name)
        source = ROOT / "examples" / name
        for file in source.iterdir():
            if file.is_file():
                (destination / file.name).write_bytes(file.read_bytes())
        return destination

    def mutate(self, directory, filename, callback):
        path = directory / filename
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        callback(data)
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def test_legal_example_is_structurally_valid(self):
        self.assertEqual(validate_project(self.example()), [])

    def test_construction_example_is_structurally_valid(self):
        self.assertEqual(validate_project(self.example("construction-scope")), [])

    def test_approval_without_reviewer_fails(self):
        folder = self.example()
        self.mutate(folder, "workflow.yaml", lambda doc: doc["nodes"][0].update({"approval_status": "approved"}))
        errors = validate_project(folder)
        self.assertTrue(any("approved requires approved_by" in x for x in errors))

    def test_completed_review_needs_identified_reviewer(self):
        folder = self.example()
        self.mutate(folder, "review-log.yaml", lambda doc: doc["reviews"][0].update({"status": "completed"}))
        errors = validate_project(folder)
        self.assertTrue(any("completed review requires reviewer_identity" in x for x in errors))

    def test_empty_node_io_fails(self):
        for direction in ("inputs", "outputs"):
            with self.subTest(direction=direction):
                folder = self.example()
                self.mutate(folder, "io-contract.yaml", lambda doc: doc["contracts"][0].update({direction: []}))
                self.assertTrue(any(f"{direction} must be a nonempty list" in x for x in validate_project(folder)))

    def test_contract_change_requires_diagram_update(self):
        folder = self.example()
        self.mutate(folder, "io-contract.yaml", lambda doc: doc["contracts"][0]["inputs"][0].update({"name": "new_field"}))
        self.assertTrue(any("diagram is stale" in x for x in validate_project(folder)))
        (folder / "workflow.md").write_text(render_project(folder), encoding="utf-8")
        self.assertEqual(validate_project(folder), [])

    def test_every_node_shows_owner_and_io_and_branch_conditions(self):
        folder = self.example()
        diagram = render_project(folder)
        wf = yaml.safe_load((folder / "workflow.yaml").read_text())
        io = yaml.safe_load((folder / "io-contract.yaml").read_text())
        self.assertEqual(diagram.count("Owner:"), len(wf["nodes"]))
        self.assertEqual(diagram.count("Inputs:"), len(wf["nodes"]))
        self.assertEqual(diagram.count("Outputs:"), len(wf["nodes"]))
        for contract in io["contracts"]:
            for entry in contract["inputs"] + contract["outputs"]:
                self.assertIn(entry["name"], diagram)
        for edge in wf["edges"]:
            self.assertIn(edge["condition"], diagram)

    def test_renderer_escapes_untrusted_mermaid_labels(self):
        folder = self.example()
        self.mutate(folder, "workflow.yaml", lambda doc: doc["nodes"][0].update({"title": '檢查 "資料" <script> | end'}))
        diagram = render_project(folder)
        self.assertIn('檢查 &quot;資料&quot; &lt;script&gt; &#124; end', diagram)
        self.assertNotIn('<script>', diagram)

    def test_source_supported_needs_source_ref(self):
        folder = self.example()
        self.mutate(folder, "workflow.yaml", lambda doc: doc["nodes"][0].update({"evidence_status": "source_supported"}))
        errors = validate_project(folder)
        self.assertTrue(any("source_supported must include source_refs" in x for x in errors))

    def test_unknown_role_fails(self):
        folder = self.example()
        self.mutate(folder, "workflow.yaml", lambda doc: doc["nodes"][0].update({"owner_role": "unknown_role"}))
        errors = validate_project(folder)
        self.assertTrue(any("owner_role must refer" in x for x in errors))

    def test_orphan_contract_fails(self):
        folder = self.example()
        self.mutate(folder, "io-contract.yaml", lambda doc: doc["contracts"].pop())
        errors = validate_project(folder)
        self.assertTrue(any("has no I/O contract" in x for x in errors))


if __name__ == "__main__":
    unittest.main()
