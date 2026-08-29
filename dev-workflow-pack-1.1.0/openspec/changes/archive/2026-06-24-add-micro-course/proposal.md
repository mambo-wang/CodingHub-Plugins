# Proposal: 微课模块（视频共享）

## 为什么（Why）

CodingHub 当前定位为 AI 工具/资源管理平台，缺乏视频内容共享能力。用户（尤其是 AI 学习者）对「微课」——即短视频教程——有明确需求：上传演示视频、分享使用经验、通过评论互动交流。增加微课模块可将平台从「工具目录」升级为「AI 学习社区」，显著提升用户黏性和内容丰富度。

## 变更内容（What Changes）

- 新增 **Video 实体**及相关数据表（video、video_comment、video_like、video_favorite）
- 新增**视频上传**功能：用户可上传 MP4 视频文件（单文件 ≤ 1GB），存储于本地磁盘
- 新增**视频流式播放**：后端支持 HTTP Range 请求，前端使用 `<video>` 标签直接播放 MP4
- 新增**视频互动功能**：点赞、评论、收藏（登录后操作），复用论坛模块的互动模式
- 新增**视频列表页**（`/videos`）、**视频详情页**（`/videos/:id`）、**视频上传页**（`/videos/upload`）
- 修改 **ProfilePage.vue**：用户中心增加「我的视频」和「我的收藏」tab
- 修改 **SecurityConfig.java**：视频播放/列表接口免登录，互动接口需登录
- 修改 Spring 配置：增大 `multipart.max-file-size` 至 1GB，支持大文件上传
- 修改 **Header.vue** 导航：添加「微课」入口链接

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `video-core`: 视频核心功能——上传、存储、列表查询、详情查询、流式播放（HTTP Range）、更新/删除、播放量统计、我的视频列表
- `video-interaction`: 视频互动功能——点赞/取消点赞（toggle）、评论列表/发评论（XSS 过滤）、收藏/取消收藏（toggle）、互动状态查询、我的收藏列表

### 修改能力（Modified Capabilities）

（无需修改现有 spec，微课模块是全新功能，仅修改现有配置和页面组件）

## 影响范围（Impact）

| 影响范围 | 说明 |
|----------|------|
| **后端新增** | 4 个 Model、4 个 Repository、2 个 Service、2 个 Controller、约 10 个 DTO、1 个 Config |
| **后端修改** | `SecurityConfig.java`（白名单）、`application.yaml`（multipart 配置） |
| **前端新增** | 3 个页面、3 个组件、1 个 Service、1 个 Types 文件 |
| **前端修改** | `ProfilePage.vue`（新增 tab）、`Header.vue`（新增导航）、`router/index.ts`（新增路由） |
| **数据库** | 新增 4 张表（video、video_comment、video_like、video_favorite） |
| **磁盘** | 视频文件占用本地磁盘空间（`uploads/videos/`） |
| **无 Breaking Change** | 所有变更为新增功能，不影响现有工具/论坛模块 |

## MVP 范围

**包含：** 视频上传（MP4 ≤ 1GB 本地存储）、直接 MP4 播放（HTTP Range）、点赞/评论/收藏、视频列表/详情页、播放量统计

**不包含（后续迭代）：** 视频转码/HLS、弹幕系统、视频分类、分片上传、OSS/CDN、视频审核
