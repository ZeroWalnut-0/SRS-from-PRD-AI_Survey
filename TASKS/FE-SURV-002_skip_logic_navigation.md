---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-SURV-002: 스킵 로직에 따른 다음 문항 동적 전환 로직 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-SURV-002] 스킵 로직에 따른 다음 문항 동적 전환 로직 구현
- 목적: 응답자가 선택한 보기에 할당된 스킵(분기) 로직을 해석하여 다음 페이지에 보여줄 질문 번호를 동적으로 라우팅한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L254)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 클라이언트 상태 관리 스토어 내 `currentQuestionIndex` 상태 추가
- [ ] 스킵 로직 해석 함수(`getNextQuestionIndex`) 작성
- [ ] 문항 전환 시 부드러운 Fade-in/out 애니메이션 처리 (Framer Motion 활용)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 1번 문항에서 5번으로 스킵
- Given: 1번 문항의 A 보기에 5번으로의 스킵 조건이 걸려있음
- When: 응답자가 A 보기를 선택하고 '다음' 버튼을 누름
- Then: 2, 3, 4번 문항을 건너뛰고 즉시 5번 문항 화면으로 전환된다.

## :gear: Technical & Non-Functional Constraints
- 사용성: '이전' 버튼 클릭 시 스킵했던 경로를 그대로 역추적하는 히스토리 스택 관리 필요

## :checkered_flag: Definition of Done (DoD)
- [ ] 복합 스킵 경로 시나리오 검증 통과

## :construction: Dependencies & Blockers
- Depends on: #FE-SURV-001
- Blocks: #FE-SURV-003
