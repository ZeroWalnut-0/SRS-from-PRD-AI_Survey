---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-002: 쿼터 상태 조회 API 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-002] 쿼터 상태 조회 API (`GET /api/v1/quotas/{quota_id}/status`)
- 목적: 특정 쿼터의 달성 현황(목표치 대비 현재 응답 수 및 마감 여부)을 실시간으로 조회한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L529)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#9`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L719)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] API Route Handler 구현 (`/app/api/v1/quotas/[quota_id]/status/route.ts`)
- [ ] `QUOTA_CELL` 테이블의 셀 그룹별 통계 조회
- [ ] DTO 매핑 및 JSON 응답 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 상태 조회 성공
- Given: 존재하는 `quota_id`로 요청함
- When: GET 요청이 실행됨
- Then: 200 OK와 함께 셀별 정보가 반환된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 응답시간 p95 ≤ 300ms

## :checkered_flag: Definition of Done (DoD)
- [ ] 반환된 누적 수치와 DB 원본 값의 일치성 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-001
- Blocks: #FE-QT-002
