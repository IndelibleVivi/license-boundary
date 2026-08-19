#!/usr/bin/env python3
"""Validate License Boundary's repository and distributed Skill contract."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def compact(text: str) -> str:
    """Collapse formatting whitespace while preserving words and Markdown."""
    return " ".join(text.split())


def require_file(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing required file: {relative}")
    return path


def read(relative: str) -> str:
    path = require_file(relative)
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"file is not valid UTF-8: {relative}")
        return ""


REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "LICENSE-DOCUMENTATION.md",
    "LICENSING.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "AGENTS.md",
    "VERSION",
    "skills/license-boundary/SKILL.md",
    "skills/license-boundary/LICENSE.txt",
    "skills/license-boundary/NOTICE.md",
    "skills/license-boundary/agents/openai.yaml",
    ".github/workflows/validate.yml",
    "scripts/test_validate_architecture.py",
)

for required in REQUIRED_FILES:
    require_file(required)

workflow = read(".github/workflows/validate.yml")
for command in (
    "python3 scripts/validate_release.py",
    "python3 scripts/validate_architecture.py",
    "python3 scripts/test_validate_architecture.py",
):
    if command not in workflow:
        fail(f"validation workflow does not run required command: {command}")

version = read("VERSION").strip()
if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
    fail(f"VERSION is not a supported semantic version: {version!r}")

readme = read("README.md")
readme_compact = compact(readme)
for expected in (
    f"at v{version}.",
    f"--ref v{version}",
):
    if expected not in readme:
        fail(f"README.md is not pinned to VERSION: missing {expected!r}")

if "they do not\ndetermine the license of repositories analyzed or changed" not in readme:
    fail("README.md must state that License Boundary does not license target repositories")

if "Third-party redistribution remains governed by SUL-1.0" in readme_compact:
    fail("README.md must not apply SUL-1.0 to all repository redistribution")
for scoped_claim in (
    "Third-party redistribution of SUL-covered functional materials remains governed by SUL-1.0",
    "Documentation and other separately mapped paths remain governed by the licenses identified in [LICENSING.md](LICENSING.md).",
):
    if scoped_claim not in readme_compact:
        fail(f"README.md lost layered redistribution scope: {scoped_claim}")

root_license = require_file("LICENSE")
packaged_license = require_file("skills/license-boundary/LICENSE.txt")
if root_license.is_file() and packaged_license.is_file():
    if root_license.read_bytes() != packaged_license.read_bytes():
        fail("LICENSE and skills/license-boundary/LICENSE.txt differ")

license_text = read("LICENSE")
if not license_text.startswith("# Sustainable Use License\n\nVersion 1.0\n"):
    fail("LICENSE must begin with the unmodified SUL-1.0 heading and version")
if "Repository Licensing Notice" in license_text:
    fail("repository-specific scope notices belong in NOTICE.md or LICENSING.md")

skill_text = read("skills/license-boundary/SKILL.md")
frontmatter_match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
if not frontmatter_match:
    fail("SKILL.md has invalid YAML frontmatter boundaries")
else:
    frontmatter = frontmatter_match.group(1)
    name_match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.MULTILINE)
    description_match = re.search(
        r'^description:\s*"([^"]+)"\s*$', frontmatter, re.MULTILINE
    )
    if not name_match or name_match.group(1) != "license-boundary":
        fail("SKILL.md frontmatter name must be license-boundary")
    if not description_match:
        fail("SKILL.md frontmatter must contain one quoted description")
    else:
        description = description_match.group(1)
        if len(description) > 1024:
            fail("SKILL.md description exceeds 1024 characters")
        for trigger in (
            "LICENSE file",
            "open source",
            "commercial use",
            "fork/derivative",
            "contributor rights",
            "forward-only relicensing",
        ):
            if trigger not in description:
                fail(f"SKILL.md description lost trigger phrase: {trigger}")

if len(skill_text.splitlines()) >= 500:
    fail("SKILL.md must remain under 500 lines")
if len(skill_text.split()) >= 5000:
    fail("SKILL.md must remain under 5000 words")

for guardrail in (
    "Do not describe this as OSI open source.",
    "Repository ownership and a\nshort contributor list do not prove copyright ownership.",
    "Stop for professional review when",
    "A licensing recommendation or file edit does not authorize a commit",
):
    if guardrail not in skill_text:
        fail(f"SKILL.md lost critical guardrail: {guardrail!r}")

agent_yaml = read("skills/license-boundary/agents/openai.yaml")


def quoted_yaml_value(key: str) -> str | None:
    match = re.search(
        rf'^\s*{re.escape(key)}:\s*"([^"]*)"\s*$',
        agent_yaml,
        re.MULTILINE,
    )
    return match.group(1) if match else None


if quoted_yaml_value("display_name") != "License Boundary":
    fail("agents/openai.yaml display_name is stale")
short_description = quoted_yaml_value("short_description")
if short_description is None or not 25 <= len(short_description) <= 64:
    fail("agents/openai.yaml short_description must be 25-64 characters")
default_prompt = quoted_yaml_value("default_prompt")
if default_prompt is None or "$license-boundary" not in default_prompt:
    fail("agents/openai.yaml default_prompt must mention $license-boundary")
elif len(default_prompt) > 320:
    fail("agents/openai.yaml default_prompt is too long")
if re.search(r"^\s*products:\s*$", agent_yaml, re.MULTILINE):
    fail("agents/openai.yaml contains the stale products policy field")

root_notice = read("NOTICE.md")
root_notice_compact = compact(root_notice)
package_notice = read("skills/license-boundary/NOTICE.md")
for relative, notice in (
    ("NOTICE.md", root_notice),
    ("skills/license-boundary/NOTICE.md", package_notice),
):
    for required_notice in (
        "Copyright (c) 2026 Faye (@IndelibleVivi)",
        "Created by Faye & Cove.",
        "https://github.com/IndelibleVivi/license-boundary",
    ):
        if required_notice not in notice:
            fail(f"{relative} is missing required attribution: {required_notice}")

if "Modified distributions must preserve required notices" in root_notice_compact:
    fail("NOTICE.md must not apply SUL-1.0 modification duties to all paths")
for scoped_notice in (
    "For SUL-covered functional materials, redistribution must preserve the required notices",
    "Documentation and other separately mapped paths remain governed by the licenses identified in `LICENSING.md`.",
):
    if scoped_notice not in root_notice_compact:
        fail(f"NOTICE.md lost layered redistribution scope: {scoped_notice}")

if "`LICENSE.txt`" not in package_notice:
    fail("distributed NOTICE.md must point to LICENSE.txt")
if "does not determine the license of repositories" not in package_notice:
    fail("distributed NOTICE.md must separate Skill and target-repository licensing")

licensing = read("LICENSING.md")
for mapped_path in (
    "`scripts/`",
    "root `NOTICE.md`",
    "`skills/license-boundary/SKILL.md`",
    "`README.md`",
    "project-original files under `docs/`",
):
    if mapped_path not in licensing:
        fail(f"LICENSING.md does not map {mapped_path}")
if "They do not determine the license of repositories analyzed or edited" not in licensing:
    fail("LICENSING.md must separate Skill and target-repository licensing")

contributing = read("CONTRIBUTING.md")
for contribution_guardrail in (
    "No copyright assignment or contributor",
    "inbound-equals-outbound",
    "Third-party redistribution remains subject to the applicable public license.",
):
    if contribution_guardrail not in contributing:
        fail(f"CONTRIBUTING.md lost guardrail: {contribution_guardrail}")

stale_phrases = (
    "only distribution authority",
    "standalone-only distribution ownership",
    "downstream Softpowers projection",
)
for relative in ("README.md", "CONTRIBUTING.md", "AGENTS.md", "CHANGELOG.md"):
    text = read(relative)
    for phrase in stale_phrases:
        if phrase in text:
            fail(f"{relative} contains stale distribution wording: {phrase!r}")

for relative in (
    "README.md",
    "LICENSING.md",
    "CONTRIBUTING.md",
    "LICENSE-DOCUMENTATION.md",
):
    text = read(relative)
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local_target = unquote(target.split("#", 1)[0])
        if local_target and not (ROOT / local_target).exists():
            fail(f"{relative} has a broken local link: {target}")

changelog = read("CHANGELOG.md")
if f"## {version} — " not in changelog:
    fail("CHANGELOG.md has no heading for VERSION")

if ERRORS:
    print("License Boundary validation failed:", file=sys.stderr)
    for error in ERRORS:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"License Boundary {version} validation passed.")
