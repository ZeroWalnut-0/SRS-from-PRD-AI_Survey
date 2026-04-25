---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-RT-002: 조건별 리다이렉트 경로 검증"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-RT-002] 조건별 리다이렉트 경로 검증
- 목적: 설문 종료 시 유저 상태(완료, 스크린아웃, 쿼터풀)에 따라 정확한 패널사 URL로 302 리다이렉트가 분기되는지 테스트한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.4.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L377)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 세 가지 시나리오의 응답자 데이터 셋업
- [ ] `/api/v1/routing/redirect/{resp_id}` 호출 후 Location 헤더 값 검사

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 스크린아웃 처리
- Given: 불성실 응답 판정자
- When: 리다이렉트 API 호출
- Then: 패널사의 `screenout_url`로 이동한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] HTTP Status 302 Found 응답 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-RT-002, #API-013
- Blocks: None
