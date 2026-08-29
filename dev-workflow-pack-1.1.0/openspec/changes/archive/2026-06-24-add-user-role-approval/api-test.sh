#!/bin/bash
# API Test Script for add-user-role-approval change
# Based on specs/**/*.md scenarios

BASE="http://localhost:8082"
PASS=0
FAIL=0
SKIP=0
RESULTS=""
FAILED_DETAILS=""

run_test() {
  local tc_id=$1 tc_name=$2 method=$3 url=$4 token=$5 body=$6 expect_code=$7 expect_contains=$8

  local auth_arg=""
  [ -n "$token" ] && auth_arg="-H \"Authorization: Bearer $token\""
  local body_arg=""
  [ -n "$body" ] && body_arg="-H \"Content-Type: application/json\" -d '$body'"

  local raw
  raw=$(eval curl -s -w '"\n%{http_code}"' -X "$method" "\"$url\"" $auth_arg $body_arg 2>&1)

  local http_code=$(echo "$raw" | tail -1 | tr -d '"')
  local body_text=$(echo "$raw" | sed '$d')

  local status="PASS"
  [ "$http_code" != "$expect_code" ] && status="FAIL"
  if [ -n "$expect_contains" ] && ! echo "$body_text" | grep -qi "$expect_contains"; then
    status="FAIL"
  fi

  if [ "$status" == "PASS" ]; then
    PASS=$((PASS+1))
    echo "✅ $tc_id: $tc_name (expect=$expect_code actual=$http_code)"
  else
    FAIL=$((FAIL+1))
    echo "❌ $tc_id: $tc_name (expect=$expect_code actual=$http_code)"
    echo "   Response: ${body_text:0:300}"
    FAILED_DETAILS="$FAILED_DETAILS\n### $tc_id: $tc_name\n- Request: $method $url\n- Expected: $expect_code\n- Actual: $http_code\n- Response: ${body_text:0:300}\n"
  fi
  RESULTS="$RESULTS\n| $tc_id | $tc_name | $status | expect=$expect_code actual=$http_code |"
}

get_token() {
  curl -s -X POST "$BASE/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$1\",\"password\":\"$2\"}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('accessToken',''))" 2>/dev/null
}

echo "=========================================="
echo "  API Test: add-user-role-approval"
echo "=========================================="
echo ""

# === Step 1: Super admin login ===
echo "--- Preparing test accounts ---"
SUPER_ADMIN_TOKEN=$(get_token "admin" "Cloud@1234")
if [ -z "$SUPER_ADMIN_TOKEN" ]; then
  echo "FATAL: Super admin login failed."
  exit 1
fi
echo "Super admin logged in."

# === Step 2: Create test users (username max 20 chars) ===
TS=$(date +%s | tail -c 7)  # last 6 digits
OWNER_USER="tow_$TS"        # tow_123456 = 10 chars
USER_B_USER="tub_$TS"
ADMIN_USER="tad_$TS"
REJECT_USER="trj_$TS"
DELETE_USER="tdl_$TS"
NICK_O="测创建"
NICK_B="测用户B"
NICK_A="测管理"
NICK_R="测拒绝"
NICK_D="测删除"
PASSWD="test123456"

# Register owner (USER, ACTIVE immediately)
curl -s -X POST "$BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$OWNER_USER\",\"nickname\":\"$NICK_O\",\"password\":\"$PASSWD\"}" > /dev/null

# Register user B (USER)
curl -s -X POST "$BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USER_B_USER\",\"nickname\":\"$NICK_B\",\"password\":\"$PASSWD\"}" > /dev/null

# Register admin (ADMIN, PENDING)
curl -s -X POST "$BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$ADMIN_USER\",\"nickname\":\"$NICK_A\",\"password\":\"$PASSWD\",\"role\":\"ADMIN\"}" > /dev/null

# Register reject target (ADMIN, PENDING)
curl -s -X POST "$BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$REJECT_USER\",\"nickname\":\"$NICK_R\",\"password\":\"$PASSWD\",\"role\":\"ADMIN\"}" > /dev/null

echo "Test users registered."

# === Step 3: Get tokens ===
OWNER_TOKEN=$(get_token "$OWNER_USER" "$PASSWD")
USER_B_TOKEN=$(get_token "$USER_B_USER" "$PASSWD")
echo "Owner token: ${OWNER_TOKEN:0:20}..."
echo "UserB token: ${USER_B_TOKEN:0:20}..."

