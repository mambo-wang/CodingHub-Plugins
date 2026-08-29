# Impact Analysis: add-sort-and-pin

> Generated from codebase at `D:\repos\CodingHub`
> Change design: `openspec/changes/add-sort-and-pin/design.md`

---

## 1. Change Surface

### 1.1 Backend — Modified Files

| # | File (relative to `backend/src/main/java/com/iaihub/toolbox/`) | Change Type | Summary |
|---|---|---|---|
| 1 | `model/Tool.java` | MODIFY | Add `pinned` boolean field (default false), add `@Index` for `(pinned, score)` |
| 2 | `model/forum/ForumPost.java` | MODIFY | Add `pinned` boolean field (default false), add `@Index` for `(pinned, score)` |
| 3 | `model/video/Video.java` | MODIFY | Add `pinned` boolean field, add `score` BigDecimal field, add `updateScore()` method, wire `incrementXxx()` to call `updateScore()`, add `@Index` for `(pinned, score)` |
| 4 | `repository/ToolRepository.java` | MODIFY | Add `findByFiltersOrderByHot` JPQL (`ORDER BY pinned DESC, score DESC`), add `findTop5ByStatusOrderByScoreDesc` |
| 5 | `repository/forum/ForumPostRepository.java` | MODIFY | Add `findByStatusOrderByHot` JPQL, add search/category variants with hot sort, add `findTop5ByStatusOrderByScoreDesc` |
| 6 | `repository/video/VideoRepository.java` | MODIFY | Add `findByStatusOrderByHot` JPQL, add `findTop5ByStatusOrderByScoreDesc` |
| 7 | `service/ToolService.java` | MODIFY | Extend `getTools()` to handle `sortBy=hot` (pinned+score), add `pinTool(id)`, `unpinTool(id)`, `getHotTop5()` |
| 8 | `service/forum/ForumPostService.java` | MODIFY | Add `sortBy` parameter to `getPostList()`, add `pinPost(id)`, `unpinPost(id)`, `getHotTop5()` |
| 9 | `service/video/VideoService.java` | MODIFY | Add `sortBy` parameter to `getVideoList()`, add `pinVideo(id)`, `unpinVideo(id)`, `getHotTop5()`, wire `updateScore()` into `incrementViewCount/Like/Comment` |
| 10 | `controller/ToolController.java` | MODIFY | Change `sortBy` default from `"latest"` to `"hot"`, add `GET /hot-top5`, `POST /{id}/pin`, `DELETE /{id}/pin` |
| 11 | `controller/forum/ForumPostController.java` | MODIFY | Add `sortBy` param to `getPostList()`, add `GET /hot-top5`, `POST /{id}/pin`, `DELETE /{id}/pin` |
| 12 | `controller/video/VideoController.java` | MODIFY | Add `sortBy` param to `getVideoList()`, add `GET /hot-top5`, `POST /{id}/pin`, `DELETE /{id}/pin` |
| 13 | `dto/ToolSummaryDTO.java` | MODIFY | Add `pinned` (Boolean), `score` (BigDecimal) fields |
| 14 | `dto/forum/ForumPostDTO.java` | MODIFY | Add `pinned` (Boolean), `score` (BigDecimal) fields to record |
| 15 | `dto/video/VideoListItem.java` | MODIFY | Add `pinned` (Boolean), `score` (BigDecimal) fields |
| 16 | `config/SecurityConfig.java` | MODIFY | Add security rules: `POST/DELETE /{module}/{id}/pin` requires ADMIN or SUPER_ADMIN role; `GET /{module}/hot-top5` is public |

### 1.2 Backend — New Files

| # | File | Purpose |
|---|---|---|
| 1 | `scripts/migrations/V4__add_sort_and_pin.sql` | DDL: add `pinned` column to `tool`, `forum_post`, `video`; add `score` column to `video`; add composite indexes `(pinned DESC, score DESC)` |

### 1.3 Frontend — Modified Files

