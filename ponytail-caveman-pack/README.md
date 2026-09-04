# ponytail-caveman-pack

把两个开源 Claude Code 插件移植为一个 CodeBuddy 插件包，**安装后即自动启用**：

- **ponytail** —— 懒人极简编码（YAGNI 优先，写最少代码），来自 <https://github.com/DietrichGebert/ponytail>
- **caveman** —— 穴居人极简沟通（说话更短更直），及其一族附属技能，来自 <https://github.com/JuliusBrussee/caveman>

两个技能在 `skills/` 下随取随用；对应的生命周期钩子在会话开始自动注入规则、在每轮提问后跟踪模式切换。

## 目录结构

```
ponytail-caveman-pack/
├── plugin.json / .codebuddy-plugin/plugin.json   # 插件清单
├── hooks/
│   ├── hooks.json                 # 钩子注册（3 个事件）
│   ├── codebuddy-hook.js          # 统一适配器（CodeBuddy 契约 ⇄ 上游 Claude Code 脚本）
│   ├── ponytail/                  # 上游 ponytail 钩子脚本（原样搬运）
│   └── caveman/                   # 上游 caveman 钩子脚本（原样搬运）
├── skills/                        # 技能（SKILL.md）
│   ├── ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review
│   ├── caveman, caveman-commit, caveman-compress, caveman-discover, caveman-evidence-review,
│   │   caveman-explore, caveman-help, caveman-learn, caveman-manage, caveman-optimize,
│   │   caveman-review, caveman-setup, caveman-stats, cavecrew
│   └── investigate-first, lean-build, migration, safe-refactor, surgical-patch, verify-and-stop
├── commands/                      # 斜杠命令
│   ├── ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review
│   └── caveman, caveman-commit, caveman-review, caveman-stats
└── agents/                        # cavecrew 子代理定义
    ├── cavecrew-investigator.md
    ├── cavecrew-builder.md
    └── cavecrew-reviewer.md
```

## 钩子如何工作

| 事件 | 触发 | 注入内容 |
|---|---|---|
| `SessionStart` | 每次会话开始（含 resume/clear/compact） | ponytail 规则 + caveman 规则（按各自档位） |
| `UserPromptSubmit` | 每轮提问 | 检测 `/ponytail`、`/caveman`、`/caveman-commit`、`/caveman-review`、`/caveman-stats` 及自然语言触发词，写/读模式状态，附加强化指令 |
| `SubagentStart` | 每次启动子代理 | ponytail 规则（默认对全部子代理注入，可用 `PONYTAIL_SUBAGENT_MATCHER` 限定） |

CodeBuddy 的钩子契约与上游脚本（Claude Code 原生格式）不同，因此所有注册都指向
`hooks/codebuddy-hook.js` 适配器：

- 读取 stdin 负载并归一化（`prompt` 兼容字符串 / `{content}` / `user_prompt` 三种形态）；
- 用同一 Node 运行上游脚本，注入 `CLAUDE_PLUGIN_ROOT`，并把状态目录隔离到 `~/.codebuddy`（`CLAUDE_CONFIG_DIR`，不污染 `~/.claude`）；
- 把上游的纯文本输出或 JSON 统一转成
  `{ "continue": true, "hookSpecificOutput": { "hookEventName": ..., "additionalContext": ... } }`；
- 剥离上游附带的 "STATUSLINE SETUP NEEDED" 提示块（CodeBuddy 无 Claude 状态栏，属噪音）；
- 8s 超时与 stdin 1.5s 兜底，保证钩子绝不阻塞会话。

## 用法

### ponytail（极简代码）

- 会话内激活：`/ponytail`（默认 full）、`/ponytail ultra`、`/ponytail lite`；停用：`/ponytail off`，或直接说 "stop ponytail" / "normal mode"。
- 随时可用命令与技能：`/ponytail-review`（当前改动审查）、`/ponytail-audit`（全仓库审计）、`/ponytail-debt`（把 `ponytail:` 注释收进台账）、`/ponytail-gain`（收益记分牌）、`/ponytail-help`（速查卡）。
- 默认档位 `full` 可用 `PONYTAIL_DEFAULT_MODE=off|lite|full|ultra` 环境变量或配置文件 `~/.config/ponytail/config.json`（Windows：`%APPDATA%\ponytail\config.json`，内容 `{"defaultMode":"off"}`）修改。

### caveman（极简沟通）

- 会话内激活：`/caveman`（默认 full）、`/caveman ultra`、`/caveman lite`、`/caveman wenyan-full`（文言风味）；停用：`/caveman off`，或直接说 "stop caveman" / "normal mode"。
- 自然语言触发："talk like a caveman"、"caveman mode"、"speak caveman" 等；"stop caveman mode" 停用。
- 附属能力：`/caveman-commit`（极简提交信息）、`/caveman-review`（每行一个发现的代码审查）、`/caveman-compress`（把本地改动提炼成 CLAUDE.md 风格笔记）、`/caveman-stats`（会话用量）、`/caveman-help`（速查卡）；`cavecrew` 三个子代理（investigator/builder/reviewer）专用于把输出压得更省。
- 默认档位可用 `CAVEMAN_DEFAULT_MODE` 环境变量或 caveman 配置文件（Windows：`%APPDATA%\caveman\config.json`，内容 `{"defaultMode":"off"}`）修改。

## 注意事项

- **模式状态按会话记忆**，新开会话回到默认档位；状态文件位于 `~/.codebuddy`（通过注入的 `CLAUDE_CONFIG_DIR`）。
- 云端类能力（`caveman-setup` / `caveman-manage` / `caveman-optimize` / `caveman-evidence-review` / `caveman-discover` / `caveman-learn`）依赖上游 `@caveman-ai/cli` 与 Caveman Cloud 账号，本包只搬运其技能说明。
- `caveman-stats` / `caveman-compress` 需要解析会话转录文件，转录格式与 CodeBuddy 不完全一致时可能只返回部分数据，属上游兼容性限制。
- 上游默认 **ponytail 与 caveman 都按 full 档开启**；若只想要其中一个，按上文"默认档位"方式把另一个设成 `off`，或从 `hooks/hooks.json` 删除对应条目。
- `hooks/ponytail/*-statusline.*`、`hooks/caveman/*-statusline.*` 为上游状态栏脚本，CodeBuddy 不使用，保留仅为随包完整。

## 上游与许可

- ponytail：<https://github.com/DietrichGebert/ponytail>（MIT）
- caveman：<https://github.com/JuliusBrussee/caveman>（MIT）

本包对两仓库做“搬运 + CodeBuddy 适配”，未改动其技能/脚本逻辑。
