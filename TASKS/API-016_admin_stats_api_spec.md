---
name: API Contract Task
about: API Endpoint 명세 및 계약 정의
title: "[API] API-016: GET /api/v1/admin/stats API 계약 정의"
labels: 'api-contract, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-016] Admin 도메인 API 계약 정의
- 목적: 백오피스 대시보드에서 활용할 전체 통계(총 매출, 총 응답 수, 완료율 등)를 한 번에 조회하는 API 명세를 정의한다.

## :link: References (Spec & Context)
- API 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `GET /api/v1/admin/stats` 엔드포인트 규격 확정
- [ ] 권한 검증: Authorization 헤더 기반 어드민(Admin) Role 필수 요구 조건 기재

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 어드민 권한 접근
- Given: Valid Admin JWT
- When: API 요청
- Then: 통계 JSON 객체가 200 OK와 함께 리턴된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 일반 유저 토큰으로 요청 시 403 Forbidden 리턴 명세 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-010, #BE-RL-002
- Blocks: #BE-ADMIN-001
