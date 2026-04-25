---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-053: 수익/결제 현황 대시보드 차트 UI 개발"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-053] 수익/결제 현황 대시보드 차트 UI 개발
- 목적: 기간별 매출 추이 및 총 누적 수익 지표를 차트 형태로 한눈에 파악할 수 있도록 대시보드를 구성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `Recharts` 활용: 일별/월별 매출 막대(Bar) 차트 렌더링
- [ ] 주요 요약 스탯 카드(Total Revenue, ARPU, MAU 등) 디자인

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 차트 툴팁
- Given: 매출 차트
- When: 특정 막대 위에 마우스 포인터를 올림
- Then: "YYYY-MM-DD : 99,000원" 형태의 상세 안내 툴팁이 팝업된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 빈 차트 데이터일 경우 `No Data` 안내 표시

## :construction: Dependencies & Blockers
- Depends on: #UI-050, #FE-ADMIN-002
- Blocks: None
