# License Boundary Repository Contract

This repository is the canonical public source and official release channel
for the `license-boundary` Codex skill. Edit the skill only under
`skills/license-boundary/`. Faye-maintained companion repositories may
recommend a tested release, but do not carry or update a same-named copy.

Keep the skill low-friction for users with different levels of licensing
knowledge. Preserve one plain-language best-fit recommendation, no more than
one or two material alternatives, and explicit user selection of the final
license and scope. Do not silently turn source-available terms into “open
source,” infer ownership from repository control, or invent license text.

When changing licensing claims in this repository, follow `LICENSING.md` and
update every affected public surface consistently. Preserve contributor and
third-party rights, stage exact paths, and inspect the staged diff. Before
committing, run `python3 scripts/validate_release.py`,
`python3 scripts/test_validate_release.py`,
`python3 scripts/validate_architecture.py`, and
`python3 scripts/test_validate_architecture.py`. Run the system
`quick_validate.py` against `skills/license-boundary/` when it is available.

Do not publish or update files in another repository unless that separate
repository action is explicitly in scope. Do not merge, tag, release, or
deploy unless the task explicitly authorizes that action.
