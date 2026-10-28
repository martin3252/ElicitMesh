#!/usr/bin/env python3
"""Build a reproducible, self-contained skill ZIP using only the standard library."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "SKILL.md", "README.md", "README.zh-TW.md", "LICENSE",
    "CONTRIBUTING.md", "SECURITY.md", "requirements.txt",
    "agents/openai.yaml", "scripts/validate_spec.py", "tests/test_validate_spec.py",
)


def build(destination: Path) -> None:
    files = [ROOT / name for name in FILES]
    for directory in ("references", "examples"):
        files.extend(p for p in (ROOT / directory).rglob("*") if p.is_file())
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(files):
            name = "elicit-mesh/" + path.relative_to(ROOT).as_posix()
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
    print(f"Built {args.output}")
