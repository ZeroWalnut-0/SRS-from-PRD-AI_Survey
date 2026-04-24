---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-DASH-002: 사용자별 설문 목록 및 요약 정보 조회 핸들러 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-DASH-002] 사용자별 설문 목록 및 요약 정보 조회 핸들러 구현
- 목적: 로그인한 사용자가 소유한 모든 설문 리스트와 각 설문의 핵심 지표(응답 수 등)를 효율적으로 조회하여 대시보드 메인 화면에 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-024`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/surveys/route.ts` (GET) 구현
- [ ] 세션 정보(`user_id`) 기반의 `Document` & `ParsedForm` Join 조회
- [ ] 각 설문별 최신 응답 수 집계 (Include count)
- [ ] 검색 및 필터링(상태별) 쿼리 파라미터 처리
- [ ] 페이지네이션 로직 구현 (Limit, Offset)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 본인 소유 설문만 조회
- Given: A 사용자와 B 사용자가 각각 설문을 생성함
- When: A 사용자로 로그인하여 목록을 조회함
- Then: B 사용자의 설문은 노출되지 않고 A 사용자의 설문만 정확히 나열되어야 한다.

Scenario 2: 응답 수 실시간 반영
- Given: 특정 설문에 10개의 응답이 존재함
- When: 대시보드 목록을 조회함
- Then: 해당 설문 행의 '응답 수' 컬럼에 10이 표시되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 목록 조회의 경우 사용자가 가장 자주 머무는 화면이므로 레이턴시 ≤ 200ms를 유지한다.
- 보안: 다른 사용자의 `form_id`로 접근 시 403 또는 404 처리를 철저히 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 사용자별 필터링이 적용된 설문 목록 API가 구현되었는가?
- [ ] 각 설문별 응답 수 합계가 정확히 반환되는가?
- [ ] 페이지네이션 및 상태 필터링이 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-003, #DB-004 (Document/Form 테이블)
- Blocks: #FE-DASH-001 (대시보드 UI 연동)
