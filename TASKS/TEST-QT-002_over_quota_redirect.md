---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-QT-002: Over-quota 초과 수용 오차율 검증 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-QT-002] Over-quota 초과 수용 오차율 검증 테스트
- 목적: 쿼터 목표치(예: 100명)에 도달한 즉시 추가 진입을 차단하여, 동시성 환경에서도 오차율 1% 이내(최대 101명)로 목표를 엄격히 준수하는지 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L528)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] k6 부하 테스트 스크립트 작성 (`/tests/load/quota_concurrency.js`)
- [ ] 시나리오: 목표 쿼터가 1명 남은 상태(99/100) 셋업
- [ ] 50명의 가상 유저(VU)가 동시에 `POST /api/v1/responses` 제출 시뮬레이션
- [ ] 응답 상태 코드 분석: 1명은 200 OK, 49명은 302/400 (Quota Full) 수신 여부 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 동시성 제어 및 오차율 방어
- Given: 특정 쿼터 셀의 현재 수집 수 99개, 목표 100개
- When: 50건의 응답이 1초 이내에 동시 도달
- Then: 최종 저장된 응답 수는 정확히 100개(오차 0%) 또는 최대 101개(오차 1%) 이내여야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] k6 테스트 실행 결과 `http_req_failed`가 초과 요청 분만큼 정상 발생했는지 확인
- [ ] DB 트랜잭션 데드락(Deadlock) 발생 여부 확인 (0건이어야 함)

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-003
- Blocks: None