| # | File (relative to `frontend/src/`) | Change Type | Summary |
|---|---|---|---|
| 1 | `types/index.ts` | MODIFY | Add `pinned?`, `score?` to `ToolSummary` interface |
| 2 | `types/tool.ts` | MODIFY | Add `pinned?`, `score?` to `ToolSummary` and `ToolDetailDTO` |
| 3 | `types/forum.ts` | MODIFY | Add `pinned?`, `score?` to `ForumPost` interface |
| 4 | `types/video.ts` | MODIFY | Add `pinned?`, `score?` to `VideoListItem` interface |
| 5 | `pages/HomePage.vue` | MODIFY | Add SortTab component, fetch hot-top5 IDs, render pin/hot icons on cards, change default sortBy to `"hot"` |
| 6 | `pages/forum/PostListPage.vue` | MODIFY | Add SortTab, pass `sortBy` param to `forumService.getPostList()`, fetch hot-top5, render icons |
| 7 | `pages/video/VideoListPage.vue` | MODIFY | Add SortTab, pass `sortBy` param to `videoService.getVideoList()`, fetch hot-top5, render icons |
| 8 | `services/forum.ts` | MODIFY | Add `sortBy` to `getPostList()` params, add `getHotTop5()`, `pinPost()`, `unpinPost()` |
| 9 | `services/video.ts` | MODIFY | Add `sortBy` to `getVideoList()` params, add `getHotTop5()`, `pinVideo()`, `unpinVideo()` |
| 10 | `services/tool.ts` | MODIFY | Add `getHotTop5()`, `pinTool()`, `unpinTool()` |

### 1.4 Frontend — New Files

| # | File | Purpose |
|---|---|---|
| 1 | `components/common/SortTab.vue` | Reusable "hot / latest" tab switcher, emits `update:sortBy` |
| 2 | `components/common/PinIcon.vue` | Pin icon (upward arrow) shown when `item.pinned === true` |
| 3 | `components/common/HotIcon.vue` | Fire icon shown when `hotTop5Ids.has(item.id)` |

---

## 2. Call Graph

### 2.1 Tool Module — List with Sort

```
HomePage.vue
  └─ fetchTools() → GET /api/v1/tools?sortBy={hot|latest}
       └─ ToolController.getTools(categoryId, keyword, sortBy, page, size)
            └─ ToolService.getTools(categoryId, keyword, sortBy, page, size)
                 ├─ [sortBy=hot]    → ToolRepository.findByFiltersOrderByHot(categoryId, keyword, pageable)
                 │                     JPQL: ORDER BY t.pinned DESC, t.score DESC
                 ├─ [sortBy=latest] → ToolRepository.findByFilters(categoryId, keyword, pageable)   [EXISTING, unchanged]
                 │                     JPQL: ORDER BY t.createdAt DESC
                 └─ [sortBy=name]   → ToolRepository.findByFiltersOrderByName(...)                   [EXISTING, unchanged]
            └─ toSummaryDTO(tool) → now includes pinned, score fields
```

### 2.2 Tool Module — Hot Top 5

```
HomePage.vue (onMounted)
  └─ GET /api/v1/tools/hot-top5
       └─ ToolController.getHotTop5()
            └─ ToolService.getHotTop5()
                 └─ ToolRepository.findTop5ByStatusOrderByScoreDesc()
                      JPQL: SELECT t.id FROM Tool t WHERE t.status='NORMAL' ORDER BY t.score DESC LIMIT 5
            └─ Returns List<Long> (5 IDs)
  └─ Cached as Set<number> hotTop5Ids
  └─ Per card: if hotTop5Ids.has(tool.id) → show HotIcon
```

### 2.3 Tool Module — Pin / Unpin

```
PinIcon.vue (admin click)
  └─ POST /api/v1/tools/{id}/pin  (or DELETE to unpin)
       └─ ToolController.pinTool(id) / unpinTool(id)
            ├─ SecurityConfig: requires ADMIN or SUPER_ADMIN
            └─ ToolService.pinTool(id) / unpinTool(id)
                 └─ toolRepository.findByIdAndStatusNormal(id) → set pinned=true/false → save
```

### 2.4 Forum Module — List with Sort

```
PostListPage.vue
  └─ loadPosts() → forumService.getPostList({category, keyword, sortBy, page, size})
       └─ GET /api/forum/posts?sortBy={hot|latest}
            └─ ForumPostController.getPostList(category, tag, keyword, sortBy, page, size)
                 └─ ForumPostService.getPostList(categoryId, keyword, sortBy, pageable)
                      ├─ [sortBy=hot]    → postRepository.findByStatusOrderByHot(status, pageable)
                      │                     JPQL: ORDER BY p.pinned DESC, p.score DESC
                      └─ [sortBy=latest] → postRepository.findByStatusOrderByCreatedAtDesc(status, pageable) [EXISTING]
                 └─ toDTO(post) → now includes pinned, score fields
```

