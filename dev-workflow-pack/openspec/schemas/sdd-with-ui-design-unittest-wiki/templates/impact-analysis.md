# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。
>
> **位置**：在 `design` 之后、`tasks` 之前生成。
>
> **触发条件**：仅当 `design.md` 涉及**修改现有代码**时必选；纯新增模块/页面时跳过此 artifact。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | N | `<path/to/new-file>` |
| 修改 | M | `<path/to/modified-file>` |
| 删除 | K | `<path/to/deleted-file>` |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `<Class>.<method>` | `<path:line>` | L0 / L1 / L2 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `<module>` 通过 `<intermediate>` 调用 `<target>`

### 2.3 反向调用图（被谁调用）

```
[被改动的类/函数]
  ├── [调用方 1] (file:line)
  │     ├── [传递调用方 1.1] (file:line)
  │     └── [传递调用方 1.2] (file:line)
  └── [调用方 2] (file:line)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `<repository/class>` | 数据访问层 | L0 / L1 |
| `<config/util>` | 配置/工具 | L0 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `<controller/endpoint>` | API 调用方变化 |
| `<frontend/page>` | 数据结构/接口变化 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `<path/to/test.java>` | 单元 | 仍有效 | 无需改动 |
| `<path/to/test.java>` | 集成 | 需更新 | 修改断言 / mock |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增，不影响现有代码 | 无 |
| **L1** | 修改函数签名/公共 API | 全量回归 + 通知调用方 |
| **L2** | 修改数据库 schema / 业务规则 / 跨模块契约 | 完整测试套件 + 灰度发布 |

**本次改动风险等级**: L0 / L1 / L2

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

```bash
bash scripts/lint-arch.sh
```

**结果**: PASS / FAIL（若 FAIL 必须修复后继续）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `<test-name>` —— 覆盖 `<scenario>`，位于 `<path>`
- [ ] `<test-name>` —— 覆盖 `<scenario>`，位于 `<path>`

---

## 8. 检查清单 (Checklist)

- [ ] 已识别所有直接/传递调用方
- [ ] 已列出上游/下游依赖
- [ ] 已评估风险等级
- [ ] `scripts/lint-arch.sh` 校验通过
- [ ] 已列出回归测试清单
- [ ] （L2 风险）已通知相关模块负责人

---

**生成工具**: CodeGraph MCP（codegraph_callers / codegraph_callees / codegraph_impact）+ scripts/lint-arch.sh
**生成时间**: <YYYY-MM-DD HH:MM>
**基础**: openspec/changes/<change-name>/proposal.md
