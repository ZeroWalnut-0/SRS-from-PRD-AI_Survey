---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-002: 파싱 완료 레이턴시 테스트"
labels: 'test, performance, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-002] 파싱 완료 레이턴시 테스트
- 목적: 문서 업로드부터 파싱 결과 생성까지 걸리는 시간이 10초(최대 15초) 이내인지 성능을 측정한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L560)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] k6 부하 테스트 툴을 이용한 단건 처리 시간(Duration) 로깅
- [ ] 임계치(15,000ms) 초과 시 경고 발생

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 제한 시간 만족
- Given: 5MB 미만 문서
- When: 파싱 실행
- Then: 10초 이내에 `status=COMPLETED` 폴링 성공

## :checkered_flag: Definition of Done (DoD)
- [ ] p95 레이턴시 측정 지표 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005, #NFR-PERF-002
- Blocks: None
