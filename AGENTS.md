# github-profile · GitHub 个人主页 README

`github.com/davidfuzju` 的 Profile README 仓——GitHub 约定：与账号同名的仓，其 `README.md`
即个人主页正文。

- **项目类型**：custom（内容仓，无构建、无 CI、无依赖）
- **工作区形态**：单仓项目（形态 A）。`~/Workspaces/tokendivers/projects/github-profile`
  是指向本仓的软链；领域文档真身若有则直接落本仓，**不做注入**
- **搜索层**：qmd collection `github-profile`（qmd 不跟软链，工作区那条 collection 覆盖不到本仓）

| 路径        | 用途     | 备注                                                                          |
| ----------- | -------- | ----------------------------------------------------------------------------- |
| `README.md` | 主页正文 | 顶部放横幅 `assets/banner.png`，单图，不分明暗主题 |
| `assets/`   | 横幅图   | `banner.png`（2400×840）+ `banner.svg`，均由 `banner.py` 生成，勿手改 |
| `banner.py` | 横幅生成器 | `python3 banner.py`，依赖 `rsvg-convert`；设计语汇见 `CONTEXT.md` |
| `CONTEXT.md` | 领域语汇 | 横幅立意、术语、呈现规格与已知的坑 |
| `docs/agents/` | agent 配置 | issue tracker / triage 标签 / 领域文档消费规则；由 `/setup-matt-pocock-skills` 生成 |

## Agent skills

### Issue tracker

GitHub Issues on `davidfuzju/davidfuzju`（`gh` CLI）。See `docs/agents/issue-tracker.md`.

### Triage labels

五个规范角色，label 字符串与角色同名（默认值）。See `docs/agents/triage-labels.md`.

### Domain docs

Single-context：根 `CONTEXT.md` + `docs/adr/`。See `docs/agents/domain.md`.
