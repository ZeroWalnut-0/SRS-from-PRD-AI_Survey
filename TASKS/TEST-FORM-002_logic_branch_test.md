---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-FORM-002: 문항 스킵 로직(Skip Logic) 분기 검증 테스트"
labels: 'test, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-FORM-002] 문항 스킵 로직(Skip Logic) 분기 검증 테스트
- 목적: 설정된 스킵 로직에 따라 실제 설문 응답 시 문항 건너뛰기 또는 스크린아웃 처리가 정확히 수행되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #FE-FORM-004 (스킵 로직 UI), #FE-FORM-007 (모바일 폼)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 단순 문항 점프(A응답 시 3번으로 이동) 확인
- [ ] 시나리오 2: 스크린아웃 로직(B응답 시 종료) 확인
- [ ] 시나리오 3: 복합 조건 로직(A이면서 B일 때 이동) 확인
- [ ] 시나리오 4: 로직에 의해 건너뛴 문항의 데이터가 `null`로 전송되는지 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 1번 문항에서 '아니오' 선택 시 5번으로 이동하도록 로직이 설정됨
- When: 실제 모바일 폼에서 '아니오'를 선택하고 [다음]을 클릭함
- Then: 2, 3, 4번 문항을 건너뛰고 즉시 5번 문항이 화면에 나타나야 한다.

## :gear: Technical Constraints
- 도구: Playwright 또는 Cypress E2E 테스트

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 분기 시나리오에 대해 문항 이동이 정확히 수행되는가?
- [ ] 스크린아웃 시 결과 페이지 또는 외부 URL로의 이동이 정상적인가?
- [ ] 건너뛴 문항의 응답값이 DB에 불필요하게 저장되지 않는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-004 (스킵 로직), #BE-FORM-002
- Blocks: None
