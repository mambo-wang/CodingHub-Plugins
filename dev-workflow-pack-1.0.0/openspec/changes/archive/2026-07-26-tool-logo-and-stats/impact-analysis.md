# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。
>
> **位置**：在 `design` 之后、`tasks` 之前生成。
>
> **触发条件**：本次涉及修改现有代码（Tool/Category 实体、ToolService、ToolFileService、DTO），必须执行。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 3 | `frontend/src/components/ToolLogo.vue`（可选封装）、`frontend/src/utils/format.ts`（formatCount）、`backend/.../service/ToolLogoService.java`（可选，logo 绑定逻辑亦可内联 ToolService） |
| 修改 | 11 | `backend/.../model/Tool.java`、`model/Category.java`、`model/ToolFile.java`、`dto/ToolSummaryDTO.java`、`dto/ToolDetailDTO.java`、`dto/CategoryDTO.java`、`service/ToolService.java`、`service/ToolFileService.java`、`repository/UnifiedFavoriteRepository.java`、`repository/ToolFileRepository.java`、`controller/ToolController.java`（logo 绑定端点）；前端 `pages/HomePage.vue`、`pages/ToolDetailPage.vue`、工具上传/编辑表单、管理端分类页 |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 被改符号 | 调用方 | 位置 | 风险等级 |
|--------|--------|------|----------|
| `ToolService.toSummaryDTO` | `createTool` | `service/ToolService.java:97` | L1 |
| `ToolService.toSummaryDTO` | `getTools`（stream map） | `service/ToolService.java:65` | L1 |
| `ToolService.toSummaryDTO` | `getMyTools`（stream map） | `service/ToolService.java:236` | L1 |
| `ToolService.toDetailDTO` | `getToolById` | `service/ToolService.java:89` | L1 |
| `ToolService.toDetailDTO` | `updateTool` | `service/ToolService.java:138` | L1 |
| `ToolFileService.downloadFile` | `getFileInputStream` | `service/ToolFileService.java:183` | L1 |
| `ToolFileService.downloadFile` | `ToolFileController.downloadFile` | `controller/ToolFileController.java:68` | L1 |
| `ToolService.getTools` | `ToolController.getTools` / `GET /api/v1/tools` | `controller/ToolController.java:25` | L1 |
| `ToolService.getMyTools` | `GET /api/v1/users/me/tools` | `controller/UserController.java:36` | L1 |
| `CategoryService` | `CategoryController` | `controller/CategoryController.java:19` | L0（仅 DTO 加字段） |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- 前端广场页 `HomePage.vue` 通过 `GET /api/v1/tools` 消费 `ToolSummaryDTO`（新增 logoUrl/favoriteCount/downloadCount 字段，向后兼容）。
- 前端「我的工具」通过 `GET /api/v1/users/me/tools` 消费同一 DTO。
- 工具详情页 `ToolDetailPage.vue` 通过 `GET /api/v1/tools/{id}` 消费 `ToolDetailDTO`。
- 文件下载链路：`GET /api/v1/tools/{toolId}/files/{fileId}/download` → `ToolFileController.downloadFile` → `getFileInputStream` → `ToolFileService.downloadFile`（下载计数注入点）。

### 2.3 反向调用图（被谁调用）

