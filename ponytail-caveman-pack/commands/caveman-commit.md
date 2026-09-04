---
name: caveman-commit
description: 为已暂存改动生成极简 Conventional Commits 提交信息
---

The user invoked /caveman-commit (one-shot: generate a commit message, then stop; do not switch any mode or keep "commit mode" active afterward).

Inspect the staged changes (git diff --cached; if nothing is staged, fall back to unstaged git diff and say so). Write ONE conventional commit message, compressed to intent only: <type>(<scope>): <subject> where type is fix/feat/refactor/docs/chore/test/perf/style/build/ci/revert. If the change spans several intents, pick the dominant type and put the rest in a short body, no more than a few lines. No commentary, no jokes, no preamble — just the message, ready to paste.
