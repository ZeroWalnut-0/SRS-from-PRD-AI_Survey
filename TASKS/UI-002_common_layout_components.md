---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-002: 공통 레이아웃 컴포넌트(GNB, 네비게이션) 개발"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-002] 공통 레이아웃 컴포넌트 개발
- 목적: 웹 전반에 사용될 Global Navigation Bar(상단) 및 모바일 해상도 대응을 위한 Bottom Navigation 구조를 완성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 데스크톱 뷰: 상단 고정 GNB (로고, 메뉴 목록, 마이페이지 아이콘)
- [ ] 모바일 뷰 (≤ 768px): 하단 고정 탭 바 UI 분기 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 반응형 분기
- Given: 브라우저 너비 1024px
- When: 너비를 375px로 축소
- Then: GNB가 사라지고 모바일 전용 하단 탭 바가 노출된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Next.js `Link` 태그를 통한 클라이언트 사이드 네비게이션 확인

## :construction: Dependencies & Blockers
- Depends on: #UI-001
- Blocks: #UI-003
