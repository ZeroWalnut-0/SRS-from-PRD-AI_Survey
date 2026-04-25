---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] TEST-F4-004: 중복 IP(IP Hash 기반) 응답 차단 테스트"
labels: 'feature, test, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-F4-004] 중복 IP 응답 차단 테스트
- 목적: 동일한 IP 주소(해시값)로부터 짧은 간격 내에 들어오는 중복 설문 응답을 탐지하여 스팸 데이터를 차단하는 로직을 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L492)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 동일한 IP 해시값을 가진 연속 제출 시뮬레이션 코드 작성
- [ ] 두 번째 제출 건에 대해 `quota_status = SCREENOUT` 판정이 내려지는지 테스트

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 중복 IP 차단 성공
- Given: 'Hash_A'로 1분 전 제출 이력이 존재함
- When: 'Hash_A'로 다시 제출 시도
- Then: 데이터 적재가 거부되거나 무효 처리된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Jest 테스트 결과 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-FORM-004, #DB-005
- Blocks: None
