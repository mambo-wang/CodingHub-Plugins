---
name: caveman-stats
description: 查看当前会话 caveman 用量（token 数、节省估算）与模式状态
---

The user invoked /caveman-stats (one-shot: report, change nothing — do not switch modes or write flag files).

Report the caveman usage for the current session by running the stats script shipped with this plugin:

1. Resolve the plugin root: if the environment exposes CODEBUDDY_PLUGIN_ROOT, use it; otherwise locate the installed "ponytail-caveman-pack" directory (typical marketplace install: ~/.codebuddy/plugins/.../ponytail-caveman-pack).
2. Run: node "<pluginRoot>/hooks/caveman/caveman-stats.js" --session-file "<current session transcript path, if available>" (with the current session id when known). For example: node ".../hooks/caveman/caveman-stats.js" --session-id <session-id>.
3. Summarize the script's output in two or three terse lines: mode state, session count, tokens, and estimated savings.
4. If the transcript file is not available, state the mode state and say per-session token stats are unavailable here. Keep the whole reply under six lines.
