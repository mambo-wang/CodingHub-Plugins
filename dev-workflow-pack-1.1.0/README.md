# dev-workflow-pack

开发工作流全家桶插件包。

## 内容

| 组件 | 位置 | 说明 |
|------|------|------|
| Matt Pocock 工程技能集 | `skills/`（7 项） | grill-me、write-a-skill、improve-codebase-architecture 等 |
| OpenSpec 工作流技能 | `skills/`（13 项） | openspec-new-change / propose / apply / verify / archive 全流程 |
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