### 2.5 Forum Module — Hot Top 5 & Pin

```
PostListPage.vue → GET /api/forum/posts/hot-top5 → ForumPostController → ForumPostService → ForumPostRepository
PostListPage.vue → POST/DELETE /api/forum/posts/{id}/pin → ForumPostController → ForumPostService (ADMIN only)
```

### 2.6 Video Module — List with Sort

```
VideoListPage.vue
  └─ loadVideos() → videoService.getVideoList(page, size, sortBy)
       └─ GET /api/v1/videos?sortBy={hot|latest}
            └─ VideoController.getVideoList(page, size, sortBy)
                 └─ VideoService.getVideoList(page, size, sortBy)
                      ├─ [sortBy=hot]    → videoRepository.findByStatusOrderByHot(status, pageable)
                      │                     JPQL: ORDER BY v.pinned DESC, v.score DESC
                      └─ [sortBy=latest] → videoRepository.findByStatusOrderByCreatedAtDesc(status, pageable) [EXISTING]
                 └─ toVideoListItem(video) → now includes pinned, score fields
```

### 2.7 Video Module — Hot Top 5 & Pin

```
VideoListPage.vue → GET /api/v1/videos/hot-top5 → VideoController → VideoService → VideoRepository
VideoListPage.vue → POST/DELETE /api/v1/videos/{id}/pin → VideoController → VideoService (ADMIN only)
```

### 2.8 Entity-Level: Video score field addition

```
Video.incrementViewCount()   → now calls updateScore()  [NEW]
Video.incrementLikeCount()   → now calls updateScore()  [NEW]
Video.decrementLikeCount()   → now calls updateScore()  [NEW]
Video.incrementCommentCount()→ now calls updateScore()  [NEW]
Video.updateScore()          → score = viewCount*1 + likeCount*3 + commentCount*5  [NEW, mirrors Tool/ForumPost]
```

---

## 3. Dependency Chain

### 3.1 Database (Upstream)

```
MySQL (ai_tool_square)
  ├─ tool         → ADD COLUMN pinned BOOLEAN DEFAULT FALSE; ADD INDEX idx_tool_pinned_score (pinned DESC, score DESC);
  ├─ forum_post   → ADD COLUMN pinned BOOLEAN DEFAULT FALSE; ADD INDEX idx_forum_post_pinned_score (pinned DESC, score DESC);
  └─ video        → ADD COLUMN pinned BOOLEAN DEFAULT FALSE;
                    ADD COLUMN score DECIMAL(10,2) DEFAULT 0;
                    ADD INDEX idx_video_pinned_score (pinned DESC, score DESC);
```

Migration file: `scripts/migrations/V4__add_sort_and_pin.sql`

### 3.2 Backend Config

```
SecurityConfig.java
  ├─ Add: .requestMatchers(HttpMethod.GET, "/api/v1/tools/hot-top5").permitAll()
  ├─ Add: .requestMatchers(HttpMethod.POST, "/api/v1/tools/{id}/pin").hasAnyRole("ADMIN","SUPER_ADMIN")
  ├─ Add: .requestMatchers(HttpMethod.DELETE, "/api/v1/tools/{id}/pin").hasAnyRole("ADMIN","SUPER_ADMIN")
  ├─ Same pattern for /api/forum/posts/{id}/pin and /api/v1/videos/{id}/pin
  └─ Same pattern for /api/forum/posts/hot-top5 and /api/v1/videos/hot-top5 (public GET)
```

### 3.3 Frontend (Downstream)

```
Types (types/*.ts)
  └─ Add pinned?, score? to ToolSummary, ForumPost, VideoListItem

Services (services/*.ts)
  └─ Add sortBy param, getHotTop5(), pinXxx(), unpinXxx() functions

Components (components/common/)
  └─ SortTab.vue, PinIcon.vue, HotIcon.vue (new shared components)

Pages (pages/)
  └─ HomePage.vue, PostListPage.vue, VideoListPage.vue
     └─ Import SortTab, PinIcon, HotIcon
     └─ Wire sortBy state, hotTop5Ids cache, admin pin actions
```

### 3.4 Cross-cutting Dependencies

