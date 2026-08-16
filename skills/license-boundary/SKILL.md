---
name: license-boundary
description: "Choose, audit, add, or change licensing for a concrete repository from wanted permissions and available rights. Trigger for a LICENSE file, which license, open source versus source-available or no license, commercial use, resale or paid hosting, code versus docs/assets, forks, third-party or contributor rights, or forward-only relicensing. Do not trigger for routine publish, push, release, or deploy work without a licensing decision, or abstract legal questions unrelated to a concrete project."
---

# License Boundary

Start from the permissions the project actually needs, then map those needs to
current ownership and repository paths. Treat this as repository licensing
hygiene, not individualized legal advice.

## Start with the user's real goal

Distinguish these outcomes before naming a license:

- **OSI open source:** anyone may use the software commercially and may sell
  copies. Reciprocity can require source sharing, but cannot prohibit commerce.
- **Source-available / use-restricted:** source is visible and selected uses are
  granted, but commercial provision, distribution, competition, or another use
  may be restricted. Do not describe this as OSI open source.
- **No public grant:** default copyright applies. A public code host may still
  allow viewing and forking under its platform terms; visibility is not a
  general permission to use, modify, or redistribute.
- **Layered publication:** code, documentation, diagrams, data, trademarks,
  examples, and third-party material may require different terms.

Ask only for a choice that changes the answer and cannot be recovered from the
request or project. Common decisive questions are whether commercial use,
internal business use, paid distribution or hosted provision, modification,
redistribution, and reciprocal source sharing should be permitted.

## Make the user's choice easy

Do not require license vocabulary from the user. State the practical outcome
first: who may use the material internally, sell copies, charge for hosting,
modify or redistribute it, and which notice, source-sharing, adaptation, or
ShareAlike conditions follow.

Lead with one best-fit recommendation and a short reason. Offer at most one or
two materially different alternatives, and only when their tradeoff could
plausibly change the choice. If the user already names an exact license and
scope, verify that it fits instead of reteaching the whole decision tree.

Choose by governed material, not by the repository label. A repository whose
main public artifact is a guide, publication, diagram set, or other authored
content may need a content license even when it also contains scripts; map
functional code separately when necessary.

The user retains the final licensing choice. Before adding or changing public
license terms, obtain explicit selection of the exact license or licenses and
their scope unless the current request already supplies that selection. A
request to help choose or recommend authorizes a recommendation, not silent
finalization. Once the choice and file-edit authority are clear, implement it
without another approval ritual.

## Establish the rights boundary

Inspect the current target branch and relevant history before editing. Classify
each affected path as:

- project-original material controlled by the person offering the license;
- a contribution whose author retained copyright;
- upstream or derivative material governed by an existing license;
- vendored, copied, generated, or data material whose provenance or governing
  terms differ from the project default; or
- private or unpublished material outside the intended grant.

Check existing `LICENSE*`, `LICENSING*`, notices, AUTHORS/acknowledgements,
package metadata, release tags, and source history. Repository ownership and a
short contributor list do not prove copyright ownership. Do not state that
upstream material itself changed license merely because its license is
permissive. Preserve the upstream license text, required notices, attribution,
and continuing permissions for upstream material. A permissive license may
allow modifications or a derivative work as a whole to be distributed under
additional or different terms; apply those terms only to rights the relevant
licensor can grant and only as the upstream license permits. Use a path or
provenance map when the boundary would otherwise be unclear.

Stop and report the unresolved boundary when required consent is missing,
derivation is unclear, or a normal repository audit cannot establish who can
license the material.

Stop for professional review when the result turns on disputed or undocumented
ownership or assignment, employment or work-for-hire terms, whether combined
software is a derivative work for copyleft purposes, a commercially material
interpretation of NonCommercial or internal-use language, patent exposure, or
a negotiated exception or custom license.

## Match a standard license to the goal

Use current official terms; never invent restrictions from a summary. An SPDX
identifier establishes a standard identifier and text, not OSI approval.

- MIT and Apache-2.0 are permissive OSI licenses and allow commercial use and
  sale. Apache-2.0 adds an express contributor patent grant and patent-
  termination terms and, on redistribution, requires changed-file notices and
  preservation of applicable `NOTICE` material.
