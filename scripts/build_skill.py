#!/usr/bin/env python3
"""Build a reproducible, self-contained skill ZIP using only the standard library."""

import argparse
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "SKILL.md", "README.md", "README.zh-TW.md", "LICENSE",
    "CONTRIBUTING.md", "SECURITY.md", "requirements.txt",
    "agents/openai.yaml", "scripts/validate_spec.py", "scripts/render_diagram.py", "tests/test_validate_spec.py",
)
SKILLS = ("elicit-mesh", "em-brainstorm", "em-diagram", "em-review")


def source_files() -> list[Path]:
    files = [ROOT / name for name in FILES]
    for directory in ("references", "examples"):
        files.extend(p for p in (ROOT / directory).rglob("*")
                     if p.is_file() and p.suffix in (".md", ".yaml"))
    return sorted(files)


def skill_files(name):
    files = {p.relative_to(ROOT): p for p in source_files()}
    if name != "elicit-mesh":
        for relative in ("SKILL.md", "agents/openai.yaml"):
            files[Path(relative)] = ROOT / "skills" / name / relative
    return sorted(files.items())


def build_codex(destination: Path) -> None:
    """Materialize the same four standalone skills for both plugin hosts."""
    for name in SKILLS:
        for relative, path in skill_files(name):
            target = destination / name / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)


def build(destination: Path, skill="elicit-mesh") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for relative, path in skill_files(skill):
            name = skill + "/" + relative.as_posix()
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "skill.zip")
    args = parser.parse_args()
    build(args.output)
    for skill in SKILLS[1:]:
        build(args.output.parent / f"{skill}.zip", skill)
    build_codex(ROOT / "dist" / "skills")
    print(f"Built {args.output}")
