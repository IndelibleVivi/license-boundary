#!/usr/bin/env python3
"""Validate the editable License Boundary decision architecture assets."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ZIP = ROOT / "docs/architecture/license-boundary-decision-flow.excalidraw.zip"
EN_SVG = ROOT / "docs/architecture/license-boundary-decision-flow.svg"
ZH_SVG = ROOT / "docs/architecture/license-boundary-decision-flow.zh-CN.svg"
DOC_PATH = ROOT / "docs/architecture/README.md"
SVG_ROOT_TAG = "{http://www.w3.org/2000/svg}svg"
SVG_TEXT_TAG = "{http://www.w3.org/2000/svg}text"
EXPECTED_FRAMES = {
    "README · landscape": (2100, 1180),
    "中文 · landscape": (2100, 1180),
    "XHS · portrait": (1200, 1600),
}
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read_text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required architecture file: {path.relative_to(ROOT)}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"architecture file is not valid UTF-8: {path.relative_to(ROOT)}")
        return ""


en_svg = read_text(EN_SVG)
zh_svg = read_text(ZH_SVG)
docs = read_text(DOC_PATH)

for path, svg, language, title in (
    (EN_SVG, en_svg, "en", "License Boundary Decision Architecture"),
    (ZH_SVG, zh_svg, "zh-CN", "License Boundary 决策架构"),
):
    if not svg:
        continue
    try:
        svg_root = ET.fromstring(svg)
    except ET.ParseError as exc:
        fail(f"{path.name} is not well-formed XML: {exc}")
        continue
    if svg_root.tag != SVG_ROOT_TAG:
        fail(f"{path.name} must use an SVG root element")
        continue
    if svg_root.attrib.get("viewBox") != "0 0 2100 1180":
        fail(f"{path.name} must keep the 2100×1180 landscape viewBox")
    visible_text = [
        "".join(element.itertext()) for element in svg_root.iter(SVG_TEXT_TAG)
    ]
    if not any(title in text for text in visible_text):
        fail(f"{path.name} lost its visible title")
    if f"projection-language:{language}" not in svg:
        fail(f"{path.name} is missing its projection language marker")
    if "payload-type:application/vnd.excalidraw+json" in svg:
        fail(f"{path.name} must remain a projection, not a second editable source")

scene: object | None = None
if not SOURCE_ZIP.is_file():
    fail("missing canonical Excalidraw source archive")
else:
    try:
        with zipfile.ZipFile(SOURCE_ZIP) as archive:
            names = archive.namelist()
            if names != ["license-boundary-decision-flow.excalidraw"]:
                fail(f"source archive must contain exactly one scene; found {names!r}")
            else:
                scene = json.loads(archive.read(names[0]).decode("utf-8"))
    except (zipfile.BadZipFile, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"cannot recover canonical Excalidraw scene: {exc}")

if not isinstance(scene, dict):
    fail("canonical Excalidraw scene must be a JSON object")
else:
    if scene.get("type") != "excalidraw":
        fail("canonical source is not an Excalidraw scene")
    if scene.get("appState", {}).get("theme") != "light":
        fail("canonical architecture must keep the default light theme")

    elements = scene.get("elements")
    if not isinstance(elements, list):
        fail("canonical Excalidraw scene has no element list")
    else:
        raw_frames = [
            element
            for element in elements
            if isinstance(element, dict)
            and element.get("type") == "frame"
        ]
        if len(raw_frames) != len(EXPECTED_FRAMES):
            fail(
                "canonical scene must contain exactly "
                f"{len(EXPECTED_FRAMES)} frames; found {len(raw_frames)}"
            )

        frame_names = [frame.get("name") for frame in raw_frames]
        if any(
            not isinstance(name, str) or not name.strip() for name in frame_names
        ):
            fail("every canonical frame must have a non-empty name")
        else:
            duplicate_names = sorted(
                {name for name in frame_names if frame_names.count(name) > 1}
            )
            if duplicate_names:
                fail(f"canonical scene has duplicate frame names: {duplicate_names!r}")

            frames = {
                frame["name"]: (frame.get("width"), frame.get("height"))
                for frame in raw_frames
            }
            if frames != EXPECTED_FRAMES:
                fail(
                    "canonical scene must contain the English landscape, "
                    f"Chinese landscape, and XHS frames; found {frames!r}"
                )

        texts = {
            element.get("text")
            for element in elements
            if isinstance(element, dict)
            and element.get("type") == "text"
            and isinstance(element.get("text"), str)
        }
        for required_text in (
            "License Boundary Decision Architecture",
            "License Boundary 决策架构",
            "一个 license 决定，怎样落到整个 repo？",
        ):
            if required_text not in texts:
                fail(f"canonical scene lost frame title: {required_text}")

if docs:
    for phrase in (
        "decision architecture, not runtime component architecture",
        "README · landscape",
        "中文 · landscape",
        "XHS · portrait",
        "canonical editable",
        "default light theme",
    ):
        if phrase not in docs:
            fail(f"architecture README is missing update-contract phrase: {phrase!r}")

if ERRORS:
    print("Architecture validation failed:", file=sys.stderr)
    for error in ERRORS:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("License Boundary decision architecture validation passed.")
