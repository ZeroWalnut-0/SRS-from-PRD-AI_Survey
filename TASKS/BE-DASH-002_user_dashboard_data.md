---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-DASH-002: 사용자별 대시보드 데이터 조회"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-DASH-002] 사용자별 대시보드 데이터 조회
- 목적: 로그인한 유저의 메인 홈 화면 구성을 위해, 해당 유저가 생성한 설문지 목록과 각 설문의 상태 요약을 원스톱으로 조회한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L276)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] API Route Handler `/app/api/v1/dashboard/surveys/route.ts` 구현
- [ ] 세션 유저 ID를 기준으로 `PARSED_FORM` 목록 필터링 쿼리
- [ ] 각 설문별 총 응답 수 Join 연산

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 생성 이력이 있는 유저의 조회
- Given: 유효한 로그인 세션이 활성화되어 있음
- When: 대시보드 데이터 API가 호출됨
- Then: 본인이 생성한 설문지 정보 리스트를 200 OK로 반환한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 타인의 `user_id`로 생성된 설문 목록이 노출되지 않도록 철저한 Scope 격리

## :checkered_flag: Definition of Done (DoD)
- [ ] 권한이 없는 비로그인 요청 시 401 Unauthorized 응답 검증

## :construction: Dependencies & Blockers
- Depends on: #DB-002, #DB-004
- Blocks: #FE-DASH-001
