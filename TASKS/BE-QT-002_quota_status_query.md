---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-002: Quota 충족 상태 조회 Route Handler 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-002] Quota 충족 상태 조회 Route Handler 구현
- 목적: 현재 진행 중인 조사의 쿼터별 수집 현황(현재수/목표수)을 DB에서 집계하여 대시보드용 데이터로 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#9`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-011_quota_status_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-011_quota_status_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/quotas/[quota_id]/status/route.ts` 구현
- [ ] `QUOTA_CELL` 테이블에서 해당 `quota_id`에 속한 모든 레코드 조회
- [ ] 응답 데이터 구성: 각 셀의 `group_key`, `target_count`, `current_count`, `is_full` 포함
- [ ] 캐시 활용 검토: 빈번한 조회를 대비해 짧은 주기(예: 5초)의 SWR 또는 캐시 적용 검토

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 현황 데이터 반환
- Given: 유효한 `quota_id`로 요청함
- When: 핸들러가 실행됨
- Then: 200 OK와 함께 현재까지 수집된 모든 쿼터 셀의 카운트 정보가 배열 형태로 반환되어야 한다.

Scenario 2: 존재하지 않는 쿼터 조회
- Given: 삭제되었거나 잘못된 `quota_id`
- When: 조회를 시도함
- Then: 404 Not Found를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 대시보드 폴링을 지원하기 위해 쿼리 속도 ≤ 200ms 유지.
- 부하 관리: 대량의 응답이 수집 중일 때 조회 쿼리가 인덱스를 타도록 최적화한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-011` 규격에 맞는 응답을 반환하는가?
- [ ] DB 조회 로직이 정확하며 최신 카운트를 반영하는가?
- [ ] 예외 케이스(404 등) 처리가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-008 (QUOTA_CELL), #API-011 (Quota Status DTO)
- Blocks: #FE-QT-002 (쿼터 대시보드 연동)
