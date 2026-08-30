#!/usr/bin/env python3
"""CodeBuddy SessionStart hook: make OpenSpec initialization discoverable.

The plugin ships an ``openspec/`` directory (specs/schemas/changes for the
OpenSpec workflow). CodeBuddy loads plugin components from the *install*
directory, so that payload never reaches a project by itself. This hook
injects a short hint when the current project has no ``openspec/`` yet and the
plugin does, so the agent can offer the ``/init-openspec`` command to the user.

It deliberately does NOT copy anything automatically: the bundled payload is
project-specific (config.yaml carries the origin project's stack and possibly
credentials) and must only land in a project after explicit user consent.

Degrades silently on any error — the hook never blocks session startup.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _read_event() -> dict:
    if sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
        raw = raw.lstrip("\ufeff").strip()
    except Exception:  # noqa: BLE001
        return {}
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _plugin_openspec_dir() -> Path | None:
    for var in ("CODEBUDDY_PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT"):
        val = os.environ.get(var, "").strip()
        if val and (Path(val) / "openspec").is_dir():
            return Path(val) / "openspec"
    here = Path(__file__).resolve()
    if (here.parents[1] / "openspec").is_dir():
        return here.parents[1] / "openspec"
    return None


def _resolve_project_root(event: dict) -> Path | None:
    candidates = [
        os.environ.get("CODEBUDDY_PROJECT_DIR"),
        os.environ.get("CLAUDE_PROJECT_DIR"),
        event.get("cwd"),
    ]
    for c in candidates:
        if c and os.path.isdir(c):
            return Path(c)
    return None


def main() -> int:
    event = _read_event()
    src = _plugin_openspec_dir()
    project = _resolve_project_root(event)

    # No payload shipped, or no project context — stay silent.
    if src is None or project is None:
        print(json.dumps({"continue": True}))
        return 0

    # Project already has openspec/ (or is not a git repo) — stay silent.
    if (project / "openspec").is_dir() or not (project / ".git").is_dir():
        print(json.dumps({"continue": True}))
        return 0

    hint = (
        "[openspec] 当前项目尚未初始化 OpenSpec 目录。"
        "若想使用本插件的 OpenSpec 全流程工作流"
        "（openspec-new-change / propose / apply / verify / archive），"
        "请先询问用户是否运行 /init-openspec 将插件自带的 openspec/ 初始化到项目根目录；"
        "用户拒绝则忽略本提示，不要自动创建。"
    )

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):
        pass

    print(
        json.dumps(
            {
                "continue": True,
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": hint,
                },
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
