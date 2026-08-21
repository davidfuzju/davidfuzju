# github-profile · GitHub 个人主页 README

`github.com/davidfuzju` 的 Profile README 仓——GitHub 约定：与账号同名的仓，其 `README.md`
即个人主页正文。

- **项目类型**：custom（内容仓，无构建、无 CI、无依赖）
- **工作区形态**：单仓项目（形态 A）。`~/Workspaces/tokendivers/projects/github-profile`
  是指向本仓的软链；领域文档真身若有则直接落本仓，**不做注入**
- **搜索层**：qmd collection `github-profile`（qmd 不跟软链，工作区那条 collection 覆盖不到本仓）

| 路径        | 用途     | 备注                                                                          |
| ----------- | -------- | ----------------------------------------------------------------------------- |
| `README.md` | 主页正文 | 顶部横幅位以 HTML 注释整段停用；启用前需先放好 `assets/banner-{light,dark}.png` |
| `assets/`   | 横幅图   | 设计宽 1200px，实图按 2x 导出 2400px；light / dark 两版由 `<picture>` 切换      |
| `docs/agents/` | agent 配置 | issue tracker / triage 标签 / 领域文档消费规则；由 `/setup-matt-pocock-skills` 生成 |

## Agent skills

### Issue tracker

GitHub Issues on `davidfuzju/davidfuzju`（`gh` CLI）。See `docs/agents/issue-tracker.md`.

### Triage labels

五个规范角色，label 字符串与角色同名（默认值）。See `docs/agents/triage-labels.md`.

### Domain docs

Single-context：根 `CONTEXT.md` + `docs/adr/`。See `docs/agents/domain.md`.
