---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-RT-002: 리다이렉트 URL 파라미터 치환 정확성 테스트"
labels: 'test, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-RT-002] 리다이렉트 URL 파라미터 치환 정확성 테스트
- 목적: 외부 패널사 리다이렉트 시, URL 내에 포함된 변수(예: `{resp_id}`)가 실제 데이터로 정확히 치환되어 전송되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-RT-002 (리다이렉트 핸들러)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: `resp_id` 파라미터 치환 확인 (예: `?uid={resp_id}`)
- [ ] 시나리오 2: 커스텀 파라미터 추가 시 유지 여부 확인
- [ ] 시나리오 3: URL 인코딩(URL Encoding) 처리 확인 (특수문자 포함 시)

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 리다이렉트 URL이 `https://panel.com/callback?uid={resp_id}&status=1`로 설정됨
- When: ID가 `uuid-123`인 응답자의 조사가 완료됨
- Then: 실제 리다이렉트되는 최종 URL이 `https://panel.com/callback?uid=uuid-123&status=1`과 완벽히 일치해야 한다.

## :gear: Technical Constraints
- 도구: API Integration Test

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 예약된 변수가 실제 값으로 정확히 치환되는가?
- [ ] 치환된 URL이 브라우저에서 유효하게 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RT-002 (리다이렉트 핸들러)
- Blocks: None
