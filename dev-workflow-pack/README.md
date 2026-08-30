# dev-workflow-pack

开发工作流全家桶插件包。

## 内容

| 组件 | 位置 | 说明 |
|------|------|------|
| Matt Pocock 工程技能集 | `skills/`（25 项） | grill-me、tdd、code-review、codebase-design、to-spec/to-tickets、wayfinder 等（上游 mattpocock/skills v1.2.3 官方插件全集） |
| Superpowers 核心技能库 | `skills/`（14 项） | test-driven-development、systematic-debugging、writing-plans/executing-plans、requesting/receiving-code-review、using-git-worktrees 等（上游 obra/superpowers v6.3.0） |
| OpenSpec 工作流技能 | `skills/`（14 项） | openspec-new-change / propose / apply / verify / archive / update-change 全流程（12 项来自 OpenSpec v1.11.0）+ openspec-write-plan / executing-plans（来自 dyx/openspec-superpowers v1.0.1） |
| OpenSpec OPSX 命令 | `commands/opsx/`（11 项） | `/opsx:propose` / `new` / `continue` / `explore` / `apply` / `update` / `verify` / `sync` / `archive` / `write-plan` / `executing-plans`，与上述技能同源的斜杠命令入口（OpenSpec CLI CodeBuddy 适配器生成，含 `/init-openspec` 共 12 个命令） |
| UI/UX 设计技能 | `skills/ui-ux-pro-max/` | 可搜索设计知识库 |
| CodingHub 平台操作技能 | `skills/codinghub/` | 工具广场/插件市场/论坛/知识库操作，MCP 优先 + chub CLI（Python/Node 双实现）降级 |
| 蒸馏代理 | `agents/distill-worker.md` | CodeWiki 补蒸馏 subagent（配合 codewiki MCP） |
| 会话钩子 | `hooks/` | SessionStart 任务关联提示 + SessionEnd 对话捕获（`hooks.json` 随插件启用自动合并） |
| CodeWiki 约定模板 | `references/codewiki-agents-template.md` | 项目接入 CodeWiki 时可复制进 AGENTS.md 的约定段 |
| OpenSpec 规范目录 | `openspec/` | CodingHub 项目的 specs / changes / schemas |
| MCP 配置 | `.mcp.json` | codewiki 服务器（需自行安装，见下） |

## CodeWiki MCP 安装步骤

