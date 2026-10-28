"""Exercise the uploaded artifact independently of the repository layout."""

import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_skill import build, build_codex, SKILLS
import yaml
from validate_spec import validate_project


class DistributionTests(unittest.TestCase):
    def test_codex_bundle_matches_the_portable_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            build_codex(destination)
            generated = {p.relative_to(destination).as_posix(): p.read_bytes()
                         for p in destination.rglob("*") if p.is_file()}
            committed = ROOT / "dist/skills"
            self.assertEqual(generated, {p.relative_to(committed).as_posix(): p.read_bytes()
                                         for p in committed.rglob("*") if p.is_file()})
            for name in SKILLS:
                filename = "skill.zip" if name == "elicit-mesh" else f"{name}.zip"
                with ZipFile(ROOT / "dist" / filename) as archive:
                    self.assertEqual({n: data for n, data in generated.items() if n.startswith(name + "/")},
                                     {n: archive.read(n) for n in archive.namelist()})

    def test_all_stage_packages_are_self_contained(self):
        for name in SKILLS:
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as tmp:
                skill = ROOT / "dist/skills" / name
                frontmatter = yaml.safe_load((skill / "SKILL.md").read_text().split("---")[1])
                self.assertEqual(frontmatter["name"], name)
                self.assertTrue((skill / "agents/openai.yaml").is_file())
                self.assertTrue((skill / "scripts/render_diagram.py").is_file())
                self.assertFalse(any(skill.rglob("sample-output.md")))
                self.assertFalse(any(skill.rglob("quality-rules.yaml")))
                self.assertEqual({p.name for p in (skill / "examples").iterdir() if p.is_dir()},
                                 {"legal-unfair-dismissal"})
                self.assertEqual(validate_project(skill / "examples/legal-unfair-dismissal"), [])

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
            self.assertEqual(validate_project(skill / "examples/legal-unfair-dismissal"), [])
