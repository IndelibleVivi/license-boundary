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
SVG_RECT_TAG = "{http://www.w3.org/2000/svg}rect"
SVG_PATH_TAG = "{http://www.w3.org/2000/svg}path"
MINIMUM_PROJECTION_NODES = 6
MINIMUM_PROJECTION_CONNECTORS = 6
EXPECTED_PROJECTION_LABELS = {
    "en": (
        "PERMISSION GOALS",
        "RIGHTS EVIDENCE",
        "LICENSE + SCOPE",
        "REPOSITORY LANDING",
        "VERIFY",
        "AUTHORITY UNRESOLVED",
    ),
    "zh-CN": (
        "权限目标",
        "权利证据",
        "许可 + 范围",
        "仓库级落地",
        "验证",
        "授权边界未确认",
    ),
}
MINIMUM_SOURCE_NODES = 6
MINIMUM_SOURCE_CONNECTORS = 6
EXPECTED_SOURCE_LABELS = {
    "README · landscape": EXPECTED_PROJECTION_LABELS["en"],
    "中文 · landscape": EXPECTED_PROJECTION_LABELS["zh-CN"],
    "XHS · portrait": (
        "权限目标",
        "权利证据",
        "LICENSE + SCOPE",
        "整个 REPO 一起落地",
        "验证",
        "无法确认授权边界",
    ),
}
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


def is_render_hidden(
    element: ET.Element, parents: dict[ET.Element, ET.Element]
) -> bool:
    current: ET.Element | None = element
    while current is not None:
        display = current.attrib.get("display", "").strip().lower()
        visibility = current.attrib.get("visibility", "").strip().lower()
        opacity = current.attrib.get("opacity", "").strip().lower()
        for declaration in current.attrib.get("style", "").split(";"):
            property_name, separator, value = declaration.partition(":")
            if not separator:
                continue
            property_name = property_name.strip().lower()
            value = value.split("!", 1)[0].strip().lower()
            if property_name == "display":
                display = value
            elif property_name == "visibility":
                visibility = value
            elif property_name == "opacity":
                opacity = value
        if display == "none" or visibility in {"hidden", "collapse"}:
            return True
        try:
            if opacity and float(opacity.removesuffix("%")) <= 0:
                return True
        except ValueError:
            pass
        current = parents.get(current)
    return False


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
    parents = {child: parent for parent in svg_root.iter() for child in parent}
    visible_text = [
        "".join(element.itertext())
        for element in svg_root.iter(SVG_TEXT_TAG)
        if not is_render_hidden(element, parents)
    ]
    if not any(title in text for text in visible_text):
        fail(f"{path.name} lost its visible title")
    for label in EXPECTED_PROJECTION_LABELS[language]:
        if not any(label in text for text in visible_text):
            fail(f"{path.name} lost representative semantic label: {label!r}")
    visible_nodes = sum(
        1
        for element in svg_root.iter(SVG_RECT_TAG)
        if not is_render_hidden(element, parents)
    )
    if visible_nodes < MINIMUM_PROJECTION_NODES:
        fail(
            f"{path.name} must keep at least {MINIMUM_PROJECTION_NODES} "
            f"visible diagram nodes; found {visible_nodes}"
        )
    visible_connectors = sum(
        1
        for element in svg_root.iter(SVG_PATH_TAG)
        if element.attrib.get("marker-end")
        and not is_render_hidden(element, parents)
    )
    if visible_connectors < MINIMUM_PROJECTION_CONNECTORS:
        fail(
            f"{path.name} must keep at least {MINIMUM_PROJECTION_CONNECTORS} "
            f"visible diagram connectors; found {visible_connectors}"
        )
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
            if not duplicate_names and frames == EXPECTED_FRAMES:
                frame_ids = {frame["name"]: frame.get("id") for frame in raw_frames}
                for frame_name, required_labels in EXPECTED_SOURCE_LABELS.items():
                    frame_elements = [
                        element
                        for element in elements
                        if isinstance(element, dict)
                        and element.get("frameId") == frame_ids[frame_name]
                        and not element.get("isDeleted")
                    ]
                    frame_texts = [
                        element.get("text")
                        for element in frame_elements
                        if element.get("type") == "text"
                        and isinstance(element.get("text"), str)
                    ]
                    for label in required_labels:
                        if not any(label in text for text in frame_texts):
                            fail(
                                f"source frame lost representative semantic label "
                                f"{label!r}: {frame_name}"
                            )
                    source_nodes = sum(
                        element.get("type") == "rectangle"
                        for element in frame_elements
                    )
                    if source_nodes < MINIMUM_SOURCE_NODES:
                        fail(
                            f"source frame must keep at least {MINIMUM_SOURCE_NODES} "
                            f"decision nodes: {frame_name}; found {source_nodes}"
                        )
                    source_connectors = sum(
                        element.get("type") == "arrow"
                        for element in frame_elements
                    )
                    if source_connectors < MINIMUM_SOURCE_CONNECTORS:
                        fail(
                            f"source frame must keep at least "
                            f"{MINIMUM_SOURCE_CONNECTORS} connectors: {frame_name}; "
                            f"found {source_connectors}"
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
