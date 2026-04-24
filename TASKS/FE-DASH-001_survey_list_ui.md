---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-DASH-001: 설문 목록 및 통합 대시보드 UI 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-DASH-001] 설문 목록 및 통합 대시보드 UI 구현
- 목적: 사용자가 자신이 생성한 모든 설문 목록을 확인하고, 전체적인 진행 상태(수집 중, 완료 등)를 한눈에 파악할 수 있는 메인 대시보드를 구축한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-024`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- UI 컴포넌트: `shadcn/ui` (Table, Card, Badge)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/page.tsx` 또는 `app/(dashboard)/surveys/page.tsx` 생성
- [ ] 설문 목록 테이블 구현 (제목, 생성일, 상태, 응답 수, 액션 버튼)
- [ ] 상태별 필터링 기능 추가 (전체, 수집 중, 완료)
- [ ] 설문 요약 카드 구현 (총 설문 수, 오늘 수집된 응답 수 등)
- [ ] [새 설문 만들기] 플로팅 버튼 또는 히어로 섹션 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 목록 조회
- Given: 사용자가 로그인하여 대시보드에 진입함
- When: 설문 목록 데이터가 로드됨
- Then: 자신이 생성한 설문들이 최신순으로 표시되어야 하며, 각 설문의 현재 상태가 배지로 표시되어야 한다.

Scenario 2: 상태 필터링 작동
- Given: 여러 상태의 설문이 혼재함
- When: '수집 중' 필터를 클릭함
- Then: 현재 `PUBLISHED` 상태인 설문들만 목록에 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 목록 조회 및 렌더링 레이턴시 ≤ 300ms.
- UX: 데이터가 없는 경우 "첫 설문을 만들어보세요"와 같은 공백 페이지(Empty State)를 제공한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 설문 목록 및 요약 카드가 디자인대로 구현되었는가?
- [ ] 상태 필터링 및 정렬 기능이 작동하는가?
- [ ] 개별 설문 상세 페이지로의 이동이 정상적인가?

## :construction: Dependencies & Blockers
- Depends on: #BE-DASH-002 (목록 조회 API)
- Blocks: None
