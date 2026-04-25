---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] TEST-F4-002: 무성의 응답(패턴 반복) 탐지 알고리즘 테스트"
labels: 'feature, test, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-F4-002] 무성의 응답(패턴 반복) 탐지 알고리즘 테스트
- 목적: 동일한 번호(예: "1, 1, 1, 1...")만 반복 선택하여 불성실하게 응답한 케이스를 탐지하는 유닛 테스트를 작성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L492)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 연속 동일 응답 판별 로직(Straightlining Detector) 테스트 스위트 준비
- [ ] 임계치(예: 80% 이상 동일 번호)를 넘는 모의 응답 세트 대입 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 일렬 답변 차단
- Given: 객관식 5문항 모두 1번 보기 선택
- When: 패턴 탐지 로직 통과
- Then: 무성의 응답으로 판정되어 `SCREENOUT` 플래그가 부여된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 단위 테스트 Pass 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-FORM-004
- Blocks: None
