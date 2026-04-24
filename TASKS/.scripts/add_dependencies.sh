#!/bin/bash
# Batch add Dependencies & Blockers section to TEST/NFR files missing it
TASKS_DIR="/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS"

add_deps() {
  local file="$1"
  local deps="$2"
  local blocks="$3"
  # Only add if file exists and doesn't already have Dependencies section
  if [ -f "$file" ] && ! grep -q ":construction: Dependencies" "$file"; then
    printf "\n## :construction: Dependencies & Blockers\n- Depends on: %s\n- Blocks: %s\n" "$deps" "$blocks" >> "$file"
    echo "Updated: $(basename "$file")"
  fi
}

# TEST-PARSE files
add_deps "$TASKS_DIR/TEST-PARSE-002_file_validation_test.md" "#BE-PARSE-001 (서버 검증)" "None"
add_deps "$TASKS_DIR/TEST-PARSE-003_hwpx_conversion_test.md" "#FE-PARSE-003 (HWPX 안내 모달), #BE-PARSE-001" "None"
add_deps "$TASKS_DIR/TEST-PARSE-004_parsing_latency_test.md" "#BE-PARSE-005 (AI SDK 연동)" "None"
add_deps "$TASKS_DIR/TEST-PARSE-005_fallback_path_test.md" "#BE-PARSE-002, #BE-PARSE-003, #BE-PARSE-004" "None"
add_deps "$TASKS_DIR/TEST-PARSE-006_skip_elements_notice_test.md" "#BE-PARSE-006 (스킵 요소 기록)" "None"
add_deps "$TASKS_DIR/TEST-PARSE-007_hwp_convert_guide_test.md" "#FE-PARSE-003, #BE-PARSE-001" "None"
add_deps "$TASKS_DIR/TEST-PARSE-008_rate_limit_blocking_test.md" "#BE-RL-001 (한도 미들웨어)" "None"
add_deps "$TASKS_DIR/TEST-PARSE-009_file_hash_cache_test.md" "#BE-PARSE-010 (파일 해시 캐시)" "None"

# TEST-PAY files
add_deps "$TASKS_DIR/TEST-PAY-002_zip_packaging_test.md" "#BE-PAY-003 (ZIP 컴파일 로직)" "None"
add_deps "$TASKS_DIR/TEST-PAY-003_download_access_test.md" "#BE-PAY-004 (서명 URL), #BE-PAY-005 (다운로드 핸들러)" "None"
add_deps "$TASKS_DIR/TEST-PAY-004_payment_callback_flow_test.md" "#BE-PAY-002 (결제 콜백), #BE-PAY-004" "None"
add_deps "$TASKS_DIR/TEST-PAY-005_payment_failure_blocking_test.md" "#BE-PAY-002, #BE-PAY-005" "None"
add_deps "$TASKS_DIR/TEST-PAY-006_missing_value_zero_tolerance_test.md" "#BE-PAY-006 (결측치 검증)" "None"
add_deps "$TASKS_DIR/TEST-PAY-007_paywall_preview_assets_test.md" "#FE-PAY-003 (Paywall 미리보기)" "None"

# TEST-QT files
add_deps "$TASKS_DIR/TEST-QT-001_quota_matrix_test.md" "#BE-QT-001 (쿼터 설정)" "None"
add_deps "$TASKS_DIR/TEST-QT-003_atomic_concurrency_test.md" "#BE-QT-003 (원자적 증가), #DB-012 (RPC)" "None"
add_deps "$TASKS_DIR/TEST-QT-004_quota_latency_alert_test.md" "#BE-QT-005 (레이턴시 모니터링)" "None"
add_deps "$TASKS_DIR/TEST-QT-005_quota_full_slack_alert_test.md" "#BE-QT-004 (Slack 알림)" "None"

# TEST-RT files
add_deps "$TASKS_DIR/TEST-RT-001_panel_postback_test.md" "#BE-RT-001 (포스트백 등록)" "None"
add_deps "$TASKS_DIR/TEST-RT-002_redirect_parameter_test.md" "#BE-RT-002 (리다이렉트 핸들러)" "None"

# TEST-RET files
add_deps "$TASKS_DIR/TEST-RET-001_automatic_cleanup_test.md" "#BE-RET-001 (삭제 스케줄러)" "None"
add_deps "$TASKS_DIR/TEST-RET-002_security_encryption_test.md" "#BE-RET-001, #NFR-SEC-001 (TLS)" "None"

# TEST-WM files
add_deps "$TASKS_DIR/TEST-WM-001_watermark_rendering_test.md" "#FE-WM-001 (워터마크 배너)" "None"
add_deps "$TASKS_DIR/TEST-WM-002_watermark_viral_flow_test.md" "#FE-WM-002 (워터마크 리다이렉션)" "None"

# TEST-FORM files
add_deps "$TASKS_DIR/TEST-FORM-001_editor_dnd_test.md" "#FE-FORM-001 (에디터 레이아웃)" "None"
add_deps "$TASKS_DIR/TEST-FORM-002_logic_branch_test.md" "#FE-FORM-004 (스킵 로직), #BE-FORM-002" "None"
add_deps "$TASKS_DIR/TEST-FORM-003_mobile_rendering_test.md" "#FE-FORM-007 (모바일 폼 렌더링)" "None"
add_deps "$TASKS_DIR/TEST-FORM-004_submission_integrity_test.md" "#BE-FORM-004 (응답 제출 핸들러)" "None"

# TEST-ADMIN
add_deps "$TASKS_DIR/TEST-ADMIN-001_admin_access_test.md" "#BE-RL-002 (RBAC), #FE-ADMIN-001 (관리자 레이아웃)" "None"

# NFR files
add_deps "$TASKS_DIR/NFR-COST-002_cloud_budget_alert_setup.md" "#NFR-INFRA-003 (Vercel CI/CD), #NFR-INFRA-004 (Supabase 초기화)" "None"
add_deps "$TASKS_DIR/NFR-PERF-003_quota_latency_benchmark.md" "#BE-QT-003 (원자적 쿼터 증가)" "None"
add_deps "$TASKS_DIR/NFR-SEC-002_postgresql_encryption_check.md" "#DB-001 (Prisma 초기화), #NFR-INFRA-004 (Supabase)" "None"

echo "--- Done: Dependencies batch update complete ---"