# === Step 4: Approve admin via super admin ===
# pending-users returns data as a list
ADMIN_USER_ID=$(curl -s "$BASE/api/v1/admin/pending-users" \
  -H "Authorization: Bearer $SUPER_ADMIN_TOKEN" \
  | python3 -c "
import sys,json
d=json.load(sys.stdin)
data=d.get('data',[])
if isinstance(data,list):
    for u in data:
        if u.get('username')=='$ADMIN_USER': print(u['id']); break
elif isinstance(data,dict):
    for u in data.get('content',[]):
        if u.get('username')=='$ADMIN_USER': print(u['id']); break
" 2>/dev/null)

if [ -n "$ADMIN_USER_ID" ]; then
  curl -s -X PUT "$BASE/api/v1/admin/approve/$ADMIN_USER_ID" \
    -H "Authorization: Bearer $SUPER_ADMIN_TOKEN" > /dev/null
  ADMIN_TOKEN=$(get_token "$ADMIN_USER" "$PASSWD")
  echo "Admin approved (id=$ADMIN_USER_ID), token: ${ADMIN_TOKEN:0:20}..."
else
  echo "WARNING: Could not find pending admin. Some tests will skip."
fi

# Get reject user ID
REJECT_ID=$(curl -s "$BASE/api/v1/admin/pending-users" \
  -H "Authorization: Bearer $SUPER_ADMIN_TOKEN" \
  | python3 -c "
import sys,json
d=json.load(sys.stdin)
data=d.get('data',[])
if isinstance(data,list):
    for u in data:
        if u.get('username')=='$REJECT_USER': print(u['id']); break
elif isinstance(data,dict):
    for u in data.get('content',[]):
        if u.get('username')=='$REJECT_USER': print(u['id']); break
" 2>/dev/null)

echo ""
echo "--- Running Tests ---"
echo ""

# ============================================================
# SPEC: auth/spec.md - 用户认证
# ============================================================

run_test "TC-001" "用户使用用户名登录" \
  "POST" "$BASE/api/v1/auth/login" \
  "" '{"username":"'"$OWNER_USER"'","password":"'"$PASSWD"'"}' "200" "accessToken"

run_test "TC-002" "登录密码错误返回401" \
  "POST" "$BASE/api/v1/auth/login" \
  "" '{"username":"'"$OWNER_USER"'","password":"wrongpassword"}' "401" ""

run_test "TC-003" "登录用户不存在返回401" \
  "POST" "$BASE/api/v1/auth/login" \
  "" '{"username":"nonexistent_xyz","password":"password123"}' "401" ""

run_test "TC-004" "注册密码长度不足返回400" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"shortpw_'$TS'","nickname":"短密码","password":"12345"}' "400" ""

run_test "TC-005" "普通用户注册成功返回201" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"newu_'$TS'","nickname":"新用户A","password":"password123"}' "201" "accessToken"

run_test "TC-006" "管理员注册成功进入待审批(PENDING)" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"newa_'$TS'","nickname":"新管理","password":"password123","role":"ADMIN"}' "201" "PENDING"

run_test "TC-007" "注册用户名已存在返回409" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"'"$OWNER_USER"'","nickname":"重复用户","password":"password123"}' "409" ""

run_test "TC-008" "PENDING状态用户登录被拒绝返回403" \
  "POST" "$BASE/api/v1/auth/login" \
  "" '{"username":"newa_'"$TS"'","password":"password123"}' "403" ""

# ============================================================
# SPEC: auth-api/spec.md - 昵称注册 & 管理端API鉴权
# ============================================================

run_test "TC-009" "注册昵称重复返回409" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"dupn_'"$TS"'","nickname":"'"$NICK_O"'","password":"password123"}' "409" ""

run_test "TC-010" "注册昵称长度不足返回400" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"sn_'"$TS"'","nickname":"A","password":"password123"}' "400" ""

run_test "TC-011" "注册SUPER_ADMIN角色被拒绝返回400" \
  "POST" "$BASE/api/v1/auth/register" \
  "" '{"username":"sup_'"$TS"'","nickname":"超管","password":"password123","role":"SUPER_ADMIN"}' "400" ""

run_test "TC-012" "获取当前用户信息含nickname和role" \
  "GET" "$BASE/api/v1/users/me" \
  "$OWNER_TOKEN" "" "200" "nickname"

