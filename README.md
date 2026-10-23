# CodingHub-Plugins

插件市场仓库。智能体只需配置本仓库 git 地址即可拉取插件列表。

仓库地址：`https://github.com/mambo-wang/CodingHub-Plugins.git`

## 拉取流程

```
1. 客户端配置 git 市场地址：https://github.com/mambo-wang/CodingHub-Plugins.git
2. 客户端读 .codebuddy-plugin/marketplace.json → 插件列表（name / version / description / source）
3. 用户选插件 → 客户端按 source 路径安装
```

## 插件列表

| 插件 | 版本 | 说明 |
|------|------|------|
| dev-workflow-pack | 1.1.1 | 开发工作流全家桶（工程技能集 + OpenSpec 工作流 + CodeWiki 团队记忆） |
| ponytail-caveman-pack | 1.0.0 | 极简代码与极简沟通双引擎 |
| tech-article-write-pack | 1.0.0 | 技术文章写作技能包（评测长文 + 架构图 + 文本人化 + 公众号排版） |

## 新增插件约定

1. 插件放独立目录，目录名 = 插件 name（kebab-case）
2. 必须含 `.codebuddy-plugin/plugin.json`（客户端清单入口，缺它组件不注册）
3. 根 `plugin.json` 可选，仅平台展示用
4. 在 `.codebuddy-plugin/marketplace.json` 与根 `marketplace.json` 的 `plugins` 数组加条目（name/version/description/source），两文件内容必须一致
5. 禁止在 plugin.json 声明 `commands`/`skills` 字段，组件靠目录自动扫描
6. 本地跑 `python scripts/validate_marketplace.py`，CI 也会校验
