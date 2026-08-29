## 为什么（Why）

当前 CodingHub 后端强绑定 MySQL 8.x：数据源 URL/驱动/Hibernate 方言、初始化脚本（`Makefile`、`init-db-windows.ps1`、`scripts/init-db.sql`）以及 `db/migration` 下的 DDL 均使用 MySQL 专有语法。但经代码探查，业务层对具体数据库几乎无强依赖：

- 全仓**零** `nativeQuery=true`，所有查询走 JPQL/Hibernate，方言无关；
- 主键统一 `GenerationType.IDENTITY`、枚举统一 `@Enumerated(EnumType.STRING)`，在 MySQL 与 PostgreSQL 下均兼容；
- 建表实际由 Hibernate `ddl-auto: update` 负责，migration/脚本用于手动初始化与种子。

因此无需做单向迁移，也无需改动任何业务代码。目标是让应用**同时兼容两种数据库，由配置文件（Spring Profile）指定使用哪一种**，既保留现有 MySQL 环境，又为团队提供切换到 PostgreSQL 的自由，消除数据库锁定。

## 变更内容（What Changes）

- `backend/build.gradle`：**保留** `com.mysql:mysql-connector-j`，**新增** `org.postgresql:postgresql`（两者共存，非替换）。
- `backend/src/main/resources/application.yml`：重构为单文件多文档——通用配置（JPA、`ddl-auto`、`globally_quoted_identifiers`）置于顶部，下方用 `---` 分隔出 `spring.config.activate.on-profile: mysql` 与 `postgresql` 两段，各自提供 `spring.datasource`（url/driver/username/password）。**移除硬编码的 `MySQLDialect`**，交由 Hibernate 6 按 JDBC 连接自动探测方言，从而实现"同一份实体、两种库都能跑"。
- `backend/src/main/java/com/iaihub/toolbox/model/User.java`：将 `@Table(name = "`user`")` 中的 MySQL 反引号去掉，改为 `@Table(name = "user")`，配合 `globally_quoted_identifiers=true` 在两种库下都将标识符加引号（解决 PostgreSQL 保留字 `user` 问题）。约 1 行改动，非业务逻辑。
- 初始化脚本：`Makefile` 的 `db` 目标、`init-db-windows.ps1`、`scripts/init-db.sql` 提供 MySQL 与 PostgreSQL 两套（或 PostgreSQL 侧直接交由 `ddl-auto` 建表），按激活 profile 选用。
- 不修改任何 Controller/Service/Repository/DTO 业务代码，不修改 JPQL 查询。

## 能力清单（Capabilities）

### 新增能力（New Capabilities）
- `database-persistence`：定义应用的数据库持久化配置能力——数据源连接、方言、Schema 初始化**必须同时兼容 MySQL 与 PostgreSQL**，且可通过配置（Profile）选择使用哪一种，现有领域数据模型与业务查询语义在两种库下保持一致。

### 修改能力（Modified Capabilities）
<!-- 本次为基础设施层扩展，不改变各业务能力的对外需求（REQUIREMENTS），故无业务能力级 delta。 -->

## 影响范围（Impact）

- **代码（极少）**：`backend/build.gradle`（依赖共存）、`application.yml`（多文档 Profile）、`User.java`（去掉反引号）。**无业务逻辑改动**。
- **脚本**：`Makefile`（`db` 目标支持两库）、`init-db-windows.ps1`、`scripts/init-db.sql`。
- **测试**：`application-test.yml` 仍用 H2，因查询方言无关，两种库路径均可覆盖；视情况将 H2 `MODE` 与默认 profile 对齐。
- **JPA 层**：现有 `@Query` 均为 JPQL，`GenerationType.IDENTITY` 与枚举字符串映射在两库兼容，风险低。
- **依赖/环境**：运行时按激活 profile 连接对应数据库；本地/部署需具备所选数据库服务。
- **文档**：`AGENTS.md`、`docs/`、`README.md` 的数据库说明补充"双库可选 + Profile 切换"用法。

## 默认值与选择机制

- 不指定 profile 时默认回退到 `mysql`，保持现状向后兼容。
- 启动时通过 `--spring.profiles.active=postgresql`（或环境变量 `SPRING_PROFILES_ACTIVE`）选择；非激活 profile 的 `spring.datasource` 不会被加载、不会绑定，故"两套配置同时存在"无害。
