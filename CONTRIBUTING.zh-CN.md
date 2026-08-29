# 参与贡献

[English](CONTRIBUTING.md) | **简体中文**

贡献应当让 License Boundary 始终保持小而具体，并对 licensing 基础不同的人都
真正有用。

## Canonical source

Official releases 从本 repository 的 `skills/license-boundary/` 制作。
Faye 维护的 companion projects 应指向经过测试的 release，而不是携带同名副本，
也不作为它的 update channel。

第三方再分发仍须遵守相应的 public license。再分发的副本必须保留该 license
要求的 notices；修改过受保护 material 的副本必须标明修改。项目只把 official
repository 的 tagged releases 认作 official License Boundary releases。

请保留这些 product boundaries：

- 从实际许可目标出发，不要求用户先掌握 license 词汇；
- 先给一个 best-fit recommendation，只提供一到两个有实质差异的备选；
- 让用户明确作出最终选择；
- 把希望实行的 policy 与项目实际能够授予的权利分开；
- 准确区分 OSI open source 与 source-available terms；以及
- 遇到真实的 ownership、derivative-work、patent 或 negotiated-license
  不确定性时停下来，不编造法律结论。

## 验证

运行 repository 和 architecture validators 及其 regression tests：

```bash
python3 scripts/validate_release.py
python3 scripts/test_validate_release.py
python3 scripts/validate_architecture.py
python3 scripts/test_validate_architecture.py
```

如果 system skill validator 可用，也运行：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/license-boundary
```

另外还要检查 exact diff 与 relative links，并运行 `git diff --check`。
如果修改了 skill，必须保持 `agents/openai.yaml` 与 `SKILL.md` 一致。

## Contribution licensing

你保留自己 contribution 的 copyright。提交 contribution 即表示你同意按照
[`LICENSING.md`](LICENSING.md) 中适用于目标文件的 license 授权：
functional materials 使用 SUL-1.0，documentation 使用 CC BY-NC-SA 4.0。
不要求 copyright assignment 或 contributor license agreement。

这项 inbound-equals-outbound policy 不会把 contribution 的 ownership 转给
maintainer，也不会让 maintainer 自动取得以 commercial 或 proprietary terms
另行授权的独立权力。请只提交你有权贡献的 material，并标明所有 third-party
或 upstream material 及其 governing terms。

本页是 contribution guide 的中文版本，不翻译或替代 governing legal terms。
如果表述出现冲突，以 [`LICENSING.md`](LICENSING.md) 和其中指向的 legal
texts 为准。