run_test "TC-013" "未认证访问管理接口返回403" \
  "GET" "$BASE/api/v1/admin/users" \
  "" "" "403" ""

run_test "TC-014" "普通用户访问管理接口返回403" \
  "GET" "$BASE/api/v1/admin/users" \
  "$OWNER_TOKEN" "" "403" ""

# ============================================================
# SPEC: admin-approval/spec.md
# ============================================================

run_test "TC-015" "超级管理员查看待审批列表" \
  "GET" "$BASE/api/v1/admin/pending-users" \
  "$SUPER_ADMIN_TOKEN" "" "200" ""

run_test "TC-016" "普通用户访问待审批列表返回403" \
  "GET" "$BASE/api/v1/admin/pending-users" \
  "$OWNER_TOKEN" "" "403" ""

if [ -n "$ADMIN_TOKEN" ]; then
  run_test "TC-017" "管理员访问待审批列表返回403" \
    "GET" "$BASE/api/v1/admin/pending-users" \
    "$ADMIN_TOKEN" "" "403" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-017 skipped (no admin token)"
  RESULTS="$RESULTS\n| TC-017 | 管理员访问待审批列表返回403 | SKIP | no admin token |"
fi

run_test "TC-018" "审批不存在的用户返回404" \
  "PUT" "$BASE/api/v1/admin/approve/999999" \
  "$SUPER_ADMIN_TOKEN" "" "404" ""

if [ -n "$ADMIN_TOKEN" ]; then
  run_test "TC-019" "管理员执行审批操作返回403" \
    "PUT" "$BASE/api/v1/admin/approve/999999" \
    "$ADMIN_TOKEN" "" "403" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-019 skipped (no admin token)"
  RESULTS="$RESULTS\n| TC-019 | 管理员执行审批操作返回403 | SKIP | no admin token |"
fi

run_test "TC-020" "对ACTIVE用户执行审批返回400" \
  "PUT" "$BASE/api/v1/admin/approve/$ADMIN_USER_ID" \
  "$SUPER_ADMIN_TOKEN" "" "400" ""

if [ -n "$REJECT_ID" ]; then
  run_test "TC-021" "超级管理员拒绝审批" \
    "PUT" "$BASE/api/v1/admin/reject/$REJECT_ID" \
    "$SUPER_ADMIN_TOKEN" "" "200" ""

  run_test "TC-022" "拒绝后用户登录返回403" \
    "POST" "$BASE/api/v1/auth/login" \
    "" '{"username":"'"$REJECT_USER"'","password":"'"$PASSWD"'"}' "403" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-021/022 skipped (no reject user)"
  RESULTS="$RESULTS\n| TC-021 | 超级管理员拒绝审批 | SKIP | no reject user |"
  RESULTS="$RESULTS\n| TC-022 | 拒绝后用户登录返回403 | SKIP | no reject user |"
fi

# ============================================================
# SPEC: admin-user-management/spec.md
# ============================================================

if [ -n "$ADMIN_TOKEN" ]; then
  run_test "TC-023" "管理员查看用户列表" \
    "GET" "$BASE/api/v1/admin/users?page=0&size=10" \
    "$ADMIN_TOKEN" "" "200" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-023 skipped"
  RESULTS="$RESULTS\n| TC-023 | 管理员查看用户列表 | SKIP | no admin token |"
fi

run_test "TC-024" "超级管理员查看用户列表" \
  "GET" "$BASE/api/v1/admin/users?page=0&size=10" \
  "$SUPER_ADMIN_TOKEN" "" "200" ""

run_test "TC-025" "按角色筛选用户(ADMIN)" \
  "GET" "$BASE/api/v1/admin/users?role=ADMIN" \
  "$SUPER_ADMIN_TOKEN" "" "200" ""

run_test "TC-026" "按状态筛选用户(PENDING)" \
  "GET" "$BASE/api/v1/admin/users?status=PENDING" \
  "$SUPER_ADMIN_TOKEN" "" "200" ""

if [ -n "$ADMIN_TOKEN" ]; then
  run_test "TC-027" "管理员封禁用户返回403" \
    "PUT" "$BASE/api/v1/admin/users/$ADMIN_USER_ID/status" \
    "$ADMIN_TOKEN" '{"status":"DISABLED"}' "403" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-027 skipped"
  RESULTS="$RESULTS\n| TC-027 | 管理员封禁用户返回403 | SKIP | no admin token |"
