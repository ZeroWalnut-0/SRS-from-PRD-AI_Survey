---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PAY-004: 결제 성공 콜백 및 서명 URL 발급 흐름 테스트"
labels: 'test, backend, integration, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PAY-004] 결제 성공 콜백 및 서명 URL 발급 흐름 테스트
- 목적: PG사로부터 결제 성공 신호를 받았을 때, DB 상태 갱신부터 최종 다운로드용 서명 URL 발급까지의 전체 파이프라인이 정상 작동하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PAY-002 (콜백), #BE-PAY-004 (서명 URL)
- 성공 기준: TC-FUNC-011, 012

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 정상 결제 승인 콜백 수신 시 `payment_cleared = true` 갱신 확인
- [ ] 시나리오 2: 승인 직후 `ZIP_DATAMAP.download_url`에 서명된 URL이 생성되는지 확인
- [ ] 시나리오 3: 중복된 콜백 수신 시 멱등성(Idempotency) 보장 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 대기 중인 결제 세션 (status = PENDING)
- When: PG사 가상 승인 콜백(POST /api/v1/payments/callback)을 전송함
- Then: DB 레코드가 SUCCESS로 변경되어야 하며, 반환된 URL로 실제 Storage 파일 접근이 가능해야 한다.

## :gear: Technical Constraints
- 도구: Supertest + Supabase Admin SDK

## :checkered_flag: Definition of Done (DoD)
- [ ] 결제 승인 후 데이터 패키지 다운로드가 즉시 활성화되는가?
- [ ] 발급된 URL이 지정된 시간 동안만 유효한가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-002 (결제 콜백), #BE-PAY-004
- Blocks: None
