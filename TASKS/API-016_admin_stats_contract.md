---
name: API/Contract Task
about: 관리자 통계 조회 API 명세
title: "[API Spec] API-016: 관리자용 전체 통계 조회 API 계약 정의"
labels: 'api, admin, contract'
assignees: ''
---

## :dart: Summary
- 목적: 운영자가 시스템 전반의 성과(파싱 완료율, 결제 전환율, 사용자 증가 추이)를 파악할 수 있는 통계 데이터를 제공하는 API 규격을 정의한다.

## :link: References (Spec & Context)
- SRS 문서: `§4.2.8 REQ-NF-033 ~ 037`
- 엔드포인트: `GET /api/v1/admin/stats`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `AdminStatsResponse` DTO 정의:
    - `total_documents`: 전체 업로드 문서 수
    - `parsing_success_rate`: 파싱 성공률 (%)
    - `total_payments`: 총 결제 횟수 및 금액
    - `conversion_rate`: 파싱 대비 결제 전환율 (%)
    - `daily_stats`: 일자별 추이 리스트 (date, count, revenue)
- [ ] 권한 체크 로직 포함: `role === 'ADMIN'` 필터링 명시

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 관리자 권한으로 통계 조회
- Given: 관리자 계정으로 인증된 상태
- When: `GET /api/v1/admin/stats` 호출 시
- Then: 200 OK와 함께 정의된 통계 스키마가 반환되어야 한다.

Scenario 2: 일반 사용자 권한으로 통계 조회
- Given: 일반 사용자 계정으로 인증된 상태
- When: `GET /api/v1/admin/stats` 호출 시
- Then: 403 Forbidden 에러가 반환되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 관리자 전용 API는 별도의 미들웨어에서 `ip_hash` 및 `role` 검증 수행.
- 성능: 통계 연산은 DB 부하를 고려하여 Supabase View 또는 캐싱 적용 검토.

## :checkered_flag: Definition of Done (DoD)
- [ ] API Request/Response DTO 타입이 정의되었는가?
- [ ] 권한 위반 시의 에러 응답 규약이 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: `DB-010` (Audit Log)
- Blocks: `BE-ADMIN-001`, `FE-ADMIN-002`