fi

run_test "TC-028" "超级管理员封禁普通用户" \
  "PUT" "$BASE/api/v1/admin/users/$ADMIN_USER_ID/status" \
  "$SUPER_ADMIN_TOKEN" '{"status":"DISABLED"}' "200" ""

run_test "TC-029" "封禁后用户登录返回403" \
  "POST" "$BASE/api/v1/auth/login" \
  "" '{"username":"'"$ADMIN_USER"'","password":"'"$PASSWD"'"}' "403" ""

run_test "TC-030" "超级管理员解禁用户" \
  "PUT" "$BASE/api/v1/admin/users/$ADMIN_USER_ID/status" \
  "$SUPER_ADMIN_TOKEN" '{"status":"ACTIVE"}' "200" ""

run_test "TC-031" "解禁后用户可登录" \
  "POST" "$BASE/api/v1/auth/login" \
  "" '{"username":"'"$ADMIN_USER"'","password":"'"$PASSWD"'"}' "200" "accessToken"

run_test "TC-032" "封禁不存在的用户返回404" \
  "PUT" "$BASE/api/v1/admin/users/999999/status" \
  "$SUPER_ADMIN_TOKEN" '{"status":"DISABLED"}' "404" ""

if [ -n "$ADMIN_TOKEN" ]; then
  run_test "TC-033" "管理员删除用户返回403" \
    "DELETE" "$BASE/api/v1/admin/users/999999" \
    "$ADMIN_TOKEN" "" "403" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-033 skipped"
  RESULTS="$RESULTS\n| TC-033 | 管理员删除用户返回403 | SKIP | no admin token |"
fi

run_test "TC-034" "删除不存在的用户返回404" \
  "DELETE" "$BASE/api/v1/admin/users/999999" \
  "$SUPER_ADMIN_TOKEN" "" "404" ""

# Create a user to delete
curl -s -X POST "$BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$DELETE_USER\",\"nickname\":\"$NICK_D\",\"password\":\"$PASSWD\"}" > /dev/null

DELETE_USER_ID=$(curl -s "$BASE/api/v1/admin/users?keyword=$DELETE_USER" \
  -H "Authorization: Bearer $SUPER_ADMIN_TOKEN" \
  | python3 -c "
import sys,json
d=json.load(sys.stdin)
data=d.get('data',{})
content=data.get('content',data) if isinstance(data,dict) else data
if isinstance(content,list):
    for u in content:
        if u.get('username')=='$DELETE_USER': print(u['id']); break
" 2>/dev/null)

if [ -n "$DELETE_USER_ID" ]; then
  run_test "TC-035" "超级管理员删除普通用户" \
    "DELETE" "$BASE/api/v1/admin/users/$DELETE_USER_ID" \
    "$SUPER_ADMIN_TOKEN" "" "200" ""

  run_test "TC-036" "删除后username可重新注册" \
    "POST" "$BASE/api/v1/auth/register" \
    "" "{\"username\":\"$DELETE_USER\",\"nickname\":\"重新注册\",\"password\":\"$PASSWD\"}" "201" ""
else
  SKIP=$((SKIP+1)); echo "⏭️ TC-035/036 skipped"
  RESULTS="$RESULTS\n| TC-035 | 超级管理员删除普通用户 | SKIP | no delete user |"
  RESULTS="$RESULTS\n| TC-036 | 删除后username可重新注册 | SKIP | no delete user |"
fi

# ============================================================
# SPEC: user-role/spec.md - JWT过滤器
# ============================================================

run_test "TC-037" "ACTIVE用户请求受保护接口成功" \
  "GET" "$BASE/api/v1/users/me" \
  "$OWNER_TOKEN" "" "200" ""

# ============================================================
# Summary
# ============================================================
echo ""
echo "=========================================="
echo "  Test Summary"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
echo "  Skipped: $SKIP"
echo "  Total:  $((PASS+FAIL+SKIP))"
echo "=========================================="
echo ""
echo "| TC ID | Test Case | Status | Notes |"
echo "|-------|-----------|--------|-------|"
echo -e "$RESULTS"

if [ -n "$FAILED_DETAILS" ]; then
  echo ""
  echo "=== FAILED CASES DETAIL ==="
  echo -e "$FAILED_DETAILS"
fi
