# dev-workflow-pack

开发工作流全家桶插件包。

## 内容

| 组件 | 位置 | 说明 |
|------|------|------|
| Matt Pocock 工程技能集 | `skills/`（7 项） | grill-me、write-a-skill、improve-codebase-architecture 等 |
| OpenSpec 工作流技能 | `skills/`（13 项） | openspec-new-change / propose / apply / verify / archive 全流程 |
| UI/UX 设计技能 | `skills/ui-ux-pro-max/` | 可搜索设计知识库 |
| CodeWiki-Plus 源码 | `codewiki-plus/` | LLM Wiki 生成器 + MCP 服务器（Python ≥ 3.12） |
| OpenSpec 规范目录 | `openspec/` | CodingHub 项目的 specs / changes / schemas |
| MCP 配置 | `.mcp.json` | codewiki 服务器，相对路径 |

## CodeWiki MCP 安装步骤

`.mcp.json` 使用相对路径指向插件内的 `codewiki-plus/` 源码，首次使用需安装依赖：

```bash
cd codewiki-plus
python -m venv .venv && .venv\Scripts\activate   # Windows；macOS/Linux 用 .venv/bin/activate
pip install -e .
```

或使用 uv（项目自带 uv.lock）：`uv sync`。

依赖安装后，`.mcp.json` 中的 `python -m codewiki.mcp.server`（cwd 为 `./codewiki-plus`）即可启动。
如客户端从其他工作目录解析 `python`，可将 `.mcp.json` 中的 command 改为所建 venv 的解释器路径。
API Key 等配置参见 `codewiki-plus/README.md`。
