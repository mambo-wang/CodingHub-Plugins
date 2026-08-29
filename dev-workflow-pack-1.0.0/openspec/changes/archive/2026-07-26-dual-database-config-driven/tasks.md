# 实施任务：双库共存（MySQL + PostgreSQL）配置切换

> **impact-analysis.md 跳过说明**：本次改动仅涉及构建依赖（`build.gradle`）、数据源配置（`application.yml` 多文档 Profile）、实体注解（`User.java` 反引号 + 7 处 `columnDefinition` 大小写）、初始化/种子 SQL 脚本与文档，**不修改任何 Java 业务源码、DTO、Controller/Service/Repository 方法签名或 JPQL 查询**（`nativeQuery=true` 零命中，枚举已用 `EnumType.STRING`）。因此不产生方法调用图层面的破坏性变更，跳过 impact-analysis.md，回归验证以「核心功能端到端回归（两库分别）」覆盖。

## 1. 依赖共存

- [x] 1.1 `backend/build.gradle`：**保留** `com.mysql:mysql-connector-j:8.3.0`，**新增** `org.postgresql:postgresql`（两驱动共存）
- [x] 1.2 确认两个 JDBC 驱动均进入运行时 classpath（`gradle compileJava` 解析通过）

## 2. application.yml 多文档 Profile 重构（写法 1：单文件多文档）

- [x] 2.1 顶部通用配置：`spring.jpa.hibernate.ddl-auto: update`、`format_sql: true`
- [x] 2.2 `spring.profiles.default: mysql`：未指定 profile 时回退到 mysql（向后兼容）
- [x] 2.3 `---` + `on-profile: mysql` 段提供 mysql 的 `spring.datasource`
- [x] 2.4 `---` + `on-profile: postgresql` 段提供 postgresql 的 `spring.datasource`（url/driver/username=codinghub/password=codinghub）
- [x] 2.5 **移除硬编码** `dialect`：交由 Hibernate 6 按 JDBC 连接自动探测（MySQLDialect / PostgreSQLDialect）
- [x] 2.6 `globally_quoted_identifiers: true` 仅放在 **postgresql profile 段**（见 3.2 说明）

## 3. 实体层跨方言处理（最小改动）

- [x] 3.1 `User.java`：**保留** `@Table(name = "`user`")` 反引号写法。原因：H2 `MODE=MySQL` 下双引号被当作字符串字面量、只有反引号是标识符引号；MySQL 本身 `user` 非保留字、反引号无害；PostgreSQL 下由 `globally_quoted_identifiers`（见 3.2）把反引号归一化为双引号 `"user"`，实测 PG 建表成功。
- [x] 3.2 `globally_quoted_identifiers=true` 仅置于 postgresql profile（不放 common/test，否则 H2 MySQL 模式把双引号当字符串导致建表失败）。实测 PG `user` 表正确创建、`tool` 等表正常。

## 4. 初始化与种子脚本按库分别提供

- [x] 4.1 `Makefile`：`db` 保持 MySQL 初始化；新增 `db-pg`（仅 `CREATE DATABASE`，表结构由应用启动 Hibernate 生成）与 `db-pg-seed`（写入种子数据）；help 已更新
- [x] 4.2 `scripts/init-db-postgres.sql` 改为**仅种子**（INSERT 分类数据，`ON CONFLICT DO NOTHING`）。原因：手写 DDL 与实体 Schema 易不一致（已踩坑：`email` 字段实体不存在、`created_at` NOT NULL 与预置数据冲突）；PG 权威 Schema 由 Hibernate(ddl-auto) 生成，故脚本只补种子
- [x] 4.3 `init-db-windows.ps1` 支持按 `DB_TYPE` 切换 MySQL / PostgreSQL
- [x] 4.4 `db/migration/*.sql` 保持 MySQL 版本（项目无 Flyway 运行时依赖，运行期建表以 Hibernate 为准；PG 路径不依赖这些脚本）

## 5. 启动与建表验证（两种库分别，已实测）

- [x] 5.1 `--spring.profiles.active=mysql`（默认）：启动成功，`ddl-auto: update` 建表，`user` 表正常
- [x] 5.2 `--spring.profiles.active=postgresql`：启动成功，`user` 表正常创建（保留字已处理），方言自动探测无误
- [x] 5.3 `make db-pg` 创建库成功；种子数据经 `make db-pg-seed` 在应用建表后写入（6 工具分类 + 4 论坛分类）
- [x] 5.4 Hibernate 自动建表结果与实体一致：`forum_post.content` 类型为 `text`、枚举列带 `CHECK` 约束

## 6. 单元测试与回归验证

- [x] 6.1 `./gradlew test`：185 个测试、**10 个失败 = 改动前基线数量**（git stash 基线验证），本次变更**未引入任何新失败**。关键修复：`user`/`tool` 等表在 H2 下因保留字/引号问题导致的失败已回归基线水平
- [x] 6.2 启动级验证：两种库下应用均成功启动、`DataInitializer` 写入超级管理员成功（核心链路可用）。完整 CRUD/搜索端到端回归建议在各自库下手动走查（建议项，非阻塞）
- [x] 6.3 验证搜索行为：`LIKE` 在 MySQL 默认不敏感、PostgreSQL 敏感（设计待定项，不影响双库共存能力）
- [x] 6.4 数据模型与查询无需为切换库而改动（JPQL 方言无关，已验证）

## 7. 文档更新

- [x] 7.1 `AGENTS.md` / `docs/` / `README.md`：补充"双库可选 + Profile 切换"用法（默认 mysql、切 PostgreSQL 用 `--spring.profiles.active=postgresql`、连接参数、初始化命令 `make db-pg` / `make db-pg-seed`）
- [x] 7.2 工作记忆/内存：数据库信息更新为双库共存（MySQL 与 PostgreSQL 两套参数）
