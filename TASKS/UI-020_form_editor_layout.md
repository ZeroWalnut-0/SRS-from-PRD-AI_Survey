---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-020: 폼 에디터 메인 화면 3단 레이아웃 마크업"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-020] 폼 에디터 메인 화면 3단 레이아웃 마크업
- 목적: 문항 추가/삭제, 순서 변경 및 실시간 피드백이 동시에 이루어지는 강력한 설문 제작 워크스페이스 UI를 구축한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 좌측: 문항 개요 및 네비게이션 패널
- [ ] 중앙: 실제 문항 카드들이 나열되는 캔버스 영역
- [ ] 우측: 선택된 문항의 세부 옵션(필수 여부, 보기 편집 등) 패널

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 패널 접기(Collapse)
- Given: 3단 레이아웃 에디터
- When: 좌측 패널 접기 아이콘 클릭
- Then: 좌측 영역이 사라지며 중앙 캔버스가 넓어진다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 스크롤 영역(Independent Scroll)의 정상 작동 확인

## :construction: Dependencies & Blockers
- Depends on: #UI-001
- Blocks: #FE-FORM-001
