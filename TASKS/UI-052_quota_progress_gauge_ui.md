---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-052: 쿼터 모니터링 대시보드 프로그레스 게이지 UI 개발"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-052] 쿼터 모니터링 프로그레스 게이지 UI 개발
- 목적: 할당표(성별 x 연령 등)별로 응답 목표 수량이 얼마나 달성되었는지를 원형 프로그레스(Radial Gauge)로 미려하게 시각화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] SVG 기반의 Radial Progress 컴포넌트 설계 (진행률 퍼센트 및 `현재/목표` 텍스트 중앙 배치)
- [ ] 100% 도달 시 게이지 컬러가 초록색으로 변경되는 테마 로직

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 게이지 렌더링
- Given: 20대 남성 쿼터 (목표 100, 현재 50)
- When: 화면 렌더링
- Then: 게이지가 정확히 반(50%)만큼 채워진 상태로 출력된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 호버(Hover) 시 툴팁으로 상세 수치 제공

## :construction: Dependencies & Blockers
- Depends on: #UI-050, #FE-QT-002
- Blocks: None
