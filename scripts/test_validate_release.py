#!/usr/bin/env python3
"""Regression tests for the repository release validator."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_release.py"


class ReleaseValidationTests(unittest.TestCase):
    def test_identically_modified_sul_copies_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            case_root = Path(temporary_directory) / "repo"
            shutil.copytree(
                ROOT,
                case_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )

            license_text = (case_root / "LICENSE").read_text(encoding="utf-8")
            modified_text = (
                license_text
                + "\nAdditional restriction: redistribution requires approval.\n"
            )
            (case_root / "LICENSE").write_text(modified_text, encoding="utf-8")
            (case_root / "skills/license-boundary/LICENSE.txt").write_text(
                modified_text,
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(case_root / "scripts" / VALIDATOR.name)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("must match the pinned canonical SUL-1.0 text", result.stderr)


if __name__ == "__main__":
    unittest.main()