本插件**不含** CodeWiki-Plus 源码。`.mcp.json` 声明的 `codewiki` 服务器需要你先自行安装 [CodeWiki-Plus](https://github.com/mambo-wang/CodeWiki-Plus)，并保证插件启用时 `python` 能导入 `codewiki` 包：

```bash
pip install codewiki-plus          # 或克隆源码后 pip install -e . / uv sync
```

若客户端解析的 `python` 不是安装了 codewiki 的解释器，把 `.mcp.json` 中的 `command` 改为对应 venv 解释器路径。未安装时 codewiki 服务器启动会失败，但不影响插件其余组件（技能/命令/代理）使用。API Key 等配置参见 CodeWiki-Plus 的 README。

## 在新项目初始化 repowiki

本插件的会话钩子、蒸馏代理与知识工作流都依赖**项目根目录**下的 `repowiki/`。该目录不随插件分发（插件安装目录也不被这些组件读取），而是用 CodeWiki MCP 工具在项目内就地初始化——`schema.yaml`、`ontology.yaml`、`review_checklist.yaml` 都是 CodeWiki 内置模板，初始化时自动落盘，无需手工拷贝。

**单仓项目**——在项目根目录执行一次：

```
init_wiki()          # 默认 repo_path=当前目录，output_dir=<项目>/repowiki
```

自动创建 `repowiki/` 骨架（`wiki/modules/`、`wiki/entities/`、`notes/` 等），落盘三份模板，并在项目 `AGENTS.md` 的标记块之间注入 CodeWiki 使用约定。幂等，可安全重跑。

**多仓产品线（harness 工作台）**——在 harness 主仓目录执行一次，首次必须指定知识布局：

```
init_workspace(layout="colocated")    # 或 "centralized"
```

- `colocated`：每个业务仓各自保留 `repowiki/`（两跳检索）
- `centralized`：全部知识集中在工作区级 `repowiki/`（一跳检索，CodeWiki-Plus-Harness 采用的布局）

会生成 `bootstrap.sh` / `bootstrap.ps1` 克隆脚本、`.gitignore`、`repo-map.md` 导航页与工作区约定；之后用 `add_workspace_repo(url=<克隆URL>)` 登记新业务仓。

> `init_wiki` 注入的约定与 `references/codewiki-agents-template.md` 内容对应——正常情况无需手工拷贝模板，它留作参考或无法自动注入时的备用。
>
> 项目有了 `repowiki/` 之后，本插件随附的会话钩子即自动生效（见下节）。

## 更新记录（2026-08-30）

技能库对齐上游最新版：

- **OpenSpec**（Fission-AI/OpenSpec v1.11.0）：11 个 openspec-* 技能由 CLI 1.4.1 生成版整体更新，新增 `openspec-update-change`。
- **Superpowers**（obra/superpowers v6.3.0）：新引入全部 14 个核心技能（TDD、systematic-debugging、writing-plans / executing-plans、requesting / receiving-code-review、subagent-driven-development、using-git-worktrees 等）。
- **Matt Pocock 技能集**（mattpocock/skills v1.2.3）：按官方插件清单纯化——移除上游已删除的 design-an-interface（并入 codebase-design）、write-a-skill（由 writing-for-agents 取代）、research-ts-decisions（由 research 取代）、document-ai-hero-api，全量同步官方 25 个技能。
- **openspec-superpowers**（dyx/openspec-superpowers v1.0.1）：与包内版本一致，无变化。

## 在新项目初始化 openspec

插件随包分发了 `openspec/` 规范目录（`config.yaml`、`specs/`、`schemas/`、`changes/`）。CodeBuddy 的插件组件（技能/命令）都是从插件安装目录直接加载的，**没有**"安装后自动把文件放进项目根目录"的内建机制——`openspec/` 需要在目标项目中显式初始化，方式任选：

- **命令**：会话中运行 `/init-openspec`（agent 会调用 `scripts/init_openspec.py` 完成复制）。
- **脚本**：手动执行 `python "<插件目录>/scripts/init_openspec.py"`，默认复制到当前项目根目录。

行为：

- **幂等**：目标项目已有 `openspec/` 时直接跳过，不覆盖任何文件；需合并覆盖同名文件时加 `--force`。
- **会话提示**：`hooks/init_openspec_hint.py`（SessionStart）检测到项目缺 `openspec/` 时，会提示 agent 询问用户是否初始化——只提示、不自动复制，且仅对 git 仓库生效。
- **注意**：`openspec/config.yaml` 含来源项目（CodingHub）的技术栈信息与配置，初始化到新项目后请按实际修改；如含敏感凭据，发布插件前应清理。

> 与 repowiki 一样，`openspec/` 也遵循"按需初始化"：不强制、不打扰未使用 OpenSpec 工作流的项目。

## codinghub skill 首次配置

技能目录内只带 `config.json.example`。首次使用时复制为 `config.json` 并填写你的 CodingHub 实例地址与账号：

```bash
cp skills/codinghub/config.json.example skills/codinghub/config.json
```

> `config.json` 含凭据，不要提交到 git。

## CodeWiki 团队记忆钩子说明

- `hooks/task_session_start.py`：会话开始时注入「任务关联」流程（选择/新建任务、拉取任务上下文、补蒸馏委托）。
- `hooks/capture_session_end.py`：会话结束时后台捕获对话到 `repowiki/raw/`（fire-and-forget，不阻塞 IDE）。
- 两个钩子都只在**存在 `repowiki/` 目录的项目**中生效；未接入 CodeWiki 的项目静默跳过，不受打扰。
- 钩子依赖 `codewiki` 包可导入（同上安装）。项目接入 CodeWiki 的完整约定（采纳声明、知识沉淀、任务记忆）见 `references/codewiki-agents-template.md`。
