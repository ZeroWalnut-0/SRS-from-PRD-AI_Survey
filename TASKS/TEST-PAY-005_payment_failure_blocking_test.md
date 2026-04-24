---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PAY-005: 결제 실패/미결제 시 다운로드 권한 차단 테스트"
labels: 'test, backend, security, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PAY-005] 결제 실패/미결제 시 다운로드 권한 차단 테스트
- 목적: 결제가 완료되지 않았거나 실패한 상태에서 데이터 패키지 다운로드를 시도할 경우, 시스템이 이를 정확히 차단하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PAY-005 (다운로드 핸들러)
- 성공 기준: TC-FUNC-013

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: `payment_cleared = false`인 상태에서 다운로드 API 호출 시 403 에러 확인
- [ ] 시나리오 2: 로그인하지 않은 익명 사용자의 다운로드 시도 차단 확인
- [ ] 시나리오 3: 자신의 것이 아닌 타인의 패키지 다운로드 시도 차단 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 미결제 상태의 `package_id`
- When: `GET /api/v1/packages/{package_id}/download` API를 호출함
- Then: 서버는 HTTP 403 Forbidden 응답을 반환해야 하며, 서명된 URL을 노출하지 않아야 한다.

## :gear: Technical Constraints
- 도구: API Integration Test (RBAC 검증 포함)

## :checkered_flag: Definition of Done (DoD)
- [ ] 비정상적인 다운로드 시도가 100% 차단되는가?
- [ ] 에러 메시지가 보안상 취약하지 않은 형태로 제공되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-002, #BE-PAY-005
- Blocks: None
