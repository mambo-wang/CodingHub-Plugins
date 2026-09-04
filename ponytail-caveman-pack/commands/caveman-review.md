---
name: caveman-review
description: 压缩式代码审查 —— 每个发现一行，带位置与修复建议
---

The user invoked /caveman-review (one-shot: review the current diff, then stop; do not switch any mode or keep "review mode" active afterward).

Review the current uncommitted changes for correctness and quality. One line per finding, compressed: <file:line> <problem>. <fix>. If the finding is nit-level, mark it (nit). Cover: bugs and logic errors, missing edge cases, regressions, unnecessary complexity, and anything dangerous. End with a one-line verdict: ship / ship with nits / needs changes. If the diff is clean: "Clean. Ship."
