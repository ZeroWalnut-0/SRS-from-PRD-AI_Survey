---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-008: Rate Limit 초과 예외 테스트"
labels: 'test, infrastructure, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-008] Rate Limit 초과 예외 테스트
- 목적: 무료 계정 조건에서 하루 3회를 초과하여 4번째 파싱을 시도할 때, API가 HTTP 429 상태 코드를 정확히 반환하는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L543)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 동일 IP 또는 유저 ID로 단시간 내 4회 연속 업로드 요청
- [ ] 4번째 요청의 HTTP Status 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 4회차 차단
- Given: 금일 파싱 3회 완료
- When: 4회차 업로드
- Then: 응답 코드 429 및 "일일 파싱 한도 초과" 메시지 리턴

## :checkered_flag: Definition of Done (DoD)
- [ ] 24시간 경과 후 한도가 초기화되어 다시 파싱 가능한지 Time-travel 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-RL-001
- Blocks: None
