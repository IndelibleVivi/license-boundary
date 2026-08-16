# Contributing

Contributions should keep License Boundary small, concrete, and useful to
people with very different levels of licensing knowledge.

## Canonical source

Edit the skill only in `skills/license-boundary/`. Copies distributed through
Softpowers or another package are downstream projections and must not become a
second authoring authority.

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
