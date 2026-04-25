---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-003: 쿼터 풀(Quota Full) 상태 감지 시 진입 차단 및 안내 모달"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-003] 쿼터 풀 상태 감지 시 진입 차단 및 안내 모달
- 목적: 특정 인구통계학적 쿼터가 이미 가득 찬 경우, 해당 조건의 응답자 진입을 조기에 차단하여 무의미한 응답 수집을 방지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L514)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 설문 진입 시 성별/연령 스크리닝 질문 우선 렌더링
- [ ] 선택된 값에 따른 쿼터 마감 여부 클라이언트 체크 및 차단 페이지 노출

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 마감된 쿼터 대상자 차단
- Given: '20대 여성' 쿼터 마감(Quota Full) 상태
- When: 응답자가 20대 여성으로 체크하고 다음 버튼을 누름
- Then: "죄송합니다. 해당 할당의 모집이 마감되었습니다." 페이지로 즉시 라우팅된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 차단 대상자의 추가 문항 노출 차단 검증

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-007
- Blocks: None
