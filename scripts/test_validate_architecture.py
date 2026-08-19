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

    def test_comment_only_projection_title_is_rejected(self) -> None:
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
                '<svg xmlns="http://www.w3.org/2000/svg" '
                'viewBox="0 0 2100 1180">'
                "<!-- License Boundary Decision Architecture -->"
                "<!-- projection-language:en -->"
                "</svg>",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("lost its visible title", result.stderr)

    def test_title_hidden_by_ancestor_is_rejected(self) -> None:
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
                '<svg xmlns="http://www.w3.org/2000/svg" '
                'viewBox="0 0 2100 1180">'
                "<!-- projection-language:en -->"
                '<g display="none"><text>'
                "License Boundary Decision Architecture"
                "</text></g>"
                "</svg>",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("lost its visible title", result.stderr)

    def test_title_under_transparent_ancestor_is_rejected(self) -> None:
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
                '<svg xmlns="http://www.w3.org/2000/svg" '
                'viewBox="0 0 2100 1180">'
                "<!-- projection-language:en -->"
                '<g style="opacity: 0"><text>'
                "License Boundary Decision Architecture"
                "</text></g>"
                "</svg>",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("lost its visible title", result.stderr)

    def test_title_only_projection_is_rejected(self) -> None:
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
                '<svg xmlns="http://www.w3.org/2000/svg" '
                'viewBox="0 0 2100 1180">'
                "<!-- projection-language:en -->"
                "<text>License Boundary Decision Architecture</text>"
                "</svg>",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("lost representative semantic label", result.stderr)

    def test_frame_and_title_only_canonical_scene_is_rejected(self) -> None:
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

            frame_titles = {
                "License Boundary Decision Architecture",
                "License Boundary 决策架构",
                "一个 license 决定，怎样落到整个 repo？",
            }
            scene["elements"] = [
                element
                for element in scene["elements"]
                if element.get("type") == "frame"
                or (
                    element.get("type") == "text"
                    and element.get("text") in frame_titles
                )
            ]

            with zipfile.ZipFile(
                source_zip, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                archive.writestr(
                    SOURCE_NAME,
                    json.dumps(scene, ensure_ascii=False, separators=(",", ":")),
                )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("source frame lost representative semantic label", result.stderr)

    def test_deleted_canonical_frame_titles_are_rejected(self) -> None:
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

            frame_titles = {
                "License Boundary Decision Architecture",
                "License Boundary 决策架构",
                "一个 license 决定，怎样落到整个 repo？",
            }
            for element in scene["elements"]:
                if (
                    element.get("type") == "text"
                    and element.get("text") in frame_titles
                ):
                    element["isDeleted"] = True

            with zipfile.ZipFile(
                source_zip, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                archive.writestr(
                    SOURCE_NAME,
                    json.dumps(scene, ensure_ascii=False, separators=(",", ":")),
                )

            result = subprocess.run(
                [sys.executable, str(case_scripts / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("source frame lost its active title", result.stderr)


if __name__ == "__main__":
    unittest.main()
