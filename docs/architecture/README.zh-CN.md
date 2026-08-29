# License Boundary 决策架构

[English](README.md) | **简体中文**

这张图描述的是 decision architecture，而不是 runtime component architecture。
它把许可目标、权利证据、用户最终选择、repo-wide implementation 与 verification
保留为彼此独立的边界。

## 文件

- `license-boundary-decision-flow.excalidraw.zip` 是 canonical editable
  source。Archive 内含一个 `license-boundary-decision-flow.excalidraw`
  scene，以及三个 source frames：
  - `README · landscape`：用于 repository README 的 English
    2100×1180 projection；
  - `中文 · landscape`：中文 2100×1180 landscape projection；以及
  - `XHS · portrait`：中文 1200×1600 social projection。
- `license-boundary-decision-flow.svg` 是 English README projection。
- `license-boundary-decision-flow.zh-CN.svg` 是中文 landscape
  projection。

## 更新约定

1. 从 source archive 解压并导入 `.excalidraw` scene。
2. 编辑 source frames，不要另画一份平行 representation。
3. 将 `README · landscape` 导出为
   `license-boundary-decision-flow.svg`。
4. 将 `中文 · landscape` 导出为
   `license-boundary-decision-flow.zh-CN.svg`。
5. 需要 social projection 时，将 `XHS · portrait` 导出为
   1200×1600 PNG；PNG 是 release artifact，不是第二份 source of truth。
6. 三个 frames 都保持 default light theme、aligned grid、orthogonal
   connectors 与一致的 semantic structure。

## 文字替代

许可目标与权利证据汇合为 license-and-scope recommendation，由用户明确确认
最终选择。确认后的条款再落到 `LICENSE`、`LICENSING`、
`NOTICE`、`README`、package metadata、contribution terms 与
license history，随后核对 exact diff、links、notices、history boundary 与
受影响的 checks。若 ownership、derivation、patent 或 custom-license 问题仍未
解决，就停下来寻求 professional review，而不是猜一个答案。
