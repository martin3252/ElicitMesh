"""ElicitMesh validator regression tests; no external case facts are used."""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_spec import validate_project  # noqa: E402


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
        self.mutate(folder, "quality-rules.yaml", lambda doc: doc["rules"][0].update({"approval_status": "approved"}))
        errors = validate_project(folder)
        self.assertTrue(any("approved requires approved_by" in x for x in errors))

    def test_pending_review_cannot_support_approved_rule(self):
        folder = self.example()
        self.mutate(folder, "quality-rules.yaml", lambda doc: doc["rules"][0].update({
            "originating_feedback": "review-001",
            "approval_status": "approved",
            "approved_by": "named_lawyer",
            "approved_at": "2026-10-28",
        }))
        errors = validate_project(folder)
        self.assertTrue(any("completed review" in x for x in errors))

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
