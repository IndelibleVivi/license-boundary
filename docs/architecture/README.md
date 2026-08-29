# License Boundary decision architecture

**English** | [简体中文](README.zh-CN.md)

This diagram describes decision architecture, not runtime component architecture.
It keeps permission goals, rights evidence, the user's final selection,
repository-wide implementation, and verification as separate boundaries.

## Files

- `license-boundary-decision-flow.excalidraw.zip` is the canonical editable
  source. The archive contains one `license-boundary-decision-flow.excalidraw`
  scene with three source frames:
  - `README · landscape` — the English 2100×1180 repository projection;
  - `中文 · landscape` — the Chinese 2100×1180 landscape projection; and
  - `XHS · portrait` — the Chinese 1200×1600 social projection.
- `license-boundary-decision-flow.svg` is the English README projection.
- `license-boundary-decision-flow.zh-CN.svg` is the Chinese landscape
  projection.

## Update contract

1. Extract and import the `.excalidraw` scene from the source archive.
2. Edit the source frames rather than redrawing a second representation.
3. Export `README · landscape` to `license-boundary-decision-flow.svg`.
4. Export `中文 · landscape` to
   `license-boundary-decision-flow.zh-CN.svg`.
5. Export `XHS · portrait` as a 1200×1600 PNG when a social projection is
   needed; the PNG is a release artifact, not a second source of truth.
6. Keep the default light theme, aligned grid, orthogonal connectors, and
   semantic structure consistent across all three frames.

## Text alternative

Permission goals and rights evidence converge on a license-and-scope
recommendation. The user explicitly confirms the final choice. The confirmed
terms then land across `LICENSE`, `LICENSING`, `NOTICE`, `README`, package
metadata, contribution terms, and license history before the exact diff, links,
notices, history boundary, and affected checks are verified. Unresolved
ownership, derivation, patent, or custom-license questions stop for
professional review instead of being guessed through.
