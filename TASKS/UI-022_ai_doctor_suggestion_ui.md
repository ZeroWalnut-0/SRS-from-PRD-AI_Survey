---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-022: AI 주치의 제안 배지 및 팝오버 모달 UI 개발"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-022] AI 주치의 제안 배지 및 팝오버 모달 UI
- 목적: AI가 감지한 설문 문항의 보완점(예: 편향된 어휘, 모호한 선택지)을 유저에게 친절하게 제안하는 UI 요소들을 배치한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 문항 카드 우측 상단에 'AI 추천' 플로팅 배지(Badge) 배치
- [ ] 배지 클릭 시 상세 피드백과 '적용하기' 버튼이 있는 Popover UI 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 피드백 팝오버 오픈
- Given: 경고 배지가 노출된 문항
- When: 배지 호버(Hover) 또는 클릭
- Then: AI의 수정 제안 문장이 팝업 형태로 매끄럽게 떠오른다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모달 외 영역 클릭 시 닫힘(Close) 기능

## :construction: Dependencies & Blockers
- Depends on: #UI-021, #FE-PARSE-007
- Blocks: None
