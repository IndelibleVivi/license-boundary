# Contributing

Contributions should keep License Boundary small, concrete, and useful to
people with very different levels of licensing knowledge.

## Canonical source

Official releases are authored from `skills/license-boundary/` in this
repository. Faye-maintained companion projects should point to a tested release
rather than carry a same-named copy or act as an update channel.

Third-party redistribution remains subject to the applicable public license.
Redistributed copies must preserve notices required by that license. Copies
that modify covered material must identify those changes. The project
recognizes only tagged releases from the official repository as official
License Boundary releases.

Preserve these product boundaries:

- start from practical permissions rather than requiring license vocabulary;
- lead with one best-fit recommendation and at most one or two material
  alternatives;
- keep the user's final choice explicit;
- separate desired policy from rights the project can actually grant;
- distinguish OSI open source from source-available terms accurately; and
- stop at real ownership, derivative-work, patent, or negotiated-license
  uncertainty instead of inventing legal conclusions.

## Validation

Run the repository and architecture validators and their regression tests:

```bash
python3 scripts/validate_release.py
python3 scripts/test_validate_release.py
python3 scripts/validate_architecture.py
python3 scripts/test_validate_architecture.py
```

Run the system skill validator when it is available:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/license-boundary
```

Also inspect the exact diff, check relative links, and run `git diff --check`.
Changes to the skill must keep `agents/openai.yaml` aligned with `SKILL.md`.

## Contribution licensing

You retain copyright in your contribution. By submitting it, you agree to
license it under the license that applies to the target file in
[LICENSING.md](LICENSING.md): SUL-1.0 for functional materials and
CC BY-NC-SA 4.0 for documentation. No copyright assignment or contributor
license agreement is required.

This inbound-equals-outbound policy does not give the maintainer ownership of
your contribution or independent authority to offer it under commercial or
proprietary terms. Submit only material you have the right to contribute, and
identify any third-party or upstream material and its governing terms.
