---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-008: 의심 응답 데이터 패치 및 상태 복원(ACTIVE) API 연동"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-008] 의심 응답 데이터 패치 및 상태 복원 API 연동
- 목적: AI Data Bouncer가 걸러낸 무성의 응답 중, 정상적인 응답으로 판명된 건을 수동으로 정상 응답 풀에 복원시키는 관리자 기능을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L492)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 의심 응답(Bouncer 감지) 리스트 그리드 UI 구현
- [ ] 각 행(Row) 우측에 '복원하기' 액션 버튼 추가 및 API 바인딩

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 응답 복원 성공
- Given: AI에 의해 제외된 ID `resp_999`
- When: '복원하기' 클릭
- Then: 해당 행이 목록에서 사라지며 정상 응답 카운트에 합산된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 복원 성공 안내 토스트 메시지 노출

## :construction: Dependencies & Blockers
- Depends on: #FE-ADMIN-001, #API-004
- Blocks: None
