---
name: init-openspec
description: 将插件自带的 openspec/ 规范目录（config.yaml、specs/、schemas/、changes/）初始化到当前项目根目录，是 OpenSpec 全流程工作流的前提
---

把插件内置的 `openspec/` 目录复制到当前项目根目录，使本项目具备 OpenSpec 工作流能力（之后可用 openspec-new-change / propose / apply / verify / archive 等技能）。

执行步骤：

1. **定位插件安装目录**：先运行 `echo $CODEBUDDY_PLUGIN_ROOT`（Windows PowerShell 用 `echo $env:CODEBUDDY_PLUGIN_ROOT`）。若输出为空，向用户询问插件安装位置，或提示用户在 IDE 插件管理里查看安装路径。

2. **运行初始化脚本**：
   ```bash
   python "<插件目录>/scripts/init_openspec.py"
   ```
   脚本默认把 `openspec/` 复制到当前项目根目录（即 CODEBUDDY_PROJECT_DIR），幂等——若项目已有 `openspec/` 会直接跳过。

3. **验证并告知用户**：确认项目根目录出现 `openspec/`（含 `config.yaml`、`specs/`、`schemas/`、`changes/`），然后告诉用户：
   - 已初始化 OpenSpec 工作流目录；
   - 可用 `/openspec-new-change` 开始新变更，或用 `/openspec-onboard` 走完整流程。

注意事项：

- 脚本只做复制，不修改项目已有文件（`openspec/` 已存在时默认不覆盖；需要覆盖同名文件可加 `--force`）。
- `openspec/config.yaml` 里含原项目的项目描述与技术栈信息（可能含敏感凭据），复制后提醒用户按当前项目实际情况修改该文件。
- 若用户不需要 OpenSpec 工作流，说明该命令不会做任何事，跳过即可。