| Dependency | Direction | Impact |
|---|---|---|
| `OverviewServiceImpl.getVideoRanks()` | Reads Video | Currently uses `viewCount` for ranking. After adding `score` to Video, consider migrating to `score`-based ranking for consistency. **Not required for this change** but noted as follow-up. |
| `UnifiedLikeService` / `UnifiedCommentService` | Writes to Tool/ForumPost/Video | When likes/comments are added, `incrementXxx()` is called. For Video, this now triggers `updateScore()`. Must verify `VideoInteractionService` calls `video.incrementLikeCount()` (not direct field set). |
| `McpSearchService` | Reads ToolRepository | Uses `findTop10ByStatusAndNameContainingIgnoreCase` — unaffected by sort/pin changes. |

---

## 4. Affected Tests

### 4.1 Tests That WILL Break (constructor / mock mismatch)

| Test File | Reason | Fix Required |
|---|---|---|
| `service/ToolServiceTest.java` | Constructor in `setUp()` creates `ToolService(toolRepository, toolCommentRepository, toolLikeRepository, categoryRepository, userRepository, toolFileService)` — **note: the test passes 6 args but current ToolService has 4 fields**. If pin/unpin is added to ToolService, no constructor change needed (uses same repos). But `Tool.builder()` in test data doesn't set `pinned` — Lombok `@Builder.Default` handles this. | **Low risk**: verify `pinned` default is `false` in builder. If ToolService constructor changes, update `setUp()`. |
| `service/forum/ForumPostServiceTest.java` | Constructor: `ForumPostService(postRepository, categoryRepository, postTagRepository, userRepository)` — 4 args match current. Pin/unpin added to same service, no constructor change. `ForumPost.builder()` doesn't set `pinned` — `@Builder.Default` should handle. | **Low risk**: verify default. |
| `service/video/VideoServiceTest.java` | Constructor: `VideoService(videoRepository, userRepository, videoLikeRepository, videoFavoriteRepository, videoStorageConfig)` — **note: test uses old VideoLikeRepository/VideoFavoriteRepository but current code uses UnifiedLikeRepository/UnifiedFavoriteRepository**. Test is already stale. Adding `sortBy` param to `getVideoList()` will change the method signature. | **Must update**: fix constructor args to match current code, add `sortBy` param to `getVideoList()` test calls, add `pinned`/`score` to Video builder in test data. |

### 4.2 Tests That Need New Test Cases

| Test File | New Test Cases Needed |
|---|---|
| `service/ToolServiceTest.java` | `pinTool_shouldSetPinnedTrue()`, `unpinTool_shouldSetPinnedFalse()`, `pinTool_shouldThrowForbiddenForNonAdmin()`, `getHotTop5_shouldReturn5Ids()` |
| `service/forum/ForumPostServiceTest.java` | `pinPost_shouldSetPinnedTrue()`, `unpinPost_shouldSetPinnedFalse()`, `getPostList_withSortByHot_shouldCallHotQuery()` |
| `service/video/VideoServiceTest.java` | `pinVideo_shouldSetPinnedTrue()`, `getVideoList_withSortByHot()`, `incrementViewCount_shouldUpdateScore()` |

### 4.3 Tests Unaffected

| Test File | Reason |
|---|---|
| `config/DataInitializerTest.java` | No sort/pin logic |
| `config/JwtAuthenticationFilterTest.java` | Auth filter, unrelated |
| `controller/OverviewControllerTest.java` | Overview ranking, not modified |
| `controller/ToolFileControllerTest.java` | File upload, unrelated |
| `model/ToolFileTest.java` | File model, unrelated |
| `repository/PostFavoriteRepositoryTest.java` | Favorites, unrelated |
| `repository/ToolFileRepositoryTest.java` | File repo, unrelated |
| `service/PostFavoriteServiceTest.java` | Favorites, unrelated |
| `service/ToolFileServiceTest.java` | File service, unrelated |
| `service/UnifiedCommentServiceTest.java` | Comments, unrelated |
| `service/UnifiedFavoriteServiceTest.java` | Favorites, unrelated |
| `service/UnifiedLikeServiceTest.java` | Likes, unrelated |
| `service/UserServiceTest.java` | User management, unrelated |
| `service/video/VideoInteractionServiceTest.java` | Interaction toggle, may need update if it directly sets viewCount/likeCount instead of calling increment methods |
| `service/video/VideoStreamTest.java` | Streaming, unrelated |

---

## 5. Risk Assessment

### L0 — Critical (blocks deployment)

