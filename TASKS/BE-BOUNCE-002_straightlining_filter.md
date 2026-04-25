---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-BOUNCE-002: Straightlining (한 번호로 밀기) 필터 로직 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-BOUNCE-002] Straightlining 필터 로직 구현
- 목적: 객관식 문항들에 대하여 고민 없이 하나의 번호(예: 전부 3번)만 계속 찍고 넘어간 패턴을 감지하여 불량 응답으로 분류한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 품질 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L590)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 제출된 JSON 응답 배열 내 객관식 보기 번호의 연속성/동일성 패턴 스캔 알고리즘 작성
- [ ] 연속 동일 응답 개수 임계치(예: 10개 연속) 초과 시 필터링

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 일렬 밀기 탐지
- Given: 1~15번 문항의 답이 모두 '4'인 응답
- When: 유효성 검사 수행
- Then: `RESPONSE.status = 'BOUNCED'` 처리 및 사유 'STRAIGHTLINING' 기록.

## :checkered_flag: Definition of Done (DoD)
- [ ] 역채점(Reverse-coded) 문항이 포함된 경우의 탐지 정확성 검토

## :construction: Dependencies & Blockers
- Depends on: #BE-FORM-004, #DB-005
- Blocks: #FE-FORM-008
