# Database Persistence

## ADDED Requirements

### Requirement: 数据源 MUST 支持通过配置在 MySQL 与 PostgreSQL 间切换

系统 MUST 同时兼容 MySQL 与 PostgreSQL 两种关系型数据源，并 MUST 通过配置（Spring Profile）指定当前使用哪一种；不指定时 MUST 默认回退到 MySQL，保持向后兼容。两种 JDBC 驱动 MUST 同时存在于构建依赖中，非激活 profile 的 `spring.datasource` 配置 MUST 不被加载、不被绑定。

#### Scenario: 通过 profile 选择 PostgreSQL 启动

- **WHEN** 以 `--spring.profiles.active=postgresql` 启动后端
- **THEN** 应用加载 postgresql 段的 `spring.datasource`（`driver-class-name` 为 `org.postgresql.Driver`，URL 以 `jdbc:postgresql://` 开头）
- **AND** 构建依赖同时包含 `com.mysql:mysql-connector-j` 与 `org.postgresql:postgresql`

#### Scenario: 通过 profile 选择 MySQL 启动

- **WHEN** 以 `--spring.profiles.active=mysql` 或不指定 profile 启动后端
- **THEN** 应用加载 mysql 段的 `spring.datasource`（`driver-class-name` 为 `com.mysql.cj.jdbc.Driver`，URL 以 `jdbc:mysql://` 开头）

#### Scenario: 非激活 profile 的配置不生效

- **WHEN** 激活某一 profile 启动应用
- **THEN** 另一个数据库的 `spring.datasource` 配置未被加载、未绑定到活动数据源，不产生驱动或连接冲突

#### Scenario: 方言按连接自动探测

- **WHEN** 应用使用任一激活 profile 启动并加载数据源
- **THEN** Hibernate 依据 JDBC 连接元数据自动解析对应方言（MySQLDialect / PostgreSQLDialect），无需在配置中硬编码 `dialect`
- **AND** 应用成功建立连接并完成启动，不抛出方言相关异常

### Requirement: 两种数据库下 Schema 与实体映射 MUST 均有效

同一份 JPA 实体与 `ddl-auto: update` MUST 能在 MySQL 与 PostgreSQL 下均成功生成有效 Schema；`user` 等保留字、自增主键、字符串枚举列在两种库下 MUST 语义一致。

#### Scenario: user 保留字在两种库下均可建表

- **WHEN** Hibernate 在任一激活 profile 下自动建表
- **THEN** `user` 表在 MySQL 与 PostgreSQL 下均能成功创建（`globally_quoted_identifiers=true` 配合实体 `@Table(name = "user")` 处理保留字）
- **AND** 实体 `User.java` 不再使用 MySQL 反引号 `` `user` `` 专属写法

#### Scenario: 自增主键与枚举列语义正确

- **WHEN** 向包含自增主键与状态枚举列的表插入记录
- **THEN** 主键由数据库自动生成且在两种库下唯一递增（`IDENTITY` / `AUTO_INCREMENT`）
- **AND** 状态列以字符串形式存储枚举值（如 `NORMAL`/`DELETED`），与 `@Enumerated(EnumType.STRING)` 一致

#### Scenario: 初始化脚本按库分别兼容

- **WHEN** 在所选数据库实例上执行对应初始化/种子脚本
- **THEN** 脚本使用对应库兼容语法（MySQL 或 PostgreSQL），无跨库专有语法错误
- **AND** 种子数据可幂等插入

### Requirement: 业务行为在两种数据源下 MUST 保持一致

数据源在 MySQL 与 PostgreSQL 间切换 MUST 对上层业务透明，现有领域数据模型、REST API 契约与 JPA 查询语义 MUST 保持不变，无需修改任何业务代码。

#### Scenario: 核心功能在两库下均回归通过

- **WHEN** 分别在 MySQL 与 PostgreSQL 数据源下运行核心业务流程（用户登录、工具 CRUD 与点赞、论坛发帖与评论、收藏、知识库、通知）
- **THEN** 各接口返回结果与单一 MySQL 时期一致，不出现因方言差异导致的查询失败或数据异常

#### Scenario: 实体与查询无需为切换库而改动

- **WHEN** 在两种数据源下运行应用
- **THEN** 现有 Controller/Service/Repository/DTO 与 JPQL 查询无需任何修改即可正常工作（因查询方言无关）

### Requirement: 自动化测试 MUST 在激活方言下通过

后端自动化测试 MUST 在所选/默认 profile 对应的方言兼容数据源下通过，不因双库共存引入不稳定。

#### Scenario: 测试在默认 profile 下通过

- **WHEN** 执行后端自动化测试（默认 profile = mysql）
- **THEN** 测试在 H2（与 mysql 兼容模式对齐）下全部通过，不依赖 PostgreSQL 专有语法
- **AND** 因查询方言无关，等价于两种库路径均被覆盖
