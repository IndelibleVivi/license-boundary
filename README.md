# License Boundary

License Boundary is a small Codex skill for choosing, auditing, adding, or
changing a repository license without making the user learn license vocabulary
first.

It starts from practical outcomes—who may use the project internally, sell
copies, charge for hosting, modify it, or redistribute it—then checks what the
current rights holder can actually license. It leads with one best-fit
recommendation, offers only materially different alternatives, and leaves the
exact license and scope to the user.

Created by Faye & Cove.

## Install

Ask Codex:

```text
Use $skill-installer to install skills/license-boundary from
IndelibleVivi/license-boundary at v0.1.0-rc2.
```

Or use the system installer directly:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo IndelibleVivi/license-boundary \
  --path skills/license-boundary \
  --ref v0.1.0-rc2
```

The installed skill is available to Codex on the next turn. The installer
refuses to overwrite an existing skill directory.

The distributed skill folder includes the complete SUL-1.0 terms in
`LICENSE.txt` and the project notice in `NOTICE.md`; recipients do not need the
repository root to receive the terms governing the functional package.

## What it helps with

- choosing between permissive open source, copyleft, source-available, layered
  licensing, or no public grant;
- explaining commercial use, resale, hosted provision, modification,
  redistribution, attribution, and source-sharing consequences in plain
  language;
- separating code, documentation, diagrams, data, trademarks, and third-party
  material when one repository-wide license would be misleading;
- checking upstream, derivative, contributor, and ownership boundaries before
  making a rights claim;
- applying the selected terms consistently across license files, path maps,
  README language, package metadata, contribution terms, and notices; and
- preserving earlier public grants during a forward-only license change.

The skill may clarify a boundary that changes the answer, but it should not
turn a straightforward choice into a questionnaire. The user confirms the
final license and scope before public legal terms are written.

## Example requests

```text
Which license fits if people may modify this tool but may not sell it or offer
it as a paid hosted service?
```

```text
Audit this repository before I replace MIT. Keep earlier MIT copies valid and
tell me whether contributors or upstream code limit what I can relicense.
```

```text
License the software under Apache-2.0 and the handbook and diagrams under
CC BY-SA 4.0. Update every affected repository surface after I confirm.
```

## Boundaries

License Boundary supports repository licensing hygiene; it is not
individualized legal advice. It stops for professional review when a result
depends on disputed ownership, employment or assignment terms, a difficult
copyleft derivative-work question, commercially material interpretation of
NonCommercial language, patent exposure, or a negotiated exception.

The standalone repository is the canonical source for the skill. Softpowers
may distribute an exact, version-pinned projection, but does not become a
second authoring authority.

## Licensing

This is a source-available / fair-code distribution, not OSI open source.
Project-original functional materials in `skills/license-boundary/` are
licensed under SUL-1.0. Project-original README and other documentation are
licensed under CC BY-NC-SA 4.0. SUL-1.0 permits internal business use, but
distributing or providing the covered functional materials to others for a fee
or for commercial purposes is outside the public license; required notices
must remain visible.

See [LICENSING.md](LICENSING.md) for the authoritative path map,
[LICENSE](LICENSE) for the SUL-1.0 terms, and
[LICENSE-DOCUMENTATION.md](LICENSE-DOCUMENTATION.md) for the documentation
license.
