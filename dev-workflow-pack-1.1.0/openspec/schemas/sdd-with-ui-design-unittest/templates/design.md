## 背景（Context）

<!-- 背景与现状、约束条件、相关方 -->

## 目标 / 非目标（Goals / Non-Goals）

**目标：**
<!-- 本设计要达成的目标 -->

**非目标：**
<!-- 明确排除的范围 -->

## 决策（Decisions）

<!-- 关键设计决策及理由（为何选 X 而非 Y？列出备选方案） -->

## 架构图

<!-- 【条件生成】当变更涉及多个模块/服务、引入新架构模式或改变系统拓扑时使用 -->
<!-- 使用 flowchart 展示模块间依赖关系和数据流向 -->

```mermaid
flowchart TD
    %% 示例：替换为实际架构
    Client --> Frontend["前端 :5173"]
    Frontend --> Backend["后端 :8082"]
    Backend --> DB["数据库 :3306"]
    Backend --> Storage["文件存储"]
```

## 流程图

<!-- 【条件生成】当涉及复杂业务流程、审批链路、算法逻辑时使用 -->
<!-- 使用 flowchart TD（上下）或 LR（左右），用 {菱形} 表示判断节点 -->

```mermaid
flowchart TD
    %% 示例：替换为实际流程
    A[开始] --> B{条件判断}
    B -->|是| C[路径 A]
    B -->|否| D[路径 B]
    C --> E[结束]
    D --> E
```

## 时序图

<!-- 【条件生成】当涉及多系统交互、API 调用链路、消息流转时使用 -->
<!-- 使用 participant 定义参与者，->> 请求，-->> 响应 -->

```mermaid
sequenceDiagram
    %% 示例：替换为实际交互
    participant C as 客户端
    participant S as 服务器
    participant DB as 数据库
    C->>S: 请求
    S->>DB: 查询
    DB-->>S: 结果
    S-->>C: 响应
```

## 状态图

<!-- 【条件生成】当涉及对象状态变迁（订单、审批、工单等）时使用 -->
<!-- [*] 表示初始/终止状态，--> 上的文本是触发事件 -->

```mermaid
stateDiagram-v2
    %% 示例：替换为实际状态流转
    [*] --> 初始状态
    初始状态 --> 状态A : 触发事件
    状态A --> 状态B : 触发事件
    状态B --> [*]
```

## 数据模型

<!-- 【条件生成】当涉及数据库表结构变更、实体关系变更时使用 -->
<!-- GitHub Mermaid ER 图仅支持标准类型：int, string, float, boolean, date, datetime -->
<!-- 禁止使用 bigint, text, decimal, long 等非标准类型，否则 GitHub 无法渲染 -->

```mermaid
erDiagram
    %% 示例：替换为实际实体关系
    USER ||--o{ ORDER : "拥有"
    USER {
        int id PK
        string username
        string email
    }
    ORDER {
        int id PK
        int userId FK
        float amount
        string status
    }
```

## 风险 / 权衡（Risks / Trade-offs）

<!-- 已知风险和权衡。格式：[风险] → 缓解措施 -->

## 迁移计划（Migration Plan）

<!-- 【可选】部署步骤、回滚策略（如涉及数据迁移或部署变更） -->

## 待定问题（Open Questions）

<!-- 待决策或未知事项 -->
