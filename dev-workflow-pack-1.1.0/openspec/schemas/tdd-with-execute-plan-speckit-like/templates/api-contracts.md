# API Contracts

**Feature**: <!-- 功能标识 -->
**Date**: <!-- 日期 YYYY-MM-DD -->

## Base URL

```
<!-- API基础路径，如 /api/v1 -->
```

## Common Headers

| Header | Required | Description |
|--------|----------|-------------|
| Content-Type | Yes | `application/json` |
| Accept | Yes | `application/json` |
| Authorization | Conditional | `Bearer <accessToken>` — 需要认证的接口必填 |

## Common Response Structure

所有API响应遵循统一信封格式：

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

**错误码定义**：

| code | meaning |
|------|---------|
| 200 | 成功 |
| 400 | 请求参数无效 |
| 401 | 未认证——缺少或无效的Token |
| 403 | 无权限——权限不足 |
| 404 | 资源不存在 |
| 409 | 冲突——资源已存在 |
| 500 | 服务器内部错误 |

---

## [模块名称] APIs

### [METHOD] [路径] — [接口名称]

**描述**: <!-- 接口功能描述 -->

**认证**: 公开 / 需认证

**路径参数**:

| param | type | required | description |
|-------|------|----------|-------------|
| <!-- 参数名 --> | <!-- 类型 --> | <!-- Yes/No --> | <!-- 描述 --> |

**查询参数**:

| param | type | required | default | description |
|-------|------|----------|---------|-------------|
| <!-- 参数名 --> | <!-- 类型 --> | <!-- Yes/No --> | <!-- 默认值 --> | <!-- 描述 --> |

**请求体**:
```json
{
  "<field1>": "<value1>",
  "<field2>": "<value2>"
}
```

**请求字段说明**:

| field | type | required | description |
|-------|------|----------|-------------|
| <!-- 字段名 --> | <!-- 类型 --> | <!-- Yes/No --> | <!-- 描述 --> |

**输入校验**:
- <!-- 校验规则，如：email必须为合法邮箱格式 -->

**成功响应** (<!-- 状态码 -->):
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "<field1>": "<value1>",
    "<field2>": "<value2>"
  }
}
```

**响应字段说明**:

| field | type | description |
|-------|------|-------------|
| <!-- 字段名 --> | <!-- 类型 --> | <!-- 描述 --> |

**错误响应**:
- <!-- 状态码 -->: <!-- 错误描述 -->

---

<!-- 按上述格式继续添加更多接口 -->
