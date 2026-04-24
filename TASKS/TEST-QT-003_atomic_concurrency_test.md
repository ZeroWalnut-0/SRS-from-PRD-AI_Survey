---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-QT-003: 쿼터 카운트 원자성 및 동시성 스트레스 테스트"
labels: 'test, backend, performance, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-QT-003] 쿼터 카운트 원자성 및 동시성 스트레스 테스트
- 목적: 수백 명의 응답자가 동시에 동일한 쿼터 셀에 응답을 제출할 때, DB의 카운트가 목표치를 초과하지 않고 정확히 원자적으로 증가하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #DB-012 (Supabase RPC), #BE-QT-003 (원자적 증가 로직)
- 기술 요구사항: 동시성 오차율 0% (REQ-FUNC-020)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 100명의 가상 사용자가 목표치 50인 셀에 동시 제출 시도
- [ ] 시나리오 2: 목표 도달 직후(Last Mile)의 동시 요청 차단 확인
- [ ] 시나리오 3: 네트워크 지연 상황에서의 DB 락(Lock) 경합 및 성능 측정

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 특정 쿼터 셀의 `target_count`가 50으로 설정됨
- When: 100건의 응답 요청을 동시에(0.1초 이내) 쏟아부음
- Then: 최종 `current_count`는 정확히 50이어야 하며, 51번째 이후의 요청은 모두 실패(Quota Full) 처리되어야 한다.

## :gear: Technical Constraints
- 도구: k6 (Load Testing Tool)
- 환경: Supabase PostgreSQL 실환경 (RPC 호출 위주)

## :checkered_flag: Definition of Done (DoD)
- [ ] 동시성 상황에서 쿼터 초과 수집 사례가 발견되지 않는가?
- [ ] 원자적 연산(`increment_quota_cell`)의 성공률이 100%인가?

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-003 (원자적 증가), #DB-012 (RPC)
- Blocks: None