| Risk | Mitigation |
|---|---|
| **Database migration failure**: Adding columns to 3 tables + index. If migration fails midway, tables may be in inconsistent state. | Use transactional DDL (MySQL supports it for InnoDB). Test migration on staging first. Provide rollback SQL (`ALTER TABLE ... DROP COLUMN`). |
| **Video.score is NULL for existing rows**: After adding `score` column with `DEFAULT 0`, existing videos have score=0 but actual viewCount/likeCount/commentCount may be non-zero. Scores will be inconsistent until next interaction event. | Acceptable per design doc: "video.score 默认 null，访问时自动计算". Alternatively, add a one-time `UPDATE video SET score = viewCount*1 + likeCount*3 + commentCount*5 WHERE score IS NULL` in migration. |

### L1 — High (degrades functionality)

| Risk | Mitigation |
|---|---|
| **VideoServiceTest already stale**: Test uses old `VideoLikeRepository`/`VideoFavoriteRepository` but current code uses `UnifiedLikeRepository`/`UnifiedFavoriteRepository`. Tests will not compile or will fail. | Fix constructor in `setUp()` as part of this change. This is pre-existing technical debt. |
| **`sortBy` default change for Tool**: Changing default from `"latest"` to `"hot"` alters existing behavior. Users accustomed to seeing newest-first will see hot-first. | This is intentional per design. Communicate in release notes. |
| **ForumPostService.getPostList() signature change**: Adding `sortBy` parameter changes the method signature. All callers (ForumPostController) must be updated. | Single caller, straightforward update. |
| **SecurityConfig misconfiguration**: If pin endpoints are not properly restricted, non-admin users could pin/unpin content. | Add explicit `.hasAnyRole("ADMIN","SUPER_ADMIN")` for pin endpoints. Test with non-admin JWT. |

### L2 — Medium (cosmetic / minor inconvenience)

| Risk | Mitigation |
|---|---|
| **Top5 cache staleness**: After a pin/unpin or new interaction, the top5 list may be briefly outdated until next page load. | Per design: "前端每次进入列表页重新请求 top5，延迟可接受". |
| **Pinned items overflow**: If admin pins more items than page size, all pinned items fill the first page. | Per design: "置顶项不会很多（管理员手动操作），风险极低". Add admin UI guidance. |
| **ForumPostDTO is a record**: Adding fields to a Java record changes its canonical constructor. All `new ForumPostDTO(...)` calls must add the new parameters. | Search for all `new ForumPostDTO(` usages. Currently only `ForumPostService.toDTO()` creates instances. |
| **OverviewServiceImpl video ranking**: Still uses `viewCount` instead of `score`. After Video gets a `score` field, the ranking methodology is inconsistent with Tool/ForumPost. | Not in scope for this change. File as follow-up task. |

---

## 6. Regression Suggestions

### 6.1 Backend Regression Tests

1. **GET /api/v1/tools?sortBy=hot** — verify pinned items appear first, then sorted by score DESC
2. **GET /api/v1/tools?sortBy=latest** — verify pure createdAt DESC, no pinned priority (unchanged from current behavior)
3. **GET /api/v1/tools/hot-top5** — verify returns exactly 5 IDs ordered by score DESC
4. **POST /api/v1/tools/{id}/pin** with ADMIN token — verify `pinned=true` persisted
5. **POST /api/v1/tools/{id}/pin** with USER token — verify 403 Forbidden
6. **DELETE /api/v1/tools/{id}/pin** — verify `pinned=false` persisted
7. **Same 6 tests for Forum and Video modules** (18 total endpoint tests)
8. **Video.incrementViewCount()** — verify `score` is updated after increment
9. **Video.getVideoList(sortBy=hot)** — verify score-based ordering with pinned priority
10. **SecurityConfig** — verify hot-top5 endpoints are public (no auth required)

### 6.2 Frontend Regression Tests (Manual)

1. **HomePage**: Default sort is "hot"; switching to "latest" re-fetches and removes pin/hot icons
2. **PostListPage**: SortTab appears; switching works; pin icon shows for pinned posts in hot mode
3. **VideoListPage**: SortTab appears; switching works; hot icon shows for top5 videos
4. **Admin pin action**: Admin sees pin button on cards; clicking toggles pin state; non-admin does not see pin button
5. **Hot icon**: Only visible in "hot" sort mode; matches top5 IDs from API

### 6.3 E2E Smoke Test

