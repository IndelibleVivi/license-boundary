# License Boundary Repository Contract

This repository is the canonical public source for the `license-boundary`
Codex skill. Edit the skill only under `skills/license-boundary/`; downstream
packaging copies are version-pinned projections, not parallel source.

Keep the skill low-friction for users with different levels of licensing
knowledge. Preserve one plain-language best-fit recommendation, no more than
one or two material alternatives, and explicit user selection of the final
license and scope. Do not silently turn source-available terms into “open
source,” infer ownership from repository control, or invent license text.

When changing licensing claims in this repository, follow `LICENSING.md` and
update every affected public surface consistently. Preserve contributor and
third-party rights, stage exact paths, inspect the staged diff, and validate
`skills/license-boundary/` before committing.

Do not publish or update a downstream Softpowers projection from this
repository unless that separate repository action is explicitly in scope.
