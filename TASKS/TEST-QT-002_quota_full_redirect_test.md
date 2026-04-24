---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-QT-002: 쿼터 마감 오차율 및 리다이렉트 검증 테스트"
labels: 'test, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-QT-002] 쿼터 마감 오차율 및 리다이렉트 검증 테스트
- 목적: 목표 쿼터가 가득 찼을 때, 추가 응답자가 정확히 차단(QUOTAFULL 리다이렉트)되는지 확인하고, 동시 접속 상황에서도 오차율이 1% 이내인지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-019`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 관련 태스크: #BE-QT-003 (원자적 쿼터 증가)

## :white_check_mark: Test Scenarios (검증 시나리오)
- [ ] `tests/load/quota.concurrency.test.ts` 부하 테스트 스크립트 작성
- [ ] 시나리오 1: 목표 쿼터(예: 100명)에 도달하기 직전(99명) 상황 시뮬레이션
- [ ] 시나리오 2: 동시 50명이 마지막 1자리를 두고 경쟁하는 상황 (Race Condition 테스트)
- [ ] 시나리오 3: 쿼터 마감 후 진입하는 응답자가 `status: 'QUOTAFULL'` 응답을 받는지 확인
- [ ] 시나리오 4: 마감 후 DB의 `current_count`가 `target_count`를 초과하지 않았는지 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 목표 쿼터가 100명인 설문
- When: 150명의 가상 사용자가 동시에 응답을 제출함
- Then: 최종 성공 응답자는 정확히 100명이어야 하며, 나머지 50명은 `QUOTAFULL` 리다이렉트 경로로 안내되어야 한다. (오차 1% 이내)

## :gear: Technical & Non-Functional Constraints
- 도구: k6 또는 Artillery를 활용한 동시성 테스트 (REQ-NF-013)
- 데이터: `DB-012` RPC 함수를 직접 호출하여 원자성 레벨 검증

## :checkered_flag: Definition of Done (DoD)
- [ ] 동시 접속 상황에서도 쿼터 초과 응답자가 발생하지 않는가?
- [ ] 쿼터 마감 감지 레이턴시가 1초 이내인가?
- [ ] 리다이렉트 정보가 응답자에게 정확히 전달되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-003 (원자적 쿼터 증가), #DB-012 (Supabase RPC)
- Blocks: #TEST-QT-003 (동시성 데드락 테스트)
