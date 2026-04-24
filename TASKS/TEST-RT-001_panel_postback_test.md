---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-RT-001: 패널사 포스트백(Postback) 성공 연동 테스트"
labels: 'test, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-RT-001] 패널사 포스트백(Postback) 성공 연동 테스트
- 목적: 설문 완료 시 외부 패널사에서 정의한 성공 포스트백 URL로 응답자의 ID를 포함하여 정상적으로 신호가 전달되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-RT-001, #BE-RT-002

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 조사 성공 시 Success URL로 리다이렉트 확인
- [ ] 시나리오 2: URL 내 응답자 고유 ID(UID) 치환 여부 확인
- [ ] 시나리오 3: HTTP 302 응답 헤더의 `Location` 값 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 패널사로부터 받은 성공 URL `https://panel.com/complete?uid={resp_id}`
- When: 설문 응답을 완료하고 리다이렉트 API를 호출함
- Then: 브라우저가 해당 URL(UID가 실제 값으로 바뀐 상태)로 리다이렉트되어야 한다.

## :gear: Technical Constraints
- 도구: Integration Test

## :checkered_flag: Definition of Done (DoD)
- [ ] 리다이렉트 로직이 외부 패널사 연동 규격을 완벽히 충족하는가?
- [ ] 상태별(성공/실패) URL 매핑이 정확한가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RT-001 (포스트백 등록)
- Blocks: None