- GPL and AGPL are OSI-approved copyleft license families, not noncommercial
  licenses; commercial use, sale, and paid hosting remain permitted. Select an
  exact version and SPDX expression, including the `-only` versus `-or-later`
  choice. For AGPL-3.0, do not imply that every network use triggers source
  disclosure: section 13 applies when the Program is modified and the modified
  version supports remote network interaction, requiring an offer of
  Corresponding Source to those remote users.
- SUL-1.0 is source-available: it permits personal, noncommercial, and internal
  business use, while distribution or provision to others must be free of
  charge and noncommercial.
- PolyForm-Noncommercial-1.0.0 permits use, modification, and distribution only
  for its defined permitted purposes. It does not contain SUL-1.0's general
  internal-business-use permission; read the complete permitted-purpose
  language instead of treating it as a synonym for “no resale.”
- Creative Commons does not recommend CC licenses for software, but a current
  CC license can fit copyrightable documentation and separate media. Choose the
  specific license from the user's goals concerning attribution, commercial
  use, adaptations, NoDerivatives, and ShareAlike; do not default to CC
  BY-NC-SA. Under CC, NonCommercial is a defined, purpose-based standard, and
  ShareAlike applies when Adapted Material is shared. Clearly exclude code,
  trademarks, and third-party material outside the CC grant.
- No license is a deliberate option when no public reuse grant is intended.

Prefer a recognized license over a custom clause. If no standard option matches
the desired commercial boundary, describe the mismatch and recommend counsel
rather than fabricating legal text.

When the choice depends on license scope, check current primary sources:

- OSI Open Source Definition and FAQ for open-source/commercial-use claims;
- SPDX `SUL-1.0` for the Sustainable Use License text;
- PolyForm's official license text for its permitted purposes;
- Creative Commons FAQ and canonical legal code for CC scope; and
- GitHub's repository-licensing documentation for no-license and host-platform
  behavior.

## Apply the smallest complete repository change

Use one license for a homogeneous project. For mixed surfaces, add only the
artifacts needed to make the map unambiguous, commonly:

- `LICENSE` containing the governing software license text;
- `LICENSE-DOCUMENTATION.md` linking to the canonical documentation terms;
- `LICENSING.md` mapping current repository paths;
- `LICENSE-HISTORY.md` recording a forward-only transition; and
- `THIRD_PARTY_NOTICES.md` when incorporated material requires it.

Update README language, badges, package metadata, contribution terms, and
release notes only when they are affected. For layered packages, use the
package ecosystem's supported SPDX expression or license-file mechanism.
If no accurate machine-readable value exists, keep the path map authoritative
and avoid assigning a misleading single identifier to contents that do not
share one license.

Name each rights holder only for material they control. Do not imply copyright
assignment or sole-licensor authority merely because someone maintains the
repository. Preserve authorship credit separately from legal licensing claims.
An inbound=outbound rule does not transfer copyright. It grants only the rights
supplied by the applicable license and contribution process. Determine
separately whether those rights include sublicensing or distribution under
additional terms. Do not infer ownership, exclusive rights, or authority to
offer a proprietary or commercial exception beyond the inbound grant or any
separate contributor agreement.

## Preserve earlier grants

When earlier revisions were publicly distributed or repository history already
contains a different license, preserve those earlier terms and record the cutoff
precisely enough to avoid ambiguity, normally by identifying the last prior-
license commit. Do not claim that previously distributed copies lost their
earlier permissions, and do not create a tag, release, or history rewrite solely
to manufacture a boundary.

A licensing recommendation or file edit does not authorize a commit, push, PR,
merge, release, deployment, commercial exception, public reply, or account
change. Follow the task's actual Git and publication authority.

## Verify proportionately

- Inspect the exact diff and staged paths; exclude private material and
  unrelated changes.
- Check that legal text or official links, path maps, metadata, notices, and
  version/history boundaries agree.
- Check relative links and run `git diff --cached --check` when committing.
- Run only the narrow code or packaging checks affected by the licensing edit.
- If separate Git or publication actions are authorized, report exactly which
  actions were performed. Do not add deployment or runtime verification to a
  licensing-only task.
