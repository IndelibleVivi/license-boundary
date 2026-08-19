#!/usr/bin/env python3
"""Regression tests for the architecture asset validator."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_architecture.py"
ARCHITECTURE_DIR = ROOT / "docs/architecture"
SOURCE_NAME = "license-boundary-decision-flow.excalidraw"


class ArchitectureFrameValidationTests(unittest.TestCase):
    def run_with_extra_frame(
        self, *, name: str | None
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            case_root = Path(temporary_directory)
            case_scripts = case_root / "scripts"
            case_scripts.mkdir()
            shutil.copy2(VALIDATOR, case_scripts / VALIDATOR.name)
            shutil.copytree(ARCHITECTURE_DIR, case_root / "docs/architecture")

            source_zip = (
                case_root
                / "docs/architecture/license-boundary-decision-flow.excalidraw.zip"
            )
            with zipfile.ZipFile(source_zip) as archive:
                scene = json.loads(archive.read(SOURCE_NAME))

            source_frame = next(
                element
                for element in scene["elements"]
                if element.get("type") == "frame"
                and element.get("name") == "README · landscape"
            )
            extra_frame = dict(source_frame)
            extra_frame["id"] = "regression-extra-frame"
            if name is None:
                extra_frame.pop("name", None)
            else:
                extra_frame["name"] = name
            scene["elements"].append(extra_frame)

            with zipfile.ZipFile(
                source_zip, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                archive.writestr(
                    SOURCE_NAME,
                    json.dumps(scene, ensure_ascii=False, separators=(",", ":")),
                )

            return subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_duplicate_fourth_frame_is_rejected(self) -> None:
        result = self.run_with_extra_frame(name="README · landscape")

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("duplicate frame names", result.stderr)

    def test_unnamed_fourth_frame_is_rejected(self) -> None:
        result = self.run_with_extra_frame(name=None)

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("non-empty name", result.stderr)

    def test_truncated_svg_projection_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            case_root = Path(temporary_directory)
            case_scripts = case_root / "scripts"
            case_scripts.mkdir()
            shutil.copy2(VALIDATOR, case_scripts / VALIDATOR.name)
            shutil.copytree(ARCHITECTURE_DIR, case_root / "docs/architecture")

            projection = (
                case_root
                / "docs/architecture/license-boundary-decision-flow.svg"
            )
            svg = projection.read_text(encoding="utf-8")
            title_start = svg.index("License Boundary Decision Architecture")
            title_end = svg.index("</text>", title_start) + len("</text>")
            projection.write_text(svg[:title_end], encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("not well-formed XML", result.stderr)

    def test_non_svg_xml_projection_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            case_root = Path(temporary_directory)
            case_scripts = case_root / "scripts"
            case_scripts.mkdir()
            shutil.copy2(VALIDATOR, case_scripts / VALIDATOR.name)
            shutil.copytree(ARCHITECTURE_DIR, case_root / "docs/architecture")

            projection = (
                case_root
                / "docs/architecture/license-boundary-decision-flow.svg"
            )
            projection.write_text(
                '<not-svg viewBox="0 0 2100 1180">'
                "License Boundary Decision Architecture "
                "projection-language:en"
                "</not-svg>",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("must use an SVG root element", result.stderr)


if __name__ == "__main__":
    unittest.main()
