---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-QT-005: 쿼터 100% 도달 시 Slack 알림 발송 검증 테스트"
labels: 'test, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-QT-005] 쿼터 100% 도달 시 Slack 알림 발송 검증 테스트
- 목적: 특정 쿼터 셀의 수집이 완료(100% 충족)되었을 때 관리자에게 Slack 알림이 정상적으로 전송되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-QT-004 (Slack 알림)
- 성공 기준: TC-FUNC-022

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 쿼터 목표치 도달 직전(Last response) 상황 시뮬레이션
- [ ] 시나리오 2: 마지막 응답 제출 후 `is_full = true` 변경 확인
- [ ] 시나리오 3: Slack 채널로 "쿼터 마감" 알림 전송 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 10/10 목표의 쿼터에서 마지막 응답을 제출함
- When: 백엔드 쿼터 처리 로직이 완료됨
- Then: Slack Webhook을 통해 실시간으로 해당 쿼터 그룹의 마감 소식이 통보되어야 한다.

## :gear: Technical Constraints
- 도구: Slack Webhook Mocking 또는 테스트 채널 실전송

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터 마감 소식이 누락 없이 관리자에게 전달되는가?
- [ ] 알림 메시지의 가독성이 확보되었는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-004 (Slack 알림)
- Blocks: None
