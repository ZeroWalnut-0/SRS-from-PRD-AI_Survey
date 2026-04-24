---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PAY-003: 다운로드 권한 및 URL 만료 보안 테스트"
labels: 'test, backend, security, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PAY-003] 다운로드 권한 및 URL 만료 보안 테스트
- 목적: 결제되지 않은 사용자의 접근을 차단하고, 발급된 서명된 URL이 일정 시간 후 정확히 만료되는지 보안 관점에서 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PAY-004 (서명된 URL)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 미결제 계정으로 다운로드 API 호출 시 403 에러 확인
- [ ] 시나리오 2: 서명된 URL 발급 후 5분 경과 시 접근 차단 확인
- [ ] 시나리오 3: 타인의 결제 건에 대해 URL 발급 시도 시 차단 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 5분 유효기간의 서명된 URL이 발급됨
- When: 5분 1초가 경과한 시점에 해당 URL로 접속함
- Then: Storage 서버로부터 `Access Denied` 또는 `Expired` 에러를 받아야 한다.

## :gear: Technical Constraints
- 도구: Integration Test (Wait & Retry)

## :checkered_flag: Definition of Done (DoD)
- [ ] 미인증/미결제 접근이 100% 차단되는가?
- [ ] URL 만료 정책이 정확히 적용되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-004 (서명 URL), #BE-PAY-005 (다운로드 핸들러)
- Blocks: None
