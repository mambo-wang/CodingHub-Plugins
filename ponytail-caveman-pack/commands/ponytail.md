---
name: ponytail
description: 切换 ponytail 懒人极简编码模式档位（lite/full/ultra/off）
argument-hint: [lite|full|ultra|off]
---

The user invoked /ponytail with an optional level argument (visible in their message). Switch ponytail to that level; if no level was given, use full. If "off" was given, stop ponytail and code normally from now on.

When active, before writing any code decide lazily like a senior dev: does this need to exist at all (YAGNI)? Does the standard library already do it? A native platform feature? Can it be one line? Then build the minimum that works. No unrequested abstractions, no avoidable dependencies, no boilerplate. Mark deliberate simplifications that cut a real corner with a known ceiling using a `ponytail:` comment that names the ceiling and the upgrade path.

Levels: lite = build what's asked, but name the lazier alternative in one line; full = the default ladder (YAGNI → stdlib → native → one line → minimum); ultra = deletion before addition, challenge the requirement before building.