```
ToolService.toSummaryDTO
  ├── createTool (ToolService.java:97)  ← POST /api/v1/tools
  ├── getTools (ToolService.java:65)    ← GET /api/v1/tools ← HomePage.vue
  └── getMyTools (ToolService.java:236) ← GET /api/v1/users/me/tools

ToolFileService.downloadFile
  ├── getFileInputStream (ToolFileService.java:183)
  │     └── ToolFileController.downloadFile (ToolFileController.java:68)
  └── ToolFileController.downloadFile (controller 直接调用)
        └── GET /api/v1/tools/{toolId}/files/{fileId}/download
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `UnifiedFavoriteRepository`（新增 count 方法） | 数据访问层 L2 | L1（跨模块读取统一收藏） |
| `ToolFileRepository`（新增 sum/group 查询） | 数据访问层 L2 | L1 |
| `ImageUploadController`（复用上传端点） | 控制器 L4 | L0（仅前端复用，不改后端） |
| `UploadConfig` | 配置 L0 | L0 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `GET /api/v1/tools` / `GET /api/v1/users/me/tools` | 响应 DTO 新增字段（向后兼容） |
| `GET /api/v1/tools/{id}` | ToolDetailDTO 新增 logoUrl/favoriteCount/downloadCount |
| `GET /api/v1/categories` | CategoryDTO 新增 logoUrl |
| `HomePage.vue` 工具卡片 | 渲染 logo + 统计行 |
| `ToolDetailPage.vue` | 标题区 logo |
| 工具上传/编辑表单 | logo 上传组件 |
| 管理端分类管理 | 分类默认 logo 设置 |
| MCP 工具检索输出 | 若复用 ToolSummaryDTO 则附带新字段（不影响既有消费） |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `service/ToolServiceTagFilterTest.java` | 单元 | 需更新 | `ToolService` 构造器追加 `UnifiedFavoriteRepository`/`ToolFileRepository`，需补 mock 实参（位置参数末尾追加） |
| `controller/ToolControllerTagFilterTest.java` | 单元 | 仍有效 | ToolController 若仅新增 logo 端点不改既有构造，无需改动；新增 logo 端点另写测试 |
| `service/ToolFileServiceTest.java` | 单元 | 编译排除（历史损坏） | 不扩展；下载计数新逻辑新建独立测试类 |
| `controller/ToolFileControllerTest.java` | 单元 | 编译排除（历史损坏） | 不扩展 |
| `repository/ToolFileRepositoryTest.java` | 集成 | 需更新/扩展 | 新增 `sumDownloadCountGroupByToolId` 查询测试 |
| `model/ToolFileTest.java` | 单元 | 需更新 | 新增 `downloadCount` 默认值/自增断言 |
| `service/McpSearchServiceTagFilterTest.java` | 单元 | 仍有效 | 不依赖本次改动符号 |

> 注：`ToolServiceTest.java` 在 compileTestJava 中被 exclude（历史损坏），不在回归范围；新增 ToolService 测试须新建正确构造的测试类（见 MEMORY 测试约定）。

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增，不影响现有代码 | 无 |
| **L1** | 修改函数签名/公共 API | 全量回归受影响模块单元测试 |
| **L2** | 修改数据库 schema / 业务规则 / 跨模块契约 | 完整测试套件 + 向后兼容验证 |

**本次改动风险等级**: **L2**

理由：涉及数据库 schema 变更（`tool.logo_url`、`category.logo_url`、`tool_file.download_count` 三列，ddl-auto:update 自动添加）；跨模块读取统一互动 `unified_favorite`；`ToolService` 构造器签名变化影响既有测试。缓解：所有 API 仅新增字段不改语义（向后兼容），存量行新列 NULL/0 无需回填，前端对缺失字段有占位兜底。

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

```bash
bash scripts/lint-arch.sh
```

**结果**: **PASS**（`scripts/lint-arch.sh` 在本机 Git Bash 环境挂起，改用等价 Python 脚本逐文件扫描 import 层级，输出 `PASS: no layer violations`）。

新增依赖方向校验：`ToolService`(L3) → `UnifiedFavoriteRepository`/`ToolFileRepository`(L2) 合法；`config→repository` 例外规则不涉及本次改动。

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `ToolServiceLogoStatsTest`（新建）—— 覆盖 logo 三级回退（tool→category→null）与 favoriteCount/downloadCount 批量聚合，位于 `service/`
- [ ] `ToolFileDownloadCountTest`（新建）—— 覆盖 `downloadFile` 触发 `download_count` 原子自增，位于 `service/`
- [ ] `ToolFileRepositoryTest`（扩展）—— 覆盖 `sumDownloadCountGroupByToolId` 分组聚合，位于 `repository/`
- [ ] `ToolControllerLogoTest`（新建）—— 覆盖 `POST /api/v1/tools/{id}/logo` 鉴权（owner/admin）与写库，位于 `controller/`
- [ ] `ToolServiceTagFilterTest`（更新）—— 补构造器新增依赖的 mock，确保既有标签过滤测试仍绿
- [ ] 前端 `HomePage.vue` 手动回归 —— 卡片 logo 渲染、裂图兜底、统计行四项在 375px/768px/1024px 完整展示，双主题切换

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L2）
- [x] `scripts/lint-arch.sh` 校验通过（等价 Python 扫描 PASS）
- [x] 已列出回归测试清单
- [x] （L2 风险）已在 design.md 迁移计划中说明向后兼容与回滚策略

---

## 9. 设计修正建议

- design.md 已覆盖主要受影响文件；补充提示：`ToolDetailDTO` 与 `CategoryDTO` 也需新增字段（detail 页 logo + 分类 logo），已在改动范围表中列明。
- `McpSearchService` 若复用 `ToolSummaryDTO` 组装结果，新字段自动附带，无需额外改动，但建议在 MCP 回归中确认不破坏既有输出结构。

---

**生成工具**: CodeGraph MCP（codegraph_callers / codegraph_status）+ 等价 Python 层级扫描
**生成时间**: 2026-07-21
**基础**: openspec/changes/tool-logo-and-stats/proposal.md
