"""Exercise the uploaded artifact independently of the repository layout."""

import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_skill import build
from validate_spec import validate_project


class DistributionTests(unittest.TestCase):
    def test_download_matches_source_and_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "first.zip", Path(tmp) / "second.zip"
            build(first)
            build(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first.read_bytes(), (ROOT / "dist/skill.zip").read_bytes(),
                             "Run python scripts/build_skill.py to refresh the download")

    def test_packaged_examples_validate_without_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            with ZipFile(ROOT / "dist/skill.zip") as archive:
                self.assertIsNone(archive.testzip())
                archive.extractall(destination)
                names = archive.namelist()
                self.assertTrue(all(n.startswith("elicit-mesh/") for n in names))
                self.assertFalse(any("__pycache__" in n or "/.git" in n for n in names))
            skill = destination / "elicit-mesh"
            for file in ("SKILL.md", "README.md", "README.zh-TW.md", "LICENSE",
                         "references/schema.md", "scripts/validate_spec.py"):
                self.assertTrue((skill / file).is_file(), file)
            for example in ("legal-unfair-dismissal", "construction-scope"):
                self.assertEqual(validate_project(skill / "examples" / example), [])