```
1. Start backend + frontend
2. Login as ADMIN
3. Visit HomePage → verify "hot" tab is active by default
4. Pin a tool → verify it appears at top in hot sort
5. Switch to "latest" → verify pin icon hidden, order is chronological
6. Visit PostListPage → repeat pin/sort checks
7. Visit VideoListPage → repeat pin/sort checks
8. Login as regular USER → verify pin buttons are not visible
9. Check /api/v1/tools/hot-top5 returns correct IDs
```

---

## 7. Layer Dependency Check

The `scripts/lint-arch.sh` script exists and checks backend package-layer dependencies.

**Anticipated lint impact**: None. The change adds fields to models (L1), queries to repositories (L2), logic to services (L3), and endpoints to controllers (L4). No cross-layer violations are introduced:

- `controller/` → calls `service/` methods (L4 → L3) — OK
- `service/` → calls `repository/` methods (L3 → L2) — OK
- `repository/` → references `model/` entities (L2 → L1) — OK
- `dto/` → pure data classes (L1) — no upward dependencies

**Note**: `config/SecurityConfig.java` (L0) will add request matchers for new endpoints. This is standard Spring Security configuration and does not violate layer rules (config is allowed to reference any layer).

Run before implementation:
```bash
bash scripts/lint-arch.sh
```

---

## 8. Checklist

- [ ] **Migration SQL**: Write `V4__add_sort_and_pin.sql` with `pinned` columns, `score` column (video), composite indexes
- [ ] **Migration rollback**: Write corresponding `DROP COLUMN` / `DROP INDEX` statements
- [ ] **Video entity**: Add `score` field + `updateScore()` method + wire into `incrementXxx()` methods
- [ ] **Tool entity**: Add `pinned` field with `@Builder.Default`
- [ ] **ForumPost entity**: Add `pinned` field with `@Builder.Default`
- [ ] **Video entity**: Add `pinned` field with `@Builder.Default`
- [ ] **ToolRepository**: Add hot-sort JPQL query + top5 query
- [ ] **ForumPostRepository**: Add hot-sort JPQL query + top5 query
- [ ] **VideoRepository**: Add hot-sort JPQL query + top5 query
- [ ] **ToolService**: Add `sortBy=hot` branch + `pinTool/unpinTool/getHotTop5` methods
- [ ] **ForumPostService**: Add `sortBy` param + `pinPost/unpinPost/getHotTop5` methods
- [ ] **VideoService**: Add `sortBy` param + `pinVideo/unpinVideo/getHotTop5` methods
- [ ] **ToolController**: Change default sortBy, add 3 new endpoints
- [ ] **ForumPostController**: Add `sortBy` param, add 3 new endpoints
- [ ] **VideoController**: Add `sortBy` param, add 3 new endpoints
- [ ] **ToolSummaryDTO**: Add `pinned` + `score` fields
- [ ] **ForumPostDTO**: Add `pinned` + `score` fields to record
- [ ] **VideoListItem**: Add `pinned` + `score` fields
- [ ] **SecurityConfig**: Add pin endpoint rules (ADMIN only) + top5 public rules
- [ ] **Frontend types**: Add `pinned?`, `score?` to ToolSummary, ForumPost, VideoListItem
- [ ] **Frontend services**: Add sortBy param, getHotTop5(), pinXxx(), unpinXxx() to tool/forum/video services
- [ ] **SortTab.vue**: Create shared sort tab component
- [ ] **PinIcon.vue**: Create shared pin icon component
- [ ] **HotIcon.vue**: Create shared hot icon component
- [ ] **HomePage.vue**: Integrate SortTab, hot-top5 fetch, PinIcon, HotIcon
- [ ] **PostListPage.vue**: Integrate SortTab, hot-top5 fetch, PinIcon, HotIcon, pass sortBy to API
- [ ] **VideoListPage.vue**: Integrate SortTab, hot-top5 fetch, PinIcon, HotIcon, pass sortBy to API
- [ ] **Fix VideoServiceTest**: Update stale constructor (UnifiedLikeRepository/UnifiedFavoriteRepository)
- [ ] **Update all 3 service tests**: Add pinned/score to test entity builders
- [ ] **Add new test cases**: pin/unpin authorization, hot sort ordering, top5 correctness
- [ ] **Run `bash scripts/lint-arch.sh`**: Verify no layer violations
- [ ] **Run full test suite**: `./gradlew test` — verify all pass
- [ ] **Manual E2E smoke test**: Verify sort switching, pin/unpin, icons across all 3 modules
