---
name: Test Task
about: 관리자 접근 권한 검증 테스트
title: "[Test] TEST-ADMIN-001: 관리자 전용 대시보드 접근 권한 및 통계 조회 보안 테스트"
labels: 'test, admin, security'
assignees: ''
---

## :dart: Summary
- 목적: 관리자 전용 페이지 및 API가 일반 사용자에게 노출되거나 호출되지 않도록 RBAC(Role Based Access Control) 체계의 무결성을 검증한다.

## :link: References (Spec & Context)
- SRS 문서: `§1.3 (RBAC), §4.2.3 REQ-NF-019`
- 관련 태스크: `FE-ADMIN-001`, `BE-ADMIN-001`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] [Unit Test] `role` 필터링 로직 검증 (ADMIN vs USER)
- [ ] [Integration Test] 일반 사용자 토큰으로 관리자 API 호출 시 403 반환 확인
- [ ] [E2E Test] 일반 사용자가 브라우저 주소창에 `/admin` 직접 입력 시 리다이렉트 여부 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 권한 위반 차단
- Given: `role`이 'USER'인 세션으로 로그인함
- When: `/api/v1/admin/stats` 엔드포인트에 요청을 보냄
- Then: 서버는 반드시 403 Forbidden 상태 코드를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `ip_hash` 기반 차단이 적용된 경우, 관리자 허용 IP 리스트와 대조하는 로직도 함께 검증.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 비관리자 접근 시나리오가 성공적으로 차단되는가?
- [ ] 보안 취약점(ID 변조 등)을 통한 접근 시도가 실패하는가?

## :construction: Dependencies & Blockers
- Depends on: `BE-ADMIN-001`, `FE-ADMIN-001`
- Blocks: None
